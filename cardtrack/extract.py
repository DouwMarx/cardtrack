"""Text extraction: pdftotext (preferred) / pypdf for PDFs, trafilatura for HTML.
Produces the display text and the whitespace-normalized fingerprint that drives
change detection (raw bytes churn on every fetch; extracted text does not).
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from functools import lru_cache
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path


def sniff_kind(content: bytes, content_type: str | None, url: str = "") -> str:
    if content.startswith(b"%PDF-"):
        return "pdf"
    ct = (content_type or "").lower()
    if "pdf" in ct:
        return "pdf"
    if "html" in ct or "xml" in ct:
        return "html"
    lowered = url.lower().split("?")[0]
    if lowered.endswith(".pdf"):
        return "pdf"
    head = content[:2048].lstrip().lower()
    if head.startswith((b"<!doctype", b"<html", b"<head", b"<body")):
        return "html"
    if ct.startswith("text/"):
        return "text"
    return "binary"


def ext_for(kind: str) -> str:
    return {"pdf": "pdf", "html": "html", "text": "txt"}.get(kind, "bin")


def _pdf_text(content: bytes) -> str | None:
    if shutil.which("pdftotext"):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tf:
            tf.write(content)
            tf.flush()
            try:
                proc = subprocess.run(
                    ["pdftotext", "-layout", "-enc", "UTF-8", tf.name, "-"],
                    capture_output=True, timeout=120,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    return proc.stdout.decode("utf-8", errors="replace")
            except (subprocess.TimeoutExpired, OSError):
                pass
    try:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages)
        return text if text.strip() else None
    except Exception:
        return None


class _TagStripper(HTMLParser):
    SKIP = {"script", "style", "noscript", "template", "svg", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth and data.strip():
            self.parts.append(data)


_FOOTER_TOKEN = re.compile(r"\S*footer\S*", re.IGNORECASE)


def _protect_content_containers(html: str) -> str:
    """Keep footnote blocks out of the boilerplate remover's reach.

    trafilatura discards any element whose class contains "footer". In August 2026
    Anthropic wrapped its footnote block in a "...postFooter" container and the footnotes
    silently vanished from three documents' extracted text while the raw HTML still held
    them (see the 2026-09-22 report). Find the ancestors of footnote elements with lxml,
    then rewrite exactly those class attributes in the original string: trafilatura
    must still receive the HTML as served (a pre-parsed tree extracts differently)."""
    if "footnote" not in html.lower():
        return html
    try:
        from lxml import html as lxml_html

        tree = lxml_html.fromstring(html)
    except Exception:
        return html
    rewrites: dict[str, str] = {}
    for el in tree.iter():
        cls = el.get("class") if hasattr(el, "get") else None
        if not cls or "footnote" not in cls.lower():
            continue
        node = el
        while node is not None:
            ncls = node.get("class")
            if ncls and _FOOTER_TOKEN.search(ncls):
                rewrites[ncls] = _FOOTER_TOKEN.sub("", ncls).strip()
            node = node.getparent()
    for old_cls, new_cls in rewrites.items():
        for quote in ('"', "'"):
            html = html.replace(f"class={quote}{old_cls}{quote}", f"class={quote}{new_cls}{quote}")
    return html


def _html_text(content: bytes, url: str = "") -> str | None:
    html = content.decode("utf-8", errors="replace")
    try:
        import trafilatura

        text = trafilatura.extract(
            _protect_content_containers(html), url=url or None, include_comments=False,
            include_tables=True, favor_recall=True,
        )
        if text and text.strip():
            return text
    except Exception:
        pass
    stripper = _TagStripper()
    try:
        stripper.feed(html)
    except Exception:
        return None
    text = "\n".join(stripper.parts)
    return text if text.strip() else None


def extract_text(content: bytes, content_type: str | None, url: str = "") -> tuple[str | None, str]:
    """Return (display_text, method). display_text is None when extraction fails."""
    kind = sniff_kind(content, content_type, url)
    if kind == "pdf":
        text = _pdf_text(content)
        return (clean_display_text(text) if text else None, "pdf")
    if kind == "html":
        text = _html_text(content, url)
        return (clean_display_text(text) if text else None, "html")
    if kind == "text":
        # empty after cleaning == failed extraction, per the contract above, so every
        # consumer (fingerprint raw-hash fallback, NULL text_path) stays consistent
        return (clean_display_text(content.decode("utf-8", errors="replace")) or None,
                "text")
    return None, "binary"


def clean_display_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


@lru_cache(maxsize=8)
def _compiled_ignores(patterns: tuple[str, ...]) -> list[re.Pattern]:
    return [re.compile(p) for p in patterns]


# Rotating recommendation blocks, excluded from the fingerprint line-wise:
# (a) a "Related content" heading truncates the text. In the last quarter it always
#     does; anywhere earlier only when the tail is at least two teaser groups, each
#     at most title / blurb / "Read more" long. Short posts (an 18-line access
#     policy) carry the block well before the last quarter; the shape condition is
#     what keeps a real section below a same-named heading from being hidden. A real
#     section shaped exactly like two teaser groups is indistinguishable at line
#     level and is accepted. Measured 2026-10-05: all 31 stored tails qualify;
# (b) trailing alternating (blurb, "Read more") pairs are stripped from the end —
#     blog pages append 3 rotating post teasers with no heading before them. Bounded
#     to the last quarter so a same-shaped line mid-document can never blind change
#     detection to real content below it.
FOOTER_PAIR_MARKER = "^Read more$"
FOOTER_HEADING = "^Related content$"
TEASER_GROUP_LINES = 3
MIN_TEASER_GROUPS = 2

# A line that is nothing but a date ("Jan 14, 2026", "05 July 2026", "2026-09-03",
# optionally labelled "Updated"). Not a fingerprint ignore: a date-only edit still
# mints a version, but the diff classifier treats it as furniture.
_MONTH = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?"
          r"|Sept?(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?")
DATE_LINE_PATTERN = (
    r"(?i)^(?:(?:published|updated|last updated|posted|date)\s*[:\-]?\s*)?"
    rf"(?:{_MONTH} \d{{1,2}},? \d{{4}}|\d{{1,2}} {_MONTH} \d{{4}}|\d{{4}}-\d{{2}}-\d{{2}})[.,]?$"
)


def _all_teasers(tail: list[str], marker: re.Pattern) -> bool:
    """True when `tail` is nothing but teaser groups: each ends in a marker line, is
    at most TEASER_GROUP_LINES long, and there are at least MIN_TEASER_GROUPS."""
    if not tail or not marker.search(tail[-1]):
        return False
    markers = [i for i, line in enumerate(tail) if marker.search(line)]
    starts = [-1] + markers[:-1]
    return (len(markers) >= MIN_TEASER_GROUPS
            and all(m - s <= TEASER_GROUP_LINES for s, m in zip(starts, markers, strict=True)))


def strip_furniture_lines(text: str, ignore_patterns: tuple[str, ...]) -> list[str]:
    """Lines of `text` minus dynamic page furniture: the recommendation blocks above
    and every line matching `ignore_patterns` (settings.yaml
    fingerprint.ignore_line_patterns — download counters, sidebars). Shared by the
    fingerprint and by the diff classifier so "unchanged" means the same thing in
    both places. Display text is never filtered."""
    lines = text.split("\n")
    floor = int(len(lines) * 0.75)
    marker = _compiled_ignores((FOOTER_PAIR_MARKER,))[0]
    heading = _compiled_ignores((FOOTER_HEADING,))[0]
    for i, line in enumerate(lines):
        if heading.search(line) and (i >= floor or _all_teasers(lines[i + 1:], marker)):
            lines = lines[:i]
            break
    while len(lines) >= 2 and len(lines) > floor and marker.search(lines[-1]):
        del lines[-2:]  # "Read more" plus the rotating teaser line above it
    regexes = _compiled_ignores(ignore_patterns)
    return [line for line in lines if not any(r.search(line) for r in regexes)]


def normalize_for_fingerprint(text: str, ignore_patterns: tuple[str, ...] = ()) -> str:
    """Whitespace-collapse, minus dynamic page furniture (strip_furniture_lines), so
    furniture-only churn never mints a new document version. Empty patterns = plain
    collapse."""
    if ignore_patterns:
        text = "\n".join(strip_furniture_lines(text, ignore_patterns))
    return " ".join(text.split())


def fingerprint_text(text: str, ignore_patterns: tuple[str, ...] = ()) -> str:
    return hashlib.sha256(
        normalize_for_fingerprint(text, ignore_patterns).encode("utf-8")).hexdigest()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


# Bump whenever extraction or fingerprint normalisation changes what is derived from
# the same raw bytes (a new trafilatura, a pre-clean rule, a footer rule). Together
# with the ignore patterns it identifies the derived layer; the monitor refuses to
# run until stored texts and fingerprints have been rebuilt to match
# (scripts/extract_text.py --reextract-all --apply).
#   1  original
#   2  footnote containers protected from the boilerplate remover (2026-09-23)
#   3  "Related content" teaser block stripped wherever it sits, not only in the
#      last quarter (2026-10-05)
DERIVED_LAYER_VERSION = 3


def derived_config_id(ignore_patterns: tuple[str, ...] = ()) -> str:
    payload = json.dumps({"version": DERIVED_LAYER_VERSION,
                          "ignore_patterns": list(ignore_patterns)}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def write_text_file(text_dir: Path, content_hash: str, text: str,
                    overwrite: bool = False) -> Path:
    text_dir.mkdir(parents=True, exist_ok=True)
    path = text_dir / f"{content_hash}.txt"
    if overwrite or not path.exists():
        path.write_text(text, encoding="utf-8")
    return path


def write_raw_blob(raw_dir: Path, content_hash: str, ext: str, content: bytes) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{content_hash}.{ext}"
    if not path.exists():  # append-only: never overwrite an existing blob
        path.write_bytes(content)
    return path
