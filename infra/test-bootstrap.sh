#!/usr/bin/env bash
# Run infra/bootstrap.sh in a throwaway Debian 13 container, overlay the current
# working tree, then run the test suite and build the report as the app user.
# Proves the package list and pinned tools are enough for every phase, without a VPS.
#   infra/test-bootstrap.sh            (needs docker; --privileged for bubblewrap)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
docker run --rm --privileged -e REPO_URL -v "$REPO:/src:ro" debian:trixie bash -euo pipefail -c '
  export DEBIAN_FRONTEND=noninteractive
  # the bootstrap under test is /src/infra/bootstrap.sh; it clones the public repo
  bash /src/infra/bootstrap.sh "${REPO_URL:-https://github.com/DouwMarx/cardtrack.git}" cardtrack
  # overlay uncommitted work so this tests the tree, not the last commit
  tar -C /src --exclude=.venv --exclude=data/raw --exclude=.git --exclude=.env -cf - . \
    | runuser -u cardtrack -- tar -C /home/cardtrack/cardtrack -xf -
  runuser -u cardtrack -- bash -lc "
    set -euo pipefail
    cd ~/cardtrack && ~/.local/bin/uv sync --frozen -q
    echo \"claude \$(~/.local/bin/claude --version)\"
    CI=1 ~/.local/bin/uv run pytest -q -rf 2>&1 | tail -6
    report/run.sh pdf && ~/.local/bin/uv run python scripts/report_html.py --report-dir report \
      --out /tmp/pub --model claude-test --skill-url https://example.com/SKILL.md >/dev/null
    echo \"report html: \$(grep -c \"<table\" /tmp/pub/report.html) tables\"
  "
'
