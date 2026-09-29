"""scripts/deploy_update.sh end to end with real git: a bare origin, a production
clone with an unpushed data commit, and upstream commits whose tests pass or fail."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEST_CMD = "test \"$(cat verdict.txt)\" = pass"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout.strip()


def _seed(src: Path) -> None:
    for rel in ("pyproject.toml", "uv.lock", "cardtrack", "scripts/lib.sh",
                "scripts/deploy_update.sh", "scripts/get_setting.py"):
        s, d = ROOT / rel, src / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_dir():
            shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(s, d)
    (src / "config").mkdir()
    (src / "config" / "settings.yaml").write_text(
        yaml.safe_dump({"deploy": {"auto_pull": True, "test_cmd": TEST_CMD}}))
    (src / "verdict.txt").write_text("pass\n")
    (src / ".gitignore").write_text(".venv/\n.run.lock\nstate/\n")
    (src / "logs").mkdir()
    (src / "logs" / ".keep").write_text("")


def _setup(tmp_path: Path) -> tuple[Path, Path, Path]:
    origin, dev, prod = tmp_path / "origin.git", tmp_path / "dev", tmp_path / "prod"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    subprocess.run(["git", "clone", "-q", str(origin), str(dev)], check=True)
    for repo in (dev,):
        git(repo, "config", "user.email", "t@t"), git(repo, "config", "user.name", "t")
    _seed(dev)
    git(dev, "add", "-A"), git(dev, "commit", "-qm", "seed")
    git(dev, "push", "-q", "origin", "main")
    subprocess.run(["git", "clone", "-q", str(origin), str(prod)], check=True)
    git(prod, "config", "user.email", "p@p"), git(prod, "config", "user.name", "p")
    return origin, dev, prod


def _deploy(prod: Path, role: str | None = "prod") -> str:
    env = {**os.environ, "CARDTRACK_ROOT": str(prod)}
    env.pop("CARDTRACK_ROLE", None)
    if role:
        env["CARDTRACK_ROLE"] = role
    env.pop("VIRTUAL_ENV", None)
    p = subprocess.run(["bash", str(prod / "scripts" / "deploy_update.sh"), str(prod)],
                       env=env, capture_output=True, text=True, timeout=600)
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout


def _push_verdict(dev: Path, verdict: str, msg: str) -> str:
    (dev / "verdict.txt").write_text(verdict + "\n")
    (dev / "cardtrack" / "marker.py").write_text(f"# {msg}\n")   # a code change
    git(dev, "add", "-A"), git(dev, "commit", "-qm", msg), git(dev, "push", "-q", "origin", "main")
    return git(dev, "rev-parse", "HEAD")


def test_bad_commit_is_rejected_then_good_commit_deploys(tmp_path):
    _, dev, prod = _setup(tmp_path)
    # production has an unpushed data commit (yesterday's push failed)
    (prod / "logs" / "data.txt").write_text("run output\n")
    git(prod, "add", "logs/data.txt"), git(prod, "commit", "-qm", "data")
    before = git(prod, "rev-parse", "HEAD")

    bad = _push_verdict(dev, "fail", "bad")
    out = _deploy(prod)
    assert "tests FAILED" in out
    assert git(prod, "rev-parse", "HEAD") == before           # stayed on last good commit
    assert (prod / "state" / ".deploy_rejected").read_text().startswith(bad)
    assert "failed tests before" in _deploy(prod)              # not retried every run

    _push_verdict(dev, "pass", "fixed")
    out = _deploy(prod)
    assert "now running" in out
    assert not (prod / "state" / ".deploy_rejected").exists()
    assert (prod / "cardtrack" / "marker.py").read_text() == "# fixed\n"
    assert (prod / "logs" / "data.txt").exists()                # data commit rebased, kept
    assert git(prod, "merge-base", "--is-ancestor", "origin/main", "HEAD") == ""


def test_dirty_checkout_and_dev_role_are_left_alone(tmp_path):
    _, dev, prod = _setup(tmp_path)
    _push_verdict(dev, "pass", "new")
    (prod / "verdict.txt").write_text("local edit\n")
    assert "dirty" in _deploy(prod)
    git(prod, "checkout", "--", "verdict.txt")
    assert "no auto-pull" in _deploy(prod, role=None)      # the default role is dev
    (prod / ".env").write_text("CARDTRACK_ROLE=dev\n")
    assert "no auto-pull" in _deploy(prod, role=None)
    assert not (prod / "cardtrack" / "marker.py").exists()
