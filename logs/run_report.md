# cardtrack run report — 2026-09-09 (run id `2026-09-09T06:17Z-local`)

Last successful agent run: `2026-09-07T06:37:38Z`. The 2026-09-08 run failed in Phase B (OAuth
token revoked) on top of a total monitor outage, so **two days of Phase A output land in this
run**: 40 new candidate links, 3 new version diffs, and a 48-hour search window rather than 24.
Search lookback taken as since 2026-09-06, i.e. the 72 h floor, which is wider than
last-success-to-now and is the right call after an outage day.

Today is a Wednesday, so no weekly retrospective sweep was due.

Headline: three new rows — OpenAI's **ChatGPT Images 2.5 System Card**, Meta's **Muse agent
security document**, and InclusionAI's **Ling-3.0-flash-VL**. Citation mining on the GPT-6 Astra
card turned up a published independent cyber evaluation we structurally cannot catalogue, which is
the most important thing in this report and is written up in `PROPOSALS.md`.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | `add` | OpenAI — *ChatGPT Images 2.5 System Card* (2026-09-08) | **written** → `openai-chatgpt-images-2-5-system-card` (doc 299, v526) |
| 2 | `add` | Meta — *How We Built Safety Into Muse* (2026-09-08) | **written** → `meta-muse-other` (doc 300, v527) |
| 3 | `add` | InclusionAI — *Ling-3.0-flash-VL* (2026-09-04) | **written** → `inclusion-ai-ling-3-0-flash-vl-model-card` (doc 301, v528) |
| 4 | `field_update` | `openai-chatgpt-images-2-5-system-card` `related_urls` | **written** |
| 5 | `annotate_version` | `nvidia-gr00t-h-model-card` v525 | **written** |

Five proposals, five written. No rejections, no duplicates, no noops.

## 1. Phase A candidate triage

249 candidate links in the file, 40 of them new since the last agent run. Three were proposed; the
rest resolved as follows.

**Proposed**

- `deploymentsafety.openai.com/chatgpt-images-2-5` — the successor to the catalogued ChatGPT
  Images 2.0 card, covering **GPT-Image-2.5-Sunburst** and **GPT-Image-2.5-Flare**. Catalogued at
  the full-document PDF per the OpenAI convention, with the hub landing page recorded as a
  `web_version` (proposal 4). It carries real numbers: 77.0 % safe / 21.9 % blocked / 1.09 %
  unsafe-presented for Sunburst and 79.4 / 19.2 / 1.41 for Flare against an Images 2.0 baseline of
  75.2 / 23.1 / 1.64, plus a per-policy-category table (sexual content, hate, violence and gore,
  extremism, self-harm, political imagery, abuse, wrongdoing, deepfakes, jailbreaks). Section 3.4
  records a Preparedness determination that neither model crosses the Bio High or Cyber High
  threshold. Tagged `cbrn`, `cyber`, `harmful_manipulation`, `societal_harm` — see the judgment
  calls below, since the Images 2.0 row carries only `cbrn`.
- `research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse` — Meta's
  security and safety documentation for the Muse agent, built on Muse Spark 1.3. Threat model plus
  mitigations: Muse Secure VM, a Sentinel permission authority over connector actions and network
  egress, human-in-the-loop gates, least privilege, browser protections, and a bug bounty paying up
  to $300k per report and up to $130k for a successful prompt injection.
- `huggingface.co/inclusionAI/Ling-3.0-flash-VL` — 124B total / ~5.5B active vision-language
  member of the Ling 3.0 family, MIT, 1M context, scoring 42 on Artificial Analysis Intelligence
  Index v4.1.1 against 38 for the text-only Ling-3.0-flash.

**Newly resolved this run**

- `deepmind.google/blog/alphagenome-atlas-…` and `deepmind.google/science/alphagenome/` —
  **skip.** AlphaGenome Atlas is a precomputed dataset of predicted effects for 9 billion
  single-nucleotide variants, served from a specialised genomics predictor. Not a generative or
  general-purpose model, and it contains no biosecurity or dangerous-capability assessment — only a
  not-for-clinical-use disclaimer. Out under `covered_model_class` on both limbs.
