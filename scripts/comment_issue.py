#!/usr/bin/env python3
"""The only route to GitHub issue comments, for agent and human alike.
Every comment is logged to logs/comments.jsonl; without a configured repo (or gh),
comments land in the outbox log instead of GitHub."""

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
    if len(body) > 8000:
        # tripwire, not a style rule: a paragraph never hits this; a dumped file does
        print(json.dumps({"status": "error", "reason": "body exceeds 8000 characters"}))
        return 2

    repo = Repo.locate(args.root)
    repo.logs_dir.mkdir(parents=True, exist_ok=True)
    gh_repo = repo.setting("github.repo") or ""
    use_gh = bool(repo.setting("github.use_gh", True))

    # Agent-authored comments NEVER post directly, even where gh happens to be
    # authenticated (human terminal, or CARDTRACK_NO_SANDBOX=1): they queue to the
    # outbox and pass flush_outbox.py's secret scan first. The gate is the actor,
    # not the sandbox, so a relaxed sandbox can't open an unscanned channel.
    is_agent = os.environ.get("CARDTRACK_ACTOR") == "agent"
    delivered = False
    detail = ""
    if gh_repo and use_gh and shutil.which("gh") and not is_agent:
        cmd = ["gh", "issue", "comment", str(args.issue), "-R", gh_repo, "--body-file", "-"]
        proc = subprocess.run(cmd, input=body, capture_output=True, text=True, timeout=60)
        delivered = proc.returncode == 0
        detail = (proc.stdout or proc.stderr).strip()[-500:]
        if delivered and args.resolve:
            subprocess.run(["gh", "issue", "edit", str(args.issue), "-R", gh_repo,
                            "--add-label", "resolved"],
                           capture_output=True, text=True, timeout=60)

    if delivered and args.resolve:
        conn = connect(repo.db_path)
        try:
            changelog_log(conn, os.environ.get("CARDTRACK_RUN_ID", "manual"),
                          "issue_resolved", None,
                          {"issue": args.issue, "body": body[:1000],
                           "actor": os.environ.get("CARDTRACK_ACTOR", "human")})
            conn.commit()
        finally:
            conn.close()

    if not delivered:
        # gh is unauthenticated inside the sandbox by design: queue for
        # flush_outbox.py, which posts OUTSIDE the sandbox after the secret scan.
        # (Before 2026-08-31 undelivered comments were only logged and silently
        # never reached GitHub.)
        with open(repo.logs_dir / "comments_outbox.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": utcnow(), "issue": args.issue, "body": body,
                                "resolve": args.resolve}, ensure_ascii=False) + "\n")

    with open(repo.logs_dir / "comments.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": utcnow(), "issue": args.issue, "body": body,
                            "delivered": delivered, "resolve": args.resolve,
                            "detail": detail}, ensure_ascii=False) + "\n")

    print(json.dumps({"status": "commented" if delivered else "queued",
                      "issue": args.issue}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
