"""HTTP fetching with the guardrails the write path and monitor rely on:
browser UA, manual redirect resolution (≤5 hops, each hop host-checked),
per-document size caps, and an SSRF guard against private/loopback hosts.
"""

from __future__ import annotations

import ipaddress
import re
import socket
import time
from dataclasses import dataclass, field

import requests

from .canonical import canonicalize_url

# Client-side redirect stubs: a 200 whose whole body is <meta http-equiv="refresh"
# content="0; url=..."> (Palisade's blog, Sept 2026). To a link checker that page is
# alive; to a reader it is gone. A refresh with a delay over a few seconds is a
# reload, not a move, and is left alone.
_META_TAG = re.compile(rb"<meta\b[^>]*>", re.IGNORECASE)
_HTTP_EQUIV_REFRESH = re.compile(rb"http-equiv\s*=\s*[\"']?refresh[\"']?", re.IGNORECASE)
_REFRESH_CONTENT = re.compile(
    rb"content\s*=\s*[\"']\s*(\d+)\s*;\s*url\s*=\s*[\"']?([^\"'>\s]+)", re.IGNORECASE)
MAX_REFRESH_DELAY_SECONDS = 5


def client_redirect_target(content: bytes | None, content_type: str | None,
                           base_url: str) -> str | None:
    """URL a meta-refresh stub points at, or None when the body is a real page."""
    if not content or (content_type and "html" not in content_type.lower()):
        return None
    for tag in _META_TAG.finditer(content[:16384]):
        meta = tag.group(0)
        if not _HTTP_EQUIV_REFRESH.search(meta):
            continue
        m = _REFRESH_CONTENT.search(meta)
        if not m or int(m.group(1)) > MAX_REFRESH_DELAY_SECONDS:
            continue
        from urllib.parse import urljoin

        target = urljoin(base_url, m.group(2).decode("utf-8", errors="replace").strip())
        return target if target != base_url else None
    return None

BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
MAX_REDIRECTS = 5
PERMANENT_REDIRECTS = {301, 308}
REDIRECT_CODES = {301, 302, 303, 307, 308}
# 400 included: several publishers (Meta) answer bot-detected requests with 400
BLOCKED_STATUSES = {400, 401, 403, 406, 429, 503}
IMPERSONATE_TRIGGER = BLOCKED_STATUSES
NOT_FOUND_STATUSES = {404, 410}
OK_STATUSES = {200, 206}
# Rate limiting is transient like a 5xx, not a bot wall: going straight to the
# impersonation fallback (also rate-limited) turned a one-minute limit into
# document_retrievable=false and a lost lead for a day.
RETRY_STATUSES = {429}
DEFAULT_RETRY_DELAY_SECONDS = 2
# Bounded low: the monitor probes ~330 URLs sequentially, so a host advertising
# Retry-After: 60 across its pages would add minutes per page to Phase A.
MAX_RETRY_DELAY_SECONDS = 15


def retry_delay(retry_after: str | None) -> float:
    """Seconds to wait before the one retry: Retry-After in delay-seconds form,
    clamped to MAX_RETRY_DELAY_SECONDS; the default for an absent, HTTP-date or
    malformed header (an HTTP-date is rare on 429s and not worth parsing)."""
    if retry_after and retry_after.strip().isdigit():
        return float(min(int(retry_after.strip()), MAX_RETRY_DELAY_SECONDS))
    return float(DEFAULT_RETRY_DELAY_SECONDS)


@dataclass
class FetchResult:
    url: str                      # final URL after redirects (as served)
    ok: bool = False
    status: int | None = None
    content: bytes | None = None
    content_type: str | None = None
    permanent_redirect: bool = False  # the requested URL has permanently moved
    stable_url: str = ""          # canonical identity: follows ONLY permanent redirects;
                                  # frozen at the first temporary redirect (302/303/307)
    impersonated: bool = False    # fetched via browser-TLS impersonation fallback
    truncated: bool = False
    error: str | None = None
    hops: list[str] = field(default_factory=list)
    retry_after: str | None = None  # Retry-After header of a 429/5xx, as served

    @property
    def outcome(self) -> str:
        """Classify for the monitor: ok | not_found | blocked | error."""
        if self.status in OK_STATUSES:
            return "ok"
        if self.status in NOT_FOUND_STATUSES:
            return "not_found"
        if self.status in BLOCKED_STATUSES:
            return "blocked"
        return "error"


