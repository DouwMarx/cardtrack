# Shared shell helpers. Source, do not execute.
#
# envget KEY [ROOT]: print one value from $ROOT/.env without exporting the file.
# run_daily.sh deliberately never sources .env before Phase B: the agent sandbox
# inherits the environment, so a global `set -a; . .env` would hand the
# Cloudflare/OpenRouter tokens to the agent. Read single keys instead.
envget() {
  local key="$1" root="${2:-${ROOT:-.}}" line
  [ -f "$root/.env" ] || return 0
  line="$(grep -m1 -E "^[[:space:]]*(export[[:space:]]+)?${key}=" "$root/.env" || true)"
  line="${line#*=}"
  line="${line%\"}"; line="${line#\"}"
  line="${line%\'}"; line="${line#\'}"
  printf '%s' "$line"
}

# Directory holding the Claude CLI login for the /login (non-token) auth mode.
claude_config_dir() { printf '%s' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"; }

# Schedulers (cron, systemd timers) run with a minimal PATH. Prepend the places
# uv/claude/npx/git actually live on NixOS and Debian; nonexistent dirs are harmless.
standard_path() {
  export PATH="$HOME/.local/bin:$HOME/.nix-profile/bin:/etc/profiles/per-user/$USER/bin:/run/current-system/sw/bin:/usr/local/bin:$PATH"
}
