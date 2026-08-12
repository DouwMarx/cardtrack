"""End-to-end through the documented user path: seed via the propose_doc.py CLI,
monitor via its CLI, detect a silent update, build the site, check the outputs.
Also exercises run_daily.sh itself (Phase A + C, everything else disabled)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest

from .conftest import PROJECT_ROOT, make_proposal, run_cli


def test_full_pipeline_via_clis(repo_root, http_server, pdf_bytes):
    from .conftest import Route

    # 1. seed one HTML doc + one PDF doc through the CLI, JSON mode and flag mode
    http_server.set_html("/card-a", "Model A shows strong evaluation performance.")
    http_server.routes["/card-b.pdf"] = Route(body=pdf_bytes, content_type="application/pdf")

    code, res, err = run_cli("propose_doc.py", "--json", "-", "--run-id", "seedrun",
                             root=repo_root,
                             stdin=json.dumps(make_proposal(http_server, path="/card-a",
                                                            model_names=["Model A"])))
    assert code == 0 and res["status"] == "written", (res, err)

    code, res_b, err = run_cli(
        "propose_doc.py", "--run-id", "seedrun", "--action", "add",
        "--url", http_server.url("/card-b.pdf"), "--title", "Model B Evaluation Report",
        "--publisher", "testeval", "--doc-type", "independent_eval",
        "--model", "Model B", "--publication-date", "2026-02-02",
        "--justification", "Independent eval of Model B.",
        "--evidence-url", http_server.url("/index-page"),
        "--safety-evals", "yes",
        "--attest", "primary_source", "--attest", "about_a_specific_model_or_eval",
        "--attest", "distinct_model_release", "--attest", "notable_release",
        root=repo_root)
    assert code == 0 and res_b["status"] == "written", (res_b, err)
    assert res_b["slug"] == "testeval-model-b-independent-eval"

    # 2. monitor: no changes → no new versions
    code, summary, err = run_cli("monitor.py", "--run-id", "m1", root=repo_root)
    assert code == 0 and summary["new_versions"] == 0, (summary, err)

    # 3. silent update → monitor picks it up as a new version
    http_server.set_html("/card-a", "Model A card updated with new red-team results.")
    code, summary, err = run_cli("monitor.py", "--run-id", "m2", root=repo_root)
    assert code == 0 and summary["new_versions"] == 1, (summary, err)

    # 4. state summary reflects both docs
    code, state, err = run_cli("state_summary.py", root=repo_root)
    assert code == 0 and state["document_count"] == 2

    # 5. build site; both pages and metadata exist; version history shows 2 versions
    code, build, err = run_cli("build_site.py", "--no-pagefind", root=repo_root)
    assert code == 0 and build["documents"] == 2, (build, err)
    meta = json.loads((repo_root / "site" / "data" / "metadata.json").read_text())
    by_slug = {d["slug"]: d for d in meta["documents"]}
    assert by_slug[res["slug"]]["version_count"] == 2
    assert by_slug[res_b["slug"]]["doc_type"] == "independent_eval"
    assert by_slug[res_b["slug"]]["is_independent"] == 1

    page = (repo_root / "site" / "docs" / f"{res['slug']}.html").read_text()
    assert "red-team results" in page, "latest version's text is published"

    # 6. commit message renders from the changelog
    code, out, err = run_cli("build_site.py", "--emit-commit-msg", "m2", root=repo_root)
    assert code == 0 and "1 new version(s)" in out

    # 7. extraction rebuild is a no-op when nothing changed
    code, stats, err = run_cli("extract_text.py", "--reextract-all", root=repo_root)
    assert code == 0 and stats["versions"] == 3 and stats["conflicts"] == []


def test_comment_issue_outbox_mode(repo_root):
    code, res, err = run_cli("comment_issue.py", "--issue", "7",
                             "--body", "Verified: the link is alive again.",
                             root=repo_root)
    assert code == 0 and res["status"] == "logged_only"
    logged = (repo_root / "logs" / "comments.jsonl").read_text()
    assert "alive again" in logged


@pytest.mark.skipif(shutil.which("uv") is None or shutil.which("flock") is None,
                    reason="run_daily.sh needs uv and flock")
def test_run_daily_orchestration(repo_root, http_server):
    """Phase A + C through the actual shell entrypoint (agent/publish disabled)."""
    http_server.set_html("/card-a", "Daily run content.")
    code, res, err = run_cli("propose_doc.py", "--json", "-", "--run-id", "seed",
                             root=repo_root,
                             stdin=json.dumps(make_proposal(http_server, path="/card-a",
                                                            model_names=["DailyModel"])))
    assert code == 0 and res["status"] == "written", (res, err)

    env = dict(os.environ, CARDTRACK_ROOT=str(repo_root), RUN_ID="daily-e2e")
    proc = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / "run_daily.sh")],
                          capture_output=True, text=True, timeout=600, env=env)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Phase A" in proc.stdout and "Phase C" in proc.stdout
    assert "agent disabled" in proc.stdout
    assert (repo_root / "site" / "index.html").exists()
    logs = list((repo_root / "logs").glob("run-*.log"))
    assert logs, "run log written"
