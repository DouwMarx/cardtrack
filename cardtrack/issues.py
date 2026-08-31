"""Issue filing: GitHub when configured, otherwise a local outbox file.

The outbox (logs/issues_outbox.jsonl) keeps the when_uncertain=file_issue policy
functional before the public repo exists, and in tests.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

from .repo import Repo, utcnow


def file_issue(repo: Repo, title: str, body: str, labels: list[str]) -> str:
    """Returns an issue reference: a GitHub URL, or 'outbox:<line>' in outbox mode."""
    gh_repo = repo.setting("github.repo") or ""
    use_gh = bool(repo.setting("github.use_gh", True))
    # Agent-filed issues always queue to the outbox (scanned by flush_outbox before
    # delivery); only non-agent callers may post directly. Gate on actor, not
    # sandbox, so a relaxed sandbox never opens an unscanned channel.
    is_agent = os.environ.get("CARDTRACK_ACTOR") == "agent"
    if gh_repo and use_gh and shutil.which("gh") and not is_agent:
        cmd = ["gh", "issue", "create", "-R", gh_repo, "--title", title, "--body", body]
        for label in labels:
            cmd += ["--label", label]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout.strip().splitlines()[-1]
        except (subprocess.TimeoutExpired, OSError):
            pass
        # fall through to outbox on any gh failure

    repo.logs_dir.mkdir(parents=True, exist_ok=True)
    outbox = repo.logs_dir / "issues_outbox.jsonl"
    record = {"ts": utcnow(), "title": title, "body": body, "labels": labels}
    with open(outbox, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    with open(outbox, encoding="utf-8") as f:
        line_no = sum(1 for _ in f)
    return f"outbox:{line_no}"
