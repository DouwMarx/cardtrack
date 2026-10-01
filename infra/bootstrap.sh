#!/usr/bin/env bash
# Idempotent host setup for a cardtrack production box (Debian 13). Run as root.
# infra/provision.sh runs it over SSH on a fresh server; re-running it is safe and
# is how a host gets new packages or pinned tool versions.
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
# gh: issues and push auth; sqlite3: report
# snapshot; rclone: R2 archive backup; pandoc/latexmk/texlive: weekly report.
apt-get install -y -q --no-install-recommends \
  git curl ca-certificates rsync xz-utils unzip bubblewrap poppler-utils gh sqlite3 \
  pandoc latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
  texlive-bibtex-extra lmodern python3 jq unattended-upgrades systemd-container

# Node.js, pinned (versions.env), from the official release, checksum-verified.
# Installed under /opt and linked into /usr/local/bin, which precedes /usr/bin.
NODE_DIR="/opt/node-v$NODE_VERSION"
if [ ! -x "$NODE_DIR/bin/node" ]; then
  case "$(dpkg --print-architecture)" in amd64) NARCH=x64 ;; arm64) NARCH=arm64 ;;
    *) echo "unsupported architecture for Node.js"; exit 1 ;; esac
  NTAR="node-v$NODE_VERSION-linux-$NARCH.tar.xz"
  NTMP="$(mktemp -d)"
  curl -fsSLo "$NTMP/$NTAR" "https://nodejs.org/dist/v$NODE_VERSION/$NTAR"
  curl -fsSLo "$NTMP/SHASUMS256.txt" "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt"
  (cd "$NTMP" && grep " $NTAR\$" SHASUMS256.txt | sha256sum -c --quiet -)
  mkdir -p "$NODE_DIR" && tar -xJf "$NTMP/$NTAR" -C "$NODE_DIR" --strip-components=1
  rm -rf "$NTMP"
fi
for b in node npm npx; do ln -sf "$NODE_DIR/bin/$b" "/usr/local/bin/$b"; done

# rclone, pinned the same way (official release + its SHA256SUMS).
if [ "$(/usr/local/bin/rclone version 2>/dev/null | head -1)" != "rclone v$RCLONE_VERSION" ]; then
  case "$(dpkg --print-architecture)" in amd64) RARCH=amd64 ;; arm64) RARCH=arm64 ;;
    *) echo "unsupported architecture for rclone"; exit 1 ;; esac
  RZIP="rclone-v$RCLONE_VERSION-linux-$RARCH.zip"
  RTMP="$(mktemp -d)"
  curl -fsSLo "$RTMP/$RZIP" "https://downloads.rclone.org/v$RCLONE_VERSION/$RZIP"
  curl -fsSLo "$RTMP/SHA256SUMS" "https://downloads.rclone.org/v$RCLONE_VERSION/SHA256SUMS"
  (cd "$RTMP" && grep " $RZIP\$" SHA256SUMS | sha256sum -c --quiet -)
  unzip -q -j "$RTMP/$RZIP" '*/rclone' -d "$RTMP/bin"
  install -m 755 "$RTMP/bin/rclone" /usr/local/bin/rclone
  rm -rf "$RTMP"
fi

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
