#!/usr/bin/env bash
# OS-level sandbox for the curation agent. Tool scoping (--allowedTools) is ergonomics;
# this is the boundary. Layout inside the sandbox:
#   - / and the repo: read-only
#   - $HOME: tmpfs (hides ~/.ssh, ~/.config/secrets.env, ~/.config/gh, everything)
#   - $ROOT/.env: masked with /dev/null (Cloudflare token invisible)
#   - writable: $CARDTRACK_SANDBOX_RW (default "data logs"; logs holds PROPOSALS.md),
#     and an EPHEMERAL $HOME/.claude (discarded after the run, so poisoned
#     settings/hooks never reach the host; gh is unauthenticated inside, so issues
#     fall back to the outbox, which run_daily.sh flushes OUTSIDE the box)
#   - environment: every key named in .env is unset, so no deploy token reaches the
#     agent even if a caller exported .env; only the Claude credential passes in
#
# Claude credentials, two modes:
#   - CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`, set in .env or the env):
#     passed in as an env var. One-year, model-requests-only token; no refresh
#     dance, no credential file. Recommended for unattended hosts.
#   - otherwise the /login credential file under ${CLAUDE_CONFIG_DIR:-~/.claude},
#     seeded with the refresh token stripped (see below).
#
# Known residual gap (documented in README): propose_doc.py runs inside the sandbox,
# so data/ must be writable and a fully compromised agent could bypass the validator
# and write data/ directly. Provenance + the changelog-to-commit diff make that
# visible; git revert undoes it.
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT="${CARDTRACK_ROOT:-$SCRIPT_ROOT}"
# shellcheck source=lib.sh
. "$SCRIPT_ROOT/scripts/lib.sh"

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

read -r -a RW_DIRS <<< "${CARDTRACK_SANDBOX_RW:-data logs}"
RW_BINDS=()
for d in "${RW_DIRS[@]}"; do
  case "$d" in /*|*..*|.|./*|"") echo "[agent_sandbox] ERROR: RW path must be a repo subdirectory: $d" >&2; exit 91 ;; esac
  mkdir -p "$ROOT/$d"
  RW_BINDS+=(--bind "$ROOT/$d" "$ROOT/$d")
done
if [ -d "$ROOT/logs" ] && [[ " ${RW_DIRS[*]} " == *" logs "* ]]; then
  touch "$ROOT/logs/PROPOSALS.md" "$ROOT/logs/friction.jsonl"
fi

# Read-only islands inside writable dirs (the report agent must not write the
# published edition itself; scripts/run_report.sh publishes it after checks).
read -r -a RO_DIRS <<< "${CARDTRACK_SANDBOX_RO:-}"
RO_BINDS=()
for d in "${RO_DIRS[@]}"; do
  case "$d" in /*|*..*) echo "[agent_sandbox] ERROR: RO path must be repo-relative: $d" >&2; exit 91 ;; esac
  mkdir -p "$ROOT/$d"
  RO_BINDS+=(--ro-bind "$ROOT/$d" "$ROOT/$d")
done

CLAUDE_TOKEN="${CLAUDE_CODE_OAUTH_TOKEN:-$(envget CLAUDE_CODE_OAUTH_TOKEN "$ROOT")}"
CRED_FILE="$(claude_config_dir)/.credentials.json"

# Ephemeral agent home: credentials in, nothing out. Seed ONLY the credential
# file — the host settings.json (permission modes, hooks) must not shape the
# sandboxed agent's permission posture; the CLI runs on its defaults + the
# explicit --allowedTools list in settings.yaml.
AGENT_HOME="$ROOT/.agent-home"
rm -rf "$AGENT_HOME"
mkdir -p "$AGENT_HOME/.claude"
if [ -z "$CLAUDE_TOKEN" ] && [ -f "$CRED_FILE" ]; then
  # Blast-radius reduction: the -p session needs only the short-lived access
  # token. Strip the long-lived refresh token and any MCP OAuth tokens (they
  # grant personal-data access far beyond this repo) so a prompt-injected agent
  # that reads its own credential file has the least to steal. If the access
  # token has expired, Phase B fails cleanly and any interactive `claude` use
  # refreshes it for the next run.
  PYBIN="$ROOT/.venv/bin/python"
  [ -x "$PYBIN" ] || PYBIN="$SCRIPT_ROOT/.venv/bin/python"
  [ -x "$PYBIN" ] || PYBIN="$(command -v python3)"
  "$PYBIN" - "$CRED_FILE" \
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
# Session-bus and agent sockets would let the agent ask the host's systemd user
# manager to run commands outside the sandbox (verified 2026-09-29), so /run is
# replaced below and these pointers go too.
ENV_UNSET=(--unsetenv CLAUDE_CONFIG_DIR --unsetenv ANTHROPIC_API_KEY
           --unsetenv DBUS_SESSION_BUS_ADDRESS --unsetenv XDG_RUNTIME_DIR
           --unsetenv SSH_AUTH_SOCK --unsetenv GPG_AGENT_INFO)
for envfile in "$ROOT/.env" "$SCRIPT_ROOT/.env"; do
  [ -f "$envfile" ] || continue
  ENV_MASK+=(--ro-bind /dev/null "$envfile")
  while IFS= read -r key; do
    [ "$key" = CLAUDE_CODE_OAUTH_TOKEN ] && continue    # passed in on purpose, below
    ENV_UNSET+=(--unsetenv "$key")
  done < <(grep -E '^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*=' "$envfile" \
             | sed -E 's/^[[:space:]]*(export[[:space:]]+)?//; s/=.*//')
