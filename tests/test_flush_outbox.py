"""flush_outbox.py against a fake `gh` on PATH (a real executable, real argv):
open-title dedup (#28/#31/#32) and the missing-label fallback (roster issues)."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
log = os.environ["FAKE_GH_LOG"]
open(log, "a").write(json.dumps(sys.argv[1:]) + "\n")
if sys.argv[1:3] == ["issue", "list"]:
    print(json.dumps([{"title": t} for t in json.loads(os.environ["FAKE_GH_OPEN"])]))
    sys.exit(0)
if sys.argv[1:3] == ["issue", "create"] and "--label" in sys.argv:
    print("could not add label: 'pipeline-failure' not found", file=sys.stderr)
    sys.exit(1)
print("https://github.com/o/r/issues/99")
'''


def _run(tmp_path: Path, records: list[dict], open_titles: list[str]) -> list[list[str]]:
    (tmp_path / "config").mkdir()
    (tmp_path / "logs").mkdir()
    (tmp_path / "config" / "settings.yaml").write_text(
        yaml.safe_dump({"github": {"repo": "o/r", "use_gh": True}}))
    with open(tmp_path / "logs" / "issues_outbox.jsonl", "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text(FAKE_GH)
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "gh.log"
    env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}",
           "FAKE_GH_LOG": str(log), "FAKE_GH_OPEN": json.dumps(open_titles),
           "HOME": str(tmp_path)}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "flush_outbox.py"),
                    "--root", str(tmp_path)], env=env, check=True, capture_output=True)
    return [json.loads(line) for line in log.read_text().splitlines()]


def _creates(calls):
    return [c for c in calls if c[:2] == ["issue", "create"]]


def test_duplicate_of_open_issue_is_not_filed_again(tmp_path):
    recs = [{"ts": "2026-09-29T00:00:00Z", "title": "needs-review: X", "body": "b", "labels": []},
            {"ts": "2026-09-29T00:00:00Z", "title": "needs-review: X", "body": "b", "labels": []},
            {"ts": "2026-09-29T00:00:00Z", "title": "needs-review: Y", "body": "b", "labels": []}]
    calls = _run(tmp_path, recs, open_titles=["needs-review: X"])
    titles = [c[c.index("--title") + 1] for c in _creates(calls)]
    assert titles == ["needs-review: Y"]
    assert (tmp_path / "logs" / "issues_outbox.jsonl").read_text() == ""


def test_missing_label_falls_back_to_unlabelled_issue(tmp_path):
    recs = [{"ts": "2026-09-29T00:00:00Z", "title": "roster failed", "body": "b",
             "labels": ["pipeline-failure"]}]
    calls = _run(tmp_path, recs, open_titles=[])
    creates = _creates(calls)
    assert len(creates) == 2 and "--label" in creates[0] and "--label" not in creates[1]
    assert (tmp_path / "logs" / "issues_outbox.jsonl").read_text() == ""
