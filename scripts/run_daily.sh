#!/usr/bin/env bash
# Daily run orchestrator: Phase A monitor → Phase B agent → Phase C build/publish.
# Idempotent and lock-guarded; a missed day self-heals on the next run.
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
export CARDTRACK_ROOT="$ROOT"
cd "$SCRIPT_ROOT"
# shellcheck source=lib.sh
. "$SCRIPT_ROOT/scripts/lib.sh"
standard_path

RUN_ID="${RUN_ID:-$(date -u +%Y-%m-%dT%H:%MZ)-local}"
mkdir -p "$ROOT/logs" "$ROOT/state"
# One-time move (2026-09-29): markers used to live in logs/, which the agent can write.
for m in .agent_last_success .monitor_last_ok .deploy_last_ok .health_state.json; do
  [ -f "$ROOT/logs/$m" ] && [ ! -f "$ROOT/state/$m" ] && mv "$ROOT/logs/$m" "$ROOT/state/$m"
done
AGENT_FAILED=0
DEPLOY_FAILED=0
# prod: publishes, files alert issues, pulls new code before running.
# dev (default, so a fresh clone can never publish with your git credentials):
# runs every phase but never commits, pushes, deploys, flushes issues or pulls.
# Production sets CARDTRACK_ROLE=prod in .env (infra/prod.env.example).
ROLE="${CARDTRACK_ROLE:-$(envget CARDTRACK_ROLE "$ROOT")}"; ROLE="${ROLE:-dev}"
# Non-secret: where the /login credential lives when no setup-token is used.
CFG_DIR="$(envget CLAUDE_CONFIG_DIR "$ROOT")"
[ -n "$CFG_DIR" ] && export CLAUDE_CONFIG_DIR="${CFG_DIR/#\~/$HOME}"
publish_on() { [ "$ROLE" = "prod" ] && [ "$(setting "$1" false)" = "true" ]; }

exec 9>"$ROOT/.run.lock"
# Wait rather than skip: the weekly report holds this lock for up to ~2 h, and a
# skipped day would never be retried (the timer already fired).
flock -w 10800 9 || { echo "[run_daily] lock held for 3 h; exiting for a retry"; exit 75; }

LOG="$ROOT/logs/run-$(date -u +%Y%m%d-%H%M%SZ).log"
exec > >(tee -a "$LOG") 2>&1

PY=(uv run --project "$SCRIPT_ROOT" python)
setting() { "${PY[@]}" scripts/get_setting.py "$1" --default "${2:-}" --root "$ROOT"; }
# Fail fast on unparseable config: every `setting` call would otherwise fall back
# to its default and silently disable features (report.enabled -> off, exit 0).
"${PY[@]}" scripts/get_setting.py site.title --root "$ROOT" >/dev/null \
  || { echo "ERROR: config/settings.yaml does not parse; refusing to run on defaults"; exit 2; }

echo "== cardtrack run $RUN_ID ($(date -u +%FT%TZ), role=$ROLE) =="
# New code arrives BEFORE this script starts (systemd ExecStartPre runs
# scripts/deploy_update.sh), because git rewriting a bash script mid-run corrupts it.

# Network gate. The Persistent timer fires the instant the laptop resumes from
# suspend, seconds before Wi-Fi is back; without this every phase fails in the
# first minute (2026-09-16..22). Exit 75 = EX_TEMPFAIL: nothing was touched,
# and the systemd unit retries the whole run later (Restart=on-failure).
"${PY[@]}" scripts/wait_for_network.py --root "$ROOT" \
  || { echo "[run_daily] NO NETWORK: exiting for a later retry"; exit 75; }

# Roster sync first, so a newly admitted publisher's index_urls are swept by
# the monitor the same day (config/roster.yaml). Fail-closed inside; the shell
# fallback only covers an interpreter-level crash, which must not stop the day.
echo "-- Phase A: roster sync"
"${PY[@]}" scripts/roster.py --run-id "$RUN_ID" --root "$ROOT" \
  || echo "[run_daily] WARNING: roster sync crashed; previous overlay kept"