done
# The token travels in the environment, never in bwrap's argv (/proc/*/cmdline is
# world-readable for the whole run).
if [ -n "$CLAUDE_TOKEN" ]; then export CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_TOKEN"
else ENV_UNSET+=(--unsetenv CLAUDE_CODE_OAUTH_TOKEN); fi

# /run holds the user bus, the systemd manager socket, ssh-agent and docker.sock.
# Replace it with an empty tmpfs and put back only what name resolution and NixOS
# binaries need, read-only.
RUN_KEEP=()
for keep in /run/current-system /run/systemd/resolve /run/nscd; do
  [ -e "$keep" ] && RUN_KEEP+=(--ro-bind "$keep" "$keep")
done
# A /login credential dir outside $HOME would stay readable through --ro-bind /.
HIDE_CFG=()
CFG_REAL="$(claude_config_dir)"
case "$CFG_REAL" in "$HOME"|"$HOME"/*) ;; *) [ -d "$CFG_REAL" ] && HIDE_CFG=(--tmpfs "$CFG_REAL") ;; esac

# the venv's python symlinks into uv's toolchain dir; expose it read-only
# (interpreters only — no secrets live there)
UV_PY=()
[ -d "$HOME/.local/share/uv" ] && UV_PY=(--ro-bind "$HOME/.local/share/uv" "$HOME/.local/share/uv")

exec bwrap \
  --ro-bind / / \
  --dev /dev \
  --proc /proc \
  --tmpfs /tmp \
  --tmpfs /run \
  "${RUN_KEEP[@]}" \
  --tmpfs "$HOME" \
  "${HIDE_CFG[@]}" \
  --ro-bind "$SCRIPT_ROOT" "$SCRIPT_ROOT" \
  --ro-bind "$ROOT" "$ROOT" \
  "${UV_PY[@]}" \
  "${RW_BINDS[@]}" \
  "${RO_BINDS[@]}" \
  "${ENV_MASK[@]}" \
  --bind "$AGENT_HOME/.claude" "$HOME/.claude" \
  --setenv HOME "$HOME" \
  --setenv CARDTRACK_SANDBOX 1 \
  --setenv DISABLE_AUTOUPDATER 1 \
  "${ENV_UNSET[@]}" \
  --new-session \
  --unsetenv GH_TOKEN \
  --unsetenv GITHUB_TOKEN \
  --unshare-pid \
  --die-with-parent \
  "$@"
