"""Phase A: deterministic monitoring, no LLM.
1) link-check all active/moved documents (3-strike dead rule; 403/429 never strike),
2) fingerprint-check a rotating subset (silent-update detection),
3) diff allowlisted publisher index pages into candidates.json for the agent.
"""

from __future__ import annotations

import json
import math
import sqlite3
from datetime import UTC, datetime, timedelta
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

import requests

from .canonical import canonicalize_url
from .db import connect
from .extract import extract_text, fingerprint_text, sha256_bytes
from .fetch import fetch, probe
from .identity import find_doc_by_url
from .propose import process_proposal
from .repo import Repo, utcnow

DEAD_STRIKES = 3
BLOCKED_ESCALATION_RUNS = 3
CANDIDATE_TTL_DAYS = 14
# Absolute backstop so the backlog stays bounded even if Phase B never succeeds.
CANDIDATE_HARD_TTL_DAYS = 8 * CANDIDATE_TTL_DAYS

NOISE_SUFFIXES = (
    ".css", ".js", ".mjs", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".otf", ".xml", ".rss", ".atom", ".json",
    ".mp4", ".webm", ".mp3", ".zip", ".tar", ".gz", ".webp", ".avif",
)


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []  # (href, text)
        self._current_href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._current_href = href
                self._text_parts = []

    def handle_data(self, data):
        if self._current_href is not None:
            self._text_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._current_href is not None:
            text = " ".join("".join(self._text_parts).split())[:200]
            self.links.append((self._current_href, text))
            self._current_href = None


def _record_check(conn: sqlite3.Connection, doc_id: int, run_id: str, check_type: str,
                  status: int | None, outcome: str, final_url: str | None = None,
                  byte_size: int | None = None) -> None:
    conn.execute(
        "INSERT INTO link_checks (document_id, run_id, ts, check_type, http_status, outcome, "
        "final_url, byte_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (doc_id, run_id, utcnow(), check_type, status, outcome, final_url, byte_size),
    )


def _recent_outcomes(conn: sqlite3.Connection, doc_id: int, check_type: str, n: int) -> list[str]:
    """Latest outcome per run for the last n runs that checked this doc (idempotent
    re-runs within one run_id count once)."""
    rows = conn.execute(
        """SELECT outcome FROM link_checks
           WHERE document_id = :d AND check_type = :t
             AND id IN (SELECT MAX(id) FROM link_checks
                        WHERE document_id = :d AND check_type = :t GROUP BY run_id)
           ORDER BY id DESC LIMIT :n""",
        {"d": doc_id, "t": check_type, "n": n},
    ).fetchall()
    return [r["outcome"] for r in rows]


