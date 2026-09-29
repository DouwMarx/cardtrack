"""The public archive of original documents (Cloudflare R2, served at
settings `archive.public_base_url`).

Every stored version's original bytes are published at `<base>/raw/<file>`, the
same hash-addressed file name as in data/raw/, so anyone can check a download
against the sha256 in the database. `config/withheld.txt` lists content hashes kept
off the public bucket (takedown requests); they stay in the private backup.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .repo import Repo, utcnow

WITHHELD_FILE = "withheld.txt"


def withheld_hashes(repo: Repo) -> set[str]:
    """Content hashes withheld from the public bucket: one sha256 per line,
    `#` starts a comment (reason, date, requester)."""
    path = repo.config_dir / WITHHELD_FILE
    if not path.exists():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        h = line.split("#", 1)[0].strip().lower()
        if h:
            out.add(h)
    return out


def public_base(repo: Repo) -> str:
    return (repo.setting("archive.public_base_url", "") or "").rstrip("/")


def raw_url(base: str, raw_path: str | None, content_hash: str, withheld: set[str]) -> str | None:
    if not base or not raw_path or content_hash.lower() in withheld:
        return None
    return f"{base}/raw/{Path(raw_path).name}"


def manifest(repo: Repo, conn: sqlite3.Connection) -> dict:
    """Every stored version with its hash and download link, for the public
    `manifest.json` (the bucket itself cannot be listed by visitors)."""
    base = public_base(repo)
    withheld = withheld_hashes(repo)
    rows = conn.execute(
        "SELECT d.slug, d.title, d.publisher, d.canonical_url, d.status, "
        "       v.id AS version_id, v.fetched_at, v.content_type, v.byte_size, "
        "       v.content_hash, v.raw_path, v.text_path "
        "FROM document_versions v JOIN documents d ON d.id = v.document_id "
        "ORDER BY d.slug, v.fetched_at, v.id").fetchall()
    versions = []
    for r in rows:
        url = raw_url(base, r["raw_path"], r["content_hash"], withheld)
        versions.append({
            "document": r["slug"], "title": r["title"], "publisher": r["publisher"],
            "canonical_url": r["canonical_url"], "status": r["status"],
            "version_id": r["version_id"], "fetched_at": r["fetched_at"],
            "content_type": r["content_type"], "byte_size": r["byte_size"],
            "sha256": r["content_hash"],
            "file": f"raw/{Path(r['raw_path']).name}" if r["raw_path"] else None,
            "url": url,
            "withheld": url is None and bool(base),
        })
    return {"generated_at": utcnow(), "base_url": base,
            "versions": versions,
            "counts": {"versions": len(versions),
                       "withheld": sum(1 for v in versions if v["withheld"])}}
