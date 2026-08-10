#!/usr/bin/env python3
"""Print one settings.yaml value (dotted path) for shell scripts. Booleans print
as 'true'/'false'; missing keys print the provided default or empty."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("key", help="dotted path, e.g. publish.git_commit")
    p.add_argument("--default", default="")
    p.add_argument("--root")
    args = p.parse_args(argv)
    value = Repo.locate(args.root).setting(args.key, args.default)
    if value is None:
        value = args.default
    if isinstance(value, bool):
        print("true" if value else "false")
    else:
        print(value)
    return 0


if __name__ == "__main__":
    sys.exit(main())
