"""Tests for the 2026-08-31 roadmap features: risk_domains tags, related_urls,
access_policy doc_type + restricted openness, version change summaries, the
fingerprint furniture filter, and the outbound secret scan."""

from __future__ import annotations

import json
import sqlite3

from cardtrack.db import DOC_TYPES, connect
from cardtrack.extract import fingerprint_text
from cardtrack.monitor import run_monitor
from cardtrack.propose import process_proposal
from cardtrack.sitebuild import build_site

from .conftest import make_proposal

# ---------------------------------------------------------------- risk_domains

def test_risk_domains_add_and_export(repo, http_server):
    http_server.set_html("/doc1", "Bio uplift and cyber evals inside.")
    res = process_proposal(
        repo, make_proposal(http_server, risk_domains=["cyber", "cbrn", "cyber"]),
        "run1")
    assert res.status == "written"
    conn = connect(repo.db_path)
    row = conn.execute("SELECT risk_domains FROM documents WHERE slug = ?",
                       (res.slug,)).fetchone()
    conn.close()
    assert json.loads(row["risk_domains"]) == ["cbrn", "cyber"]  # sorted, deduped

    build_site(repo, run_pagefind=False)
    meta = json.loads((repo.site_dir / "data" / "metadata.json").read_text())
    doc = next(d for d in meta["documents"] if d["slug"] == res.slug)
    assert doc["risk_domains"] == ["cbrn", "cyber"]
    assert meta["risk_domains"]["cbrn"] == "CBRN"  # vocabulary → labels for the UI
    page = (repo.site_dir / "docs" / f"{res.slug}.html").read_text()
    assert "Cyber offence" in page and 'data-pagefind-filter="risk:cbrn"' in page


def test_risk_domains_unknown_tag_rejected(repo, http_server):
    http_server.set_html("/doc1", "content")
    res = process_proposal(
        repo, make_proposal(http_server, risk_domains=["cyber", "vibes"]), "run1")
    assert res.status == "rejected"
    assert "vibes" in res.reason


def test_risk_domains_field_update_with_stale_guard(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    ok = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "risk_domains",
        "old": [], "new": ["loss_of_control"],
        "justification": "alignment assessment section", "evidence_urls": []}, "run2")
    assert ok.status == "written"
    stale = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "risk_domains",
        "old": [], "new": ["cbrn"],
        "justification": "j", "evidence_urls": []}, "run3")
    assert stale.status == "rejected" and "stale_old_value" in stale.reason


# ---------------------------------------------------------------- related_urls

def test_related_urls_add_field_update_and_render(repo, http_server):
    http_server.set_html("/doc1", "The full report.")
    http_server.set_html("/announce", "We are releasing a model.")
    announce = http_server.url("/announce")
    res = process_proposal(
        repo, make_proposal(http_server, related_urls=[
            {"url": announce, "kind": "announcement", "note": "launch post"}]),
        "run1")
    assert res.status == "written"
    conn = connect(repo.db_path)
    row = conn.execute("SELECT related_urls FROM documents WHERE slug = ?",
                       (res.slug,)).fetchone()
    conn.close()
    stored = json.loads(row["related_urls"])
    assert stored[0]["kind"] == "announcement" and stored[0]["note"] == "launch post"

    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{res.slug}.html").read_text()
    assert "launch post" in page and announce in page

    bad_kind = process_proposal(repo, {
        "action": "field_update", "slug": res.slug, "field": "related_urls",
        "new": [{"url": announce, "kind": "press_release"}],
        "justification": "j", "evidence_urls": []}, "run2")
    assert bad_kind.status == "rejected" and "kind" in bad_kind.reason


def test_related_urls_must_not_claim_own_url(repo, http_server):
    """alt_urls is dedup identity; a related url equal to the document's own URL
    would silently shadow it."""
    http_server.set_html("/doc1", "content")
    res = process_proposal(
        repo, make_proposal(http_server, related_urls=[
            {"url": http_server.url("/doc1"), "kind": "announcement"}]), "run1")
    assert res.status == "rejected" and "own URL" in res.reason


# ------------------------------------------- access_policy + restricted openness

