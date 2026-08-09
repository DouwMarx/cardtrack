# cardtrack — Design Specification (MVP)

*Working name `cardtrack`; rename freely. Status: draft for implementation. Scale target: ~1,000–5,000 documents.*

A continuously maintained, publicly browsable database of AI model documentation — first-party model/system cards **and** independent evaluation reports — with change tracking, provenance, and full-text search. Curated daily by an LLM agent operating behind deterministic guardrails; published as a static site.

---

## 1. Scope

**In scope (MVP)**
- Cataloging documents: metadata rows for model cards, system cards, independent evaluations, addenda. Scope starts at documents published 2026-01-01 or later (configurable).
- Archiving: immutable raw bytes of every observed version (PDF and HTML), stored locally only; never committed to git, never published.
- Change tracking: detect new versions (content fingerprint change), dead links, moved documents.
- Text extraction: powers search, change detection, and the published per-document text. Originals are linked, never re-hosted.
- Static site: filterable/sortable table, per-document pages, scoped search (metadata vs full text), CSV export, issue reporting.
- Daily autonomous run: deterministic monitoring + agent discovery, auto-merged writes, structured changelog.
- Public error-reporting loop via GitHub issues, processed by the agent.

**Out of scope (MVP)** — see §14 roadmap
- Structured field extraction (eval scores, benchmark tables, model comparisons).
- A `models` table / model-centric views. Documents are the primary entity; `model_names` is a filterable text field.
- GitHub Actions execution (designed for, not enabled; runs locally under cron first).
- Any server-side component (no D1, no Workers).

---

## 2. Design principles

These are the invariants. Implementation details may change; these should not.

1. **Agent proposes, code disposes.** The agent never touches the database, the raw store, or git directly. All writes flow through one validated CLI tool with veto power. Correctness properties (no duplicates, valid schema, caps) are guaranteed by deterministic code, never by agent diligence.
2. **Deterministic core, agentic edge.** Everything that can be plain Python is plain Python (link checks, hash comparison, index-page diffing, site build). The LLM is used only where judgment is required: discovery of unknown sources, credibility assessment, metadata fill.
3. **Identity is layered.** Byte identity (SHA-256 of raw bytes; names the blob), content identity (SHA-256 of extracted text; detects real change), location identity (canonical URL), logical identity (publisher + doc_type + models). New content at a known logical identity = new *version*, not new *document*.
4. **Facts are immutable; state is derived.** Version rows and changelog entries are append-only. "Latest", "active" etc. are SQL views, never mutated flags. Deletion is a status change (soft delete), never row removal.
5. **Detect-and-revert over prevent.** No human pre-merge review. Instead: conservative criteria, per-run caps, tiered trust, public provenance on every entry, and cheap reversal (one `git revert`).
6. **Idempotent runs.** Re-running after a crash or double-trigger is a no-op. All writes are upserts keyed on canonical URL / content hash.
7. **Grow in rows, not columns.** Future data (eval scores, new benchmarks) must land as rows in new tables or JSON, never as schema migrations triggered by content.
8. **Raw bytes are the insurance policy.** Extraction is a re-runnable derived layer; the hash-addressed originals are the ground truth that survives our own bugs. The raw store lives outside git (local disk, covered by machine backup) and is append-only.
9. **Vendor-agnostic agent boundary.** The agent's entire contract is: prompt file in, CLI tools during, run report out. Swapping Claude Code for another CLI agent is a one-line change.
10. **The agent cannot modify its own cage.** The repo's code, schema, criteria, and prompts are read-only to the agent. Its only self-improvement channel is appending to `PROPOSALS.md`.

---

## 3. System overview

