#!/usr/bin/env bash
# Provision a fresh Debian 13 server you can SSH into as root with your key.
# Runs infra/bootstrap.sh there (packages, app user, pinned uv + Claude Code, repo
# clone, key-only SSH) and gives the app user the same authorized keys as root.
#
#   infra/provision.sh <host> [--repo-url URL]
#
# Proven end to end by infra/rehearse.sh. Next: infra/push-secrets.sh <host>.
set -euo pipefail
HOST="${1:?usage: provision.sh <host> [--repo-url URL]}"; shift
REPO_URL="https://github.com/DouwMarx/cardtrack.git"
while [ $# -gt 0 ]; do
  case "$1" in
    --repo-url) REPO_URL="$2"; shift 2 ;;
    *) echo "unknown option $1"; exit 2 ;;
  esac
done
SSH=(ssh -o StrictHostKeyChecking=accept-new "root@$HOST")

"${SSH[@]}" "grep -q 'VERSION_ID=\"13\"' /etc/os-release" \
  || { echo "host is not Debian 13; reinstall it with Debian 13 first"; exit 1; }

"${SSH[@]}" bash -s -- "$REPO_URL" <<'REMOTE'
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -q && apt-get install -y -q git ca-certificates curl >/dev/null
rm -rf /opt/cardtrack-bootstrap
git clone -q "$1" /opt/cardtrack-bootstrap
bash /opt/cardtrack-bootstrap/infra/bootstrap.sh "$1" cardtrack
# same keys as root, so `ssh cardtrack@host` works for push-secrets/migrate-data
install -d -m 700 -o cardtrack -g cardtrack /home/cardtrack/.ssh
install -m 600 -o cardtrack -g cardtrack /root/.ssh/authorized_keys /home/cardtrack/.ssh/authorized_keys
REMOTE
echo "provisioned; next: infra/push-secrets.sh $HOST"