echo "-- Phase A: monitor"
MON_JSON="$("${PY[@]}" scripts/monitor.py --run-id "$RUN_ID" --root "$ROOT")"
echo "$MON_JSON"
# Total link-check outage (network down): monitor.py freezes candidate expiry
# itself; here we just make the day visibly abnormal in git log.
# NB: the JSON must travel via argv — with a heredoc, stdin carries the script
# itself, so piping data in would silently read nothing (bug found 2026-09-07).
MONITOR_OUTAGE="$("${PY[@]}" - "$MON_JSON" <<'PYEOF'
import json, sys
try:
    s = json.loads(sys.argv[1].strip().splitlines()[-1])
    print(1 if s.get("checked", 0) > 0 and s.get("ok", 0) == 0 else 0)
except Exception:
    print(0)
PYEOF
)"
if [ "$MONITOR_OUTAGE" = "1" ]; then
  echo "[run_daily] MONITOR OUTAGE: all link checks errored (network down?)"
else
  date -u +%FT%TZ > "$ROOT/state/.monitor_last_ok"
fi

echo "-- Phase B: agent"
if [ "$(setting agent.enabled false)" = "true" ]; then
  "${PY[@]}" scripts/state_summary.py --root "$ROOT" --out "$ROOT/logs/state_summary.json"
  GH_REPO="$(setting github.repo)"
  if [ -n "$GH_REPO" ] && command -v gh >/dev/null; then
    gh issue list -R "$GH_REPO" --label data-error --state open \
      --json number,title,body,labels,url --limit 100 \
      > "$ROOT/logs/.issues_a.json" || echo "[]" > "$ROOT/logs/.issues_a.json"
    gh issue list -R "$GH_REPO" --label missing-doc --state open \
      --json number,title,body,labels,url --limit 100 \
      > "$ROOT/logs/.issues_b.json" || echo "[]" > "$ROOT/logs/.issues_b.json"
    "${PY[@]}" - "$ROOT/logs/.issues_a.json" "$ROOT/logs/.issues_b.json" \
      > "$ROOT/logs/open_issues.json" <<'MERGE'
import json, sys
seen = {}
for path in sys.argv[1:]:
    try:
        with open(path) as f:
            for item in json.load(f):
                seen[item["number"]] = item
    except Exception:
        pass
print(json.dumps(sorted(seen.values(), key=lambda x: x["number"]), indent=1))
MERGE
    rm -f "$ROOT/logs/.issues_a.json" "$ROOT/logs/.issues_b.json"
  else
    echo "[]" > "$ROOT/logs/open_issues.json"
  fi
  AGENT_CMD="$(setting agent.cmd)"
  if [ -n "$AGENT_CMD" ]; then
    export CARDTRACK_RUN_ID="$RUN_ID"
    export CARDTRACK_ACTOR="agent"
    # One authoritative turn cap: the agent command interpolates this, so the
    # number lives in settings.yaml and nowhere else.
    export CARDTRACK_MAX_TURNS="$(setting agent.max_turns 600)"
    # Wall clock, not turns, is what must never run into tomorrow's trigger.
    AGENT_TIMEOUT="$(setting agent.timeout_seconds 7200)"
    # Self-heal the most common Phase B outage: an expired OAuth access token.
    # The sandbox strips the refresh token (see agent_sandbox.sh), so refresh can
    # only happen out here on the host — one trivial headless call does it, and
    # only runs when the token would expire before the agent could finish.
    # Not needed (and skipped) with a setup-token in CLAUDE_CODE_OAUTH_TOKEN.
    CRED_FILE="$(claude_config_dir)/.credentials.json"
    if [ "${CARDTRACK_SKIP_TOKEN_REFRESH:-}" != "1" ] \
        && [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-$(envget CLAUDE_CODE_OAUTH_TOKEN "$ROOT")}" ] \
        && command -v claude >/dev/null && [ -f "$CRED_FILE" ]; then
      NEED_REFRESH="$("${PY[@]}" - "$CRED_FILE" "$AGENT_TIMEOUT" <<'PYEOF'
