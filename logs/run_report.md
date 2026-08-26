# cardtrack run report — 2026-08-26T06:50Z-local

**Corpus at start:** 253 documents (248 active, 4 removed, 1 moved).
**Corpus at end:** 258 documents (253 active, 4 removed, 1 moved) — net +5 active.
**Proposed this run:** 5 proposals, 5 accepted by the validator, all `add`, no rejects, no
needs-review filings, nothing removed.
**Open issues:** `[]`, unverifiable — see task 4. **Blocked-URL escalations:** none, and it is a real
zero.

Phase A was healthy again: `checked: 249, ok: 249, not_found: 0, blocked: 0, errors: 0,
fingerprint_checked: 38, new_versions: 19, candidates_new: 18`. The zeros are observations, not the
artefacts of a dead phase.

**Yesterday's cap finding did not recur, and the reason confirms the diagnosis rather than weakening
it.** The 2026-08-25 run lost 10 revision detections to `max_new_versions_per_run` because the cron
drifted ~3 minutes *earlier* and two runs shared one rolling-24 h budget. Today the run started
later — yesterday's versions landed 06:18:27–06:19:08Z, today's from 06:51:25Z, about 24 h 33 m
apart — so yesterday's 16 had aged out and all 19 of today's were written. Zero `cap_exceeded` rows
this run. That is the same mechanism producing the opposite outcome from a few minutes of drift,
which is exactly the point of `PROPOSALS.md` 2026-08-25 §1: whether a revision is recorded currently
depends on cron jitter. Not re-filed.

The substance of this run is a **four-month-old coverage hole**: the entire NVIDIA Ising family was
missing from a corpus that already held 32 NVIDIA rows.

## Writes

