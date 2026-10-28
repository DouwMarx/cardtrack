"""The Analysis page (weekly AI-generated briefing): Markdown -> HTML conversion with
real pandoc, its publication gates (word cap, minimum figures, tables, figure files,
collapsible sections), and the site page with its mandatory disclaimer."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cardtrack.sitebuild import build_site, model_display_name
from scripts.report_html import convert

SKILL = "https://github.com/o/r/blob/abc/.claude/skills/cardtrack-report/SKILL.md"

MD = """# Test briefing

Lead: the [Opus card](https://systemcards.org/docs/opus.html) dropped a safeguard (v1→v2).

## What changed

Two documents changed; the table has the numbers.

| Id | Document | Versions |
|---|---|---|
| A1 | Opus card<br>https://cdn.example.com/Claude%20Opus%205%20Card.pdf | v1→v2 |
| A2 | Second row survives the %20 above | v3→v4 |

![Changes by category](out/figures/fig_a.png)

## Tracker reliability

![Link checks per run](figures/fig_b.png)

![Discovery lag](fig_c.png)
"""


@pytest.fixture
def report_dir(tmp_path: Path) -> Path:
    r = tmp_path / "report"
    (r / "out" / "figures").mkdir(parents=True)
    (r / "report.md").write_text(MD)
    for name in ("fig_a", "fig_b", "fig_c"):
        (r / "out" / "figures" / f"{name}.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (r / "out" / "results.json").write_text(
        json.dumps({"snapshot_ts": "2026-09-22T11:46:41+00:00"}))
    return r


def test_convert_keeps_tables_links_and_figures_and_collapses_sections(report_dir, tmp_path):
    out = tmp_path / "published"
    meta = convert(report_dir, out, "claude-fable-5-1", SKILL, "2026-09-29T00:00:00Z")
    html = (out / "report.html").read_text()
    assert html.startswith('<h1 class="report-title">Test briefing</h1>')
    assert html.count("<table") == 1
    assert "Claude%20Opus%205%20Card.pdf" in html and "Second row survives" in html
    assert "<br>" in html                                   # line break inside a cell
    assert 'href="https://systemcards.org/docs/opus.html"' in html
    # the lead stays visible; each ## section is a <details>, the first open
    assert html.index("Lead:") < html.index("<details")
    assert html.count("<details") == 2
    assert '<details class="section" id="sec-what-changed" open><summary><h2>' in html
    assert '<details class="section" id="sec-tracker-reliability"><summary><h2>' in html
    # figure paths are normalised by basename and copied
    for name in ("fig_a", "fig_b", "fig_c"):
        assert f'src="figures/{name}.png"' in html and (out / "figures" / f"{name}.png").exists()
    assert "<figcaption>Discovery lag</figcaption>" in html
    assert meta["snapshot"].startswith("2026-09-22") and meta["model"] == "claude-fable-5-1"
    assert meta["figures"] == 3 and 0 < meta["words"] < 60


def test_word_cap_counts_prose_not_tables(report_dir, tmp_path):
    convert(report_dir, tmp_path / "ok", "m", SKILL, max_words=80)
    with pytest.raises(SystemExit, match="words outside tables, cap is 10"):
        convert(report_dir, tmp_path / "p2", "m", SKILL, max_words=10)
    # a long table never trips the cap
    rows = "".join(f"| B{i} | {'word ' * 40} | v |\n" for i in range(50))
    md = (report_dir / "report.md").read_text().replace("| v3→v4 |\n", "| v3→v4 |\n" + rows)
    (report_dir / "report.md").write_text(md)
    convert(report_dir, tmp_path / "p3", "m", SKILL, max_words=80)


def test_too_few_figures_fails_loudly(report_dir, tmp_path):
    with pytest.raises(SystemExit, match="3 distinct figures, at least 4 required"):
        convert(report_dir, tmp_path / "published", "m", SKILL, min_figures=4)
    # the same file twice counts once; a caption with brackets or a title still resolves
    md = (report_dir / "report.md").read_text().replace(
        "![Discovery lag](fig_c.png)", '![Share [%] of docs](out/figures/fig_a.png "t")')
    (report_dir / "report.md").write_text(md)
    with pytest.raises(SystemExit, match="2 distinct figures"):
        convert(report_dir, tmp_path / "p2", "m", SKILL)


@pytest.mark.parametrize("img,msg", [
    ('<img src="https://evil.example/x.png">', "images must be PNG files"),
    ("![svg](figures/fig_a.svg)", "images must be PNG files"),
    ("![up](figures/../x.png)", "figure x.png missing")])     # basename only, no traversal
def test_non_local_or_non_png_image_fails(report_dir, tmp_path, img, msg):
    md = (report_dir / "report.md").read_text().replace("## Tracker reliability",
                                                        img + "\n\n## Tracker reliability")
    (report_dir / "report.md").write_text(md)
    with pytest.raises(SystemExit, match=msg):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def test_legitimate_pipes_do_not_trip_the_table_gate(report_dir, tmp_path):
    md = (report_dir / "report.md").read_text().replace(
        "Two documents changed; the table has the numbers.",
        "Either\\|or in prose, `a | b` in code, and a one-column table:\n\n"
        "| Only |\n|-|\n| x |\n\n```\n| a | b |\n|---|---|\n```\n")
    (report_dir / "report.md").write_text(md)
    convert(report_dir, tmp_path / "published", "m", SKILL)
    html = (tmp_path / "published" / "report.html").read_text()
    assert html.count("<table") == 2 and "Either|or" in html


def test_unclosed_raw_block_fails_instead_of_swallowing_the_report(report_dir, tmp_path):
    md = (report_dir / "report.md").read_text().replace("## Tracker reliability",
                                                        "<style>\n\n## Tracker reliability")
    (report_dir / "report.md").write_text(md)
    with pytest.raises(SystemExit, match="unclosed raw HTML block"):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def test_missing_figure_file_fails_loudly(report_dir, tmp_path):
    (report_dir / "out" / "figures" / "fig_c.png").unlink()
    with pytest.raises(SystemExit, match="fig_c.png missing"):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def test_broken_table_fails_loudly(report_dir, tmp_path):
    md = (report_dir / "report.md").read_text().replace("|---|---|---|\n", "")
    (report_dir / "report.md").write_text(md)
    with pytest.raises(SystemExit, match="table failed"):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def test_report_must_start_with_a_title(report_dir, tmp_path):
    (report_dir / "report.md").write_text("No title here\n\n## Section\n")
    with pytest.raises(SystemExit, match="must start with a single '# Title'"):
        convert(report_dir, tmp_path / "published", "m", SKILL)


def _publish(repo, report_dir: Path, meta: dict | None = None) -> None:
    pub = repo.root / "report" / "published"
    convert(report_dir, pub, "claude-fable-5-1", SKILL, "2026-09-29T00:00:00Z")
    if meta is not None:
        (pub / "meta.json").write_text(json.dumps(meta))


def test_analysis_page_has_disclaimer_and_nav(repo, report_dir):
    _publish(repo, report_dir)
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "analysis.html").read_text()
    assert "AI-generated report" in page
    assert "Claude Fable 5.1" in page and "claude-fable-5-1" in page
    assert f'href="{SKILL}"' in page
    assert 'src="./analysis/figures/fig_a.png"' in page
    assert (repo.site_dir / "analysis" / "figures" / "fig_a.png").exists()
    assert "<details" in page
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
    md = (report_dir / "report.md").read_text().replace(
        "## Tracker reliability",
        'See [this](javascript:alert(1)) and [that](https://ok.example/x).\n\n'
        '<script>alert(2)</script>\n\n<p onclick="alert(3)">x</p>\n\n## Tracker reliability')
    (report_dir / "report.md").write_text(md)
    convert(report_dir, tmp_path / "published", "m", SKILL)
    html = (tmp_path / "published" / "report.html").read_text()
    assert "javascript:" not in html and "<script" not in html and "onclick" not in html
    assert 'href="https://ok.example/x"' in html
    assert html.count("<table") == 1


def test_author_cannot_borrow_site_classes_or_ids(report_dir, tmp_path):
    md = (report_dir / "report.md").read_text().replace(
        "## Tracker reliability",
        '<div class="disclaimer" id="top"><p>Reviewed by a human.</p></div>\n\n'
        '## Tracker reliability')
    (report_dir / "report.md").write_text(md)
    convert(report_dir, tmp_path / "published", "m", SKILL)
    html = (tmp_path / "published" / "report.html").read_text()
    assert "Reviewed by a human" in html
    assert 'class="disclaimer"' not in html and 'id="top"' not in html


def test_published_dir_holds_only_html_figures_and_meta(repo, report_dir):
    """The site publishes HTML only: no source file and no PDF reach report/published."""
    _publish(repo, report_dir)
    names = {p.name for p in (repo.root / "report" / "published").iterdir()}
    assert names == {"report.html", "figures", "meta.json"}
    build_site(repo, run_pagefind=False)
    assert not (repo.site_dir / "analysis" / "report.md").exists()