import json, sys, time
try:  # expiresAt is epoch-ms metadata, not a secret value
    exp = json.load(open(sys.argv[1])).get("claudeAiOauth", {}).get("expiresAt", 0)
    print("yes" if exp / 1000 < time.time() + int(sys.argv[2]) else "no")
except Exception:
    print("no")
PYEOF
)"
      if [ "$NEED_REFRESH" = "yes" ]; then
        echo "[run_daily] access token expires within the agent window; refreshing"
        REFRESH_GUARD=()
        command -v timeout >/dev/null && REFRESH_GUARD=(timeout 120)
        "${REFRESH_GUARD[@]}" claude -p "ok" --max-turns 1 >/dev/null 2>&1 \
          || echo "[run_daily] WARNING: token refresh failed; run any interactive claude command"
      fi
    fi
    # Heartbeat: the agent must both exit 0 AND have written this run's report —
    # exit status alone can lie (a wedged CLI can exit 0 having done nothing).
    PHASE_B_MARK="$ROOT/state/.phase_b_started"
    touch "$PHASE_B_MARK"
    GUARD=()
    if command -v timeout >/dev/null; then
      GUARD=(timeout --kill-after=60 "$AGENT_TIMEOUT")
    else
      echo "[run_daily] WARNING: coreutils timeout missing; agent runs unguarded"
    fi
    RC=0
    "${GUARD[@]}" bash scripts/agent_sandbox.sh bash -c "$AGENT_CMD" || RC=$?
    if [ "$RC" -eq 124 ] || [ "$RC" -eq 137 ]; then
      echo "[run_daily] agent killed by the ${AGENT_TIMEOUT}s wall-clock backstop (continuing to Phase C)"
    elif [ "$RC" -ne 0 ]; then
      echo "[run_daily] agent exited $RC (continuing to Phase C)"
    fi
    if [ "$RC" -eq 0 ] && [ "$ROOT/logs/run_report.md" -nt "$PHASE_B_MARK" ]; then
      date -u +%FT%TZ > "$ROOT/state/.agent_last_success"
    else
      [ "$RC" -eq 0 ] && echo "[run_daily] agent exited 0 but wrote no run report; treating as FAILED"
      AGENT_FAILED=1
      # No issue from here: scripts/health.py (end of run) alarms on the AGE of
      # .agent_last_success, so same-morning retries can never read as an outage.
      echo "[run_daily] AGENT PHASE FAILED (last success: $(cat "$ROOT/state/.agent_last_success" 2>/dev/null || echo never))"
    fi
    rm -f "$PHASE_B_MARK"
    unset CARDTRACK_ACTOR CARDTRACK_MAX_TURNS
    # preserve the session transcript before the next run's sandbox wipes it
    # (local-only audit trail: which tool calls the agent actually made)
    if [ -d "$ROOT/.agent-home/.claude/projects" ]; then
      mkdir -p "$ROOT/logs/agent-transcripts"
      cp -r "$ROOT/.agent-home/.claude/projects" \
        "$ROOT/logs/agent-transcripts/$RUN_ID" 2>/dev/null || true
    fi
  else
    echo "[run_daily] agent.enabled=true but agent.cmd is empty; skipping"
  fi
else
  echo "agent disabled (agent.enabled=false)"
  # Deliberately agent-less deployments still get normal candidate TTL expiry
  # (the guard in monitor.py would otherwise stretch it to the hard cap).
  date -u +%FT%TZ > "$ROOT/state/.agent_last_success"
fi

echo "-- Phase C: build & publish"
"${PY[@]}" scripts/build_site.py --root "$ROOT"

