#!/usr/bin/env bash
# Install the systemd user units for THIS checkout and enable the timers.
# The unit files in scripts/systemd/ name the maintainer's laptop path; this
# rewrites it to wherever the repo actually lives (laptop, VPS, fork).
#   scripts/install_units.sh            install + enable all three timers
#   scripts/install_units.sh --disable  stop and disable them (e.g. after cutover)
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
TIMERS=(cardtrack.timer cardtrack-canary.timer cardtrack-report.timer)
if [ "${1:-}" = "--disable" ]; then
  systemctl --user disable --now "${TIMERS[@]}" 2>/dev/null || true
  echo "timers disabled"; exit 0
fi
mkdir -p "$UNIT_DIR"
for f in "$REPO"/scripts/systemd/*.service "$REPO"/scripts/systemd/*.timer; do
  sed "s|%h/projects/ais/system_card_db|$REPO|g" "$f" > "$UNIT_DIR/$(basename "$f")"
done
systemctl --user daemon-reload
systemctl --user enable --now "${TIMERS[@]}"
loginctl enable-linger "$USER" 2>/dev/null || true   # keep timers firing when logged out
systemctl --user list-timers "${TIMERS[@]}" --no-pager