def host_is_public(hostname: str) -> bool:
    """Reject loopback/private/link-local/reserved targets (checks all resolved addresses)."""
    if not hostname or hostname.lower() in ("localhost",):
        return False
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False
    for info in infos:
        try:
            addr = ipaddress.ip_address(info[4][0])
        except ValueError:
            return False
        if not addr.is_global:
            return False
    return True


def fetch(
    url: str,
    *,
    max_bytes: int,
    timeout: float,
    allow_private_hosts: bool = False,
    range_bytes: int | None = None,
    session: requests.Session | None = None,
    impersonate_fallback: bool = True,
) -> FetchResult:
    """GET with manual redirect handling, plus two recovery layers:
    - one retry after a pause on 5xx or 429 (a single transient upstream error or
      rate-limit must not permanently burn a lead — rejected proposals are not
      retried by callers; a 429 honours Retry-After, bounded),
    - one retry with browser-TLS impersonation (curl_cffi) when bot-blocked
      (400/401/403/406/429/503), so bot-walled publishers don't bias the corpus.
    range_bytes limits the request to a prefix (the monitor's link probe; many
    CDNs mishandle HEAD)."""
    result = _fetch_requests(url, max_bytes=max_bytes, timeout=timeout,
                             allow_private_hosts=allow_private_hosts,
                             range_bytes=range_bytes, session=session)
    if not result.ok and result.status is not None and (
            result.status >= 500 or result.status in RETRY_STATUSES):
        time.sleep(retry_delay(result.retry_after))
        result = _fetch_requests(url, max_bytes=max_bytes, timeout=timeout,
                                 allow_private_hosts=allow_private_hosts,
                                 range_bytes=range_bytes, session=session)
    if (impersonate_fallback and not result.ok
            and result.status in IMPERSONATE_TRIGGER):
        fallback = _fetch_impersonate(url, max_bytes=max_bytes, timeout=timeout,
                                      allow_private_hosts=allow_private_hosts,
                                      range_bytes=range_bytes)
        if fallback.ok or (fallback.status is not None
                           and fallback.status not in IMPERSONATE_TRIGGER):
            return fallback
    return result


def _fetch_requests(
    url: str,
    *,
    max_bytes: int,
    timeout: float,
    allow_private_hosts: bool = False,
    range_bytes: int | None = None,
    session: requests.Session | None = None,
) -> FetchResult:
    sess = session or requests.Session()
    headers = {"User-Agent": BROWSER_UA, "Accept": "*/*"}
    if range_bytes:
        headers["Range"] = f"bytes=0-{range_bytes - 1}"

    current = url.strip()
    result = FetchResult(url=current, stable_url=current)
    chain_permanent = True
    for _hop in range(MAX_REDIRECTS + 1):
        try:
            canonical_probe = canonicalize_url(current)
        except ValueError as e:
            result.error = str(e)
            return result
        from urllib.parse import urlsplit

        host = urlsplit(canonical_probe).hostname or ""
        if not allow_private_hosts and not host_is_public(host):
            result.error = f"host not public: {host}"
            return result

        try:
            resp = sess.get(
                current, headers=headers, timeout=timeout,
                allow_redirects=False, stream=True,
            )
        except requests.RequestException as e:
            result.error = f"{type(e).__name__}: {e}"
            result.url = current
            return result

        result.status = resp.status_code
        result.url = current
        if resp.status_code in REDIRECT_CODES:
            location = resp.headers.get("Location")
            resp.close()
            if not location:
                result.error = "redirect without Location"
                return result
            from urllib.parse import urljoin

            result.hops.append(current)
            current = urljoin(current, location)
            if resp.status_code in PERMANENT_REDIRECTS and chain_permanent:
                result.stable_url = current
                result.permanent_redirect = True
            else:
                chain_permanent = False
            continue

        # terminal response
        result.content_type = (resp.headers.get("Content-Type") or "").split(";")[0].strip() or None
        if resp.status_code not in OK_STATUSES:
            result.retry_after = resp.headers.get("Retry-After")
            resp.close()
            return result
        chunks: list[bytes] = []
        size = 0
        try:
            for chunk in resp.iter_content(chunk_size=65536):
                chunks.append(chunk)
                size += len(chunk)
                if size > max_bytes:
                    result.truncated = True
                    break
        except requests.RequestException as e:
            result.error = f"{type(e).__name__}: {e}"
            return result
        finally:
            resp.close()
        result.content = b"".join(chunks)
        if result.truncated and not range_bytes:
            result.error = f"exceeds max_fetch_bytes ({max_bytes})"
            return result
        target = client_redirect_target(result.content, result.content_type, current)
        if target:
            # treat like a 301: the old URL now only points elsewhere
            result.hops.append(current)
            result.content = None
            result.truncated = False
            current = target
            if chain_permanent:
                result.stable_url = current
                result.permanent_redirect = True
            continue
        result.ok = True
        return result

    result.error = f"too many redirects (>{MAX_REDIRECTS})"
    return result


