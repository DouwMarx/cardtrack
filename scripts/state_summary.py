#!/usr/bin/env python3
"""Compact known-state JSON for the agent's context: every document's
(slug, publisher, doc_type, model_names, canonical_url, status) plus counts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.db import connect  # noqa: E402
from cardtrack.repo import Repo, utcnow  # noqa: E402


def build_summary(repo: Repo) -> dict:
    conn = connect(repo.db_path)
    try:
        docs = []
        for row in conn.execute(
            "SELECT slug, publisher, doc_type, model_names, canonical_url, status, "
            "publication_date, last_checked FROM documents ORDER BY publisher, slug"
        ):
            d = dict(row)
            d["model_names"] = json.loads(d["model_names"])
            docs.append(d)
        by_status: dict[str, int] = {}
        for d in docs:
            by_status[d["status"]] = by_status.get(d["status"], 0) + 1
        by_publisher: dict[str, int] = {}
        for d in docs:
            by_publisher[d["publisher"]] = by_publisher.get(d["publisher"], 0) + 1
        return {
            "generated_at": utcnow(),
            "document_count": len(docs),
            "by_status": by_status,
            "by_publisher": by_publisher,
            "documents": docs,
        }
    finally:
        conn.close()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--out", help="write to file instead of stdout")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    summary = build_summary(repo)
    text = json.dumps(summary, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
