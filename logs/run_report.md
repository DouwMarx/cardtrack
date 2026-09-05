# cardtrack agent run report — 2026-09-05T06:19Z-local

Run id `2026-09-05T06:19Z-local`. Phase A: 250 checked, 250 ok, 0 blocked, 0 dead,
81 new candidate links, 20 stored versions awaiting a change summary, 0 open GitHub issues,
0 blocked-URL escalations.

**Lookback**: `logs/.agent_last_success` was missing, so the search window fell back to the
72-hour minimum. Yesterday's run (2026-09-04) failed entirely — Phase A errored on all 246
checks and Phase B never started — so the last successful agent run was 2026-09-03 and 72 h
covers the gap. Today is a Saturday, so no weekly retrospective sweep was due.

## Proposals submitted — 8 adds, 5 annotations, all `written`

| # | Action | Slug | Verdict |
|---|---|---|---|
| 1 | add | `openai-gpt-6-astra-system-card` | `written` (doc 283, ver 500) |
| 2 | add | `google-deepmind-gemini-3-8-flash-model-card` | `written` (doc 284, ver 501) |
| 3 | add | `google-deepmind-gemini-3-8-flash-cyber-access-policy` | `written` (doc 285, ver 502) |
| 4 | add | `xai-grok-4-6-other` | `written` (doc 286, ver 503) |
| 5 | add | `meta-muse-spark-1-3-other` | `written` (doc 287, ver 504) |
| 6 | add | `anthropic-claude-mythos-preview-access-policy-2` | `written` (doc 288, ver 505) |
| 7 | add | `inclusion-ai-llada-image-model-card` | `written` (doc 289, ver 506) |
| 8 | add | `alibaba-qwen-qwen-drive-1-0-4b-model-card` | `written` (doc 290, ver 507) |
| 9 | annotate | `inclusion-ai-ui-venus-2-9b-model-card` v479 | `written` |
| 10 | annotate | `nvidia-nvidia-nemotron-3-super-120b-a12b-model-card` v495 | `written` |
| 11 | annotate | `openai-gpt-5-6-sol-other` v499 | `written` |
| 12 | annotate | `nvidia-cosmos3-edge-model-card` v497 | `written` |
| 13 | annotate | `openai-gpt-5-6-cyber-other` v482 | `written` |

No rejections and no duplicates this run.

### Notes on the adds

**GPT-6 Astra System Card** (OpenAI, 2026-09-03) — the run's headline find, from the
Deployment Safety Hub index diff. I fetched and read the ~115-page PDF. Canonical URL is the
PDF per the full-document rule, with the hub page as `web_version` and the launch post as
`announcement`. Tagged `cbrn`, `cyber`, `loss_of_control`, `societal_harm`; `closed`. First
OpenAI model to meet the Critical cybersecurity threshold under the Preparedness Framework.

**Gemini 3.8 Flash model card** (Google DeepMind, 2026-09-02) — read the PDF in full.
Only `societal_harm` tagged: the card's Frontier Safety Assessment does not run per-domain
evaluations, it inherits the Gemini 3.7 Flash result, so the only substantive assessment
content of its own is the content-safety table and the child-safety human red teaming.
Canonical URL is the `deepmind-media` PDF, matching the existing Gemini convention.

**Fairwind Program** (Google, 2026-09-02) — `access_policy` for the named gated model
Gemini 3.8 Flash Cyber, which ships only through the program. Application plus vetting plus
operational conditions on use, so it clears the named-model-plus-program-structure bar.
`restricted`. Direct counterpart to the existing `google-deepmind-gemini-3-5-flash-cyber-other`.

**Biosecurity at the frontier** (xAI, 2026-09-01) — `other`; reports commissioned LatchBio
BioSecBench-Refusal (62.1% average) and BioSecBench-Surveillance (53.5%) results for
Grok 4.6 against Grok 4.5 and 4.3. Passes the system-card test cleanly. LatchBio is not
allowlisted; if it publishes its own copy that is a separate co-published document.

