# cardtrack daily curation — run `2026-08-17T06:15Z-local`

Corpus went from 225 to 228 documents. Four proposals, four written, none rejected and none
routed to a review issue. Phase A worked properly for the first time in three days
(`checked: 222, ok: 222, errors: 0`), which is what made the rest of this run possible.

Only one of today's three adds came from today's news. **Gemini 3.7 Flash** (2026-08-13) was the
genuine new release. The other two were dug out of the *candidate backlog*: an in-scope
Thinking Machines model release from **May** and an NVIDIA technical report from **June**, both
surfaced by the pipeline on 2026-08-09/10 and stepped over by every run since. That is this
run's main finding, and its first `PROPOSALS.md` entry.

The second finding is housekeeping that turned out to matter. On arrival `logs/run_report.md`
described the 2026-08-14 run and a corpus of 218, while the database held 225. The 2026-08-15
run wrote seven documents and then died on `Error: Reached max turns (60)` before writing its
report, and 2026-08-16 lost the network entirely. Two days of writes with no narrative record.

## Counts

| | |
|---|---|
| Documents at start / end | 225 → **228** |
| Candidates in `logs/candidates.json` | 2,616 — **39 new** since 2026-08-13 |
| Candidate backlog scanned by hand | 2,577 older entries → 176-link shortlist → **2 in-scope finds** |
| Documents fetched and read in full | 11 |
| HuggingFace orgs swept by creation date via API | 14 |
| Web searches | 4 |
| Proposals submitted | 4 (3 `add`, 1 `field_update`) |
| Written | **4** (ids 226, 227, 228 + notes on 226) |
| Rejected | 0 |
| Routed to review issues | 0 |
| Open GitHub issues to investigate | 0 (`logs/open_issues.json` is `[]`) |
| Blocked-URL escalations | 0 (`blocked_escalations` empty) |
| Friction lines appended | 5 |
| `PROPOSALS.md` entries | 3 |

## Proposals and validator verdicts

| # | Document | Publisher | Date | Safety evals | Verdict |
|---|---|---|---|---|---|
| 1 | Gemini 3.7 Flash Model Card | google_deepmind | 2026-08-13 | **yes** | `written` 226, `google-deepmind-gemini-3-7-flash-model-card` |
| 2 | *(field_update)* `notes` on id 226 — PDF twin | google_deepmind | — | — | `written` 226 |
| 3 | Interaction Models: A Scalable Approach to Human-AI Collaboration | thinking_machines | 2026-05-11 | **yes** | `written` 227, `thinking-machines-tml-interaction-small-model-card` |
| 4 | Cosmos 3: Omnimodal World Models for Physical AI | nvidia | 2026-06-22 | no | `written` 228, `nvidia-cosmos3-edge-other` |

### 1–2. Gemini 3.7 Flash — the one genuine release of the day

`deepmind.google/models/model-cards/gemini-3-7-flash/`, announced the same day on `blog.google`
as "our most intelligent workhorse model yet for coding and agents", with the announcement
linking straight to the card. Distinct release on the corpus's own precedent: 3.5 Flash (id 13)
and 3.6 Flash (id 14) are separate rows and 3.7 Flash carries its own pricing, its own March 2026
knowledge cutoff and its own evaluation run. `has_safety_evals=true` and substantially so — text-
to-text, multilingual and image-to-text safety, tone and unjustified-refusal evaluations, manual
red teaming by specialists outside the model-development team, child-safety launch thresholds,
and a Frontier Safety Framework assessment across CBRN, cybersecurity, harmful manipulation and
ML R&D/misalignment concluding that "Gemini 3.7 Flash did not reach any tracked or critical
capability levels". `openness=closed` — API and app distribution only, no weights.

The follow-up `field_update` records something the schema has no field for: the same card is also
served as a PDF at `storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-7-Flash-Model-Card.pdf`
(HTTP 200, 313 KB, verified). I checked and the twinning is systematic — 3.6 Flash and
3.5 Flash-Lite both exist in both formats — and the corpus is split arbitrarily between the two
surfaces. Third `PROPOSALS.md` entry.

### 3. TML-Interaction-Small — 98 days old, seen for 8

