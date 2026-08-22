# cardtrack run report — 2026-08-22T06:17Z-local

**Corpus at start:** 248 documents (244 active, 3 removed, 1 moved). **Written this run:** 2 adds
(ids 249–250) and 1 new version (id 203, version 357). **Filed as needs-review:** 1 (`outbox:1`).
**Rejected:** none beyond that. **Open issues:** `[]`, but that value is not verifiable from inside the
sandbox — see task 4 below. **Blocked-URL escalations:** none in `candidates.json`.

Phase A worked today: `checked: 245, ok: 245, not_found: 0, blocked: 0, errors: 0, moved: 0,
marked_dead: 0, fingerprint_checked: 37, new_versions: 16, candidates: 2690, candidates_new: 33`.
A clean sweep after yesterday's total failure, and the 33 new links were real links.

## The headline: the corpus was serving corrected-away safety numbers, and the fix for that is blocked

Both of this run's most substantive findings are about **a document the corpus already held**, not about
anything new on the internet. Neither surfaced from the candidate list.

### xAI revised the Grok 4.6 model card in place, five days ago (fixed)

I opened `media.x.ai/v1/website/card-4p6-4cd2dc57.pdf` for citation mining and found the cover now reads
**`Revision: 2026-08-17`** against the stored `Revision: 2026-08-12`. The revision opens with a changelog
whose substantive line is:

> Corrected eval results on HackerBench v0.2, Self-harm, MASK, LAB.

Those are four safety and behavioural evaluations. The corpus had been serving the pre-correction numbers
for five days, including the HackerBench v0.2 harmful/dual-use compliance figure quoted in that row's own
add justification. The revision also restructures the card: it adds §4.3 PartBench, §4.4 CADGenBench,
§4.5 CADBench and a new §6 "Search capabilities and factuality" (Factuality/Hallucination, DeepSearchQA),
updates KernelBenchInternal to v1.1 on a harder task split, drops "Vals Index", and grows the card from
34 to 40+ pages. I downloaded and read both editions and compared them page by page.

| | stored (v236) | live today |
|---|---|---|
| bytes | 524,224 | 540,844 |
| md5 | `5faf54cc75e26c987541719b7e2d56f1` | `7640cdde745a18a2390cd5fbde55fd55` |
| cover | Revision: 2026-08-12 | Revision: 2026-08-17 |

Proposed as a new version — verdict:
`{"status": "written", "slug": "xai-grok-4-6-model-card", "document_id": 203, "version_id": 357}`.

**Why the monitor did not catch it:** `fingerprint_checked: 37` against 244 active documents. About 85% of
the corpus went revision-unchecked this run, and this PDF was in the unchecked 85%. This is the failure
mode of the 2026-08-18 proposal, now with corrected safety numbers on a frontier model as the payload.

### Cursor's launch-day copy is now the only surviving edition of it — and cannot be added (blocked)

The 2026-08-13 run found `cursor.com/resources/grok-4-6-model-card.pdf`, verified it byte-identical to
xAI's, and recorded it in the xAI row's `notes` rather than cataloguing it. I downloaded it today: it is
**still the launch-day bytes** — 524,224 B, md5 `5faf54cc75e26c987541719b7e2d56f1`, byte-for-byte the
version 236 the corpus stored. Cursor now hosts the only public copy of the pre-correction Grok 4.6 card;
xAI's URL no longer serves it.

I proposed it as its own row per the co-publication rule, mirroring the Grok 4.5 pair the corpus already
holds (ids 180 and 202). Verdict:
`{"status": "issue_filed", "reason": "content_duplicate_of:xai-grok-4-6-model-card", "issue_ref": "outbox:1"}`.

The validator is right on its own terms — the fingerprints *are* identical — and I have not retried it.
But the two rules cannot both be satisfied here, and not by accident: launch partners publish identical
bytes **on launch day**, so the window in which a co-publication is proposable is exactly the window in
which it is indistinguishable from a mirror; and because the dedup check matches *any stored version* of
the sibling row, once the launch-day bytes are stored the partner copy is blocked permanently rather than
until divergence. Grok 4.5 is two rows only because it was caught after divergence and the launch-day
bytes had never been stored. Filed to `logs/PROPOSALS.md` with a suggested fix: make the duplicate check
publisher-aware, since identical content under a *different* allowlisted publisher is the signature of a
co-publication, not a re-host.

## Added (2) — an InclusionAI guardrail line that has been missing since May

Both cards fetched and read in full, dated from HuggingFace commit history rather than repo metadata.