# Outbound review gate (outside the sandbox): deterministic secret scan over
# everything about to go public, then an optional LLM screen over agent-authored
# text. Fail CLOSED: on any finding, nothing is flushed, committed, or deployed
# this run (see logs/SECURITY_HOLD.md), and the run exits nonzero for visibility.
HOLD=0
# A hold from a previous run persists until a human clears the file: the flagged
# text is still in the DB/logs this run would otherwise publish.
if [ -s "$ROOT/logs/SECURITY_HOLD.md" ]; then
  HOLD=1
  echo "[run_daily] SECURITY HOLD: unresolved logs/SECURITY_HOLD.md from a prior run; review, clean, delete it, then rerun"
fi
if [ "$HOLD" -eq 0 ]; then
  # Full heuristic scan over the agent-authored surface (docs.sqlite carries every
  # changelog justification/notes/summary; logs carries reports + outboxes).
  "${PY[@]}" scripts/secret_scan.py --root "$ROOT" "$ROOT/data/docs.sqlite" "$ROOT/logs" \
    || { HOLD=1; echo "[run_daily] SECURITY HOLD: secret scan findings (logs/SECURITY_HOLD.md)"; }
fi
if [ "$HOLD" -eq 0 ]; then
  # Literal-only scan over the rest of the published+deployed surface (site/,
  # data/text/): exact-match against live local secret values has zero false
  # positives, so it is safe over third-party document text that would trip the
  # heuristic regexes. This closes the exfil channel through those dirs.
  "${PY[@]}" scripts/secret_scan.py --root "$ROOT" --literal-only "$ROOT/site" "$ROOT/data/text" \
    || { HOLD=1; echo "[run_daily] SECURITY HOLD: literal secret found in site/ or data/text/ (logs/SECURITY_HOLD.md)"; }
fi
if [ "$HOLD" -eq 0 ]; then
  "${PY[@]}" scripts/review_outbound.py --root "$ROOT" \
    || { HOLD=1; echo "[run_daily] SECURITY HOLD: LLM screen flagged outbound text (logs/SECURITY_HOLD.md)"; }
fi

if [ "$HOLD" -eq 0 ] && [ "$ROLE" = "prod" ]; then
  # deliver issues/comments the sandboxed agent could only queue (gh is
  # unauthenticated inside; flush re-scans each record individually)
  "${PY[@]}" scripts/flush_outbox.py --root "$ROOT"
fi

if [ "$HOLD" -eq 0 ] && publish_on publish.git_commit; then
  # render the message BEFORE staging: --emit-commit-msg opens the DB, and
  # connect() rewrites views, which would leave docs.sqlite perpetually dirty
  MSG="$("${PY[@]}" scripts/build_site.py --root "$ROOT" --emit-commit-msg "$RUN_ID")"
  # Outages must be visible where the operator actually looks: git log.
  if [ "$AGENT_FAILED" -ne 0 ]; then
    MSG="[agent failed; last success $(cut -c1-10 "$ROOT/state/.agent_last_success" 2>/dev/null || echo never)] $MSG"
  fi
  if [ "$MONITOR_OUTAGE" = "1" ]; then
    MSG="[monitor outage] $MSG"
  fi
  # Allow-list, not a directory sweep: `git add logs` once published the agent's
  # scratch files (2026-09-21). Every path is named; a missing one is skipped
  # because a missing pathspec would abort the whole add.
  for path in data site config/sources.generated.yaml \
              logs/friction.jsonl logs/PROPOSALS.md logs/RESOLVED.md logs/run_report.md \
              logs/issues_outbox.jsonl logs/comments_outbox.jsonl; do
    [ -e "$ROOT/$path" ] && git -C "$ROOT" add "$path"
  done
  if git -C "$ROOT" diff --cached --quiet; then
    echo "nothing to commit"
  else
    git -C "$ROOT" commit -m "$MSG"
  fi
  # Push whenever ahead (also yesterday's stranded commit). A push flake must not
  # abort the run; the next run retries. Never `pull --rebase` here: that would
  # bring in upstream code the test gate has not seen, or has rejected.
  # deploy_update.sh rebases and tests before the next run instead.
  if publish_on publish.git_push && [ -n "$(git -C "$ROOT" log --oneline '@{u}..HEAD' 2>/dev/null)" ]; then
    git -C "$ROOT" push || echo "[run_daily] WARNING: push failed; next run retries"
  fi
  if [ -z "$(git -C "$ROOT" log --oneline '@{u}..HEAD' 2>/dev/null)" ]; then
    date -u +%FT%TZ > "$ROOT/state/.push_last_ok"
  fi
