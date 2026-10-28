#!/usr/bin/env python3
"""Convert the weekly research report (report/report.md, written by the report agent)
into the HTML fragment the site's Analysis page embeds, plus its figures.

    report_html.py --report-dir report --out report/published \
        --model claude-fable-5-1 --skill-url https://github.com/.../SKILL.md \
        --max-words 1200 --min-figures 3

Pandoc converts the Markdown; this script then imposes the edition's shape:

- the document starts with one `# Title` line; the text before the first `##` is the
  lead and stays visible; every `##` section becomes a collapsible <details> block
  (the first one open, the rest collapsed), so readers expand what they care about
- a word cap over everything except tables (the Analysis page is a briefing, not a
  paper) and a minimum number of figures; both fail the conversion loudly, so the
  agent fixes the report instead of the pipeline publishing a wordy or figure-less one
- a Markdown table that did not survive pandoc (it degrades into "a | b | c" prose)
  fails the conversion rather than silently dropping evidence
- figures are PNG files copied from report/out/figures/ by basename; a missing,
  remote or non-PNG image fails, and the same file counts once

The HTML is sanitized against an allowlist because the site embeds it unescaped and
the agent reads untrusted documents. Writes out/report.html, out/figures/*.png and
out/meta.json; the disclaimer is rendered by the site template from meta.json, so
the report author cannot edit it away.
"""

from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_MAX_WORDS = 1200
DEFAULT_MIN_FIGURES = 3

# The site embeds this HTML unescaped, and it derives from agent-written Markdown (the
# agent reads untrusted documents). Allowlist what pandoc emits for this report;
# drop everything else, including scripts, event handlers and javascript: URLs.
ALLOWED_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "caption", "cite", "code", "col", "colgroup",
    "dd", "details", "div", "dl", "dt", "em", "figcaption", "figure", "h1", "h2", "h3",
    "h4", "h5", "h6", "hr", "i", "img", "li", "ol", "p", "pre", "section", "small", "span",
    "strong", "sub", "summary", "sup", "table", "tbody", "td", "tfoot", "th", "thead", "tr",
    "u", "ul",
}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "template", "svg", "math"}
# No class/id: the site styles the mandatory disclaimer by class, and the author must
# not be able to imitate it. Section ids are added by collapsible_sections() afterwards.
ALLOWED_ATTRS = {"href", "src", "alt", "title", "colspan", "rowspan", "style", "role", "open"}
SAFE_HREF = re.compile(r"^(https?://|mailto:|#)", re.I)
# Images only from the edition's own figures, PNG only (an SVG would run script on the
# site origin when opened directly); src is rewritten to figures/<basename>.
PNG_NAME = re.compile(r"^[\w-]+\.png$")
SAFE_STYLE = re.compile(r"^\s*(width|text-align)\s*:\s*[\w.%\s-]+;?\s*$", re.I)
# A pipe table pandoc could not parse degrades into "a | b | c" line blocks.
DEGRADED_TABLE_LINE = re.compile(r"(?m)^[^|\n]*\|[^|\n]*\|")