**Muse Spark 1.3 Evaluation Methodology** (Meta, 2026-09-02) — one row, not two: the
methodology PDF is canonical and the launch blog is recorded as `announcement`, per the rule
against cataloguing an announcement and its full report separately. Capability benchmarks
only, so `has_safety_evals: false`. **Gap flagged**: Meta has published no Muse Spark 1.3
safety and preparedness report — the 1.1-pattern URL
`ai.meta.com/static-resource/muse-spark-1-3-evaluation-report/` returns HTTP 500 and search
finds nothing. The launch post asserts improved adversarial robustness and prompt-injection
resistance without publishing results. Worth re-checking on later runs.

**Expanding Project Glasswing** (Anthropic, 2026-06-02) — a backlog gap, not a recent
release, found while polling known restricted-access program names. The database held the
Glasswing launch page (2026-04-07) and the initial update (2026-05-22) but not the expansion
post that sits between them, which extends Claude Mythos Preview access to ~150 new
organizations under stated security requirements and critical-infrastructure eligibility.
Exactly the class the retrospective sweep exists to catch.

**LLaDA-Image** and **Qwen-Drive-1.0-4B** — HuggingFace org-page leads that survived the
scope notes. Both open-weight permissive, both with the publishing org's own technical
report supplying notability outside the repo. Neither reports safety evaluations; for
Qwen-Drive that was a judgment call (see below). LLaDA-Image folds the Turbo and FP8
re-uploads into one row.

### Notes on the annotations

Reviewed all 20 entries in `logs/updated_docs.json`, annotated the 5 substantive ones.

The most consequential is **UI-Venus-2-9B**: the card's headline safety claim was materially
revised downward — the previous version claimed the OSBlind attack success rate was cut to
12.3% from the 90%+ typical of prior GUI agents; the new version reports 11.3% on OSHarm and
**48.8%** on OSBlind against 25.3% and 79.4% for the Qwen3.5-9B base. The same revision
withdraws the Apache-2.0 declaration and states the model-weight license is pending final
confirmation, citing conflicting upstream license statements. The stored `openness` value for
this row may now be wrong; I recorded the change in the annotation rather than guessing at a
`field_update`, since the state summary does not expose the current stored value.

**GPT-5.6-Cyber** (v482) is a removal-only diff and I judged it substantive rather than
extraction noise: it drops two complete, semantically coherent blocks — the macOS Keychain /
Chrome cookies worked example (the page's only concrete demonstration of the reduced-refusal
behaviour it describes) and a named customer testimonial — while every adjacent line and every
quantitative result is byte-identical. Flagging the reasoning in case an operator disagrees.

### Skipped, with reasons

- **`anthropic.com/news/enterprise-frontier-safeguards`** (2026-09-01) — read it. Not an
  access policy: EFS is an opt-in data-residency and automated-monitoring feature for existing
  enterprise customers, explicitly *not* a condition of access to any named model. Product
  announcement, out of scope for `other` as well.
- **`anthropic.com/research/formalizing-fermats-last-theorem`** (2026-09-04) — read it.
  Research that uses Claude as a tool to produce a proof; no evaluation of a named model
  against results. Excluded by `about_a_specific_model_or_eval`.
- **`anthropic.com/news/model-hardware-standard-research-preview`** (2026-08-27) — a gated
  research preview with an application process, but it gates a hardware *specification*, not a
  named model or model family. No named model, so skipped.
- **UK AISI "Optimal stopping"** (2026-08-27) — fetched; a methodology paper about the
  `optstop` evaluation tool, tested on MATH/GPQA/WritingBench with no model named or assessed.
  Fails the system-card test.
- **RAND WRA5251-1** (2026-09-02) — a life-sciences research-policy framework; no named model.
- **`tencent/Ex-Omni`** — fetched; a facial-blendshape animation model from an external
  academic collaboration, outside the Tencent scope note (Hy LLM/VLM line, HY-World, flagship
  embodied/UI agents) and with no safety evals.
- **`inclusionAI/Ling-3.0-flash-Fin`**, **NVIDIA `Qwen3.8-*-NVFP4`**, **`*-GGUF`**,
  **`*-singprobe`**, **NVIDIA `SDLLM-*-1.7B-Base`** — domain fine-tunes, quantizations and
  small research artifacts; fail `distinct_model_release` or `notable_release`.
- **xAI Grok Bot posts, Cursor customer stories, Mistral Agentic Search, Meta Muse Voice
  Transcribe, `blog.google` agentic-video and WeatherNext 3, Epoch data-insights and
  FrontierMath-Erdos, `ai.google` / `labs.google` navigation links** — product and marketing
  pages, or trend analyses with no named model under assessment. The
  `ai.google/gemini-for-science` index contributed ~40 pure navigation links this run; the
  `google_deepmind` scope note handled them correctly.