fi

# Before the deploy, so a new version's "original" link never points at a file
# that is not uploaded yet.
if [ "$HOLD" -eq 0 ] && [ "$ROLE" = "prod" ]; then
  bash scripts/backup.sh "$ROOT" || echo "[run_daily] WARNING: R2 backup failed (health alarms after 36 h)"
fi

if [ "$HOLD" -eq 0 ] && publish_on publish.wrangler_deploy; then
  # Subshell: the deploy token is exported for wrangler only, never to later steps.
  # A failed deploy (2026-09-20: DNS error) used to kill the run under set -e with
  # exit 1, which systemd never retries; now it is exit 5 and a health alarm.
  # Only the two Cloudflare variables reach the (npm-fetched) wrangler process.
  if ( CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(envget CLOUDFLARE_API_TOKEN "$ROOT")}"
       CLOUDFLARE_ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-$(envget CLOUDFLARE_ACCOUNT_ID "$ROOT")}"
       export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID
       npx -y "wrangler@$(setting publish.wrangler_version 4)" pages deploy "$ROOT/site" \
         --project-name "$(setting publish.wrangler_project cardtrack)" \
         --commit-dirty=true ); then
    date -u +%FT%TZ > "$ROOT/state/.deploy_last_ok"
  else
    DEPLOY_FAILED=1
    echo "[run_daily] DEPLOY FAILED (wrangler); the next run retries"
  fi
fi

# Health: open/close one GitHub issue per failing condition (time-based, self-closing).
"${PY[@]}" scripts/health.py --root "$ROOT" || echo "[run_daily] WARNING: health check crashed"

# Local run output is unbounded otherwise (the laptop reached 124 MB in 8 weeks).
# Tracked files are never touched; only per-run logs, transcripts and diffs age out.
RETENTION_DAYS="$(setting logs.retention_days 90)"
if [ "$RETENTION_DAYS" -gt 0 ] 2>/dev/null; then
  find "$ROOT/logs" -maxdepth 1 -type f \( -name 'run-*.log' -o -name 'report-*.log' \) \
    -mtime +"$RETENTION_DAYS" -delete 2>/dev/null || true
  find "$ROOT/logs/agent-transcripts" "$ROOT/logs/version_diffs" -mindepth 1 -maxdepth 1 \
    -mtime +"$RETENTION_DAYS" -exec rm -rf {} + 2>/dev/null || true
fi


if [ "$HOLD" -ne 0 ]; then
  echo "== run $RUN_ID HELD (nothing published; see logs/SECURITY_HOLD.md) =="
  exit 10      # distinct from 1 (any unexpected set -e failure), which systemd retries
fi
if [ "$AGENT_FAILED" -ne 0 ]; then
  # Publishing still happened; the nonzero exit marks the systemd unit failed so
  # the outage is visible in `systemctl --user --failed` too, and triggers the
  # unit's Restart=on-failure retry (lock-guarded, caps are rolling 24 h).
  echo "== run $RUN_ID complete BUT AGENT PHASE FAILED (see above) =="
  exit 3
fi
if [ "$MONITOR_OUTAGE" = "1" ]; then
  echo "== run $RUN_ID complete BUT MONITOR OUTAGE (network dropped mid-run; retry scheduled) =="
  exit 4
fi
if [ "$DEPLOY_FAILED" -ne 0 ]; then
  echo "== run $RUN_ID complete BUT DEPLOY FAILED (retry scheduled) =="
  exit 5
fi
echo "== run $RUN_ID complete =="