`thinkingmachines.ai/blog/interaction-models/`, 2026-05-11. A 276B-parameter (12B active)
multi-stream interaction model trained from scratch, announced as a research preview. Not an
essay: it names the model, gives the architecture, and reports a comparative benchmark table
against GPT-realtime, Gemini 3.1 Flash Live and Qwen 3.5 Omni (FD-bench V1/V1.5/V3, QIVD, Audio
MultiChallenge, BigBench Audio, IFEval text and voice, TimeSpeak, CueSpeak, RepCount-A,
ProactiveVideoQA, Charades), plus a safety section on modality-appropriate refusals and
long-horizon robustness with Harmbench refusal rates per model — hence `has_safety_evals=true`.
Distinct from the corpus's only other Thinking Machines models, the open-weights Inkling family.

`openness=closed`, verified two ways rather than inferred: `huggingface.co/thinkingmachines`
holds only Inkling, Inkling-Small and their NVFP4 quantizations, a site-wide HF search for
"TML-Interaction" returns zero repos, and the post itself describes a gated research preview.

The uncomfortable part: `thinkingmachines.ai/blog/` **is** a configured `index_url`, Phase A
surfaced this link on 2026-08-09, and eight runs stepped over it.

### 4. Cosmos 3 technical report — and an absence worth recording

`research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf`, dated 2026-6-22 on its title
page. 29 MB, 613k characters of extracted text, covering Cosmos3-Super, Cosmos3-Nano,
Cosmos3-Edge and the Text2Image / Image2Video / Policy-DROID variants, with third-party
Artificial Analysis and RoboArena rankings cited. Catalogued as a document distinct from the two
HuggingFace family cards already held (ids 54, 55) on the precedent set three days ago by the
Nemotron 3 Ultra Technical Report (id 224) sitting beside its model card (id 52).

`has_safety_evals=false` is the substantive finding here. Across the whole report: "guardrail" 0
occurrences, "red team" 0, "misuse" 0, "harmful" 0, "risk assessment" 0; the five uses of
"safety" all refer to warehouse-safety scene data. An openly-licensed world-action model family
for embodied agents, shipped with checkpoints, datasets and benchmarks under OpenMDW-1.1, with no
safety or dangerous-capability evaluation in its technical report.

## Checked and deliberately skipped

Of today's 39 new candidates, 36 were skipped:

- **`blog.google/…/introducing-gemini-3-7-flash/`** — launch announcement, no evaluations;
  recorded as an evidence URL on id 226 instead.
- **Anthropic "How Claude's text watermark works"** (2026-08-14) — an explainer on watermarking
  method and EU AI Act compliance. Names no specific Claude model and reports no evaluation of
  one; the only quantitative claim cited is DeepMind's SynthID-Text result about Gemini. Fails
  the system-card test.
- **xAI "Grok 4.6 in GitHub Copilot"** (2026-08-14) — partnership/availability announcement,
  explicitly out of scope for `doc_type: other`. I checked for a Copilot-hosted Grok 4.6 card of
  the kind Cursor published for Grok 4.5 (id 202); there is none, and GitHub is not allowlisted.
  `x.ai/api/changelog` is a console changelog.
- **Cursor** — four posts, none in scope: `joining-spacex` (acquisition), `firetiger`
  (acquisition), `aiuc-1` (a security certification, no named model), `builds` + the matching
  changelog entry (product feature).
- **Epoch AI** — `9-big-questions-benchmarks-can-help-answer`, `will-financing-bottleneck-ai-compute`,
  `chip-performance-per-dollar`, `employer-provided-ai-by-occupation`. Benchmark methodology and
  compute economics; none assesses a named model.
- **DeepSeek** — `news260813` is the GA announcement for DeepSeek-V4-Pro-0813, already catalogued
  as id 207; `deepseek-harness` quickstart is developer documentation.
- **Quantization, format and drafter variants** — `Qwen/Qwen3.8-27B-FP8`,
  `nvidia/Kimi-K3-NVFP4`, `nvidia/DeepSeek-V4-Pro-nvfp4-DSpark`,
  `nvidia/DeepSeek-V4-Flash-nvfp4-DSpark`. Excluded by `distinct_model_release`, and the last
  two would in any case be NVIDIA re-uploads of another publisher's model.
- **`nvidia/NVIDIA-Nemotron-Labs-Teacher-{Chat,STEM,Competition-Coding,Instruction-Following}`**
  — already covered: id 225 is the family row listing all five Teacher models.
  `nvidia/Cosmos3-Edge-Policy-DROID` is covered by id 55.
- **`inclusionAI/Ling-3.0-flash` discussion thread** — the model itself is id 182.
- **Collections, datasets, spaces, user profiles and HF discussion threads** — 20 links
  (`Qwen/qwen38`, `tencent/ui-mate`, `nvidia/Nemotron-SFT-SWE-v3.5`, `nvidia/AV-Causal-Scenario-Retrieval-Challenge`,
  `huggingface.co/papers/2608.13391`, and assorted user pages). `tencent/ui-mate` still contains
  no items, as on 2026-08-14.

