#!/usr/bin/env bash
# OS-level sandbox for the curation agent. Tool scoping (--allowedTools) is ergonomics;
# this is the boundary. Layout inside the sandbox:
#   - / and the repo: read-only
#   - $HOME: tmpfs (hides ~/.ssh, ~/.config/secrets.env, ~/.config/gh, everything)
#   - $ROOT/.env: masked with /dev/null (Cloudflare token invisible)
#   - writable: $ROOT/data and $ROOT/logs (which holds PROPOSALS.md), and an EPHEMERAL
#     $HOME/.claude seeded with only the CLI credentials (discarded after the run,
#     so poisoned settings/hooks never reach the host; gh is unauthenticated inside,
#     so issues fall back to the outbox, which run_daily.sh flushes OUTSIDE the box)
#
# Known residual gap (documented in README): propose_doc.py runs inside the sandbox,
# so data/ must be writable and a fully compromised agent could bypass the validator
# and write data/ directly. Provenance + the changelog-to-commit diff make that
# visible; git revert undoes it.
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"

if ! command -v bwrap >/dev/null 2>&1; then
  # Fail closed: an unsandboxed autonomous agent is a silent security downgrade.
  # (Install bubblewrap; or for a one-off supervised run, set CARDTRACK_NO_SANDBOX=1.)
  if [ "${CARDTRACK_NO_SANDBOX:-}" = "1" ]; then
    echo "[agent_sandbox] WARNING: CARDTRACK_NO_SANDBOX=1 — running WITHOUT the OS sandbox" >&2
    exec "$@"
  fi
  echo "[agent_sandbox] ERROR: bwrap not found; refusing to run the agent unsandboxed" >&2
  exit 90
fi

mkdir -p "$ROOT/data" "$ROOT/logs"
touch "$ROOT/logs/PROPOSALS.md" "$ROOT/logs/friction.jsonl"

# Ephemeral agent home: credentials in, nothing out.
AGENT_HOME="$ROOT/.agent-home"
rm -rf "$AGENT_HOME"
mkdir -p "$AGENT_HOME/.claude"
for f in .credentials.json settings.json; do
  [ -f "$HOME/.claude/$f" ] && cp "$HOME/.claude/$f" "$AGENT_HOME/.claude/$f"
done

ENV_MASK=()
[ -f "$ROOT/.env" ] && ENV_MASK=(--ro-bind /dev/null "$ROOT/.env")

# the venv's python symlinks into uv's toolchain dir; expose it read-only
# (interpreters only — no secrets live there)
UV_PY=()
[ -d "$HOME/.local/share/uv" ] && UV_PY=(--ro-bind "$HOME/.local/share/uv" "$HOME/.local/share/uv")

exec bwrap \
  --ro-bind / / \
  --dev /dev \
  --proc /proc \
  --tmpfs /tmp \
  --tmpfs "$HOME" \
  --ro-bind "$SCRIPT_ROOT" "$SCRIPT_ROOT" \
  --ro-bind "$ROOT" "$ROOT" \
  "${ENV_MASK[@]}" \
  "${UV_PY[@]}" \
  --bind "$ROOT/data" "$ROOT/data" \
  --bind "$ROOT/logs" "$ROOT/logs" \
  --bind "$AGENT_HOME/.claude" "$HOME/.claude" \
  --setenv HOME "$HOME" \
  --setenv CARDTRACK_SANDBOX 1 \
  --unshare-pid \
  --die-with-parent \
  "$@"
