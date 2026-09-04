import pytest

from cardtrack.canonical import canonicalize_url

CASES = [
    # (input, expected)
    ("HTTPS://Example.COM/Path", "https://example.com/Path"),          # host lowered, path kept
    ("https://example.com:443/a", "https://example.com/a"),            # default port dropped
    ("http://example.com:80/a", "http://example.com/a"),
    ("http://example.com:8080/a", "http://example.com:8080/a"),        # non-default port kept
    ("https://example.com", "https://example.com/"),                   # empty path → /
    ("https://example.com/a#section-2", "https://example.com/a"),      # fragment stripped
    ("https://example.com/a?utm_source=tw&utm_campaign=x", "https://example.com/a"),
    ("https://example.com/a?ref=hn", "https://example.com/a"),
    ("https://example.com/a?fbclid=abc&id=7", "https://example.com/a?id=7"),
    ("https://example.com/a?id=7&b=2", "https://example.com/a?id=7&b=2"),  # kept, in order
    ("https://example.com./a", "https://example.com/a"),               # trailing host dot
    ("  https://example.com/a  ", "https://example.com/a"),            # whitespace
]


@pytest.mark.parametrize("raw,expected", CASES)
def test_canonicalize_table(raw, expected):
    assert canonicalize_url(raw) == expected


def test_canonicalize_is_idempotent():
    for raw, _ in CASES:
        once = canonicalize_url(raw)
        assert canonicalize_url(once) == once


@pytest.mark.parametrize("bad", ["ftp://example.com/x", "javascript:alert(1)",
                                 "mailto:a@b.c", "file:///etc/passwd", "not a url"])
def test_non_http_rejected(bad):
    with pytest.raises(ValueError):
        canonicalize_url(bad)
