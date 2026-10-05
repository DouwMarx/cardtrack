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
    repo.state_dir.mkdir(exist_ok=True)
    (repo.state_dir / ".agent_last_success").write_text(earlier)
    run_monitor(repo, "r2")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert [c["url"] for c in backlog] == ["https://x.test/stale-lead"]

    # agent succeeded after the lead appeared → normal TTL expiry applies
    assert first_seen < utcnow()
    (repo.state_dir / ".agent_last_success").write_text(utcnow())
    run_monitor(repo, "r3")
    backlog = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert backlog == []

    # hard cap: with no agent success at all, an 8x-TTL-old lead is dropped
    (repo.state_dir / ".agent_last_success").unlink()
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


def test_meta_refresh_stub_marks_moved(repo, http_server):
    """A page replaced by a client-side redirect stub answers 200 to a link checker but
    is gone for a reader (Palisade, Sept 2026): treat it like a permanent redirect."""
    added = seed(repo, http_server, "/old-post", model_names=["StubModel"])
    http_server.set_html("/new-home", "Seeded content.")
    target = http_server.url("/new-home")
    http_server.routes["/old-post"] = Route(body=f"""<!DOCTYPE html><html><head>
    <title>Redirecting&hellip;</title>
    <link rel="canonical" href="{target}">
    <meta http-equiv="refresh" content="0; url={target}">
    </head><body><h1>Redirecting&hellip;</h1>
    <a href="{target}">Click here if you are not redirected.</a></body></html>""".encode())
    summary = run_monitor(repo, "r1")
    assert summary["moved"] == 1
    assert get_status(repo, added.slug) == "moved"


def test_collapsed_page_is_not_minted_as_a_version(repo, http_server):
    long_body = " ".join(["A substantive paragraph about the model and its evaluations."] * 40)
    added = seed(repo, http_server, "/big-doc", body=long_body, model_names=["BigModel"])
    http_server.set_html("/big-doc", "Listing: v1.0, 256k context, pricing.")
    summary = run_monitor(repo, "r1")
    assert summary["new_versions"] == 0
    assert summary["content_collapsed"] == [added.slug]
    conn = connect(repo.db_path)
    outcome = conn.execute(
        "SELECT outcome FROM link_checks WHERE document_id=? AND check_type='fingerprint' "
        "ORDER BY id DESC LIMIT 1", (added.document_id,)).fetchone()[0]
    n = conn.execute("SELECT COUNT(*) FROM document_versions WHERE document_id=?",
                     (added.document_id,)).fetchone()[0]
    conn.close()
    assert outcome == "content_collapsed"
    assert n == 1


def test_extractor_drift_is_labelled_not_reported_as_deletion(repo, http_server):
    """Text the extractor drops (here: moved into a <footer>) is still in the raw capture,
    so the new version carries an extractor-drift note instead of posing as a deletion."""
    para = "The tested model was an unreleased internal prototype and is not planned for release."
    body = " ".join(["Main text about the evaluation methodology and the results table."] * 20)
    added = seed(repo, http_server, "/drift-doc",
                 body=f"{body}</p><p>{para}", model_names=["DriftModel"])
    http_server.routes["/drift-doc"] = Route(body=f"""<!DOCTYPE html><html><head>
    <title>Doc</title></head><body><article><h1>Doc</h1><p>{body}</p></article>
    <footer><p>{para}</p><a href="/privacy">Privacy</a></footer></body></html>""".encode())
    summary = run_monitor(repo, "r1")
    assert summary["new_versions"] == 1
    assert summary["extractor_drift"] == 1
    conn = connect(repo.db_path)
    note = conn.execute(
        "SELECT change_summary FROM document_versions WHERE document_id=? "
        "ORDER BY id DESC LIMIT 1", (added.document_id,)).fetchone()[0]
    conn.close()
    assert note and note.startswith("Extractor drift")


def _text_route(*lines: str) -> Route:
    # text/plain keeps the extracted lines exactly as served (no boilerplate removal)
    return Route(body="\n".join(lines).encode(), content_type="text/plain")


