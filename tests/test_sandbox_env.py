"""Run the real bwrap sandbox and inspect what the agent process can see.
Requires bubblewrap with unprivileged user namespaces (CI enables them)."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = ROOT / "scripts" / "agent_sandbox.sh"

pytestmark = pytest.mark.skipif(shutil.which("bwrap") is None and not os.environ.get("CI"),
                                reason="bubblewrap not installed (CI installs it)")


def _run(tmp_path: Path, env_file: str, inner: str, **env) -> subprocess.CompletedProcess:
    # real layout: the repo lives under $HOME, never the other way round
    home = tmp_path / "home"
    root = home / "repo"
    root.mkdir(parents=True, exist_ok=True)
    (root / ".env").write_text(env_file)
    full = {**os.environ, "CARDTRACK_ROOT": str(root), "HOME": str(home), **env}
    return subprocess.run(["bash", str(SANDBOX), "bash", "-c", inner], env=full,
                          capture_output=True, text=True, timeout=60)


def test_env_keys_are_stripped_and_token_passes(tmp_path):
    p = _run(tmp_path,
             "CLOUDFLARE_API_TOKEN=cf-secret-value\nCLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat-test\n",
             'echo "cf=${CLOUDFLARE_API_TOKEN:-unset} tok=${CLAUDE_CODE_OAUTH_TOKEN:-unset}"; '
             'cat "$CARDTRACK_ROOT/.env"; ls -A "$HOME/.claude"',
             CLOUDFLARE_API_TOKEN="cf-secret-value")  # as if a caller exported .env
    assert p.returncode == 0, p.stderr
    assert "cf=unset tok=sk-ant-oat-test" in p.stdout
    assert "cf-secret-value" not in p.stdout          # .env masked with /dev/null
    assert ".credentials.json" not in p.stdout        # token mode seeds no file


def test_login_mode_seeds_slimmed_file_from_config_dir(tmp_path):
    cfg = tmp_path / "claude-cfg"  # outside $HOME: the tmpfs would hide it otherwise
    cfg.mkdir()
    (cfg / ".credentials.json").write_text(
        '{"claudeAiOauth": {"accessToken": "a", "refreshToken": "r", "expiresAt": 1}, '
        '"mcpOAuth": {"x": "y"}}')
    p = _run(tmp_path, "OTHER=1\n", 'cat "$HOME/.claude/.credentials.json"',
             CLAUDE_CONFIG_DIR=str(cfg))
    assert p.returncode == 0, p.stderr
    assert '"accessToken"' in p.stdout and "refresh" not in p.stdout and "mcp" not in p.stdout


def test_writable_paths_are_configurable(tmp_path):
    p = _run(tmp_path, "", 'touch "$CARDTRACK_ROOT/report/ok" && '
             '(touch "$CARDTRACK_ROOT/data/no" 2>/dev/null && echo data-writable || echo data-ro)',
             CARDTRACK_SANDBOX_RW="report")
    assert p.returncode == 0, p.stderr
    assert (tmp_path / "home" / "repo" / "report" / "ok").exists()
    assert "data-ro" in p.stdout


def test_rw_path_escape_is_refused(tmp_path):
    p = _run(tmp_path, "", "true", CARDTRACK_SANDBOX_RW="../etc")
    assert p.returncode == 91


def test_host_sockets_and_session_pointers_are_hidden(tmp_path):
    """/run/user holds the systemd user manager's bus: reachable, it lets the agent
    start commands outside the sandbox (found in review, 2026-09-29)."""
    p = _run(tmp_path, "", 'ls -A /run; echo "xdg=${XDG_RUNTIME_DIR:-unset} '
             'dbus=${DBUS_SESSION_BUS_ADDRESS:-unset} ssh=${SSH_AUTH_SOCK:-unset}"',
             XDG_RUNTIME_DIR="/run/user/1000", DBUS_SESSION_BUS_ADDRESS="unix:path=/x",
             SSH_AUTH_SOCK="/run/user/1000/agent")
    assert p.returncode == 0, p.stderr
    assert "user" not in p.stdout.split("xdg=")[0].split()
    assert "xdg=unset dbus=unset ssh=unset" in p.stdout


def test_repo_root_cannot_be_made_writable(tmp_path):
    for rw in (".", "./", ""):
        p = _run(tmp_path, "", "true", CARDTRACK_SANDBOX_RW=rw or " ")
        assert p.returncode == 91 or rw == "", (rw, p.stderr)


def test_read_only_island_inside_writable_dir(tmp_path):
    p = _run(tmp_path, "", 'touch "$CARDTRACK_ROOT/report/a" && '
             '(touch "$CARDTRACK_ROOT/report/published/b" 2>/dev/null '
             '&& echo pub-rw || echo pub-ro)',
             CARDTRACK_SANDBOX_RW="report", CARDTRACK_SANDBOX_RO="report/published")
    assert p.returncode == 0, p.stderr
    assert "pub-ro" in p.stdout


def test_tools_installed_under_home_are_runnable(tmp_path):
    """Claude Code's native installer puts `claude` in ~/.local/bin (Debian hosts);
    the $HOME tmpfs hid it and the agent failed with exit 127 (rehearsal, 2026-09-29)."""
    home = tmp_path / "home"
    (home / ".local" / "share" / "claude" / "versions").mkdir(parents=True)
    real = home / ".local" / "share" / "claude" / "versions" / "9.9.9"
    real.write_text("#!/bin/sh\necho fake-claude-ran\n")
    real.chmod(0o755)
    (home / ".local" / "bin").mkdir(parents=True)
    (home / ".local" / "bin" / "claude").symlink_to(real)
    p = _run(tmp_path, "", "claude",
             PATH=f"{home}/.local/bin:{os.environ['PATH']}")
    assert p.returncode == 0, p.stderr
    assert "fake-claude-ran" in p.stdout