- **HuggingFace `/papers/`, `/discussions/`, and bare user-profile links** — not primary
  model documentation.
- Annotations skipped as noise: `anthropic-claude-fable-5-addendum` (v498, related-content
  sidebar only), `tencent-hunyuan-hy3` (v492, HF leaderboard-widget reordering),
  `us-caisi-kimi-k3-independent-eval` (v477, an "Updated August 28, 2026" date line with no
  body change), the two Gemini cards (v480/v481, one-clause use-case rewording), and the
  remaining download-count and Spaces-count churn. `inclusion-ai-ling-3-0-flash` (v491) was a
  near miss — the vLLM install switched from an inclusionAI fork to upstream and two
  leaderboard scores appeared — but it lost the fifth slot to GPT-5.6-Cyber.

## Blocked URLs and open issues

`blocked_escalations` and `open_issues` were both empty, so tasks 4 and 5 had no work.
`open_issues.json` reading `[]` is indistinguishable from a failed GitHub fetch, and
yesterday's log shows `api.github.com` was unreachable then; today's Phase A reported no
errors, so I am treating the empty list as real.

## Citation mining

Fetched the GPT-6 Astra card's external-evaluation sections (8.8 alignment — UK AISI and
Apollo Research; 9.3 monitorability — UK AISI; 10.1.1 bio/chem — SecureBio) and checked each
evaluator for a standalone publication. **None exists yet**: `aisi.gov.uk/work` shows nothing
after 2026-08-27, `apolloresearch.ai/research` nothing after 2026-07-21, and no SecureBio
Astra report is findable. Their findings currently live only inside the OpenAI card. Recorded
as a lead in the Astra row's `notes` — these are likely to appear as standalone reports in the
next days and should be caught then.

## Silent-org check

Publishers with no document dated on or after 2026-08-22 at run start: mistral, cursor,
thinking_machines, xiaomi, nvidia, moonshot_ai, poolside, stepfun, and the evaluators
uk_aisi, apollo_research, epoch_ai, securebio, us_caisi, rand, saferai, far_ai,
palisade_research. Searched mistral, thinking_machines, moonshot_ai, epoch_ai, uk_aisi and
apollo_research; the only qualifying documents found were the two UK AISI/Apollo checks above
(neither publishing) and Mistral's recent output, which is OCR, transcription and the Agentic
Search retrieval product — all excluded by the Mistral scope note. Nothing proposable.
Restricted-access program poll (Rosalind, Daybreak, Glasswing, LSVP, Cyber Verification
Program, Claude Science, Gemini for Science / Co-Scientist, Fairwind) produced the two
Google Fairwind adds and the Anthropic Glasswing backfill.

## Friction (3 lines appended)

1. **`publisher_bot_wall`** — `openai.com/index/` returned HTTP 403 to all four fetches
   attempted. Concrete cost this run: two OpenAI access-policy documents absent from the
   corpus, `trusted-access-for-cyber/` and `scaling-trusted-access-for-cyber-defense/`, both
   defining vetting conditions for named gated cyber models. I could not read them, so I could
   not attest criteria, so I did not propose them. Also unread: `safety-overview-gpt-6-astra/`
   and `path-to-astra/`, the launch-day safety companions to the Astra card. This is new
   evidence for the open 2026-08-12 PROPOSALS entry, not a new proposal.
2. **`ambiguous_criteria`** — `has_safety_evals` for task-domain safety metrics (Qwen-Drive's
   WaymoQA safety and at-fault scores). Escalated to PROPOSALS.md; third instance.
3. **`stale_task_input`** — missing `.agent_last_success`, caused by yesterday's total
   Phase A/B failure, which nonetheless committed as "no changes".

## PROPOSALS.md

One new entry, **2026-09-05 — `has_safety_evals` has no rule for domain-safety metrics**.
Third recurrence of the same judgment call, and the corpus already holds several robotics,
driving and world-model rows likely judged inconsistently by different runs. Asks for one
line in `criteria.yaml`. Nothing filed for the `openai.com` block — the 2026-08-12 entry
already covers it and this run only adds evidence.
