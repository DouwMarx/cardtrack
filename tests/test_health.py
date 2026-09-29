"""scripts/health.py: time-based thresholds, self-closing issues, no day-one alarms.
Each test pins a false or missed alarm the old failstreak code produced."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

from cardtrack.repo import Repo
from scripts import health

NOW = datetime(2026, 9, 29, 12, 0, tzinfo=UTC)


def _repo(tmp_path: Path, env: str = "", **settings) -> Repo:
    (tmp_path / "config").mkdir()
    (tmp_path / "logs").mkdir()
    (tmp_path / "state").mkdir()
    base = {"agent": {"enabled": True, "cmd": "claude -p x --model opus"},
            "publish": {"wrangler_deploy": True}}
    base.update(settings)
    (tmp_path / "config" / "settings.yaml").write_text(yaml.safe_dump(base))
    if env:
        (tmp_path / ".env").write_text(env)
    return Repo(root=tmp_path)


def _mark(repo: Repo, name: str, when: datetime) -> None:
    (repo.state_dir / name).write_text(when.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


def _fresh_markers(repo: Repo, when: datetime = NOW) -> None:
    for m in (".agent_last_success", ".monitor_last_ok", ".deploy_last_ok"):
        _mark(repo, m, when)


def _failing(conds) -> set[str]:
    return {c.key for c in conds if c.failing}


def test_same_morning_retries_are_not_an_outage(tmp_path):
    """Issue #35: two failed runs 33 minutes apart after a success the day before."""
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    _mark(repo, ".agent_last_success", NOW - timedelta(hours=26))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == set()


def test_agent_down_past_threshold_alarms(tmp_path):
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    _mark(repo, ".agent_last_success", NOW - timedelta(hours=40))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"agent-down"}


def test_missing_marker_starts_clock_instead_of_alarming(tmp_path):
    """A fresh install (or the newly added monitor/deploy markers) must not alarm."""
    repo = _repo(tmp_path)
    assert _failing(health.evaluate(repo, NOW, canary=False)) == set()
    later = NOW + timedelta(hours=37)
    assert _failing(health.evaluate(repo, later, canary=False)) == {
        "agent-down", "monitor-down", "deploy-failing"}


def test_monitor_and_deploy_failures_alarm(tmp_path):
    """Previously visible only as a commit prefix (monitor) or not at all (deploy)."""
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    _mark(repo, ".monitor_last_ok", NOW - timedelta(days=3))
    _mark(repo, ".deploy_last_ok", NOW - timedelta(days=2))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"monitor-down", "deploy-failing"}


def test_disabled_features_are_not_checked(tmp_path):
    repo = _repo(tmp_path, agent={"enabled": False}, publish={"wrangler_deploy": False})
    _mark(repo, ".monitor_last_ok", NOW)
    assert {c.key for c in health.evaluate(repo, NOW + timedelta(days=9), canary=False)} == {
        "monitor-down", "deploy-rejected", "outbox-stuck", "claude-token-expiring"}


def test_stuck_outbox_alarms(tmp_path):
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    old = (NOW - timedelta(hours=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    (repo.logs_dir / "issues_outbox.jsonl").write_text(json.dumps({"ts": old, "title": "t"}) + "\n")
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"outbox-stuck"}


def test_token_expiry_warning(tmp_path):
    repo = _repo(tmp_path, env="CLAUDE_CODE_OAUTH_TOKEN=abc\nCLAUDE_TOKEN_CREATED=2025-10-20\n")
    _fresh_markers(repo)
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"claude-token-expiring"}
    (tmp_path / ".env").write_text("CLAUDE_CODE_OAUTH_TOKEN=abc\nCLAUDE_TOKEN_CREATED=2026-09-01\n")
    assert _failing(health.evaluate(repo, NOW, canary=False)) == set()


def test_canary_tolerates_one_transient_error(tmp_path):
    repo = _repo(tmp_path)
    calls = []

    def flaky(cmd, env):
        calls.append(cmd)
        return (1, "API Error: 529 Overloaded") if len(calls) == 1 else (0, "OK.")

    assert not health.canary_condition(repo, wait_s=0, runner=flaky).failing
    assert "--model" in calls[0] and calls[0][calls[0].index("--model") + 1] == "opus"


def test_canary_alarms_after_repeated_failure_and_passes_token(tmp_path):
    repo = _repo(tmp_path, env="CLAUDE_CODE_OAUTH_TOKEN=tok-123\n")
    seen_env = {}

    def down(cmd, env):
        seen_env.update(env)
        return 1, "You've hit your session limit"

    c = health.canary_condition(repo, attempts=2, wait_s=0, runner=down)
    assert c.failing and "session limit" in c.body
    assert seen_env["CLAUDE_CODE_OAUTH_TOKEN"] == "tok-123"
    assert "ANTHROPIC_API_KEY" not in seen_env


