#!/usr/bin/env bash
# Idempotent host setup for a cardtrack production box (Debian 13). Run as root.
# cloud-init runs it on first boot (infra/cloud-init.yaml.tftpl); re-running it is
# safe and is how a host gets new packages or pinned tool versions.
#
#   bootstrap.sh <repo-url> [user]
#
# Leaves the box ready except for secrets: infra/push-secrets.sh then writes .env,
# authenticates gh and enables the timers.
set -euo pipefail
REPO_URL="${1:?usage: bootstrap.sh <repo-url> [user]}"
APP_USER="${2:-cardtrack}"
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=versions.env
. "$HERE/versions.env"

export DEBIAN_FRONTEND=noninteractive
apt-get update -q
# git/curl/ca: fetch + clone; bubblewrap: agent sandbox; poppler-utils: PDF text;
# nodejs/npm: npx wrangler + pagefind; gh: issues and push auth; sqlite3: report
# snapshot; rclone: R2 archive backup; pandoc/latexmk/texlive: weekly report.
apt-get install -y -q --no-install-recommends \
  git curl ca-certificates rsync bubblewrap poppler-utils nodejs npm gh sqlite3 rclone \
  pandoc latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
  texlive-bibtex-extra lmodern python3 jq unattended-upgrades systemd-container

# SSH: keys only. Some images (netcup) ship with root password login enabled.
if [ -d /etc/ssh/sshd_config.d ]; then
  cat > /etc/ssh/sshd_config.d/10-cardtrack.conf <<'SSHD'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin prohibit-password
SSHD
  systemctl reload ssh 2>/dev/null || true
fi

# Security updates install themselves; the pipeline's own tools stay pinned.
dpkg-reconfigure -f noninteractive unattended-upgrades >/dev/null

id "$APP_USER" >/dev/null 2>&1 || useradd --create-home --shell /bin/bash "$APP_USER"
# user systemd instance keeps running (and timers keep firing) with nobody logged in
# start the user's systemd manager now and keep it running without a login;
# the file fallback covers containers without logind (infra/test-bootstrap.sh)
loginctl enable-linger "$APP_USER" 2>/dev/null \
  || { mkdir -p /var/lib/systemd/linger && touch "/var/lib/systemd/linger/$APP_USER"; }

run_as() { runuser -u "$APP_USER" -- bash -lc "$1"; }
run_as "export DISABLE_AUTOUPDATER=1
  grep -q DISABLE_AUTOUPDATER ~/.profile || echo 'export DISABLE_AUTOUPDATER=1' >> ~/.profile
  [ \"\$(~/.local/bin/uv --version 2>/dev/null | cut -d' ' -f2)\" = '$UV_VERSION' ] \
    || curl -LsSf https://astral.sh/uv/$UV_VERSION/install.sh | sh
  [ \"\$(~/.local/bin/claude --version 2>/dev/null | cut -d' ' -f1)\" = '$CLAUDE_CODE_VERSION' ] \
    || curl -fsSL https://claude.ai/install.sh | bash -s $CLAUDE_CODE_VERSION
  [ -d ~/cardtrack/.git ] || git clone -q '$REPO_URL' ~/cardtrack
  cd ~/cardtrack
  git config --global user.name 'cardtrack bot'
  git config --global user.email '$APP_USER@users.noreply.github.com'
  ~/.local/bin/uv sync --frozen -q"
echo "bootstrap done: repo at ~$APP_USER/cardtrack; next: infra/push-secrets.sh"
