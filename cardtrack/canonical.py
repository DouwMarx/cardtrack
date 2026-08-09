"""URL canonicalization (spec §5 identity rules).

Offline normalization only: lowercase scheme+host, drop default ports and fragments,
strip known tracking params. Redirect resolution happens in fetch.py; callers
canonicalize the post-redirect final URL.
"""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_EXACT = {
    "ref", "ref_src", "ref_url", "fbclid", "gclid", "dclid", "msclkid",
    "mc_cid", "mc_eid", "igshid", "twclid", "s_kwcid", "mkt_tok", "cmpid",
}
TRACKING_PREFIXES = ("utm_",)

DEFAULT_PORTS = {"http": 80, "https": 443}


def is_http_url(url: str) -> bool:
    try:
        return urlsplit(url.strip()).scheme.lower() in ("http", "https")
    except ValueError:
        return False


def _is_tracking(param: str) -> bool:
    p = param.lower()
    return p in TRACKING_EXACT or p.startswith(TRACKING_PREFIXES)


def canonicalize_url(url: str) -> str:
    """Normalize a URL for identity comparison. Raises ValueError on non-http(s) URLs."""
    parts = urlsplit(url.strip())
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https"):
        raise ValueError(f"not an http(s) URL: {url!r}")
    host = (parts.hostname or "").lower().rstrip(".")
    if not host:
        raise ValueError(f"URL has no host: {url!r}")
    netloc = host
    if parts.port is not None and parts.port != DEFAULT_PORTS.get(scheme):
        netloc = f"{host}:{parts.port}"
    path = parts.path or "/"
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not _is_tracking(k)]
    query = urlencode(kept)
    return urlunsplit((scheme, netloc, path, query, ""))
