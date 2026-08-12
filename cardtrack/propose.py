"""The write path. Every mutation — agent, monitor, or human — flows through
process_proposal(). It canonicalizes, dedups, fetches, fingerprints, applies criteria
and caps, and only then writes. Agent proposes; this code disposes.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, timedelta
from urllib.parse import urlsplit

from . import changelog as changelog_mod
from .canonical import canonicalize_url
from .db import connect
from .extract import (
    ext_for,
    extract_text,
    fingerprint_text,
    sha256_bytes,
    sniff_kind,
    write_raw_blob,
    write_text_file,
)
from .fetch import fetch
from .identity import derive_slug, find_doc_by_url, find_logical_duplicates
from .issues import file_issue
from .repo import Repo, utcnow

ACTIONS = {"add", "new_version", "status_change", "field_update"}
STATUSES = {"active", "moved", "dead", "superseded", "removed"}
DOC_TYPES = {"model_card", "system_card", "independent_eval", "addendum", "other"}
FIELD_UPDATE_FIELDS = {"title", "publication_date", "model_names", "notes", "canonical_url",
                       "safety_evals", "openness"}
OPENNESS_VALUES = {"closed", "open_weight_restrictive", "open_weight_permissive", "mixed"}


@dataclass
class ProposalResult:
    status: str  # written | duplicate | noop | rejected | issue_filed
    reason: str | None = None
    slug: str | None = None
    document_id: int | None = None
    version_id: int | None = None
    issue_ref: str | None = None
    run_id: str | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class _Ctx:
    """Per-call context bundling repo, connection, run bookkeeping."""

    def __init__(self, repo: Repo, conn: sqlite3.Connection, run_id: str, actor: str,
                 local_content: bytes | None = None,
                 local_content_type: str | None = None):
        self.repo = repo
        self.conn = conn
        self.run_id = run_id
        self.actor = actor
        self.local_content = local_content
        self.local_content_type = local_content_type


class _LocalContent:
    """Pseudo fetch result for operator-supplied bytes (bot-walled or offline docs).
    The URL is still recorded as canonical identity; provenance marks the transport."""

    def __init__(self, url: str, content: bytes, content_type: str | None):
        self.url = url
        self.stable_url = url
        self.ok = True
        self.status = None
        self.content = content
        self.content_type = content_type
        self.permanent_redirect = False
        self.impersonated = False
        self.manual = True


def process_proposal(
    repo: Repo,
    proposal: dict,
    run_id: str,
    actor: str = "agent",
    conn: sqlite3.Connection | None = None,
    local_content: bytes | None = None,
    local_content_type: str | None = None,
) -> ProposalResult:
    repo.ensure_dirs()
    own_conn = conn is None
    conn = conn or connect(repo.db_path)
    ctx = _Ctx(repo, conn, run_id, actor, local_content, local_content_type)
    try:
        result = _dispatch(ctx, proposal)
        conn.commit()
        return result
    except Exception:
        conn.rollback()
        raise
    finally:
        if own_conn:
            conn.close()


def _dispatch(ctx: _Ctx, proposal: dict) -> ProposalResult:
    err = _validate_schema(proposal)
    if err:
        return _reject(ctx, proposal, f"invalid_schema: {err}")
    action = proposal["action"]
    if action == "add":
        return _handle_add(ctx, proposal)
    if action == "new_version":
        return _handle_new_version(ctx, proposal)
    if action == "status_change":
        return _handle_status_change(ctx, proposal)
    return _handle_field_update(ctx, proposal)


# ---------- schema ----------

def _validate_schema(p: dict) -> str | None:
    if not isinstance(p, dict):
        return "proposal must be a JSON object"
    action = p.get("action")
    if action not in ACTIONS:
        return f"action must be one of {sorted(ACTIONS)}"
    if not isinstance(p.get("justification"), str) or not p["justification"].strip():
        return "justification (non-empty string) is required"
    ev = p.get("evidence_urls")
    if not isinstance(ev, list) or not all(isinstance(u, str) for u in ev):
        return "evidence_urls (list of strings) is required"
    if action in ("add", "new_version"):
        if not isinstance(p.get("url"), str) or not p["url"].strip():
            return "url is required"
    if action == "add":
        if not isinstance(p.get("title"), str) or not p["title"].strip():
            return "title is required"
        if not isinstance(p.get("publisher"), str) or not p["publisher"].strip():
            return "publisher is required"
        if p.get("doc_type") not in DOC_TYPES:
            return f"doc_type must be one of {sorted(DOC_TYPES)}"
        mn = p.get("model_names")
        if not isinstance(mn, list) or not all(isinstance(m, str) for m in mn):
            return "model_names (list of strings) is required"
        pd = p.get("publication_date")
        if pd is not None and _parse_date(pd) is None:
            return "publication_date must be ISO 8601 (YYYY-MM-DD) or null"
        if not isinstance(p.get("criteria", {}), dict):
            return "criteria must be an object"
        if not isinstance(p.get("soft", {}), dict):
            return "soft (criteria) must be an object"
    if action == "status_change":
        if not p.get("slug"):
            return "slug is required"
        if p.get("new") not in STATUSES:
            return f"new (status) must be one of {sorted(STATUSES)}"
    if action == "field_update":
        if not p.get("slug"):
            return "slug is required"
        if p.get("field") not in FIELD_UPDATE_FIELDS:
            return f"field must be one of {sorted(FIELD_UPDATE_FIELDS)}"
        if "new" not in p:
            return "new (value) is required"
    return None


def _parse_date(value) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None


# ---------- shared helpers ----------

def _reject(ctx: _Ctx, proposal: dict, reason: str,
            document_id: int | None = None, extra: dict | None = None) -> ProposalResult:
    detail = {"proposal": proposal, "reason": reason, "actor": ctx.actor,
              "outcome": "rejected", **(extra or {})}
    changelog_mod.log(ctx.conn, ctx.run_id, "reject", document_id, detail)
    return ProposalResult(status="rejected", reason=reason,
                          document_id=document_id, run_id=ctx.run_id)


def _file_issue(ctx: _Ctx, proposal: dict, reason: str, title: str, body: str,
                labels: list[str], document_id: int | None = None,
                extra: dict | None = None) -> ProposalResult:
    ref = file_issue(ctx.repo, title, body, labels)
    detail = {"proposal": proposal, "reason": reason, "actor": ctx.actor,
              "outcome": "issue_filed", "issue_ref": ref, **(extra or {})}
    changelog_mod.log(ctx.conn, ctx.run_id, "reject", document_id, detail)
    return ProposalResult(status="issue_filed", reason=reason, issue_ref=ref,
                          document_id=document_id, run_id=ctx.run_id)


CAP_WINDOW_HOURS = 24


def _window_cutoff() -> str:
    return (datetime.now(UTC) - timedelta(hours=CAP_WINDOW_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _count_recent_actions(conn: sqlite3.Connection, action: str) -> int:
    """Cap accounting over a rolling window keyed on the changelog's own timestamps.
    Deliberately NOT keyed on run_id: run ids are caller-supplied, and caps must be
    guaranteed by deterministic code, never by caller diligence."""
    return conn.execute(
        "SELECT COUNT(*) FROM changelog WHERE action = ? AND ts > ?",
        (action, _window_cutoff()),
    ).fetchone()[0]


def _recent_fetched_bytes(conn: sqlite3.Connection) -> int:
    """Bytes fetched in the rolling window: every changelog detail that carries a
    byte_size (writes, post-fetch rejects/issues) plus monitor/no-op fetches logged
    in link_checks. Persistent across the separate CLI processes the agent spawns."""
    cutoff = _window_cutoff()
    total = 0
    for row in conn.execute("SELECT detail FROM changelog WHERE ts > ?", (cutoff,)):
        try:
            b = json.loads(row["detail"]).get("byte_size")
        except json.JSONDecodeError:
            continue
        if isinstance(b, int):
            total += b
    row = conn.execute(
        "SELECT COALESCE(SUM(byte_size), 0) FROM link_checks WHERE ts > ?", (cutoff,)
    ).fetchone()
    return total + row[0]


def _fetch_document(ctx: _Ctx, url: str) -> tuple[object | None, str | None]:
    """Fetch with caps. Returns (FetchResult, error_reason)."""
    caps = ctx.repo.settings.get("caps", {})
    max_bytes = int(caps.get("max_fetch_bytes", 52428800))
    budget = int(caps.get("max_total_fetch_bytes_per_run", 524288000))
    if _recent_fetched_bytes(ctx.conn) >= budget:
        return None, "fetch_budget_exceeded"
    result = fetch(
        url,
        max_bytes=max_bytes,
        timeout=float(caps.get("fetch_timeout_seconds", 60)),
        allow_private_hosts=bool(ctx.repo.setting("fetch.allow_private_hosts", False)),
        impersonate_fallback=bool(ctx.repo.setting("fetch.impersonate_fallback", True)),
    )
    if not result.ok or result.content is None:
        why = result.error or f"HTTP {result.status}"
        return None, f"document_retrievable=false: {why}"
    return result, None


# Shared-hosting suffixes where a same-registrable-domain match proves nothing.
SHARED_SUFFIXES = {"github.io", "pages.dev", "netlify.app", "vercel.app", "web.app"}


def _host_known_for_publisher(ctx: _Ctx, publisher: str, url: str) -> bool:
    """Is this URL's host already associated with the publisher — exactly, or via a
    non-shared registrable domain — through sources.yaml index_urls or existing docs?"""
    host = (urlsplit(url).hostname or "").lower()
    if not host:
        return False
    known: set[str] = set()
    info = ctx.repo.publisher_info(publisher)
    if info:
        for index_url in (info[0].get("index_urls") or []):
            h = (urlsplit(index_url).hostname or "").lower()
            if h:
                known.add(h)
    for row in ctx.conn.execute(
            "SELECT canonical_url, alt_urls FROM documents WHERE publisher = ?", (publisher,)):
        for u in [row["canonical_url"], *json.loads(row["alt_urls"])]:
            h = (urlsplit(u).hostname or "").lower()
            if h:
                known.add(h)
    if host in known:
        return True
    apex = ".".join(host.rsplit(".", 2)[-2:])
    if apex in SHARED_SUFFIXES:
        return False
    return any(k == apex or k.endswith("." + apex) for k in known)


def _content_identity(content: bytes, content_type: str | None, url: str):
    """Returns (content_hash, fingerprint, text, kind, method)."""
    content_hash = sha256_bytes(content)
    kind = sniff_kind(content, content_type, url)
    text, method = extract_text(content, content_type, url)
    fp = fingerprint_text(text) if text else content_hash  # extraction failed → raw hash
    return content_hash, fp, text, kind, method


def _insert_version(ctx: _Ctx, document_id: int, fetched, content_hash: str,
                    fp: str, text: str | None, kind: str, method: str = "") -> int:
    raw_path = write_raw_blob(ctx.repo.raw_dir, content_hash, ext_for(kind), fetched.content)
    text_path = None
    if text is not None:
        text_path = write_text_file(ctx.repo.text_dir, content_hash, text)
    extraction = {"method": method or kind}
    if getattr(fetched, "manual", False):
        extraction["transport"] = "manual_upload"
    elif getattr(fetched, "impersonated", False):
        extraction["transport"] = "browser_impersonation"
    else:
        extraction["transport"] = "direct"
    try:
        import trafilatura

        extraction["trafilatura"] = trafilatura.__version__
    except Exception:
        pass
    cur = ctx.conn.execute(
        """INSERT INTO document_versions
           (document_id, content_hash, content_fingerprint, fetched_at, content_type,
            byte_size, raw_path, text_path, extraction)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (document_id, content_hash, fp, utcnow(), fetched.content_type,
         len(fetched.content), _relpath(ctx.repo, raw_path),
         _relpath(ctx.repo, text_path) if text_path else None,
         json.dumps(extraction)),
    )
    return cur.lastrowid


