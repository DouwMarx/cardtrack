#!/usr/bin/env bash
# Weekly research report (systemd cardtrack-report.timer). Regenerates report/ with
# the sandboxed agent following .claude/skills/cardtrack-report/SKILL.md, converts
# it to the site's Analysis page (report/published/), and commits it. The next
# daily run deploys it. Holds the same lock as run_daily.sh, so they never overlap.
set -euo pipefail
SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
export CARDTRACK_ROOT="$ROOT"
cd "$SCRIPT_ROOT"
# shellcheck source=lib.sh
. "$SCRIPT_ROOT/scripts/lib.sh"
standard_path
ROLE="${CARDTRACK_ROLE:-$(envget CARDTRACK_ROLE "$ROOT")}"; ROLE="${ROLE:-dev}"
CFG_DIR="$(envget CLAUDE_CONFIG_DIR "$ROOT")"
[ -n "$CFG_DIR" ] && export CLAUDE_CONFIG_DIR="${CFG_DIR/#\~/$HOME}"
PY=(uv run --project "$SCRIPT_ROOT" python)
setting() { "${PY[@]}" scripts/get_setting.py "$1" --default "${2:-}" --root "$ROOT"; }
# Fail fast on unparseable config: every `setting` call would otherwise fall back
# to its default and silently disable features (report.enabled -> off, exit 0).
"${PY[@]}" scripts/get_setting.py site.title --root "$ROOT" >/dev/null \
  || { echo "ERROR: config/settings.yaml does not parse; refusing to run on defaults"; exit 2; }

[ "$(setting report.enabled false)" = "true" ] || { echo "report.enabled is off"; exit 0; }

exec 9>"$ROOT/.run.lock"
flock -w 10800 9 || { echo "[report] run lock busy for 3 h; giving up (systemd retries)"; exit 75; }

mkdir -p "$ROOT/logs" "$ROOT/state"
RUN_ID="report-$(date -u +%Y%m%dT%H%MZ)"
exec > >(tee -a "$ROOT/logs/$RUN_ID.log") 2>&1
echo "== cardtrack weekly report $RUN_ID (role=$ROLE) =="

"$ROOT/report/run.sh" snapshot "$ROOT"
"$ROOT/report/run.sh" pairs "$ROOT"
SKILL_SHA="$(git -C "$ROOT" rev-parse HEAD)"
START_MARK="$ROOT/state/.report_started"
touch "$START_MARK"
rm -f "$ROOT/report/out/RUN_SUMMARY.md"

AGENT_CMD="$(setting report.cmd)"
TIMEOUT="$(setting report.timeout_seconds 7200)"
RC=0
CARDTRACK_SANDBOX_RW="report" CARDTRACK_SANDBOX_RO="report/published" timeout --kill-after=60 "$TIMEOUT" \
  bash scripts/agent_sandbox.sh bash -c "$AGENT_CMD" || RC=$?
if [ -d "$ROOT/.agent-home/.claude/projects" ]; then
  mkdir -p "$ROOT/logs/agent-transcripts"
  cp -r "$ROOT/.agent-home/.claude/projects" "$ROOT/logs/agent-transcripts/$RUN_ID" 2>/dev/null || true
fi
if [ "$RC" -ne 0 ] || ! [ "$ROOT/report/tex/report.pdf" -nt "$START_MARK" ] \
    || ! [ -s "$ROOT/report/out/RUN_SUMMARY.md" ]; then
  echo "[report] FAILED: agent exit $RC, or no rebuilt PDF / RUN_SUMMARY.md; nothing published"
  # never half-publish; on a dev checkout keep the edits for inspection
  if [ "$ROLE" = "prod" ]; then
    git -C "$ROOT" checkout -- report 2>/dev/null || true
    git -C "$ROOT" clean -fdq report/published 2>/dev/null || true
  fi
  exit 3
fi

# The model that actually wrote this edition, from the session transcript (the
# --model alias resolves server-side, so the alias alone would be the wrong claim).
MODEL="$("${PY[@]}" - "$ROOT/.agent-home/.claude/projects" <<'PYEOF'
import collections, glob, json, sys
c = collections.Counter()
for f in glob.glob(sys.argv[1] + "/*/*.jsonl"):          # main session, not sub-agents
    for line in open(f, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        m = d.get("message") or {}
        if d.get("type") == "assistant" and isinstance(m, dict) and m.get("model", "").startswith("claude"):
            c[m["model"]] += 1
print(c.most_common(1)[0][0] if c else "")
PYEOF
)"
[ -n "$MODEL" ] || { echo "[report] could not determine the model; not publishing without provenance"; exit 3; }
GH_REPO="$(setting github.repo)"
# Convert into a staging dir; report/published changes only after every check.
STAGE="$(mktemp -d)"
"${PY[@]}" scripts/report_html.py --report-dir "$ROOT/report" --out "$STAGE" \
  --model "$MODEL" \
  --skill-url "https://github.com/$GH_REPO/blob/$SKILL_SHA/.claude/skills/cardtrack-report/SKILL.md"

# Everything under report/ is agent-written and about to be public. Literal scan
# (zero false positives): quoting third-party documents must not trip regexes.
"${PY[@]}" scripts/secret_scan.py --root "$ROOT" --literal-only "$ROOT/report" "$STAGE" \
  || { echo "[report] SECURITY HOLD: local secret found under report/; nothing published"
       rm -rf "$STAGE"; exit 10; }

rm -rf "$ROOT/report/published"
mkdir -p "$ROOT/report"
mv "$STAGE" "$ROOT/report/published"
chmod 755 "$ROOT/report/published"
date -u +%FT%TZ > "$ROOT/state/.report_last_ok"
if [ "$ROLE" = "prod" ] && [ "$(setting publish.git_commit false)" = "true" ]; then
  git -C "$ROOT" add report
  if ! git -C "$ROOT" diff --cached --quiet; then
    git -C "$ROOT" commit -q -m "[report] weekly analysis $(date -u +%F), written by $MODEL"
    if [ "$(setting publish.git_push false)" = "true" ]; then
      git -C "$ROOT" push -q \
        || { git -C "$ROOT" pull --rebase --quiet && git -C "$ROOT" push -q; } \
        || echo "[report] WARNING: push failed; the next daily run pushes it"
    fi
  fi
fi
echo "== report $RUN_ID complete ($MODEL); the next daily run deploys it =="
