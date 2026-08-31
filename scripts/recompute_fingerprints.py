#!/usr/bin/env python3
"""One-off operator migration: recompute every stored content fingerprint with the
current fingerprint.ignore_line_patterns (settings.yaml), collapsing version rows
that differ only by page furniture.

Run this whenever the ignore patterns change — stored fingerprints must match what
the monitor computes, or every unchanged document mints a bogus "new version" on
its next fetch. Per document: fingerprints are recomputed from the stored
text_path files; the EARLIEST version of each resulting fingerprint is kept (its
first-seen provenance is the honest one) and later furniture-only duplicates are
deleted. Raw blobs and extracted text files stay on disk untouched; the changelog
is append-only and keeps the full fetch history.

Dry-run by default; --apply to write.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.db import connect  # noqa: E402
from cardtrack.extract import fingerprint_text  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    patterns = repo.fingerprint_ignore_patterns
    conn = connect(repo.db_path)

    summary = {"status": "dry_run" if not args.apply else "applied",
               "versions": 0, "recomputed": 0, "pruned": 0, "docs_affected": 0}
    pruned_slugs: dict[str, int] = {}
    updates: list[tuple[int, str]] = []  # (version id, new fingerprint)
    deletes: list[int] = []
    try:
        docs = conn.execute("SELECT id, slug FROM documents ORDER BY id").fetchall()
        for doc in docs:
            versions = conn.execute(
                "SELECT * FROM document_versions WHERE document_id = ? "
                "ORDER BY fetched_at ASC, id ASC", (doc["id"],)).fetchall()
            seen: dict[str, int] = {}  # new fp -> kept version id
            doc_touched = False
            for v in versions:
                summary["versions"] += 1
                if not v["text_path"]:
                    fp = v["content_fingerprint"]  # extraction failed → raw hash stays
                else:
                    path = repo.root / v["text_path"]
                    if not path.exists():
                        fp = v["content_fingerprint"]
                    else:
                        fp = fingerprint_text(
                            path.read_text(encoding="utf-8"), patterns)
                if fp in seen:
                    # furniture-only duplicate of an earlier version → prune
                    summary["pruned"] += 1
                    pruned_slugs[doc["slug"]] = pruned_slugs.get(doc["slug"], 0) + 1
                    doc_touched = True
                    deletes.append(v["id"])
                    continue
                seen[fp] = v["id"]
                if fp != v["content_fingerprint"]:
                    summary["recomputed"] += 1
                    doc_touched = True
                    updates.append((v["id"], fp))
            if doc_touched:
                summary["docs_affected"] += 1
        if args.apply:
            # deletes first, then updates via unique placeholders: a kept row's new
            # fingerprint may equal another row's CURRENT one, so direct updates
            # can trip UNIQUE(document_id, content_fingerprint) mid-flight
            for vid in deletes:
                conn.execute("DELETE FROM document_versions WHERE id = ?", (vid,))
            for vid, _fp in updates:
                conn.execute("UPDATE document_versions SET content_fingerprint = ? "
                             "WHERE id = ?", (f"migrating:{vid}", vid))
            for vid, fp in updates:
                conn.execute("UPDATE document_versions SET content_fingerprint = ? "
                             "WHERE id = ?", (fp, vid))
            conn.commit()
    finally:
        conn.close()
    summary["pruned_by_doc"] = dict(sorted(pruned_slugs.items(),
                                           key=lambda kv: -kv[1]))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
