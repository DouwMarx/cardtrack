# cardtrack daily curation — run `2026-08-12T06:17Z-local`

Corpus went from 196 to 201 documents. Six proposals, five written, one rejected — and the
rejection is the run's most useful finding.

Three genuinely new releases landed in the 72-hour window and all three are now catalogued:
**Meta's Muse Glimmer** (2026-08-10, card + methodology report), **NVIDIA Nemotron 3.5
Lightning** (2026-08-11) and **InclusionAI Ling-3.0-tiny** (2026-08-10). RAND CAST published
a new biosecurity evaluation of named frontier agents on 2026-08-11; it is in.

Two frontier releases from tier-1/2 publishers are **not** in, and neither is a judgement
call — both are fetch failures. OpenAI shipped **GPT-5.6-Cyber** on 2026-08-10 and its launch
announcement now sits behind a Cloudflare challenge that rejects the validator as well as me.
Alibaba shipped **Qwen3.8-Max** on 2026-08-03 and its blog serves an identical JavaScript
shell for every URL. Details and a suggested fix in `logs/PROPOSALS.md`.

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 2476 across 28 publishers |
| New this run (`first_seen` 2026-08-12) | 266 — qwen 140, deepmind 30, epoch 21, nvidia 19, anthropic 13, meta 12, openai 9, xai 8, inclusion_ai 6, mistral 3, securebio 2, rand 2, palisade 1 |
| Candidates triaged | all 266; none matched an existing `canonical_url` |
| Documents fetched and read | 21 (blogs, model cards, two PDFs read in full) |
| Index pages swept beyond Phase A | 8 (deploymentsafety.openai.com, anthropic.com/news, deepmind blog, metr.org/blog, apolloresearch.ai/research, epoch.ai/latest, far.ai/blog, transluce.org/news), plus qwen.ai/blog, the frozen qwenlm.github.io blog, and HF org listings for six publishers via the API |
| Web searches | 14 |
| Proposals submitted | 6 |
| Written as rows | 5 (ids 197–201) |
| Routed to review issues | 0 |
| Rejected | 1 (unretrievable) |
| Open GitHub issues to investigate | 0 (`logs/open_issues.json` is `[]`) |
| Blocked-URL escalations | 0 (`blocked_escalations` empty in `candidates.json`) |
| Friction lines appended | 5 |
| PROPOSALS.md entries | 1 |

## Proposals and validator verdicts

| # | Document | Publisher | Date | Safety evals | Verdict |
|---|---|---|---|---|---|
| 1 | **Testing LLM Agents on the Use of Biological Tools for Nucleic Acid Synthesis Screening Evasion** (RR-A4741-2) | rand | 2026-08-11 | yes | `written` id 197, slug `rand-gemini-3-1-pro-independent-eval-2` |
| 2 | **Muse Glimmer 30B Model Card** | meta | 2026-08-10 | yes | `written` id 198, slug `meta-muse-glimmer-model-card` |
| 3 | Muse Glimmer Evaluation Methodology | meta | 2026-08-10 | yes | `written` id 199, slug `meta-muse-glimmer-other` |
| 4 | NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 Model Card | nvidia | 2026-08-11 | no | `written` id 200 |
| 5 | Ling-3.0-tiny Model Card | inclusion_ai | 2026-08-10 | no | `written` id 201 |
| 6 | Expanding Daybreak as the Cyber Defense Window Narrows (GPT-5.6-Cyber) | openai | 2026-08-10 | yes | **`rejected`** — `document_retrievable=false: HTTP 403` |

1. **RAND CAST, RR-A4741-2** — read the full 48-page PDF. Two named models were run as ReAct
   agents against four biological-tool configurations and scored through an eleven-metric
   pipeline ending at a real commercial nucleic-acid synthesis screen: **Gemini 3.1 Pro**
   (3 of 30 Protein-2 redesigns evaded screening) and **DeepSeek V4 Pro** (3 of 30). Claude
   Opus 4.7 and GPT-5.5 were dropped from the primary assessment because refusals and content
   filters blocked testing — a safeguard result in its own right, and the reason the authors
   say their numbers understate the capability ceiling. Sequel to RRA4741-1 (2026-06-25),
   already catalogued; cross-referenced in notes.
2. **Muse Glimmer 30B** — Meta Superintelligence Lab's card on Hugging Face, Apache 2.0,
   announced on research.meta.ai the same day. Four-axis safety evaluation (content safety,
   agentic risk including indirect prompt-injection resistance, privacy, preparedness) plus a
   Preparedness Team assessment rating chem/bio, cyber and loss-of-control at Moderate or
   lower under Meta's Advanced AI Scaling Framework. Distinct model, not a Muse Spark variant.
