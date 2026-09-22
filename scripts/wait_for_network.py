#!/usr/bin/env python3
"""Block until the network answers (settings: network.probe_urls,
network.wait_seconds). Exit 0 when up, 75 (EX_TEMPFAIL) when the deadline
passes so the scheduler can retry the whole run later."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.network import DEFAULT_PROBE_URLS, EX_TEMPFAIL, wait_for_network  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    urls = list(repo.setting("network.probe_urls") or DEFAULT_PROBE_URLS)
    wait = float(repo.setting("network.wait_seconds", 900))
    up, waited = wait_for_network(urls, wait_seconds=wait)
    if up:
        if waited > 1:
            print(f"[wait_for_network] network up after {waited:.0f}s")
        return 0
    print(f"[wait_for_network] no network after {waited:.0f}s; exiting {EX_TEMPFAIL} for retry")
    return EX_TEMPFAIL


if __name__ == "__main__":
    sys.exit(main())
