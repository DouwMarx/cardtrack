"""Changelog: append-only records; the commit message is a rendered view of them."""

from __future__ import annotations

import json
import sqlite3

from .repo import utcnow


def log(conn: sqlite3.Connection, run_id: str, action: str,
        document_id: int | None, detail: dict) -> int:
    cur = conn.execute(
        "INSERT INTO changelog (run_id, ts, action, document_id, detail) VALUES (?, ?, ?, ?, ?)",
        (run_id, utcnow(), action, document_id,
         json.dumps(detail, ensure_ascii=False, sort_keys=True)),
    )
    return cur.lastrowid


def entries_for_run(conn: sqlite3.Connection, run_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM changelog WHERE run_id = ? ORDER BY id", (run_id,)
    ).fetchall()


def render_commit_message(conn: sqlite3.Connection, run_id: str) -> str:
    """Human-readable summary of one run's changelog rows (the JSON stays canonical)."""
    entries = entries_for_run(conn, run_id)
    by_action: dict[str, list[dict]] = {}
    for row in entries:
        by_action.setdefault(row["action"], []).append(json.loads(row["detail"]))

    def slugs(action: str) -> list[str]:
        return [d.get("slug") or d.get("url") or "?" for d in by_action.get(action, [])]

    parts = []
    if "add" in by_action:
        parts.append(f"add {len(by_action['add'])}")
    if "new_version" in by_action:
        parts.append(f"{len(by_action['new_version'])} new version(s)")
    if "status_change" in by_action:
        parts.append(f"{len(by_action['status_change'])} status change(s)")
    if "field_update" in by_action:
        parts.append(f"{len(by_action['field_update'])} field update(s)")
    if "issue_resolved" in by_action:
        parts.append(f"{len(by_action['issue_resolved'])} issue(s) resolved")
    headline = f"cardtrack run {run_id}: " + (", ".join(parts) if parts else "no changes")

    lines = [headline, ""]
    for action in ("add", "new_version", "status_change", "field_update", "issue_resolved"):
        for slug in slugs(action):
            lines.append(f"- {action}: {slug}")
    rejects = len(by_action.get("reject", []))
    if rejects:
        lines.append(f"- rejects/issues filed: {rejects} (see changelog table)")
    return "\n".join(lines).strip() + "\n"