```
                         ┌─────────────────────────────────────────────┐
                         │                daily run (cron)             │
                         │                                             │
 sources.yaml ──────────►│  PHASE A: monitor (deterministic, no LLM)   │
 (allowlist, 2 tiers)    │   • HEAD-check known URLs → status changes  │
                         │   • hash-check rotating subset → versions   │
                         │   • diff publisher index pages → candidates │
                         │                                             │
 GitHub issues ─────────►│  PHASE B: agent (Claude Code, headless)     │
 (data-error label)      │   • input: TASK.md + state summary +        │
                         │     criteria.yaml + Phase A candidates      │
                         │   • web search for new docs/sources         │
                         │   • investigates issues                     │
                         │   • output: proposals via propose_doc.py    │
                         │            + run report + PROPOSALS.md      │
                         │                                             │
                         │  propose_doc.py (VALIDATOR — veto power)    │
                         │   canonicalize → dedup → fetch → hash →     │
                         │   criteria → caps → write or reject         │
                         │        │                                    │
                         │        ▼                                    │
                         │  data/docs.sqlite + data/raw/<hash> +       │
                         │  changelog (table + rendered commit msg)    │
                         │                                             │
                         │  PHASE C: build & publish                   │
                         │   • render per-doc pages + metadata.json    │
                         │   • Pagefind index                          │
                         │   • git commit + push                       │
                         │   • wrangler pages deploy site/             │
                         └───────────────┬─────────────────────────────┘
                                         ▼
                          Cloudflare Pages → cards.douwmarx.com
                                         ▼
                          visitors: browse / search / report issue ──► GitHub issues
```

---

## 4. Repository layout

```
cardtrack/
├── config/
│   ├── sources.yaml          # allowlist: publishers + evaluators, tiers, index URLs
│   ├── criteria.yaml         # inclusion criteria (hard + soft)
│   └── settings.yaml         # caps, cadences, paths, AGENT_CMD
├── prompts/
│   └── TASK.md               # the agent's daily instructions (human-edited only)
├── scripts/
│   ├── monitor.py            # Phase A: link check, fingerprint check, index diff
│   ├── propose_doc.py        # THE write path: validate + upsert (also a CLI for humans)
│   ├── comment_issue.py      # the only route to GitHub issue comments (agent and human)
│   ├── state_summary.py      # exports compact known-state JSON for agent context
│   ├── extract_text.py       # pdftotext / trafilatura wrapper → data/text/<hash>.txt
│   ├── build_site.py         # DB → site/ (pages, metadata.json)
│   └── run_daily.sh          # orchestrates A → B → C, logging, lock file
├── data/
│   ├── docs.sqlite           # source of truth (metadata, versions, changelog); committed
│   ├── raw/<sha256>.<ext>    # immutable blobs; LOCAL ONLY, gitignored
│   └── text/<sha256>.txt     # extracted text (derived, re-buildable); committed
├── site/                     # built output, committed, deployed via wrangler
│   ├── index.html            # table UI
│   ├── docs/<slug>.html      # per-document pages
│   ├── data/metadata.json    # export of site_documents view
│   └── pagefind/             # generated search index
├── logs/                     # run logs, friction.jsonl (gitignored or committed—your call)
├── PROPOSALS.md              # agent's append-only improvement suggestions
└── .github/workflows/        # empty at MVP; daily.yml added at Actions migration
```

**Agent write permissions**: may execute `scripts/propose_doc.py` and `scripts/comment_issue.py`, and append to `PROPOSALS.md` and `logs/friction.jsonl`. Everything else read-only. The agent never runs `git` or writes to GitHub directly. Enforcement is layered: `--allowedTools` scoping for ergonomics, plus an OS-level sandbox (bwrap or a dedicated user with read-only mounts on everything except the four writable paths) as the actual boundary — tool-scoping prefix matching alone is not a security boundary.

---

## 5. Data model

SQLite. Source of truth is `data/docs.sqlite`; the site consumes exports, never the live file.

