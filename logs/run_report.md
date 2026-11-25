# Run report — 2026-11-25T06:16Z-local

Last agent success: 2026-11-24T06:28Z. Search window: the 72 h minimum (since 2026-11-22). Today is a Wednesday, so there was no weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | `nvidia-nemotron-labs-image-30b-a3b-model-card`: https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B (text-to-image, 30B-A3B, NVIDIA non-commercial license; open_weight_restrictive; has_safety_evals false) | **written** (doc 495, v1331) |
| 2 | add | `anthropic-claude-mythos-5-2-access-policy`: https://support.claude.com/en/articles/15425695-covered-models (Anthropic "Covered Models" designation and terms page; Fable/Mythos 5, 5.1, 5.2; restricted) | **written** (doc 496, v1332) |
| 3 | field_update | `anthropic-claude-fable-5-access-policy` related_urls += the 2026-11-23 EFS public-beta post (kind announcement); the existing x.com thread is kept | **written** |
| 4 | annotate_version | `openai-gpt-6-2-astra-system-card` v1321: Nov 22 change-log entry and P0/P0.5 definitions in the Sabotage v2 section | **written** |

Notes on #1 and #2:
- **#1**: the model is the raster generator of NVIDIA's Nemotron-Labs-VisualCreation ("Pixel as Code") framework, initialized from Nemotron 3 Nano.
  - Notability outside the repo: the arXiv tech report 2611.31358 (submitted 2026-11-23), which is also used as the publication date, plus coverage by zicq, AGI Hunt and explainx.
  - The HF repo was created privately on 2026-09-24.
  - The card has benchmark tables but only a generic limitations paragraph.
- **#2**: this is a living page that shows no date ("Updated over 2 weeks ago").
  - I used the first Wayback capture, 2026-06-09T21:27Z, which matches the first designation date in its own table.
  - It sets access terms that follow the named models on every surface: Mythos models go to approved partners only, there is 30-day minimum retention, and the ZDR transition is tied to EFS.
  - Recipe: the Wayback CDX API (`web.archive.org/cdx/search/cdx?url=…&limit=5`) fetches fine through read_doc.py `--raw`.

## Task 1: Phase A candidates (first_seen 2026-11-25)

- **nvidia/Nemotron-Labs-Image-30B-A3B**: proposed (#1).
- **nvidia/BioReason-Pro-2-9B-RL / -SFT**: skipped.
  - It is a single-task protein-function predictor (GO terms plus a rationale; it generates no sequences), a Qwen3.5-9B LoRA plus ESM3 encoder.
  - That makes it a domain task model, and the card has no safety evals, only the boilerplate Model Card++ subcard reference.
- **NIST CAISSI "Towards best practices for evaluating SI-driven uplift"** (draft NIST SP 2400-801, 2026-11-24): skipped. It is a methodology guideline open for comment and evaluates no named model.
- **METR "Interpreting a recent acceleration in pretraining loss"** (2026-11-24): skipped. It is commentary on OpenAI's published perplexity data, not an evaluation of a named model. The underlying OpenAI piece (Pachocki, "Perplexity and Intelligence") is a policy essay, not model documentation.
- **inclusionAI Ming-Image collection**: skipped. It only re-surfaced, and its items are Ming-Image-0.1 repos last updated in October.
- **Papers and furniture**: skipped as research or furniture. This covers Tencent papers (VenusOCR2.0, WeMM-Ecom), TiMiHOKGameTranslator (translation, out of scope), the nvidia DVSM Space, NuRec/simready discussions, the Microduck blog, Kimi K3/K3.1 tokenizer discussions, the StepFun eDMD paper, MiniMax LinkedIn and a dataset, an inclusionAI paper, a Baidu README discussion, HF user profiles, and the thinkingmachines careers page.
- Older carried-over candidates (first_seen 11-11 to 11-24) were triaged in earlier runs and not revisited.

## Task 2: Targeted web search

Queries:
- system card November 2026
- model card released November 24 2026
- trusted access program November 2026
- Enterprise Frontier Safeguards beta (claude.com/anthropic.com)
- independent eval METR/AISI/Apollo November 2026
- OpenAI pretraining loss
- DeepSeek/Mistral/xAI/Meta week of Nov 23
- Gemini for Science / Claude Science / GPT-Rosalind / LSVP
- open-weight releases Nov 23–24

Results:
- **Anthropic EFS public beta (2026-11-23)**: the claude.com post names no specific model, so I linked it to the existing EFS row (#3). Searching around it turned up the uncatalogued Covered Models page (#2).
- **Already cataloged**: GPT-6.2 Astra/Sol, GPT-6 Cyber (system card and announcement), the GPT-Rosalind family (5.5 card, 6 addendum, 5 access-policy rows), Fable/Mythos 5.2, Gemini 4 Neon, and METR's Q4 capability update.
- **AWS Bedrock Trusted Access API**, **AWS Strands Decider v2** and **Sarvam-105B-1711**: skipped. The publishers are not allowlisted.
- **Anthropic "Early progress on accelerating drug development with Claude"**: skipped. It is partnership case studies, not a model evaluation.
- **qwen-audio-3.1-live**: skipped. It is an API-only voice model in Model Studio release notes, with no model card.
- **No new documented releases** from DeepSeek, Mistral, xAI or Meta in the window, which matches the third-party trackers.

## Task 3: Citation mining

- **Nemotron-Labs-Image card**: cites Nemotron 3 Nano Omni, Nemotron 3.5 Super-VL, Nemotron 3 Ultra and Cosmos 3, all in the DB. VisionCode is not released yet.
- **Covered Models page**: links sub-pages on retention and BAA, which are policy furniture.
- **Yesterday's adds** (GPT-6.2 in ChatGPT, Ling-3.2-air): already mined.
- Nothing new to propose.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked URLs

`blocked_escalations` is empty. `phase_a_summary.blocked` lists 7 HF pages that returned HTTP 429 (streak 1): tencent/Hy4-flash, baidu/ERNIE-5.5-Flash-Base, baidu/ERNIE-Image, tencent/Hy4, inclusionAI/LingSante-3.1-flash, LingSante-3.1-air-VL and Ling-3.2-air. I re-fetched all seven and every one returned HTTP 200, so they are alive and the 429s were transient rate limiting. `not_found` is empty.

## Task 6: Document updates

- **Top 5, all already judged in earlier runs, not re-read**: v1304 (Hydrogen, U+200B noise), v1056, v773, v1170 (stale) and v924 (noise).
- **openai-gpt-6-2-astra-system-card v1321** (rank 6, the only new entry): **substantive**. It adds a Nov 22 change-log entry and P0/P0.5 definitions in the OAI-repo Sabotage v2 section; everything else is PDF reflow. Annotated (#4).

## Task 7: Friction logged

- `recurrence` (of 2026-11-18T06:28:28Z): the updated_docs top 5 is now entirely already-judged entries, and the only new substantive version sat at rank 6.

## Task 8: Proposals

None filed. The stale-queue problem is already covered by an existing PROPOSALS.md entry.