class FakeGh:
    def __init__(self, open_issues):
        self.open = list(open_issues)
        self.calls = []

    def __call__(self, args):
        self.calls.append(args)
        out = json.dumps(self.open) if args[:2] == ["issue", "list"] else "https://x/1\n"
        return subprocess.CompletedProcess(args, 0, stdout=out, stderr="")

    def verbs(self):
        return [(a[1], a[2] if a[1] == "close" else a[a.index("--title") + 1] if "--title" in a
                 else None) for a in self.calls if a[1] != "list"]


def test_sync_opens_once_and_closes_on_recovery():
    gh = FakeGh([{"number": 7, "title": "pipeline-alert: agent-down"}])
    conds = [health.Condition("agent-down", True, "x"),
             health.Condition("monitor-down", True, "y")]
    health.sync_issues("o/r", conds, gh=gh)
    assert gh.verbs() == [("create", "pipeline-alert: monitor-down")]  # agent-down already open

    gh = FakeGh([{"number": 7, "title": "pipeline-alert: agent-down"}])
    health.sync_issues("o/r", [health.Condition("agent-down", False)], gh=gh)
    assert gh.verbs() == [("close", "7")]


def test_sync_closes_legacy_failstreak_issues_once_agent_recovers():
    """Issues #34/#35 were filed by the old code and never closed."""
    legacy = [{"number": 34, "title": "pipeline-failure: agent phase down 2 consecutive runs (a)"},
              {"number": 35, "title": "pipeline-failure: agent phase down 2 consecutive runs (b)"}]
    gh = FakeGh(legacy)
    health.sync_issues("o/r", [health.Condition("agent-down", True, "x")], gh=gh)
    assert ("close", "34") not in gh.verbs()
    gh = FakeGh(legacy)
    health.sync_issues("o/r", [health.Condition("agent-down", False)], gh=gh)
    assert {v for v in gh.verbs()} == {("close", "34"), ("close", "35")}


def test_sync_changes_nothing_when_listing_fails():
    def broken(args):
        return subprocess.CompletedProcess(args, 1, stdout="", stderr="auth")

    assert "error" in health.sync_issues("o/r", [health.Condition("agent-down", True, "x")],
                                         gh=broken)


def test_rejected_deploy_alarms_until_cleared(tmp_path):
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    (repo.state_dir / ".deploy_rejected").write_text("abc123 2026-09-29T06:00:00Z\n")
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"deploy-rejected"}
    (repo.state_dir / ".deploy_rejected").unlink()
    assert _failing(health.evaluate(repo, NOW, canary=False)) == set()


def test_weekly_report_alarms_only_after_a_missed_edition(tmp_path):
    repo = _repo(tmp_path, report={"enabled": True})
    _fresh_markers(repo)
    _mark(repo, ".report_last_ok", NOW - timedelta(days=7, hours=20))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == set()
    _mark(repo, ".report_last_ok", NOW - timedelta(days=9))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"report-stale"}


def test_backup_checked_only_when_r2_configured(tmp_path):
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    assert "backup-stale" not in {c.key for c in health.evaluate(repo, NOW, canary=False)}
    (tmp_path / ".env").write_text("R2_BUCKET=b\n")
    _mark(repo, ".backup_last_ok", NOW - timedelta(days=2))
    assert _failing(health.evaluate(repo, NOW, canary=False)) == {"backup-stale"}


def test_future_marker_is_not_trusted(tmp_path):
    """logs/ was agent-writable; a forged far-future stamp must not silence alarms."""
    repo = _repo(tmp_path)
    _fresh_markers(repo)
    _mark(repo, ".agent_last_success", NOW + timedelta(days=365))
    health.evaluate(repo, NOW, canary=False)          # starts the first-seen clock
    later = NOW + timedelta(hours=37)
    for m in (".monitor_last_ok", ".deploy_last_ok"):
        _mark(repo, m, later)
    assert _failing(health.evaluate(repo, later, canary=False)) == {"agent-down"}


def test_canary_needs_a_real_ok(tmp_path):
    repo = _repo(tmp_path)
    c = health.canary_condition(repo, attempts=1, wait_s=0,
                                runner=lambda cmd, env: (0, "Invalid token, please login"))
    assert c.failing


def test_disabled_check_issue_closes_but_canary_issue_survives_daily_run():
    gh = FakeGh([{"number": 3, "title": "pipeline-alert: report-stale"},
                 {"number": 4, "title": "pipeline-alert: claude-unavailable"}])
    health.sync_issues("o/r", [health.Condition("agent-down", False)], gh=gh)
    assert gh.verbs() == [("close", "3")]
