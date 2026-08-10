#!/usr/bin/env python3
"""Text extraction wrapper (pdftotext / trafilatura). Two modes:
  --file PATH            extract one local file to stdout (debugging)
  --reextract-all        re-run extraction over the whole raw store (the derived
                         layer is rebuilt from immutable raw bytes; fingerprints
                         recompute; UNIQUE conflicts are reported, never forced)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.db import connect  # noqa: E402
from cardtrack.extract import extract_text, fingerprint_text, write_text_file  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def reextract_all(repo: Repo) -> dict:
    conn = connect(repo.db_path)
    stats = {"versions": 0, "updated": 0, "failed": 0, "conflicts": []}
    try:
        for row in conn.execute("SELECT * FROM document_versions ORDER BY id").fetchall():
            stats["versions"] += 1
            raw = repo.root / row["raw_path"]
            if not raw.exists():
                stats["failed"] += 1
                continue
            content = raw.read_bytes()
            text, _method = extract_text(content, row["content_type"])
            if text is None:
                stats["failed"] += 1
                continue
            fp = fingerprint_text(text)
            text_path = write_text_file(repo.text_dir, row["content_hash"], text)
            if fp != row["content_fingerprint"]:
                clash = conn.execute(
                    "SELECT id FROM document_versions WHERE document_id = ? AND "
                    "content_fingerprint = ? AND id != ?",
                    (row["document_id"], fp, row["id"])).fetchone()
                if clash:
                    stats["conflicts"].append(
                        {"version_id": row["id"], "collides_with": clash["id"],
                         "fingerprint": fp,
                         "note": "two versions now extract to identical text; "
                                 "needs human review"})
                    continue
            conn.execute(
                "UPDATE document_versions SET content_fingerprint = ?, text_path = ? "
                "WHERE id = ?",
                (fp, str(text_path.relative_to(repo.root)), row["id"]))
            stats["updated"] += 1
        conn.commit()
    finally:
        conn.close()
    return stats


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--file", help="extract a single local file to stdout")
    p.add_argument("--content-type", help="content type hint for --file")
    p.add_argument("--reextract-all", action="store_true")
    args = p.parse_args(argv)

    if args.file:
        content = Path(args.file).read_bytes()
        text, method = extract_text(content, args.content_type, args.file)
        if text is None:
            print(f"[extract_text] extraction failed (method: {method})", file=sys.stderr)
            return 1
        print(text)
        return 0
    if args.reextract_all:
        stats = reextract_all(Repo.locate(args.root))
        print(json.dumps(stats, ensure_ascii=False, indent=1))
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
