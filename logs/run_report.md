# cardtrack run report — 2026-08-21T07:27Z-local

**Corpus at start:** 240 documents (236 active, 3 removed, 1 moved). **Written this run:** 8 adds
(ids 241–248). **Filed as needs-review issues:** 2 (`outbox:1`, `outbox:2`). **Rejected:** none.
**Open issues:** unknown — see the caveat below. **Blocked-URL escalations:** none.

## Phase A did not work, and that is this run's headline

`checked: 237, ok: 0, not_found: 0, blocked: 0, errors: 237, fingerprint_checked: 36,
new_versions: 0, candidates: 2660, candidates_new: 0`.

Every fetch errored. This is the **fifth** occurrence of the silent-total-failure pattern first logged
2026-08-14. At 08:05Z I re-swept all 43 configured `index_urls` by hand from the same venv via
`cardtrack.fetch` and got **43/43 HTTP 200**; every document fetch inside this run's nine proposals also
succeeded. The failure was transient and total, not publisher-side.

Three things were lost silently, and the log reports all three as if the day had been clean:

- **No link diffing.** `candidates_new: 0` means no diff ran, not that nothing was published. I redid
  the diff by hand — 94 links on the index pages absent from both `candidates.json` and the corpus, five
  of them content rather than furniture. One became the `outbox:2` proposal (below). Without the hand diff
  this run would have found nothing new anywhere.
- **No link-checking.** `ok: 0` means not one active document was checked, so `marked_dead: 0` today
  carries no information.
- **No revision sweep.** `fingerprint_checked: 36 / new_versions: 0` is indistinguishable from 36
  failed fetches.

Phase B also logged `error connecting to api.github.com` twice. **`logs/open_issues.json` is `[]` but
that value is unverified** — with the API unreachable, the fetch cannot tell "no open issues" from
"could not ask". Task 4 is therefore completed as far as possible against unknown input, not
completed-with-nothing-found. Both issues this run filed landed in `logs/issues_outbox.jsonl` rather
than on GitHub and will be seen only if the outbox is drained.

## Added (8) — a backlog sweep at the corpus's thinnest publishers

Every card below was fetched and read in full, and dated from its HuggingFace commit history rather
than from repository metadata alone. All are Apache-2.0 or MIT, hence
`openness: open_weight_permissive`. **`has_safety_evals` is false on all eight**, verified by reading
plus a keyword sweep for safety/risk/harm/red-team/jailbreak/refusal/misuse over each full card: not one
contains a safety section, red-teaming result, or risk assessment.

