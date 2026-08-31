# cardtrack

A continuously maintained, publicly browsable database of AI model documentation —
first-party model/system cards and independent evaluation reports — with change
tracking, provenance, and full-text search. Curated daily by an LLM agent behind
deterministic guardrails; published as a static site.

Live site: https://systemcards.org (also reachable at https://cards.douwmarx.com).

## Setup (clean clone)

Requirements: Python ≥3.11 with [uv](https://docs.astral.sh/uv/), and for the full
pipeline: `node`/`npx` (Pagefind + wrangler), `pdftotext` (poppler; optional —
falls back to pypdf), `gh` (optional — GitHub issues loop), `bwrap` (optional —
agent sandbox), the `claude` CLI (agent phase; authenticate once with `claude login`).

Debian/Ubuntu: `apt install git curl nodejs npm poppler-utils bubblewrap` then the
[uv](https://docs.astral.sh/uv/getting-started/installation/),
[gh](https://github.com/cli/cli#installation), and
[claude](https://claude.com/claude-code) installers. Note: bwrap needs unprivileged
user namespaces (default-on in Debian 12+; Ubuntu 24.04 restricts them via AppArmor —
if `bwrap true` fails there, the sandbox script warns and the agent phase should stay
disabled or run with a relaxed AppArmor profile).

```sh
uv sync                      # installs deps + dev tools (pytest, ruff, poe)
uv run poe test              # full test suite (local HTTP servers, no internet)
cp env.example .env          # then fill in Cloudflare credentials (deploy only)
```

## Everyday commands

```sh
uv run poe test                          # pytest
uv run poe lint                          # ruff
uv run poe monitor                       # Phase A only (link/fingerprint/index checks)
uv run poe build                         # rebuild site/ from the DB
uv run poe serve                         # preview at http://localhost:8791
uv run poe daily                         # full daily run (A → B → C)
```

The table UI loads `data/metadata.json` via fetch, so preview through `poe serve`
(or any HTTP server) — opening `site/index.html` via `file://` shows an empty table.

## Adding a document by hand

Everything goes through the validator — humans included:

```sh
uv run python scripts/propose_doc.py \
  --action add \
  --url "https://www.anthropic.com/…" \
  --title "Claude Fable 5 System Card" \
  --publisher anthropic --doc-type system_card \
  --model "Claude Fable 5" --publication-date 2026-08-01 \
  --justification "First-party system card announced at …" \
  --evidence-url "https://www.anthropic.com/news/…" \
  --attest primary_source --attest about_a_specific_model_or_eval \
  --attest distinct_model_release --attest notable_release \
  --attest covered_model_class \
  --source-of-lead manual
```

It prints a JSON verdict: `written | duplicate | noop | rejected | issue_filed`.
Proposals can also be piped as JSON: `propose_doc.py --json -` (see
`prompts/TASK.md` for the record format).

## The daily run

`scripts/run_daily.sh` orchestrates: Phase A `monitor.py` (deterministic
link checks, fingerprint rotation, index diffs) → Phase B agent (only if
`agent.enabled: true` in `config/settings.yaml`) → Phase C `build_site.py` +
optional git commit/push + optional Cloudflare Pages deploy (gated by the
`publish.*` settings).

Scheduling — systemd user timer (works on NixOS and Debian; the script holds its
own lock, so overlapping runs are impossible):

```sh
cp scripts/systemd/cardtrack.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now cardtrack.timer
loginctl enable-linger $USER     # keep timers firing when logged out
```

Classic cron works too where cron exists (not on NixOS by default):

```
15 06 * * *  $HOME/projects/ais/system_card_db/scripts/run_daily.sh >> $HOME/projects/ais/system_card_db/logs/cron.log 2>&1
```

`run_daily.sh` sets its own PATH (NixOS profiles, `~/.local/bin`, system dirs), so
it runs correctly under a scheduler's minimal environment on either OS.

Phase B uses the `claude` CLI via `agent.cmd` in settings — it authenticates with
your Claude subscription login (`env -u ANTHROPIC_API_KEY` guards against silently
switching to API billing). Swapping in another CLI agent is a one-line change to
`agent.cmd`.

## Operational notes

- **Source of truth**: `data/docs.sqlite` (committed). `data/raw/` holds immutable
  hash-addressed original bytes — local only, gitignored, never published.
  `data/text/` is derived, re-buildable via `scripts/extract_text.py --reextract-all`.
- **Reverting a bad run**: `git revert <run commit>` then
  `uv run poe build && npx -y wrangler pages deploy site --project-name cardtrack`.
  The raw store is append-only and untouched by reverts.
- **Issues loop**: issues are for EXCLUSION, never pre-approval — every allowlisted
  publisher auto-merges (tier is a provenance label). The validator no longer files
  review issues for duplicates: it resolves them deterministically (same-publisher
  identical content = mirror → skip; cross-publisher identical content = co-publication
  → admit and flag; a similar title is a duplicate only if the extracted text is also
  similar). GitHub issues are now just visitor-filed data-error/missing-doc reports;
  the operator can force a skipped add with `propose_doc.py --override-duplicate-review`.
  The agent reports pipeline limitations to `PROPOSALS.md`, not issues.
- **Caps and criteria** live in `config/settings.yaml` / `config/criteria.yaml`;
  the allowlist (with per-publisher `scope` notes) in `config/sources.yaml`. The
  agent cannot modify any of them. The `risk_domains` tag vocabulary is defined in
  `criteria.yaml` and gated by the validator.
- **Canonical URLs favor the full document** (usually the PDF) over announcement
  pages; companions live in the structured `related_urls` field, same-document
  mirrors in `alt_urls` (identity-bearing, drives dedup). Version rows carry
  agent-written `change_summary` notes (validated `annotate_version` action);
  Phase A emits `logs/updated_docs.json` + diffs for versions still needing one.
- **Fingerprints ignore page furniture** (`fingerprint.ignore_line_patterns` in
  settings.yaml — HF download counters, rotating blog footers, access-date stamps).
  If you change the patterns, run `scripts/recompute_fingerprints.py --apply`
  or every unchanged document mints a bogus version on its next fetch.

## Security model

The agent proposes; `propose_doc.py` disposes. Correctness (no duplicates, valid
schema, caps, allowlist) is enforced deterministically at the write boundary, never
by agent diligence. Caps and the fetch budget are enforced over a **rolling 24 h
window** keyed on the changelog's own timestamps — caller-supplied run ids group
entries but can never reset limits. (Backfills: temporarily raise the caps in
`config/settings.yaml`, then restore them.)

Phase B runs inside `scripts/agent_sandbox.sh` (bwrap): the filesystem is read-only,
`$HOME` is a tmpfs (no `~/.ssh`, no `~/.config/secrets.env`, no gh auth), the
repo-local `.env` is masked with `/dev/null`, and the only writable paths are
`data/`, `logs/`, `PROPOSALS.md`, plus an **ephemeral** `~/.claude` seeded with a
**slimmed** credential file — the long-lived refresh token and any MCP OAuth tokens
are stripped at seed time, so the worst a prompt-injected agent can exfiltrate is a
short-lived access token (verified empirically 2026-08-31: headless `--allowedTools`
does deny unlisted tools, and runs authenticate fine on the slimmed file). The host
`settings.json` is deliberately NOT seeded. Issues and issue comments the sandboxed
agent writes land in outboxes (`issues_outbox.jsonl`, `comments_outbox.jsonl`);
`scripts/flush_outbox.py` delivers them to GitHub *outside* the sandbox.

**Outbound review gate** (Phase C, outside the sandbox, fail-closed): before
anything is flushed, committed, pushed, or deployed, `scripts/secret_scan.py` runs
high-precision secret patterns plus exact-match against the machine's live secret
values over `docs.sqlite` + `logs/`, and `scripts/review_outbound.py` (settings
`review.llm_screen`) runs one cheap LLM pass over agent-authored outbound text with
a narrow hold-only-clear-leaks charter. On any finding the run publishes nothing,
writes `logs/SECURITY_HOLD.md`, and exits non-zero; quarantined records go to
`logs/*.held.jsonl` (gitignored). Accepted residual: the agent's own WebFetch/
WebSearch request URLs are an un-gateable exfil channel — bounded by the credential
slimming above, per "some risk is acceptable".

Known residual gaps at MVP, accepted deliberately: (1) the validator runs inside
the sandbox, so `data/` itself is agent-writable and a fully compromised agent
could bypass it — provenance display, the changelog-to-commit diff, `git revert`,
and the append-only raw store bound the damage; the stronger boundary (validator
behind privilege separation) is future work. (2) The SSRF guard resolves
DNS separately from the fetch, so a DNS-rebinding attacker can race it — impact is
limited to reading the local network from a machine that exposes no local services
to the agent's benefit. (3) `canonical_url` moves require a publisher-known host
plus identical content; shared hosts (e.g. `storage.googleapis.com`) make the host
check weaker than it looks, which is why the content fingerprint must also match.
Everything the agent reads (web pages, issue text) is treated as untrusted input.

## Status

1. ✅ Schema + validator + extraction + 76-test suite; 23 documents seeded through the tool
2. ✅ Site live at https://systemcards.org (Pages project `cardtrack`; systemcards.org +
   www + cards.douwmarx.com all attached, CNAMEs → cardtrack-aar.pages.dev, HTTPS active)
3. ✅ Daily schedule live (systemd user timer, 06:15 UTC, linger enabled)
4. ✅ Agent enabled and battle-tested (backfill drain + audits, 2026-08-09/10)
5. ✅ 2026 corpus backfilled (supervised session, 2026-08-09); deepen later by lowering `min_publication_date`
