"""Validator tests — the component everything else trusts."""

from __future__ import annotations

import json

from cardtrack.db import connect
from cardtrack.propose import process_proposal

from .conftest import make_proposal


def counts(repo):
    conn = connect(repo.db_path)
    try:
        return {
            "documents": conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
            "versions": conn.execute("SELECT COUNT(*) FROM document_versions").fetchone()[0],
            "changelog": conn.execute("SELECT COUNT(*) FROM changelog").fetchone()[0],
        }
    finally:
        conn.close()


def test_add_happy_path(repo, http_server):
    http_server.set_html("/doc1", "The model was evaluated extensively.")
    result = process_proposal(repo, make_proposal(http_server), "run1")
    assert result.status == "written"
    assert result.slug == "testlab-testmodel-1-system-card"

    conn = connect(repo.db_path)
    doc = conn.execute("SELECT * FROM documents WHERE slug = ?", (result.slug,)).fetchone()
    ver = conn.execute("SELECT * FROM document_versions WHERE document_id = ?",
                       (doc["id"],)).fetchone()
    entry = conn.execute("SELECT * FROM changelog WHERE action='add'").fetchone()
    conn.close()

    assert doc["status"] == "active"
    assert doc["is_independent"] == 0
    assert json.loads(doc["model_names"]) == ["TestModel 1"]
    assert (repo.root / ver["raw_path"]).exists(), "raw blob stored"
    assert (repo.root / ver["text_path"]).exists(), "extracted text stored"
    detail = json.loads(entry["detail"])
    assert detail["justification"] and detail["slug"] == result.slug


def test_idempotent_rerun_is_noop(repo, http_server):
    http_server.set_html("/doc1", "Stable content.")
    first = process_proposal(repo, make_proposal(http_server), "run1")
    assert first.status == "written"
    before = counts(repo)
    again = process_proposal(repo, make_proposal(http_server), "run1")
    assert again.status == "duplicate"
    assert again.reason == "fingerprint_already_stored"
    assert counts(repo) == before, "no new rows on re-run"


def test_same_url_new_content_becomes_new_version(repo, http_server):
    http_server.set_html("/doc1", "Original content of the card.")
    first = process_proposal(repo, make_proposal(http_server), "run1")
    http_server.set_html("/doc1", "Updated content: new evaluations added.")
    second = process_proposal(repo, make_proposal(http_server), "run2")
    assert second.status == "written"
    assert second.document_id == first.document_id
    c = counts(repo)
    assert c["documents"] == 1 and c["versions"] == 2


def test_unknown_publisher_rejected(repo, http_server):
    http_server.set_html("/doc1", "content")
    result = process_proposal(repo, make_proposal(http_server, publisher="evilcorp"), "run1")
    assert result.status == "rejected"
    assert "publisher_on_allowlist" in result.reason
    assert counts(repo)["documents"] == 0


def test_unfetchable_rejected(repo, http_server):
    result = process_proposal(repo, make_proposal(http_server, path="/missing-404"), "run1")
    assert result.status == "rejected"
    assert "document_retrievable" in result.reason


def test_oversize_rejected(repo_root, http_server):
    from cardtrack.repo import Repo

    from .conftest import Route, write_test_config

    write_test_config(repo_root, http_server, caps={"max_fetch_bytes": 1000})
    http_server.routes["/big"] = Route(body=b"x" * 5000, content_type="text/html")
    result = process_proposal(Repo(root=repo_root), make_proposal(http_server, path="/big"), "run1")
    assert result.status == "rejected"
    assert "max_fetch_bytes" in result.reason


def test_non_http_url_rejected(repo):
    proposal = {
        "action": "add", "url": "file:///etc/passwd", "title": "x",
        "publisher": "testlab", "doc_type": "system_card", "model_names": ["M"],
        "publication_date": "2026-03-01", "justification": "j",
        "criteria": {"primary_source": True, "about_a_specific_model_or_eval": True},
        "evidence_urls": [], "source_of_lead": "manual",
    }
    result = process_proposal(repo, proposal, "run1")
    assert result.status == "rejected"
    assert "url_invalid" in result.reason


def test_before_date_floor_rejected(repo, http_server):
    http_server.set_html("/old-doc", "Ancient card.")
    result = process_proposal(
        repo, make_proposal(http_server, path="/old-doc", publication_date="2024-06-01"), "run1")
    assert result.status == "rejected"
    assert "before_min_publication_date" in result.reason


