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
