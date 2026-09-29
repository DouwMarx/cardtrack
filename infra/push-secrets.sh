#!/usr/bin/env bash
# Deliver secrets to a bootstrapped host and switch it on.
#   infra/push-secrets.sh <host>              new deployment: also enables the timers
#   infra/push-secrets.sh <host> --no-enable  moving production: migrate-data.sh enables
#                                             them after the old host is stopped
#
# Reads infra/prod.env (gitignored; template: infra/prod.env.example), writes it as
# the host's .env (mode 600), logs gh in with GH_TOKEN (git push + issues), then
# installs and enables the timers. Re-run it to rotate any secret.
set -euo pipefail
HOST="${1:?usage: push-secrets.sh <host> [--no-enable]}"
ENABLE=1; [ "${2:-}" = "--no-enable" ] && ENABLE=0
HERE="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${CARDTRACK_PROD_ENV:-$HERE/prod.env}"   # override: rehearsals with a dev-role copy
[ -f "$ENV_FILE" ] || { echo "missing $ENV_FILE (copy prod.env.example)"; exit 1; }
for k in CARDTRACK_ROLE CLAUDE_CODE_OAUTH_TOKEN CLAUDE_TOKEN_CREATED GH_TOKEN \
         CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID; do
  grep -qE "^$k=.+" "$ENV_FILE" || { echo "prod.env: $k is empty"; exit 1; }
done
SSH=(ssh -o StrictHostKeyChecking=accept-new "cardtrack@$HOST")
"${SSH[@]}" 'umask 077; cat > ~/cardtrack/.env' < "$ENV_FILE"
"${SSH[@]}" "ENABLE=$ENABLE bash -ls" <<'REMOTE'
set -euo pipefail
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
cd ~/cardtrack
. scripts/lib.sh
envget GH_TOKEN . | gh auth login --with-token
gh auth setup-git
gh auth status 2>&1 | head -3
scripts/canary.sh || true
if [ "$ENABLE" = 1 ]; then scripts/install_units.sh; else echo "timers NOT enabled (--no-enable)"; fi
REMOTE
echo "secrets delivered; the canary result is above."
