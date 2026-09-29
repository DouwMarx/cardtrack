#!/usr/bin/env python3
"""Deterministic pipeline health check: one GitHub issue per failing condition,
opened when the condition has held long enough and closed when it clears.

Runs OUTSIDE the agent sandbox, at the end of every daily run and from the
early-morning canary timer (--canary). Issue text is fixed by this script, never
by the agent, so an alert cannot carry agent-authored content.

Design rules, each learned from a real false or missed alarm:
- Thresholds are wall-clock ages, never run counts. Retries 30 minutes apart
  once filed a "2 day outage" for a 90-minute quota blip (issue #35).
- Every issue closes itself when its condition clears. Outage issues used to
  stay open forever after recovery (issue #34).
- Monitor and deploy failures alarm too. Before, they only showed in git log.
- A condition with no success marker yet starts its clock at first sight, so a
  fresh install or a newly added marker never alarms on day one.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.repo import Repo, utcnow  # noqa: E402

TITLE_PREFIX = "pipeline-alert: "
# Issues filed by the pre-health.py failstreak code; closed on recovery too.
LEGACY_PREFIXES = ("pipeline-failure: agent phase down",)
STALE_HOURS = 36          # one missed day plus the retry window
REPORT_STALE_HOURS = 8 * 24   # one missed weekly edition plus a day
OUTBOX_STUCK_HOURS = 24
TOKEN_LIFETIME_DAYS = 365
TOKEN_WARN_DAYS = 30
CANARY_ONLY = {"claude-unavailable"}


@dataclass
class Condition:
    key: str
    failing: bool
    body: str = ""


def _parse_ts(value: str) -> datetime | None:
    value = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=UTC)
        except ValueError:
            continue
    return None


def _env_value(repo: Repo, key: str) -> str:
    if os.environ.get(key):
        return os.environ[key]
    env_path = repo.root / ".env"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(rf"^\s*(?:export\s+)?{re.escape(key)}=(.*)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return ""


class State:
    """first_seen clocks for markers that do not exist yet (state/.health_state.json)."""

    def __init__(self, path: Path):
        self.path = path
        try:
            self.data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.data = {}

    def first_seen(self, key: str, now: datetime) -> datetime:
        ts = _parse_ts(self.data.get(key, "")) if key in self.data else None
        if ts is None:
            self.data[key] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            ts = now
        return ts

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=1) + "\n", encoding="utf-8")


def marker_condition(repo: Repo, state: State, now: datetime, key: str,
                     marker: str, what: str, hint: str, hours: int = STALE_HOURS) -> Condition:
    path = repo.state_dir / marker
    last = _parse_ts(path.read_text(encoding="utf-8")) if path.exists() else None
    if last and last > now + timedelta(minutes=10):
        last = None                      # a future stamp is a forgery or a clock bug
    since = last or state.first_seen(f"marker:{marker}", now)
    age = now - since
    if age <= timedelta(hours=hours):
        return Condition(key, False)
    last_txt = last.strftime("%Y-%m-%d %H:%MZ") if last else "never recorded"
    return Condition(key, True,
                     f"{what} has not succeeded for {age.total_seconds() / 3600:.0f} hours "
                     f"(last success: {last_txt}; threshold {hours} h).\n\n{hint}")


def outbox_condition(repo: Repo, now: datetime) -> Condition:
    stuck = 0
    for name in ("issues_outbox.jsonl", "comments_outbox.jsonl"):
        path = repo.logs_dir / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                ts = _parse_ts(json.loads(line).get("ts", ""))
            except json.JSONDecodeError:
                continue
            if ts and now - ts > timedelta(hours=OUTBOX_STUCK_HOURS):
                stuck += 1
    if not stuck:
        return Condition("outbox-stuck", False)
    return Condition("outbox-stuck", True,
                     f"{stuck} queued issue/comment record(s) in logs/*_outbox.jsonl are older "
                     f"than {OUTBOX_STUCK_HOURS} h. gh delivery keeps failing: check `gh auth "
                     "status` on the host and the flush_outbox line in the latest run log.")


def rejected_condition(repo: Repo) -> Condition:
    path = repo.state_dir / ".deploy_rejected"
    if not path.exists():
        return Condition("deploy-rejected", False)
    sha, _, when = path.read_text(encoding="utf-8").strip().partition(" ")
    return Condition("deploy-rejected", True,
                     f"Production refused to move to origin/main {sha[:12]} ({when}): the test "
                     "suite failed on it, so the host keeps running the previous commit. Fix "
                     "main; the next run picks up the new commit and this issue closes.")


def token_condition(repo: Repo, now: datetime) -> Condition:
    if not _env_value(repo, "CLAUDE_CODE_OAUTH_TOKEN"):
        return Condition("claude-token-expiring", False)
    created = _parse_ts(_env_value(repo, "CLAUDE_TOKEN_CREATED"))
    if created is None:
        return Condition("claude-token-expiring", True,
                         "CLAUDE_CODE_OAUTH_TOKEN is set but CLAUDE_TOKEN_CREATED (YYYY-MM-DD) "
                         "is missing from .env, so its one-year expiry cannot be tracked.")
    left = created + timedelta(days=TOKEN_LIFETIME_DAYS) - now
    if left > timedelta(days=TOKEN_WARN_DAYS):
        return Condition("claude-token-expiring", False)
    return Condition("claude-token-expiring", True,
                     f"The Claude setup-token created {created:%Y-%m-%d} expires in about "
                     f"{max(left.days, 0)} days. Renew it (see infra/README.md, 'Rotate the "
                     "Claude token') before the daily agent starts failing.")


def agent_model(repo: Repo) -> str:
    m = re.search(r"--model\s+(\S+)", repo.setting("agent.cmd", "") or "")
    return m.group(1) if m else "opus"


def canary_condition(repo: Repo, attempts: int = 3, wait_s: int = 120,
                     runner: Callable[[list[str], dict], tuple[int, str]] | None = None
                     ) -> Condition:
    """One tiny model call with the pipeline's own credentials and model. A single
    429/529 is not an outage, so only `attempts` consecutive failures alarm."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    token = _env_value(repo, "CLAUDE_CODE_OAUTH_TOKEN")
    if token:
        env["CLAUDE_CODE_OAUTH_TOKEN"] = token
    config_dir = _env_value(repo, "CLAUDE_CONFIG_DIR")
    if config_dir and not token:
        env["CLAUDE_CONFIG_DIR"] = os.path.expanduser(config_dir)
    cmd = ["claude", "-p", "Reply with the single word: ok", "--model", agent_model(repo),
           "--max-turns", "1", "--output-format", "text"]

    def default_runner(c: list[str], e: dict) -> tuple[int, str]:
        try:
            p = subprocess.run(c, env=e, capture_output=True, text=True, timeout=180)
            return p.returncode, (p.stdout + p.stderr).strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            return 1, str(exc)

    run = runner or default_runner
    last = ""
    for i in range(attempts):
        rc, out = run(cmd, env)
        if rc == 0 and re.fullmatch(r"\W*ok\W*", out.strip(), re.I):
            return Condition("claude-unavailable", False)
        last = out.splitlines()[-1][:300] if out else f"exit {rc}"
        if i < attempts - 1:
            time.sleep(wait_s)
    return Condition("claude-unavailable", True,
                     f"The pre-run canary could not get a reply from `claude --model "
                     f"{agent_model(repo)}` after {attempts} attempts. Last output:\n\n"
                     f"```\n{last}\n```\n\nToday's agent phase will fail the same way. "
                     "Expired or revoked token: see infra/README.md, 'Rotate the Claude "
                     "token'. Usage limit: it resets by itself; this issue closes on the next "
                     "passing check.")


