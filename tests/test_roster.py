"""Roster sync (cardtrack/roster.py): OpenRouter rankings -> additive publisher
overlay. Real local HTTP server, real files; no mocks."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import yaml

from cardtrack.repo import Repo
from cardtrack.roster import (
    OVERLAY_NAME,
    SNAPSHOT_NAME,
    AuthorStat,
    aggregate,
    read_api_key,
    run_roster,
    select_authors,
)
from tests.conftest import ATTESTED, Route, TestServer, make_proposal

# ---------------------------------------------------------------- fixtures

# Per-day token counts. Shares (of the attributable total, stealth excluded):
# biglab 60.5 -> ~0.59, testlab 20 -> 0.195, midlab 15 -> 0.146, small 5 -> 0.049,
# tail 2 -> 0.019 -> cumulative 0.99 crosses inside `tail`, so `tiny` (0.5) is out.
DAILY = {
    "biglab": 60_500, "testlab": 20_000, "midlab": 15_000, "small": 5_000,
    "tail": 2_000, "tiny": 500, "stealth": 30_000, "~biglab": 9_000,
}


def make_payload(days: int = 30, daily: dict | None = None, *, version: str = "v1",
                 flaky_slug: str | None = None, flaky_days: int = 3) -> dict:
    daily = daily or DAILY
    end = date(2026, 9, 21)
    rows = []
    for i in range(days):
        d = (end - timedelta(days=i)).isoformat()
        for slug, tokens in daily.items():
            if slug == flaky_slug and i >= flaky_days:
                continue
            rows.append({"date": d, "model_permaslug": f"{slug}/model-{slug}",
                         "total_tokens": str(tokens)})
        rows.append({"date": d, "model_permaslug": "other", "total_tokens": "999999"})
    start = (end - timedelta(days=days - 1)).isoformat()
    return {"data": rows, "meta": {"as_of": "2026-09-22T00:00:00Z", "version": version,
                                   "start_date": start, "end_date": end.isoformat()}}


MODELS = {"data": [
    {"id": "biglab/model-a", "name": "Big Lab: Model A", "hugging_face_id": "BigLabHF/model-a"},
    {"id": "biglab/model-b", "name": "Big Lab: Model B", "hugging_face_id": "BigLabHF/model-b"},
    {"id": "midlab/m", "name": "MidLab: M", "hugging_face_id": None},
    {"id": "small/s", "name": "small/s-no-colon", "hugging_face_id": "smallhf/s"},
]}


def serve(server: TestServer, payload: dict, models: dict | None = MODELS) -> None:
    server.routes["/rankings"] = Route(body=json.dumps(payload).encode(),
                                       content_type="application/json")
    if models is not None:
        server.routes["/models"] = Route(body=json.dumps(models).encode(),
                                         content_type="application/json")


def write_policy(root: Path, server: TestServer, **overrides) -> None:
    policy = {
        "enabled": True,
        "endpoint": server.url("/rankings"),
        "models_endpoint": server.url("/models"),
        "cumulative_share": 0.99,
        "min_days_present": 7,
        "guards": {"min_days_in_window": 20, "min_authors": 3, "max_authors": 100,
                   "failstreak_issue_after": 3},
        "aliases": {},
        "ignore": ["stealth"],
        "deny": [],
    }
    policy.update(overrides)
    (root / "config" / "roster.yaml").write_text(yaml.safe_dump(policy))


def overlay_of(root: Path) -> dict:
    return yaml.safe_load((root / "config" / OVERLAY_NAME).read_text())


# ---------------------------------------------------------------- pure logic

def test_aggregate_drops_other_internal_aliases_and_ignored():
    stats, other_share = aggregate(make_payload()["data"], {"ignore": ["stealth"]})
    slugs = [a.slug for a in stats]
    assert slugs == ["biglab", "testlab", "midlab", "small", "tail", "tiny"]
    assert all(a.days_present == 30 for a in stats)
    assert abs(sum(a.share for a in stats) - 1.0) < 1e-9
    # 'other' is 999999/day against 103000 attributable/day (stealth and ~biglab excluded)
    assert abs(other_share - 999_999 / (999_999 + 103_000)) < 1e-9


def test_cumulative_cut_admits_the_author_that_crosses_the_line():
    stats = [AuthorStat("a", 70, 30, 0.70), AuthorStat("b", 25, 30, 0.25),
             AuthorStat("c", 4, 30, 0.04), AuthorStat("d", 1, 30, 0.01)]
    chosen = [a.slug for a in select_authors(stats, {"cumulative_share": 0.99})]
    assert chosen == ["a", "b", "c"]  # 0.95 < 0.99 admits c; 0.99 >= 0.99 stops before d
    chosen = [a.slug for a in select_authors(stats, {"cumulative_share": 0.90})]
    assert chosen == ["a", "b"]


def test_min_days_present_filters_spikes_without_shifting_the_cut():
    stats = [AuthorStat("a", 70, 30, 0.70), AuthorStat("spike", 25, 2, 0.25),
             AuthorStat("c", 5, 30, 0.05)]
    chosen = [a.slug for a in select_authors(stats, {"cumulative_share": 0.99,
                                                     "min_days_present": 7})]
    assert chosen == ["a", "c"]


def test_read_api_key_from_dotenv(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    repo = Repo(root=tmp_path)
    assert read_api_key(repo) is None
    (tmp_path / ".env").write_text('# c\nOTHER=1\nexport OPENROUTER_API_KEY="sk-or-abc"\n')
    assert read_api_key(repo) == "sk-or-abc"
    monkeypatch.setenv("OPENROUTER_API_KEY", "fromenv")
    assert read_api_key(repo) == "fromenv"


# ---------------------------------------------------------------- end to end

def test_sync_writes_additive_overlay_and_snapshot(repo_root: Path, http_server: TestServer):
    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    repo = Repo(root=repo_root)
    out = run_roster(repo, "r1", api_key="k")
    assert out["status"] == "ok", out
    ov = overlay_of(repo_root)
    # testlab is curated -> never in the overlay; tiny is below the 99% cut
    assert set(ov["publishers"]) == {"biglab", "midlab", "small", "tail"}
    assert out["new"] == ["biglab", "midlab", "small", "tail"]
    big = ov["publishers"]["biglab"]
    assert big["display_name"] == "Big Lab"
    assert big["index_urls"] == ["https://huggingface.co/BigLabHF"]
    assert big["origin"] == "openrouter" and big["tier"] == 2
    assert ov["publishers"]["midlab"]["index_urls"] == []          # no HF org known
    assert ov["publishers"]["small"]["display_name"] == "small"     # no "Org: " prefix
    assert "window_end" not in ov["meta"] and "last_seen" not in big   # nothing volatile
    snap = json.loads((repo_root / "logs" / SNAPSHOT_NAME).read_text())
    assert snap["meta"]["window_end"] == "2026-09-21"
    assert 0 < snap["meta"]["other_share_of_all_tokens"] < 1
    status = {a["slug"]: a["status"] for a in snap["authors"]}
    assert status == {"biglab": "overlay", "testlab": "curated", "midlab": "overlay",
                      "small": "overlay", "tail": "overlay", "tiny": "below_cut"}
    # effective allowlist now admits overlay publishers (fresh Repo: config is
    # loaded once per process, exactly as the daily run's later phases do); base untouched
    repo = Repo(root=repo_root)
    assert repo.publisher_info("biglab")[1] == "publishers"
    assert "biglab" not in repo.base_sources["publishers"]
    assert repo.publisher_info("testlab")[0]["tier"] == 1


def test_overlay_publisher_passes_the_validator_gate(repo_root: Path, http_server: TestServer):
    from cardtrack.propose import process_proposal

    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    http_server.set_html("/bigcard", "Big Lab Model A system card with evaluations.")
    repo = Repo(root=repo_root)
    assert run_roster(repo, "r1", api_key="k")["status"] == "ok"
    p = make_proposal(http_server, "/bigcard", publisher="biglab",
                      title="Model A Card", model_names=["Model A"])
    res = process_proposal(Repo(root=repo_root), p, run_id="t", actor="human")
    assert res.status == "written", res
    rejected = process_proposal(Repo(root=repo_root),
                                make_proposal(http_server, "/bigcard", publisher="tiny"),
                                run_id="t", actor="human")
    assert rejected.status == "rejected" and "allowlist" in rejected.reason


def test_disabled_policy_skips_and_ignores_existing_overlay(repo_root: Path,
                                                            http_server: TestServer):
    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    assert run_roster(Repo(root=repo_root), "r1", api_key="k")["status"] == "ok"
    write_policy(repo_root, http_server, enabled=False)
    repo = Repo(root=repo_root)
    assert run_roster(repo, "r2", api_key="k") == {"status": "disabled"}
    assert (repo_root / "config" / OVERLAY_NAME).exists()      # file kept for re-enable
    assert repo.publisher_info("biglab") is None                # but not in effect
    assert set(repo.sources["publishers"]) == {"testlab", "tier2lab"}


def test_deny_takes_effect_immediately_even_while_sync_fails_closed(repo_root: Path,
                                                                     http_server: TestServer):
    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    assert run_roster(Repo(root=repo_root), "r1", api_key="k")["status"] == "ok"
    assert Repo(root=repo_root).publisher_info("biglab") is not None
    write_policy(repo_root, http_server, deny=["biglab"])
    http_server.routes["/rankings"] = Route(status=503, body=b"down")
    assert run_roster(Repo(root=repo_root), "r2", api_key="k")["status"] == "kept_previous"
    assert "biglab" in overlay_of(repo_root)["publishers"]        # file untouched...
    assert Repo(root=repo_root).publisher_info("biglab") is None  # ...but denied in effect


def test_missing_roster_policy_means_base_list_only(repo: Repo):
    assert repo.roster_policy == {}
    assert set(repo.sources["publishers"]) == {"testlab", "tier2lab"}


def _good_then(repo_root: Path, http_server: TestServer, bad_payload: dict | None,
               *, models=MODELS, api_key="k") -> tuple[bytes, dict]:
    serve(http_server, make_payload(), models)
    write_policy(repo_root, http_server)
    assert run_roster(Repo(root=repo_root), "good", api_key="k")["status"] == "ok"
    before = (repo_root / "config" / OVERLAY_NAME).read_bytes()
    if bad_payload is not None:
        serve(http_server, bad_payload, models)
    out = run_roster(Repo(root=repo_root), "bad", api_key=api_key)
    return before, out


def test_schema_change_keeps_previous_overlay(repo_root: Path, http_server: TestServer):
    before, out = _good_then(repo_root, http_server, make_payload(version="v2"))
    assert out["status"] == "kept_previous" and "version" in out["reason"]
    assert (repo_root / "config" / OVERLAY_NAME).read_bytes() == before
    assert (repo_root / "logs" / ".roster_failstreak").read_text() == "1"


def test_truncated_window_keeps_previous_overlay(repo_root: Path, http_server: TestServer):
    before, out = _good_then(repo_root, http_server, make_payload(days=5))
    assert out["status"] == "kept_previous" and "days in window" in out["reason"]
    assert (repo_root / "config" / OVERLAY_NAME).read_bytes() == before


def test_same_membership_leaves_overlay_byte_identical(repo_root: Path,
                                                        http_server: TestServer):
    """The overlay's git diff is the human review gate on allowlist widening, so
    a day with the same members (even different shares/window) must not touch it."""
    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    assert run_roster(Repo(root=repo_root), "r1", api_key="k")["status"] == "ok"
    path = repo_root / "config" / OVERLAY_NAME
    before, mtime = path.read_bytes(), path.stat().st_mtime_ns
    shifted = {k: v * 3 if k == "midlab" else v for k, v in DAILY.items()}
    serve(http_server, make_payload(days=28, daily=shifted))
    out = run_roster(Repo(root=repo_root), "r2", api_key="k")
    assert out["status"] == "ok" and out["new"] == [] and out["dropped"] == []
    assert path.read_bytes() == before and path.stat().st_mtime_ns == mtime


def test_programming_error_is_fail_closed_and_counted(repo_root: Path,
                                                      http_server: TestServer):
    before, out = _good_then(repo_root, http_server, None)
    write_policy(repo_root, http_server,
                 guards={"min_days_in_window": "many", "min_authors": 3,
                         "max_authors": 100, "failstreak_issue_after": 3})
    out = run_roster(Repo(root=repo_root), "bad", api_key="k")
    assert out["status"] == "kept_previous" and out["reason"].startswith("crash: ValueError")
    assert (repo_root / "config" / OVERLAY_NAME).read_bytes() == before
    assert (repo_root / "logs" / ".roster_failstreak").read_text() == "1"


def test_http_error_and_missing_key_keep_previous_overlay(repo_root: Path,
                                                          http_server: TestServer,
                                                          monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    before, out = _good_then(repo_root, http_server, None, api_key=None)
    assert out["status"] == "kept_previous" and "OPENROUTER_API_KEY" in out["reason"]
    http_server.routes["/rankings"] = Route(status=500, body=b"boom")
    out = run_roster(Repo(root=repo_root), "bad2", api_key="k")
    assert out["status"] == "kept_previous" and "HTTP 500" in out["reason"]
    assert (repo_root / "config" / OVERLAY_NAME).read_bytes() == before
    assert (repo_root / "logs" / ".roster_failstreak").read_text() == "2"


def test_failstreak_files_one_issue_then_success_resets(repo_root: Path,
                                                         http_server: TestServer):
    _, out = _good_then(repo_root, http_server, make_payload(version="v2"))
    assert out["failstreak"] == 1 and out["issue_ref"] is None
    out = run_roster(Repo(root=repo_root), "bad2", api_key="k")
    assert out["failstreak"] == 2 and out["issue_ref"] is None
    out = run_roster(Repo(root=repo_root), "bad3", api_key="k")
    assert out["failstreak"] == 3 and out["issue_ref"].startswith("outbox:")
    outbox = (repo_root / "logs" / "issues_outbox.jsonl").read_text().splitlines()
    assert len(outbox) == 1 and "roster sync" in json.loads(outbox[0])["title"]
    out = run_roster(Repo(root=repo_root), "bad4", api_key="k")
    assert out["failstreak"] == 4 and out["issue_ref"] is None    # one issue per episode
    serve(http_server, make_payload())
    assert run_roster(Repo(root=repo_root), "good2", api_key="k")["status"] == "ok"
    assert not (repo_root / "logs" / ".roster_failstreak").exists()


def test_additive_carry_over_deny_and_promotion(repo_root: Path, http_server: TestServer):
    serve(http_server, make_payload())
    write_policy(repo_root, http_server)
    assert run_roster(Repo(root=repo_root), "r1", api_key="k")["status"] == "ok"
    # Next window: biglab vanished from rankings, tail is denied, small got curated.
    gone = {k: v for k, v in DAILY.items() if k != "biglab"}
    serve(http_server, make_payload(daily=gone))
    write_policy(repo_root, http_server, deny=["tail"])
    src = yaml.safe_load((repo_root / "config" / "sources.yaml").read_text())
    src["publishers"]["small"] = {"tier": 1, "index_urls": []}
    (repo_root / "config" / "sources.yaml").write_text(yaml.safe_dump(src))
    out = run_roster(Repo(root=repo_root), "r2", api_key="k")
    assert out["status"] == "ok"
    ov = overlay_of(repo_root)
    assert "biglab" in ov["publishers"]            # additive: dropping out never removes
    assert "tail" not in ov["publishers"]          # deny removes
    assert "small" not in ov["publishers"]         # promoted to base: overlay copy dropped
    assert "tiny" in ov["publishers"]              # with biglab gone, the 99% cut reaches tiny
    assert out["dropped"] == ["small", "tail"] and out["new"] == ["tiny"]
    repo = Repo(root=repo_root)
    assert repo.publisher_info("small")[0]["tier"] == 1       # base wins


def test_aliases_map_slugs_onto_curated_keys(repo_root: Path, http_server: TestServer):
    serve(http_server, make_payload(daily={"test-lab": 50_000, "midlab": 50_000}))
    write_policy(repo_root, http_server, aliases={"test-lab": "testlab"},
                 guards={"min_days_in_window": 20, "min_authors": 2, "max_authors": 100,
                         "failstreak_issue_after": 3})
    out = run_roster(Repo(root=repo_root), "r1", api_key="k")
    assert out["status"] == "ok"
    assert set(overlay_of(repo_root)["publishers"]) == {"midlab"}
    snap = json.loads((repo_root / "logs" / SNAPSHOT_NAME).read_text())
    assert {a["slug"]: a["status"] for a in snap["authors"]} == {"test-lab": "curated",
                                                                 "midlab": "overlay"}


def test_models_endpoint_outage_is_not_fatal(repo_root: Path, http_server: TestServer):
    serve(http_server, make_payload(), models=None)     # /models 404s
    write_policy(repo_root, http_server)
    out = run_roster(Repo(root=repo_root), "r1", api_key="k")
    assert out["status"] == "ok" and out["models_info_available"] is False
    ov = overlay_of(repo_root)
    assert ov["publishers"]["biglab"]["display_name"] == "biglab"
    assert ov["publishers"]["biglab"]["index_urls"] == []


def test_monitor_sweeps_overlay_index_urls(repo_root: Path, http_server: TestServer):
    """The overlay's index_urls feed Phase A discovery exactly like curated ones."""
    from cardtrack.monitor import run_monitor

    http_server.routes["/models"] = Route(
        body=json.dumps({"data": [{"id": "biglab/x", "name": "Big Lab: X",
                                   "hugging_face_id": None}]}).encode(),
        content_type="application/json")
    serve(http_server, make_payload(), models=None)
    write_policy(repo_root, http_server)
    run_roster(Repo(root=repo_root), "r1", api_key="k")
    ov = overlay_of(repo_root)
    ov["publishers"]["biglab"]["index_urls"] = [http_server.url("/biglab-index")]
    (repo_root / "config" / OVERLAY_NAME).write_text(yaml.safe_dump(ov))
    http_server.set_html("/biglab-index",
                         '<a href="/biglab-card">Model A card</a>', title="Big Lab index")
    http_server.routes["/index-page"] = Route(body=b"<html><body>none</body></html>")
    run_monitor(Repo(root=repo_root), "m1")
    cands = json.loads((repo_root / "logs" / "candidates.json").read_text())
    urls = {c.get("url") for c in cands.get("candidates", [])}
    assert http_server.url("/biglab-card") in urls
    assert ATTESTED  # silence unused-import lint if fixtures change
