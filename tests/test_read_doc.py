"""scripts/read_doc.py: the agent's read helper must read what the validator reads
and leave no trace in data/."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

from cardtrack.propose import process_proposal

from .conftest import PROJECT_ROOT, Route, make_proposal


def run_read_doc(root: Path, *args: str):
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "read_doc.py"),
           "--root", str(root), *args]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


def _data_snapshot(root: Path) -> tuple:
    db = root / "data" / "docs.sqlite"
    files = sorted(str(p.relative_to(root)) for p in (root / "data").rglob("*")
                   if p.is_file())
    digest = hashlib.sha256(db.read_bytes()).hexdigest() if db.exists() else None
    return digest, files


def test_url_html_extracted_and_nothing_written(repo_root, http_server):
    http_server.set_html("/page", "The model was evaluated on cyber tasks.", title="Card X")
    before = _data_snapshot(repo_root)
    code, out, err = run_read_doc(repo_root, http_server.url("/page"))
    assert code == 0, err
    assert "evaluated on cyber tasks" in out
    assert "nonce" not in out, "extraction, not raw HTML"
    assert "HTTP 200" in err and "html extraction" in err
    assert _data_snapshot(repo_root) == before, "a read must not store anything"


def test_url_pdf_extracted(repo_root, http_server, pdf_bytes):
    http_server.routes["/card.pdf"] = Route(body=pdf_bytes, content_type="application/pdf")
    code, out, err = run_read_doc(repo_root, http_server.url("/card.pdf"))
    assert code == 0, err
    assert "Model evaluation results inside" in out
    assert "pdf extraction" in err


def test_url_raw_prints_body(repo_root, http_server):
    http_server.set_html("/page", "Body text.")
    code, out, _ = run_read_doc(repo_root, http_server.url("/page"), "--raw")
    assert code == 0
    assert "<!DOCTYPE html>" in out and "Body text." in out


def test_url_blocked_exits_nonzero_with_reason(repo_root, http_server):
    http_server.routes["/walled"] = Route(status=403, body=b"forbidden")
    code, out, err = run_read_doc(repo_root, http_server.url("/walled"))
    assert code == 1 and out == ""
    assert err.strip().startswith("read_doc: blocked: HTTP 403"), err


def test_url_not_found_and_too_large(repo_root, http_server):
    code, _, err = run_read_doc(repo_root, http_server.url("/nope"))
    assert code == 1 and "not found: HTTP 404" in err
    http_server.routes["/big"] = Route(body=b"x" * 6_000_000, content_type="text/html")
    code, _, err = run_read_doc(repo_root, http_server.url("/big"))  # cap is 5 MB in tests
    assert code == 1 and err.startswith("read_doc: too large"), err


def test_max_chars_truncates_with_marker(repo_root, http_server):
    http_server.set_html("/long", "word " * 2000)
    code, out, _ = run_read_doc(repo_root, http_server.url("/long"), "--max-chars", "100")
    assert code == 0
    assert "[read_doc: truncated at 100 of" in out
    assert len(out.split("\n\n[read_doc:")[0]) == 100


def test_slug_prints_latest_text_path_and_text(repo, repo_root, http_server):
    http_server.set_html("/doc1", "First capture text.")
    added = process_proposal(repo, make_proposal(http_server), "run1")
    http_server.set_html("/doc1", "Second capture text, revised.")
    assert process_proposal(repo, make_proposal(http_server), "run2").status == "written"
    before = _data_snapshot(repo_root)
    code, out, err = run_read_doc(repo_root, added.slug)
    assert code == 0, err
    first_line, _, text = out.partition("\n")
    assert first_line.startswith("data/text/") and (repo_root / first_line).exists()
    assert "Second capture text, revised." in text, "latest version wins"
    assert "First capture" not in text
    assert _data_snapshot(repo_root) == before


def test_unknown_slug_exits_nonzero(repo, repo_root, http_server):
    http_server.set_html("/doc1", "content")
    process_proposal(repo, make_proposal(http_server), "run1")  # DB exists
    code, out, err = run_read_doc(repo_root, "no-such-slug")
    assert code == 1 and out == "" and "not found" in err