def evaluate(repo: Repo, now: datetime, canary: bool,
             runner: Callable | None = None) -> list[Condition]:
    state = State(repo.state_dir / ".health_state.json")
    conds = []
    if bool(repo.setting("agent.enabled", False)):
        conds.append(marker_condition(
            repo, state, now, "agent-down", ".agent_last_success", "The curation agent (Phase B)",
            "Candidates are piling up untriaged. See the Phase B section of the latest "
            "logs/run-*.log."))
    conds.append(marker_condition(
        repo, state, now, "monitor-down", ".monitor_last_ok", "The link monitor (Phase A)",
        "Every link check errored, which usually means the host has no network."))
    if bool(repo.setting("publish.wrangler_deploy", False)):
        conds.append(marker_condition(
            repo, state, now, "deploy-failing", ".deploy_last_ok", "The site deploy (wrangler)",
            "The live site is stale. Check CLOUDFLARE_API_TOKEN and the wrangler lines of "
            "the latest run log."))
    if bool(repo.setting("report.enabled", False)):
        conds.append(marker_condition(
            repo, state, now, "report-stale", ".report_last_ok", "The weekly research report",
            "The Analysis page is out of date. See the latest logs/report-*.log and "
            "report/out/RUN_SUMMARY.md.", hours=REPORT_STALE_HOURS))
    if _env_value(repo, "R2_BUCKET"):
        conds.append(marker_condition(
            repo, state, now, "backup-stale", ".backup_last_ok", "The R2 copy of data/raw",
            "The raw archive has no fresh off-site copy. Check the R2_* keys in .env and "
            "the [backup] lines of the latest run log."))
    if repo.setting("publish.git_push", False) and _env_value(repo, "CARDTRACK_ROLE") == "prod":
        conds.append(marker_condition(
            repo, state, now, "push-failing", ".push_last_ok", "Pushing to GitHub",
            "Commits are piling up on the host. Check `gh auth status` and the push "
            "lines of the latest run log."))
    conds.append(rejected_condition(repo))
    conds.append(outbox_condition(repo, now))
    conds.append(token_condition(repo, now))
    if canary:
        conds.append(canary_condition(repo, runner=runner))
    state.save()
    return conds


