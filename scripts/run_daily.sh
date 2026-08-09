#!/usr/bin/env bash
# Daily run orchestrator (spec §8): Phase A monitor → Phase B agent → Phase C build/publish.
# Idempotent and lock-guarded; a missed day self-heals on the next run.
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
export CARDTRACK_ROOT="$ROOT"
cd "$SCRIPT_ROOT"

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
    bash scripts/agent_sandbox.sh bash -c "$AGENT_CMD" \
      || echo "[run_daily] agent exited nonzero (continuing to Phase C)"
    unset CARDTRACK_ACTOR
    # deliver issues the sandboxed agent could only queue (gh is unauthenticated inside)
    "${PY[@]}" scripts/flush_outbox.py --root "$ROOT"
  else
    echo "[run_daily] agent.enabled=true but agent.cmd is empty; skipping"
  fi
else
  echo "agent disabled (agent.enabled=false)"
fi

echo "-- Phase C: build & publish"
"${PY[@]}" scripts/build_site.py --root "$ROOT"

if [ "$(setting publish.git_commit false)" = "true" ]; then
  # scoped add: never sweep unrelated working-tree changes into an automated commit
  git -C "$ROOT" add data site PROPOSALS.md logs 2>/dev/null || true
  if git -C "$ROOT" diff --cached --quiet; then
    echo "nothing to commit"
  else
    MSG="$("${PY[@]}" scripts/build_site.py --root "$ROOT" --emit-commit-msg "$RUN_ID")"
    git -C "$ROOT" commit -m "$MSG"
    if [ "$(setting publish.git_push false)" = "true" ]; then
      git -C "$ROOT" push
    fi
  fi
fi

if [ "$(setting publish.wrangler_deploy false)" = "true" ]; then
  if [ -f "$ROOT/.env" ]; then set -a; . "$ROOT/.env"; set +a; fi
  npx -y wrangler pages deploy "$ROOT/site" \
    --project-name "$(setting publish.wrangler_project cardtrack)" \
    --commit-dirty=true
fi

echo "== run $RUN_ID complete =="
