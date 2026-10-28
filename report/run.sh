#!/usr/bin/env bash
# Rebuild the research report's inputs and check the edition from a fresh snapshot.
#
#   report/run.sh snapshot   read-only snapshot of the repo (DB, run logs, journal) into report/data
#   report/run.sh pairs      version-pair diffs + batches of still-unclassified pairs
#   report/run.sh analyze    results.json, tables/*.md, figures/*.png, comprehensive_report.md
#   report/run.sh html       convert report/report.md -> out/html/ with the published checks
#                            (word cap, minimum figures, tables, figure files), for a preview
#   report/run.sh all        snapshot + pairs + analyze (classification is a separate,
#                            agent-driven step between "pairs" and "analyze": CLASSIFY_INSTRUCTIONS.md)
#
# Procedure and conventions: .claude/skills/cardtrack-report/SKILL.md
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
cd "$HERE"
# The repo venv (report deps are a default uv group). Inside the agent sandbox the
# venv is read-only and $HOME is tmpfs, so call its python directly, never `uv run`.
if [ -x "$REPO/.venv/bin/python" ]; then PY=("$REPO/.venv/bin/python"); else PY=(uv run --project "$REPO" python); fi
setting() { "${PY[@]}" "$REPO/scripts/get_setting.py" "$1" --default "${2:-}" --root "$REPO"; }
step="${1:-all}"
case "$step" in
  snapshot) ./snapshot.sh "${2:-$REPO}" ;;
  pairs)    "${PY[@]}" build_pairs.py --repo "${2:-$REPO}" ;;
  analyze)  "${PY[@]}" analyze.py >/dev/null && echo "analysis written to out/" ;;
  html)
    "${PY[@]}" "$REPO/scripts/report_html.py" --report-dir "$HERE" --out "$HERE/out/html" \
      --model preview --skill-url preview \
      --max-words "$(setting report.max_words 1200)" --min-figures "$(setting report.min_figures 3)" \
      && echo "preview written to out/html/report.html" ;;
  all)
    "$0" snapshot "${2:-$REPO}"
    "$0" pairs "${2:-$REPO}"
    n=$(ls pairs/batches 2>/dev/null | wc -l)
    if [ "$n" -gt 0 ]; then
      echo "NOTE: $n batch file(s) of unclassified version pairs in pairs/batches/."
      echo "      Classify them (CLASSIFY_INSTRUCTIONS.md) into classifications/ before trusting the change statistics."
    fi
    "$0" analyze ;;
  *) echo "unknown step: $step" >&2; exit 2 ;;
esac