class _Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.in_table = 0
        self.words = 0          # words outside tables (the cap)
        self.figures: set[str] = set()      # distinct figure files
        self.bad_images: list[str] = []     # images that are not a local PNG

    def handle_starttag(self, tag, attrs, closed=False):
        if tag in DROP_WITH_CONTENT:
            self.skip += 0 if closed else 1
            return
        if self.skip or tag not in ALLOWED_TAGS:
            return
        if tag == "table":
            self.in_table += 1
        if tag == "img":
            src = (dict(attrs).get("src") or "").strip()
            name = Path(src).name
            if re.match(r"^[a-z]+:", src, re.I) or not PNG_NAME.match(name):
                self.bad_images.append(src or "(no src)")
                return
            attrs = [(k, f"figures/{name}" if k == "src" else v) for k, v in attrs]
            self.figures.add(name)
        kept = []
        for k, v in attrs:
            v = v or ""
            if k not in ALLOWED_ATTRS:
                continue
            if k == "href" and not SAFE_HREF.match(v.strip()):
                continue
            if k == "style" and not SAFE_STYLE.match(v):
                continue
            if k == "open":
                kept.append(" open")
                continue
            kept.append(f' {k}="{htmllib.escape(v, quote=True)}"')
        self.out.append(f"<{tag}{''.join(kept)}{' /' if closed else ''}>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and tag in ALLOWED_TAGS:
            if tag == "table":
                self.in_table = max(0, self.in_table - 1)
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            if not self.in_table:
                self.words += len(data.split())
            self.out.append(htmllib.escape(data, quote=False))


def sanitize(html: str) -> _Sanitizer:
    p = _Sanitizer()
    p.feed(html)
    p.close()
    if p.skip:
        raise SystemExit("report_html: an unclosed raw HTML block (<script>, <style>, ...) "
                         "would swallow the rest of the report")
    if p.bad_images:
        raise SystemExit("report_html: images must be PNG files in report/out/figures/, not "
                         + ", ".join(p.bad_images))
    return p


def split_title(md: str) -> tuple[str, str]:
    """The report starts with one `# Title` line; everything after it is the body."""
    m = re.match(r"\s*#\s+(?P<title>[^\n]+)\n", md)
    if not m:
        raise SystemExit("report_html: report.md must start with a single '# Title' line")
    return m.group("title").strip(), md[m.end():]


def collapsible_sections(body_html: str) -> str:
    """Lead (before the first <h2>) stays visible; each <h2> section becomes a
    <details> block, the first open and the rest collapsed. Runs on sanitized HTML,
    so the class and id it adds are the only ones on the page."""
    parts = re.split(r"(?=<h2\b)", body_html)
    out = [parts[0]]
    for i, chunk in enumerate(parts[1:]):
        m = re.match(r"<h2\b[^>]*>(.*?)</h2>(.*)$", chunk, re.S)
        if not m:
            out.append(chunk)
            continue
        heading, rest = m.groups()
        slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", heading).lower()).strip("-")
        state = " open" if i == 0 else ""
        out.append(f'<details class="section" id="sec-{slug}"{state}><summary><h2>{heading}</h2>'
                   f"</summary>{rest}</details>")
    return "".join(out)


def convert(report_dir: Path, out_dir: Path, model: str, skill_url: str,
            generated_at: str | None = None, max_words: int = DEFAULT_MAX_WORDS,
            min_figures: int = DEFAULT_MIN_FIGURES) -> dict:
    src = report_dir / "report.md"
    if not src.exists():
        raise SystemExit(f"report_html: {src} not found")
    title, body_md = split_title(src.read_text(encoding="utf-8"))

    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "in.md").write_text(body_md, encoding="utf-8")
        (t / "tpl.html").write_text("$body$\n", encoding="utf-8")
        cmd = ["pandoc", "in.md", "-f", "markdown", "-t", "html5", "--template", "tpl.html",
               "--wrap", "none", "-o", "out.html"]
        subprocess.run(cmd, cwd=t, check=True, capture_output=True, text=True)
        html = (t / "out.html").read_text(encoding="utf-8")

    san = sanitize(html)
    h1 = f'<h1 class="report-title">{htmllib.escape(title, quote=False)}</h1>\n'
    html = h1 + collapsible_sections("".join(san.out))
    words = san.words + len(title.split())

    # A pipe table pandoc could not parse degrades into "a | b | c" line blocks, which
    # would silently drop evidence from the published report.
    outside = re.sub(r"<(table|pre|code)\b.*?</\1>", "", html, flags=re.S).replace("<br />", "\n")
    outside = re.sub(r"<[^>]+>", "", outside)
    if DEGRADED_TABLE_LINE.search(outside):
        raise SystemExit("report_html: a table failed to convert (a line with two pipes "
                         "outside any table)")
    if words > max_words:
        raise SystemExit(f"report_html: {words} words outside tables, cap is {max_words}; "
                         "cut the report, not the cap")
    if len(san.figures) < min_figures:
        raise SystemExit(f"report_html: {len(san.figures)} distinct figures, at least "
                         f"{min_figures} required")

    fig_out = out_dir / "figures"
    shutil.rmtree(fig_out, ignore_errors=True)
    fig_out.mkdir()
    for name in sorted(san.figures):
        png = report_dir / "out" / "figures" / name
        if not png.exists():
            raise SystemExit(f"report_html: figure {name} missing in out/figures")
        shutil.copy2(png, fig_out / name)
    (out_dir / "report.html").write_text(html, encoding="utf-8")

    snapshot = ""
    results = report_dir / "out" / "results.json"
    if results.exists():
        try:
            snapshot = str(json.loads(results.read_text(encoding="utf-8")).get("snapshot_ts", ""))
        except json.JSONDecodeError:
            snapshot = ""
    meta = {"model": model, "skill_url": skill_url,
            "generated_at": generated_at or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "snapshot": snapshot, "words": words, "figures": len(san.figures)}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return meta


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--report-dir", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--model", required=True, help="model id that wrote the report")
    p.add_argument("--skill-url", required=True, help="URL of the skill file at the commit used")
    p.add_argument("--generated-at", help="UTC timestamp (default: now)")
    p.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS,
                   help="words allowed outside tables (default %(default)s)")
    p.add_argument("--min-figures", type=int, default=DEFAULT_MIN_FIGURES,
                   help="figures required (default %(default)s)")
    a = p.parse_args(argv)
    print(json.dumps(convert(a.report_dir, a.out, a.model, a.skill_url, a.generated_at,
                             a.max_words, a.min_figures)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