def test_furniture_only_version_is_marked_and_kept_from_the_agent(repo, http_server):
    """17 of the last 19 Anthropic versions in 2026-09 differed only by a dropped date
    line and rotating "Read more" teasers, and they crowded real revisions out of the
    agent's 5-per-run summary budget. The monitor now labels them itself and orders the
    rest by substantive changed lines."""
    from cardtrack.monitor import FURNITURE_SUMMARY

    body = "The model was evaluated on autonomy tasks and scored 40% on the suite."
    http_server.routes["/furniture"] = _text_route("Jan 14, 2026", body,
                                                   "Teaser about drones.", "Read more")
    http_server.routes["/small"] = _text_route(body)
    http_server.routes["/big"] = _text_route(body, "Section A.", "Section B.")
    def add(path, name):  # seed() would overwrite the text route with HTML
        result = process_proposal(repo, make_proposal(http_server, path=path,
                                                      model_names=[name]), "seed")
        assert result.status == "written"
        return result

    furn = add("/furniture", "FurnitureModel")
    small = add("/small", "SmallModel")
    big = add("/big", "BigModel")
    http_server.routes["/furniture"] = _text_route(body, "Teaser about markets.", "Read more")
    http_server.routes["/small"] = _text_route(body.replace("40%", "45%"))
    http_server.routes["/big"] = _text_route(body, "Section A revised.", "Section B revised.",
                                             "Section C added.")

    summary = run_monitor(repo, "r1")
    assert summary["new_versions"] == 3
    queue = json.loads((repo.logs_dir / "updated_docs.json").read_text())["updated_docs"]
    assert [e["slug"] for e in queue] == [big.slug, small.slug], \
        "furniture left out; biggest real revision first"
    assert queue[0]["substantive_lines"] == 5 and queue[1]["substantive_lines"] == 2
    conn = connect(repo.db_path)
    note = conn.execute(
        "SELECT change_summary FROM document_versions WHERE document_id=? "
        "ORDER BY id DESC LIMIT 1", (furn.document_id,)).fetchone()[0]
    conn.close()
    assert note == FURNITURE_SUMMARY


def test_hf_api_index_is_parsed_as_json(repo_root, http_server):
    """huggingface.co/api/models?author=<org>&sort=createdAt lists repos by creation
    time, which the org's HTML page does not (Qwen3.8 surfaced 5 days late, a flagship
    Hunyuan release never). Each entry becomes a candidate at /<id>."""
    import yaml

    from cardtrack.repo import Repo

    api_path = "/api/models?author=testorg&sort=createdAt&direction=-1&limit=100"
    fresh = (datetime.now(UTC) - timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    old = (datetime.now(UTC) - timedelta(days=monitor_mod.CANDIDATE_TTL_DAYS + 1)
           ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    payload = json.dumps([
        {"id": "testorg/new-model", "createdAt": fresh, "likes": 3},
        {"id": "testorg/new-model", "createdAt": fresh},  # dup
        {"id": "testorg/old-checkpoint", "createdAt": old},  # listings reach back years
        {"_id": "entry without an id"},
    ]).encode()
    http_server.routes[api_path] = Route(body=payload, content_type="application/json")
    sources_path = repo_root / "config" / "sources.yaml"
    sources = yaml.safe_load(sources_path.read_text())
    sources["publishers"]["testlab"]["index_urls"] = [http_server.url(api_path)]
    sources_path.write_text(yaml.safe_dump(sources))
    repo = Repo(root=repo_root)

    summary = run_monitor(repo, "r1")
    candidates = json.loads((repo.logs_dir / "candidates.json").read_text())["candidates"]
    assert summary["candidates"] == 1
    assert candidates[0]["url"] == http_server.url("/testorg/new-model")
    assert candidates[0]["link_text"] == "testorg/new-model"
    assert candidates[0]["published_at"] == fresh
    assert candidates[0]["first_seen"] > fresh, \
        "first_seen stays the discovery time, so the TTL cannot expire a repo on sight"
    conn = connect(repo.db_path)
    baselined = [r[0] for r in conn.execute("SELECT url FROM index_links ORDER BY url")]
    conn.close()
    assert baselined == [http_server.url("/testorg/new-model"),
                         http_server.url("/testorg/old-checkpoint")], \
        "a repo older than the TTL is baselined, never queued (460 such on day one)"

    # a broken payload is skipped, not fatal, and the backlog survives
    http_server.routes[api_path] = Route(body=b"<html>rate limited</html>",
                                         content_type="application/json")
    summary2 = run_monitor(repo, "r2")
    assert summary2["candidates_new"] == 0 and summary2["candidates"] == 1


def test_phase_a_summary_lists_blocked_and_not_found_every_run(repo, http_server):
    """The agent's "investigate blocked URLs" step saw an empty list for three runs while
    10 openai.com rows sat blocked; every blocked or 404 URL now appears from run 1
    with its streak. The 3-run escalation and dead rules are unchanged."""
    walled = seed(repo, http_server, "/walled", body="Walled content.",
                  model_names=["WalledModel"])
    gone = seed(repo, http_server, "/vanished", body="Vanished content.",
                model_names=["VanishedModel"])
    http_server.routes["/walled"] = Route(status=403, body=b"begone bot")
    del http_server.routes["/vanished"]

    run_monitor(repo, "r1")
    out = json.loads((repo.logs_dir / "candidates.json").read_text())
    assert out["blocked_escalations"] == []
    seen = {k: [(e["slug"], e["http_status"], e["streak"]) for e in v]
            for k, v in out["phase_a_summary"].items()}
    assert seen == {"blocked": [(walled.slug, 403, 1)], "not_found": [(gone.slug, 404, 1)]}

    run_monitor(repo, "r2")
    run_monitor(repo, "r3")
    out = json.loads((repo.logs_dir / "candidates.json").read_text())
    assert out["phase_a_summary"]["blocked"][0]["streak"] == 3
    assert out["phase_a_summary"]["not_found"][0]["streak"] == 3
    assert [e["slug"] for e in out["blocked_escalations"]] == [walled.slug]
    assert get_status(repo, gone.slug) == "dead"
