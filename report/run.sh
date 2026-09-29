#!/usr/bin/env bash
# Rebuild the research report from a fresh snapshot of this repo's database.
#
#   report/run.sh snapshot   read-only snapshot of the repo (DB, run logs, journal) into report/data
#   report/run.sh pairs      version-pair diffs + batches of still-unclassified pairs
#   report/run.sh analyze    results.json, macros.tex, tables/, figures/, comprehensive_report.md
#   report/run.sh pdf        compile tex/report.tex -> tex/report.pdf and render page PNGs
#   report/run.sh all        snapshot + pairs + analyze + pdf (classification is a separate,
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
step="${1:-all}"
case "$step" in
  snapshot) ./snapshot.sh "${2:-$REPO}" ;;
  pairs)    "${PY[@]}" build_pairs.py --repo "${2:-$REPO}" ;;
  analyze)  "${PY[@]}" analyze.py >/dev/null && echo "analysis written to out/" ;;
  pdf)
    cd tex
    latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex >/dev/null
    cp report.aux ../out/report.aux      # label numbers for the HTML version
    latexmk -c >/dev/null 2>&1 || true
    rm -f page-*.png
    pdftoppm -r 80 -png report.pdf page >/dev/null 2>&1 || true
    echo "tex/report.pdf: $(pdfinfo report.pdf | awk '/Pages/ {print $2}') pages" ;;
  all)
    "$0" snapshot "${2:-$REPO}"
    "$0" pairs "${2:-$REPO}"
    n=$(ls pairs/batches 2>/dev/null | wc -l)
    if [ "$n" -gt 0 ]; then
      echo "NOTE: $n batch file(s) of unclassified version pairs in pairs/batches/."
      echo "      Classify them (CLASSIFY_INSTRUCTIONS.md) into classifications/ before trusting section 6."
    fi
    "$0" analyze
    "$0" pdf ;;
  *) echo "unknown step: $step" >&2; exit 2 ;;
esac
