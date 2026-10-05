"""cardtrack.fetch: a rate-limited (429) host gets one paused retry, like a 5xx,
honouring a bounded Retry-After, before any impersonation fallback."""

from __future__ import annotations

import time

from cardtrack.fetch import MAX_RETRY_DELAY_SECONDS, fetch, retry_delay

BODY = b"<html><body><p>Served after the rate limit lifted.</p></body></html>"


class _RateLimitedRoute:
    """Duck-typed conftest Route: 429 for the first `limited` hits on this path,
    200 afterwards. Driven by the server's hit log, which the handler appends to
    before it reads the route, so no state lives on the route itself."""

    content_type = "text/html"
    block_plain_client = False
    body = BODY

    def __init__(self, server, path: str, limited: int = 1,
                 retry_after: str | None = None):
        self.server, self.path, self.limited, self.retry_after = (
            server, path, limited, retry_after)

    def _limited(self) -> bool:
        return self.server.hits.count(self.path) <= self.limited

    @property
    def status(self) -> int:
        return 429 if self._limited() else 200

    @property
    def headers(self) -> dict:
        if self._limited() and self.retry_after is not None:
            return {"Retry-After": self.retry_after}
        return {}


def test_429_then_200_is_retried_after_retry_after(http_server):
    http_server.routes["/limited"] = _RateLimitedRoute(http_server, "/limited",
                                                       retry_after="1")
    t0 = time.monotonic()
    result = fetch(http_server.url("/limited"), max_bytes=100_000, timeout=5,
                   allow_private_hosts=True)
    elapsed = time.monotonic() - t0
    assert result.ok and result.status == 200 and result.content == BODY
    assert not result.impersonated, "retry on the primary client, not the fallback"
    assert http_server.hits.count("/limited") == 2
    assert elapsed >= 1.0, "Retry-After honoured"


def test_429_without_retry_after_uses_default_pause(http_server):
    http_server.routes["/limited2"] = _RateLimitedRoute(http_server, "/limited2")
    t0 = time.monotonic()
    result = fetch(http_server.url("/limited2"), max_bytes=100_000, timeout=5,
                   allow_private_hosts=True, impersonate_fallback=False)
    assert result.ok and result.status == 200
    assert time.monotonic() - t0 >= 2.0


def test_persistent_429_is_still_blocked(http_server):
    http_server.routes["/wall"] = _RateLimitedRoute(http_server, "/wall", limited=99,
                                                    retry_after="0")
    result = fetch(http_server.url("/wall"), max_bytes=100_000, timeout=5,
                   allow_private_hosts=True)
    assert not result.ok and result.status == 429 and result.outcome == "blocked"
    assert result.retry_after == "0"


def test_retry_delay_is_bounded():
    assert retry_delay(None) == 2.0
    assert retry_delay("5") == 5.0
    assert retry_delay("100000") == MAX_RETRY_DELAY_SECONDS
    assert retry_delay("Wed, 21 Oct 2026 07:28:00 GMT") == 2.0, "HTTP-date → default"
    assert retry_delay("garbage") == 2.0
