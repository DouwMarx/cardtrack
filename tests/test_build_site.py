"""Site build tests, including the XSS posture: everything web-derived is escaped."""

from __future__ import annotations

import json

from cardtrack.propose import process_proposal
from cardtrack.repo import Repo
from cardtrack.sitebuild import build_site

from .conftest import make_proposal, write_test_config


def test_build_outputs(repo, http_server):
    http_server.set_html("/doc1", "The model was evaluated on autonomy tasks.")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    summary = build_site(repo, run_pagefind=False)
    assert summary["documents"] == 1

    meta = json.loads((repo.site_dir / "data" / "metadata.json").read_text())
    assert meta["documents"][0]["slug"] == added.slug
    assert meta["documents"][0]["version_count"] == 1
    assert "notes" not in meta["documents"][0]

    page = (repo.site_dir / "docs" / f"{added.slug}.html").read_text()
    assert "Test Model System Card" in page
    assert "data-pagefind-body" in page
    assert "autonomy tasks" in page
    assert "A test document that meets all criteria." in page, "provenance shows justification"
    assert "primary_source" in page, "provenance shows criteria attestations"
    assert (repo.site_dir / "index.html").exists()
    assert (repo.site_dir / "search.html").exists()
    assert (repo.site_dir / "style.css").exists()
    assert (repo.site_dir / "app.js").exists()


def test_extracted_text_is_escaped(repo, http_server):
    payload = 'Injected <script>alert("xss")</script> & <img src=x onerror=alert(1)>'
    http_server.set_html("/evil-doc", payload)
    added = process_proposal(
        repo, make_proposal(http_server, path="/evil-doc", model_names=["EvilModel"],
                            title='Evil <script>document.title</script> Card'), "run1")
    assert added.status == "written"
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{added.slug}.html").read_text()
    assert "<script>alert(" not in page
    assert "<script>document.title</script>" not in page
    assert "&lt;script&gt;" in page


def test_removed_doc_page_pruned(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    build_site(repo, run_pagefind=False)
    page_path = repo.site_dir / "docs" / f"{added.slug}.html"
    assert page_path.exists()

    process_proposal(repo, {"action": "status_change", "slug": added.slug, "new": "removed",
                            "justification": "test removal", "evidence_urls": []}, "run2")
    build_site(repo, run_pagefind=False)
    assert not page_path.exists(), "soft-deleted docs leave the site (rows are kept)"
    meta = json.loads((repo.site_dir / "data" / "metadata.json").read_text())
    assert meta["documents"] == []


def test_dead_doc_keeps_page_with_labeled_link(repo, http_server):
    http_server.set_html("/doc1", "content stays available")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    process_proposal(repo, {"action": "status_change", "slug": added.slug, "new": "dead",
                            "justification": "404 x3", "evidence_urls": []}, "run2")
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{added.slug}.html").read_text()
    assert "link was dead at last check" in page
    assert "content stays available" in page


def test_issue_link_present_when_repo_configured(repo_root, http_server):
    write_test_config(repo_root, http_server, gh_repo="example/cardtrack")
    repo = Repo(root=repo_root)
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{added.slug}.html").read_text()
    assert "https://github.com/example/cardtrack/issues/new?labels=data-error" in page
    assert added.slug in page
