#!/usr/bin/env python3
"""Deliver queued issues (logs/issues_outbox.jsonl) and issue comments
(logs/comments_outbox.jsonl) to GitHub via gh. Runs OUTSIDE the agent sandbox
(run_daily.sh Phase C), where gh is authenticated — inside the sandbox gh has no
credentials, so both channels queue here.

Every record passes the deterministic secret scan first; records with findings are
diverted to *.held.jsonl and never posted. Delivered records move to *.sent.jsonl;
failures stay queued for the next run."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.changelog import log as changelog_log  # noqa: E402
from cardtrack.db import connect  # noqa: E402
from cardtrack.repo import Repo, utcnow  # noqa: E402
from scripts.secret_scan import load_secret_values, scan_bytes  # noqa: E402


def _read_outbox(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _write_outbox(path: Path, records: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _append(path: Path, rec: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _gh(cmd: list[str], stdin: str | None = None):
    try:
        return subprocess.run(cmd, input=stdin, capture_output=True, text=True,
                              timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)

    gh_repo = repo.setting("github.repo") or ""
    use_gh = bool(repo.setting("github.use_gh", True))
    if not (gh_repo and use_gh and shutil.which("gh")):
        print(json.dumps({"status": "not_configured", "delivered": 0}))
        return 0

    secret_values = load_secret_values(repo)
    summary = {"status": "ok", "delivered": 0, "comments_delivered": 0,
               "held": 0, "remaining": 0}

    # ---- issues ----
    outbox = repo.logs_dir / "issues_outbox.jsonl"
    remaining = []
    for rec in _read_outbox(outbox):
        text = (rec.get("title", "") + "\n" + rec.get("body", "")).encode()
        if scan_bytes(text, "issues_outbox", secret_values):
            _append(repo.logs_dir / "issues_outbox.held.jsonl",
                    {**rec, "held_at": utcnow(), "held_reason": "secret_scan"})
            summary["held"] += 1
            continue
        cmd = ["gh", "issue", "create", "-R", gh_repo,
               "--title", rec["title"], "--body", rec["body"]]
        for label in rec.get("labels", []):
            cmd += ["--label", label]
        proc = _gh(cmd)
        if proc and proc.returncode == 0:
            rec["delivered_at"] = utcnow()
            rec["issue_url"] = proc.stdout.strip().splitlines()[-1] if proc.stdout else ""
            _append(repo.logs_dir / "issues_outbox.sent.jsonl", rec)
            summary["delivered"] += 1
        else:
            remaining.append(rec)
    _write_outbox(outbox, remaining)
    summary["remaining"] += len(remaining)

    # ---- issue comments ----
    coutbox = repo.logs_dir / "comments_outbox.jsonl"
    cremaining = []
    for rec in _read_outbox(coutbox):
        if scan_bytes(rec.get("body", "").encode(), "comments_outbox", secret_values):
            _append(repo.logs_dir / "comments_outbox.held.jsonl",
                    {**rec, "held_at": utcnow(), "held_reason": "secret_scan"})
            summary["held"] += 1
            continue
        proc = _gh(["gh", "issue", "comment", str(rec["issue"]), "-R", gh_repo,
                    "--body-file", "-"], stdin=rec["body"])
        if proc and proc.returncode == 0:
            if rec.get("resolve"):
                _gh(["gh", "issue", "edit", str(rec["issue"]), "-R", gh_repo,
                     "--add-label", "resolved"])
                conn = connect(repo.db_path)
                try:
                    changelog_log(conn, os.environ.get("CARDTRACK_RUN_ID", "flush"),
                                  "issue_resolved", None,
                                  {"issue": rec["issue"], "body": rec["body"][:1000],
                                   "actor": "flush_outbox"})
                    conn.commit()
                finally:
                    conn.close()
            rec["delivered_at"] = utcnow()
            _append(repo.logs_dir / "comments_outbox.sent.jsonl", rec)
            summary["comments_delivered"] += 1
        else:
            cremaining.append(rec)
    _write_outbox(coutbox, cremaining)
    summary["remaining"] += len(cremaining)

    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
