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
agent sandbox), the `claude` CLI (agent phase), and for the weekly report `pandoc`,
`latexmk` and TeX Live.

Production host: `infra/` turns a fresh Debian 13 server into production over SSH;
see [infra/README.md](infra/README.md). The exact Debian package
list lives in `infra/bootstrap.sh`, and `infra/test-bootstrap.sh` proves it in a
container. Note: bwrap needs unprivileged
user namespaces (default-on in Debian 12+; Ubuntu 24.04 restricts them via AppArmor —
if `bwrap true` fails there, the sandbox script warns and the agent phase should stay
disabled or run with a relaxed AppArmor profile).

```sh
uv sync                      # installs deps + dev tools (pytest, ruff, poe)
uv run poe test              # full test suite (local HTTP servers, no internet)
cp env.example .env          # set CARDTRACK_ROLE=dev on a development machine
```

Roles: a checkout with `CARDTRACK_ROLE=prod` (the default) publishes, files alert
issues and pulls new code before each run. `CARDTRACK_ROLE=dev` runs every phase but
never commits, pushes, deploys or files issues. Develop on a dev checkout, push to
`main`; production picks the change up at its next run, only if the test suite passes
on it (`deploy.*` in settings.yaml, `scripts/deploy_update.sh`), and otherwise stays on
the last good commit and opens a `pipeline-alert: deploy-rejected` issue.

## Everyday commands

```sh
uv run poe test                          # pytest
uv run poe lint                          # ruff
uv run poe monitor                       # Phase A only (link/fingerprint/index checks)
uv run poe build                         # rebuild site/ from the DB
uv run poe serve                         # preview at http://localhost:8791
uv run poe daily                         # full daily run (A → B → C)
uv run poe smoke                         # live smoke test of systemcards.org + the archive
uv run poe test-bootstrap                # setup script + tests in a clean Debian 13 container
uv run poe rehearse                      # dress rehearsal of a production host (see infra/README.md)
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
  --safety-evals yes \
  --source-of-lead manual
```

It prints a JSON verdict: `written | duplicate | noop | rejected | issue_filed`.
Proposals can also be piped as JSON: `propose_doc.py --json -` (see
`prompts/TASK.md` for the record format).

## Publisher roster sync

`config/sources.yaml` is the curated allowlist. `config/roster.yaml` adds a
deterministic Phase A step (`uv run poe roster`) that pulls OpenRouter's daily
rankings dataset, ranks model authors by trailing-window token share, and writes
`config/sources.generated.yaml`: an additive overlay of tier-2 publishers that
together cover `cumulative_share` (99%) of attributable traffic and are not
already curated. `Repo.sources` merges the two; base wins on any collision. Overlay entries
carry only identity (tier 2, display name, HuggingFace org as `index_urls` when
known); they have no `scope` note, so the agent applies `covered_model_class`
strictly and finds their documents by web search. Authors present on fewer than
`min_days_present` days of the window are ignored as spikes. Needs
`OPENROUTER_API_KEY` in the environment or `.env` (any key; the endpoints are
free, two calls per run). The overlay changes only when membership changes and
is committed with the daily run, so its diff is the review gate on widening.

Fail-closed: a fetch error, schema change, truncated window, or crash keeps
the previous overlay untouched and logs a warning. Failures are counted in
`logs/.roster_failstreak` (manual runs included; a success clears it) and the
third in a row files a `pipeline-failure` issue. An author dropping out of the
rankings never removes a publisher. Escape hatches: `enabled: false`,
`deny: [slug]` (honoured at load time, so it works even while the sync is
down), `git revert` of the daily commit, or copying an overlay stanza into
`sources.yaml` to make it curated. `logs/roster_openrouter.json` records every
author seen in the window, why it was or was not admitted, and how much of all
traffic the allowlist covers once the dataset's unattributed "other" bucket is
counted.

## The daily run

`scripts/run_daily.sh` orchestrates: Phase A `monitor.py` (deterministic
link checks, fingerprint rotation, index diffs) → Phase B agent (only if
`agent.enabled: true` in `config/settings.yaml`) → Phase C `build_site.py` +
optional git commit/push + optional Cloudflare Pages deploy (gated by the
`publish.*` settings).

Scheduling — systemd user timers (NixOS and Debian). Three timers share one lock,
so runs never overlap; a run waits for the lock instead of skipping its day:

| Timer | When (UTC) | Does |
|---|---|---|
| `cardtrack-canary` | daily 05:15 | one model call with the pipeline's credentials + health issues |
| `cardtrack` | daily 06:15 | pull + test new code, then the A → B → C run |
| `cardtrack-report` | Sunday 02:00 | the weekly research report (Analysis page) |

```sh
scripts/install_units.sh             # install for this checkout's path, enable, linger
scripts/install_units.sh --disable   # stop them (e.g. on the old host after a move)
```

Classic cron works too where cron exists (not on NixOS by default):

```
15 06 * * *  <repo>/scripts/deploy_update.sh; <repo>/scripts/run_daily.sh >> <repo>/logs/cron.log 2>&1
```

`run_daily.sh` sets its own PATH (NixOS profiles, `~/.local/bin`, system dirs), so
it runs correctly under a scheduler's minimal environment on either OS.

Laptops: a missed firing runs the moment the machine resumes, before Wi-Fi is
back. The run therefore waits for the network first (`network.*` in
settings.yaml; exit 75 after 15 min with nothing touched), and the service unit
retries a failed day every 30 min, at most 5 starts per day (`Restart=on-failure`;
a security hold, exit 10, is never retried). After editing the unit files, re-run
`scripts/install_units.sh`.

