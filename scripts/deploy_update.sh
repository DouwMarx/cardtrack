#!/usr/bin/env bash
# Pull-based deploy for a production checkout. Runs as the daily unit's
# ExecStartPre, i.e. before run_daily.sh is read, so the update can never rewrite
# a script that bash is executing. This file is itself rewritten by the rebase
# below, so everything lives in main(), which bash parses fully before running.
#
#   1. fetch origin/main; stop if it is the sha rejected last time
#   2. rebase this checkout (and any unpushed data commit) onto it
#   3. if code changed: uv sync --frozen, run the test suite
#   4. tests fail -> reset to the previous commit, record the rejected sha
#      (scripts/health.py raises a "deploy-rejected" issue while it exists)
#
# Only acts when CARDTRACK_ROLE=prod (default) and settings deploy.auto_pull: true.
# Skips, never fails the run, on: dirty tracked files, network errors, rebase conflicts.
set -euo pipefail

main() {
  local script_root root
  script_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  root="${1:-${CARDTRACK_ROOT:-$script_root}}"
  # shellcheck source=lib.sh
  . "$script_root/scripts/lib.sh"
  standard_path
  cd "$root"
  local role; role="${CARDTRACK_ROLE:-$(envget CARDTRACK_ROLE "$root")}"
  [ "$role" = "prod" ] || { echo "[deploy] role=${role:-dev}: no auto-pull"; return 0; }
  [ "$(uv run --project "$root" python scripts/get_setting.py deploy.auto_pull --default false --root "$root")" = "true" ] \
    || { echo "[deploy] deploy.auto_pull is off"; return 0; }

  exec 8>"$root/.run.lock"
  flock -w 900 8 || { echo "[deploy] run lock busy; skipping update"; return 0; }

  git fetch --quiet origin main || { echo "[deploy] fetch failed; keeping current code"; return 0; }
  local target old rejected="$root/state/.deploy_rejected"
  target="$(git rev-parse origin/main)"
  old="$(git rev-parse HEAD)"
  if git merge-base --is-ancestor origin/main HEAD; then
    return 0                                  # nothing new upstream
  fi
  if [ -f "$rejected" ] && [ "$(cut -d' ' -f1 "$rejected")" = "$target" ]; then
    echo "[deploy] origin/main $target failed tests before; waiting for a new commit"
    return 0
  fi
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[deploy] tracked files are modified; not updating a dirty checkout"
    return 0
  fi
  if ! git rebase --quiet origin/main; then
    git rebase --abort 2>/dev/null || true
    echo "[deploy] rebase onto $target conflicted; keeping current code"
    return 0
  fi
  if git diff --quiet "$old" HEAD -- . ':(exclude)data' ':(exclude)site' ':(exclude)logs'; then
    echo "[deploy] upstream changed data only"
    rm -f "$rejected"
    return 0
  fi
  echo "[deploy] testing $target"
  if ! uv sync --frozen --quiet; then
    echo "[deploy] uv sync failed (network?); staying on $(git rev-parse --short "$old"), retry next run"
    git reset --quiet --hard "$old"; uv sync --frozen --quiet || true
    return 0
  fi
  local test_cmd out passed=1
  test_cmd="$(uv run --project "$root" python scripts/get_setting.py deploy.test_cmd --default "uv run pytest -q -x" --root "$root")"
  out="$(bash -c "$test_cmd" 2>&1)" && passed=0
  printf '%s\n' "$out" | tail -20
  if [ "$passed" -eq 0 ]; then
    echo "[deploy] now running $(git rev-parse --short HEAD)"
    rm -f "$rejected"
  else
    echo "[deploy] tests FAILED on $target; staying on $(git rev-parse --short "$old")"
    git reset --quiet --hard "$old"
    uv sync --frozen --quiet || true
    mkdir -p "$root/state"; echo "$target $(date -u +%FT%TZ)" > "$rejected"
  fi
  return 0
}

main "$@"
exit $?
