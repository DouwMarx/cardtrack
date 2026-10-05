#!/usr/bin/env python3
"""The agent's append channel for logs/friction.jsonl and logs/PROPOSALS.md.

Why a script: the sandboxed agent has no shell redirection, so before this existed
it either rewrote the whole file through its Edit tool or left "pending" copies in
logs/ that got committed (2026-09-21). This is the single audited append path; it
also stamps run_id and keeps `kind` to a fixed vocabulary so the log can be
counted instead of read.

  log_note.py friction --kind KIND --detail TEXT [--url U] [--slug S] [--recurrence-of TS]
  log_note.py proposal --title TITLE (--body TEXT | --body-file PATH)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo, utcnow  # noqa: E402

# One value per root cause the pipeline can act on. `recurrence` is for a problem
# already in the log (point at it with --recurrence-of); `regression` is for one
# listed as fixed in logs/RESOLVED.md. Anything else is `other` with a clear detail.
KINDS = {
    "unfetchable_agent_side": "the agent's own fetch tool fails on a URL Phase A reads fine",
    "transient_rejection": "validator rejected on a 429/5xx/timeout that later cleared",
    "ambiguous_criteria": "criteria.yaml or TASK.md gives no answer for a document class",
    "tooling": "a sandbox/allowlist/CLI limitation cost turns",
    "diff_noise": "a stored version is page furniture, not a content change",
    "index_gap": "a real release was not in candidates.json (index page lag, stale URL)",
    "cap": "a cap stopped an in-scope write",
    "data_error": "a wrong field, slug, URL or status in the database",
    "schema_gap": "no doc_type/field/vocabulary for a document class",
    "recurrence": "an obstacle already logged; cite it with --recurrence-of",
    "regression": "a problem logs/RESOLVED.md lists as fixed came back",
    "other": "none of the above (say why in detail)",
}
MAX_DETAIL = 1500  # a diary entry is a proposal; keep the log countable


def append_friction(repo: Repo, args: argparse.Namespace) -> dict:
    if args.kind not in KINDS:
        return {"status": "error", "reason": f"kind must be one of: {', '.join(KINDS)}"}
    detail = args.detail.strip()
    if not detail:
        return {"status": "error", "reason": "detail is empty"}
    if len(detail) > MAX_DETAIL:
        return {"status": "error",
                "reason": f"detail is {len(detail)} chars; max {MAX_DETAIL}. Put the long "
                          "form in a proposal (log_note.py proposal) and cite it here."}
    if args.kind == "recurrence" and not args.recurrence_of:
        return {"status": "error", "reason": "kind=recurrence needs --recurrence-of <ts>"}
    entry = {"ts": utcnow(), "run_id": os.environ.get("CARDTRACK_RUN_ID", ""),
             "kind": args.kind, "detail": detail}
    for key in ("url", "slug", "recurrence_of"):
        if getattr(args, key):
            entry[key] = getattr(args, key)
    path = repo.logs_dir / "friction.jsonl"
    _append(path, json.dumps(entry, ensure_ascii=False) + "\n")
    return {"status": "ok", "file": str(path.relative_to(repo.root)), "ts": entry["ts"]}


def append_proposal(repo: Repo, args: argparse.Namespace) -> dict:
    title = args.title.strip()
    if not title:
        return {"status": "error", "reason": "title is empty"}
    body = Path(args.body_file).read_text(encoding="utf-8") if args.body_file else args.body
    body = (body or "").strip()
    if not body:
        return {"status": "error", "reason": "body is empty"}
    date = utcnow()[:10]
    section = f"---\n\n## {date} — {title}\n\n{body}\n\n"
    path = repo.logs_dir / "PROPOSALS.md"
    _append(path, section)
    return {"status": "ok", "file": str(path.relative_to(repo.root)),
            "heading": f"{date} — {title}"}


def _append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Make sure the new record starts on its own line even if the file's last write
    # (a human edit, an older agent) left no trailing newline.
    needs_nl = path.exists() and path.stat().st_size > 0 and not path.read_bytes().endswith(b"\n")
    with open(path, "a", encoding="utf-8") as f:
        if needs_nl:
            f.write("\n")
        f.write(text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    sub = p.add_subparsers(dest="target", required=True)

    f = sub.add_parser("friction", help="append one JSON line to logs/friction.jsonl",
                       description="kinds:\n" + "\n".join(f"  {k:24} {v}"
                                                           for k, v in KINDS.items()),
                       formatter_class=argparse.RawDescriptionHelpFormatter)
    f.add_argument("--kind", required=True, choices=sorted(KINDS), metavar="KIND")
    f.add_argument("--detail", required=True, help=f"plain text, max {MAX_DETAIL} chars")
    f.add_argument("--url", help="the URL this is about, if any")
    f.add_argument("--slug", help="the stored document this is about, if any")
    f.add_argument("--recurrence-of", help="ts of the earlier friction entry this repeats")

    q = sub.add_parser("proposal", help="append a dated section to logs/PROPOSALS.md")
    q.add_argument("--title", required=True)
    q.add_argument("--body", help="markdown body (problem, suggested change, evidence)")
    q.add_argument("--body-file", help="read the body from this file instead")

    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    if args.target == "friction":
        out = append_friction(repo, args)
    else:
        if bool(args.body) == bool(args.body_file):
            out = {"status": "error", "reason": "exactly one of --body/--body-file"}
        else:
            out = append_proposal(repo, args)
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
