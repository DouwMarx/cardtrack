"""The Analysis page (weekly AI-generated report): LaTeX -> HTML conversion with
real pandoc, and the site page with its mandatory disclaimer."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cardtrack.sitebuild import build_site, model_display_name
from scripts.report_html import convert

SKILL = "https://github.com/o/r/blob/abc/.claude/skills/cardtrack-report/SKILL.md"

TEX = r"""\documentclass{article}
\graphicspath{{../out/figures/}}
\input{../out/macros.tex}
\title{Test report}
\begin{document}
\maketitle
We tracked \nDocs{} documents (Figure~\ref{fig:a}; Appendix~\ref{app:x}) \cite{k1}.
\begin{figure}\includegraphics[width=\linewidth]{fig_a}\caption{A figure}\label{fig:a}\end{figure}
\appendix
\section{Changes}\label{app:x}
\input{../out/tables/t.tex}
\bibliographystyle{unsrtnat}
\bibliography{refs}
\end{document}
"""

TABLE = r"""\begin{longtable}{@{}lp{5cm}@{}}
\caption{Rows.}\label{tab:t} \\
\toprule
Id & Document \\
\midrule
\endfirsthead
\toprule
Id & Document \\
\midrule
\endhead
A1 & Opus card\newline\url{https://cdn.example.com/Claude%20Opus%205%20Card.pdf} \\
A2 & Second row survives the %20 above \\
\bottomrule
\end{longtable}
"""


@pytest.fixture
def report_dir(tmp_path: Path) -> Path:
    r = tmp_path / "report"
    (r / "tex").mkdir(parents=True)
    (r / "out" / "tables").mkdir(parents=True)
    (r / "out" / "figures").mkdir(parents=True)
    (r / "tex" / "report.tex").write_text(TEX)
    (r / "tex" / "refs.bib").write_text(
        "@misc{k1, title={A source}, author={Doe, J}, year={2026}}\n")
    (r / "out" / "macros.tex").write_text(
        "\\newcommand{\\snapshotTs}{2026-09-22T11:46:41+00:00}\n\\newcommand{\\nDocs}{302}\n")
    (r / "out" / "tables" / "t.tex").write_text(TABLE)
    (r / "out" / "figures" / "fig_a.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (r / "out" / "report.aux").write_text(
        "\\newlabel{fig:a}{{1}{1}{A figure}{figure.1}{}}\n"
        "\\newlabel{app:x}{{A}{2}{Changes}{appendix.A}{}}\n")
    return r


def test_convert_keeps_tables_refs_macros_and_figures(report_dir, tmp_path):
    out = tmp_path / "published"
    meta = convert(report_dir, out, "claude-opus-5-5", SKILL, "2026-09-29T00:00:00Z")
    html = (out / "report.html").read_text()
    assert "302 documents" in html                       # macro expanded
    assert "Figure\xa01" in html and "Appendix\xa0A" in html   # numbers from the .aux
    assert html.count("<table") == 1
    assert "Claude%20Opus%205%20Card.pdf" in html        # % in \url is not a comment
    assert "Second row survives" in html                 # ...so the next row is intact
    assert "<br>" in html                                # \newline in a cell
    assert 'src="figures/fig_a.png"' in html and (out / "figures" / "fig_a.png").exists()
    assert "A Source" in html                            # citeproc bibliography
    assert meta["snapshot"].startswith("2026-09-22") and meta["model"] == "claude-opus-5-5"


def test_broken_table_fails_loudly(report_dir, tmp_path):
    (report_dir / "out" / "tables" / "t.tex").write_text(
        TABLE.replace("\\endhead", "\\endhead\n\\multicolumn{2}{l}{x & y & z} \\\\"))
    with pytest.raises(SystemExit, match="table failed"):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def _publish(repo, report_dir: Path, meta: dict | None = None) -> None:
    pub = repo.root / "report" / "published"
    convert(report_dir, pub, "claude-opus-5-5", SKILL, "2026-09-29T00:00:00Z")
    if meta is not None:
        (pub / "meta.json").write_text(json.dumps(meta))


def test_analysis_page_has_disclaimer_and_nav(repo, report_dir):
    _publish(repo, report_dir)
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "analysis.html").read_text()
    assert "AI-generated report" in page
    assert "Claude Opus 5.5" in page and "claude-opus-5-5" in page
    assert f'href="{SKILL}"' in page
    assert 'src="./analysis/figures/fig_a.png"' in page
    assert (repo.site_dir / "analysis" / "figures" / "fig_a.png").exists()
    for name in ("index.html", "about.html", "search.html"):
        assert 'href="./analysis.html">Analysis</a>' in (repo.site_dir / name).read_text()


def test_no_page_without_provenance_and_stale_page_removed(repo, report_dir):
    _publish(repo, report_dir)
    build_site(repo, run_pagefind=False)
    assert (repo.site_dir / "analysis.html").exists()
    _publish(repo, report_dir, meta={"model": "", "skill_url": SKILL})
    build_site(repo, run_pagefind=False)
    assert not (repo.site_dir / "analysis.html").exists()
    assert "analysis.html" not in (repo.site_dir / "index.html").read_text()
    shutil.rmtree(repo.root / "report")
    build_site(repo, run_pagefind=False)
    assert not (repo.site_dir / "analysis").exists()


@pytest.mark.parametrize("mid,name", [("claude-opus-5-5", "Claude Opus 5.5"),
                                      ("claude-fable-5-1", "Claude Fable 5.1"),
                                      ("claude-haiku-4-5-20251001", "Claude Haiku 4.5"),
                                      ("claude-sonnet-5", "Claude Sonnet 5")])
def test_model_display_name(mid, name):
    assert model_display_name(mid) == name


def test_agent_written_markup_cannot_inject_script(report_dir, tmp_path):
    tex = (report_dir / "tex" / "report.tex").read_text().replace(
        r"\appendix",
        r"See \href{javascript:alert(1)}{this} and \href{https://ok.example/x}{that}."
        "\n\\begin{rawhtml}<script>alert(2)</script>\\end{rawhtml}\n"
        r"\appendix")
    (report_dir / "tex" / "report.tex").write_text(tex)
    convert(report_dir, tmp_path / "published", "m", SKILL)
    html = (tmp_path / "published" / "report.html").read_text()
    assert "javascript:" not in html and "<script" not in html
    assert 'href="https://ok.example/x"' in html
    assert html.count("<table") == 1
