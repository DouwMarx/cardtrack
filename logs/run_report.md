# cardtrack run report — 2026-08-25T06:17Z-local

**Corpus at start:** 250 documents (246 active, 3 removed, 1 moved).
**Corpus at end:** 253 documents (248 active, 4 removed, 1 moved) — net +2 active.
**Proposed this run:** 4 proposals, 4 accepted by the validator (3 `add`, 1 `status_change`); one of
the three adds was mine to remove, and I removed it in the same run.
**Filed as needs-review:** none. **Open issues:** `[]`, unverifiable — see task 4.
**Blocked-URL escalations:** none, and today that is a real zero.

Phase A was **healthy for the first time in three runs**: `checked: 247, ok: 247, not_found: 0,
blocked: 0, errors: 0, fingerprint_checked: 38, new_versions: 16, candidates_new: 20`. So unlike
2026-08-21 and 2026-08-23, the zeros in that line are observations rather than artefacts of a dead
phase, and I did not need to redo the sweep by hand.

Two things nonetheless went wrong underneath a clean-looking run, and they are the substance of this
report: **Phase A silently discarded 10 of the 26 revisions it detected**, and **I reversed a prior
run's editorial judgement on two links without knowing one existed.** Both are filed to
`PROPOSALS.md`.

## Writes