| id | document | date | verdict |
|---|---|---|---|
| 249 | [SingGuard 0.8b/2b/4b/8b](https://huggingface.co/inclusionAI/SingGuard-2b) | 2026-05-29 | `{"status": "written", "slug": "inclusion-ai-singguard-0-8b-model-card", "document_id": 249, "version_id": 355}` |
| 250 | [SingGuard-NSFA 0.8B/2B/4B/9B](https://huggingface.co/inclusionAI/SingGuard-NSFA-9B) | 2026-07-13 | `{"status": "written", "slug": "inclusion-ai-singguard-nsfa-0-8b-model-card", "document_id": 250, "version_id": 356}` |

**SingGuard** is a policy-adaptive multimodal guardrail family (base: Qwen3-VL Instruct) that takes a
natural-language safety policy at runtime and returns a binary judgement plus a matched risk category
across text, image and mixed inputs; paper arXiv 2606.22873, which also introduces SingGuard-Bench (56k+
examples, 80+ risk categories). **SingGuard-NSFA** is a separate line, not a size variant: different base
(Qwen3.5), different taxonomy ("Not-Secure-For-Agents", 185 risk variants against CIA-triad and OWASP),
different paper (arXiv 2607.13081), six weeks later, with MLP classification heads for ~50ms detection
alongside the generative reasoning path. Both Apache-2.0 with public weights → `open_weight_permissive`
(verified on the cards and in repo metadata).

**How they surfaced, and why that matters.** Not from a release event. `SingGuard-2b` entered the
candidate list because someone edited its README on 2026-08-21 — the repo is from **25 May**. The NSFA
line never entered the candidate list at all; I found it by walking the family through the HuggingFace
API. `huggingface.co/inclusionAI` is a configured `index_url` fetched successfully every run, and the
corpus already held six InclusionAI rows. This is the fifth instance in four runs of the backlog
blindness first proposed on 2026-08-13: a May release stops being a new link in May.

**Granularity call, flagged for reversal if wrong.** Each size has its own separately-authored card
(differing in base model and numbers), but I proposed one row per family listing all sizes, per the family
rule — under which adding `SingGuard-2b` makes `SingGuard-8b` a size variant of something already in the
corpus. Sibling URLs are recorded in each row's `notes`; GGUF conversions excluded as format variants.
This cuts against the "one distinctly-authored card = one row" reading proposed on 2026-08-20; that
ambiguity is still live and I applied the prompt's rule.

**`has_safety_evals` attested FALSE on both, and it is the least obvious call I made.** These cards are
almost entirely safety benchmark tables (>94% F1 across the NSFA taxonomy; SOTA across six safety
categories for SingGuard). But for a guardrail the safety benchmark *is* the capability benchmark, and the
flag marks documents that assess a model as a risk *subject*. I followed corpus precedent:
`mistral-shieldstral-1-0-model-card` and `nvidia-nemotron-3-5-content-safety-model-card` both carry
`safety_evals = 0`. Consequence worth stating plainly: the site's safety filter now hides four of the
documents most densely populated with safety evaluations. Logged to friction.

## Candidates triaged (33 new links) — 4 pursued, 29 skipped

Skipped as index furniture or non-documents (17): HuggingFace user profiles (`aldjalkdf`, `leiwx52`,
`emelryan`, `nigeln`, `michael-qiu`), `substack.com/@jefftk`, HF *discussion* threads (two Qwen3.8
"Add Terminal-Bench evaluation results" threads, plus `dlesym-v1-era5` and `Ling-3.0-flash-dspark`
discussions), NVIDIA dataset cards (`PhysicalAI-Robotics-Open-H-Embodiment`,
`video-to-data-robot-dexterity-task-library-and-dataset`), `huggingface.co/papers/2608.19758`
(FlashPrefill V2 — a serving-attention paper, no named-model assessment), the duplicate
`mistral.ai/news/agentic-search` trailing-slash pair, and `transluce.org/oversight-foundations` (an index
page).

Fetched, read and skipped on judgement (12):

- **`research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2`** (2026-08-20) — the closest call of
  the run. It reports ZeroBench, SimpleVQA, CharXiv Reasoning and Design Arena results for Muse Spark 1.2
  against GPT-5.6 Sol, Opus 5, Gemini 3.7 Flash, Claude Fable 5, Kimi K3 and Grok 4.6, plus a preview of
  WildArtifactBench. The system-card test says admit — those numbers would sit in a model card's
  evaluations section unedited. The `doc_type: other` scope discipline says skip — "capability demos and
  showcases", "when in doubt, skip". `criteria.yaml`'s `when_uncertain: admit_and_flag` points back the
  other way. I skipped on the narrower, more specific rule; precedent does not settle it either
  (`google-deepmind-sl2t-other` is an admitted first-party capability blog; `meta-tribe-v2-other` was
  admitted and later removed). Logged to friction — **this is the row to add if my reading is wrong.**
- **`transluce.org/scaling-activation-oracles`** (2026-08-20) — methods research: the reported numbers
  describe the oracle's detection ability, with Qwen3-8B/14B/32B, Qwen3.6-27B, GLM-4.5 and Kimi-K2.6 as
  fixed substrate. Skipped. Note: **yesterday's run already found, evaluated and skipped this exact post
  by hand**; it arrived today as a fresh candidate with `first_seen: 2026-08-22` carrying none of that
  history, so I re-adjudicated it from scratch and independently reached the same answer. That is the
  2026-08-17 "no triage state" proposal seen from the other side.
- **`api-docs.deepseek.com/news/news260821`** (2026-08-21) — DeepSeek launched
  **DeepSeek-V4-Flash-Vision-Exp**, a distinct experimental multimodal model, API-only. There is no card:
  no repo under `huggingface.co/deepseek-ai` (checked — latest are V4-Pro-0813 and V4-Flash-0731), no tech
  report; the post is availability plus image-token pricing plus a link to a developer vision guide.
  Skipped as a product announcement, but flagged: the corpus will read this as DeepSeek silence since
  2026-08-13, which is wrong in substance. A cardless launch is a finding the schema cannot hold.
- **`huggingface.co/inclusionAI/Ling-3.0-flash-dspark`** — a 1.36B speculative-decoding draft model for
  the catalogued Ling-3.0-flash. Not one of the four things `distinct_model_release` excludes, but not
  independently useful either. Skipped on precedent: DeepSeek's own V4-Flash-DSpark and V4-Pro-DSpark have
  been public since 2026-07-04 and are not catalogued.
- **`huggingface.co/nvidia/dlesym-v1-era5`** — ensemble earth-system forecast model; the card states
  release "NGC 05/12/2025" and carries no evaluations. Pre-scope-floor re-upload; skipped.
- **`huggingface.co/inclusionAI/ArmorOCR`** — README.md exists but is empty. No document to catalog.
- **`securebio.substack.com/p/securebio-detection-updates-august`** (2026-08-20) and the three-day
  early-warning post (both copies, Substack and `securebio.org/blog/`) — biosurveillance infrastructure
  (CASPER wastewater sequencing, Zephyr nasal swabs). Claude Managed Agents and GPT Rosalind appear as
  tools SecureBio *uses*, not as subjects. Fails the system-card test.
- **`rand.org/pubs/external_publications/EP71466.html`** — "Realising the 100 Days Mission", vaccine
  development speed. Not a model evaluation; RAND is allowlisted narrowly for CAST / Project Canary output.
- **`deepmind.google/blog/from-atari-to-eve-online-…`** (2026-08-21) — a 15-year research retrospective
  plus a partnership announcement with the EVE Online developer. No named-model evaluation results.
- **`mistral.ai/news/agentic-search`** (2026-08-20) — a retrieval feature, not a model. Its FinanceBench
  and OfficeQA Pro numbers measure the retrieval system's effect using Mistral Medium 3.5 and GLM-5.2 as
  substrate; same discriminator as the Transluce skip.
- **Three xAI posts** (`grok-bot-more-plans`, `grok-4-6-vertex-ai`, `grok-build-for-everyone`) — plan
  availability, platform availability, product launch.

## Targeted search and silence checks

Nothing new from the frontier labs in the ~72h window. `deploymentsafety.openai.com` still ends at the
2026-08-06 GPT-5.6 August Updates (already catalogued); `anthropic.com/news` ends at 2026-08-14. Searches
run: "system card August 2026 model card release AI lab"; "AI model release August 20 21 2026 new model
announced"; "METR evaluation report August 2026"; "UK AI Security Institute evaluation report August
2026"; "Apollo Research scheming evaluation August 2026"; "Epoch AI OR Thinking Machines OR Transluce new
report August 2026 model evaluation"; "Xiaomi MiMo new model release 2026"; `"Muse Spark 1.2" OR "Grok
4.6" OR "Gemini 3.7" model card system card published August 2026`; `Cursor "Grok 4.6" model card`.

Orgs silent >14 days, checked beyond the index diff:

- **Xiaomi (117d)** — checked `mimo.mi.com/docs/en-US/updates/model`, the release page that is *not* a
  configured `index_url`. Newest entry is mimo-v2.5-asr; the corpus already holds MiMo-V2.5-ASR,
  MiMo-V2.5 and MiMo-V2.5-Pro. The silence is real.
- **Mistral (18d)** — checked `docs.mistral.ai/models/model-cards/`, the blind spot recorded in the
  2026-08-14 proposal. Nothing after Shieldstral 1.0 (2026-08-04). Incidental: that index also carries a
  card for **Z.ai GLM 5.2**, a third-party model Mistral serves — not proposable, since GLM is not
  Mistral's model and Z.ai is not allowlisted.
- **METR (32d), Apollo (32d), UK AISI (18d), US CAISI (30d), Epoch (22d), Thinking Machines (22d),
  Palisade (107d), StepFun (91d)** — searched; nothing published after the newest rows already held. The
  UK AISI material dominating current coverage is the 2026-08-04 incident report, already catalogued.

**Co-publication check on the pair I touched:** Cursor's `cursor.com/grok` links its FAQ "Grok 4.6 Model
Card" to the media.x.ai PDF, and `cursor.com/blog/grok-4-6` (2026-08-12) is a launch announcement rather
than a card. Neither proposed.

## Citation mining

Mined the Grok 4.6 card (which produced both headline findings above) and the Anthropic August 2026
redacted risk report. The Grok 4.6 card's §7 says third-party evaluators independently validated the cyber
results **without naming them** — a dead end for lead generation, and the same observation the 2026-08-13
run recorded. Both Anthropic PDFs resisted text extraction through the fetch tool; the risk report's
landing URL 307-redirects to `www-cdn.anthropic.com/f61d49fa…/Redacted Risk Report August 2026 .pdf`.
That row (id 240) still carries a null `publication_date`; I could not establish a day-level date from the
cover, so I did not propose a `field_update` — inventing a date to satisfy a null is worse than the null.

## Issues (task 4)

`logs/open_issues.json` is `[]` and **I cannot verify what that means.** `run_daily.sh:37-42` pipes each
`gh issue list` through `|| echo "[]"`, and the merge step swallows exceptions, so auth failure, network
failure and an empty backlog are indistinguishable. New this run: `gh` inside the agent sandbox is
unauthenticated (it prints the `gh auth login` prompt), so if the Phase B fetch ran in this environment
then `[]` was the fallback rather than an observation — though yesterday's outbox drained successfully at
2026-08-21T09:46Z, so an authenticated path exists somewhere in the harness. **Task 4 is therefore
reported as completed against unverifiable input for the second consecutive run**, not as
completed-with-nothing-found. No issues were investigated and no `comment_issue.py` calls were made.
Logged to friction; not filed as a new proposal, because the 2026-08-14 remedy — distinguish "checked,
found nothing" from "could not check" in the artifacts themselves — covers it unchanged.

## Blocked-URL escalations (task 5)

`blocked_escalations` is empty and Phase A recorded `blocked: 0, not_found: 0, errors: 0` across 245 link
checks. Nothing to escalate. Incidental: `huggingface.co` returned HTTP 429 to three of my fetches mid-run
(SingGuard-8b, ArmorOCR); all succeeded on retry, so no document was recorded as unreachable on that basis.

## Friction logged (9 lines)

`co_publication_indistinguishable_from_mirror_by_content_dedup` ·
`superseded_edition_found_by_hand_not_by_the_fingerprint_sweep` ·
`candidate_list_replays_previously_adjudicated_links` ·
`guardrail_model_safety_evals_flag_has_no_stable_reading` ·
`first_party_capability_showcase_with_named_model_benchmarks` ·
`model_launched_with_no_documentation_of_any_kind` ·
`pre_scope_floor_model_republished_under_a_new_repo` ·
`no_criteria_answer_for_speculative_decoding_draft_models` ·
`empty_open_issues_list_is_indistinguishable_from_a_failed_issue_fetch`

## Proposals filed

One entry appended to `logs/PROPOSALS.md`: the co-publication/dedup deadlock (§1, with a suggested
publisher-aware duplicate check), plus a §2 confirming-evidence note on the 2026-08-18 superseded-edition
proposal that asks for nothing new.

**Corpus at end:** 250 documents (246 active, 3 removed, 1 moved).