| id | document | publisher | verdict |
|---|---|---|---|
| 254 | [WeMM-Embedding-9B Model Card](https://huggingface.co/tencent/WeMM-Embedding-9B) | tencent_hunyuan | `{"status": "written", "slug": "tencent-hunyuan-wemm-embedding-2b-model-card", "document_id": 254, "version_id": 410}` |
| 255 | [Ising-Decoder-SurfaceCode-1-Fast model card](https://huggingface.co/nvidia/Ising-Decoder-SurfaceCode-1-Fast) | nvidia | `{"status": "written", "slug": "nvidia-ising-decoder-surfacecode-1-fast-model-card", "document_id": 255, "version_id": 411}` |
| 256 | [Ising-Decoder-ColorCode-1-Fast model card](https://huggingface.co/nvidia/Ising-Decoder-ColorCode-1-Fast) | nvidia | `{"status": "written", "slug": "nvidia-ising-decoder-colorcode-1-fast-model-card", "document_id": 256, "version_id": 412}` |
| 257 | [NVIDIA-Ising-Calibration-1-35B-A3B model card](https://huggingface.co/nvidia/Ising-Calibration-1-35B-A3B) | nvidia | `{"status": "written", "slug": "nvidia-nvidia-ising-calibration-1-35b-a3b-model-card", "document_id": 257, "version_id": 413}` |
| 258 | [NVIDIA-Ising-Calibration-1.5-31B-BF16 model card](https://huggingface.co/nvidia/Ising-Calibration-1.5-31B-BF16) | nvidia | `{"status": "written", "slug": "nvidia-nvidia-ising-calibration-1-5-31b-bf16-model-card", "document_id": 258, "version_id": 414}` |

**254 — WeMM-Embedding (2B / 4B / 9B)** is the only genuinely *new* document this run. Tencent's
universal multimodal embedding family, repos created 2026-08-25 03:10Z, built on Qwen3.5-2B/4B/9B,
with a technical report (arXiv 2608.24053) and code at `Tencent/WeMM-Embedding`. The card carries
head-to-head MMEB-v2 (78 datasets) and MMEB-v3 (190 tasks) tables against VLM2Vec, GME,
Qwen3-VL-Embedding, E5-Omni and Omni-Embed-Nemotron — quantitative evaluation that would sit
unedited in a model card's evals section. `has_safety_evals: false`: it is quickstart, serving
configs and retrieval benchmarks, with no safety, red-teaming, misuse or risk content at all.
`openness: open_weight_permissive` verified from the repo `LICENSE` file rather than the tag — HF
metadata reads `license: other` / `license_name: apache-2.0`, and the LICENSE text puts the
parameters and weights under Apache-2.0; all three Qwen3.5 base models are Apache-2.0 too, checked
via the HF API.

Worth noting against yesterday's candidate churn: the 2026-08-25 run recorded
`hf.co/collections/tencent/wemm-embedding` as an *empty* collection and skipped it. That was correct
at the time — the model repos landed the same day but had not been attached to the collection yet.
The link was right, the artefact was not there. That is a near-miss for the same "no triage state"
problem, in the direction of a skip that had to be re-decided rather than a verdict that got
reversed.

**255–258 — the NVIDIA Ising family.** Four documents, none of them new, all of them missing:

| id | model(s) | card's stated release date | licence → openness |
|---|---|---|---|
| 255 | `Ising-Decoder-SurfaceCode-1-Fast` + `-Accurate` | April 14, 2026 | NVIDIA Open Model License → restrictive |
| 256 | `Ising-Decoder-ColorCode-1-Fast` | 07/21/2026 | OpenMDW-1.1 → permissive |
| 257 | `NVIDIA-Ising-Calibration-1-35B-A3B` | April 14, 2026 | NVIDIA Open Model License → restrictive |
| 258 | `NVIDIA-Ising-Calibration-1.5-31B-BF16` | 07/23/2026 | OpenMDW-1.1 + Gemma 4 base → **unset** |

These are not obscure checkpoints. NVIDIA announced the Ising family on 2026-04-15 with a developer
blog post and a product page at `nvidia.com/en-us/solutions/quantum-computing/ising`, there are two
arXiv papers (2604.12841 for the surface-code decoders, 2607.10058 for the color-code one), a public
training framework at `github.com/NVIDIA/Ising-Decoding`, and independent trade coverage of the July
release. Each card is a full Model Card++ with architecture, datasets and quantitative Evaluation
Results (≥2× logical-error-rate reduction vs PyMatching, up to 4× at distance-31 for the surface-code
pair; ~356× at distance-31 for ColorCode; QCalEval 74.7% vs 55.5% for the Qwen3.5 base on
Calibration-1).

All four are `has_safety_evals: false`, which matches the corpus's treatment of **all 32** existing
NVIDIA rows: the Ethical Considerations paragraph and the Model Card++ subcard links (bias,
explainability, safety & security, privacy) are boilerplate, not an evaluation. I checked the
existing rows before attesting rather than deciding it fresh.

Three of the four decisions I want to flag explicitly:

- **Row granularity.** SurfaceCode `-Fast` and `-Accurate` are two URLs, same paper, same stated
  release date, differing only in R=9 vs R=13 and 0.9M vs 1.8M parameters — one row, both names.
  WeMM 2B/4B/9B likewise. `criteria.yaml`'s family rule says one row; the rule suggested on
  2026-08-19 ("one distinctly-authored card at its own URL is one row") says two and three. I
  followed the corpus's own Tencent precedent (`tencent-hunyuan-ui-mate-27b-model-card` merges
  UI-Mate-27B/-9B/-democua-27B). This is now the fourth and fifth adjudication of that question and
  it is still unwritten. Logged to friction, not re-filed.
- **ColorCode's date is contested and I recorded the weaker-looking one.** The card's own Release
  Date field says 07/21/2026; HF `createdAt` is 2026-07-15 and press coverage of the release is
  dated 2026-07-15. I used the card's self-stated date per the "document's own publication date"
  rule and put the discrepancy in `notes` rather than silently picking the tidier number.
- **258's `openness` is deliberately unset.** See the proposal below.

## The coverage hole, stated plainly

`huggingface.co/nvidia` is a configured `index_url` fetched successfully on every run. These four
repos have existed since 2026-03-30, 04-06 and 07-13/15. They entered the corpus today because
someone edited three README files on 2026-08-25 between 17:47 and 17:51Z — four months late, and by
accident.

And the accident was partial: **only the three decoder repos ever appeared in `candidates.json`.**
The two Calibration models were never candidates at any point. I found them by taking the one useful
thing the decoder cards gave me — the family name — and searching for the announcement, which led to
the NVIDIA blog, which led to the other half of the family.

This is the second confirmed instance of `PROPOSALS.md` 2026-08-19 §1 (the first was the entire
Qwen3.5 generation), so I have not re-filed it. But today adds one thing that entry did not
anticipate and that I have written into friction: its suggested ranking — *"rank by downloads so the
agent triages a 13.8M-download model card before a 200-download SAE probe"* — **would have buried
this find**. The three decoders have 170, 36 and 17 downloads and 17, 11 and 5 likes. Downloads
measure adoption, not whether a document is a canonical release record. Oldest-unheld-first, or
"has a first-party announcement or arXiv paper", would rank these correctly; downloads rank them
last.

## Task 1 — candidate triage

18 new candidates. Five became the two proposal threads above (three directly, two by following
them); the rest:

| candidate | disposition |
|---|---|
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-Base-BF16` | base twin of the held `…-A12B-BF16` row (2026-03-11); `createdAt` 2026-03-10, same release. Matches the corpus's own note on the Lightning row, which records `-Base-BF16` as deliberately not proposed |
| `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-Base-BF16` | out of scope — `createdAt` 2025-12-03, before the 2026-01-01 floor (same call as 08-25 on its FP8/BF16 siblings) |
| `nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-FP8` | quantization variant of the held BF16 row (2026-04-28) |
| `nvidia/Cosmos3-Edge/discussions/63` | an HF discussion thread ("Add August 2026 checkpoint update notice"), not a document — but it signals an edit to catalogued id `nvidia-cosmos3-edge-model-card`, i.e. fingerprint-sweep work |
| `rand.org/pubs/research_reports/RRA4704-1` (SL3, 2026-08-25) | security-controls framework (262 controls for protecting model weights), no named model evaluated — fails the system-card test. RAND is allowlisted scoped to CAST/Canary model-eval output, and all six held RAND rows carry `model_names`. Same call as 08-25 on RRA4496 |
| `palisaderesearch.org/blog/palisade-podcast-daniel-kokotajlo` | podcast episode, no named model evaluated |
| `anthropic.com/news/wellbeing-research-grants` | funding announcement |
| `cursor.com/blog/imdex` | customer case study |
| `huggingface.co/papers/2608.24053` | the WeMM technical report's HF paper page; the release itself is catalogued as id 254, and the paper page is an aggregator entry rather than the primary artefact |
| `huggingface.co/tencent/WeMM-Embedding-{4B,2B}` | covered by id 254, sibling URLs recorded in its `notes` |
| `huggingface.co/{JUNJIE99, tangyue0820, ibasov}` | user profiles — page furniture |

**One co-publication check, per the rule.** `cursor.com/grok` was in the older candidate backlog and
Cursor is allowlisted precisely because it co-publishes Grok cards. Fetched it: the page links the
Grok 4.6 model card, but at `media.x.ai/v1/website/card-4p6-4cd2dc57.pdf` — x.ai's own URL, which is
already held as `xai-grok-4-6-model-card` (id 203). There is no Cursor-hosted copy this time, so
there is no second document and nothing to cross-reference. `x.ai/news/grok-4-6` is the announcement
post, not the card.

## Task 2 — targeted search

Swept the ~72 h window and every org silent for more than 14 days. **Nothing proposable beyond the
Ising family**, which is itself the product of this task rather than of candidate triage.

- **OpenAI** — `deploymentsafety.openai.com` still tops out at the GPT-5.6 August Updates addendum
  (2026-08-06), already held as id at that date. `openai.com/news/` returns HTTP 403 to WebFetch, as
  `sources.yaml` warns; searched around it and found nothing newer than the 08-10 Daybreak post,
  which is held.
- **METR** — `metr.org/evaluations/` now 302-redirects to `metr.org/risk-assessment/`, a consolidated
  index of every METR evaluation report, review and risk report. Read it in full: nothing dated
  2026-07-22 or later. The newest evaluation report is still GPT-5.6 Sol (2026-06-26) and the newest
  Frontier Risk Report is still February–March 2026, both held.
- **SaferAI** — the GLM-5.2 Risk Evaluation Report PDF that surfaced in search
  (`safer-ai.org/u/2026/08/SaferAI-GLM-Evaluation-Report.pdf`) is the attachment of the held
  `safer-ai.org/research/glm-5-2-evaluation-report` row (2026-08-02), not a second document.
- **Epoch AI** — "Expanding our analysis of biological AI models" is dated 2026-02-20 and is a
  1,196-entry database expansion with aggregate statistics, not an evaluation of a named model.
  Fails the system-card test. Nothing model-specific since the held 07-31 data insight.
- **DeepSeek** — reconfirmed yesterday's finding: V4-Flash-Vision-Exp (released 2026-08-21) still has
  no model card anywhere. No repo under `huggingface.co/deepseek-ai` newer than V4-Pro-0813, and the
  only artefact remains the API release note that the 08-22 run skipped and the 08-25 run added and
  then removed. The corpus continues to record DeepSeek as silent since 08-13 when it in fact made an
  undocumented launch — still a schema gap, still not a row.
- **UK AISI, US CAISI, Apollo, Transluce, Palisade, FAR.AI, SecureBio, RAND, Redwood, Mistral,
  Moonshot, Qwen, Thinking Machines, poolside, StepFun, Xiaomi** — nothing new in the window.
  Because Phase A fetched all configured index pages cleanly (`errors: 0`), the orgs reading as
  silent are genuinely quiet rather than unfetched.

## Task 3 — citation mining

Scanned all 140 documents re-fetched since 2026-08-12 for references to the 13 allowlisted
evaluators plus generic "external/third-party evaluation" phrasing. **No leads.** Every named
citation resolves to something already held:

- `anthropic-claude-mythos-5-other-2` (the August 2026 Risk Report) is the richest source — METR ×14,
  AISI ×23, SecureBio, Epoch AI, RAND, Redwood Research. Its two pilot-external-review citations
  point at METR's R&D-section review (held, 2026-05-08) and SecureBio's review of Anthropic's
  unredacted chemical sections (held, 2026-07-28). Its "METR's recent Frontier Risk Report" is the
  Feb–Mar 2026 report (held); METR's own index confirms no later one exists. The Epoch, RAND and
  Redwood mentions are references to methodology and a 2024 paper, not to evaluations of a covered
  model.
- `thinking-machines-inkling-addendum` names Apollo Research, FAR.AI, Scale AI and Handshake AI as
  pre-deployment testers, but describes their findings inline rather than linking published reports;
  Scale AI and Handshake AI are not allowlisted. No separate document to propose.
- `xai-grok-4-6-model-card` refers twice to "third-party evaluators" without naming any.
- The two Anthropic PDFs added on 08-18 (ids 231, 232) are Claude Science application papers —
  de novo protein binder design and NMR/LC-MS processing — and contain no evaluator citations at
  all.

This matches the standing pattern: HF cards cite benchmarks and base models, first-party research
posts cite their own prior work, and third-party evaluator references live almost entirely in
frontier-lab system cards, none of which were published in this window.

## Task 4 — open issues

`logs/open_issues.json` is `[]` for the **fifth consecutive run**, and I again cannot distinguish
"no open issues" from "could not ask": `gh` in this sandbox is unauthenticated ("You are not logged
into any GitHub hosts"). `comment_issue.py` was not called. As on 08-25, Phase A was fully healthy
this run, which makes a genuinely empty backlog the more plausible reading — but it stays a reading.
**Task 4 is reported as completed against unverifiable input**, not as completed-with-nothing-found.
Remedy already requested (2026-08-14 proposal; the `fetch_status` field asked for on 2026-08-21);
not re-filed.

## Task 5 — blocked-URL escalations

`blocked_escalations` is `[]`, and it is informative rather than empty-by-failure: `checked: 249,
ok: 249, not_found: 0, blocked: 0` means every active document was link-checked and none was blocked
or missing. Nothing to escalate, nothing to mark dead.

One related observation logged to friction: the three gated NVIDIA Ising repos (`gated: auto`) serve
their full Model Card++ body at `huggingface.co/<repo>` (HTTP 200) but return an authentication error
at `huggingface.co/<repo>/raw/main/README.md`. The validator accepted all three, so the fetch path
evidently uses the rendered page — recording it because any future change that prefers `/raw/` for
cleaner extraction would silently start losing gated cards while the link-checker kept reporting them
`ok`.

## Task 6 — friction logged (6 lines)

`index_diff_backlog_blindness_second_instance_and_the_proposed_ranking_would_have_buried_it` ·
`openness_has_no_rule_for_base_model_license_flowthrough_and_the_corpus_is_already_split` ·
`family_row_granularity_ambiguity_bit_twice_more_this_run` ·
`slug_is_derived_from_the_alphabetically_first_model_name_not_the_canonical_document` ·
`empty_open_issues_list_is_indistinguishable_from_a_failed_issue_fetch` ·
`gated_hf_repos_serve_the_card_publicly_but_not_via_the_raw_readme_path`

## Task 7 — proposals filed (1)

**`openness` has no rule for derivative licences, and the corpus has already split the same licence
tag eleven ways.** New; nothing in `PROPOSALS.md` mentions `openness` and `criteria.yaml` does not
contain the key at all. Id 258's card names OpenMDW-1.1 as its governing terms and never mentions
Gemma, while stating in another section that the model "was developed based on `google/gemma-4-31b`"
— a use-restricted community licence that normally flows through. Both readings are defensible and
produce opposite values, so I left the field unset, which makes the row indistinguishable from one
nobody looked at. The corpus has already answered the identical question both ways without recording
that it did: thirteen rows carry `openmdw-1.1` and nothing else, ten marked permissive and three
marked restrictive, with no field saying why. The ask is one sentence of flowthrough rule in
`criteria.yaml` (most restrictive licence a user must accept governs; conflict + unconfirmed
flowthrough → record the more restrictive value and say so), plus an `openness_basis` companion so
the judgement is auditable, plus a backfill of the three restrictive OpenMDW rows.

Everything else maps onto an existing entry and was left to friction: the four-month coverage hole
onto 2026-08-19 §1 (with the download-ranking correction recorded there), the two granularity calls
onto 2026-08-19 §2 and 2026-08-20, the unverifiable issue list onto 2026-08-14 and 2026-08-21, and
the cap non-recurrence onto 2026-08-25 §1.
