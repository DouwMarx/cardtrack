# Roadmap

## Next session

- Family-row granularity ruling (raised twice in logs/PROPOSALS.md and by the
  2026-08-31 false-alarm audit): decide "one row per model generation per product
  line, sizes folded into model_names", then merge the ~8 borderline sibling rows
  (qwen3-6/8-27b, nemotron-nano-4b, cosmos3-edge, gr00t-h pair, mimo-v2-5-pro,
  poolside sizes, ling-2-6-flash).
- Decide on allowlisting bio-foundation-model orgs (Arc Institute, EvolutionaryScale)
  — their structured-access/release-mitigation docs are the open-weight mirror of
  the trusted-access programs now catalogued. Also decide whether AWS Bedrock model
  cards (only public card for GPT-5.6-Cyber) merit a tier-2 co-publisher entry.
- Periodic maintenance/QA agent (raised 2026-09-07): a recurring pass (weekly, or a
  cheap daily step) that audits rather than discovers — sweep for NULL/unclear
  fields and re-attempt verification; re-check labels against live sources
  (licenses change: Muse Spark 1.2 has promised open weights; stale HF badges);
  field-by-field verify recent adds against their sources; scan for pipeline
  failure streaks and provenance blemishes. Evidence it pays: the 2026-09-04 and
  09-07 verification sweeps of exactly this shape produced 75+ corrections
  (openness policy backfill, wrong risk_domains/safety_evals on a fresh add, four
  license misreads). Decide cadence and whether it is a TASK.md step for the
  daily agent or a separate prompt/run.
- Fingerprint leak (2026-09-22 report): Hugging Face eval-widget rows that end in a score
  (`- org/dataset · Name View evaluation results leaderboard 73.4`) pass the bullet-anchored
  `ignore_line_patterns`, so 61% of versions minted after the 31 Aug recompute are still
  furniture and HF pages flag at 37% per content check versus 9% elsewhere. Extend the
  pattern to a trailing number, run `scripts/recompute_fingerprints.py --apply`. Do this
  before the next item or daily coverage mints furniture faster.
- Daily full content coverage instead of the 15% rotation (2026-09-22 report): the
  rotation was sized on day one with no recorded rationale; edits are detected 3.5 days
  late on average and up to a week (17 days at p90 with outages). A full re-fetch is
  376 MB, under the existing 500 MB budget, and adds no requests because the link probe
  already touches every URL daily. Do it as one conditional GET per document
  (`If-None-Match` / `If-Modified-Since`, fall back to `Content-Length`), replacing the
  Range probe, and raise `max_new_versions_per_run` at the same time or a template change
  across the 78 HF cards is truncated silently. Storage at today's flag rate: ~45 MB/day
  raw (local), ~2 MB/day text (committed). Once on the always-on host.
- Classify every minted version in the pipeline (category + flags per the report taxonomy
  in `~/projects/ais/system_card_report/CLASSIFY_INSTRUCTIONS.md`) so "silent score change"
  and "content collapsed" become queryable fields; the report's Appendix A then becomes a
  live feed.
- Run the daily pipeline from committed code only (2026-09-23): the timer executes
  whatever is in the working tree, so an agent's half-finished edit ran in production for
  a day and minted one furniture version before it was caught. Have `run_daily.sh` run
  from a clean worktree at HEAD (or refuse when `git status` is dirty outside `data/`,
  `logs/` and `site/`).

## Done 2026-08-31 (roadmap items built this session)

- Restricted-access programs: new `doc_type: access_policy` + `openness: restricted`,
  TASK.md search keywords + program-name polling, seeds catalogued.
- PDF preference: 27 canonical URLs migrated to authoritative full documents;
  structured `related_urls` field (validated, rendered); TASK.md canonical-URL rule.
- Risk-domain tags: `risk_domains` controlled vocabulary (5 tags = the EU CoP
  specified systemic risks + societal harms, defined in criteria.yaml),
  validator-gated, site filters (table + search), corpus backfilled. (Autonomy /
  AI-R&D folds into loss_of_control; safeguard robustness is not a domain — tag by
  the domain a jailbreak targets.)
- False alarms: `covered_model_class` criterion + tightened `notable_release` +
  per-publisher `scope` notes; verified auxiliary-model cards removed.
- No more duplicate review-issue queue: the validator resolves duplicates
  deterministically (mirror → skip, co-publication → admit+flag, title collision
  confirmed by text similarity), per the stated admit_and_flag policy; operator
  escape hatch is `--override-duplicate-review`.
- Version-diff summaries: fingerprint furniture filter (85% of stored "versions"
  were page furniture; recomputed + pruned), `change_summary` on versions,
  `annotate_version` action, Phase A `updated_docs.json` + diffs, site column.
- Agent risk: credential slimming in the sandbox seed, GH token unset, minimal
  settings seed, deterministic secret scan + LLM screen (fail-closed) before any
  publish, comments outbox (undelivered comments used to vanish silently),
  free-text length caps, shared-host canonical-move hardening.

## Low priority extensions (not scheduled)

- **GitHub Actions**: add `.github/workflows/daily.yml` wrapping `run_daily.sh` + auth
  secrets; delete the crontab line. Prerequisite: the raw store must first move
  somewhere the runner can reach (e.g. a private R2 bucket, same hash-addressed
  keys) — it is the one piece of state that lives outside the repo.
- **Field extraction / eval scores**: populate `extraction` JSON; when stable,
  promote to `eval_results(version_id, benchmark, score, conditions)` — benchmarks
  are *data*, so new benchmarks are rows.
- **Models table** if users start thinking model-first: derive `models` + join table
  from `model_names`; no document-row changes.
- **Scale outgrows Pagefind/static**: sqlite-wasm over HTTP range requests, or D1 +
  a Worker — same SQLite data model either way.
- **related_urls link rot**: periodic HEAD checks for related urls (kept out of
  link_checks deliberately — its per-run MAX(id) dead-strike logic assumes one
  canonical check per doc per run; needs its own table or a url column first).
- Add the categories from Jane's risk monitoring report; consider getting the
  maintenance funded.

## Other options
- Make sure the updated claude report gets published weekly on the website that shows the biggest changes etc
- contact the people at  https://www.themidasproject.com/  who keep track of AI safety policies, but not really system cards.
- Add a "Download everything" button that allows someone to extract the full corpus
