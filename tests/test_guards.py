"""Regression tests for the review-driven hardening: rolling-window caps, byte
budget, env-based run ids, SSRF guard, canonical_url repoint gate, redirect
semantics, and body-escaping via the text-passthrough path."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta

from cardtrack.db import connect
from cardtrack.fetch import host_is_public
from cardtrack.propose import process_proposal
from cardtrack.repo import Repo
from cardtrack.sitebuild import build_site

from .conftest import Route, make_proposal, write_test_config


def _age_changelog(repo, hours: int) -> None:
    """Backdate every changelog row (and link_check) by N hours."""
    old = (datetime.now(UTC) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = connect(repo.db_path)
    conn.execute("UPDATE changelog SET ts = ?", (old,))
    conn.execute("UPDATE link_checks SET ts = ?", (old,))
    conn.commit()
    conn.close()


def test_caps_are_rolling_window_not_run_id(repo_root, http_server):
    """Fresh run ids must NOT reset caps; expiry of the rolling window must."""
    write_test_config(repo_root, http_server, caps={"max_new_documents_per_run": 2})
    repo = Repo(root=repo_root)
    for i in range(2):
        http_server.set_html(f"/w{i}", f"Window doc {i}.")
        r = process_proposal(repo, make_proposal(http_server, path=f"/w{i}",
                                                 model_names=[f"WModel {i}"]),
                             run_id=f"run-{i}")
        assert r.status == "written"
    http_server.set_html("/w2", "Window doc 2.")
    r = process_proposal(repo, make_proposal(http_server, path="/w2",
                                             model_names=["WModel 2"]),
                         run_id="totally-fresh-run-id")
    assert r.status == "rejected" and "cap_exceeded" in r.reason, \
        "a fresh run_id must not reset the cap"

    _age_changelog(repo, hours=25)
    r = process_proposal(repo, make_proposal(http_server, path="/w2",
                                             model_names=["WModel 2"]), run_id="later")
    assert r.status == "written", "cap frees up once the 24h window passes"


def test_version_cap_rolling(repo_root, http_server):
    write_test_config(repo_root, http_server, caps={"max_new_versions_per_run": 1})
    repo = Repo(root=repo_root)
    for i, path in enumerate(["/va", "/vb"]):
        http_server.set_html(path, f"Version-cap doc {i}.")
        assert process_proposal(repo, make_proposal(http_server, path=path,
                                                    model_names=[f"VModel {i}"]),
                                "seed").status == "written"
    http_server.set_html("/va", "Doc A changed content.")
    http_server.set_html("/vb", "Doc B changed content.")
    r1 = process_proposal(repo, {"action": "new_version", "url": http_server.url("/va"),
                                 "justification": "j", "evidence_urls": []}, "r-x")
    r2 = process_proposal(repo, {"action": "new_version", "url": http_server.url("/vb"),
                                 "justification": "j", "evidence_urls": []}, "r-y")
    assert r1.status == "written"
    assert r2.status == "rejected" and "max_new_versions_per_run" in r2.reason


def test_fetch_budget_counts_all_outcomes(repo_root, http_server):
    """Duplicate no-op fetches must count toward the budget too."""
    http_server.set_html("/b1", "Budget doc one.")
    doc_size = len(http_server.routes["/b1"].body)
    # one fetch fits, two cross the line — so the third proposal must be refused
    write_test_config(repo_root, http_server,
                      caps={"max_total_fetch_bytes_per_run": doc_size + 20})
    repo = Repo(root=repo_root)
    assert process_proposal(repo, make_proposal(http_server, path="/b1",
                                                model_names=["BModel 1"]),
                            "r1").status == "written"
    # duplicate no-op: fetches the doc again, logs bytes into link_checks
    assert process_proposal(repo, make_proposal(http_server, path="/b1",
                                                model_names=["BModel 1"]),
                            "r2").status == "duplicate"
    conn = connect(repo.db_path)
    logged = conn.execute("SELECT COALESCE(SUM(byte_size),0) FROM link_checks").fetchone()[0]
    conn.close()
    assert logged > 0, "no-op fetch bytes are accounted"
    # budget now exhausted → next fetch refused before it happens
    http_server.set_html("/b2", "Budget doc two.")
    r = process_proposal(repo, make_proposal(http_server, path="/b2",
                                             model_names=["BModel 2"]), "r3")
    assert r.status == "rejected" and "fetch_budget_exceeded" in r.reason


def test_cli_reads_run_id_and_actor_from_env(repo_root, http_server):
    http_server.set_html("/envdoc", "Env-driven run id doc.")
    import subprocess
    import sys

    from .conftest import PROJECT_ROOT
    env = dict(os.environ, CARDTRACK_RUN_ID="daily-2026-08-09", CARDTRACK_ACTOR="agent")
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "propose_doc.py"),
         "--root", str(repo_root), "--json", "-"],
        input=json.dumps(make_proposal(http_server, path="/envdoc",
                                       model_names=["EnvModel"])),
        capture_output=True, text=True, timeout=120, env=env)
    result = json.loads(proc.stdout.strip().splitlines()[-1])
    assert result["status"] == "written"
    assert result["run_id"] == "daily-2026-08-09"
    conn = connect(Repo(root=repo_root).db_path)
    detail = json.loads(conn.execute(
        "SELECT detail FROM changelog WHERE action='add'").fetchone()[0])
    conn.close()
    assert detail["actor"] == "agent"


def test_ssrf_guard_blocks_private_hosts(repo_root, http_server, tmp_path):
    assert not host_is_public("localhost")
    assert not host_is_public("127.0.0.1")
    assert not host_is_public("10.1.2.3")
    assert not host_is_public("169.254.1.1")

    # config with the guard ON: proposals to the loopback test server are refused
    write_test_config(repo_root, http_server)
    import yaml
    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())
    settings["fetch"]["allow_private_hosts"] = False
    settings_path.write_text(yaml.safe_dump(settings))
    r = process_proposal(Repo(root=repo_root),
                         make_proposal(http_server, path="/whatever"), "r1")
    assert r.status == "rejected"
    assert "host not public" in r.reason


def test_canonical_url_repoint_to_unknown_host_files_issue(repo_root, http_server):
    repo = Repo(root=repo_root)
    http_server.set_html("/home-doc", "Repoint guard content.")
    added = process_proposal(repo, make_proposal(http_server, path="/home-doc",
                                                 model_names=["RepointModel"]), "r1")
    assert added.status == "written"
    # same server, but addressed via a hostname the publisher has never used
    port = http_server.httpd.server_address[1]
    evil = f"http://localhost:{port}/home-doc"
    r = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "canonical_url",
        "new": evil, "justification": "totally legit move", "evidence_urls": []},
        "r2", actor="human")  # canonical_url is operator-only
    assert r.status == "issue_filed"
    assert "canonical_url_host_unknown" in r.reason
    conn = connect(repo.db_path)
    url = conn.execute("SELECT canonical_url FROM documents WHERE slug=?",
                       (added.slug,)).fetchone()[0]
    conn.close()
    assert "localhost" not in url, "repoint must not be written"


def test_canonical_url_repoint_with_different_content_files_issue(repo_root, http_server):
    repo = Repo(root=repo_root)
    http_server.set_html("/orig-doc", "Original body text.")
    http_server.set_html("/other-doc", "Completely different body text.")
    added = process_proposal(repo, make_proposal(http_server, path="/orig-doc",
                                                 model_names=["ContentModel"]), "r1")
    r = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "canonical_url",
        "new": http_server.url("/other-doc"),
        "justification": "move", "evidence_urls": []}, "r2", actor="human")
    assert r.status == "issue_filed"
    assert "canonical_url_content_mismatch" in r.reason


def test_url_conflict_on_repoint_rejected(repo_root, http_server):
    repo = Repo(root=repo_root)
    http_server.set_html("/own-a", "Doc A body.")
    http_server.set_html("/own-b", "Doc B body.")
    a = process_proposal(repo, make_proposal(http_server, path="/own-a",
                                             model_names=["ConflictA"]), "r1")
    b = process_proposal(repo, make_proposal(http_server, path="/own-b",
                                             model_names=["ConflictB"]), "r1")
    r = process_proposal(repo, {
        "action": "field_update", "slug": b.slug, "field": "canonical_url",
        "new": http_server.url("/own-a"), "justification": "j", "evidence_urls": []},
        "r2", actor="human")
    assert r.status == "rejected" and "url_conflict" in r.reason
    assert a.slug in r.reason


def test_alt_url_still_routes_to_document(repo_root, http_server):
    """After a canonical move, adds via the OLD url must dedup through alt_urls."""
    repo = Repo(root=repo_root)
    http_server.set_html("/old-home", "Alt routing body.")
    http_server.set_html("/new-home", "Alt routing body.")
    added = process_proposal(repo, make_proposal(http_server, path="/old-home",
                                                 model_names=["AltModel"]), "r1")
    moved = process_proposal(repo, {
        "action": "field_update", "slug": added.slug, "field": "canonical_url",
        "new": http_server.url("/new-home"), "justification": "move",
        "evidence_urls": []}, "r2", actor="human")
    assert moved.status == "written"
    again = process_proposal(repo, make_proposal(http_server, path="/old-home",
                                                 model_names=["AltModel"]), "r3")
    assert again.status == "duplicate"
    assert again.document_id == added.document_id
    conn = connect(repo.db_path)
    assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 1
    conn.close()


def test_temporary_redirect_keeps_original_canonical(repo_root, http_server):
    """302 chains must not move the canonical identity (vanity URL → rotating CDN)."""
    repo = Repo(root=repo_root)
    http_server.set_html("/cdn-target", "Vanity doc content.")
    http_server.set_redirect("/vanity", http_server.url("/cdn-target"), permanent=False)
    added = process_proposal(repo, make_proposal(http_server, path="/vanity",
                                                 model_names=["VanityModel"]), "r1")
    assert added.status == "written"
    conn = connect(repo.db_path)
    url = conn.execute("SELECT canonical_url FROM documents WHERE slug=?",
                       (added.slug,)).fetchone()[0]
    conn.close()
    assert url.endswith("/vanity"), f"302 must not move canonical, got {url}"


def test_extracted_body_escaping_via_text_passthrough(repo_root, http_server):
    """HTML-ish payloads that survive extraction (text/plain passthrough) must be
    escaped in the published page (a `| safe` regression would ship raw script)."""
    repo = Repo(root=repo_root)
    payload = 'Report text with <script>alert("xss")</script> & <b>markup</b>.'
    http_server.routes["/plain-doc"] = Route(
        body=payload.encode(), content_type="text/plain; charset=utf-8")
    added = process_proposal(repo, make_proposal(http_server, path="/plain-doc",
                                                 model_names=["PlainModel"]), "r1")
    assert added.status == "written"
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{added.slug}.html").read_text()
    assert '<script>alert("xss")</script>' not in page
    assert "&lt;script&gt;" in page


def test_identical_bytes_never_a_new_version(repo, http_server):
    """Even if the stored fingerprint is wrong (extraction drift across
    environments), identical raw bytes must short-circuit to duplicate."""
    http_server.routes["/static-doc"] = Route(
        body=b"<html><body><p>Byte-stable document body.</p></body></html>")
    added = process_proposal(repo, make_proposal(http_server, path="/static-doc",
                                                 model_names=["ByteModel"]), "r1")
    assert added.status == "written"
    conn = connect(repo.db_path)
    conn.execute("UPDATE document_versions SET content_fingerprint = 'corrupted-fp' "
                 "WHERE id = ?", (added.version_id,))
    conn.commit()
    conn.close()
    again = process_proposal(repo, {"action": "new_version",
                                    "url": http_server.url("/static-doc"),
                                    "justification": "j", "evidence_urls": []}, "r2")
    assert again.status == "duplicate", (again.status, again.reason)


def test_impersonation_fallback_defeats_bot_wall(repo, http_server):
    """A publisher that 400s the plain client must still be ingestable via the
    browser-impersonation fallback (no browser-accessibility bias)."""
    http_server.routes["/walled-doc"] = Route(
        body=b"<html><body><p>Bot-walled report body.</p></body></html>",
        block_plain_client=True)
    r = process_proposal(repo, make_proposal(http_server, path="/walled-doc",
                                             model_names=["WalledModel"]), "r1")
    assert r.status == "written", (r.status, r.reason)
    conn = connect(repo.db_path)
    extraction = json.loads(conn.execute(
        "SELECT extraction FROM document_versions WHERE id=?",
        (r.version_id,)).fetchone()[0])
    conn.close()
    assert extraction["transport"] == "browser_impersonation"


def test_impersonation_off_still_blocked(repo_root, http_server):
    import yaml
    write_test_config(repo_root, http_server)
    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())
    settings["fetch"]["impersonate_fallback"] = False
    settings_path.write_text(yaml.safe_dump(settings))
    http_server.routes["/walled-doc2"] = Route(
        body=b"<html><body><p>walled</p></body></html>", block_plain_client=True)
    r = process_proposal(Repo(root=repo_root),
                         make_proposal(http_server, path="/walled-doc2",
                                       model_names=["Walled2"]), "r1")
    assert r.status == "rejected" and "HTTP 400" in r.reason


def test_manual_content_ingestion(repo, http_server, tmp_path):
    """Operator-supplied bytes for a URL the pipeline cannot fetch at all."""
    payload = b"<html><body><p>Manually retrieved safety report.</p></body></html>"
    f = tmp_path / "manual.html"
    f.write_bytes(payload)
    r = process_proposal(
        repo,
        make_proposal(http_server, path="/unfetchable-404",
                      model_names=["ManualModel"]),
        "r1", actor="human",
        local_content=payload, local_content_type="text/html")
    assert r.status == "written", (r.status, r.reason)
    conn = connect(repo.db_path)
    extraction = json.loads(conn.execute(
        "SELECT extraction FROM document_versions WHERE id=?",
        (r.version_id,)).fetchone()[0])
    conn.close()
    assert extraction["transport"] == "manual_upload"


def test_content_file_refused_in_sandbox(repo_root, http_server, tmp_path):
    import subprocess
    import sys

    from .conftest import PROJECT_ROOT
    f = tmp_path / "payload.html"
    f.write_bytes(b"<html><body>x</body></html>")
    env = dict(os.environ, CARDTRACK_SANDBOX="1")
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "propose_doc.py"),
         "--root", str(repo_root), "--json", "-", "--content-file", str(f)],
        input=json.dumps(make_proposal(http_server, path="/x")),
        capture_output=True, text=True, timeout=60, env=env)
    assert proc.returncode == 2
    assert "human-only" in proc.stdout


def test_safety_evals_flag_stored_and_updatable(repo, http_server):
    http_server.set_html("/flagged-doc", "Red-teaming and dangerous capability evals.")
    r = process_proposal(repo, make_proposal(
        http_server, path="/flagged-doc", model_names=["FlagModel"],
        soft={"has_safety_evals": True}), "r1")
    assert r.status == "written"
    conn = connect(repo.db_path)
    assert conn.execute("SELECT safety_evals FROM documents WHERE slug=?",
                        (r.slug,)).fetchone()[0] == 1
    conn.close()

    upd = process_proposal(repo, {
        "action": "field_update", "slug": r.slug, "field": "safety_evals",
        "new": False, "justification": "reassessed: only a limitations paragraph",
        "evidence_urls": []}, "r2")
    assert upd.status == "written"
    conn = connect(repo.db_path)
    assert conn.execute("SELECT safety_evals FROM documents WHERE slug=?",
                        (r.slug,)).fetchone()[0] == 0
    conn.close()


def test_safety_evals_required_on_add(repo, http_server):
    """A NULL safety_evals doc would be invisible to the site's yes/no filters,
    so an add without the attestation is rejected, not admitted."""
    http_server.set_html("/unflagged-doc", "No soft dict provided.")
    p = make_proposal(http_server, path="/unflagged-doc", model_names=["UnflaggedModel"])
    del p["soft"]
    r = process_proposal(repo, p, "r1")
    assert r.status == "rejected"
    assert "has_safety_evals" in r.reason

    conn = connect(repo.db_path)
    assert conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 0
    conn.close()