| id | document | date | verdict |
|---|---|---|---|
| 241 | [Step 3.5 Flash](https://huggingface.co/stepfun-ai/Step-3.5-Flash) | 2026-02-01 | `{"status": "written", "slug": "stepfun-step-3-5-flash-model-card", "document_id": 241, "version_id": 331}` |
| 242 | [STEP3-VL-10B](https://huggingface.co/stepfun-ai/Step3-VL-10B) | 2026-01-13 | `{"status": "written", "slug": "stepfun-step3-vl-10b-model-card", "document_id": 242, "version_id": 332}` |
| 243 | [Step-Audio-R1.1](https://huggingface.co/stepfun-ai/Step-Audio-R1.1) | 2026-01-14 | `{"status": "written", "slug": "stepfun-step-audio-r1-1-model-card", "document_id": 243, "version_id": 333}` |
| 244 | [Ling-2.6-1T](https://huggingface.co/inclusionAI/Ling-2.6-1T) | 2026-04-29 | `{"status": "written", "slug": "inclusion-ai-ling-2-6-1t-model-card", "document_id": 244, "version_id": 334}` |
| 245 | [Ling-2.6-flash](https://huggingface.co/inclusionAI/Ling-2.6-flash) | 2026-04-28 | `{"status": "written", "slug": "inclusion-ai-ling-2-6-flash-model-card", "document_id": 245, "version_id": 335}` |
| 246 | [Ring-2.6-1T](https://huggingface.co/inclusionAI/Ring-2.6-1T) | 2026-05-14 | `{"status": "written", "slug": "inclusion-ai-ring-2-6-1t-model-card", "document_id": 246, "version_id": 336}` |
| 247 | [LLaDA2.2-flash](https://huggingface.co/inclusionAI/LLaDA2.2-flash) | 2026-07-16 | `{"status": "written", "slug": "inclusion-ai-llada2-2-flash-model-card", "document_id": 247, "version_id": 337}` |
| 248 | [Qwen3-ASR family](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | 2026-01-28 | `{"status": "written", "slug": "alibaba-qwen-qwen3-asr-0-6b-model-card", "document_id": 248, "version_id": 338}` |

**How these surfaced.** Not from a release event. StepFun held **one** row for a publisher with a full
2026 lineup, and InclusionAI held two, both from August, while the Ling 2.6 and Ring 2.6 generations and
the LLaDA2 diffusion line sat uncatalogued. A HuggingFace-API sweep by creation date across seven orgs
found them. `huggingface.co/stepfun-ai`, `huggingface.co/inclusionAI` and `huggingface.co/Qwen` are all
configured `index_urls` fetched successfully every run — but a January release stops being a new link in
January. That is the third and fourth independent instance of the backlog blindness logged on 2026-08-19
(Qwen3.5) and 2026-08-20 (NVIDIA GR00T), now at two more publishers.

**Substance worth flagging.** Step 3.5 Flash is a 196B-total/11B-active MoE claiming SWE-bench Verified
74.4 and AIME 2025 97.3 against DeepSeek V3.2, Kimi K2.5 and GLM-4.7, with 160k downloads and 834 likes
— a frontier-class open model that has been missing for six months. Ling-2.6-1T and Ring-2.6-1T are
trillion-parameter flagships (508 and 105 likes) sharing arXiv 2606.15079. Qwen3-ASR is the largest
single miss by usage: **4,498,936 downloads on the 1.7B and 4,118,924 on the 0.6B**, catalogued as one
row because the card is explicitly a family card covering the 1.7B, the 0.6B and Qwen3-ForcedAligner-0.6B.
STEP3-VL-10B's card carries a first-party correction notice — StepFun apologising for wrong Qwen3VL-8B
comparison numbers caused by a `max_tokens` misconfiguration — which is exactly the provenance a
version-tracked corpus exists to hold.

**Granularity calls, flagged for reversal if wrong.** Ling-2.6-1T and Ling-2.6-flash are proposed as two
rows, following the corpus's existing treatment of Ling-3.0-flash and Ling-3.0-tiny as two rows. All
`-base`, `-base-30T`, `-base-midtrain`, `-fp8`, `-int4`, `-FP8`, `-GGUF`, `-NVFP4` and `-hf` siblings
are excluded as checkpoint/quantisation/format variants, consistent with the 2026-08-20 treatment of the
Ling-3.0 base checkpoints. This is the same unresolved granularity question logged on 08-19 and 08-20;
I applied per-publisher consistency as the tiebreaker.

## Filed as needs-review issues (2)

**`outbox:1` — Claude Opus 5 System Card canonical URL.** `{"status": "issue_filed", "reason":
"canonical_url_content_mismatch", "document_id": 2, "issue_ref": "outbox:1"}`. The corpus holds the
193-page `c5fbac3f…` edition; `anthropic.com/transparency/model-report` as fetched today links **only**
the 194-page `b514064a…` edition, and the orphaned old hash still returns 200 so no link-check will
notice. **This corrects the 2026-08-18 run, which cleared this pair as "repagination only — full
word-diff shows no content change".** Re-diffed with `pdftotext` + page-number stripping +
`difflib.SequenceMatcher`, the revision is substantive: Table 8.1.A's FrontierBench v0.1 row changed
from `43.3 | 18.7 | 33.7 | 37.5` to `43.3 | 21.1 | 33.8 | 34.4` (Opus 4.8 18.7→21.1, Fable 5 33.7→33.8,
GPT-5.6 Sol 37.5→34.4), plus a new Harbor attribution line, a new ~128-word note on FrontierCode's
decline above high effort, and a rewritten §8 opening. The corpus and public site are serving superseded
benchmark numbers for a flagship system card. No proposal action can fix this — `add` would create a
duplicate row and `new_version` rejects any URL a document does not already carry — so the needs-review
issue is the designed outcome, not a deferral.

**`outbox:2` — Muse Spark 1.2 Multimodal Evaluation Methodology.** `{"status": "issue_filed", "reason":
"logical_duplicate_of:meta-muse-spark-1-2-other", "issue_ref": "outbox:2"}`. A genuine new document
(2026-08-20, 4 pp, first-party, found only because I redid Phase A's diff by hand) tripped the
title-similarity duplicate check against the 2026-08-05 `Muse Spark 1.2 & Muse Code Evaluation
Methodology`. Different URL, fifteen days apart, disjoint benchmark suites (multimodal vs coding), both
linked by Meta from different posts, and the content fingerprint did not fire. I proposed it under its
true title rather than perturbing it to slip past the check. Full argument in today's `PROPOSALS.md` §3.

## Checked and deliberately not proposed

- **`research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2`** (2026-08-20) — read in full. A
  capability showcase: robotics demo videos, an interactive flipbook, Design Arena rankings. Excluded by
  the `other` scope-discipline rule against capability demos. Its value was the link it carried to the
  methodology PDF proposed above.
- **`transluce.org/scaling-activation-oracles`** (2026-08-20) — the closest call, and a recurrence of
  yesterday's. Trains activation oracles over Qwen3-8B/14B/32B, Qwen3.6-27B, GLM-4.5 358B and
  Kimi-K2.6 1.1T, evaluated on evaluation-awareness prediction and reward-hacking detection via
  ImpossibleBench. Skipped on the same discriminator as yesterday's `elicitation-scaling-laws`: the
  numbers describe the *oracle's* detection ability, not the subject models' safety. Two skips in two
  days on a rule that is not written down anywhere — see the friction line.
- **`transluce.org/foundation-models-for-oversight`** (2026-07-28) — research agenda for "Pythonic world
  models"; names Claude Opus 4.8, Qwen3-32B, GPT-OSS-120B as illustrations but reports no empirical
  results. `transluce.org/oversight-foundations` is the series hub page, not a document.
- **`securebio.substack.com/p/securebio-detection-updates-august`** (2026-08-20) — biosurveillance
  operations report; mentions Claude Managed Agents, Claude Tag and GPT Rosalind as internal tooling.
  Fails the system-card test.
- **`mistral.ai/news/agentic-search`** (2026-08-20) — a retrieval toolkit, not a model. Reports
  FinanceBench 26.7%→86% and OfficeQA Pro +45.6 points, but for a search layer, not a named model.
- **`x.ai/news/grok-build-for-everyone`** (2026-08-19), **`x.ai/news/grok-4-6-amazon-bedrock`**,
  **`grok-4-6-github-copilot`** — product and availability announcements.
- **`blog.google/.../introducing-gemini-3-7-flash/`** — announcement for a model whose card the corpus
  already holds; `ai.google.dev` DiffusionGemma and Gemma 4 model cards are already held (ids at
  2026-06-10 and 2026-04-02).
- **`www.rand.org/pubs/research_reports/RRA5043-1.html`** (2026-08-17) — fetched with a browser UA after
  a 403. A dataset study of US and Chinese AI developer firms; policy analysis, no named model
  evaluated, and outside RAND's CAST/Canary eval scope.
- **RAND `PEA4952-1`, `RRA4999-1`, `RRA5083-1`** (2026-08-18) — mirror biology, biosecurity
  defense-in-depth, PPE prioritisation. No named model.
- **`epoch.ai/gradient-updates/9-big-questions-benchmarks-can-help-answer`** (2026-08-14) and three
  data-insights posts — general analysis, no named model evaluated.
- **`metr.org/blog/2026-08-14-funding-update/`** — organisational news.
- **`api-docs.deepseek.com/news/news260813`** — GA announcement for DeepSeek-V4-Pro-0813, whose card the
  corpus holds.
- **`anthropic.com/news/claude-text-watermark`**, **`academy.claude.com`**, **`/company/leadership`** —
  feature announcement and site navigation.
- **Cursor `git-at-any-scale`, `origin-code-hosting`, `08-19-26`, `joining-spacex`, `firetiger`,
  `aiuc-1`, `builds`** — company, product and changelog posts.
- **`nvidia/Nemotron-Labs-Audex-2B`, `nvidia/Cosmos3-Edge-Policy-DROID`, `tencent/UI-Mate-9B`,
  `tencent/UI-Mate-democua-27B`** — re-verified against the database as already inside existing rows'
  `model_names`.
- **`nvidia/Kimi-K3-NVFP4`, `nvidia/DeepSeek-V4-{Pro,Flash}-nvfp4-DSpark`, `Qwen/Qwen3.8-27B-FP8`,
  `Qwen/Qwen3.8-2.4T-A95B-FP8`** — quantisation re-uploads.
- **InclusionAI Ling-3.0 base checkpoints ×6, `ArmorOCR`** (2026-08-20, 0 downloads, 3 likes) — variants
  and a release too thin for `notable_release` today; ArmorOCR is worth re-checking next run.
- **HF `/papers/2608.13580` (Jais 2), `/papers/2608.16393`, `/papers/2608.17566`, `/papers/2608.19758`,
  `/papers/2608.10835`, `/papers/2608.13391`** — surfaced under publisher index pages but are
  unaffiliated arXiv listings; filing them under those publishers' keys would attribute one org's work to
  another.
- **HF collections, dataset repos, `/discussions/` threads, Spaces and org-member profile pages** — page
  furniture.

## Targeted search and silent-org audit

Beyond the hand-redone index diff, I checked directly: `anthropic.com/transparency/model-report` (which
is how the Opus 5 edition change was confirmed), `deploymentsafety.openai.com` (most recent entry still
GPT-5.6 August Updates, 2026-08-06 — **GPT-5.6-Cyber's promised full system card has still not appeared,
seventh consecutive run noting this**), all 43 index pages via `cardtrack.fetch`, and HuggingFace-API
creation-date sweeps of XiaomiMiMo, stepfun-ai, poolside, Qwen, inclusionAI, moonshotai and deepseek-ai.
Web searches for `<org> system card`, `Xiaomi MiMo release August 2026`, `Palisade Research evaluation
report 2026` and `METR evaluation report August 2026` returned nothing not already held or already
skipped.

Xiaomi (116 d silent) is genuinely silent: its HuggingFace org shows nothing since the MiMo-V2.5 family
of 2026-04-27 except a DFlash speculative-decoding variant and an FP4 quantisation. Poolside (39 d) and
Moonshot (25 d) are fully covered — every non-quantised 2026 repo already has a row. Orgs silent >14 days
with today's counts: xiaomi (116), palisade_research (106), stepfun (90 — now with three new rows
backfilled), poolside (39), cursor (38), metr (31), apollo_research (31), us_caisi (29), moonshot_ai (25),
far_ai (23), thinking_machines / redwood_research / epoch_ai (21), saferai (19), uk_aisi / mistral (17),
transluce (15). No new qualifying publication at any of them.

## Citation mining

Mined the outbound references of the three documents added on 2026-08-20. `nvidia/GR00T-H-N1.7` cites
`nvidia/GR00T-N1.7-3B`, already held as `nvidia-nvidia-isaac-gr00t-n1-7-model-card`; `nvidia/GR00T-H`
cites `nvidia/GR00T-N1.6-3B`, created 2025-12-01 and therefore below the 2026-01-01 scope floor;
`nvidia/Cosmos-H-Surgical-Simulator` cites `Cosmos-Predict2.5-2B`, resolved as out of scope yesterday on
the same grounds. Nothing new.

The productive mining was on today's own adds, and it produced a finding rather than a row: four
first-party technical reports cited by the cards I added exist **only** on arXiv — Step 3.5 Flash
(2602.10604), Step3-VL-10B (2601.09668), the shared Ling and Ring 2.6 report (2606.15079, cited by three
adds), and Open-H Embodiment (2604.21017) from yesterday's GR00T add. The corpus contains **zero**
arxiv.org URLs across all 240 documents, though it does hold self-hosted first-party technical reports.
I followed that de facto rule rather than breaking it unilaterally, and wrote it up as a friction line:
the exclusion is currently inferred from a host histogram rather than stated in `criteria.yaml`.

## Issues and escalations

`blocked_escalations` is empty. `logs/open_issues.json` is `[]` **but unverified** — Phase B could not
reach `api.github.com`, so no open issue could be investigated and none could be ruled out. No comments
were posted; `comment_issue.py` was not invoked, as there was no verified issue to respond to. No
`status_change` was warranted: every URL I fetched this run, including the orphaned Opus 5 CDN hash,
returned 200.

## Friction and proposals

Seven friction lines appended: `phase_a_total_failure_silent` (fifth occurrence, first time with the
consequences measured rather than asserted), `github_unreachable_open_issues_unverified` (new),
`superseded_edition_misjudged_as_cosmetic` (new — corrects a prior run's finding),
`logical_duplicate_false_positive_on_sibling_reports` (new),
`slug_derivation_misnames_family_documents` (recurrence, second publisher — id 248 slugged
`…qwen3-asr-0-6b…` from the alphabetically first model rather than the 1.7B the card leads with),
`system_card_test_ambiguous_for_methods_papers_with_named_subject_model` (recurrence, one day later at
the same publisher), and `first_party_technical_reports_on_arxiv_invisible` (new).

One dated `PROPOSALS.md` entry with three sections: making Phase A's total failure loud instead of
indistinguishable from a clean run (the highest-value ask, five occurrences in); the Opus 5 correction,
which strengthens rather than replaces the 2026-08-18 `canonical_url` ask and asks for nothing new; and
a narrowing of `find_logical_duplicates` so that title-token overlap alone does not misfire on
publishers with house naming conventions.
