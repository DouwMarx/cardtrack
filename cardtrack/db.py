"""SQLite schema and connection handling. Schema per spec §5, plus two append-only
fact tables (link_checks, index_links) that the monitor derives state from."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
  id               INTEGER PRIMARY KEY,
  slug             TEXT UNIQUE NOT NULL,
  title            TEXT NOT NULL,
  publisher        TEXT NOT NULL,
  doc_type         TEXT NOT NULL CHECK (doc_type IN
                     ('model_card','system_card','independent_eval','addendum','other')),
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
  notes            TEXT
);

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
CREATE VIEW IF NOT EXISTS latest_versions AS
SELECT dv.* FROM document_versions dv
WHERE dv.id = (
  SELECT id FROM document_versions
  WHERE document_id = dv.document_id
  ORDER BY fetched_at DESC, id DESC LIMIT 1
);

CREATE VIEW IF NOT EXISTS site_documents AS
SELECT d.*, lv.content_hash, lv.content_type, lv.fetched_at AS version_fetched_at,
       lv.content_fingerprint, lv.text_path,
       (SELECT COUNT(*) FROM document_versions WHERE document_id = d.id) AS version_count
FROM documents d
JOIN latest_versions lv ON lv.document_id = d.id
WHERE d.status != 'removed';
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # DELETE journal mode keeps the DB a single file (it is committed to git).
    conn.execute("PRAGMA journal_mode = DELETE")
    conn.executescript(SCHEMA)
    conn.executescript(VIEWS)
    conn.commit()
    return conn