Phase B uses the `claude` CLI via `agent.cmd` in settings — it authenticates with
a Claude subscription, never metered API billing (`env -u ANTHROPIC_API_KEY`).
Unattended hosts use a one-year token: run `claude setup-token` while signed in to
the pipeline's own account and put it in `.env` as `CLAUDE_CODE_OAUTH_TOKEN` with
`CLAUDE_TOKEN_CREATED=YYYY-MM-DD` (an issue opens 30 days before it expires).
Without a token, the `/login` session under `CLAUDE_CONFIG_DIR` (default
`~/.claude`) is used, refreshed on the host before each run. Swapping in another CLI agent is a one-line change to
`agent.cmd`.

## Alerts

`scripts/health.py` runs at the end of every daily run and from the canary. It keeps
one GitHub issue per failing condition, titled `pipeline-alert: <condition>`, and
closes it when the condition clears. Thresholds are elapsed time, never run counts,
so same-morning retries cannot read as an outage:

| Condition | Opens when |
|---|---|
| `agent-down`, `monitor-down`, `deploy-failing` | no success for 36 h |
| `report-stale` | no weekly report for 8 days |
| `backup-stale` | no R2 copy of `data/raw` for 36 h (only if R2 is configured) |
| `deploy-rejected` | production refused a commit whose tests failed |
| `outbox-stuck` | queued issues/comments undelivered for 24 h |
| `claude-token-expiring` | the setup-token is within 30 days of expiry |
| `claude-unavailable` | the canary's model call fails three times, 2 min apart |

The GitHub `dead-man` workflow covers the one case the host cannot report: the host
itself being down (no commit for 48 h).

## Analysis page (weekly report)

`scripts/run_report.sh` has a sandboxed agent (writable: `report/` only) follow
[.claude/skills/cardtrack-report/SKILL.md](.claude/skills/cardtrack-report/SKILL.md)
to regenerate the research report in `report/`. `scripts/report_html.py` converts the
LaTeX to HTML with pandoc into `report/published/`, and the site renders it at
`/analysis.html` with a disclaimer naming the model that wrote it and linking the
skill at the commit used. Maintainers steer the report by editing the skill.

## Operational notes

- **Source of truth**: `data/docs.sqlite` (committed). `data/raw/` holds immutable
  hash-addressed original bytes (gitignored, too large for git). `scripts/backup.sh`
  copies it after each production run to a private R2 bucket (`R2_BUCKET`, add-only)
  and to the public archive (`R2_PUBLIC_BUCKET`, served at `archive.public_base_url`),
  which also gets `manifest.json`, `urls.txt` and `cardtrack-dataset.tar.gz`.
  Takedowns: add the content hash to `config/withheld.txt`; the next run deletes it
  from the public bucket and drops its links, and the private copy stays.
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
  The derived layer (text files + fingerprints) is stamped with a config id
  (`DERIVED_LAYER_VERSION` in `cardtrack/extract.py` + the ignore patterns) and the
  monitor refuses to run while it is stale, so a pattern or extractor change can never
  mint a bogus version for every document. After changing the patterns run
  `scripts/recompute_fingerprints.py --apply`; after changing extraction (bump
  `DERIVED_LAYER_VERSION`) run `scripts/extract_text.py --reextract-all --apply`, which
  rewrites the text files from the raw store, recomputes fingerprints and prunes
  versions that now extract identically. Both are dry-run by default.

## Security model

The agent proposes; `propose_doc.py` disposes. Correctness (no duplicates, valid
schema, caps, allowlist) is enforced deterministically at the write boundary, never
by agent diligence. Caps and the fetch budget are enforced over a **rolling 24 h
window** keyed on the changelog's own timestamps — caller-supplied run ids group
entries but can never reset limits. (Backfills: temporarily raise the caps in
`config/settings.yaml`, then restore them.)

Phase B runs inside `scripts/agent_sandbox.sh` (bwrap): the filesystem is read-only,
`$HOME` is a tmpfs (no `~/.ssh`, no `~/.config/secrets.env`, no gh auth), the
repo-local `.env` is masked with `/dev/null` and every key named in it is unset in
the agent's environment, and the only writable paths are `data/`, `logs/` (the weekly
report agent: `report/` only) plus an **ephemeral** `~/.claude`. The one credential
that enters is Claude's:

- with a setup-token (production): `CLAUDE_CODE_OAUTH_TOKEN` as an env var. It is
  long-lived but can only make model requests, belongs to an account that holds
  nothing else, and is revocable at claude.ai/settings/claude-code. This trade was
  made after 8 of 15 agent-phase failures (2026-08-24..09-29) turned out to be
  expired or unseedable `/login` credentials.
- with a `/login` session: a **slimmed** copy of the credential file (refresh token
  and MCP OAuth tokens stripped), so only a short-lived access token can leak.

The host `settings.json` is deliberately NOT seeded. Issues and issue comments the sandboxed
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
scoping above, per "some risk is acceptable".

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

1. ✅ Schema + validator + extraction + full test suite (`poe test`); every document seeded through the tool (280+ and counting — the site header shows the live number)
2. ✅ Site live at https://systemcards.org (Pages project `cardtrack`; systemcards.org +
   www + cards.douwmarx.com all attached, CNAMEs → cardtrack-aar.pages.dev, HTTPS active)
3. ✅ Daily schedule live (systemd user timer, 06:15 UTC, linger enabled); host-as-code in
   `infra/` (any Debian 13 server; netcup in production), funded for 12 months by a
   BlueDot Rapid Grant
4. ✅ Agent enabled and battle-tested (backfill drain + audits, 2026-08-09/10)
5. ✅ 2026 corpus backfilled (supervised session, 2026-08-09); deepen later by lowering `min_publication_date`