```sql
CREATE TABLE documents (
  id               INTEGER PRIMARY KEY,
  slug             TEXT UNIQUE NOT NULL,     -- e.g. "openai-gpt-5-system-card"
  title            TEXT NOT NULL,
  publisher        TEXT NOT NULL,            -- key into sources.yaml
  doc_type         TEXT NOT NULL CHECK (doc_type IN
                     ('model_card','system_card','independent_eval','addendum','other')),
  is_independent   INTEGER NOT NULL DEFAULT 0,
  model_names      TEXT NOT NULL DEFAULT '[]',  -- JSON array; plain filterable text at MVP
  publication_date TEXT,                     -- ISO 8601; NULL if undetermined
  canonical_url    TEXT UNIQUE NOT NULL,
  alt_urls         TEXT NOT NULL DEFAULT '[]',  -- JSON array (mirrors, old locations)
  status           TEXT NOT NULL DEFAULT 'active' CHECK (status IN
                     ('active','moved','dead','superseded','removed')),
  first_seen       TEXT NOT NULL,
  last_checked     TEXT,
  last_changed     TEXT,
  source_of_lead   TEXT,                     -- 'monitor' | 'agent_search' | 'citation' | 'issue:<n>' | 'manual'
  notes            TEXT
);

CREATE TABLE document_versions (
  id                  INTEGER PRIMARY KEY,
  document_id         INTEGER NOT NULL REFERENCES documents(id),
  content_hash        TEXT NOT NULL,        -- sha256 of raw bytes; names the blob
  content_fingerprint TEXT NOT NULL,        -- sha256 of extracted text; the change-detection key
  fetched_at          TEXT NOT NULL,
  content_type        TEXT,                 -- 'application/pdf' | 'text/html' | ...
  byte_size           INTEGER,
  raw_path            TEXT NOT NULL,        -- data/raw/<hash>.<ext> (local only)
  text_path           TEXT,                 -- data/text/<hash>.txt (NULL if extraction failed)
  extraction          TEXT NOT NULL DEFAULT '{}',-- JSON; empty at MVP, future field extraction
  UNIQUE (document_id, content_fingerprint)
);

CREATE TABLE changelog (
  id           INTEGER PRIMARY KEY,
  run_id       TEXT NOT NULL,               -- e.g. '2026-08-09T06:15Z-local'
  ts           TEXT NOT NULL,
  action       TEXT NOT NULL CHECK (action IN
                 ('add','new_version','status_change','field_update','reject','issue_resolved')),
  document_id  INTEGER,                     -- NULL for rejects of never-added items
  detail       TEXT NOT NULL                -- JSON: see §7 proposal record
);

-- Derived state: views, never flags.
CREATE VIEW latest_versions AS
SELECT dv.* FROM document_versions dv
WHERE dv.id = (
  SELECT id FROM document_versions
  WHERE document_id = dv.document_id
  ORDER BY fetched_at DESC, id DESC LIMIT 1
);

CREATE VIEW site_documents AS
SELECT d.*, lv.content_hash, lv.content_type, lv.fetched_at AS version_fetched_at,
       (SELECT COUNT(*) FROM document_versions WHERE document_id = d.id) AS version_count
FROM documents d
JOIN latest_versions lv ON lv.document_id = d.id
WHERE d.status != 'removed';
```

**Identity rules**
- *Canonical URL*: lowercase scheme+host, redirects resolved (≤5 hops), fragments and known tracking params (`utm_*`, `ref`, …) stripped. Uniqueness enforced by the DB.
- *Content hash*: SHA-256 of raw bytes. Names the blob in `data/raw/`; never used for change detection (live HTML embeds nonces, tokens, and build hashes, so raw bytes churn on every fetch).
- *Content fingerprint*: SHA-256 of the extracted text (`extract_text.py` output; normalized whitespace). The key for versioning and idempotency: same fingerprint → no-op beyond `last_checked`; new fingerprint → new version. If extraction fails, fall back to the raw hash.
- *Logical identity*: `(publisher, doc_type, model_names overlap)`, with model names normalized (lowercase, strip punctuation) before comparison. Used by the validator to catch "same card, different URL" — outcome is `needs_review` (a filed issue), not an automatic merge, at MVP.

**Semantics of `status`**: `moved` = canonical URL redirected permanently (agent may propose URL update; old URL appended to `alt_urls`); `dead` = repeated 404/410-class failure (≥3 consecutive runs); `superseded` = replaced by a newer document (linked in `notes`); `removed` = curatorial soft delete. 403/429/bot-challenge responses never count toward `dead` — most AI-lab sites bot-block scripted requests; the monitor records them as blocked and routes persistent cases to the agent for confirmation via its own fetch tools. Raw bytes of `dead`/`removed` docs are retained; their pages keep the extracted text and mark the source link accordingly.

---

## 6. Configuration

**`config/sources.yaml`** — the allowlist, two categories × two tiers:
```yaml
publishers:            # first-party
  anthropic:
    tier: 1            # tier 1 = auto-merge eligible
    index_urls: ["https://www.anthropic.com/..."]   # pages Phase A diffs for new links
  openai:
    tier: 1
    index_urls: [...]
evaluators:            # independent
  metr:
    tier: 1
    index_urls: ["https://metr.org/evaluations/"]
  uk_aisi:
    tier: 1
    index_urls: [...]
# tier 2 orgs: known but lower confidence → proposals become issues, not rows
```

