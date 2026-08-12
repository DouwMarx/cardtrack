"""Static site builder: DB → site/ (index, search, per-doc pages, metadata.json),
then Pagefind indexing. The site consumes exports, never the live DB."""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import subprocess
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .db import connect
from .repo import Repo, utcnow

TEMPLATE_DIR = Path(__file__).parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(default=True, default_for_string=True),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def export_metadata(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM site_documents ORDER BY publication_date DESC, slug").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["model_names"] = json.loads(d["model_names"])
        d["alt_urls"] = json.loads(d["alt_urls"])
        for drop in ("id", "text_path", "notes"):
            d.pop(drop, None)
        out.append(d)
    return out


def _issue_url(gh_repo: str, doc: dict) -> str | None:
    if not gh_repo:
        return None
    title = quote(f"[data-error] {doc['slug']}")
    body = quote(
        f"Document: {doc['slug']}\nURL: {doc['canonical_url']}\n"
        f"Fingerprint: {doc.get('content_fingerprint', '')}\n\n"
        "What is wrong (wrong metadata, dead link, wrong version, should not be listed, ...)?\n"
    )
    return (f"https://github.com/{gh_repo}/issues/new"
            f"?labels=data-error&title={title}&body={body}")


def _publishers_map(repo: Repo) -> dict:
    """Org key → display_name/homepage/independent, for hyperlinking publishers."""
    out = {}
    for category, indep in (("publishers", False), ("evaluators", True)):
        for key, info in (repo.sources.get(category) or {}).items():
            out[key] = {
                "display_name": (info or {}).get("display_name", key),
                "homepage": (info or {}).get("homepage"),
                "independent": indep,
            }
    return out


def _doc_text(repo: Repo, text_path: str | None) -> str | None:
    if not text_path:
        return None
    path = repo.root / text_path
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def build_site(repo: Repo, run_pagefind: bool | None = None) -> dict:
    """Render everything. Returns a summary dict."""
    conn = connect(repo.db_path)
    try:
        return _build(repo, conn, run_pagefind)
    finally:
        conn.close()


def _build(repo: Repo, conn: sqlite3.Connection, run_pagefind: bool | None) -> dict:
    env = _env()
    site = repo.site_dir
    (site / "docs").mkdir(parents=True, exist_ok=True)
    (site / "data").mkdir(parents=True, exist_ok=True)

    gh_repo = repo.setting("github.repo") or ""
    site_title = repo.setting("site.title", "cardtrack")
    docs = export_metadata(conn)
    publishers = _publishers_map(repo)

    (site / "data" / "metadata.json").write_text(
        json.dumps({"generated_at": utcnow(), "publishers": publishers,
                    "documents": docs},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    # content-hash version tags for mutable assets: a deploy must never let a
    # cached old app.js/style.css meet new HTML (the URLs change instead)
    static_src = TEMPLATE_DIR / "static"
    asset_v = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:10]
               for f in static_src.iterdir() if f.is_file()}

    ctx_common = {"site_title": site_title, "gh_repo": gh_repo,
                  "generated_at": utcnow(), "asset_v": asset_v}

    # explicit cache policy; without it the CDN default (4 h browser TTL)
    # serves stale assets after every deploy
    (site / "_headers").write_text(
        "/*\n  Cache-Control: public, max-age=0, must-revalidate\n"
        "/pagefind/*\n  Cache-Control: public, max-age=86400\n",
        encoding="utf-8",
    )

    (site / "index.html").write_text(
        env.get_template("index.html.j2").render(**ctx_common, doc_count=len(docs)),
        encoding="utf-8")
    (site / "search.html").write_text(
        env.get_template("search.html.j2").render(**ctx_common), encoding="utf-8")
    (site / "about.html").write_text(
        env.get_template("about.html.j2").render(**ctx_common), encoding="utf-8")

    # per-document pages (including dead/removed-adjacent statuses; 'removed' docs are
    # excluded from site_documents, and their stale pages are pruned below)
    valid_pages = {"index.html", "search.html", "about.html"}
    for doc in docs:
        row = conn.execute("SELECT * FROM documents WHERE slug = ?", (doc["slug"],)).fetchone()
        versions = conn.execute(
            "SELECT * FROM document_versions WHERE document_id = ? "
            "ORDER BY fetched_at DESC, id DESC",
            (row["id"],)).fetchall()
        provenance = conn.execute(
            "SELECT * FROM changelog WHERE document_id = ? AND action != 'reject' ORDER BY id",
            (row["id"],)).fetchall()
        text = _doc_text(repo, versions[0]["text_path"] if versions else None)
        url_path = (doc.get("canonical_url") or "").lower().split("?")[0]
        source_kind = ("pdf" if "pdf" in (doc.get("content_type") or "").lower()
                       or url_path.endswith(".pdf") else "web")
        page = env.get_template("doc.html.j2").render(
            **ctx_common,
            doc=doc,
            source_kind=source_kind,
            publisher_home=(publishers.get(doc["publisher"]) or {}).get("homepage"),
            notes=row["notes"],
            versions=[dict(v) for v in versions],
            provenance=[{**dict(pr), "detail": json.loads(pr["detail"])} for pr in provenance],
            text=text,
            year=(doc.get("publication_date") or "")[:4] or "unknown",
            issue_url=_issue_url(gh_repo, doc),
        )
        (site / "docs" / f"{doc['slug']}.html").write_text(page, encoding="utf-8")
        valid_pages.add(f"docs/{doc['slug']}.html")

    # prune pages for removed/renamed docs
    for old in (site / "docs").glob("*.html"):
        if f"docs/{old.name}" not in valid_pages:
            old.unlink()

    # static assets
    static_src = TEMPLATE_DIR / "static"
    for asset in static_src.iterdir():
        shutil.copyfile(asset, site / asset.name)

    pagefind_ran = False
    if run_pagefind is None:
        run_pagefind = bool(repo.setting("site.run_pagefind", True))
    if run_pagefind and shutil.which("npx"):
        # fresh index dir: pagefind never prunes previous generations, and the
        # stale pf_meta/fragment files would otherwise accumulate in git forever
        shutil.rmtree(site / "pagefind", ignore_errors=True)
        proc = subprocess.run(
            ["npx", "-y", "pagefind", "--site", str(site)],
            capture_output=True, text=True, timeout=600,
        )
        pagefind_ran = proc.returncode == 0
        if not pagefind_ran:
            print(f"[build_site] pagefind failed:\n{proc.stderr[-2000:]}")
            # never ship a stale index as if it were current; the search page
            # degrades to an honest "index not built" notice
            shutil.rmtree(site / "pagefind", ignore_errors=True)

    return {"documents": len(docs), "pagefind": pagefind_ran, "site_dir": str(site)}
