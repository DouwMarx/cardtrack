"""Public archive: per-version links, withheld hashes, manifest and dataset,
and scripts/backup.sh against a real S3 endpoint (`rclone serve s3`)."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import tarfile
import time
from pathlib import Path

import pytest
import yaml

from cardtrack.archive import manifest, withheld_hashes
from cardtrack.db import connect
from cardtrack.propose import process_proposal
from cardtrack.sitebuild import build_site
from scripts.build_dataset import build

from .conftest import make_proposal

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://data.example.org"


def _enable(repo_root: Path, base: str = BASE) -> None:
    path = repo_root / "config" / "settings.yaml"
    s = yaml.safe_load(path.read_text())
    s["archive"] = {"public_base_url": base, "contact": "ops@example.org"}
    path.write_text(yaml.safe_dump(s))


def _two_docs(repo, http_server):
    http_server.set_html("/a", "First archived document.")
    http_server.set_html("/b", "Second archived document.")
    a = process_proposal(repo, make_proposal(http_server, path="/a", model_names=["A"]), "r")
    b = process_proposal(repo, make_proposal(http_server, path="/b", model_names=["B"]), "r")
    conn = connect(repo.db_path)
    rows = {r["slug"]: dict(r) for r in conn.execute(
        "SELECT d.slug, v.content_hash, v.raw_path FROM document_versions v "
        "JOIN documents d ON d.id = v.document_id")}
    conn.close()
    return rows[a.slug], rows[b.slug], a.slug, b.slug


def test_pages_link_originals_and_honour_withheld(repo, repo_root, http_server):
    _enable(repo_root)
    va, vb, sa, sb = _two_docs(repo, http_server)
    (repo_root / "config" / "withheld.txt").write_text(f"{vb['content_hash']}  # test takedown\n")
    build_site(repo, run_pagefind=False)
    page_a = (repo.site_dir / "docs" / f"{sa}.html").read_text()
    page_b = (repo.site_dir / "docs" / f"{sb}.html").read_text()
    assert f'{BASE}/raw/{Path(va["raw_path"]).name}' in page_a
    assert "archived copy" not in page_b and "withheld" in page_b
    about = (repo.site_dir / "about.html").read_text()
    assert "Never re-hosts" not in about and f"{BASE}/cardtrack-dataset.tar.gz" in about


def test_no_links_until_public_base_is_set(repo, repo_root, http_server):
    _, _, sa, _ = _two_docs(repo, http_server)
    build_site(repo, run_pagefind=False)
    page = (repo.site_dir / "docs" / f"{sa}.html").read_text()
    assert "archived copy" not in page and "<th>Original</th>" not in page


def test_manifest_and_dataset(repo, repo_root, http_server, tmp_path):
    _enable(repo_root)
    va, vb, _, _ = _two_docs(repo, http_server)
    (repo_root / "config" / "withheld.txt").write_text(f"# note\n{vb['content_hash']}\n")
    assert withheld_hashes(repo) == {vb["content_hash"]}
    out = tmp_path / "pub"
    res = build(repo, out)
    assert res["versions"] == 2 and res["withheld"] == 1
    man = json.loads((out / "manifest.json").read_text())
    urls = (out / "urls.txt").read_text().split()
    assert urls == [f'{BASE}/raw/{Path(va["raw_path"]).name}']
    assert (out / "withheld.txt").read_text().strip() == Path(vb["raw_path"]).name
    assert {v["sha256"] for v in man["versions"]} == {va["content_hash"], vb["content_hash"]}
    with tarfile.open(out / "cardtrack-dataset.tar.gz") as tar:
        names = tar.getnames()
    assert "cardtrack-dataset/docs.sqlite" in names and "cardtrack-dataset/README.txt" in names
    conn = connect(repo.db_path)
    assert manifest(repo, conn)["counts"]["withheld"] == 1
    conn.close()


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def s3(tmp_path):
    """A real S3 endpoint: `rclone serve s3` over a temp dir (buckets = subdirs)."""
    if not shutil.which("rclone"):
        if os.environ.get("CI"):
            pytest.fail("CI must provide rclone >= 1.65")
        pytest.skip("needs rclone >= 1.65")
    store = tmp_path / "s3store"
    (store / "priv").mkdir(parents=True)
    (store / "pub").mkdir()
    port = _free_port()
    proc = subprocess.Popen(["rclone", "serve", "s3", str(store), "--addr", f"127.0.0.1:{port}",
                             "--auth-key", "testkey,testsecret123"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    env = {"RCLONE_S3_PROVIDER": "Rclone", "RCLONE_S3_ACCESS_KEY_ID": "testkey",
           "RCLONE_S3_SECRET_ACCESS_KEY": "testsecret123",
           "RCLONE_S3_ENDPOINT": f"http://127.0.0.1:{port}"}
    try:
        for _ in range(60):
            if subprocess.run(["rclone", "lsd", ":s3:"], env={**os.environ, **env},
                              capture_output=True).returncode == 0:
                break
            time.sleep(0.25)
        else:
            pytest.fail("rclone serve s3 did not start: " + proc.stderr.read(2000).decode())
        yield env
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def _ls(env, path):
    p = subprocess.run(["rclone", "lsf", path], env={**os.environ, **env},
                       capture_output=True, text=True)
    return set(p.stdout.split())


def test_backup_fills_both_buckets_and_takedown_touches_only_public(
        repo, repo_root, http_server, s3, tmp_path):
    _enable(repo_root)
    va, vb, _, _ = _two_docs(repo, http_server)
    fa, fb = Path(va["raw_path"]).name, Path(vb["raw_path"]).name
    (repo_root / ".env").write_text(
        "R2_BUCKET=priv\nR2_PUBLIC_BUCKET=pub\nR2_PROVIDER=Rclone\n"
        f"R2_ACCESS_KEY_ID={s3['RCLONE_S3_ACCESS_KEY_ID']}\n"
        f"R2_SECRET_ACCESS_KEY={s3['RCLONE_S3_SECRET_ACCESS_KEY']}\n"
        f"R2_ENDPOINT={s3['RCLONE_S3_ENDPOINT']}\n")
    (repo_root / ".venv").symlink_to(ROOT / ".venv")

    def backup():
        p = subprocess.run(["bash", str(ROOT / "scripts" / "backup.sh"), str(repo_root)],
                           capture_output=True, text=True, timeout=300)
        assert p.returncode == 0, p.stdout + p.stderr

    backup()
    assert _ls(s3, ":s3:priv/raw") == {fa, fb}
    assert _ls(s3, ":s3:pub/raw") == {fa, fb}
    assert {"manifest.json", "urls.txt", "cardtrack-dataset.tar.gz"} <= _ls(s3, ":s3:pub")
    assert (repo_root / "state" / ".backup_last_ok").exists()

    # takedown: gone from the public bucket, kept in the private one
    (repo_root / "config" / "withheld.txt").write_text(f"{vb['content_hash']}\n")
    backup()
    assert _ls(s3, ":s3:pub/raw") == {fa}
    assert _ls(s3, ":s3:priv/raw") == {fa, fb}

    # restore from the private bucket reproduces the bytes
    restored = tmp_path / "restored"
    subprocess.run(["rclone", "copy", ":s3:priv/raw", str(restored)],
                   env={**os.environ, **s3}, check=True)
    for f in (fa, fb):
        assert (restored / f).read_bytes() == (repo_root / "data" / "raw" / f).read_bytes()


def test_dataset_build_leaves_the_database_untouched(repo, repo_root, http_server, tmp_path):
    """The backup runs after the daily commit; a rewritten docs.sqlite would leave the
    checkout dirty and block the next deploy."""
    _enable(repo_root)
    _two_docs(repo, http_server)
    before = repo.db_path.read_bytes()
    mtime = repo.db_path.stat().st_mtime_ns
    build(repo, tmp_path / "pub")
    assert repo.db_path.read_bytes() == before and repo.db_path.stat().st_mtime_ns == mtime