**`config/criteria.yaml`** — inclusion criteria, split by who can actually check them:
```yaml
validator_checked:                   # enforced deterministically; any failure → reject
  publisher_on_allowlist: true
  document_retrievable: true         # fetch succeeded, sane content-type & size
  min_publication_date: "2026-01-01" # scope floor; NULL dates → file_issue
agent_attested:                      # judgment calls; agent must assert, recorded in provenance
  primary_source: true               # the org's own publication, not press coverage
  about_a_specific_model_or_eval: true
soft:                                # recorded, displayed, not blocking at MVP
  has_quantitative_data: null
  pdf_available: null
policy:
  when_uncertain: file_issue         # the prime directive: an issue, not a row
```

**`config/settings.yaml`** — operational caps and cadences:
```yaml
caps:
  max_new_documents_per_run: 15
  max_new_versions_per_run: 30
  max_fetch_bytes: 52428800          # 50 MB per document
  max_total_fetch_bytes_per_run: 524288000  # 500 MB per run
  fetch_timeout_seconds: 60
cadence:
  linkcheck: all_active_every_run
  fingerprint_fraction: 0.15         # ~weekly full coverage of silent updates
agent:
  cmd: 'claude -p "$(cat prompts/TASK.md)" --allowedTools <scoped list>'
  max_turns: 60
```
`agent.cmd` is the vendor-agnosticism seam: swapping agents edits this one string.

---

## 7. The write path — `propose_doc.py`

The only mutation route, for agent and human alike. Input: one proposal record (JSON via stdin or flags).

```json
{
  "action": "add | new_version | status_change | field_update",
  "url": "https://…",
  "title": "…",
  "publisher": "anthropic",
  "doc_type": "system_card",
  "is_independent": false,
  "model_names": ["Claude Fable 5"],
  "publication_date": "2026-08-01",
  "justification": "One paragraph: why this belongs, per criteria.",
  "criteria": {"publisher_on_allowlist": true, "primary_source": true, "...": true},
  "evidence_urls": ["announcement page, index page, citing doc"],
  "source_of_lead": "agent_search",
  "queries_used": ["anthropic fable system card", "..."]
}
```

**Validation sequence** (fail → structured rejection back to the agent, logged as `reject`):
1. Schema-validate the proposal (types, enums, required fields).
2. Publisher exists in `sources.yaml`; note tier.
3. Canonicalize URL. Known canonical or alt URL? → route as `new_version` check on that document instead of `add`.
4. Fetch with timeout/size/content-type limits. Failure → reject (`document_retrievable=false`).
5. Extract text, compute fingerprint. Fingerprint already stored for this document? → no-op; update `last_checked` only. (Idempotency.)
6. Logical-duplicate scan against existing documents. Suspected match at a different URL → **do not write**; file a `needs-review` GitHub issue with both candidates.
7. Validator-checked criteria pass? All `agent_attested` criteria asserted true? Tier 1? Caps not exceeded? → **write**: store raw blob (local), store extracted text, insert version row (+ document row if `add`), append changelog row with the full proposal record as `detail`. Tier 2 or uncertain → file an issue instead.
8. Emit machine-readable result (`written | duplicate | rejected:<reason> | issue_filed:<n>`) so the agent can report accurately.

**Slugs** are derived by the validator, deterministically (`<publisher>-<primary model>-<doc_type>`, numeric suffix on collision). Agent-supplied slugs are ignored.

**Other actions**: `new_version` carries `{action, url}`; `status_change` and `field_update` carry `{action, slug, field, old, new}`. All actions require `justification` and `evidence_urls` and land in the changelog identically.

**Changelog rendering**: Phase C generates the commit message from the run's changelog rows — the JSON is canonical, the commit message is a view of it. The same records render on each document's public page as its provenance block.

---

## 8. The daily run

`run_daily.sh`, executed under cron with `flock` so overlapping runs are impossible.