| id | document | publisher | verdict |
|---|---|---|---|
| 251 | [ArmorOCR Model Card](https://huggingface.co/inclusionAI/ArmorOCR) | inclusion_ai | `{"status": "written", "slug": "inclusion-ai-armorocr-model-card", "document_id": 251, "version_id": 388}` |
| 252 | [The Multimodal Intelligence of Muse Spark 1.2](https://research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2) | meta | `{"status": "written", "slug": "meta-muse-spark-1-2-other-2", "document_id": 252, "version_id": 389}` |
| 253 | [DeepSeek-V4-Flash-Vision-Exp Release](https://api-docs.deepseek.com/news/news260821) | deepseek | `{"status": "written", ..., "document_id": 253, "version_id": 390}` — then **removed**, `{"status": "written", "slug": "deepseek-deepseek-v4-flash-vision-exp-other", "document_id": 253}` |

**251 — ArmorOCR** is the clean add and the only one of the three I would defend without
qualification. A 9B vision-language OCR model from InclusionAI (Ant Group), HF `createdAt`
2026-08-20, real weights in four safetensors shards, companion arXiv paper 2608.20122 and a GitHub
repo at `ant-research/ArmorOCR`. Distinct model, not a quant or size variant of any existing row.
Card is thin — quickstart, licence, citation, no inline benchmark tables and no safety content of
any kind — so `has_safety_evals: false`, `has_quantitative_data: false`.
`openness: open_weight_permissive`, verified: Apache-2.0, and its base model
`Qwen/Qwen3-VL-8B-Instruct` is Apache-2.0 too (checked via the HF API rather than assumed). One
search for a co-published copy found none beyond the arXiv paper and GitHub.

It had been sitting in `candidates.json` since **2026-08-22**. It is three days late because the
2026-08-24 run's Phase B died on turn zero (below).

**252 — Meta Muse Spark 1.2 multimodal post.** Kept, but flagged: see the reversal section.

**253 — DeepSeek release note.** Added, then removed by me. See the reversal section.

## The reversal, stated plainly

`research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2` and
`api-docs.deepseek.com/news/news260821` were both fetched, reasoned about carefully, and **skipped by
the 2026-08-22 run**, which recorded why in `friction.jsonl` lines 69 and 70. Nothing in
`candidates.json` or `state_summary.json` carries a trace of that, so I triaged both from scratch,
reached the opposite verdict on both, and wrote them. I found the prior decisions afterwards, while
reading `friction.jsonl` to draft today's entries — by accident, and after the rows were live on the
site.

I did not resolve the two the same way, and the asymmetry is deliberate:

- **253 (DeepSeek) — removed.** The 08-22 call was right and mine was a stretch. The page is headed
  "Multimodal API Now Live"; about half of it is Files API, image-token billing and framework
  support; and its only benchmark numbers are inside a chart image, with no figures in the text at
  all. "Product announcements" is an explicit exclusion for `doc_type: other`. I should not have
  overturned a documented decision on the weaker of two readings, and I reverted within the run.
  The 08-22 run's substantive point survives and is *not* fixed by keeping the row: DeepSeek shipped
  a distinct model on 2026-08-21 with no card anywhere (reconfirmed today — no repo under
  `huggingface.co/deepseek-ai`, newest is V4-Pro-0813), so the corpus records DeepSeek as silent
  since 08-13 when in fact it made an undocumented launch. That is a schema gap, not a row.
- **252 (Meta) — kept, with the disagreement on the record.** Roughly 40% of this post is
  quantitative evaluation that would sit unedited in a model card's evals section: ZeroBench (Muse
  Spark 1.2 54.0 vs GPT-5.6 Sol 54.6, Opus 5 47.5, Muse Spark 1.1 46.0, Gemini 3.7 Flash 30.0),
  SimpleVQA 75.0, CharXiv Reasoning 87.6, Design Arena video-to-website Elo 1279 vs Kimi K3 1243,
  plus the first public description of WildArtifactBench. None of it is published anywhere else —
  the only existing Muse Spark 1.2 row (id 90) is the *methodology* PDF at a different URL, and
  contains none of these scores. The other ~60% is qualitative demo, which on its own would be out
  of scope, and that is exactly what the 08-22 run weighed. `criteria.yaml` policy is
  `when_uncertain: admit_and_flag`; I applied it.

Both calls are defensible, which is the problem. This boundary has now been decided three times
across three runs (`google-deepmind-sl2t-other` admitted, `meta-tribe-v2-other` admitted then
removed, this one skipped on 08-22 and admitted today). It needs one sentence in `criteria.yaml`
rather than a fourth adjudication — filed as `PROPOSALS.md` 2026-08-25 §2.

## Phase A discarded 10 revisions and reported a clean run

The finding I did not go looking for. The changelog for this run id holds 10 rows with
`action=reject` and `reason: "cap_exceeded: max_new_versions_per_run (rolling 24h)"` — ids 123–131
and 133, all Anthropic research/news pages, because the cap fell at a publisher boundary in fetch
order.

The mechanism is cron drift, not a burst of editing. The cap is 30, enforced over a **rolling 24 h
window**, and the daily run creeps earlier: yesterday's versions landed at 06:22:03–06:22:20Z,
today's at 06:18:27–06:19:08Z, about three minutes short of 24 h. So yesterday's 14 were all still
inside the window and two runs shared one budget — I counted exactly 30 rows in `document_versions`
in the 24 h ending at the first rejection. A cap named `max_new_versions_per_run` can start a run 47%
spent.

Phase A's summary line says `new_versions: 16` and nothing else. A run that lost 38% of its revision
detections is indistinguishable in the log from a quiet one. The drops are *deferred* rather than
lost this time — ids 123/124 still carry `last_changed 2026-08-19` against `last_checked 2026-08-25`,
so the next run re-detects them — but convergence is not guaranteed, and if a page changes twice
before its retry lands the intermediate edition disappears with no record. Filed as `PROPOSALS.md`
2026-08-25 §1, whose cheapest ask is a single `versions_rejected_by_cap` field in the summary JSON.

**One revision that did get through is worth naming:** id 8, the GPT-5.5 System Card PDF
(2,367,063 → 2,370,043 bytes), its first change since 2026-08-09. OpenAI's deployment-safety
changelog attributes an 2026-08-19 edit to a correction of GPT-5.5's pass@4 score on the
hard-negative protein-binding evaluation — a safety-eval number corrected in place, captured by the
fingerprint sweep exactly as intended.

## Why ArmorOCR was three days late

The 2026-08-24 run's Phase B never started: `logs/run-20260824-062046Z.log` line 5 is
`API Error: 529 Overloaded`, then `[run_daily] agent exited 1 (continuing to Phase C)`. Phase C
committed Phase A's 14 new versions and deployed, so the run looks productive from the commit log,
and `run_report.md` still described 2026-08-23 when I started this morning.

Credit where due: the run log *is* honest here, so this is not the silent case the 2026-08-17
proposal describes. But the 11 candidates first seen on 08-24, plus the untriaged remainder of the
08-22 batch, sat unlooked-at — and one of them was a real add. Worth noting for whoever builds the
detector that entry asks for: it keys on "changelog has rows for this run id but `run_report.md`
does not name it", which would **not** fire here, because Phase B wrote no changelog rows and Phase
A's rows make the run look fine. A check on `agent exited non-zero` would.

## Task 1 — candidate triage

20 new candidates today plus the 11 from 08-24 that no run had looked at, and a re-check of the 08-22
batch. Everything dispositioned; the two adds above came out of it. The skips:

| candidate | disposition |
|---|---|
| `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-{FP8,BF16}` | out of scope — HF `createdAt` 2025-12-04/06, before the 2026-01-01 floor |
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-{FP8,NVFP4}` | quantization variants of id already held (`…-BF16`, 2026-03-11) |
| `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4` | quantization variant of the BF16 row (2026-04-28) |
| `nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16` | out of scope — `createdAt` 2025-10-21 |
| `nvidia/GEAR-SONIC` | out of scope — card and paper (arXiv 2511.07820) both dated 2025-11-11; repo `createdAt` 2026-02-12 is a publication artefact |
| `hf.co/collections/tencent/wemm-embedding` | empty collection — "This collection has no items" |
| `deepmind.google/blog/from-atari-to-eve-online…` | 08-21 retrospective + Fenris/EVE partnership announcement; no named model evaluated |
| `epoch.ai/publications/the-nvidia-sized-hole-in-us-gdp-statistics` | 08-24, macroeconomics, no named model |
| `epoch.ai/benchmarks/ebr-bench` | benchmark hub page, not a publication |
| `rand.org/…/RRA4496-{1,2}`, `EP71466` | nucleic-acid biosecurity and pandemic-preparedness policy; RAND is allowlisted scoped to CAST/Canary model-eval output |
| `mistral.ai/news/mistral-x-humain` | partnership announcement |
| `x.ai/news/{grok-4-6-vertex-ai, grok-bot-more-plans, grok-build-for-everyone}` | availability/product announcements |
| `api-docs.deepseek.com/guides/{vision,files_api}` | developer tutorials |
| `inclusionAI/Ling-3.0-flash-dspark` | speculative-decoding draft model for a catalogued target — same call as 08-22 |
| `inclusionAI/ConceptEdit-{12M,Bench}`, `nvidia/…-dataset` | datasets, not models |
| `huggingface.co/papers/{2608.12781, 2608.16812, 2608.18077}` | research papers (incl. NVIDIA "Hydra-0"); no corresponding model repo, and none evaluates a named released model |
| `anthropic.com/research/team/economics`, Qwen/NVIDIA/InclusionAI user profiles, Palisade nav links | page furniture |

Two Qwen candidates are worth a line: the HF discussion threads
`Qwen3.8-27B/discussions/158` and `Qwen3.8-2.4T-A95B/discussions/38` are both titled "Add
Terminal-Bench evaluation results". Not documents themselves, but they signal edits to two
catalogued cards — i.e. fingerprint-sweep work, and neither card was in today's sampled 38.

## Task 2 — targeted search

Searched the ~72 h window for new cards and evals across the frontier labs and the evaluator list,
and checked the long-silent orgs. **Nothing proposable.** METR's most recent is still the GPT-5.6 Sol
predeployment evaluation (2026-06-26, already held). UK AISI's most recent is the 2026-08-04 incident
report `INC-2026-07-28-01` — already held as id from that date. Epoch has published nothing
model-specific since 2026-08-14 (`epoch.ai/latest` items since 08-15 are the GDP piece and
employer-plan/chip-economics data insights). Apollo, Transluce, Palisade, SaferAI, FAR.AI, US CAISI:
nothing new. No frontier-lab card appeared in the window.

Because Phase A fetched all 43 configured index pages cleanly today (`errors: 0`), the orgs reading
as silent are genuinely quiet rather than unfetched — a distinction the last two runs could not make.

## Task 3 — citation mining

Mined the recently-added and recently-revised rows. **No leads.** Anthropic's
`/research/exploit-evals` (revised, id 121) cites ExploitBench (CMU/Bugcrowd), ExploitGym
(Berkeley/MPI-SP/UCSB/ASU), CyberGym, OSS-Fuzz and DefiHackLabs — academic benchmarks and datasets,
no allowlisted evaluator among them. The ArmorOCR card cites only its own arXiv paper and its Qwen3-VL
base. This matches the pattern the last several runs report: HF cards cite benchmarks and base
models, first-party research posts cite their own prior work, and third-party evaluator references
appear almost exclusively in frontier-lab system cards — none of which were published this window.

## Task 4 — open issues

`logs/open_issues.json` is `[]` for the **fourth consecutive run**, and again I cannot distinguish
"no open issues" from "could not ask": `gh` in this sandbox is unauthenticated ("You are not logged
into any GitHub hosts"). `comment_issue.py` was not called.

One thing is different today and it cuts toward the benign reading: on 08-21 and 08-23 the empty list
coincided with a failing Phase A, so a failed fetch was the likelier explanation. This run Phase A was
fully healthy, which makes a genuinely empty backlog more plausible. It remains an inference rather
than an observation, so **task 4 is reported as completed against unverifiable input**, not as
completed-with-nothing-found. Remedy already requested (2026-08-14 proposal; the `fetch_status` field
asked for in the 2026-08-21 entry); not re-filed.

## Task 5 — blocked-URL escalations

`blocked_escalations` is empty, and unlike 08-23 this is informative: `checked: 247, ok: 247,
blocked: 0` means every active document was link-checked and none was blocked or missing. Nothing to
escalate, nothing to mark dead. Note that yesterday's run did report `blocked: 2`; those two are back
to `ok` today, so they were transient bot-walls, not dead documents.

## Task 6 — friction logged (5 lines)

`rolling_cap_silently_discards_revision_detections` ·
`prior_adjudication_reversed_because_skip_decisions_are_not_machine_readable` ·
`empty_open_issues_list_is_indistinguishable_from_a_failed_issue_fetch` ·
`phase_b_died_on_turn_zero_leaving_the_candidate_backlog_untriaged` ·
`quantitative_data_lives_only_inside_an_image`

## Task 7 — proposals filed (2)

Both are new asks, not restatements:

1. **`max_new_versions_per_run` is not per run, and this run silently dropped 10 revision
   detections** — the rolling-24 h window versus a run cadence that drifts earlier, with the fix
   ordered cheapest-first (report the drops; match the window to the cadence; defer instead of
   reject).
2. **Skip decisions live only in a prose log nothing reads, and today that flipped two published
   verdicts** — asks for a machine-readable `decisions` map carried across runs, a `reverses:
   <run_id>` stamp in the changelog when a proposal overturns a recorded skip, and one sentence in
   `criteria.yaml` settling the showcase-with-benchmark-tables boundary.

Everything else I hit maps onto an existing entry and was left to friction: the stale-audit-trail
consequence of the 08-24 crash onto 2026-08-17, the unverifiable issue list onto 2026-08-14 and
2026-08-21, the draft-model and pre-floor-re-upload skips onto 2026-08-22 and 2026-08-19.
