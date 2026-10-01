#!/usr/bin/env bash
# Take a read-only snapshot of the repo state needed by the analysis.
# Usage: report/snapshot.sh [/path/to/repo]   (default: this repo)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${1:-$(cd "$HERE/.." && pwd)}"
mkdir -p "$HERE/data/runlogs"
# sqlite3's online backup gives a consistent copy even if a run is writing
if command -v sqlite3 >/dev/null; then
  sqlite3 "$SRC/data/docs.sqlite" ".backup '$HERE/data/docs.sqlite.snapshot'"
else
  cp "$SRC/data/docs.sqlite" "$HERE/data/docs.sqlite.snapshot"
fi
cp "$SRC"/logs/run-*.log "$HERE/data/runlogs/" 2>/dev/null || true
cp "$SRC/logs/friction.jsonl" "$SRC/logs/PROPOSALS.md" "$SRC/logs/candidates.json" "$HERE/data/" 2>/dev/null || true
# Host journal (only meaningful on the machine that runs the timer; optional). A host
# that never suspends, or has no journal, yields no lines: grep then exits 1, which
# under pipefail aborted the whole snapshot (found on a Debian server, 2026-10-01).
{
  { journalctl --since 2026-08-09 -o short-iso --no-pager 2>/dev/null \
      | grep -i "System returned from sleep\|Performing sleep operation" \
      | awk '{print $1 " " (($0 ~ /returned/) ? "resume" : "suspend")}'; } || true
  { journalctl --user -u cardtrack.service --since 2026-08-09 -o short-iso --no-pager 2>/dev/null \
      | grep "Starting cardtrack" | awk '{print $1 " service_start"}'; } || true
} | sort | python3 -c '
import sys, json
ev=[{"ts": l.split()[0], "kind": l.split()[1]} for l in sys.stdin if len(l.split())==2]
json.dump(ev, open(sys.argv[1], "w"), indent=1); print(len(ev), "journal events")
' "$HERE/data/journal_events.json"
echo "snapshot taken from $SRC at $(date -u +%FT%TZ)" | tee "$HERE/data/SNAPSHOT.txt"