def _relpath(repo: Repo, path) -> str:
    return str(path.relative_to(repo.root))


# ---------- add ----------

def _handle_add(ctx: _Ctx, p: dict) -> ProposalResult:
    repo, conn = ctx.repo, ctx.conn

    info = repo.publisher_info(p["publisher"])
    if info is None:
        return _reject(ctx, p, f"publisher_on_allowlist=false: {p['publisher']!r} "
                               "not in config/sources.yaml")
    pub_entry, category = info
    tier = int(pub_entry.get("tier", 2))
    is_independent = 1 if category == "evaluators" else 0

    try:
        canonical = canonicalize_url(p["url"])
    except ValueError as e:
        return _reject(ctx, p, f"url_invalid: {e}")

    existing = find_doc_by_url(conn, canonical)
    if existing:
        return _version_check(ctx, p, existing, routed_from="add")

    caps = repo.settings.get("caps", {})
    if _count_recent_actions(conn, "add") >= int(
            caps.get("max_new_documents_per_run", 15)):
        return _reject(ctx, p, f"cap_exceeded: max_new_documents_per_run "
                               f"(rolling {CAP_WINDOW_HOURS}h)")


    if ctx.local_content is not None:
        fetched = _LocalContent(canonical, ctx.local_content, ctx.local_content_type)
    else:
        fetched, err = _fetch_document(ctx, p["url"])
        if err:
            return _reject(ctx, p, err)

    final_canonical = canonicalize_url(fetched.stable_url)
    if final_canonical != canonical:
        existing = find_doc_by_url(conn, final_canonical)
        if existing:
            return _version_check(ctx, p, existing, routed_from="add",
                                  prefetched=fetched)
    canonical = final_canonical

    content_hash, fp, text, kind, method = _content_identity(
        fetched.content, fetched.content_type, canonical)

    # Content identity: identical extracted text already stored under another document
    # (mirror / same doc at a different URL) → needs_review, never an automatic merge.
    other = conn.execute(
        """SELECT d.slug, d.canonical_url FROM document_versions dv
           JOIN documents d ON d.id = dv.document_id
           WHERE dv.content_fingerprint = ? LIMIT 1""", (fp,)
    ).fetchone()
    nbytes = {"byte_size": len(fetched.content)}
    if other:
        return _file_issue(
            ctx, p, f"content_duplicate_of:{other['slug']}",
            title=f"needs-review: proposed URL duplicates content of {other['slug']}",
            body=_issue_body(ctx, p, [
                f"Proposed URL: {canonical}",
                f"Existing document: {other['slug']} ({other['canonical_url']})",
                "Extracted-text fingerprints are identical. Likely a mirror or moved copy.",
            ]),
            labels=["needs-review"], extra=nbytes,
        )

    # Validator-checked criteria (config/criteria.yaml)
    vc = repo.criteria.get("validator_checked", {})
    floor = _parse_date(vc.get("min_publication_date", "0001-01-01"))
    pub_date = _parse_date(p.get("publication_date")) if p.get("publication_date") else None
    # Unknown date: admit and flag (detect-and-revert beats pre-approval) — the row carries
    # date_unknown provenance and the site shows "unknown"; curation can fix or
    # remove later. The floor still rejects documents with KNOWN pre-floor dates.
    date_unknown = p.get("publication_date") is None
    if floor and pub_date and pub_date < floor:
        return _reject(ctx, p, f"before_min_publication_date: {pub_date} < {floor}",
                       extra=nbytes)

    # Agent-attested criteria: all must be asserted true; anything else is "uncertain",
    # and the prime directive for uncertain is an issue, not a row.
    attested = repo.criteria.get("agent_attested", {})
    asserted = p.get("criteria", {})
    missing = [k for k in attested if asserted.get(k) is not True]
    if missing:
        return _file_issue(
            ctx, p, f"criteria_not_attested: {','.join(missing)}",
            title=f"needs-review: unattested criteria for {p['title'][:80]!r}",
            body=_issue_body(ctx, p, [f"URL: {canonical}",
                                      f"Criteria not asserted true: {', '.join(missing)}"]),
            labels=["needs-review"], extra=nbytes,
        )

    # Tier is provenance metadata, not a write gate (policy change 2026-08-10:
    # the allowlist is the gate; issues are for exclusion, not inclusion).
    dups = find_logical_duplicates(conn, p["publisher"], p["doc_type"], p["model_names"],
                                   title=p["title"],
                                   exclude_canonical_url=canonical)
    if dups:
        return _file_issue(
            ctx, p, f"logical_duplicate_of:{dups[0]['slug']}",
            title=f"needs-review: possible duplicate of {dups[0]['slug']}",
            body=_issue_body(ctx, p, [
                f"Proposed: {p['title']!r} at {canonical}",
                f"Existing: {dups[0]['slug']} at {dups[0]['canonical_url']}",
                "Same publisher + doc_type + overlapping model names at a different URL.",
            ]),
            labels=["needs-review"], extra=nbytes,
        )

    # All gates passed → write.
    openness = p.get("openness")
    if openness is not None and openness not in OPENNESS_VALUES:
        return _reject(ctx, p, "invalid_value: openness must be one of "
                       "closed|open_weight_restrictive|open_weight_permissive|mixed")
    slug = derive_slug(conn, p["publisher"], p["model_names"], p["doc_type"])
    now = utcnow()
    safety = p.get("soft", {}).get("has_safety_evals")
    safety_db = None if safety is None else (1 if safety else 0)
    cur = conn.execute(
        """INSERT INTO documents
           (slug, title, publisher, doc_type, is_independent, model_names,
            publication_date, canonical_url, alt_urls, status, first_seen,
            last_checked, last_changed, source_of_lead, notes, safety_evals, openness)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]', 'active', ?, ?, ?, ?, ?, ?, ?)""",
        (slug, p["title"].strip(), p["publisher"], p["doc_type"], is_independent,
         json.dumps(sorted(p["model_names"])), p.get("publication_date"), canonical,
         now, now, now, p.get("source_of_lead", "manual"), p.get("notes"), safety_db,
         openness),
    )
    document_id = cur.lastrowid
    version_id = _insert_version(ctx, document_id, fetched, content_hash, fp, text, kind,
                                 method)

    detail = {
        **p, "slug": slug, "canonical_url": canonical, "outcome": "written",
        "actor": ctx.actor, "tier": tier, "is_independent": is_independent,
        "content_hash": content_hash, "content_fingerprint": fp,
        "byte_size": len(fetched.content), "content_type": fetched.content_type,
        "validator_criteria": {
            "publisher_on_allowlist": True, "document_retrievable": True,
            "min_publication_date": not date_unknown,
        },
        **({"date_unknown": True} if date_unknown else {}),
    }
    changelog_mod.log(conn, ctx.run_id, "add", document_id, detail)
    return ProposalResult(status="written", slug=slug, document_id=document_id,
                          version_id=version_id, run_id=ctx.run_id)