3. **Muse Glimmer Evaluation Methodology** — found by citation from the card and the
   announcement, and the announcement's own link (`ai.meta.com/static/muse-glimmer-methodology`)
   404s; the PDF lives at `research.meta.ai/static/muse-glimmer-methodology`. Read in full:
   per-benchmark methodology against Gemma4-31B and Qwen3.6-27B, including the safety suite
   (CIMemories, Siren AgentDojo prompt injection, SecureBio/CAIS MBCT-HPCT-VCT, WMDP,
   LAB-Bench, CyberGym, CyberBench). Mirrors the catalogued `muse-spark-1-2-methodology`.
   `has_safety_evals=true` records that it specifies and documents the dangerous-capability
   suite; the numeric scores sit in the card and blog, and that nuance is in the entry's notes.
4. **Nemotron 3.5 Lightning** — the card states Release Date August 11, 2026. New Nemotron
   family member (interleaved Mamba-2 + MoE), not present in any form. Proposed the BF16
   reference card only; `-NVFP4`, `-NVFP4-DSpark`, `-NVFP4-DFlash` and `-Base-BF16` are
   quantizations/derivatives of the same release and were deliberately left out.
   `has_safety_evals=false` — the card's benchmarks are capability-only and its safety content
   is a pointer to separate Model Card++ subcards.
5. **Ling-3.0-tiny** — 7.9B total / 1.3B active hybrid-reasoning MoE for local deployment,
   official InclusionAI org, repo created 2026-08-10, 164 likes inside a day. The one
   judgement call of the run: a same-family, different-size sibling of the catalogued
   Ling-3.0-flash. Attested `distinct_model_release=true` on the precedent that Nemotron 3
   Nano/Super/Ultra are three entries, and flagged it in its own notes as the entry to revert
   if maintainers read the rule the other way. `-fp8` and `-int4` not proposed.
6. **GPT-5.6-Cyber** — see below.

## The one rejection, and why it matters

OpenAI announced GPT-5.6-Cyber on 2026-08-10: built on GPT-5.6 Sol, trained for zero-day
discovery and exploit-chain development, with deliberately reduced refusals on dual-use cyber
tasks, gated behind a new applicant-vetted **Daybreak Red** tier. OpenAI reports an internal
Advanced Cybersecurity Completion Rate of 95.0% against 1.5% for GPT-5.6 Sol and 57.3% for
GPT-5.5-Cyber.

I could not read the announcement: `openai.com/index/` returns HTTP 403 with a Cloudflare
JavaScript challenge to WebFetch and to browser-UA curl alike. I proposed it anyway, with the
gap disclosed in the record, on the basis of OpenAI's own indexed page text, the OpenAI
developer-community repost (date and model names), and the official
`developers.openai.com` model page. The validator hit the same 403 and rejected it. That
verdict stands and I did not retry.

Two things follow. The block is a **regression** — three `openai.com/index/` documents were
fetched and written on 2026-07-21, 2026-08-04 and 2026-08-07. And
`deploymentsafety.openai.com` (checked directly this run) lists nothing after the 2026-08-06
GPT-5.6 August update, so GPT-5.6-Cyber presently has **no** first-party documentation in the
corpus and no route to any. Worth re-checking the Deployment Safety Hub next run.

## Checked and deliberately skipped

**From the new candidates:**

- `anthropic.com/research/riemann-zeta` (2026-08-10) — an unreleased research Claude improved
  a Riemann-hypothesis lower bound. Read it: a capability demonstration with no named model
  and no safety content. Out of scope per the `other` scope discipline.
- Anthropic `/research` backlog newly surfaced by the index (`global-workspace`,
  `off-switch-dual-use`, `how-canada-uses-claude`, `economic-index-june-2026-report`,
  `81k-interviews`, `project-deal`) — interpretability, alignment-method, and economic
  research; none evaluates a named model.
- All nine new `deploymentsafety.openai.com` links — HTML landing pages for system cards whose
  PDFs are already catalogued (gpt-5-6, gpt-live, gpt-5-6-preview, gpt-rosalind-5-5, gpt-5-5,
  gpt-5-5-instant, chatgpt-images-2-0, gpt-5-6-august-update). Duplicates.
- 30 Google DeepMind model-card links — the Gemini 2.5/2.0, Gemini 1.x, Veo 3, Imagen 4 and
  Gemma PDFs predate the 2026-01-01 scope floor; `gemini-3-6-flash` and `gemini-3-1-pro` are
  HTML views of PDFs already catalogued.
- `securebio.org/blog/kimi-k3-biology-capabilities-assessment` — same organisation's second
  host for the Substack copy already catalogued (2026-08-07). Same-publisher mirror, not a
  co-publication.