**Phase A — monitor (no LLM).** `monitor.py`, fetching with a browser User-Agent and `GET` + `Range` (many CDNs mishandle `HEAD` and bot-block default UAs):
- Check all `active`/`moved` canonical URLs; record status transitions per §5 semantics (3-strike rule on 404-class only; 403/429/challenge → blocked, escalate to agent).
- Full-fetch + fingerprint a rotating `fingerprint_fraction` of documents; fingerprint change → auto-write `new_version` through `propose_doc.py` (deterministic caller, same gate).
- Fetch each allowlisted `index_url`, extract links, diff against known canonical+alt URLs → `candidates.json`.

**Phase B — agent.** Invoke `agent.cmd`. The agent receives, via `TASK.md` and generated context files:
- The state summary (`state_summary.py`: all known `(publisher, model_names, canonical_url, status)` — ~50 KB at target scale).
- `criteria.yaml`, `candidates.json`, and open GitHub issues labeled `data-error` / `missing-doc` (fetched via `gh` CLI, read-only).

Its tasks, in order: (1) triage Phase A candidates → proposals; (2) targeted web search for the last ~72 h of releases and for allowlisted orgs silent >N days; (3) citation mining on newly added documents (cards reference predecessor cards and third-party evals); (4) investigate open issues → corrective proposals (`status_change`/`field_update`) or a comment via `comment_issue.py`; (5) confirm or clear Phase A blocked-URL escalations; (6) append friction events to `logs/friction.jsonl`; (7) append any process/schema suggestions to `PROPOSALS.md`; (8) write `logs/run_report.md`.

*Injection posture*: everything the agent reads — web pages **and issue text** — is untrusted input. Safety does not depend on the agent resisting manipulation; it depends on the write path's validation, caps, and soft-delete-only semantics. A fully compromised Phase B can, at worst, produce ≤caps junk rows from allowlisted publishers, which provenance display and `git revert` handle.

**Phase C — build & publish.** `build_site.py` exports `metadata.json` from `site_documents`, renders per-doc pages, runs `npx pagefind --site site`; then commit (generated message), push, and `wrangler pages deploy site/`. Direct upload keeps deploys independent of repo size and needs only an API token in `~/.config/secrets.env`. After a `git revert`, rerun the deploy command; the runbook says so.

**Scheduling:**
```
15 06 * * *  cd $HOME/cardtrack && flock -n .run.lock ./scripts/run_daily.sh >> logs/cron.log 2>&1
```
A missed day self-heals: the next idempotent run simply finds more. Hosting ladder: local machine (MVP) → personal server (same crontab, better uptime) → GitHub Actions if usage warrants (§14).

---

## 9. Frontend

Static, vanilla JS (or one lightweight table library), no build framework.

**Table view (`index.html`)** — loads `metadata.json` (metadata only; ~small even at 5k rows):
- Columns: title, publisher, doc_type, models, publication date, status, version count, first_seen. Show/hide toggles; sortable; CSV export of the current filtered view (client-side).
- **Filter box (metadata scope)**: substring/fuzzy match over title + model_names + publisher. This is the "give me the GPT-5.4 system card link" path — precise because it searches only identity fields, not bodies (which cite competitor models in comparison tables and would drown the signal).
- Facet filters: publisher, doc_type, is_independent, status, year.

**Search page (full-text scope)** — Pagefind UI over per-document pages. Pages carry `data-pagefind-meta` (title, publisher, date) and `data-pagefind-filter` (publisher, doc_type, year) so full-text hits remain facetable; only the extracted-text container is marked `data-pagefind-body`. Answers content questions ("which documents discuss autonomous replication").

**Per-document page (`docs/<slug>.html`)**:
- Metadata block; link out to the source (the only route to the original — no re-hosting, no inline preview); version history (dates + fingerprints, from `document_versions`).
- **Provenance block**: rendered changelog entries — when added, by which run, justification, criteria results.
- **Report an issue**: prefilled `https://github.com/<owner>/<repo>/issues/new?labels=data-error&title=…&body=…` embedding slug, URL, fingerprint.
- Extracted text (collapsed `<details>`, the Pagefind body).
- `dead`/`removed` docs keep their page and text; the source link is labeled with its status.

---

## 10. Correction & proposal loops

