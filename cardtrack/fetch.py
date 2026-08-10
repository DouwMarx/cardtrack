"""HTTP fetching with the guardrails the write path and monitor rely on:
browser UA, manual redirect resolution (≤5 hops, each hop host-checked),
per-document size caps, and an SSRF guard against private/loopback hosts.
"""

from __future__ import annotations

import ipaddress
import socket
import time
from dataclasses import dataclass, field

import requests

from .canonical import canonicalize_url

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
    - one retry after a short pause on 5xx (a single transient upstream error must
      not permanently burn a lead — rejected proposals are not retried by callers),
    - one retry with browser-TLS impersonation (curl_cffi) when bot-blocked
      (400/401/403/406/429/503), so bot-walled publishers don't bias the corpus.
    range_bytes limits the request to a prefix (the monitor's link probe; many
    CDNs mishandle HEAD)."""
    result = _fetch_requests(url, max_bytes=max_bytes, timeout=timeout,
                             allow_private_hosts=allow_private_hosts,
                             range_bytes=range_bytes, session=session)
    if not result.ok and result.status is not None and result.status >= 500:
        time.sleep(2)
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