- `tencent/AuK`, `AuK-Flash`, `spaces/tencent/AuK` — **skip, but logged as ambiguous.** AuK is an
  MIT-licensed 1.5B open speech generation and editing model (zero-shot and instruction TTS,
  content and acoustic editing, paralinguistic editing, enhancement, source separation). It sits on
  exactly the `covered_model_class` line that StepAudio 2.5 sat on two runs ago — "audio
  generation" is in, "TTS" is out — and it reports no safety evals, so I skipped it for the same
  reason. Second instance in three days, so it is now logged as a pattern rather than a one-off.
- `tencent/EVIE-8B`, `tencent/EVIE-4.5B` — **skip.** Visual-document-retrieval embedding models
  (late-interaction token embeddings, 138 retrieval tasks, no safety evals). Out under both
  `covered_model_class` and the `tencent_hunyuan` scope note. Flagging that
  `tencent/EVIE-Preview-4.5B` is nonetheless an existing row, so the same family is currently both
  in and out of the corpus; folded into the friction line below.
- `nvidia/Nemotron-3-Labs-Ultra-Math-SFT` and `-RL`, plus the `nemotron-labs-imo-2026` collection —
  **skip.** Fetched the SFT repo: these are intermediate training-stage fine-tunes of the already
  catalogued `NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16`, specialised for olympiad mathematics for the
  IMO 2026 gold-medal ensemble. Checkpoint variants of a covered model under
  `distinct_model_release`, and their only safety content is the boilerplate Model Card++ subcard
  pointer that the `risk_domains` guidance explicitly says does not count.
- `inclusionAI/LLaDA-UI` — **skip for now, worth re-checking.** It is a genuine computer-use agent
  (MoE block-wise diffusion VLM producing grounded coordinates and structured GUI actions for
  mobile, desktop and web), which `covered_model_class` names explicitly. But it is a HuggingFace
  org-page lead, and `criteria.yaml` requires announcement evidence *outside* the repo for those;
  I searched and found none — InclusionAI's September announcements cover LLaDA-Image, not
  LLaDA-UI. If an announcement or technical report appears, this becomes a straightforward add.
- `epoch.ai/publications/long-context-latency-scaling-gpt-vs-claude` — **skip.** Measures
  time-to-first-token scaling to ~1M tokens for GPT-5.6 Terra and Sol against Claude Sonnet 5 and
  Opus 5, and infers attention architecture from the curvature. Genuinely about named models, but
  it is a serving-latency and cost analysis, not a capability or safety assessment; it would not
  sit in the evaluations section of a system card.
- `openai.com/index/safety-overview-gpt-6-astra/` — **already covered**, and re-verified rather
  than assumed: it is a `related_url` of `openai-gpt-6-astra-system-card`, alongside the hub
  landing page and `openai.com/index/gpt-6-astra/`.
- `mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier` (both trailing-slash
  variants) — **skip.** A €3B Series D funding announcement. No model documentation.

**Skipped, by category** (re-checked, unchanged from prior runs): auxiliary models per
`covered_model_class` and the per-publisher `scope` notes (`tencent/Hy-MT2-1.8B-GGUF` — machine
translation and a GGUF quant, `nvidia/magpie_tts_*`, `Nemotron-3-Diarization-preview`,
`inclusionAI/ArmorOCR-GGUF`, the NVIDIA `Ising-*` decoder and calibration repos, `SDLLM-*-Base`);
quantisation and size variants (`Ling-3.0-flash-VL-fp8`, `Qwen3.8-27B-NVFP4`, `*-NVFP4`, `*-FP8`,
`*-GGUF`); and non-documents (HuggingFace user profiles — `zkniu`, `MarkWang`, `sbhendigeri`,
`vitoyy`, `zhangxgu` — collections, dataset repos, discussion threads, HF paper pages,
`claude.com/solutions/commerce`, the `ai.meta.com/learn/agentic-ai/*` explainer pages and the
`applink.muse.ai` install link, Cursor case studies, x.ai Grok Bot product posts, the Palisade
podcast episodes, and the bulk `ai.google/*` navigation block).

## 2. Targeted search

- **Frontier releases in the 48 h window.** Checked the OpenAI Deployment Safety Hub (one new
  entry, ChatGPT Images 2.5, now catalogued; GPT-6 Astra already present) and the Anthropic
  newsroom (nothing on or after 2026-09-04; the newest posts remain the two 2026-09-01 items,
  both catalogued). No un-catalogued frontier release.
