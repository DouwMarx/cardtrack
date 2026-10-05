"""scripts/log_note.py: the agent's only append path for friction.jsonl / PROPOSALS.md."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "log_note.py"


def run(repo_root: Path, *args: str, env: dict | None = None) -> tuple[int, dict]:
    full = {**os.environ, **(env or {})}
    p = subprocess.run([sys.executable, str(SCRIPT), "--root", str(repo_root), *args],
                       capture_output=True, text=True, env=full)
    # argparse usage errors print nothing on stdout
    out = json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else {}
    return p.returncode, out


def test_friction_appends_one_json_line_with_run_id(repo_root):
    rc, out = run(repo_root, "friction", "--kind", "index_gap", "--detail", "HF lag",
                  "--url", "https://huggingface.co/x/y", env={"CARDTRACK_RUN_ID": "r1"})
    assert rc == 0 and out["status"] == "ok"
    rc, _ = run(repo_root, "friction", "--kind", "tooling", "--detail", "second")
    lines = (repo_root / "logs" / "friction.jsonl").read_text().splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["kind"] == "index_gap" and first["run_id"] == "r1"
    assert first["url"] == "https://huggingface.co/x/y" and first["ts"].endswith("Z")
    assert "slug" not in first


def test_friction_repairs_missing_trailing_newline(repo_root):
    logs = repo_root / "logs"
    logs.mkdir()
    (logs / "friction.jsonl").write_text('{"ts": "t0", "kind": "other", "detail": "old"}')
    rc, _ = run(repo_root, "friction", "--kind", "other", "--detail", "new")
    assert rc == 0
    lines = (logs / "friction.jsonl").read_text().splitlines()
    assert [json.loads(line)["detail"] for line in lines] == ["old", "new"]


def test_friction_rejects_unknown_kind_long_detail_and_bare_recurrence(repo_root):
    rc, out = run(repo_root, "friction", "--kind", "ambiguous", "--detail", "x")
    assert rc != 0                                         # argparse choices
    rc, out = run(repo_root, "friction", "--kind", "cap", "--detail", "x" * 1501)
    assert rc == 2 and "max 1500" in out["reason"]
    rc, out = run(repo_root, "friction", "--kind", "recurrence", "--detail", "again")
    assert rc == 2 and "--recurrence-of" in out["reason"]
    assert not (repo_root / "logs" / "friction.jsonl").exists()


def test_proposal_appends_dated_section(repo_root, tmp_path):
    body = tmp_path / "body.md"
    body.write_text("**Problem.** A.\n\n**Suggested change.** B.\n")
    rc, out = run(repo_root, "proposal", "--title", "Watch the HF API", "--body-file", str(body))
    assert rc == 0 and out["status"] == "ok"
    rc, _ = run(repo_root, "proposal", "--title", "Second", "--body", "C")
    text = (repo_root / "logs" / "PROPOSALS.md").read_text()
    heads = [line for line in text.splitlines() if line.startswith("## ")]
    assert len(heads) == 2
    assert heads[0].endswith("— Watch the HF API") and heads[1].endswith("— Second")
    assert "**Problem.** A." in text and text.endswith("C\n\n")
    assert text.count("---") == 2


def test_proposal_requires_exactly_one_body_source(repo_root):
    rc, out = run(repo_root, "proposal", "--title", "T")
    assert rc == 2 and "exactly one" in out["reason"]
