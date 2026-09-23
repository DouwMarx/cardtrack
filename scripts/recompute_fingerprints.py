#!/usr/bin/env python3
"""Recompute every stored content fingerprint with the current normalisation and
fingerprint.ignore_line_patterns (settings.yaml), pruning version rows that differ
only by page furniture (the earliest version of each fingerprint is kept). Run it
whenever the ignore patterns change; the monitor refuses to run until you do. If
extraction itself changed, run scripts/extract_text.py --reextract-all instead,
which rewrites the text files and then does this step.

Dry-run by default; --apply to write.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.derived import recompute_fingerprints  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = p.parse_args(argv)
    summary = recompute_fingerprints(Repo.locate(args.root), apply=args.apply)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
