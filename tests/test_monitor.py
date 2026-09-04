"""Monitor tests: 3-strike dead rule, blocked ≠ dead, moved detection,
fingerprint rotation, index-page diffing."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

from cardtrack import monitor as monitor_mod
from cardtrack.db import connect
from cardtrack.monitor import run_monitor
from cardtrack.propose import process_proposal
from cardtrack.repo import utcnow

from .conftest import Route, make_proposal


def seed(repo, server, path="/doc1", **overrides):
    server.set_html(path, overrides.pop("body", "Seeded content."))
    result = process_proposal(repo, make_proposal(server, path=path, **overrides), "seed")
    assert result.status == "written"
    return result


def get_status(repo, slug):
    conn = connect(repo.db_path)
    try:
        return conn.execute("SELECT status FROM documents WHERE slug=?", (slug,)).fetchone()[0]
    finally:
        conn.close()


def test_dead_after_three_strikes_404(repo, http_server):
    added = seed(repo, http_server, "/mortal-doc", model_names=["MortalModel"])
    del http_server.routes["/mortal-doc"]  # now 404s

    for i, run in enumerate(["r1", "r2", "r3"]):
        run_monitor(repo, run)
        expected = "active" if i < 2 else "dead"
        assert get_status(repo, added.slug) == expected, f"after run {run}"


def test_rerun_same_run_id_does_not_double_strike(repo, http_server):
    added = seed(repo, http_server, "/mortal-doc2", model_names=["MortalModel Two"])
    del http_server.routes["/mortal-doc2"]
    run_monitor(repo, "r1")
    run_monitor(repo, "r1")  # crash-recovery re-run
    run_monitor(repo, "r2")
    assert get_status(repo, added.slug) == "active", "2 distinct runs ≠ 3 strikes"


def test_blocked_403_never_strikes_toward_dead(repo, http_server):
    added = seed(repo, http_server, "/guarded-doc", model_names=["GuardedModel"])
    http_server.routes["/guarded-doc"] = Route(status=403, body=b"begone bot")

    for run in ["r1", "r2", "r3", "r4"]:
        run_monitor(repo, run)
    assert get_status(repo, added.slug) == "active"

    candidates = json.loads((repo.logs_dir / "candidates.json").read_text())
    assert any(e["slug"] == added.slug for e in candidates["blocked_escalations"]), \
        "persistently blocked URL escalates to the agent"


def test_permanent_redirect_marks_moved(repo, http_server):
    added = seed(repo, http_server, "/nomad-doc", model_names=["NomadModel"])
    http_server.set_html("/nomad-new-home", "Seeded content.")
    http_server.set_redirect("/nomad-doc", http_server.url("/nomad-new-home"), permanent=True)
    run_monitor(repo, "r1")
    assert get_status(repo, added.slug) == "moved"


def test_fingerprint_rotation_detects_silent_update(repo, http_server):
    added = seed(repo, http_server, "/quiet-doc", model_names=["QuietModel"])
    http_server.set_html("/quiet-doc", "Silently updated content, no announcement.")

    summary = run_monitor(repo, "r1")  # fraction=1.0 in test config → checks everything
    assert summary["new_versions"] == 1

    conn = connect(repo.db_path)
    n = conn.execute("SELECT COUNT(*) FROM document_versions WHERE document_id=?",
                     (added.document_id,)).fetchone()[0]
    conn.close()
    assert n == 2


def test_unchanged_content_adds_no_version(repo, http_server):
    added = seed(repo, http_server, "/stable-doc", model_names=["StableModel"])
    summary = run_monitor(repo, "r1")
    assert summary["new_versions"] == 0
    conn = connect(repo.db_path)
    n = conn.execute("SELECT COUNT(*) FROM document_versions WHERE document_id=?",
                     (added.document_id,)).fetchone()[0]
    conn.close()
    assert n == 1


def test_index_diff_finds_new_links_once(repo, http_server):
    http_server.set_html("/known-doc", "Already catalogued.")
    seed(repo, http_server, "/known-doc", model_names=["KnownModel"])
    http_server.routes["/index-page"] = Route(body=f"""<html><body>
      <a href="/known-doc">Known doc</a>
      <a href="/brand-new-card">Brand new system card</a>
      <a href="/style.css">stylesheet</a>
      <a href="mailto:x@y.z">mail</a>
      <a href="{http_server.url('/index-page')}">self</a>
    </body></html>""".encode())

    summary = run_monitor(repo, "r1")
    candidates = json.loads((repo.logs_dir / "candidates.json").read_text())
    urls = [c["url"] for c in candidates["candidates"]]
    assert summary["candidates"] == 1
    assert urls == [http_server.url("/brand-new-card")]
    assert candidates["candidates"][0]["link_text"] == "Brand new system card"

    # second run: same page → nothing newly discovered, but the unprocessed
    # candidate stays in the backlog until it becomes a document or expires
    summary2 = run_monitor(repo, "r2")
    candidates2 = json.loads((repo.logs_dir / "candidates.json").read_text())
    assert summary2["candidates_new"] == 0
    assert [c["url"] for c in candidates2["candidates"]] == \
        [http_server.url("/brand-new-card")], "backlog persists unprocessed candidates"

    # once catalogued, it leaves the backlog
    http_server.set_html("/brand-new-card", "Now catalogued.")
    result = process_proposal(
        repo, make_proposal(http_server, path="/brand-new-card",
                            model_names=["BrandNewModel"]), "r2b")
    assert result.status == "written"
    run_monitor(repo, "r3")
    candidates3 = json.loads((repo.logs_dir / "candidates.json").read_text())
    assert candidates3["candidates"] == []


def test_candidate_expiry_requires_agent_run(repo, http_server):
    """Leads must not expire during an agent outage: past-TTL candidates stay in
    the backlog until a successful Phase B run postdates them (hard cap aside)."""
    def stale(days_old):
        ts = (datetime.now(UTC) - timedelta(days=days_old)
              ).strftime("%Y-%m-%dT%H:%M:%SZ")
        repo.logs_dir.mkdir(parents=True, exist_ok=True)
        (repo.logs_dir / "candidates.json").write_text(json.dumps({
            "candidates": [{"url": "https://x.test/stale-lead", "publisher": "p",
                            "index_url": "https://x.test/", "link_text": "",
                            "first_seen": ts}]}))
        return ts

    # past TTL, agent never ran → survives
    stale(monitor_mod.CANDIDATE_TTL_DAYS + 1)
    run_monitor(repo, "r1")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert [c["url"] for c in backlog] == ["https://x.test/stale-lead"], \
        "agent outage must not expire untriaged leads"

    # agent succeeded BEFORE the lead appeared → still survives
    first_seen = stale(monitor_mod.CANDIDATE_TTL_DAYS + 1)
    earlier = (datetime.now(UTC) - timedelta(
        days=monitor_mod.CANDIDATE_TTL_DAYS + 2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (repo.logs_dir / ".agent_last_success").write_text(earlier)
    run_monitor(repo, "r2")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert [c["url"] for c in backlog] == ["https://x.test/stale-lead"]

    # agent succeeded after the lead appeared → normal TTL expiry applies
    assert first_seen < utcnow()
    (repo.logs_dir / ".agent_last_success").write_text(utcnow())
    run_monitor(repo, "r3")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert backlog == []

    # hard cap: with no agent success at all, an 8x-TTL-old lead is dropped
    (repo.logs_dir / ".agent_last_success").unlink()
    stale(8 * monitor_mod.CANDIDATE_TTL_DAYS + 1)
    run_monitor(repo, "r4")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert backlog == []


def test_dead_doc_self_heals_when_url_returns(repo, http_server):
    added = seed(repo, http_server, "/lazarus-doc", model_names=["LazarusModel"])
    body = http_server.routes.pop("/lazarus-doc")
    for run in ["r1", "r2", "r3"]:
        run_monitor(repo, run)
    assert get_status(repo, added.slug) == "dead"
    # a dead doc never strikes further, and revives when the URL answers again
    http_server.routes["/lazarus-doc"] = body
    run_monitor(repo, "r4")
    assert get_status(repo, added.slug) == "active"


def test_nonconsecutive_404s_do_not_kill(repo, http_server):
    added = seed(repo, http_server, "/flaky-doc", model_names=["FlakyModel"])
    body = http_server.routes["/flaky-doc"]
    del http_server.routes["/flaky-doc"]          # 404
    run_monitor(repo, "r1")
    run_monitor(repo, "r2")
    http_server.routes["/flaky-doc"] = body       # recovers
    run_monitor(repo, "r3")
    del http_server.routes["/flaky-doc"]          # 404 again
    run_monitor(repo, "r4")
    run_monitor(repo, "r5")
    assert get_status(repo, added.slug) == "active", \
        "2+2 nonconsecutive strikes must not equal 3 consecutive"
    run_monitor(repo, "r6")
    assert get_status(repo, added.slug) == "dead"


def test_temporary_redirect_is_not_moved(repo, http_server):
    added = seed(repo, http_server, "/wanderer-doc", model_names=["WandererModel"])
    http_server.set_html("/temp-target", "Seeded content.")
    http_server.set_redirect("/wanderer-doc", http_server.url("/temp-target"),
                             permanent=False)
    run_monitor(repo, "r1")
    assert get_status(repo, added.slug) == "active", "302 is not a move"


def test_fingerprint_rotation_cadence(repo_root, http_server):
    from cardtrack.repo import Repo

    from .conftest import write_test_config

    write_test_config(repo_root, http_server, fingerprint_fraction=0.4)
    repo = Repo(root=repo_root)
    for i in range(3):
        seed(repo, http_server, f"/rot{i}", body=f"Rotation doc {i} body.",
             model_names=[f"RotModel {i}"])
    summary = run_monitor(repo, "r1")
    assert summary["fingerprint_checked"] == 2, "ceil(0.4 * 3) = 2, oldest first"
