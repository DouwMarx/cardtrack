#!/usr/bin/env python3
"""Deliver queued issues from logs/issues_outbox.jsonl to GitHub via gh.
Runs OUTSIDE the agent sandbox (run_daily.sh Phase C), where gh is authenticated.
Delivered records move to issues_outbox.sent.jsonl; failures stay queued."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo, utcnow  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    outbox = repo.logs_dir / "issues_outbox.jsonl"
    sent_path = repo.logs_dir / "issues_outbox.sent.jsonl"

    gh_repo = repo.setting("github.repo") or ""
    use_gh = bool(repo.setting("github.use_gh", True))
    if not outbox.exists():
        print(json.dumps({"status": "empty", "delivered": 0}))
        return 0
    if not (gh_repo and use_gh and shutil.which("gh")):
        print(json.dumps({"status": "not_configured", "delivered": 0}))
        return 0

    remaining, delivered = [], 0
    with open(outbox, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    for rec in records:
        cmd = ["gh", "issue", "create", "-R", gh_repo,
               "--title", rec["title"], "--body", rec["body"]]
        for label in rec.get("labels", []):
            cmd += ["--label", label]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except (subprocess.TimeoutExpired, OSError):
            proc = None
        if proc and proc.returncode == 0:
            rec["delivered_at"] = utcnow()
            rec["issue_url"] = proc.stdout.strip().splitlines()[-1] if proc.stdout else ""
            with open(sent_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            delivered += 1
        else:
            remaining.append(rec)

    with open(outbox, "w", encoding="utf-8") as f:
        for rec in remaining:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "ok", "delivered": delivered, "remaining": len(remaining)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
