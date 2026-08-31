"""SQLite schema and connection handling: the catalog tables plus two append-only
fact tables (link_checks, index_links) that the monitor derives state from."""

from __future__ import annotations

import sqlite3
from pathlib import Path

# Single source of truth for the doc_type enum: the CHECK constraint is generated
# from it, and connect() rebuilds the documents table when a live DB's CHECK
# predates the current list (SQLite cannot ALTER a CHECK).
DOC_TYPES = ("model_card", "system_card", "independent_eval", "addendum",
             "access_policy", "other")

_DOC_TYPE_CHECK = ",".join(f"'{t}'" for t in DOC_TYPES)

# The documents DDL is its own template so the CHECK-migration can instantiate it
# under a temporary name (see _rebuild_documents_if_check_stale).
_DOCUMENTS_DDL = """
CREATE TABLE IF NOT EXISTS {name} (
  id               INTEGER PRIMARY KEY,
  slug             TEXT UNIQUE NOT NULL,
  title            TEXT NOT NULL,
  publisher        TEXT NOT NULL,
  doc_type         TEXT NOT NULL CHECK (doc_type IN (""" + _DOC_TYPE_CHECK + """)),
  is_independent   INTEGER NOT NULL DEFAULT 0,
  model_names      TEXT NOT NULL DEFAULT '[]',
  publication_date TEXT,
  canonical_url    TEXT UNIQUE NOT NULL,
  alt_urls         TEXT NOT NULL DEFAULT '[]',
  status           TEXT NOT NULL DEFAULT 'active' CHECK (status IN
                     ('active','moved','dead','superseded','removed')),
  first_seen       TEXT NOT NULL,
  last_checked     TEXT,
  last_changed     TEXT,
  source_of_lead   TEXT,
  notes            TEXT,
  safety_evals     INTEGER,           -- 1 = contains safety evals, 0 = none (required on add)
  openness         TEXT,              -- restricted | closed | open_weight_restrictive
                                      -- | open_weight_permissive | NULL = not
                                      -- model-specific / multi-class / undetermined
  risk_domains     TEXT NOT NULL DEFAULT '[]',  -- controlled vocabulary (config/criteria.yaml)
  related_urls     TEXT NOT NULL DEFAULT '[]'   -- list of url/kind/note objects: companions
                                                -- that are NOT this document (announcement,
                                                -- paper, ...)
);
"""

SCHEMA = _DOCUMENTS_DDL.format(name="documents") + """

CREATE TABLE IF NOT EXISTS document_versions (
  id                  INTEGER PRIMARY KEY,
  document_id         INTEGER NOT NULL REFERENCES documents(id),
  content_hash        TEXT NOT NULL,
  content_fingerprint TEXT NOT NULL,
  fetched_at          TEXT NOT NULL,
  content_type        TEXT,
  byte_size           INTEGER,
  raw_path            TEXT NOT NULL,
  text_path           TEXT,
  extraction          TEXT NOT NULL DEFAULT '{}',
  change_summary      TEXT,          -- agent-written "what changed vs the previous
                                     -- version" (validated via annotate_version)
  UNIQUE (document_id, content_fingerprint)
);

CREATE TABLE IF NOT EXISTS changelog (
  id           INTEGER PRIMARY KEY,
  run_id       TEXT NOT NULL,
  ts           TEXT NOT NULL,
  action       TEXT NOT NULL CHECK (action IN
                 ('add','new_version','status_change','field_update','reject','issue_resolved')),
  document_id  INTEGER,
  detail       TEXT NOT NULL
);

-- Append-only fact log of monitor checks; 'dead'/'blocked' state is derived from it.
CREATE TABLE IF NOT EXISTS link_checks (
  id           INTEGER PRIMARY KEY,
  document_id  INTEGER NOT NULL REFERENCES documents(id),
  run_id       TEXT NOT NULL,
  ts           TEXT NOT NULL,
  check_type   TEXT NOT NULL CHECK (check_type IN ('link','fingerprint')),
  http_status  INTEGER,
  outcome      TEXT NOT NULL,
  final_url    TEXT,
  byte_size    INTEGER            -- bytes fetched; feeds the rolling fetch budget
);

-- Every link ever seen on an allowlisted index page; "new candidate" = not in here.
CREATE TABLE IF NOT EXISTS index_links (
  url         TEXT PRIMARY KEY,
  index_url   TEXT NOT NULL,
  publisher   TEXT NOT NULL,
  link_text   TEXT,
  first_seen  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_versions_doc ON document_versions(document_id);
CREATE INDEX IF NOT EXISTS idx_changelog_run ON changelog(run_id);
CREATE INDEX IF NOT EXISTS idx_changelog_doc ON changelog(document_id);
CREATE INDEX IF NOT EXISTS idx_link_checks_doc ON link_checks(document_id, id);
"""