- **Data errors**: visitor → prefilled issue → next run's Phase B task 4 → proposal through the standard gate → issue commented and labeled `resolved` (human closes, or auto-close if you prefer). Soft deletes only; nothing a bad report can destroy.
- **Missing documents**: `missing-doc` issues are treated as leads (`source_of_lead: issue:<n>`), subject to identical criteria — crowdsourced recall, not crowdsourced authority.
- **Process improvements**: agent appends to `PROPOSALS.md` (dated entry, problem, suggested change, evidence from `friction.jsonl`). Humans read it whenever; agents never touch code, schema, prompts, or criteria. Expected volume: rare, per your call.

---

## 11. Failure modes → mitigations

| Failure | Mitigation |
|---|---|
| Agent hallucinates a document | Validator fetches and fingerprints reality; unfetchable → reject |
| Duplicate entries | 4-layer identity at the write boundary; DB uniqueness constraints |
| Prompt injection via web page or issue | OS-sandboxed agent, constrained tools, caps, allowlist-gated writes, soft deletes, provenance + revert |
| Slop / low-quality additions | Split criteria, tier-2 → issues not rows, per-run caps, public justification on every row |
| Spurious versions from dynamic HTML | Change detection on extracted-text fingerprint, never raw bytes |
| Bot-blocking mistaken for link rot | 403/429/challenge never strike toward `dead`; agent confirms before status change |
| Silent document update missed | Rotating fingerprint checks (full coverage ~weekly) |
| Source link rot | Status lifecycle; page keeps extracted text; raw bytes retained locally |
| Run crashes mid-way | Idempotent upserts; lock file; next run recovers |
| Bad run lands | `git revert` of that run's commit + redeploy; raw store is append-only, untouched by reverts |
| Extraction bugs / improvements | Text is derived from immutable raw bytes; re-run `extract_text.py` corpus-wide, fingerprints recompute |
| Schema pressure from new content | JSON `extraction` column; future data as rows in new tables (§14), never content-driven migrations |

---

## 12. What the human still does

Honest accounting, since there's no review gate: maintain `sources.yaml` / `criteria.yaml` / `TASK.md`; skim `run_report.md` occasionally; close resolved issues; read `PROPOSALS.md` when curious; revert on the rare bad run; seed the initial corpus (backfill is just `propose_doc.py` invocations — by hand, or one supervised agent session).

## 13. Bootstrap order

1. Repo + schema + `propose_doc.py` + `extract_text.py`, with a pytest suite for the validator (canonicalization table, dedup cases, cap enforcement, idempotent re-run — this is the component everything else trusts); add 10 documents **by hand** through the tool.
2. `build_site.py` + table UI + Pagefind + per-doc pages; `wrangler pages deploy site/` → cards.douwmarx.com. (A useful public artifact already, with zero automation.)
3. `monitor.py` + `run_daily.sh` under cron **without Phase B**. (Deterministic tracking live.)
4. Add Phase B with tiny caps (e.g. 3/run); watch a week of changelogs; raise caps.
5. Backfill the 2026 corpus (bounded by `min_publication_date`; one supervised agent session).

## 14. Extension roadmap (explicitly deferred)

- **GitHub Actions**: add `.github/workflows/daily.yml` wrapping `run_daily.sh` + auth secrets; delete the crontab line. Prerequisite: the raw store must first move somewhere the runner can reach (e.g. a private R2 bucket, same hash-addressed keys) — it is the one piece of state that lives outside the repo.
- **Deeper backfill**: lower `min_publication_date` when pre-2026 coverage becomes worth the supervised effort.
- **Public archive access**: if the no-re-hosting stance changes, publish raw blobs from a bucket keyed by content hash; per-doc pages gain an "archived copy" link. No schema change.
- **Field extraction / eval scores**: populate `extraction` JSON; when stable, promote to `eval_results(version_id, benchmark, score, conditions)` — benchmarks are *data*, so new benchmarks are rows.
- **Models table** if users start thinking model-first: derive `models` + join table from `model_names`; no document-row changes.
- **Scale outgrows Pagefind/static**: sqlite-wasm over HTTP range requests, or D1 + a Worker — same SQLite data model either way.
- **Tier-2 auto-merge** once criteria FPR (false positive rate) is demonstrated low in the changelog record.

## 15. Open items

1. Commit `logs/` or gitignore it (recommendation: commit `run_report.md`, gitignore raw logs).
2. Project name.
