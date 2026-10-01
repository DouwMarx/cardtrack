#!/usr/bin/env bash
# Pre-flight check of a production host: every credential and tool the daily run,
# the weekly report and the backup need, exercised for real but without changing
# anything (no commit, push, deploy, upload or issue).
#
#   infra/check-host.sh <host>      (SSH as cardtrack@<host>, or an ssh alias)
#
# Run it after infra/push-secrets.sh and before infra/migrate-data.sh. Every
# line must say ok. It caught the wrangler/Node.js mismatch that a dev-role
# rehearsal cannot see (dev never deploys).
set -euo pipefail
HOST="${1:?usage: check-host.sh <host>}"
case "$HOST" in *@*) TARGET="$HOST" ;; *) TARGET="cardtrack@$HOST" ;; esac
ssh -o BatchMode=yes "$TARGET" bash -s <<'REMOTE'
set -uo pipefail
cd ~/cardtrack
. scripts/lib.sh
standard_path
export -f envget            # the checks below run in `bash -c` sub-shells
FAIL=0
check() {  # check <description> <command...>
  local d="$1"; shift
  local out
  # </dev/null: this script arrives on ssh's stdin, and `claude -p` reads stdin,
  # which once swallowed every check after it
  if out="$("$@" 2>&1 </dev/null)"; then echo "ok    $d"
  else echo "FAIL  $d: $(printf '%s' "$out" | tail -1 | cut -c1-160)"; FAIL=1; fi
}
setting() { .venv/bin/python scripts/get_setting.py "$1" --root .; }

check "role is prod"                       bash -c '[ "$(. scripts/lib.sh; envget CARDTRACK_ROLE .)" = prod ]'
check ".env readable by this user only"    bash -c '[ "$(stat -c %a .env)" = 600 ]'
check "pinned Claude Code"                 bash -c '[ "$(claude --version | cut -d" " -f1)" = "$(. infra/versions.env; echo $CLAUDE_CODE_VERSION)" ]'
check "pinned uv"                          bash -c '[ "$(uv --version | cut -d" " -f2)" = "$(. infra/versions.env; echo $UV_VERSION)" ]'
check "pinned Node.js"                     bash -c '[ "$(node --version)" = "v$(. infra/versions.env; echo $NODE_VERSION)" ]'
check "pinned rclone"                      bash -c '[ "$(rclone version | head -1)" = "rclone v$(. infra/versions.env; echo $RCLONE_VERSION)" ]'
check "bubblewrap sandbox starts"          bash scripts/agent_sandbox.sh true
check "git push authenticates (dry run)"   git push --dry-run origin HEAD:main
check "gh reads issues"                    gh issue list -R "$(setting github.repo)" --limit 1
check "Claude answers (pipeline account)"  bash -c '
  out=$(CLAUDE_CODE_OAUTH_TOKEN="$(envget CLAUDE_CODE_OAUTH_TOKEN .)" timeout 120 env -u ANTHROPIC_API_KEY \
        claude -p "Reply with the single word: ok" --model opus --max-turns 1 --output-format json)
  python3 -c "import json,sys; d=json.loads(sys.argv[1]); sys.exit(0 if not d.get(\"is_error\") else (print(d.get(\"result\")) or 1))" "$out"'
check "wrangler starts and sees the Pages project" bash -c '
  CLOUDFLARE_API_TOKEN="$(envget CLOUDFLARE_API_TOKEN .)" CLOUDFLARE_ACCOUNT_ID="$(envget CLOUDFLARE_ACCOUNT_ID .)" \
  timeout 240 npx -y "wrangler@$(.venv/bin/python scripts/get_setting.py publish.wrangler_version --root .)" \
    pages deployment list --project-name "$(.venv/bin/python scripts/get_setting.py publish.wrangler_project --root .)" >/dev/null'
check "OpenRouter key"                     bash -c '[ "$(curl -s -o /dev/null -w %{http_code} -H "Authorization: Bearer $(envget OPENROUTER_API_KEY .)" https://openrouter.ai/api/v1/key)" = 200 ]'
check "R2 private + public buckets readable" bash -c '
  export RCLONE_CONFIG=/dev/null RCLONE_S3_PROVIDER=Cloudflare
  RCLONE_S3_ACCESS_KEY_ID="$(envget R2_ACCESS_KEY_ID .)" RCLONE_S3_SECRET_ACCESS_KEY="$(envget R2_SECRET_ACCESS_KEY .)" \
  RCLONE_S3_ENDPOINT="$(envget R2_ENDPOINT .)"; export RCLONE_S3_ACCESS_KEY_ID RCLONE_S3_SECRET_ACCESS_KEY RCLONE_S3_ENDPOINT
  for b in "$(envget R2_BUCKET .)" "$(envget R2_PUBLIC_BUCKET .)"; do rclone lsf --max-depth 1 ":s3:$b" >/dev/null || exit 1; done'
check "report toolchain (latexmk, pandoc)" bash -c 'command -v latexmk && command -v pandoc'
exit "$FAIL"
REMOTE
