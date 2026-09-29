#!/usr/bin/env bash
# Pre-run canary (systemd cardtrack-canary.timer, one hour before the daily run):
# one model call with the pipeline's own credentials plus the health conditions.
# Files or closes GitHub issues via scripts/health.py; exits 1 if Claude is unreachable.
set -euo pipefail
SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
# shellcheck source=lib.sh
. "$SCRIPT_ROOT/scripts/lib.sh"
standard_path
exec uv run --project "$SCRIPT_ROOT" python "$SCRIPT_ROOT/scripts/health.py" --canary --root "$ROOT"
