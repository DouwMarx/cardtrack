#!/usr/bin/env bash
# Move production from this machine to a new host (run on the OLD production box).
#   infra/migrate-data.sh <host>
# 1. stop local timers, so two machines never run (and push) the same day
# 2. push any local commits, so the host starts from the latest data
# 3. copy the gitignored raw archive and the health markers
# 4. enable the timers on the host, mark this checkout as a development checkout
# Prerequisite: infra/push-secrets.sh <host> --no-enable
set -euo pipefail
HOST="${1:?usage: migrate-data.sh <host>}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
scripts/install_units.sh --disable
exec 9>"$REPO/.run.lock"; flock -w 10800 9    # let a running job finish first
git push
rsync -a --info=stats1 data/raw/ "cardtrack@$HOST:cardtrack/data/raw/"
[ -d state ] && rsync -a state/ "cardtrack@$HOST:cardtrack/state/"
ssh "cardtrack@$HOST" 'export XDG_RUNTIME_DIR=/run/user/$(id -u); cd ~/cardtrack && git pull -q --ff-only && du -sh data/raw && scripts/install_units.sh'
if grep -q '^CARDTRACK_ROLE=' .env 2>/dev/null; then
  sed -i 's/^CARDTRACK_ROLE=.*/CARDTRACK_ROLE=dev/' .env
else
  echo 'CARDTRACK_ROLE=dev' >> .env
fi
echo "cutover done: $HOST is production; this checkout is now CARDTRACK_ROLE=dev"