- **Restricted-access programme sweep.** Polled the named programmes. Both watch items carried
  since 2026-09-06 are **still open and unchanged for a third run**: the Cyber Verification
  Program still says Mythos access is coming "in the near future" while the current tier remains
  Opus- and Sonnet-class, and the Life Sciences Verification Program is still first-participants
  only and US-organisations only, with no dedicated programme page. Everything else — Rosalind
  Biodefense, Daybreak, the Trusted Access for Cyber lineage, Project Glasswing, Claude Science,
  Gemini for Science / Co-Scientist, Gemini 3.8 Flash Cyber / Fairwind, the Fable 5.1 / Mythos 5.1
  access policy — is catalogued. No new document in this class.
- **Independent evaluators.** METR's blog (newest: the 2026-08-31 security update, correctly not a
  model eval), UK AISI's work index (newest: 2026-08-27), Apollo Research's research index
  (newest: 2026-07-21) and SecureBio's Substack archive (newest: 2026-08-21, and its two most
  recent posts are pathogen-detection work, not model evals) all show nothing new in the window.
- **Orgs silent >14 days.** Phase A's index diffing covers this for most publishers, so I spot-
  checked the two quietest that produce no candidate links at all: Thinking Machines (newest post
  2026-07-31, already catalogued) and the US CAISI research blog (newest post 2026-03-23). Both
  genuinely quiet, not a monitoring failure. The CAISI blog's two 2026 posts are evaluation
  methodology, not assessments of named models, so their absence from the corpus is correct.

## 3. Citation mining

Mined the GPT-6 Astra system card, the largest recent add. It names five external evaluators:
**UK AISI** (alignment, monitorability), **Apollo Research** (strategic deception and sabotage
across six red-team environments), **SecureBio** (biological capabilities and safeguards),
**Irregular** (offensive cyber) and **Gray Swan** (indirect prompt injection). The first three are
allowlisted, and none of them has published a separate Astra report — their findings live inside
OpenAI's card, which we already hold.

**Irregular has published its own report, and we cannot catalogue it.** *Assessing GPT-6 Astra:
FrontierCyber Measures a Sharp Increase in Cyber Capability* (2026-09-03) reports Astra solving
86 of 226 FrontierCyber challenges against 34 for GPT-5.6 Sol, per-tier success rising from 14 to
63 % (Easy), 15 to 30 % (Medium) and 17 to 39 % (Hard), CyScenarioBench average success moving
from 27 to 59 %, and multiple zero-days found and exploited in widely deployed database systems,
browsers and mobile devices. It passes the system-card test unambiguously — it *is* the source of
a system-card section. But `irregular` is not in `config/sources.yaml`, so there is no key to
propose it under, and TASK.md is explicit that I must not file one org's work under another's.
Written up in `PROPOSALS.md` with the broader point: the allowlist covers the non-profit and
government evaluator ecosystem well and the commercial red-team vendor ecosystem not at all, which
biases the corpus against cyber evaluations specifically, because that is where those vendors
concentrate. Gray Swan is the same shape of gap.

The card's other citations resolve cleanly: the Hugging Face incident technical report is already
catalogued, and the GPT-5.6 Sol and GPT-5.5 cards are present. One citation I could **not**
adjudicate: *HealthBench Professional* (`cdn.openai.com/…/HealthBench-Professional.pdf`), because
the fetch tool cannot read PDFs — see friction. On the face of it a first-party benchmark-
construction paper is out under the "research that merely uses models" exclusion, but it plausibly
scores named models, and TASK.md forbids proposing a document I have not read. Carried forward.

## 4. Open issues

`logs/open_issues.json` is empty. No investigations, no comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is empty, so no `dead` proposals. Worth noting for context that Phase A
recorded 12 blocked links today against 254 OK — bot-blocking, not death, and none reached the
escalation threshold.

## 6. Document updates

18 entries pending, but 15 are the carry-over set the 2026-09-07 run already reviewed and
attributed to HuggingFace widget churn, Substack title-extraction noise and the Palisade redirect
stubs; that diagnosis holds and I did not re-litigate it. **Three diffs were new this run and all
three were read.**

**Annotated — a real document change**

- `nvidia-gr00t-h-model-card` v525 — the header notice grew from "Please see GR00T-H-N1.7 for the
  latest version of this model" to "This is the N1.6 non-commercially usable version of GR00T-H.
  Please see GR00T-H-N1.7 for the newer and commercially usable version of this model". A licensing
  disclosure that was not there before, and exactly the class of change (licence changed) the task
  calls substantive.

**Skipped as noise**

