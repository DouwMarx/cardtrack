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

# Ephemeral agent home: credentials in, nothing out. Seed ONLY the credential
# file — the host settings.json (permission modes, hooks) must not shape the
# sandboxed agent's permission posture; the CLI runs on its defaults + the
# explicit --allowedTools list in settings.yaml.
AGENT_HOME="$ROOT/.agent-home"
rm -rf "$AGENT_HOME"
mkdir -p "$AGENT_HOME/.claude"
if [ -f "$HOME/.claude/.credentials.json" ]; then
  # Blast-radius reduction: the -p session needs only the short-lived access
  # token. Strip the long-lived refresh token and any MCP OAuth tokens (they
  # grant personal-data access far beyond this repo) so a prompt-injected agent
  # that reads its own credential file has the least to steal. If the access
  # token has expired, Phase B fails cleanly and any interactive `claude` use
  # refreshes it for the next run.
  PYBIN="$ROOT/.venv/bin/python"
  [ -x "$PYBIN" ] || PYBIN="$SCRIPT_ROOT/.venv/bin/python"
  [ -x "$PYBIN" ] || PYBIN="$(command -v python3)"
  "$PYBIN" - "$HOME/.claude/.credentials.json" \
      "$AGENT_HOME/.claude/.credentials.json" <<'PYEOF'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    creds = json.load(open(src))
    oauth = creds.get("claudeAiOauth")
    if not isinstance(oauth, dict):
        raise ValueError("no claudeAiOauth block to seed")
    # Whitelist, not blacklist: seed ONLY the oauth block, minus refresh material,
    # so new top-level entries (MCP tokens, extra accounts) can never leak in.
    # "refresh" substring (not refreshToken) so a snake_case schema drift still trips.
    slim = {"claudeAiOauth": {k: v for k, v in oauth.items()
                              if "refresh" not in k.lower()}}
    out = json.dumps(slim)
    # Tripwire for FUTURE edits, not a live check: today the filter above makes
    # this unreachable, but it catches anyone later loosening the filter without
    # matching intent (e.g. narrowing it to startswith("refreshToken")).
    if any("refresh" in k.lower() or "mcp" in k.lower()
           for k in slim["claudeAiOauth"]):
        raise ValueError("sensitive keys survived slimming")
    import os
    fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(out)
except Exception as e:
    print(f"[agent_sandbox] ERROR: credential slimming failed ({e}); refusing to seed",
          file=sys.stderr)
    sys.exit(1)
PYEOF
  chmod 600 "$AGENT_HOME/.claude/.credentials.json"
fi

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
  --unsetenv GH_TOKEN \
  --unsetenv GITHUB_TOKEN \
  --unshare-pid \
  --die-with-parent \
  "$@"
