#!/usr/bin/env python3
"""Read a document the way the validator does, without storing anything.

  read_doc.py <url>  [--max-chars N] [--raw]   fetch + extract text, print to stdout
  read_doc.py <slug> [--max-chars N]           print the stored latest text of a document

The agent's own WebFetch is refused by several publishers (403) and rejects large
PDFs; the pipeline's fetcher (browser impersonation, 50 MB cap) reads them fine.
This exposes that fetcher plus the pipeline's text extraction as a read-only CLI
so documents get read before they are proposed. Nothing is written to data/ or
logs/: this is a read, not a capture. Exit 1 with a one-line reason on failure.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.extract import extract_text  # noqa: E402
from cardtrack.fetch import fetch  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402

DEFAULT_MAX_CHARS = 200_000


def _fail(reason: str) -> int:
    print(f"read_doc: {reason}", file=sys.stderr)
    return 1


def _emit(text: str, max_chars: int) -> None:
    if len(text) > max_chars:
        sys.stdout.write(text[:max_chars])
        sys.stdout.write(f"\n\n[read_doc: truncated at {max_chars} of {len(text)} chars; "
                         f"rerun with --max-chars {len(text)} for the rest]\n")
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def read_url(repo: Repo, url: str, max_chars: int, raw: bool) -> int:
    # Same caps and transport as the validator (cardtrack.propose._fetch_document),
    # minus its fetch-budget bookkeeping: fetch() itself touches neither the DB nor
    # the raw store, so reading here leaves no trace.
    caps = repo.settings.get("caps", {})
    result = fetch(
        url,
        max_bytes=int(caps.get("max_fetch_bytes", 52428800)),
        timeout=float(caps.get("fetch_timeout_seconds", 60)),
        allow_private_hosts=bool(repo.setting("fetch.allow_private_hosts", False)),
        impersonate_fallback=bool(repo.setting("fetch.impersonate_fallback", True)),
    )
    if not result.ok or result.content is None:
        if result.error:
            kind = "too large" if "max_fetch_bytes" in result.error else "error"
            return _fail(f"{kind}: {result.error} ({url})")
        return _fail(f"{result.outcome.replace('_', ' ')}: HTTP {result.status} ({url})")
    if raw:
        text = result.content.decode("utf-8", errors="replace")
        method = "raw"
    else:
        text, method = extract_text(result.content, result.content_type, result.url)
        if text is None:
            return _fail(f"extraction failed (method {method}, content-type "
                         f"{result.content_type}, {len(result.content)} bytes); "
                         "try --raw for the undecoded body")
    transport = "browser_impersonation" if result.impersonated else "direct"
    print(f"read_doc: HTTP {result.status} {len(result.content)} bytes via {transport}, "
          f"{method} extraction, {len(text)} chars"
          + (f", final url {result.url}" if result.url != url else ""), file=sys.stderr)
    _emit(text, max_chars)
    return 0


def read_slug(repo: Repo, slug: str, max_chars: int) -> int:
    if not repo.db_path.exists():
        return _fail(f"not found: no database at {repo.db_path}")
    # mode=ro: cardtrack.db.connect() runs schema DDL and journal pragmas, which is
    # a write path in disguise; a reader must not be able to touch the file.
    conn = sqlite3.connect(f"file:{repo.db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            """SELECT dv.text_path FROM document_versions dv
               JOIN documents d ON d.id = dv.document_id
               WHERE d.slug = ? ORDER BY dv.fetched_at DESC, dv.id DESC LIMIT 1""",
            (slug,)).fetchone()
    finally:
        conn.close()
    if row is None:
        return _fail(f"not found: no stored document with slug {slug!r} "
                     "(URLs must start with http:// or https://)")
    if not row["text_path"]:
        return _fail(f"no extracted text for {slug!r}: extraction failed at capture; "
                     "read the canonical URL instead")
    path = repo.root / row["text_path"]
    if not path.exists():
        return _fail(f"not found: {row['text_path']} is missing on disk")
    print(row["text_path"])
    _emit(path.read_text(encoding="utf-8"), max_chars)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target", help="http(s) URL to fetch, or the slug of a stored document")
    p.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS,
                   help=f"cap on printed characters (default {DEFAULT_MAX_CHARS}); the "
                        "output ends with a truncation marker when the cap is hit")
    p.add_argument("--raw", action="store_true",
                   help="URL mode: print the fetched body decoded as UTF-8 instead of "
                        "the extracted text (HTML source; not useful for PDFs)")
    p.add_argument("--root", help="repo root (default: auto-detected)")
    args = p.parse_args(argv)
    if args.max_chars <= 0:
        p.error("--max-chars must be positive")
    repo = Repo.locate(args.root)
    target = args.target.strip()
    if target.lower().startswith(("http://", "https://")):
        return read_url(repo, target, args.max_chars, args.raw)
    return read_slug(repo, target, args.max_chars)


if __name__ == "__main__":
    sys.exit(main())
