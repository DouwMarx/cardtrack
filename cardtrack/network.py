"""Network gate for the daily run.

The systemd timer is Persistent, so a missed 06:15 UTC firing runs the instant
the laptop resumes from suspend — seconds before Wi-Fi is back. Observed
2026-09-16..22: every "monitor outage" run started in the same second as
`PM: suspend exit`, all link checks errored within six seconds, and the OAuth
refresh failed for the same reason. Waiting for a probe URL to answer before
Phase A removes that whole failure class; when the network never comes, the
run exits 75 (EX_TEMPFAIL) having touched nothing, and systemd retries later.
"""

from __future__ import annotations

import time

import requests

EX_TEMPFAIL = 75
DEFAULT_PROBE_URLS = ("https://huggingface.co/api/models?limit=1",
                      "https://api.github.com/")


def network_up(urls: list[str] | tuple[str, ...], timeout: float = 10.0) -> str | None:
    """The first probe URL that answers any HTTP status, else None."""
    for url in urls:
        try:
            requests.get(url, timeout=timeout, headers={"User-Agent": "cardtrack-netprobe"})
            return url
        except requests.RequestException:
            continue
    return None


def wait_for_network(urls: list[str] | tuple[str, ...], *, wait_seconds: float,
                     interval: float = 15.0, timeout: float = 10.0,
                     sleep=time.sleep, clock=time.monotonic) -> tuple[bool, float]:
    """Poll until a probe answers or the deadline passes. Returns (up, waited_s)."""
    start = clock()
    while True:
        if network_up(urls, timeout=timeout):
            return True, clock() - start
        waited = clock() - start
        if waited >= wait_seconds:
            return False, waited
        sleep(min(interval, max(0.0, wait_seconds - waited)))