VIEWS = """
DROP VIEW IF EXISTS latest_versions;
DROP VIEW IF EXISTS site_documents;
CREATE VIEW latest_versions AS
SELECT dv.* FROM document_versions dv
WHERE dv.id = (
  SELECT id FROM document_versions
  WHERE document_id = dv.document_id
  ORDER BY fetched_at DESC, id DESC LIMIT 1
);

CREATE VIEW site_documents AS
SELECT d.*, lv.content_hash, lv.content_type, lv.fetched_at AS version_fetched_at,
       lv.content_fingerprint, lv.text_path,
       (SELECT COUNT(*) FROM document_versions WHERE document_id = d.id) AS version_count
FROM documents d
JOIN latest_versions lv ON lv.document_id = d.id
WHERE d.status != 'removed';
"""


def _rebuild_documents_if_check_stale(conn: sqlite3.Connection) -> None:
    """SQLite cannot ALTER a CHECK constraint. When the live table's doc_type CHECK
    predates DOC_TYPES, rebuild via the documented create-copy-drop-rename recipe.
    Order matters: renaming the OLD table would make SQLite rewrite the child
    tables' `REFERENCES documents` clauses to the temp name and leave them dangling
    after the drop — so the NEW table (which nothing references) is the one that
    gets renamed. Same rowids are copied, keeping the FK values valid. Idempotent:
    a current CHECK no-ops."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='documents'"
    ).fetchone()
    if row is None or all(f"'{t}'" in row["sql"] for t in DOC_TYPES):
        return
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        # snapshot pre-existing orphans so we only blame the rebuild for NEW ones
        before = len(conn.execute("PRAGMA foreign_key_check").fetchall())
        # views reference the table by name; drop them (connect() recreates them)
        conn.execute("DROP VIEW IF EXISTS latest_versions")
        conn.execute("DROP VIEW IF EXISTS site_documents")
        conn.execute("DROP TABLE IF EXISTS documents_new")
        conn.execute(_DOCUMENTS_DDL.format(name="documents_new"))
        new_cols = [r[1] for r in conn.execute("PRAGMA table_info(documents_new)")]
        old_cols = {r[1] for r in conn.execute("PRAGMA table_info(documents)")}
        col_list = ", ".join(c for c in new_cols if c in old_cols)
        conn.execute(
            f"INSERT INTO documents_new ({col_list}) SELECT {col_list} FROM documents")
        conn.execute("DROP TABLE documents")
        conn.execute("ALTER TABLE documents_new RENAME TO documents")
        # check BEFORE commit so a rebuild that broke FKs can still be rolled back
        after = len(conn.execute("PRAGMA foreign_key_check").fetchall())
        if after > before:
            conn.rollback()
            raise sqlite3.IntegrityError(
                f"documents rebuild introduced {after - before} dangling references")
        conn.commit()
    finally:
        conn.execute("PRAGMA foreign_keys = ON")


def connect(db_path: str | Path) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # DELETE journal mode keeps the DB a single file (it is committed to git).
    conn.execute("PRAGMA journal_mode = DELETE")
    conn.executescript(SCHEMA)
    # idempotent column migrations for DBs created before a column existed
    existing = {row[1] for row in conn.execute("PRAGMA table_info(documents)")}
    if "safety_evals" not in existing:
        conn.execute("ALTER TABLE documents ADD COLUMN safety_evals INTEGER")
    if "openness" not in existing:
        conn.execute("ALTER TABLE documents ADD COLUMN openness TEXT")
    if "risk_domains" not in existing:
        conn.execute(
            "ALTER TABLE documents ADD COLUMN risk_domains TEXT NOT NULL DEFAULT '[]'")
    if "related_urls" not in existing:
        conn.execute(
            "ALTER TABLE documents ADD COLUMN related_urls TEXT NOT NULL DEFAULT '[]'")
    existing_dv = {row[1] for row in conn.execute("PRAGMA table_info(document_versions)")}
    if "change_summary" not in existing_dv:
        conn.execute("ALTER TABLE document_versions ADD COLUMN change_summary TEXT")
    existing_lc = {row[1] for row in conn.execute("PRAGMA table_info(link_checks)")}
    if "byte_size" not in existing_lc:
        conn.execute("ALTER TABLE link_checks ADD COLUMN byte_size INTEGER")
    _rebuild_documents_if_check_stale(conn)
    conn.executescript(VIEWS)
    conn.commit()
    return conn