- `securebio.org/blog/updates-aug-2026` (2026-08-11) — read it: biosurveillance programme
  update (CASPER wastewater sequencing, Zephyr, partnerships). No model evaluated.
- `mistral.ai/news/regional-inference-open-models-new-compute` (2026-08-11) — infrastructure
  and sovereignty announcement, no new Mistral model. It links a Mistral-hosted model card for
  Z.ai's GLM-5.2, which is a third-party mirror and Z.ai is not on the allowlist.
- `x.ai/news/introducing-grok-bot` (2026-08-11) — product launch for an agent teammate
  product, no model card, no evaluations.
- `rand.org/pubs/research_briefs/RBA3845-3` (2026-08-11) — AI data-centre energy brief, not
  model documentation.
- `palisaderesearch.org/blog/palisade-podcast-tim-hua` — podcast episode.
- 140 `alibaba_qwen` and 19 `nvidia` HuggingFace links — user profiles, datasets, Spaces,
  collections, papers, and quantized re-uploads (`Nemotron-3-Super-120B-A12B-BF16-MTPv2` is a
  variant of the catalogued Nemotron-3-Super; `Ling-3.0-tiny-fp8`/`-int4` are quantizations).
- 21 `epoch_ai` links — section indexes plus data-insights and gradient-updates already
  catalogued or not model-specific (`ai-chip-production`, `hyperscaler-capex-vs-cash-flow`,
  `what-we-learned-from-1604-chinese-ai-job-postings`).

**From the silence sweep** (publishers with no document for >14 days): checked
metr, apollo_research, far_ai, epoch_ai, transluce, moonshot_ai, tencent_hunyuan, stepfun,
xiaomi, deepseek and alibaba_qwen. Nothing new qualified.

- METR has one uncatalogued 2026 post, `2026-07-28-investigating-ai-propensities-after-incidents`
  — a methods/policy essay on how external investigators should work after a misalignment
  incident. No named model; fails the system-card test.
- Apollo Research, FAR.AI, Transluce and Epoch AI have published nothing since their last
  catalogued document (2026-07-21, 07-29, 08-06 and 07-31 respectively). Epoch's newest item,
  `one-in-five-workers-delegate-work-to-ai` (2026-08-06), is a labour survey.
- Moonshot AI, Tencent, StepFun, Xiaomi and DeepSeek have shipped no new HuggingFace model
  since their last catalogued entry (checked via the HF API sorted by creation date; newest
  across all five is `deepseek-ai/DeepSeek-V4-Flash-0731`, already catalogued).
- **xAI is a documented absence, not a gap in my search.** Grok 4.6 launched 2026-08-07 and
  Grok Bot on 2026-08-11; xAI published a model card for neither, and `data.x.ai` still lists
  only the 2025 Grok 4 cards plus the catalogued Grok 4.5 card (2026-07-14). The corpus
  correctly shows xAI silent for 29 days because xAI is in fact silent.
- **Alibaba Qwen is a tooling gap, not silence** — Qwen3.8-Max (2026-08-03) and
  Qwen-Image-3.0 (2026-08-05) both shipped and neither can be fetched. See `PROPOSALS.md`.

## Citation mining

Fetched the recently added documents and followed their references. One catch, three misses:

- **Muse Glimmer card → Muse Glimmer Evaluation Methodology** (proposal 3 above). The card
  also cites the Muse Spark Safety & Preparedness Report, already catalogued.
- SecureBio's Kimi K3 assessment (2026-08-07) cites its own BioTIER dashboard and an arXiv
  methodology paper, plus Moonshot's Kimi K3 platform docs and Epoch's ECI — nothing
  allowlisted and uncatalogued.
- SaferAI's GLM-5.2 report (2026-08-02) cites benchmark papers, the CAIS dashboard and METR's
  Frontier Risk Report; METR's own copy of that report (2026-05-19) is already catalogued.
- RAND RR-A4741-2 cites academic protein-design benchmarks and its own predecessor. Nothing
  new on the allowlist.
- **Resolved an open ambiguity.** The 2026-08-10 friction line asked for a ruling on
  co-published reports; this run's contract supplies it, and I applied it to the outstanding
  case. METR's MirrorCode page stays out — I fetched it and it self-describes as "a linkpost
  for MirrorCode, a project that METR funded and co-developed with Epoch AI", i.e. a pointer,
  not a second copy. The AISI/CAISI Kimi K3 pair (two full assessments, both catalogued) is
  what the co-publication rule is for.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty, so no issue
investigations and no `comment_issue.py` calls this run. No `status_change` or `field_update`
proposals were warranted: every document I touched resolved live.
