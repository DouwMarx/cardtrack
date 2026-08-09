#!/usr/bin/env python3
"""Phase A monitor CLI (spec §8): link checks, fingerprint rotation, index-page diff.
Prints a JSON summary. Deterministic; no LLM involved."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.monitor import run_monitor  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--run-id",
                   default="monitor-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"))
    args = p.parse_args(argv)
    summary = run_monitor(Repo.locate(args.root), args.run_id)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