- `deepseek-deepseek-v4-pro-0813-model-card` v524 — download counter 85,230 → 164,699, "Spaces
  using" 5 → 12, and one new community leaderboard row (`hkust-nlp/Toolathlon`). Textbook instance
  of the HuggingFace widget churn diagnosed on 2026-09-07.
- `securebio-claude-opus-4-6-independent-eval-2` v523 — the title and subtitle lines dropped out of
  the extraction; the body is unchanged. Substack title-extraction noise, same pattern as the
  Redwood rows.

## 7. Friction log

Two lines appended to `logs/friction.jsonl`:

- `pdf_unreadable_agent_side` — the fetch tool returns raw binary for every PDF. It cost nothing on
  ChatGPT Images 2.5 only because OpenAI happens to serve an HTML twin at the same slug; most of
  the corpus is PDF-only (the Gemini model cards, the `www-cdn.anthropic.com` rows, the RAND and
  METR reports), so on those I would be attesting criteria I could not verify. It did cost me the
  HealthBench adjudication above. The `r.jina.ai` proxy the 2026-09-06 run used to get past the
  `openai.com/index` 403 wall now returns **HTTP 401**, so that workaround is gone — which also
  means that run's 403 finding should not be assumed still to hold. Suggested fix: a read-only
  helper resolving a URL or slug to the text the pipeline already extracted into `data/text/`.
- `ambiguous_criteria` — the AuK / StepAudio 2.5 speech-model question, now with the corpus
  inconsistency spelled out (`voxtral-tts-26-03`, `voxtral-mini-transcribe`, `step-audio-r1-1` and
  `EVIE-Preview-4.5B` are all rows that today's `covered_model_class` would exclude).

One piece of good news on tooling: the CLI-flag invocation of `propose_doc.py` works cleanly from
inside the sandbox and, unlike the `printf … | --json -` route the 2026-09-07 run was forced onto,
it imposes no apostrophe ban — so this run's justifications and notes are written in normal prose.
The heredoc and `>>` blocks are still real; appending to `friction.jsonl` and `PROPOSALS.md` again
required the Edit tool.

## 8. Proposals

One dated entry appended to `logs/PROPOSALS.md`: the Irregular / Gray Swan allowlist gap described
in section 3, with a concrete `sources.yaml` addition suggested and the note that admitting Gray
Swan would force the still-open arXiv-canonical-URL decision.

## Judgment calls worth an operator's eye

- **Four risk-domain tags on ChatGPT Images 2.5, where Images 2.0 carries only `cbrn`.** I tagged
  `societal_harm` and `harmful_manipulation` because the per-category evaluation table reports
  quantitative results for hate, extremism, self-harm and abuse (societal) and for political
  imagery and deepfakes (manipulation), which is substantive assessment content rather than a
  passing mention. `cyber` is the weakest of the four: the card gives a Preparedness threshold
  determination without capability scores. I read a threshold determination as a risk analysis,
  which the convention admits, but if the operator reads it as boilerplate then `cyber` and
  arguably `cbrn` should come off — and then the Images 2.0 row is the one that is wrong, not this
  one. Either way the two rows should agree, and right now they do not.
- **Cataloguing the Meta Muse post at all, with `has_safety_evals: false`.** It is a security
  architecture description, not an evaluation: no benchmark numbers, no red-team findings, only the
  unquantified claim that Muse Spark 1.3 is "close to SOTA" on prompt injection resistance. I
  admitted it because it is Meta's primary safety documentation for a frontier agent and names the
  model, and because `policy.when_uncertain` is `admit_and_flag` — but the honest description is
  that this is safeguards material a system card would carry, not a card. `risk_domains` left empty
  because agent hijacking, exfiltration and unauthorised purchases are domain-generic safeguard
  robustness. If the operator would rather this were not a row, it is one revert.
- **Ling-3.0-flash-VL as a distinct release rather than a variant.** It shares the Ling-3.0-flash
  base and inherits its language and long-context behaviour, so a strict reading of
  `distinct_model_release` could call it a variant. I read a new input modality plus new agentic
  capability as a distinct release, following the corpus precedent of `LLaDA-Image` sitting beside
  `LLaDA2.2-flash`. Its publication date (2026-09-04) comes from the repository's initial commit,
  corroborated by the Ant Ling announcement on X the same day.
- **The Irregular gap is the item I would act on first.** Everything else here is a one-row
  correction; that one is a systematic blind spot, and it is in the risk domain where the frontier
  is currently moving fastest.
