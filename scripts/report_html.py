#!/usr/bin/env python3
"""Convert the LaTeX research report (report/tex/report.tex) into the HTML
fragment the site's Analysis page embeds, plus its figures and the PDF.

    report_html.py --report-dir report --out report/published \
        --model claude-opus-5-5 --skill-url https://github.com/.../SKILL.md

Pandoc does the conversion; this script fixes what it gets wrong on this report:
\\ref numbers (taken from LaTeX's own .aux, so "Appendix A" stays A), figure paths
(\\graphicspath is ignored), table cells with \\newline (pandoc drops the whole
longtable) and % inside \\url (pandoc reads a comment). It then sanitizes the HTML
against an allowlist, because the site embeds it unescaped. Writes out/report.html,
out/figures/*.png and out/meta.json; no PDF, the site publishes HTML only. The
disclaimer is rendered by the site template from meta.json, so it cannot be edited
away by the report author.
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

BR = "CARDTRACKLINEBREAK"
TEMPLATE = """$if(title)$<h1 class="report-title">$title$</h1>$endif$
$if(abstract)$<div class="abstract">$abstract$</div>$endif$
$body$
"""


# The site embeds this HTML unescaped, and it derives from agent-written LaTeX (the
# agent reads untrusted documents). Allowlist what pandoc emits for this report;
# drop everything else, including scripts, event handlers and javascript: URLs.
ALLOWED_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "caption", "cite", "code", "col", "colgroup",
    "dd", "div", "dl", "dt", "em", "figcaption", "figure", "h1", "h2", "h3", "h4", "h5",
    "h6", "hr", "i", "img", "li", "math", "mfrac", "mi", "mn", "mo", "mrow", "msub",
    "msubsup", "msup", "mtext", "ol", "p", "pre", "section", "semantics", "annotation",
    "small", "span", "strong", "sub", "sup", "table", "tbody", "td", "tfoot", "th",
    "thead", "tr", "u", "ul",
}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "template", "svg"}
ALLOWED_ATTRS = {"href", "src", "alt", "title", "id", "class", "colspan", "rowspan",
                 "style", "role", "display", "encoding", "data-reference",
                 "data-reference-type", "data-cites"}
SAFE_URL = re.compile(r"^(https?://|mailto:|#|figures/[\w.-]+$)", re.I)
SAFE_STYLE = re.compile(r"^\s*(width|text-align)\s*:\s*[\w.%\s-]+;?\s*$", re.I)


class _Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs, closed=False):
        if tag in DROP_WITH_CONTENT:
            self.skip += 0 if closed else 1
            return
        if self.skip or tag not in ALLOWED_TAGS:
            return
        kept = []
        for k, v in attrs:
            v = v or ""
            if k not in ALLOWED_ATTRS:
                continue
            if k in ("href", "src") and not SAFE_URL.match(v.strip()):
                continue
            if k == "style" and not SAFE_STYLE.match(v):
                continue
            kept.append(f' {k}="{htmllib.escape(v, quote=True)}"')
        self.out.append(f"<{tag}{''.join(kept)}{' /' if closed else ''}>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and tag in ALLOWED_TAGS:
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(htmllib.escape(data, quote=False))


def sanitize(html: str) -> str:
    p = _Sanitizer()
    p.feed(html)
    p.close()
    return "".join(p.out)


def inline_inputs(tex: str, base: Path, depth: int = 0) -> str:
    if depth > 5:
        return tex

    def repl(m: re.Match) -> str:
        path = (base / m.group(1))
        if path.suffix != ".tex":
            path = path.with_suffix(".tex")
        if not path.exists():
            return m.group(0)
        return inline_inputs(path.read_text(encoding="utf-8"), path.parent, depth + 1)

    return re.sub(r"\\input\{([^}]+)\}", repl, tex)


def aux_labels(aux: Path) -> dict[str, str]:
    labels = {}
    if aux.exists():
        for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}",
                             aux.read_text(encoding="utf-8", errors="replace")):
            labels[m.group(1)] = m.group(2)
    return labels


def _escape_url_percent(m: re.Match) -> str:
    url = re.sub(r"(?<!\\)%", lambda _: "\\%", m.group(2))
    return "\\" + m.group(1) + "{" + url + "}"


def preprocess(tex: str, labels: dict[str, str]) -> str:
    tex = re.sub(r"\\(?:auto|c|C)?ref\{([^}]+)\}",
                 lambda m: labels.get(m.group(1), "?"), tex)
    tex = tex.replace("\\newline", BR + " ")
    # LaTeX's \url/\href take % literally; pandoc reads it as a comment and
    # swallows the rest of the table row (Claude%20Opus%205 in the appendix)
    tex = re.sub(r"\\(url|href)\{([^}]*)\}", _escape_url_percent, tex)
    tex = re.sub(r"\\graphicspath\{.*?\}\}", "", tex)
    tex = re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}",
                 lambda m: f"\\includegraphics{m.group(1) or ''}"
                           f"{{figures/{Path(m.group(2)).stem}.png}}", tex)
    return tex


def convert(report_dir: Path, out_dir: Path, model: str, skill_url: str,
            generated_at: str | None = None) -> dict:
    tex_dir = report_dir / "tex"
    src = tex_dir / "report.tex"
    labels = aux_labels(report_dir / "out" / "report.aux") or aux_labels(tex_dir / "report.aux")
    tex = preprocess(inline_inputs(src.read_text(encoding="utf-8"), tex_dir), labels)

    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "in.tex").write_text(tex, encoding="utf-8")
        (t / "tpl.html").write_text(TEMPLATE, encoding="utf-8")
        cmd = ["pandoc", "in.tex", "-f", "latex", "-t", "html5", "--template", "tpl.html",
               "--mathml", "--wrap", "none", "--citeproc",
               "--bibliography", str((tex_dir / "refs.bib").resolve()),
               "-o", "out.html"]
        subprocess.run(cmd, cwd=t, check=True, capture_output=True, text=True)
        html = (t / "out.html").read_text(encoding="utf-8")
    html = sanitize(html.replace(BR, "<br>"))
    # A table pandoc cannot parse either vanishes or degrades into "a & b & c"
    # paragraphs; both would silently drop evidence from the published report.
    n_src = len(re.findall(r"\\begin\{(?:longtable|tabular\*?|tabularx)\}", tex))
    n_out = html.count("<table")
    if n_out != n_src or re.search(r"&amp; [^<]{0,80} &amp;", html):
        raise SystemExit(f"report_html: a table failed to convert ({n_src} in the LaTeX, "
                         f"{n_out} in the HTML)")

    fig_out = out_dir / "figures"
    shutil.rmtree(fig_out, ignore_errors=True)
    fig_out.mkdir()
    for name in sorted(set(re.findall(r'src="figures/([^"]+\.png)"', html))):
        png = report_dir / "out" / "figures" / name
        if not png.exists():
            raise SystemExit(f"report_html: figure {name} missing in out/figures")
        shutil.copy2(png, fig_out / name)
    (out_dir / "report.html").write_text(html, encoding="utf-8")

    macros = (report_dir / "out" / "macros.tex")
    snap = re.search(r"\\newcommand\{\\snapshotTs\}\{([^}]*)\}",
                     macros.read_text(encoding="utf-8")) if macros.exists() else None
    meta = {"model": model, "skill_url": skill_url,
            "generated_at": generated_at or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "snapshot": snap.group(1) if snap else ""}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return meta


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--report-dir", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--model", required=True, help="model id that wrote the report")
    p.add_argument("--skill-url", required=True, help="URL of the skill file at the commit used")
    p.add_argument("--generated-at", help="UTC timestamp (default: now)")
    a = p.parse_args(argv)
    print(json.dumps(convert(a.report_dir, a.out, a.model, a.skill_url, a.generated_at)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