def test_null_date_admitted_and_flagged(repo, http_server):
    http_server.set_html("/undated", "No date anywhere.")
    result = process_proposal(
        repo, make_proposal(http_server, path="/undated", publication_date=None), "run1")
    assert result.status == "written"
    conn = connect(repo.db_path)
    doc = conn.execute("SELECT publication_date FROM documents WHERE slug=?",
                       (result.slug,)).fetchone()
    detail = json.loads(conn.execute(
        "SELECT detail FROM changelog WHERE action='add' AND document_id=?",
        (result.document_id,)).fetchone()[0])
    conn.close()
    assert doc["publication_date"] is None
    assert detail.get("date_unknown") is True, "provenance flags the unknown date"


def test_unattested_criteria_files_issue(repo, http_server):
    http_server.set_html("/doc-x", "content")
    result = process_proposal(
        repo, make_proposal(http_server, path="/doc-x", criteria={"primary_source": True}),
        "run1")  # about_a_specific_model_or_eval missing → uncertain
    assert result.status == "issue_filed"
    assert "about_a_specific_model_or_eval" in result.reason


def test_tier2_writes_row_with_tier_recorded(repo, http_server):
    """Tier is provenance, not a gate: allowlisted publishers auto-merge."""
    http_server.set_html("/tier2-doc", "A tier-2 publisher card.")
    result = process_proposal(
        repo, make_proposal(http_server, path="/tier2-doc", publisher="tier2lab"), "run1")
    assert result.status == "written"
    conn = connect(repo.db_path)
    detail = json.loads(conn.execute(
        "SELECT detail FROM changelog WHERE action='add' AND document_id=?",
        (result.document_id,)).fetchone()[0])
    conn.close()
    assert detail["tier"] == 2, "tier recorded in provenance"


def test_logical_duplicate_same_text_skipped(repo, http_server):
    """Same publisher/title/model AND near-identical text at a new URL = a genuine
    re-post → skipped as a duplicate (no review issue, no new row)."""
    body = ("The model was evaluated across cyber, bio and autonomy benchmarks with "
            "detailed results and methodology for each capability area covered.")
    http_server.set_html("/doc1", body)
    http_server.set_html("/doc1-mirror", body + " Minor trailing edit.")
    assert process_proposal(repo, make_proposal(http_server), "run1").status == "written"
    result = process_proposal(
        repo, make_proposal(http_server, path="/doc1-mirror",
                            model_names=["testmodel 1"]),  # normalized-equal name
        "run1")
    assert result.status == "duplicate"
    assert "logical_duplicate" in result.reason
    assert counts(repo)["documents"] == 1


def test_logical_title_collision_distinct_text_admitted(repo, http_server):
    """Same publisher/title/model but DIFFERENT text (e.g. two methodology reports
    named alike) is a distinct document → admitted, not flagged for review."""
    http_server.set_html("/method-a",
                         "Coding and general evaluation methodology: SWE-bench, "
                         "terminal tasks, agentic tool use, grading rules for code.")
    http_server.set_html("/method-b",
                         "Multimodal evaluation methodology: visual perception, "
                         "chart understanding, spatial reasoning, image QA protocols.")
    assert process_proposal(repo, make_proposal(
        http_server, path="/method-a", title="Muse Eval Methodology",
        model_names=["MuseModel"]), "run1").status == "written"
    r2 = process_proposal(repo, make_proposal(
        http_server, path="/method-b", title="Muse Eval Methodology",
        model_names=["MuseModel"]), "run1")
    assert r2.status == "written", (r2.status, r2.reason)
    assert counts(repo)["documents"] == 2


def test_distinct_evaluator_reports_same_model_not_flagged(repo, http_server):
    """Evaluators publish many reports covering the same models; different title +
    different date must pass the logical-dup gate (mirrors are caught by content)."""
    http_server.set_html("/eval-1", "Cyber capabilities evaluation findings.")
    http_server.set_html("/eval-2", "Cheating behaviour analysis, entirely different.")
    r1 = process_proposal(repo, make_proposal(
        http_server, path="/eval-1", publisher="testeval", doc_type="independent_eval",
        title="Our evaluation of FooModel cyber capabilities",
        publication_date="2026-04-30", model_names=["FooModel"]), "run1")
    assert r1.status == "written"
    r2 = process_proposal(repo, make_proposal(
        http_server, path="/eval-2", publisher="testeval", doc_type="independent_eval",
        title="Cheating behaviour in frontier model evaluations",
        publication_date="2026-07-21", model_names=["FooModel", "BarModel"]), "run1")
    assert r2.status == "written", (r2.status, r2.reason)


