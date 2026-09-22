"""Network gate (cardtrack/network.py + scripts/wait_for_network.py)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from cardtrack.network import EX_TEMPFAIL, network_up, wait_for_network
from tests.conftest import PROJECT_ROOT, Route, TestServer


def _closed_port_url() -> str:
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()                       # nothing listens here now
    return f"http://127.0.0.1:{port}/"


def test_network_up_returns_first_answering_probe(http_server: TestServer):
    http_server.routes["/probe"] = Route(body=b"ok")
    http_server.routes["/err"] = Route(status=503, body=b"down")
    assert network_up([_closed_port_url(), http_server.url("/err")]) == http_server.url("/err")
    assert network_up([_closed_port_url()], timeout=1) is None


def test_wait_returns_immediately_when_up(http_server: TestServer):
    http_server.routes["/probe"] = Route(body=b"ok")
    up, waited = wait_for_network([http_server.url("/probe")], wait_seconds=60)
    assert up and waited < 5


def test_wait_polls_until_up_then_gives_up_at_deadline():
    """Deterministic clock: probes fail, fail, then succeed; then a never-up case."""
    calls = {"n": 0}
    now = {"t": 0.0}
    slept: list[float] = []

    def fake_sleep(s):
        slept.append(s)
        now["t"] += s

    import cardtrack.network as net
    original = net.network_up
    try:
        def flaky(urls, timeout=10.0):
            calls["n"] += 1
            return "u" if calls["n"] >= 3 else None
        net.network_up = flaky
        up, waited = net.wait_for_network(["x"], wait_seconds=100, interval=15,
                                          sleep=fake_sleep, clock=lambda: now["t"])
        assert up and slept == [15, 15] and waited == 30

        net.network_up = lambda urls, timeout=10.0: None
        slept.clear()
        now["t"] = 0.0
        up, waited = net.wait_for_network(["x"], wait_seconds=40, interval=15,
                                          sleep=fake_sleep, clock=lambda: now["t"])
        assert not up and waited == 40 and slept == [15, 15, 10]   # never overshoots
    finally:
        net.network_up = original


def test_cli_exit_codes(repo_root: Path, http_server: TestServer):
    http_server.routes["/probe"] = Route(body=b"ok")
    settings_path = repo_root / "config" / "settings.yaml"
    settings = yaml.safe_load(settings_path.read_text())

    settings["network"] = {"probe_urls": [http_server.url("/probe")], "wait_seconds": 5}
    settings_path.write_text(yaml.safe_dump(settings))
    proc = subprocess.run(["uv", "run", "--project", str(PROJECT_ROOT), "python",
                           str(PROJECT_ROOT / "scripts" / "wait_for_network.py"),
                           "--root", str(repo_root)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr

    settings["network"] = {"probe_urls": [_closed_port_url()], "wait_seconds": 2}
    settings_path.write_text(yaml.safe_dump(settings))
    proc = subprocess.run(["uv", "run", "--project", str(PROJECT_ROOT), "python",
                           str(PROJECT_ROOT / "scripts" / "wait_for_network.py"),
                           "--root", str(repo_root)], capture_output=True, text=True)
    assert proc.returncode == EX_TEMPFAIL
    assert "no network after" in proc.stdout