def _gh(args: list[str]) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None


def sync_issues(gh_repo: str, conds: list[Condition], gh: Callable = _gh) -> dict:
    """Open one issue per failing condition, close issues whose condition cleared.
    Lists open issues directly (not the search API, which lags and caused dupes)."""
    proc = gh(["issue", "list", "-R", gh_repo, "--state", "open", "--limit", "300",
               "--json", "number,title"])
    if not proc or proc.returncode != 0:
        return {"error": "could not list issues; nothing changed"}
    open_issues = json.loads(proc.stdout or "[]")
    by_title = {i["title"]: i["number"] for i in open_issues}
    opened, closed = [], []
    for c in conds:
        title = TITLE_PREFIX + c.key
        if c.failing and title not in by_title:
            body = c.body + f"\n\n_Filed by scripts/health.py at {utcnow()}. It closes itself " \
                            "when the condition clears._"
            p = gh(["issue", "create", "-R", gh_repo, "--title", title, "--body", body])
            if p and p.returncode == 0:
                opened.append(c.key)
        elif not c.failing and title in by_title:
            gh(["issue", "close", str(by_title[title]), "-R", gh_repo, "--comment",
                f"Resolved: condition cleared ({utcnow()})."])
            closed.append(c.key)
    # An alert whose condition is no longer evaluated at all (feature switched off)
    # would otherwise stay open forever. Canary-only conditions are exempt: the
    # daily run does not evaluate them, and must not close the canary's issue.
    evaluated = {c.key for c in conds}
    for title, number in by_title.items():
        key = title[len(TITLE_PREFIX):] if title.startswith(TITLE_PREFIX) else None
        if key and key not in evaluated and key not in CANARY_ONLY:
            gh(["issue", "close", str(number), "-R", gh_repo, "--comment",
                f"Closed: this check is no longer enabled ({utcnow()})."])
            closed.append(key)
    agent_ok = any(c.key == "agent-down" and not c.failing for c in conds)
    for title, number in by_title.items():
        if agent_ok and title.startswith(LEGACY_PREFIXES):
            gh(["issue", "close", str(number), "-R", gh_repo, "--comment",
                f"Resolved: the agent phase has succeeded since ({utcnow()})."])
            closed.append(f"legacy#{number}")
    return {"opened": opened, "closed": closed}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--root")
    p.add_argument("--canary", action="store_true",
                   help="also make one model call with the pipeline's credentials")
    args = p.parse_args(argv)
    repo = Repo.locate(args.root)
    conds = evaluate(repo, datetime.now(UTC), args.canary)
    failing = [c.key for c in conds if c.failing]
    summary: dict = {"failing": failing}
    gh_repo = repo.setting("github.repo") or ""
    role = _env_value(repo, "CARDTRACK_ROLE") or "dev"
    if role != "prod":
        summary["issues"] = f"not synced (CARDTRACK_ROLE={role})"
    elif gh_repo and repo.setting("github.use_gh", True) and shutil.which("gh"):
        summary["issues"] = sync_issues(gh_repo, conds)
    print(json.dumps(summary))
    # Only the canary's own failure is an exit-code signal (systemd shows it);
    # a daily run must never fail because its health report did.
    return 1 if args.canary and "claude-unavailable" in failing else 0


if __name__ == "__main__":
    sys.exit(main())
