"""Shared fixtures: a real local HTTP server (no mocks — actual sockets, redirects,
status codes) and an isolated repo root per test."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------- http server

@dataclass
class Route:
    body: bytes = b""
    status: int = 200
    content_type: str = "text/html; charset=utf-8"
    headers: dict = field(default_factory=dict)
    block_plain_client: bool = False  # 400 for the primary client's exact UA
                                      # (simulates a TLS-fingerprinting bot wall)


class _Handler(BaseHTTPRequestHandler):
    server_version = "cardtracktest/1"

    def do_GET(self):  # noqa: N802
        from cardtrack.fetch import BROWSER_UA

        route = self.server.routes.get(self.path)  # type: ignore[attr-defined]
        self.server.hits.append(self.path)  # type: ignore[attr-defined]
        if route is not None and route.block_plain_client \
                and self.headers.get("User-Agent") == BROWSER_UA:
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"bot detected")
            return
        if route is None:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"not found")
            return
        self.send_response(route.status)
        self.send_header("Content-Type", route.content_type)
        for k, v in route.headers.items():
            self.send_header(k, v)
        self.end_headers()
        if route.status < 300 or route.status >= 400:
            body = route.body
            if b"__NONCE__" in body:
                self.server.nonce_counter += 1  # type: ignore[attr-defined]
                body = body.replace(
                    b"__NONCE__", str(self.server.nonce_counter).encode())
            self.wfile.write(body)

    def log_message(self, *args):  # silence
        pass


class TestServer:
    __test__ = False

    def __init__(self) -> None:
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self.httpd.routes = {}  # type: ignore[attr-defined]
        self.httpd.hits = []  # type: ignore[attr-defined]
        self.httpd.nonce_counter = 0  # type: ignore[attr-defined]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def routes(self) -> dict[str, Route]:
        return self.httpd.routes  # type: ignore[attr-defined]

    @property
    def hits(self) -> list[str]:
        return self.httpd.hits  # type: ignore[attr-defined]

    def url(self, path: str) -> str:
        host, port = self.httpd.server_address
        return f"http://{host}:{port}{path}"

    def set_html(self, path: str, body_text: str, title: str = "Doc") -> None:
        """Serve HTML whose raw bytes churn on every request (script nonce) while the
        extractable text stays stable — like real dynamic pages."""
        html = f"""<!DOCTYPE html><html><head><title>{title}</title>
<script>var nonce = "__NONCE__";</script></head>
<body><main><h1>{title}</h1><p>{body_text}</p></main></body></html>"""
        self.routes[path] = Route(body=html.encode())

    def set_redirect(self, path: str, target: str, permanent: bool = False) -> None:
        self.routes[path] = Route(status=301 if permanent else 302,
                                  headers={"Location": target})

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def http_server():
    server = TestServer()
    yield server
    server.stop()


# ---------------------------------------------------------------- pdf fixture

def make_pdf(text: str) -> bytes:
    """Assemble a minimal valid one-page PDF with correct xref offsets."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        None,  # content stream, built below
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    stream = f"BT /F1 14 Tf 72 720 Td ({escaped}) Tj ET".encode()
    objects[3] = (b"<< /Length " + str(len(stream)).encode()
                  + b" >>\nstream\n" + stream + b"\nendstream")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n").encode()
    return bytes(out)


@pytest.fixture
def pdf_bytes():
    return make_pdf("Hello cardtrack PDF fixture. Model evaluation results inside.")


# ---------------------------------------------------------------- repo root

def write_test_config(root: Path, server: TestServer, *, caps: dict | None = None,
                      gh_repo: str = "", fingerprint_fraction: float = 1.0) -> None:
    (root / "config").mkdir(parents=True, exist_ok=True)
    default_caps = {
        "max_new_documents_per_run": 10,
        "max_new_versions_per_run": 10,
        "max_fetch_bytes": 5_000_000,
        "max_total_fetch_bytes_per_run": 50_000_000,
        "fetch_timeout_seconds": 10,
    }
    default_caps.update(caps or {})
    settings = {
        "caps": default_caps,
        "cadence": {"fingerprint_fraction": fingerprint_fraction},
        "fetch": {"allow_private_hosts": True},
        "github": {"repo": gh_repo, "use_gh": False},  # outbox mode: never touch gh
        "site": {"title": "cardtrack-test", "run_pagefind": False},
        "publish": {"git_commit": False, "git_push": False, "wrangler_deploy": False},
        "agent": {"enabled": False, "cmd": ""},
    }
    sources = {
        "publishers": {
            "testlab": {"tier": 1, "index_urls": [server.url("/index-page")]},
            "tier2lab": {"tier": 2, "index_urls": []},
        },
        "evaluators": {
            "testeval": {"tier": 1, "index_urls": []},
        },
    }
    criteria = {
        "validator_checked": {
            "publisher_on_allowlist": True,
            "document_retrievable": True,
            "min_publication_date": "2026-01-01",
        },
        "agent_attested": {
            "primary_source": True,
            "about_a_specific_model_or_eval": True,
        },
        "policy": {"when_uncertain": "file_issue"},
    }
    import yaml

    (root / "config" / "settings.yaml").write_text(yaml.safe_dump(settings))
    (root / "config" / "sources.yaml").write_text(yaml.safe_dump(sources))
    (root / "config" / "criteria.yaml").write_text(yaml.safe_dump(criteria))


@pytest.fixture
def repo_root(tmp_path: Path, http_server: TestServer) -> Path:
    write_test_config(tmp_path, http_server)
    return tmp_path


@pytest.fixture
def repo(repo_root: Path):
    from cardtrack.repo import Repo

    return Repo(root=repo_root)


# ---------------------------------------------------------------- helpers

ATTESTED = {"primary_source": True, "about_a_specific_model_or_eval": True}


def make_proposal(server: TestServer, path: str = "/doc1", **overrides) -> dict:
    p = {
        "action": "add",
        "url": server.url(path),
        "title": "Test Model System Card",
        "publisher": "testlab",
        "doc_type": "system_card",
        "model_names": ["TestModel 1"],
        "publication_date": "2026-03-01",
        "justification": "A test document that meets all criteria.",
        "criteria": dict(ATTESTED),
        "evidence_urls": [server.url("/index-page")],
        "source_of_lead": "manual",
    }
    p.update(overrides)
    return p


def run_cli(script: str, *args: str, root: Path, stdin: str | None = None):
    """Run a scripts/ CLI exactly as a user would; returns (exit_code, parsed_json|stdout)."""
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / script), "--root", str(root), *args]
    proc = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=120)
    out = proc.stdout.strip()
    payload: object = out
    if out:
        try:
            payload = json.loads(out)  # whole stdout (pretty-printed JSON)
        except json.JSONDecodeError:
            try:
                payload = json.loads(out.splitlines()[-1])  # last-line JSON result
            except json.JSONDecodeError:
                payload = out
    return proc.returncode, payload, proc.stderr