def test_content_duplicate_same_publisher_skipped(repo, http_server):
    """Identical content at a new URL under the SAME publisher = a mirror/moved
    copy → skipped (no new row, no review issue)."""
    http_server.set_html("/doc1", "Identical bytes served twice.")
    http_server.set_html("/doc1-copy", "Identical bytes served twice.")
    assert process_proposal(repo, make_proposal(http_server), "run1").status == "written"
    result = process_proposal(
        repo, make_proposal(http_server, path="/doc1-copy", title="Other Title",
                            model_names=["OtherModel"]), "run1")
    assert result.status == "duplicate"
    assert "content_duplicate" in result.reason and "same-publisher" in result.reason
    assert counts(repo)["documents"] == 1


def test_content_duplicate_cross_publisher_admitted_as_copublication(repo, http_server):
    """Identical content under a DIFFERENT allowlisted publisher = a co-publication
    (e.g. a launch partner's own copy) → admitted and flagged, not filed for review."""
    http_server.set_html("/doc1", "Identical launch-day card bytes.")
    http_server.set_html("/copub", "Identical launch-day card bytes.")
    first = process_proposal(repo, make_proposal(http_server), "run1")
    assert first.status == "written"
    r2 = process_proposal(repo, make_proposal(
        http_server, path="/copub", publisher="tier2lab",
        model_names=["TestModel 1"]), "run1")
    assert r2.status == "written", (r2.status, r2.reason)
    assert counts(repo)["documents"] == 2
    conn = connect(repo.db_path)
    detail = conn.execute("SELECT detail FROM changelog WHERE document_id=? AND "
                          "action='add'", (r2.document_id,)).fetchone()[0]
    conn.close()
    assert json.loads(detail).get("cross_publisher_copy_of") == first.slug


def test_caps_enforced(repo_root, http_server):
    from cardtrack.repo import Repo

    from .conftest import write_test_config

    write_test_config(repo_root, http_server, caps={"max_new_documents_per_run": 2})
    repo = Repo(root=repo_root)
    for i in range(2):
        http_server.set_html(f"/capdoc{i}", f"Unique content number {i}.")
        r = process_proposal(
            repo, make_proposal(http_server, path=f"/capdoc{i}",
                                model_names=[f"CapModel {i}"]), "caprun")
        assert r.status == "written"
    http_server.set_html("/capdoc2", "One more.")
    r = process_proposal(
        repo, make_proposal(http_server, path="/capdoc2", model_names=["CapModel 2"]),
        "caprun")
    assert r.status == "rejected"
    assert "cap_exceeded" in r.reason
    # caps are a rolling window: a fresh run id must NOT reset them;
    # window expiry is covered in test_guards.py
    http_server.set_html("/capdoc3", "Next day content.")
    r = process_proposal(
        repo, make_proposal(http_server, path="/capdoc3", model_names=["CapModel 3"]),
        "caprun2")
    assert r.status == "rejected" and "cap_exceeded" in r.reason


def test_redirected_add_routes_to_existing_doc(repo, http_server):
    http_server.set_html("/doc1", "Redirect target content.")
    assert process_proposal(repo, make_proposal(http_server), "run1").status == "written"
    http_server.set_redirect("/doc1-alias", http_server.url("/doc1"), permanent=True)
    result = process_proposal(
        repo, make_proposal(http_server, path="/doc1-alias"), "run2")
    assert result.status == "duplicate", "alias resolves to known doc, same content → no-op"
    assert counts(repo)["documents"] == 1


def test_status_change_and_noop(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    r = process_proposal(repo, {
        "action": "status_change", "slug": added.slug, "new": "superseded",
        "justification": "Replaced by v2 card", "evidence_urls": ["https://example.com"],
    }, "run2")
    assert r.status == "written"
    r2 = process_proposal(repo, {
        "action": "status_change", "slug": added.slug, "new": "superseded",
        "justification": "again", "evidence_urls": [],
    }, "run2")
    assert r2.status == "noop"
    conn = connect(repo.db_path)
    assert conn.execute("SELECT status FROM documents WHERE slug=?",
                        (added.slug,)).fetchone()[0] == "superseded"
    conn.close()


def test_soft_delete_keeps_row(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    process_proposal(repo, {
        "action": "status_change", "slug": added.slug, "new": "removed",
        "justification": "curatorial removal", "evidence_urls": [],
    }, "run2")
    conn = connect(repo.db_path)
    assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM site_documents").fetchone()[0] == 0
    conn.close()


def test_field_update_with_stale_guard(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    stale = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "title",
        "old": "Wrong Old Title", "new": "New Title",
        "justification": "fix title", "evidence_urls": [],
    }, "run2")
    assert stale.status == "rejected" and "stale_old_value" in stale.reason
    good = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "title",
        "old": "Test Model System Card", "new": "Corrected Title",
        "justification": "fix title per issue #1", "evidence_urls": [],
    }, "run2")
    assert good.status == "written"
    conn = connect(repo.db_path)
    assert conn.execute("SELECT title FROM documents WHERE slug=?",
                        (added.slug,)).fetchone()[0] == "Corrected Title"
    conn.close()


