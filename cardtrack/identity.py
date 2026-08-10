"""Logical identity: model-name normalization, slug derivation, duplicate detection."""

from __future__ import annotations

import json
import re
import sqlite3


def normalize_model_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


def model_name_set(model_names: list[str]) -> set[str]:
    return {normalize_model_name(n) for n in model_names if normalize_model_name(n)}


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


def derive_slug(conn: sqlite3.Connection, publisher: str, model_names: list[str],
                doc_type: str) -> str:
    """Deterministic: <publisher>-<primary model>-<doc_type>, numeric suffix on collision.
    Agent-supplied slugs are ignored (spec §7)."""
    primary = model_names[0] if model_names else "unspecified"
    base = slugify(f"{publisher}-{primary}-{doc_type.replace('_', '-')}")
    slug = base
    n = 1
    while conn.execute("SELECT 1 FROM documents WHERE slug = ?", (slug,)).fetchone():
        n += 1
        slug = f"{base}-{n}"
    return slug


def find_doc_by_url(conn: sqlite3.Connection, canonical: str) -> sqlite3.Row | None:
    """Look up a document by canonical URL, falling back to a scan of alt_urls."""
    row = conn.execute(
        "SELECT * FROM documents WHERE canonical_url = ?", (canonical,)
    ).fetchone()
    if row:
        return row
    for row in conn.execute("SELECT * FROM documents WHERE alt_urls != '[]'"):
        if canonical in json.loads(row["alt_urls"]):
            return row
    return None


def title_similarity(a: str, b: str) -> float:
    """Jaccard similarity of normalized title tokens."""
    ta = set(normalize_model_name(a).split())
    tb = set(normalize_model_name(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


TITLE_SIMILARITY_THRESHOLD = 0.6


def find_logical_duplicates(
    conn: sqlite3.Connection,
    publisher: str,
    doc_type: str,
    model_names: list[str],
    title: str = "",
    exclude_canonical_url: str | None = None,
) -> list[sqlite3.Row]:
    """Catch "same card, different URL" (spec §5): publisher + doc_type + overlapping
    normalized model names PLUS clearly similar title. Same-date alone is not a
    trigger (two distinct docs about one model on launch day is normal); exact
    mirrors are caught separately by the content fingerprint. Outcome for a match
    is needs_review, never a merge."""
    proposed = model_name_set(model_names)
    if not proposed:
        return []
    rows = conn.execute(
        "SELECT * FROM documents WHERE publisher = ? AND doc_type = ? AND status != 'removed'",
        (publisher, doc_type),
    ).fetchall()
    matches = []
    for row in rows:
        if exclude_canonical_url and row["canonical_url"] == exclude_canonical_url:
            continue
        existing = model_name_set(json.loads(row["model_names"]))
        if not (proposed & existing):
            continue
        if title_similarity(title, row["title"]) >= TITLE_SIMILARITY_THRESHOLD:
            matches.append(row)
    return matches
