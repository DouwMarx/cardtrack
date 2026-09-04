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
        "--attest", "covered_model_class",
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
    """Undelivered comments queue for flush_outbox.py — before 2026-08-31 they were
    only logged and silently never reached GitHub (gh is unauth in the sandbox)."""
    code, res, err = run_cli("comment_issue.py", "--issue", "7",
                             "--body", "Verified: the link is alive again.",
                             root=repo_root)
    assert code == 0 and res["status"] == "queued"
    logged = (repo_root / "logs" / "comments.jsonl").read_text()
    assert "alive again" in logged
    queued = json.loads((repo_root / "logs" / "comments_outbox.jsonl").read_text())
    assert queued["issue"] == 7 and "alive again" in queued["body"]
    assert queued["resolve"] is False


@pytest.mark.skipif(shutil.which("uv") is None or shutil.which("flock") is None
                    or shutil.which("timeout") is None,
                    reason="run_daily.sh needs uv, flock and coreutils timeout")
@pytest.mark.parametrize("cmd,expected,rc", [
    # healthy agent: exits 0 AND writes the run report → heartbeat success, exit 0
    ('echo "AGENT SAW max-turns=$CARDTRACK_MAX_TURNS" '
     '&& date -u > "$CARDTRACK_ROOT/logs/run_report.md"',
     "AGENT SAW max-turns=123", 0),
    # wedged agent: killed by the backstop → run still publishes but exits 3
    ("sleep 30", "wall-clock backstop", 3),
])
def test_run_daily_agent_phase_guards(repo_root, http_server, cmd, expected, rc):
    """The turn cap has exactly one source of truth; wall clock — not turns —
    stops a runaway agent; and the heartbeat makes agent failure loud (exit 3,
    failure streak) without ever blocking build & publish."""
    import yaml

    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())
    settings["agent"] = {"enabled": True, "max_turns": 123, "timeout_seconds": 2, "cmd": cmd}
    settings_path.write_text(yaml.safe_dump(settings))

    env = dict(os.environ, CARDTRACK_ROOT=str(repo_root), RUN_ID="agent-guard",
               CARDTRACK_NO_SANDBOX="1", CARDTRACK_SKIP_TOKEN_REFRESH="1")
    proc = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / "run_daily.sh")],
                          capture_output=True, text=True, timeout=600, env=env)
    assert proc.returncode == rc, proc.stdout + proc.stderr
    assert expected in proc.stdout, proc.stdout
    assert "Phase C" in proc.stdout, "a failed agent never blocks build & publish"
    if rc == 0:
        assert (repo_root / "logs" / ".agent_last_success").exists()
        assert not (repo_root / "logs" / ".agent_failstreak").exists()
    else:
        assert (repo_root / "logs" / ".agent_failstreak").read_text().strip() == "1"
        assert "AGENT PHASE FAILED" in proc.stdout


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


@pytest.mark.skipif(shutil.which("uv") is None or shutil.which("flock") is None
                    or shutil.which("git") is None,
                    reason="run_daily.sh needs uv, flock, git")
def test_run_daily_security_hold_blocks_publish(repo_root, http_server):
    """A planted secret holds the whole run: no commit, outbox not flushed, exit 1;
    the quarantine exclusion lets a cleaned rerun pass (does not re-trip forever)."""
    import yaml

    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())
    settings["publish"]["git_commit"] = True   # commit path on; push/deploy stay off
    settings_path.write_text(yaml.safe_dump(settings))

    http_server.set_html("/card-a", "Held run content.")
    run_cli("propose_doc.py", "--json", "-", "--run-id", "seed", root=repo_root,
            stdin=json.dumps(make_proposal(http_server, path="/card-a",
                                           model_names=["HeldModel"])))
    subprocess.run(["git", "init", "-q", str(repo_root)], check=True)
    subprocess.run(["git", "-C", str(repo_root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo_root), "-c", "user.email=t@t", "-c",
                    "user.name=t", "commit", "-qm", "init"], check=True)
    base = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()

    token = "ghp_" + "a1B2c3D4" * 5  # 40 alnum chars: matches github_token
    (repo_root / "logs" / "run_report.md").write_text(f"leak {token} end\n")
    run_cli("comment_issue.py", "--issue", "9", "--body", f"leak {token}", root=repo_root)

    env = dict(os.environ, CARDTRACK_ROOT=str(repo_root), RUN_ID="held")
    proc = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / "run_daily.sh")],
                          capture_output=True, text=True, timeout=600, env=env)
    assert proc.returncode == 1, proc.stdout
    assert "SECURITY HOLD" in proc.stdout
    head = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    assert head == base, "held run must not commit"
    assert (repo_root / "logs" / "comments_outbox.jsonl").exists(), "outbox not flushed"
    assert not (repo_root / "logs" / "comments_outbox.sent.jsonl").exists()
    assert (repo_root / "logs" / "SECURITY_HOLD.md").exists()

    # clean up and rerun: the cleared hold must let publishing proceed. The token
    # persists in every log that captured it — run_report, both comment logs,
    # SECURITY_HOLD — and each is correctly scanned, so all must be cleaned.
    (repo_root / "logs" / "run_report.md").write_text("clean report\n")
    (repo_root / "logs" / "comments_outbox.jsonl").unlink()
    (repo_root / "logs" / "comments.jsonl").unlink()
    (repo_root / "logs" / "SECURITY_HOLD.md").unlink()
    proc2 = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / "run_daily.sh")],
                           capture_output=True, text=True, timeout=600,
                           env=dict(env, RUN_ID="cleared"))
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr
    assert "SECURITY HOLD" not in proc2.stdout
