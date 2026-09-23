#!/usr/bin/env python3
"""Text extraction wrapper (pdftotext / trafilatura). Two modes:
  --file PATH            extract one local file to stdout (debugging)
  --reextract-all        rebuild the derived layer from the immutable raw store:
                         re-extract every version's text, overwrite the files that
                         changed, recompute fingerprints and prune furniture-only
                         duplicates. Dry-run by default; --apply to write.
Run it after any change to extraction (bump DERIVED_LAYER_VERSION in
cardtrack/extract.py) — the monitor refuses to run until the layer matches.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.derived import reextract_all  # noqa: E402
from cardtrack.extract import extract_text  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--file", help="extract a single local file to stdout")
    p.add_argument("--content-type", help="content type hint for --file")
    p.add_argument("--reextract-all", action="store_true")
    p.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
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
        stats = reextract_all(Repo.locate(args.root), apply=args.apply)
        print(json.dumps(stats, ensure_ascii=False, indent=1))
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
