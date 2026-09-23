"""The derived layer: extracted text files and content fingerprints, both rebuilt from
the immutable raw store. Two entry points and one guard:

- reextract_all: re-run extraction over every stored version, overwrite the text files
  that changed, then recompute fingerprints (below). Dry-run reports what would change.
- recompute_fingerprints: recompute every fingerprint from the stored text with the
  current normalisation and ignore patterns; later versions whose fingerprint collapses
  onto an earlier one are pruned (the earliest version keeps the honest first-seen
  provenance). Raw blobs, text files and the changelog are never deleted.
- check_derived_layer: the monitor calls this first. If the stored texts and
  fingerprints were built by a different extractor version or ignore patterns, every
  unchanged document would mint a bogus version on its next fetch, so the run refuses
  to start and names the command that fixes it.
"""

from __future__ import annotations

import sqlite3

from .db import connect, get_meta, set_meta
from .extract import derived_config_id, extract_text, fingerprint_text, write_text_file
from .repo import Repo

META_KEY = "derived_config_id"


class DerivedLayerStale(RuntimeError):
    pass


def stamp_derived_layer(conn: sqlite3.Connection, repo: Repo) -> str:
    cid = derived_config_id(repo.fingerprint_ignore_patterns)
    set_meta(conn, META_KEY, cid)
    return cid


def check_derived_layer(conn: sqlite3.Connection, repo: Repo) -> str:
    """Bootstrap the stamp on a fresh database; refuse to run on a stale one."""
    current = derived_config_id(repo.fingerprint_ignore_patterns)
    stored = get_meta(conn, META_KEY)
    if stored is None:
        set_meta(conn, META_KEY, current)
        conn.commit()
        return current
    if stored != current:
        raise DerivedLayerStale(
            f"derived layer is stale: stored texts/fingerprints were built with config "
            f"{stored}, the code and settings now describe {current}. Run "
            "`uv run python scripts/extract_text.py --reextract-all --apply` "
            "(or `scripts/recompute_fingerprints.py --apply` if only the ignore patterns "
            "changed) before the monitor mints a bogus version for every document.")
    return current


def recompute_fingerprints(repo: Repo, apply: bool = False) -> dict:
    patterns = repo.fingerprint_ignore_patterns
    conn = connect(repo.db_path)
    summary = {"status": "applied" if apply else "dry_run", "versions": 0,
               "recomputed": 0, "pruned": 0, "docs_affected": 0}
    pruned_slugs: dict[str, int] = {}
    updates: list[tuple[int, str]] = []
    deletes: list[int] = []
    try:
        for doc in conn.execute("SELECT id, slug FROM documents ORDER BY id").fetchall():
            versions = conn.execute(
                "SELECT * FROM document_versions WHERE document_id = ? "
                "ORDER BY fetched_at ASC, id ASC", (doc["id"],)).fetchall()
            seen: dict[str, int] = {}
            touched = False
            for v in versions:
                summary["versions"] += 1
                path = repo.root / v["text_path"] if v["text_path"] else None
                if path is None or not path.exists():
                    fp = v["content_fingerprint"]  # extraction failed: raw hash stays
                else:
                    fp = fingerprint_text(path.read_text(encoding="utf-8"), patterns)
                if fp in seen:
                    summary["pruned"] += 1
                    pruned_slugs[doc["slug"]] = pruned_slugs.get(doc["slug"], 0) + 1
                    touched = True
                    deletes.append(v["id"])
                    continue
                seen[fp] = v["id"]
                if fp != v["content_fingerprint"]:
                    summary["recomputed"] += 1
                    touched = True
                    updates.append((v["id"], fp))
            if touched:
                summary["docs_affected"] += 1
        if apply:
            # deletes first, then updates through unique placeholders: a kept row's
            # new fingerprint may equal another row's current one mid-flight
            for vid in deletes:
                conn.execute("DELETE FROM document_versions WHERE id = ?", (vid,))
            for vid, _fp in updates:
                conn.execute("UPDATE document_versions SET content_fingerprint = ? "
                             "WHERE id = ?", (f"migrating:{vid}", vid))
            for vid, fp in updates:
                conn.execute("UPDATE document_versions SET content_fingerprint = ? "
                             "WHERE id = ?", (fp, vid))
            summary["derived_config_id"] = stamp_derived_layer(conn, repo)
            conn.commit()
    finally:
        conn.close()
    summary["pruned_by_doc"] = dict(sorted(pruned_slugs.items(), key=lambda kv: -kv[1]))
    summary["pruned_version_ids"] = deletes
    return summary


def reextract_all(repo: Repo, apply: bool = False) -> dict:
    conn = connect(repo.db_path)
    stats = {"status": "applied" if apply else "dry_run", "versions": 0,
             "text_changed": 0, "text_unchanged": 0, "failed": 0, "changed_version_ids": []}
    try:
        for row in conn.execute("SELECT * FROM document_versions ORDER BY id").fetchall():
            stats["versions"] += 1
            raw = repo.root / row["raw_path"]
            if not raw.exists():
                stats["failed"] += 1
                continue
            text, _method = extract_text(raw.read_bytes(), row["content_type"])
            if text is None:
                stats["failed"] += 1
                continue
            current = None
            if row["text_path"] and (repo.root / row["text_path"]).exists():
                current = (repo.root / row["text_path"]).read_text(encoding="utf-8")
            if current == text:
                stats["text_unchanged"] += 1
                continue
            stats["text_changed"] += 1
            stats["changed_version_ids"].append(row["id"])
            if apply:
                path = write_text_file(repo.text_dir, row["content_hash"], text,
                                       overwrite=True)
                conn.execute("UPDATE document_versions SET text_path = ? WHERE id = ?",
                             (str(path.relative_to(repo.root)), row["id"]))
        if apply:
            conn.commit()
    finally:
        conn.close()
    if apply:
        stats["fingerprints"] = recompute_fingerprints(repo, apply=True)
    return stats
