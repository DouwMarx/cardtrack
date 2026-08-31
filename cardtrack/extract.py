"""Text extraction: pdftotext (preferred) / pypdf for PDFs, trafilatura for HTML.
Produces the display text and the whitespace-normalized fingerprint that drives
change detection (raw bytes churn on every fetch; extracted text does not).
"""

from __future__ import annotations

import hashlib
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


def _html_text(content: bytes, url: str = "") -> str | None:
    html = content.decode("utf-8", errors="replace")
    try:
        import trafilatura

        text = trafilatura.extract(
            html, url=url or None, include_comments=False,
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


# Rotating recommendation footers, excluded from the fingerprint two ways:
# (a) trailing alternating (blurb, "Read more") pairs are stripped from the end —
# blog pages append 3 rotating post teasers with no heading before them;
# (b) a "Related content" heading in the LAST QUARTER truncates there. Both are
# bounded to the last quarter so a same-shaped line mid-document can never blind
# change detection to real content below it.
FOOTER_PAIR_MARKER = "^Read more$"
FOOTER_HEADING = "^Related content$"


def normalize_for_fingerprint(text: str, ignore_patterns: tuple[str, ...] = ()) -> str:
    """Whitespace-collapse, minus dynamic page furniture. `ignore_patterns`
    (settings.yaml fingerprint.ignore_line_patterns) drop matching lines — download
    counters, access-date stamps — and the footer rules above truncate rotating
    recommendation footers, so furniture-only churn never mints a new document
    version. Display text is never filtered; empty patterns = plain collapse."""
    if ignore_patterns:
        lines = text.split("\n")
        floor = int(len(lines) * 0.75)
        pair = _compiled_ignores((FOOTER_PAIR_MARKER,))[0]
        while len(lines) >= 2 and len(lines) > floor and pair.search(lines[-1]):
            del lines[-2:]  # "Read more" plus the rotating teaser line above it
        heading = _compiled_ignores((FOOTER_HEADING,))[0]
        for i in range(floor, len(lines)):
            if heading.search(lines[i]):
                lines = lines[:i]
                break
        regexes = _compiled_ignores(ignore_patterns)
        lines = [line for line in lines
                 if not any(r.search(line) for r in regexes)]
        text = "\n".join(lines)
    return " ".join(text.split())


def fingerprint_text(text: str, ignore_patterns: tuple[str, ...] = ()) -> str:
    return hashlib.sha256(
        normalize_for_fingerprint(text, ignore_patterns).encode("utf-8")).hexdigest()


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def write_text_file(text_dir: Path, content_hash: str, text: str) -> Path:
    text_dir.mkdir(parents=True, exist_ok=True)
    path = text_dir / f"{content_hash}.txt"
    if not path.exists():
        path.write_text(text, encoding="utf-8")
    return path


def write_raw_blob(raw_dir: Path, content_hash: str, ext: str, content: bytes) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{content_hash}.{ext}"
    if not path.exists():  # append-only: never overwrite an existing blob
        path.write_bytes(content)
    return path