def probe(url: str, *, timeout: float, allow_private_hosts: bool = False,
          session: requests.Session | None = None,
          impersonate_fallback: bool = True) -> FetchResult:
    """Cheap liveness check: GET with a small Range, redirects resolved."""
    return fetch(
        url, max_bytes=8192, timeout=timeout,
        allow_private_hosts=allow_private_hosts,
        range_bytes=2048, session=session,
        impersonate_fallback=impersonate_fallback,
    )


def _fetch_impersonate(
    url: str,
    *,
    max_bytes: int,
    timeout: float,
    allow_private_hosts: bool = False,
    range_bytes: int | None = None,
) -> FetchResult:
    """Fallback transport: curl_cffi impersonating a real Chrome TLS/HTTP2
    fingerprint. Same redirect and host guards as the primary path; the size cap
    is enforced via Content-Length pre-check plus post-download length check
    (curl_cffi is not streamed here)."""
    from urllib.parse import urljoin, urlsplit

    try:
        from curl_cffi import requests as cf_requests
    except ImportError:
        result = FetchResult(url=url, stable_url=url)
        result.error = "curl_cffi not installed"
        return result

    headers = {}
    if range_bytes:
        headers["Range"] = f"bytes=0-{range_bytes - 1}"
    current = url.strip()
    result = FetchResult(url=current, stable_url=current, impersonated=True)
    chain_permanent = True
    for _hop in range(MAX_REDIRECTS + 1):
        try:
            canonical_probe = canonicalize_url(current)
        except ValueError as e:
            result.error = str(e)
            return result
        host = urlsplit(canonical_probe).hostname or ""
        if not allow_private_hosts and not host_is_public(host):
            result.error = f"host not public: {host}"
            return result
        try:
            resp = cf_requests.get(current, headers=headers, timeout=timeout,
                                   allow_redirects=False, impersonate="chrome")
        except Exception as e:
            result.error = f"{type(e).__name__}: {e}"
            result.url = current
            return result
        result.status = resp.status_code
        result.url = current
        if resp.status_code in REDIRECT_CODES:
            location = resp.headers.get("Location")
            if not location:
                result.error = "redirect without Location"
                return result
            result.hops.append(current)
            current = urljoin(current, location)
            if resp.status_code in PERMANENT_REDIRECTS and chain_permanent:
                result.stable_url = current
                result.permanent_redirect = True
            else:
                chain_permanent = False
            continue
        result.content_type = (resp.headers.get("Content-Type") or "").split(";")[0].strip() or None
        if resp.status_code not in OK_STATUSES:
            return result
        declared = resp.headers.get("Content-Length")
        if declared and declared.isdigit() and int(declared) > max_bytes and not range_bytes:
            result.error = f"exceeds max_fetch_bytes ({max_bytes})"
            return result
        content = resp.content
        if len(content) > max_bytes:
            if range_bytes:
                content = content[:max_bytes]
                result.truncated = True
            else:
                result.truncated = True
                result.error = f"exceeds max_fetch_bytes ({max_bytes})"
                return result
        result.content = content
        result.ok = True
        return result

    result.error = f"too many redirects (>{MAX_REDIRECTS})"
    return result
