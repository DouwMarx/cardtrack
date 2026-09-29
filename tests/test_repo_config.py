"""The committed config must parse and carry the keys the shell runners read.
A YAML slip otherwise turns every `setting` call into its default (features off)."""

from __future__ import annotations

from pathlib import Path

from cardtrack.repo import Repo

ROOT = Path(__file__).resolve().parents[1]


def test_committed_settings_parse_with_runner_keys():
    repo = Repo(root=ROOT)
    for key in ("agent.cmd", "agent.enabled", "report.cmd", "report.enabled",
                "deploy.auto_pull", "deploy.test_cmd", "publish.wrangler_deploy",
                "github.repo"):
        assert repo.setting(key) not in (None, ""), key
    assert "--model" in repo.setting("report.cmd")
