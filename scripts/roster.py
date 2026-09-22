#!/usr/bin/env python3
"""Phase A roster sync CLI: refresh config/sources.generated.yaml from OpenRouter's
daily rankings (policy in config/roster.yaml). Prints a JSON summary. Fail-closed:
any data/network problem keeps the previous overlay and exits 0 with
status "kept_previous"; exit 1 only when the policy itself is broken."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo  # noqa: E402
from cardtrack.roster import run_roster  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--run-id",
                   default="roster-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
                   help="run id recorded in logs/roster_openrouter.json (default: timestamp)")
    args = p.parse_args(argv)
    summary = run_roster(Repo.locate(args.root), args.run_id)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