def _issue_body(ctx: _Ctx, p: dict, lines: list[str]) -> str:
    return "\n".join([
        *lines, "",
        f"Justification: {p.get('justification', '')}",
        f"Evidence: {', '.join(p.get('evidence_urls', []))}",
        f"Source of lead: {p.get('source_of_lead', 'unknown')}",
        f"Run: {ctx.run_id} (actor: {ctx.actor})",
    ])


# ---------- new_version ----------

def _handle_new_version(ctx: _Ctx, p: dict) -> ProposalResult:
    try:
        canonical = canonicalize_url(p["url"])
    except ValueError as e:
        return _reject(ctx, p, f"url_invalid: {e}")
    doc = find_doc_by_url(ctx.conn, canonical)
    if doc is None:
        return _reject(ctx, p, "unknown_document: no document with this URL; use action=add")
    return _version_check(ctx, p, doc)


def _version_check(ctx: _Ctx, p: dict, doc: sqlite3.Row, routed_from: str | None = None,
                   prefetched=None) -> ProposalResult:
    """Fetch a known document (always at its canonical URL, never a caller-supplied
    alias); same fingerprint → no-op, new → version row."""
    conn, repo = ctx.conn, ctx.repo
    caps = repo.settings.get("caps", {})

    fetched = prefetched
    if fetched is None and ctx.local_content is not None:
        fetched = _LocalContent(doc["canonical_url"], ctx.local_content,
                                ctx.local_content_type)
    if fetched is None:
        fetched, err = _fetch_document(ctx, doc["canonical_url"])
        if err:
            return _reject(ctx, p, err, document_id=doc["id"])

    content_hash, fp, text, kind, method = _content_identity(
        fetched.content, fetched.content_type, doc["canonical_url"])

    # Byte identity first: identical raw bytes can never be a
    # new version, even if extraction wobbles across environments.
    known = conn.execute(
        "SELECT id FROM document_versions WHERE document_id = ? AND "
        "(content_hash = ? OR content_fingerprint = ?)",
        (doc["id"], content_hash, fp),
    ).fetchone()
    now = utcnow()
    if known:
        conn.execute("UPDATE documents SET last_checked = ? WHERE id = ?", (now, doc["id"]))
        # no changelog row for a no-op, but the fetch still counts toward the budget
        conn.execute(
            "INSERT INTO link_checks (document_id, run_id, ts, check_type, http_status, "
            "outcome, byte_size) VALUES (?, ?, ?, 'fingerprint', ?, 'unchanged', ?)",
            (doc["id"], ctx.run_id, now, fetched.status, len(fetched.content)),
        )
        return ProposalResult(status="duplicate", reason="fingerprint_already_stored",
                              slug=doc["slug"], document_id=doc["id"],
                              version_id=known["id"], run_id=ctx.run_id)

    if _count_recent_actions(conn, "new_version") >= int(
            caps.get("max_new_versions_per_run", 30)):
        return _reject(ctx, p, f"cap_exceeded: max_new_versions_per_run "
                               f"(rolling {CAP_WINDOW_HOURS}h)",
                       document_id=doc["id"],
                       extra={"byte_size": len(fetched.content)})

    version_id = _insert_version(ctx, doc["id"], fetched, content_hash, fp, text, kind,
                                 method)
    conn.execute(
        "UPDATE documents SET last_checked = ?, last_changed = ? WHERE id = ?",
        (now, now, doc["id"]),
    )
    detail = {
        **p, "slug": doc["slug"], "outcome": "written", "actor": ctx.actor,
        "content_hash": content_hash, "content_fingerprint": fp,
        "byte_size": len(fetched.content), "content_type": fetched.content_type,
        **({"routed_from": routed_from} if routed_from else {}),
    }
    changelog_mod.log(conn, ctx.run_id, "new_version", doc["id"], detail)
    return ProposalResult(status="written", slug=doc["slug"], document_id=doc["id"],
                          version_id=version_id, run_id=ctx.run_id)


