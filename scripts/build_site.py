#!/usr/bin/env python3
"""Phase C site builder CLI: DB → site/ (pages, metadata.json, Pagefind index).
--emit-commit-msg renders the run's changelog rows as a commit message (the JSON
in the changelog table stays canonical; the message is a view of it)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.changelog import render_commit_message  # noqa: E402
from cardtrack.db import connect  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402
from cardtrack.sitebuild import build_site  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--no-pagefind", action="store_true", help="skip the Pagefind index step")
    p.add_argument("--emit-commit-msg", metavar="RUN_ID",
                   help="print the commit message for a run's changelog rows and exit")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)

    if args.emit_commit_msg:
        conn = connect(repo.db_path)
        try:
            print(render_commit_message(conn, args.emit_commit_msg), end="")
        finally:
            conn.close()
        return 0

    summary = build_site(repo, run_pagefind=False if args.no_pagefind else None)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
