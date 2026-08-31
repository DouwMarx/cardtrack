#!/usr/bin/env bash
# Daily run orchestrator: Phase A monitor → Phase B agent → Phase C build/publish.
# Idempotent and lock-guarded; a missed day self-heals on the next run.
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
export CARDTRACK_ROOT="$ROOT"
cd "$SCRIPT_ROOT"

# Schedulers (cron, systemd timers) run with a minimal PATH. Prepend the places
# uv/claude/npx/git actually live on NixOS and Debian; nonexistent dirs are harmless.
export PATH="$HOME/.local/bin:$HOME/.nix-profile/bin:/etc/profiles/per-user/$USER/bin:/run/current-system/sw/bin:/usr/local/bin:$PATH"

RUN_ID="${RUN_ID:-$(date -u +%Y-%m-%dT%H:%MZ)-local}"
mkdir -p "$ROOT/logs"

exec 9>"$ROOT/.run.lock"
flock -n 9 || { echo "[run_daily] another run holds the lock; exiting"; exit 0; }

LOG="$ROOT/logs/run-$(date -u +%Y%m%d-%H%M%SZ).log"
exec > >(tee -a "$LOG") 2>&1

PY=(uv run --project "$SCRIPT_ROOT" python)
setting() { "${PY[@]}" scripts/get_setting.py "$1" --default "${2:-}" --root "$ROOT"; }

echo "== cardtrack run $RUN_ID ($(date -u +%FT%TZ)) =="

echo "-- Phase A: monitor"
"${PY[@]}" scripts/monitor.py --run-id "$RUN_ID" --root "$ROOT"

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

if [ "$HOLD" -eq 0 ]; then
  # deliver issues/comments the sandboxed agent could only queue (gh is
  # unauthenticated inside; flush re-scans each record individually)
  "${PY[@]}" scripts/flush_outbox.py --root "$ROOT"
fi

if [ "$HOLD" -eq 0 ] && [ "$(setting publish.git_commit false)" = "true" ]; then
  # render the message BEFORE staging: --emit-commit-msg opens the DB, and
  # connect() rewrites views, which would leave docs.sqlite perpetually dirty
  MSG="$("${PY[@]}" scripts/build_site.py --root "$ROOT" --emit-commit-msg "$RUN_ID")"
  # scoped add: never sweep unrelated working-tree changes into an automated commit
  git -C "$ROOT" add data site logs 2>/dev/null || true
  if git -C "$ROOT" diff --cached --quiet; then
    echo "nothing to commit"
  else
    git -C "$ROOT" commit -m "$MSG"
    if [ "$(setting publish.git_push false)" = "true" ]; then
      git -C "$ROOT" push
    fi
  fi
fi

if [ "$HOLD" -eq 0 ] && [ "$(setting publish.wrangler_deploy false)" = "true" ]; then
  if [ -f "$ROOT/.env" ]; then set -a; . "$ROOT/.env"; set +a; fi
  npx -y wrangler pages deploy "$ROOT/site" \
    --project-name "$(setting publish.wrangler_project cardtrack)" \
    --commit-dirty=true
fi

if [ "$HOLD" -ne 0 ]; then
  echo "== run $RUN_ID HELD (nothing published; see logs/SECURITY_HOLD.md) =="
  exit 1
fi
echo "== run $RUN_ID complete =="