# ---------- status_change ----------

def _handle_status_change(ctx: _Ctx, p: dict) -> ProposalResult:
    conn = ctx.conn
    doc = conn.execute("SELECT * FROM documents WHERE slug = ?", (p["slug"],)).fetchone()
    if doc is None:
        return _reject(ctx, p, f"unknown_document: no document with slug {p['slug']!r}")
    old = doc["status"]
    new = p["new"]
    if old == new:
        return ProposalResult(status="noop", reason=f"status already {new!r}",
                              slug=doc["slug"], document_id=doc["id"], run_id=ctx.run_id)
    now = utcnow()
    conn.execute(
        "UPDATE documents SET status = ?, last_checked = ?, last_changed = ? WHERE id = ?",
        (new, now, now, doc["id"]),
    )
    detail = {**p, "old": old, "outcome": "written", "actor": ctx.actor}
    changelog_mod.log(conn, ctx.run_id, "status_change", doc["id"], detail)
    return ProposalResult(status="written", slug=doc["slug"], document_id=doc["id"],
                          run_id=ctx.run_id)


# ---------- field_update ----------

def _handle_field_update(ctx: _Ctx, p: dict) -> ProposalResult:
    conn = ctx.conn
    doc = conn.execute("SELECT * FROM documents WHERE slug = ?", (p["slug"],)).fetchone()
    if doc is None:
        return _reject(ctx, p, f"unknown_document: no document with slug {p['slug']!r}")
    field, new = p["field"], p["new"]

    current = doc[field]
    if field == "model_names":
        if not isinstance(new, list) or not all(isinstance(m, str) for m in new):
            return _reject(ctx, p, "invalid_value: model_names must be a list of strings",
                           document_id=doc["id"])
        current_cmp: object = json.loads(current)
        new_db = json.dumps(sorted(new))
    elif field == "publication_date":
        if new is not None and _parse_date(new) is None:
            return _reject(ctx, p, "invalid_value: publication_date must be ISO 8601",
                           document_id=doc["id"])
        floor = _parse_date(
            ctx.repo.criteria.get("validator_checked", {}).get("min_publication_date", ""))
        if new is not None and floor and _parse_date(new) < floor:
            return _reject(ctx, p, f"before_min_publication_date: {new} < {floor}; if the "
                                   "document is genuinely out of scope, propose "
                                   "status_change to 'removed' instead",
                           document_id=doc["id"])
        current_cmp, new_db = current, new
    elif field == "canonical_url":
        if not isinstance(new, str):
            return _reject(ctx, p, "invalid_value: canonical_url must be a string",
                           document_id=doc["id"])
        try:
            new_db = canonicalize_url(new)
        except ValueError as e:
            return _reject(ctx, p, f"url_invalid: {e}", document_id=doc["id"])
        owner = find_doc_by_url(conn, new_db)
        if owner and owner["id"] != doc["id"]:
            return _reject(ctx, p, f"url_conflict: {new_db} belongs to {owner['slug']}",
                           document_id=doc["id"])
        # Repointing the public "source" link is the most sensitive field there is.
        # Deterministic gate: the new host must already be known for this publisher,
        # AND the content served there must match a stored version fingerprint.
        # Anything else → needs-review issue, never a write.
        if not _host_known_for_publisher(ctx, doc["publisher"], new_db):
            return _file_issue(
                ctx, p, "canonical_url_host_unknown",
                title=f"needs-review: canonical_url move to unknown host for {doc['slug']}",
                body=_issue_body(ctx, p, [
                    f"Document: {doc['slug']} (publisher {doc['publisher']})",
                    f"Current: {doc['canonical_url']}", f"Proposed: {new_db}",
                    "The proposed host is not among this publisher's known hosts "
                    "(sources.yaml index_urls + existing document URLs).",
                ]), labels=["needs-review"], document_id=doc["id"])
        fetched, err = _fetch_document(ctx, new_db)
        if err:
            return _reject(ctx, p, err, document_id=doc["id"])
        _hash, fp, _text, _kind, _m = _content_identity(
            fetched.content, fetched.content_type, new_db)
        match = conn.execute(
            "SELECT 1 FROM document_versions WHERE document_id = ? AND "
            "content_fingerprint = ?", (doc["id"], fp)).fetchone()
        if not match:
            return _file_issue(
                ctx, p, "canonical_url_content_mismatch",
                title=f"needs-review: canonical_url move with different content "
                      f"for {doc['slug']}",
                body=_issue_body(ctx, p, [
                    f"Document: {doc['slug']}", f"Proposed URL: {new_db}",
                    "Content at the proposed URL matches no stored version of this "
                    "document (it may be a newer revision — verify by hand).",
                ]), labels=["needs-review"], document_id=doc["id"],
                extra={"byte_size": len(fetched.content)})
        current_cmp = current
    elif field == "safety_evals":
        if new not in (None, True, False, 0, 1):
            return _reject(ctx, p, "invalid_value: safety_evals must be true/false/null",
                           document_id=doc["id"])
        current_cmp = current
        new_db = None if new is None else int(bool(new))
    elif field == "openness":
        if new is not None and new not in OPENNESS_VALUES:
            return _reject(ctx, p, "invalid_value: openness must be one of "
                           "closed|open_weight_restrictive|open_weight_permissive|mixed|null",
                           document_id=doc["id"])
        current_cmp, new_db = current, new
    else:  # title, notes
        if field == "title" and (not isinstance(new, str) or not new.strip()):
            return _reject(ctx, p, "invalid_value: title must be a non-empty string",
                           document_id=doc["id"])
        if new is not None and not isinstance(new, str):
            return _reject(ctx, p, f"invalid_value: {field} must be a string",
                           document_id=doc["id"])
        current_cmp, new_db = current, new

    if "old" in p:
        old_given = p["old"]
        if field == "model_names" and isinstance(old_given, list):
            stale = sorted(old_given) != sorted(current_cmp)
        else:
            stale = old_given != current_cmp
        if stale:
            return _reject(ctx, p, f"stale_old_value: current {field} is {current_cmp!r}",
                           document_id=doc["id"])

    now = utcnow()
    if field == "canonical_url":
        alts = json.loads(doc["alt_urls"])
        if doc["canonical_url"] not in alts:
            alts.append(doc["canonical_url"])
        conn.execute(
            "UPDATE documents SET canonical_url = ?, alt_urls = ?, last_checked = ?, "
            "last_changed = ? WHERE id = ?",
            (new_db, json.dumps(alts), now, now, doc["id"]),
        )
    else:
        conn.execute(
            f"UPDATE documents SET {field} = ?, last_checked = ?, last_changed = ? WHERE id = ?",
            (new_db, now, now, doc["id"]),
        )
    old_rec = current_cmp if isinstance(current_cmp, str | int | None) else list(current_cmp)
    detail = {**p, "old": old_rec,
              "new": new_db if field != "model_names" else sorted(new),
              "outcome": "written", "actor": ctx.actor}
    changelog_mod.log(conn, ctx.run_id, "field_update", doc["id"], detail)
    return ProposalResult(status="written", slug=doc["slug"], document_id=doc["id"],
                          run_id=ctx.run_id)