def test_canonical_url_update_appends_alt(repo, http_server):
    http_server.set_html("/doc1", "content here")
    http_server.set_html("/doc1-new-home", "content here")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    old_url = http_server.url("/doc1")
    r = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "canonical_url",
        "new": http_server.url("/doc1-new-home"),
        "justification": "publisher moved the card", "evidence_urls": [old_url],
    }, "run2", actor="human")
    assert r.status == "written"
    conn = connect(repo.db_path)
    doc = conn.execute("SELECT * FROM documents WHERE slug=?", (added.slug,)).fetchone()
    conn.close()
    assert doc["canonical_url"].endswith("/doc1-new-home")
    assert old_url in json.loads(doc["alt_urls"])


def test_canonical_url_is_operator_only(repo, http_server):
    """The agent cannot repoint a public source link; it must go through the
    operator (related_urls kind full_document -> operator promotes)."""
    http_server.set_html("/doc1", "content here")
    http_server.set_html("/doc1-new-home", "content here")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    r = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "canonical_url",
        "new": http_server.url("/doc1-new-home"),
        "justification": "move", "evidence_urls": []}, "run2", actor="agent")
    assert r.status == "rejected" and "operator-only" in r.reason
    conn = connect(repo.db_path)
    url = conn.execute("SELECT canonical_url FROM documents WHERE slug=?",
                       (added.slug,)).fetchone()[0]
    conn.close()
    assert url.endswith("/doc1"), "the agent proposal must not repoint the link"


def test_invalid_schema_rejected(repo):
    r = process_proposal(repo, {"action": "add", "url": "https://example.com"}, "run1")
    assert r.status == "rejected" and "invalid_schema" in r.reason
    r2 = process_proposal(repo, {"action": "explode"}, "run1")
    assert r2.status == "rejected" and "invalid_schema" in r2.reason


def test_slug_collision_gets_suffix(repo, http_server):
    http_server.set_html("/doc1", "Card one content.")
    http_server.set_html("/doc2", "Card two content, different.")
    first = process_proposal(repo, make_proposal(http_server), "run1")
    second = process_proposal(
        repo, make_proposal(http_server, path="/doc2", title="Another card, same model",
                            doc_type="system_card",
                            model_names=["TestModel 1B"]), "run1")
    # different model → different slug, no suffix needed
    assert second.slug != first.slug

    # force a collision: same publisher/model/type at a new URL but distinct logical
    # identity is caught as logical duplicate, so collision testing goes through
    # the derive function directly
    from cardtrack.db import connect as dbconnect
    from cardtrack.identity import derive_slug

    conn = dbconnect(repo.db_path)
    slug = derive_slug(conn, "testlab", ["TestModel 1"], "system_card")
    conn.close()
    assert slug == "testlab-testmodel-1-system-card-2"


def test_openness_validated_on_add_and_field_update(repo, http_server):
    """openness accepts only the three taxonomy values (or null); invalid rejects."""
    http_server.set_html("/doc1", "The model was evaluated extensively.")
    bad = process_proposal(repo, make_proposal(http_server, openness="open_source"), "run1")
    assert bad.status == "rejected"
    assert "openness" in bad.reason

    added = process_proposal(
        repo, make_proposal(http_server, openness="open_weight_permissive"), "run1")
    assert added.status == "written"
    conn = connect(repo.db_path)
    row = conn.execute("SELECT openness FROM documents WHERE slug = ?",
                       (added.slug,)).fetchone()
    conn.close()
    assert row["openness"] == "open_weight_permissive"

    # clearing to null is how multi-class / non-model-specific docs are marked
    upd = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "openness",
        "old": "open_weight_permissive", "new": None,
        "justification": "spans models in different openness classes",
        "evidence_urls": ["https://example.com/license"]}, "run2")
    assert upd.status == "written"
    conn = connect(repo.db_path)
    row = conn.execute("SELECT openness FROM documents WHERE slug = ?",
                       (added.slug,)).fetchone()
    conn.close()
    assert row["openness"] is None

    for retired in ("mixed", "totally_open"):
        bad2 = process_proposal(repo, {
            "action": "field_update", "slug": added.slug, "field": "openness",
            "new": retired, "justification": "nope",
            "evidence_urls": ["https://example.com/license"]}, "run3")
        assert bad2.status == "rejected"