def run_monitor(repo: Repo, run_id: str) -> dict:
    repo.ensure_dirs()
    conn = connect(repo.db_path)
    session = requests.Session()
    caps = repo.settings.get("caps", {})
    timeout = float(caps.get("fetch_timeout_seconds", 60))
    allow_private = bool(repo.setting("fetch.allow_private_hosts", False))
    impersonate = bool(repo.setting("fetch.impersonate_fallback", True))
    budget = int(caps.get("max_total_fetch_bytes_per_run", 524288000))
    bytes_used = 0

    summary: dict = {"run_id": run_id, "checked": 0, "ok": 0, "not_found": 0, "blocked": 0,
                     "errors": 0, "moved": 0, "marked_dead": 0, "fingerprint_checked": 0,
                     "new_versions": 0, "candidates": 0, "budget_exhausted": False}
    blocked_escalations: list[dict] = []

    try:
        # ---- 1. link check ----
        docs = conn.execute(
            "SELECT * FROM documents WHERE status IN ('active','moved','dead') ORDER BY id"
        ).fetchall()
        for doc in docs:
            result = probe(doc["canonical_url"], timeout=timeout,
                           allow_private_hosts=allow_private, session=session,
                           impersonate_fallback=impersonate)
            summary["checked"] += 1
            outcome = result.outcome if result.status is not None else "error"
            final_url = None
            if result.status is not None and result.permanent_redirect:
                # stable_url follows only permanent hops — a 302 to a CDN never
                # counts as a move
                try:
                    final_url = canonicalize_url(result.stable_url)
                except ValueError:
                    final_url = result.stable_url
                if outcome == "ok" and final_url != doc["canonical_url"]:
                    outcome = "redirect_permanent"
            _record_check(conn, doc["id"], run_id, "link", result.status, outcome, final_url)
            conn.commit()

            if doc["status"] == "dead":
                # self-heal: a dead doc that answers again goes back to active
                if outcome in ("ok", "redirect_permanent"):
                    process_proposal(repo, {
                        "action": "status_change", "slug": doc["slug"], "new": "active",
                        "justification": f"URL answers HTTP {result.status} again after "
                                         "being marked dead",
                        "evidence_urls": [doc["canonical_url"]],
                    }, run_id, actor="monitor", conn=conn)
                    summary["revived"] = summary.get("revived", 0) + 1
                continue

            if outcome in ("ok", "redirect_permanent"):
                summary["ok"] += 1
                conn.execute("UPDATE documents SET last_checked = ? WHERE id = ?",
                             (utcnow(), doc["id"]))
                conn.commit()
                if outcome == "redirect_permanent" and doc["status"] == "active":
                    process_proposal(repo, {
                        "action": "status_change", "slug": doc["slug"], "new": "moved",
                        "justification": f"Canonical URL permanently redirects to {final_url}",
                        "evidence_urls": [doc["canonical_url"]],
                    }, run_id, actor="monitor", conn=conn)
                    summary["moved"] += 1
            elif outcome == "not_found":
                summary["not_found"] += 1
                recent = _recent_outcomes(conn, doc["id"], "link", DEAD_STRIKES)
                if (len(recent) == DEAD_STRIKES
                        and all(o == "not_found" for o in recent)
                        and doc["status"] != "dead"):
                    process_proposal(repo, {
                        "action": "status_change", "slug": doc["slug"], "new": "dead",
                        "justification": f"HTTP {result.status} on {DEAD_STRIKES} "
                                         "consecutive runs (404-class only)",
                        "evidence_urls": [doc["canonical_url"]],
                    }, run_id, actor="monitor", conn=conn)
                    summary["marked_dead"] += 1
            elif outcome == "blocked":
                summary["blocked"] += 1
                recent = _recent_outcomes(conn, doc["id"], "link", BLOCKED_ESCALATION_RUNS)
                if len(recent) == BLOCKED_ESCALATION_RUNS and all(o == "blocked" for o in recent):
                    blocked_escalations.append({
                        "slug": doc["slug"], "url": doc["canonical_url"],
                        "http_status": result.status,
                        "note": f"blocked on {BLOCKED_ESCALATION_RUNS} consecutive runs; "
                                "confirm with agent-side fetch before any status change",
                    })
            else:
                summary["errors"] += 1

        # ---- 2. fingerprint rotation ----
        frac = float(repo.setting("cadence.fingerprint_fraction", 0.15))
        candidates_fp = conn.execute(
            """SELECT d.*, COALESCE(
                     (SELECT MAX(ts) FROM link_checks
                      WHERE document_id = d.id AND check_type = 'fingerprint'),
                     (SELECT MAX(fetched_at) FROM document_versions WHERE document_id = d.id),
                     '') AS last_fp
               FROM documents d WHERE d.status IN ('active','moved')
               ORDER BY last_fp ASC, d.id ASC""",
        ).fetchall()
        take = math.ceil(frac * len(candidates_fp)) if candidates_fp else 0
        for doc in candidates_fp[:take]:
            if bytes_used >= budget:
                summary["budget_exhausted"] = True
                break
            result = fetch(doc["canonical_url"],
                           max_bytes=int(caps.get("max_fetch_bytes", 52428800)),
                           timeout=timeout, allow_private_hosts=allow_private,
                           session=session, impersonate_fallback=impersonate)
            summary["fingerprint_checked"] += 1
            if not result.ok or result.content is None:
                _record_check(conn, doc["id"], run_id, "fingerprint", result.status,
                              result.outcome if result.status else "error")
                conn.commit()
                continue
            bytes_used += len(result.content)
            text, _method = extract_text(result.content, result.content_type,
                                         doc["canonical_url"])
            fp = (fingerprint_text(text, repo.fingerprint_ignore_patterns) if text
                  else sha256_bytes(result.content))
            known = conn.execute(
                "SELECT 1 FROM document_versions WHERE document_id = ? AND "
                "content_fingerprint = ?", (doc["id"], fp)).fetchone()
            _record_check(conn, doc["id"], run_id, "fingerprint", result.status,
                          "unchanged" if known else "changed",
                          byte_size=len(result.content))
            conn.commit()
            if known:
                conn.execute("UPDATE documents SET last_checked = ? WHERE id = ?",
                             (utcnow(), doc["id"]))
                conn.commit()
            else:
                res = process_proposal(repo, {
                    "action": "new_version", "url": doc["canonical_url"],
                    "justification": "Content fingerprint changed on scheduled re-fetch",
                    "evidence_urls": [doc["canonical_url"]],
                    "source_of_lead": "monitor",
                }, run_id, actor="monitor", conn=conn)
                if res.status == "written":
                    summary["new_versions"] += 1

        # ---- 3. index-page diff ----
        new_candidates: list[dict] = []
        for category in ("publishers", "evaluators"):
            for pub_key, entry in (repo.sources.get(category) or {}).items():
                for index_url in (entry or {}).get("index_urls") or []:
                    if bytes_used >= budget:
                        summary["budget_exhausted"] = True
                        break
                    result = fetch(index_url, max_bytes=10 * 1024 * 1024, timeout=timeout,
                                   allow_private_hosts=allow_private, session=session,
                                   impersonate_fallback=impersonate)
                    if not result.ok or result.content is None:
                        continue
                    bytes_used += len(result.content)
                    collector = _LinkCollector()
                    try:
                        collector.feed(result.content.decode("utf-8", errors="replace"))
                    except Exception:
                        continue
                    seen_this_page: set[str] = set()
                    for href, text in collector.links:
                        absolute = urljoin(result.url, href)
                        try:
                            canonical = canonicalize_url(absolute)
                        except ValueError:
                            continue
                        path = urlsplit(canonical).path.lower()
                        if path.endswith(NOISE_SUFFIXES):
                            continue
                        if canonical in seen_this_page:
                            continue
                        seen_this_page.add(canonical)
                        if canonical == canonicalize_url(index_url):
                            continue
                        if conn.execute("SELECT 1 FROM index_links WHERE url = ?",
                                        (canonical,)).fetchone():
                            continue
                        known_doc = find_doc_by_url(conn, canonical)
                        conn.execute(
                            "INSERT OR IGNORE INTO index_links "
                            "(url, index_url, publisher, link_text, first_seen) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (canonical, index_url, pub_key, text, utcnow()))
                        if not known_doc:
                            new_candidates.append({
                                "url": canonical, "publisher": pub_key,
                                "index_url": index_url, "link_text": text,
                            })
                    conn.commit()
        # merge with the previous backlog: candidates stay listed until they become
        # documents or expire (the agent may skip a day; discovery must not be lossy)
        repo.logs_dir.mkdir(parents=True, exist_ok=True)
        candidates_path = repo.logs_dir / "candidates.json"
        backlog: list[dict] = []
        if candidates_path.exists():
            try:
                backlog = json.loads(candidates_path.read_text()).get("candidates", [])
            except (json.JSONDecodeError, OSError):
                backlog = []
        cutoff = (datetime.now(UTC) - timedelta(days=CANDIDATE_TTL_DAYS)
                  ).strftime("%Y-%m-%dT%H:%M:%SZ")
        # A candidate only "had its chance" if the agent actually ran after it
        # appeared — expiring leads during an agent outage silently loses them
        # (this is how the Fable 5.1 announcement nearly slipped through in
        # 2026-09). run_daily.sh stamps this file after each successful Phase B;
        # a hard cap keeps the backlog bounded even if the agent never runs.
        # A total link-check outage (network down: everything errored) must not
        # burn TTL either — freeze expiry entirely on such runs.
        total_outage = summary["checked"] > 0 and summary["ok"] == 0
        hard_cutoff = (datetime.now(UTC) - timedelta(days=CANDIDATE_HARD_TTL_DAYS)
                       ).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            agent_last_success = (repo.logs_dir / ".agent_last_success"
                                  ).read_text().strip()
        except OSError:
            agent_last_success = ""
        merged: dict[str, dict] = {}
        for entry in backlog + new_candidates:
            url = entry.get("url")
            if not url or url in merged:
                continue
            entry.setdefault("first_seen", utcnow())
            if not total_outage and entry["first_seen"] < cutoff and (
                    agent_last_success > entry["first_seen"]
                    or entry["first_seen"] < hard_cutoff):
                continue
            if find_doc_by_url(conn, url):
                continue  # became a document; drop from backlog
            merged[url] = entry
        summary["candidates"] = len(merged)
        summary["candidates_new"] = len(new_candidates)
        (candidates_path).write_text(
            json.dumps({
                "run_id": run_id, "generated_at": utcnow(),
                "candidates": list(merged.values()),
                "blocked_escalations": blocked_escalations,
            }, ensure_ascii=False, indent=1),
            encoding="utf-8")
        conn.commit()

        # ---- 4. surface unsummarized versions to the agent ----
        summary["updated_docs"] = emit_updated_docs(repo, conn, run_id)
    finally:
        conn.close()
    return summary


UPDATED_DOCS_CAP = 20
DIFF_CHAR_CAP = 20000


def emit_updated_docs(repo: Repo, conn: sqlite3.Connection, run_id: str) -> int:
    """Write logs/updated_docs.json: every stored version that has a predecessor but
    no change_summary yet, with a capped unified diff on disk. The agent reads this,
    writes 1-3 factual sentences per entry via the annotate_version proposal. Listing
    ALL unsummarized versions (not just today's) makes the loop self-healing when the
    agent skips a day."""
    import difflib

    rows = conn.execute(
        """SELECT dv.id, dv.document_id, dv.fetched_at, dv.text_path, dv.change_summary,
                  d.slug
           FROM document_versions dv JOIN documents d ON d.id = dv.document_id
           WHERE d.status != 'removed'
           ORDER BY dv.document_id, dv.fetched_at, dv.id""").fetchall()
    by_doc: dict[int, list] = {}
    for r in rows:
        by_doc.setdefault(r["document_id"], []).append(r)

    entries = []
    diff_dir = repo.logs_dir / "version_diffs"
    for versions in by_doc.values():
        for prev, cur in zip(versions, versions[1:], strict=False):
            if cur["change_summary"] is not None:
                continue
            if not prev["text_path"] or not cur["text_path"]:
                continue
            prev_path = repo.root / prev["text_path"]
            cur_path = repo.root / cur["text_path"]
            if not prev_path.exists() or not cur_path.exists():
                continue
            a = prev_path.read_text(encoding="utf-8").splitlines()
            b = cur_path.read_text(encoding="utf-8").splitlines()
            diff_lines = list(difflib.unified_diff(a, b, lineterm="", n=2))
            added = sum(1 for line in diff_lines if line.startswith("+") and
                        not line.startswith("+++"))
            removed = sum(1 for line in diff_lines if line.startswith("-") and
                          not line.startswith("---"))
            diff_dir.mkdir(parents=True, exist_ok=True)
            diff_path = diff_dir / f"{cur['slug']}-v{cur['id']}.diff"
            diff_path.write_text("\n".join(diff_lines)[:DIFF_CHAR_CAP], encoding="utf-8")
            entries.append({
                "slug": cur["slug"], "version_id": cur["id"],
                "prev_version_id": prev["id"], "fetched_at": cur["fetched_at"],
                "added_lines": added, "removed_lines": removed,
                "diff_path": str(diff_path.relative_to(repo.root)),
            })
    entries.sort(key=lambda e: e["fetched_at"], reverse=True)
    entries = entries[:UPDATED_DOCS_CAP]
    (repo.logs_dir / "updated_docs.json").write_text(
        json.dumps({"run_id": run_id, "generated_at": utcnow(),
                    "updated_docs": entries}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    return len(entries)
