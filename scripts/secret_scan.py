#!/usr/bin/env python3
"""Deterministic secret scan over outbound artifacts, run OUTSIDE the agent sandbox
before anything is committed, pushed, deployed, or posted (run_daily.sh Phase C and
flush_outbox.py). High-precision patterns only — normal curation prose never trips
them — plus exact-match against the live local secret values (.env and the Claude
credential file), which catches literal leaks with zero false positives.

Findings never include the matched secret itself, only pattern name + location.
Exit codes: 0 = clean, 3 = findings (callers fail closed).
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo, utcnow  # noqa: E402

PATTERNS = [
    ("anthropic_api_key", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("openai_style_key", re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{36,}")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("oauth_token_json", re.compile(r'"(accessToken|refreshToken)"\s*:\s*"[^"]{16,}"')),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
]

SCAN_SUFFIXES = {".md", ".json", ".jsonl", ".txt", ".html", ".sqlite", ".csv", ".yaml"}


def load_secret_values(repo: Repo) -> list[bytes]:
    """Literal secret values currently on this machine: .env values and the tokens
    in the Claude credential file. Loaded only into this process for matching;
    never logged, never included in findings."""
    values: list[bytes] = []
    env_path = repo.root / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                v = line.split("=", 1)[1].strip().strip("'\"")
                if len(v) >= 12:
                    values.append(v.encode())
    cred_path = Path.home() / ".claude" / ".credentials.json"
    if cred_path.exists():
        try:
            def collect(node):
                if isinstance(node, dict):
                    for v in node.values():
                        collect(v)
                elif isinstance(node, str) and len(node) >= 16:
                    values.append(node.encode())
            collect(json.loads(cred_path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass
    return values


def scan_bytes(data: bytes, source: str, secret_values: list[bytes],
               literal_only: bool = False) -> list[dict]:
    findings = []
    for value in secret_values:
        if value in data:
            findings.append({"source": source, "pattern": "literal_local_secret"})
            break
    if literal_only:
        # exact-match against real local secret values only: zero false positives,
        # so safe to run over third-party document text (site/, data/text/) where
        # an example token in an API doc would trip the heuristic regexes
        return findings
    text = data.decode("utf-8", errors="replace")
    for name, pattern in PATTERNS:
        if pattern.search(text):
            findings.append({"source": source, "pattern": name})
    return findings


def scan_paths(repo: Repo, paths: list[Path], literal_only: bool = False) -> list[dict]:
    secret_values = load_secret_values(repo)
    findings: list[dict] = []
    for base in paths:
        files = [base] if base.is_file() else [
            f for f in sorted(base.rglob("*"))
            if f.is_file() and f.suffix in SCAN_SUFFIXES
            and "pagefind" not in f.parts and "raw" not in f.parts
            and "agent-transcripts" not in f.parts
            # quarantine artifacts are EXPECTED to contain the held secrets;
            # they are gitignored and must not re-trip the scan forever
            and ".held" not in f.name and f.name != "SECURITY_HOLD.md"
        ]
        for f in files:
            try:
                findings.extend(scan_bytes(f.read_bytes(), str(f), secret_values,
                                           literal_only))
            except OSError:
                continue
            if f.suffix == ".sqlite":
                # also scan the logical dump: a secret straddling a SQLite
                # page/overflow boundary is split by page headers in raw bytes
                try:
                    con = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
                    try:
                        dump = "\n".join(con.iterdump()).encode()
                    finally:
                        con.close()
                except sqlite3.Error:
                    continue
                findings.extend(scan_bytes(dump, f"{f} (logical dump)",
                                           secret_values, literal_only))
    return findings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--literal-only", action="store_true",
                   help="only exact-match against live local secret values (no "
                        "heuristic regexes) — safe over third-party document text")
    p.add_argument("paths", nargs="+", help="files or directories to scan")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    findings = scan_paths(repo, [Path(x) for x in args.paths], args.literal_only)
    if findings:
        repo.logs_dir.mkdir(parents=True, exist_ok=True)
        hold = repo.logs_dir / "SECURITY_HOLD.md"
        with open(hold, "a", encoding="utf-8") as f:
            f.write(f"\n## {utcnow()} secret_scan findings\n")
            for x in findings:
                f.write(f"- {x['pattern']} in {x['source']}\n")
            f.write("Publishing was held. Inspect the files, clean or discard the "
                    "affected content, delete this section, and rerun.\n")
        print(json.dumps({"status": "findings", "count": len(findings),
                          "findings": findings}))
        return 3
    print(json.dumps({"status": "clean"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
