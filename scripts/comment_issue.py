#!/usr/bin/env python3
"""The only route to GitHub issue comments, for agent and human alike.
Every comment is logged to logs/comments.jsonl; without a configured repo (or gh),
comments land in the outbox log instead of GitHub."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.changelog import log as changelog_log  # noqa: E402
from cardtrack.db import connect  # noqa: E402
from cardtrack.repo import Repo, utcnow  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--issue", required=True, type=int, help="issue number")
    p.add_argument("--body", help="comment body")
    p.add_argument("--body-file", help="file containing the comment body ('-' for stdin)")
    p.add_argument("--resolve", action="store_true",
                   help="also add the 'resolved' label (humans close issues)")
    args = p.parse_args(argv)

    if bool(args.body) == bool(args.body_file):
        print(json.dumps({"status": "error", "reason": "exactly one of --body/--body-file"}))
        return 2
    if args.body_file:
        body = sys.stdin.read() if args.body_file == "-" else Path(args.body_file).read_text()
    else:
        body = args.body
    if not body.strip():
        print(json.dumps({"status": "error", "reason": "empty body"}))
        return 2

    repo = Repo.locate(args.root)
    repo.logs_dir.mkdir(parents=True, exist_ok=True)
    gh_repo = repo.setting("github.repo") or ""
    use_gh = bool(repo.setting("github.use_gh", True))

    delivered = False
    detail = ""
    if gh_repo and use_gh and shutil.which("gh"):
        cmd = ["gh", "issue", "comment", str(args.issue), "-R", gh_repo, "--body-file", "-"]
        proc = subprocess.run(cmd, input=body, capture_output=True, text=True, timeout=60)
        delivered = proc.returncode == 0
        detail = (proc.stdout or proc.stderr).strip()[-500:]
        if delivered and args.resolve:
            subprocess.run(["gh", "issue", "edit", str(args.issue), "-R", gh_repo,
                            "--add-label", "resolved"],
                           capture_output=True, text=True, timeout=60)

    if delivered and args.resolve:
        import os
        conn = connect(repo.db_path)
        try:
            changelog_log(conn, os.environ.get("CARDTRACK_RUN_ID", "manual"),
                          "issue_resolved", None,
                          {"issue": args.issue, "body": body[:1000],
                           "actor": os.environ.get("CARDTRACK_ACTOR", "human")})
            conn.commit()
        finally:
            conn.close()

    with open(repo.logs_dir / "comments.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": utcnow(), "issue": args.issue, "body": body,
                            "delivered": delivered, "resolve": args.resolve,
                            "detail": detail}, ensure_ascii=False) + "\n")

    print(json.dumps({"status": "commented" if delivered else "logged_only",
                      "issue": args.issue}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