From the backlog scan (176-link shortlist beyond the two adds), the notable non-finds:

- **SecureBio `securebio.org/blog/<slug>/` pages are mirrors**, not new documents. I fetched four
  and confirmed each matches an already-catalogued Substack post: the Kimi K3 biology assessment
  (2026-08-07), the GPT-5.5 pre-release assessment (2026-04-23), the Anthropic unredacted CB
  review (2026-07-28) and the biosecurity-safeguard piece (2026-07-16). Proposing them would have created
  four duplicate rows — the URL-based dedup guard would not have caught them.
- **`anthropic.com/news/political-even-handedness`** is dated **Nov 13, 2025** — a genuine
  named-model evaluation (Claude Opus 4.1 95%, Sonnet 4.5 94%, Gemini 2.5 Pro 97%, Grok 4 96%,
  GPT-5 89%, Llama 4 66%) but before the 2026-01-01 scope floor. Not proposed.
- The remaining shortlist is pre-2026 system cards and addenda (OpenAI's GPT-5.x line, xAI's 2025
  cards, METR's 2024–25 evaluation reports), alternate URLs for documents already held, or
  methodology posts with no named model (UK AISI's Inspect tooling series, US CAISI's
  transcript-analysis and red-teaming-competition posts, RAND's evaluation-practice perspectives).

## Targeted search and silent-org audit

Searches for frontier documentation from the last ~72 hours returned nothing beyond Gemini 3.7
Flash. `deploymentsafety.openai.com` still carries nothing newer than the 2026-08-06 GPT-5.6
August update (id in corpus), so GPT-5.6-Cyber's promised full system card has still not
appeared. METR's `/risk-assessment/` page — which is *not* a configured `index_url`, and which
`/evaluations/` redirects to — lists exactly one 2026 evaluation report, GPT-5.6 Sol, which the corpus already holds at
`metr.org/blog/2026-06-26-gpt-5-6-sol/`. Everything else there is 2025 or earlier. No METR gap
of the Mistral kind.

Fifteen publishers are >14 days silent. A HuggingFace-API sweep by creation date across 14 orgs
confirms the silence is real rather than a looking-in-the-wrong-place artefact: every repo
created since the last catalogued release is a quantization, GGUF, NVFP4 or speculative-decoding
drafter variant — `XiaomiMiMo/MiMo-V2.5-DFlash` (2026-07-03), `stepfun-ai/Step-3.7-Flash-GGUF`,
`tencent/Hy-MT2-30B-A3B-GGUF`, `poolside/spec-decoding-subfolder-fixture`. `xiaomi` (112 d),
`palisade_research` (102 d) and `stepfun` (86 d) remain the longest-silent and remain, as far as
I can verify, genuinely quiet. `ByteDance/Bernini-Diffusers-v2` (2026-08-13) is a real release
but ByteDance is not allowlisted.

## Citation mining

I mined the stored text of ids 219–226 rather than re-fetching them. Outbound references were
overwhelmingly to benchmark repositories and papers, not to documents in scope. The one
allowlisted-publisher link found, `thinkingmachines.ai/blog/on-policy-distillation` (cited by the
Nemotron 3 Ultra report), is a 2025 training-methods essay with no named-model assessment —
out of scope on both date and the system-card test. The Thinking Machines find above came from
the backlog scan, not from citations.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty, so there was nothing to
investigate and no comments were posted. Unlike the 2026-08-14 and 2026-08-16 runs, today's
issue list was written with the network up, so the empty list is trustworthy this time.

## One more thing worth a look

Phase A reported `fingerprint_checked: 34, new_versions: 18` — over half the sampled corpus
apparently revised overnight. It was not. I diffed three: Kimi K3 (id 44) moved its download
counter from 1,456,459 to 2,136,775 and swapped a leaderboard widget; Nemotron 3 Ultra (id 52)
gained one SWE-bench leaderboard row; the Anthropic biology-safeguards post (id 101) gained a
"How Claude's text watermark works — Read more" link in its related-posts strip. The affected ids
(43–55, 101–103, 195, 196) are contiguous, i.e. whatever the rotation sampled. Each writes a
stored version and a changelog row, so a genuine silent revision to a system card would be hard
to see among the download-counter churn. Logged as friction rather than a proposal, since one
morning's three diffs is thin evidence for a normalizer change.