def test_access_policy_doc_type_and_restricted_openness(repo, http_server):
    http_server.set_html("/access", "Trusted access program for TestModel RS.")
    res = process_proposal(repo, make_proposal(
        http_server, path="/access", doc_type="access_policy",
        title="TestModel RS Trusted Access Overview",
        model_names=["TestModel RS"], openness="restricted"), "run1")
    assert res.status == "written"
    assert res.slug.endswith("access-policy")
    conn = connect(repo.db_path)
    row = conn.execute("SELECT doc_type, openness FROM documents WHERE slug = ?",
                       (res.slug,)).fetchone()
    conn.close()
    assert row["doc_type"] == "access_policy" and row["openness"] == "restricted"


def test_doc_type_field_update(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    ok = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "doc_type",
        "old": "system_card", "new": "access_policy",
        "justification": "relabel: this documents who may access the model",
        "evidence_urls": []}, "run2")
    assert ok.status == "written"
    bad = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "doc_type",
        "new": "blogpost", "justification": "j", "evidence_urls": []}, "run3")
    assert bad.status == "rejected"


def test_old_check_constraint_db_is_rebuilt(tmp_path):
    """A live DB created before access_policy existed carries the old CHECK baked
    in; connect() must rebuild the table (SQLite cannot ALTER a CHECK)."""
    db_path = tmp_path / "old.sqlite"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE documents (
          id INTEGER PRIMARY KEY, slug TEXT UNIQUE NOT NULL, title TEXT NOT NULL,
          publisher TEXT NOT NULL,
          doc_type TEXT NOT NULL CHECK (doc_type IN
            ('model_card','system_card','independent_eval','addendum','other')),
          is_independent INTEGER NOT NULL DEFAULT 0,
          model_names TEXT NOT NULL DEFAULT '[]', publication_date TEXT,
          canonical_url TEXT UNIQUE NOT NULL, alt_urls TEXT NOT NULL DEFAULT '[]',
          status TEXT NOT NULL DEFAULT 'active', first_seen TEXT NOT NULL,
          last_checked TEXT, last_changed TEXT, source_of_lead TEXT, notes TEXT)""")
    conn.execute("""
        CREATE TABLE document_versions (
          id INTEGER PRIMARY KEY,
          document_id INTEGER NOT NULL REFERENCES documents(id),
          content_hash TEXT NOT NULL, content_fingerprint TEXT NOT NULL,
          fetched_at TEXT NOT NULL, content_type TEXT, byte_size INTEGER,
          raw_path TEXT NOT NULL, text_path TEXT,
          extraction TEXT NOT NULL DEFAULT '{}',
          UNIQUE (document_id, content_fingerprint))""")
    conn.execute(
        "INSERT INTO documents (slug, title, publisher, doc_type, canonical_url, "
        "first_seen) VALUES ('a-b-c', 'T', 'p', 'model_card', 'https://x.test/a', 'ts')")
    conn.execute(
        "INSERT INTO document_versions (document_id, content_hash, "
        "content_fingerprint, fetched_at, raw_path) VALUES (1, 'h', 'f', 'ts', 'r')")
    conn.commit()
    conn.close()

    conn = connect(db_path)
    kept = conn.execute("SELECT * FROM documents WHERE slug = 'a-b-c'").fetchone()
    assert kept["title"] == "T" and kept["risk_domains"] == "[]"
    conn.execute(
        "INSERT INTO documents (slug, title, publisher, doc_type, canonical_url, "
        "first_seen) VALUES ('d-e-f', 'U', 'p', 'access_policy', 'https://x.test/b', 'ts')")
    conn.commit()
    # the rebuild must not leave child FKs pointing at a renamed/dropped table
    # (the failure mode of ALTER TABLE ... RENAME on the referenced table)
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    ver_sql = conn.execute("SELECT sql FROM sqlite_master "
                           "WHERE name='document_versions'").fetchone()["sql"]
    assert "documents_new" not in ver_sql and "documents_old" not in ver_sql
    conn.execute(
        "INSERT INTO document_versions (document_id, content_hash, "
        "content_fingerprint, fetched_at, raw_path) VALUES (1, 'h2', 'f2', 'ts', 'r')")
    conn.execute("DELETE FROM document_versions WHERE content_hash = 'h2'")
    conn.commit()
    sql = conn.execute("SELECT sql FROM sqlite_master WHERE name='documents'"
                       ).fetchone()["sql"]
    assert all(f"'{t}'" in sql for t in DOC_TYPES)
    conn.close()


# ---------------------------------------------------------------- annotate_version

def _two_versions(repo, http_server):
    http_server.set_html("/doc1", "Original content of the card.")
    first = process_proposal(repo, make_proposal(http_server), "run1")
    http_server.set_html("/doc1", "Updated content: pass@4 corrected to 1.5%.")
    second = process_proposal(repo, make_proposal(http_server), "run2")
    assert second.status == "written" and second.version_id != first.version_id
    return first, second


def test_annotate_version_happy_path(repo, http_server):
    _first, second = _two_versions(repo, http_server)
    res = process_proposal(repo, {
        "action": "annotate_version", "slug": second.slug,
        "version_id": second.version_id,
        "summary": "Corrected pass@4 score from 0.4% to 1.5%.",
        "justification": "diff shows the score correction",
        "evidence_urls": []}, "run3")
    assert res.status == "written"
    conn = connect(repo.db_path)
    row = conn.execute("SELECT change_summary FROM document_versions WHERE id = ?",
                       (second.version_id,)).fetchone()
    conn.close()
    assert "1.5%" in row["change_summary"]

    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{second.slug}.html").read_text()
    assert "Corrected pass@4" in page and "initial version" in page


def test_annotate_version_gates(repo, http_server):
    first, second = _two_versions(repo, http_server)
    base = {"action": "annotate_version", "slug": second.slug,
            "justification": "j", "evidence_urls": []}
    initial = process_proposal(repo, {**base, "version_id": first.version_id,
                                      "summary": "x"}, "r")
    assert initial.status == "rejected" and "no_predecessor" in initial.reason
    url = process_proposal(repo, {**base, "version_id": second.version_id,
                                  "summary": "see https://evil.test"}, "r")
    assert url.status == "rejected" and "plain text" in url.reason
    markup = process_proposal(repo, {**base, "version_id": second.version_id,
                                     "summary": "<script>x</script>"}, "r")
    assert markup.status == "rejected"
    long = process_proposal(repo, {**base, "version_id": second.version_id,
                                   "summary": "y" * 501}, "r")
    assert long.status == "rejected" and "500" in long.reason
    missing = process_proposal(repo, {**base, "version_id": 99999, "summary": "x"}, "r")
    assert missing.status == "rejected" and "unknown_version" in missing.reason


def test_justification_length_cap(repo, http_server):
    http_server.set_html("/doc1", "content")
    res = process_proposal(
        repo, make_proposal(http_server, justification="x" * 8001), "run1")
    assert res.status == "rejected" and "8000" in res.reason


# ---------------------------------------------------------------- fingerprint filter

FURNITURE_PATTERNS = (r"^Downloads last month", r"^\s*[\d,.]+\s*$")


def test_furniture_lines_do_not_change_fingerprint():
    a = "Model card intro.\nEval table: 42%\nDownloads last month\n1,234"
    b = "Model card intro.\nEval table: 42%\nDownloads last month\n999,999"
    assert fingerprint_text(a) != fingerprint_text(b)  # unfiltered: churn
    assert (fingerprint_text(a, FURNITURE_PATTERNS)
            == fingerprint_text(b, FURNITURE_PATTERNS))


def test_substantive_change_still_changes_fingerprint():
    a = "Model card intro.\nEval table: 42%\nDownloads last month"
    b = "Model card intro.\nEval table: 43%\nDownloads last month"
    assert (fingerprint_text(a, FURNITURE_PATTERNS)
            != fingerprint_text(b, FURNITURE_PATTERNS))


def test_footer_truncation_only_in_last_quarter():
    body = "\n".join(f"line {i}" for i in range(20))
    with_footer = body + "\nRelated content\nrotating blurb A"
    with_other_footer = body + "\nRelated content\nrotating blurb B"
    assert (fingerprint_text(with_footer, FURNITURE_PATTERNS)
            == fingerprint_text(with_other_footer, FURNITURE_PATTERNS))
    # an early "Related content" heading must NOT blind the fingerprint to real
    # content after it
    early = "Related content\n" + body + "\nreal ending A"
    early2 = "Related content\n" + body + "\nreal ending B"
    assert (fingerprint_text(early, FURNITURE_PATTERNS)
            != fingerprint_text(early2, FURNITURE_PATTERNS))


def test_trailing_read_more_pairs_stripped():
    """Blog pages end with rotating (teaser, "Read more") pairs and no heading —
    the alternating tail is stripped pairwise from the fingerprint."""
    body = "\n".join(f"line {i}" for i in range(30))
    a = body + "\nTeaser about topic A\nRead more\nTeaser two A\nRead more"
    b = body + "\nTeaser about topic B\nRead more\nTeaser two B\nRead more"
    assert (fingerprint_text(a, FURNITURE_PATTERNS)
            == fingerprint_text(b, FURNITURE_PATTERNS))
    changed = body.replace("line 3", "line 3 CHANGED") \
        + "\nTeaser about topic A\nRead more"
    assert (fingerprint_text(a, FURNITURE_PATTERNS)
            != fingerprint_text(changed, FURNITURE_PATTERNS))


def test_monitor_ignores_furniture_only_change(repo_root, http_server):
    """End-to-end: with patterns configured, a furniture-only page change mints no
    new version, and updated_docs.json lists real updates for the agent."""
    import yaml

    from cardtrack.repo import Repo

    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())
    settings["fingerprint"] = {"ignore_line_patterns": list(FURNITURE_PATTERNS)}
    settings_path.write_text(yaml.safe_dump(settings))
    repo = Repo(root=repo_root)

    from .conftest import Route

    def page(prose: str, downloads: str) -> None:
        # furniture on its own block elements, like a real HF sidebar
        html = (f"<!DOCTYPE html><html><head><title>Doc</title></head><body><main>"
                f"<h1>Doc</h1><p>{prose}</p>"
                f"<p>Downloads last month</p><p>{downloads}</p></main></body></html>")
        http_server.routes["/doc1"] = Route(body=html.encode())

    http_server.routes.pop("/index-page", None)
    page("Stable prose.", "1,000")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    assert added.status == "written"

    page("Stable prose.", "2,000")
    run_monitor(repo, "run2")
    conn = connect(repo.db_path)
    count = conn.execute("SELECT COUNT(*) FROM document_versions").fetchone()[0]
    conn.close()
    assert count == 1, "furniture-only change must not mint a version"

    page("New evals added.", "2,000")
    run_monitor(repo, "run3")
    conn = connect(repo.db_path)
    count = conn.execute("SELECT COUNT(*) FROM document_versions").fetchone()[0]
    conn.close()
    assert count == 2, "substantive change must mint a version"

    updated = json.loads((repo_root / "logs" / "updated_docs.json").read_text())
    assert len(updated["updated_docs"]) == 1
    entry = updated["updated_docs"][0]
    assert entry["slug"] == added.slug and entry["added_lines"] >= 1
    assert (repo_root / entry["diff_path"]).exists()


# ---------------------------------------------------------------- secret scan

def test_secret_scan_catches_planted_token(repo_root):
    from .conftest import run_cli

    (repo_root / "logs").mkdir(exist_ok=True)
    report = repo_root / "logs" / "run_report.md"
    report.write_text("Checked 3 docs. ghp_" + "a1B2" * 10 + " end.\n")
    code, res, err = run_cli("secret_scan.py", str(report), root=repo_root)
    assert code == 3 and res["status"] == "findings", (res, err)
    assert res["findings"][0]["pattern"] == "github_token"
    hold = (repo_root / "logs" / "SECURITY_HOLD.md").read_text()
    assert "github_token" in hold
    assert "ghp_" not in hold, "findings must never quote the secret"


def test_secret_scan_matches_local_env_values(repo_root):
    from .conftest import run_cli

    (repo_root / ".env").write_text("CLOUDFLARE_API_TOKEN=supersecretvalue123456\n")
    (repo_root / "logs").mkdir(exist_ok=True)
    leak = repo_root / "logs" / "PROPOSALS.md"
    leak.write_text("odd text supersecretvalue123456 in prose\n")
    code, res, err = run_cli("secret_scan.py", str(leak), root=repo_root)
    assert code == 3 and res["findings"][0]["pattern"] == "literal_local_secret"


def test_secret_scan_clean_prose_passes(repo_root):
    from .conftest import run_cli

    (repo_root / "logs").mkdir(exist_ok=True)
    report = repo_root / "logs" / "run_report.md"
    report.write_text("Checked 12 candidates; proposed 2 adds; both written.\n"
                      "Verified https://example.test/card.pdf resolves.\n")
    code, res, err = run_cli("secret_scan.py", str(report), root=repo_root)
    assert code == 0 and res["status"] == "clean", (res, err)


def test_secret_scan_all_patterns(repo_root):
    """Every high-precision pattern trips on a synthetic match."""
    from .conftest import run_cli
    (repo_root / "logs").mkdir(exist_ok=True)
    samples = {
        "anthropic_api_key": "sk-ant-" + "A1b2C3d4E5f6G7h8I9j0",
        "openai_style_key": "sk-proj-" + "A1b2C3d4E5f6G7h8I9j0",
        "github_token": "ghp_" + "a1B2c3D4" * 5,
        "aws_access_key": "AKIA" + "ABCDEFGH12345678",
        "private_key_block": "-----BEGIN RSA PRIVATE KEY-----",
        "oauth_token_json": '"refreshToken": "abcdefghijklmnop1234"',
        "jwt": "eyJhbGciOiJITUZ.eyJzdWIiOiIxMjM0.dozjgNryP4J3jVmNH",
    }
    for name, sample in samples.items():
        f = repo_root / "logs" / f"{name}.txt"
        f.write_text(f"leading text {sample} trailing\n")
        code, res, _ = run_cli("secret_scan.py", str(f), root=repo_root)
        assert code == 3 and any(x["pattern"] == name for x in res["findings"]), \
            (name, res)
        f.unlink()


def test_secret_scan_scans_sqlite_field(repo):
    """Planting a token in a DB text field is caught (Phase C scans docs.sqlite)."""
    from .conftest import run_cli
    conn = connect(repo.db_path)
    conn.execute("INSERT INTO documents (slug, title, publisher, doc_type, "
                 "canonical_url, first_seen) VALUES "
                 "('x-y-z','T','p','model_card','https://x.test/z','ts')")
    conn.execute("UPDATE documents SET notes = ? WHERE slug='x-y-z'",
                 ("secret ghp_" + "a1B2c3D4" * 5 + " here",))
    conn.commit()
    conn.close()
    code, res, _ = run_cli("secret_scan.py", str(repo.db_path), root=repo.root)
    assert code == 3 and res["status"] == "findings", res


def test_secret_scan_skips_quarantine_files(repo_root):
    from .conftest import run_cli
    (repo_root / "logs").mkdir(exist_ok=True)
    token = "ghp_" + "a1B2c3D4" * 5
    (repo_root / "logs" / "issues_outbox.held.jsonl").write_text(token + "\n")
    (repo_root / "logs" / "SECURITY_HOLD.md").write_text(token + "\n")
    code, res, _ = run_cli("secret_scan.py", str(repo_root / "logs"), root=repo_root)
    assert code == 0, res  # quarantine artifacts must not re-trip forever


def test_annotate_version_stale_old_guard(repo, http_server):
    _first, second = _two_versions(repo, http_server)
    base = {"action": "annotate_version", "slug": second.slug,
            "version_id": second.version_id, "justification": "j", "evidence_urls": []}
    process_proposal(repo, {**base, "summary": "First summary."}, "r1")
    stale = process_proposal(repo, {**base, "old": "wrong prior value",
                                    "summary": "Second."}, "r2")
    assert stale.status == "rejected" and "stale_old_value" in stale.reason
    ok = process_proposal(repo, {**base, "old": "First summary.",
                                 "summary": "Second."}, "r3")
    assert ok.status == "written"


def test_annotate_version_uppercase_url_rejected(repo, http_server):
    _first, second = _two_versions(repo, http_server)
    res = process_proposal(repo, {
        "action": "annotate_version", "slug": second.slug,
        "version_id": second.version_id, "summary": "See HTTPS://EVIL.TEST for more.",
        "justification": "j", "evidence_urls": []}, "r")
    assert res.status == "rejected" and "plain text" in res.reason


def test_freetext_length_caps(repo, http_server):
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    long_title = process_proposal(
        repo, make_proposal(http_server, path="/doc2", title="x" * 501), "run1")
    assert long_title.status == "rejected" and "title exceeds" in long_title.reason
    long_notes = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "notes",
        "new": "y" * 8001, "justification": "j", "evidence_urls": []}, "run2")
    assert long_notes.status == "rejected" and "exceeds" in long_notes.reason
    long_related_note = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "related_urls",
        "new": [{"url": http_server.url("/other"), "kind": "paper", "note": "z" * 501}],
        "justification": "j", "evidence_urls": []}, "run3")
    assert long_related_note.status == "rejected"


def test_review_override_admits_same_publisher_duplicate_operator_only(repo, http_server):
    """Same-publisher identical content is skipped as a mirror by default; an
    operator can override to admit it, the agent cannot (override ignored for agent)."""
    http_server.set_html("/orig", "Identical body text under one publisher.")
    http_server.set_html("/mirror", "Identical body text under one publisher.")
    first = process_proposal(repo, make_proposal(http_server, path="/orig"), "r1")
    assert first.status == "written"

    # same publisher + identical content at a new URL → skipped (mirror), no issue
    dup = process_proposal(
        repo, make_proposal(http_server, path="/mirror", title="Other",
                            model_names=["OtherModel"]), "r2")
    assert dup.status == "duplicate" and "content_duplicate" in dup.reason

    # the agent's override is ignored (still skipped)
    agent_try = process_proposal(
        repo, make_proposal(http_server, path="/mirror", title="Other",
                            model_names=["OtherModel"]),
        "r3", actor="agent", override_review=True)
    assert agent_try.status == "duplicate"

    # the operator's override admits it
    ok = process_proposal(
        repo, make_proposal(http_server, path="/mirror", title="Other",
                            model_names=["OtherModel"]),
        "r4", actor="human", override_review=True)
    assert ok.status == "written"
    conn = connect(repo.db_path)
    detail = conn.execute("SELECT detail FROM changelog WHERE document_id=? AND "
                          "action='add'", (ok.document_id,)).fetchone()[0]
    conn.close()
    assert json.loads(detail).get("review_override") is True


def test_related_urls_nonstring_url_rejects_cleanly(repo, http_server):
    """A non-string url must produce a clean reject, not an uncaught AttributeError."""
    http_server.set_html("/doc1", "content")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    res = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "related_urls",
        "new": [{"url": 12345, "kind": "paper"}],
        "justification": "j", "evidence_urls": []}, "run2")
    assert res.status == "rejected" and "must be a string" in res.reason


def test_as_of_prose_is_not_erased_from_fingerprint():
    """Regression: an anchored 'As of <date>' pattern once erased real prose. A
    bug-bounty-stats sentence change must still change the fingerprint."""
    patterns = ("^- [\\d,.]+\\s*$",)  # the current bullet-only counter pattern
    a = "Safety section.\nAs of June 5, 2026, the bug bounty received 100,000 attempts."
    b = "Safety section.\nAs of August 20, 2026, the bug bounty received 400,000 attempts."
    assert fingerprint_text(a, patterns) != fingerprint_text(b, patterns)


def test_standalone_numeric_table_cell_still_counts():
    """The bare-counter pattern is bullet-anchored, so a lone numeric table cell
    (no '- ' prefix) is real content, not furniture."""
    patterns = ("^- [\\d,.]+\\s*$",)
    a = "Metric\n44.2\nrest"
    b = "Metric\n42.2\nrest"
    assert fingerprint_text(a, patterns) != fingerprint_text(b, patterns)
