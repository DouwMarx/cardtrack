# cardtrack daily curation — run `2026-08-14T07:00Z-local`

Corpus went from 206 to 218 documents. Twelve proposals, twelve written, none rejected and none
routed to a review issue.

The run's defining fact is that **Phase A saw nothing at all**. It reported `checked: 203,
ok: 0, errors: 203`, and Phase B logged two `error connecting to api.github.com` lines — a
transient network outage during the 07:00:36Z window. Five minutes later the same venv fetched
all 43 configured `index_urls` successfully, 43/43 HTTP 200. So `candidates.json` carries
nothing newer than yesterday, no link-check or fingerprint pass ran against the 202 active
documents, and everything below came from my own sweep, targeted search and citation mining
rather than from the pipeline. That silent-degradation failure is this run's first
`PROPOSALS.md` entry.

The second is what the manual sweep exposed once it went beyond the configured index set:
**Mistral had been 108 days silent because nobody was polling its model-card catalogue.** Nine
in-scope 2026 cards were sitting at `docs.mistral.ai/models/…`, one of them ten days old. Eight
are now in. The same shape explains Anthropic's Project Deal (112 days, filed under `/features/`)
and OpenAI's GPT-5.6-Cyber post (four days, filed under `/index/`).

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 2,579 — **0 new** (Phase A fetched nothing) |
| Index pages swept by hand | 43 (every configured `index_url`), all 200, plus `docs.mistral.ai/models/model-cards/` |
| HuggingFace orgs swept by creation date via API | 12 (`Qwen`, `deepseek-ai`, `tencent`, `XiaomiMiMo`, `nvidia`, `moonshotai`, `stepfun-ai`, `inclusionAI`, `meta-models`, `meta-llama`, `ByteDance`, `zai-org`) |
| Documents fetched and read | 24 (beyond the 43 index pages) |
| Web searches | 10 |
| Proposals submitted | 12 |
| Written as rows | **12** (ids 207–218) |
| Rejected | 0 |
| Routed to review issues | 0 |
| Open GitHub issues to investigate | 0 (`logs/open_issues.json` is `[]`, though it was written during the outage — treat with suspicion) |
| Blocked-URL escalations | 0 (`blocked_escalations` empty) |
| Friction lines appended | 5 |
| `PROPOSALS.md` entries | 2 |

## Proposals and validator verdicts

| # | Document | Publisher | Date | Safety evals | Verdict |
|---|---|---|---|---|---|
| 1 | DeepSeek-V4-Pro-0813 Model Card | deepseek | 2026-08-13 | no | `written` 207, `deepseek-deepseek-v4-pro-0813-model-card` |
| 2 | Model Card: Shieldstral 1.0 | mistral | 2026-08-04 | no | `written` 208, `mistral-shieldstral-1-0-model-card` |
| 3 | Model Card: OCR 4.1 | mistral | 2026-07-16 | no | `written` 209, `mistral-mistral-ocr-4-1-model-card` |
| 4 | Model Card: OCR 4.0 | mistral | 2026-06-23 | no | `written` 210, `mistral-mistral-ocr-4-0-model-card` |
| 5 | Model Card: Leanstral 1.5 | mistral | 2026-06-30 | no | `written` 211, `mistral-leanstral-1-5-model-card` |
| 6 | Model Card: Leanstral | mistral | 2026-03-16 | no | `written` 212, `mistral-leanstral-model-card` |
| 7 | Model Card: Mistral Moderation 2 | mistral | 2026-03-01 | no | `written` 213, `mistral-mistral-moderation-2-model-card` |
| 8 | Model Card: Voxtral TTS | mistral | 2026-03-23 | no | `written` 214, `mistral-voxtral-tts-model-card` |
| 9 | Model Card: Voxtral Mini Transcribe Realtime | mistral | 2026-02-04 | no | `written` 215, `mistral-voxtral-mini-transcribe-realtime-model-card` |
| 10 | Model Card: Voxtral Mini Transcribe 2 | mistral | 2026-02-04 | no | `written` 216, `mistral-voxtral-mini-transcribe-2-model-card` |
| 11 | **Expanding Daybreak as the Cyber Defense Window Narrows** | openai | 2026-08-10 | **yes** | `written` 217, `openai-gpt-5-6-cyber-other` |
| 12 | Project Deal: our Claude-run marketplace experiment | anthropic | 2026-04-24 | no | `written` 218, `anthropic-claude-opus-4-5-other` |

### 1. DeepSeek-V4-Pro-0813 (the one genuinely-today release)

Created on HuggingFace 2026-08-13 and announced the same day on DeepSeek's own news feed
(`api-docs.deepseek.com/news/news260813`). The card says it supersedes the preview version and
attaches a DSpark speculative-decoding module to the V4-Pro preview structure. Ten benchmarks
against V4-Flash-0731, both preview models, GLM-5.2, Kimi K3, Opus-4.8 and Fable-5 — HLE 42.7 /
60.0 with tools, Terminal Bench 2.1 87.9, Cybergym 83.3, DeepSWE 62.7. Catalogued as a distinct
release on the corpus's own precedent: `DeepSeek-V4-Flash-0731` already sits beside the April
V4-Pro/V4-Flash preview card. `openness=open_weight_permissive`, MIT, verified in the card's
licence section. `has_safety_evals=false` is the finding: no safety, red-team, refusal, misuse
or risk content anywhere — Cybergym appears purely as a capability score.

Not proposed alongside it: `Qwen3.8-2.4T-A95B-FP8`, `Ling-3.0-tiny-int4`, `Ling-3.0-tiny-fp8`,
`Muse-Glimmer-30B-GGUF`, `-ExecuTorch-PTE` and `-assistant` (the last is Muse Glimmer's
speculative-decoding drafter, not a model release), and `nvidia/Cosmos3-Edge-Policy-DROID`,
already covered by the Cosmos3-Edge row. `ByteDance/Bernini-Diffusers-v2` (2026-08-13) is a
real new release but ByteDance is not on the allowlist.

### 2–10. The Mistral catalogue

`mistral` read 108 days silent this morning. `mistral.ai/news/` is its only `index_url`;
its canonical cards live at `docs.mistral.ai/models/<slug>`, indexed at
`docs.mistral.ai/models/model-cards/`. Every card below carries its own explicit "Release Date"
line, which is what `publication_date` records.

- **Shieldstral 1.0** (2026-08-04) — 3.8B multimodal moderation model, 32k context, natural-language
  policy questions returning binary classifications, prompt/response/paired-image assessment and
  refusal detection. `open_weight_permissive`: Apache 2.0, weights at
  `mistralai/Shieldstral-1.0-3B`. `has_safety_evals=false` despite being a safety model — the card
  reports no evaluation results at all.
- **OCR 4.1** (2026-07-16) and **OCR 4.0** (2026-06-23) — separate releases a month apart, 4.1 adding
  block-level confidence scores. `closed`; no weights repo under `huggingface.co/mistralai`.
- **Leanstral 1.5** (2026-06-30) and **Leanstral** (2026-03-16) — 119B-total/6.5B-active Lean 4
  formal-proof models, both `open_weight_permissive` with public weights
  (`Leanstral-1.5-119B-A6B`, `Leanstral-2603`). The 1.5 card records the older model's retirement.
- **Mistral Moderation 2** (2026-03-01) — 128k moderation model with jailbreak detection, `closed`.
- **Voxtral TTS** (2026-03-23) — zero-shot voice cloning, 9 languages, ~90 ms to first audio. The
  `has_safety_evals=false` here is substantive rather than clerical: a voice-cloning model
  documented with no misuse discussion, consent or provenance safeguards. `openness` omitted —
  custom "GACC BY-NC 4.0v26.03" licence, no corresponding weights repo, so nothing verifiable.
- **Voxtral Mini Transcribe Realtime** and **Voxtral Mini Transcribe 2** (both 2026-02-04) — the
  live and batch transcription models, separate cards, API names and prices. The realtime one has
  its own weights repo (`Voxtral-Mini-4B-Realtime-2602`, Apache 2.0); the batch one does not
  clearly, so its `openness` is omitted. If maintainers read the two as one family release, #10 is
  the row to fold into #9 — that judgement is in the proposal notes rather than hidden.

Not proposed: `docs.mistral.ai/models/zai-glm-5-2`. It is a Mistral-authored card for Z.ai's
GLM-5.2 served on Mistral's platform. Filing a third party's model under `publisher: mistral`
would misattribute it, and `zai` is not on the allowlist. Recording it here rather than
proposing it, per the co-publication rule.

### 11. GPT-5.6-Cyber — the gap two previous runs recorded, now closed

`openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/`, published
2026-08-10, is OpenAI's launch-and-evaluation post for GPT-5.6-Cyber, built on GPT-5.6 Sol and
trained to reduce refusals on dual-use cyber tasks. It is dense with exactly the content the
system-card test asks for: an internal Advanced Cybersecurity Completion Rate evaluation
(**95.0%** for GPT-5.6-Cyber against 1.5% for Sol with safeguards, 2.0% via Daybreak Blue,
57.3% for GPT-5.5-Cyber, over exploit-chain development, authentication bypass and privilege
escalation); ExploitGym and ExploitBench exploit-development results including a 300→600-turn
sensitivity analysis; a zero-day severity-and-calibration benchmark; and a Vulnerability
Discovery and Report Writing evaluation on which GPT-5.6-Cyber is reported as *worse* than Sol.
It states the Preparedness Framework determination — High for cyber, below Critical — and
documents the Daybreak Blue/Red access tiers, identity verification, monitoring and scoped
permissions, along with the residual misuse and misalignment risk of running with reduced
safeguards. It also says a full system card "will be published at a later date"; the Deployment
Safety Hub still carries nothing newer than the 2026-08-06 GPT-5.6 August update.

**This was a retry of a proposal the 2026-08-12 run made and the validator rejected**
(`document_retrievable=false: HTTP 403`), which the run contract discourages. I did not know
that when I proposed it — I reached the URL from a search for GPT-5.6-Cyber and read the page
through `cardtrack.fetch`'s impersonation fallback after `WebFetch` 403'd — and found the prior
rejection afterwards while reading `PROPOSALS.md`. The retry succeeded, which confirms that
run's diagnosis that the 403 was a transient bot-wall rather than a property of the URL. Flagged
in `friction.jsonl` as `transient_reject_recovered`, because the general lesson is that
"don't retry rejected proposals" is right for criteria rejections and wrong for
fetch-dependent ones.

### 12. Project Deal (citation mining)

Yesterday's Anthropic multiagent-systems report links two prior pieces; Project Glasswing is
already catalogued, Project Deal was not. It is a controlled experiment, not an essay: 69
employees with $100 budgets, four parallel Slack marketplaces, two runs Opus 4.5 only and two
randomly assigning Opus 4.5 or Haiku 4.5, producing 186 deals over 500+ items and just over
$4,000 in value. Opus users completed ~2 more deals, items sold for $3.64 more under an Opus
agent, Opus buyers paid $2.45 less — and perceived fairness was identical (4.05 vs 4.06), so the
Haiku-represented participants did measurably worse without noticing. That is agentic-evaluation
content in the shape the corpus already accepts from `project-pilot` and `project-fetch-phase-two`.
`has_safety_evals=false`: confabulation, jailbreaking, prompt injection and quiet capability-gap
inequality are named as deployment risks, but there is no red-teaming and no formal risk
assessment.

## Checked and deliberately skipped

- **Cursor** — three new blog posts, none in scope: `aiuc-1` (a security *certification*
  announcement, no named model), `builds` (product feature) and `firetiger` (acquisition).
  Cursor is allowlisted as a co-publisher of Grok cards; nothing of that kind appeared.
- **Epoch AI** — `chip-performance-per-dollar` (2026-08-13) and `will-financing-bottleneck-ai-compute`
  are compute-economics pieces with no named-model assessment. `expanding-our-analysis-of-biological-ai-models`
  (2026-02-20) surveys documentation practices across 1,196 models rather than evaluating a named
  one — it fails the system-card test the way a meta-analysis does.
- **OpenAI "Putting frontier cyber models in more trusted hands"** (2026-08-10) — same-day sibling
  of #11, but it is a launch-partner announcement (IBM Consulting, Palo Alto Networks, Akamai)
  with no evaluations. Explicitly excluded from `doc_type: other`.
- **Anthropic transparency hub** — the Fable 5 & Mythos 5 system card is now also served from a
  new `www-cdn.anthropic.com` hash URL. The catalogued row points at the stable HTML landing page
  (`anthropic.com/claude-fable-5-mythos-5-system-card`), so this is a CDN asset rotation, not a new
  document; whether the PDF's content changed is the fingerprint pass's job, and that pass did not
  run today.
- **Tencent** — a `ui-mate` collection appeared on the HF org page but contains no items yet.
- **SecureBio, Redwood, RAND, METR, Apollo, UK AISI, US CAISI, Transluce, SaferAI, FAR.AI,
  Palisade, Thinking Machines, DeepMind, Meta, xAI, poolside** — swept; the only "new" links were
  `/comments` and `/feed` variants of already-catalogued posts, or static assets. Targeted searches
  for METR, Apollo and UK AISI August output found nothing newer than what is already in.
- **Silent-org audit** — HF API by creation date confirms `xiaomi` (109 d), `stepfun`, `moonshot_ai`
  (18 d) and `tencent_hunyuan` (30 d) have published no new repos. `poolside` (108 d) and
  `palisade_research` (99 d) show nothing new on their own indexes. Mistral's 108-day silence was
  the one that turned out to be an artefact of where we look, which is why the path-audit
  suggestion is in `PROPOSALS.md`.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty, so there was nothing to
investigate or comment on. Both files were generated during the outage window, and Phase B could
not reach `api.github.com` — an empty issue list this morning is weak evidence that no issues are
open. No comments were posted.
