# Run report — 2026-11-24T06:20Z-local

Last agent success: 2026-11-23T06:28Z. Search window: the 72 h minimum (since 2026-11-21). Today is a Tuesday, so there was no weekly retrospective sweep (it ran yesterday).

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | `openai-gpt-6-2-november-23-system-card`: https://deploymentsafety.openai.com/gpt-6-2-chatgpt/gpt-6-2-chatgpt.pdf (GPT-6.2 in ChatGPT System Card, 2026-11-23; closed; cbrn, cyber, loss_of_control, societal_harm) | **written** (doc 493, v1314) |
| 2 | add | `inclusion-ai-ling-3-2-air-model-card`: https://huggingface.co/inclusionAI/Ling-3.2-air (124B/5.5B-active multimodal MoE, MIT, has_safety_evals false) | **written** (doc 494, v1315) |
| 3 | annotate_version | `openai-gpt-live-1-1-system-card` v1307: change log, GPT-Live-1.1 API added, new API result columns | **written** |
| 4 | field_update | `openai-gpt-live-1-1-system-card` model_names += "GPT-Live-1.1 API" | **written** |

Notes on #1 and #2:
- **#1**: the HTML page (deploymentsafety.openai.com/gpt-6-2-chatgpt) extracts to only 1480 chars (one section), so I read the full 62k-char PDF. It is the canonical `url`, with the HTML page recorded as `web_version` and the ChatGPT release notes as `announcement`.
  - The card is for a separate chat-tab checkpoint, "GPT-6.2 (November 23)". It reports its own Preparedness tables: Critical for cyber, High for bio/chem, High for AI self-improvement.
  - It refers to the existing `openai-gpt-6-2-astra-system-card` for methodology, so I cross-referenced that row in notes.
  - Coverage: MacRumors, iClarified and thetechhacker.
- **#2**: repo created 2026-11-23 (HF API), license MIT. Covered outside the repo by Artificial Analysis, runtimewire, aiweekly and OrcaRouter.

## Task 1: Phase A candidates (first_seen 2026-11-24)

- **deploymentsafety.openai.com/gpt-6-2-chatgpt**: proposed (#1).
- **inclusionAI/Ling-3.2-air** (and the ling-32 collection): proposed (#2). The collection is recorded as a related URL.
- **LingSante-3.1-air-VL-MXFP4**: skipped. It is a quantization of the existing `inclusion-ai-lingsante-3-1-air-vl-model-card`.
- **Anthropic "Working with AI"** (2026-11-23): skipped. It is an interview-based study of enterprise AI adoption and evaluates no named model.
- **DeepMind "Finding faster quantum algorithms with agents and formal verification"**: skipped. It is a capability showcase of Gemini 4 agent teams with no model evaluation results that would pass the system-card test.
- **UK AISI "Attack policy selection can make monitor evaluations misleading"**: skipped. It is methodology research that uses Qwen 3.8 27B and GPT-5.4 as subjects; it does not evaluate them.
- **Apollo Research /science/ links** (15): skipped. These are old Apollo posts (2023 to 2025: linear probes, scheming demo, evals gap, science of evals and similar) that the index surfaced again after a site restructure. All predate the 2026-01-01 floor or are essays.
- **Tencent Hy-MT3 family** (1.8B/7B/30B-A3B plus FP8/GGUF): skipped. These are machine-translation models, which the tencent_hunyuan scope excludes.
- **Tencent WeMM-Ecom family** (0.8B to 35B-A3B plus quants) and OmniEVIE-4B: skipped. They are WeChat e-commerce VLM and feature-extraction models outside the Hunyuan line; same reasoning as WePocketModel yesterday.
- **Tencent HF paper 2611.30581** (pipeline-parallel system): research, skipped.
- **baidu/ERNIE-5.5-Flash-Preview, -FP8, -BF16** and the collection: the base card is already `baidu-ernie-5-5-flash-preview-model-card`; the others are precision variants. Skipped.
- **nvidia/MiMo-V2.6-Flash-RL-NVFP4**: skipped. It is an NVIDIA quantized re-host of Xiaomi's model.
- **NVIDIA CodonFM collection and repos**: skipped. They are codon-level RNA encoders (auxiliary, from Oct 2025, before the floor).
- **MiniMax H3 discussions, HF user profiles, baidu/README Space**: furniture, skipped.
- Older carried-over candidates (first_seen 11-11 to 11-23) were triaged in earlier runs and not revisited.

## Task 2: Targeted web search

Queries:
- GPT-6.2 ChatGPT release notes
- Ling-3.2-air release
- system/model cards Nov 2026
- trusted access programs Nov 2026
- LSVP / Cyber Verification Program / Mythos
- METR/Apollo/UK AISI evals of GPT-6.2 / Fable 5.2 / Gemini 4
- releases Nov 22–23
- DeepSeek Nov 2026
- xAI Grok model card
- Qwen/GLM/MiMo Nov 21
- Kimi K3.1 Pro Prime

Results:
- **Already cataloged**: GPT-6.2 Astra/Sol, Inkling 2 Mini, Gemini 4 Carbon/Hydrogen/Neon, LSVP and CVP pages, Fairwind, GPT-Rosalind pages, METR's 2026-11-05 Anthropic AI R&D acceleration posts, Kimi K3.1 Pro (plus FAR.AI and SecureBio evals), and Grok 4.7 (xai and cursor rows).
- **OpenAI "Broad access through consistent standards"** (2026-10-21): skipped. It is a usage-policy and provider-review update that assigns no access conditions to a named model.
- **OpenAI "Expanding ChatGPT for academic researchers"** (2026-11-16): skipped. The application gate grants ChatGPT Plus (a paid tier) and names no model or family.
- **Kimi K3.1 Pro Prime**: skipped. It is a faster serving lane on the same weights as K3.1 Pro, so not a distinct release.
- **"DeepSeek V4.1 Flash 1017 Uncensored (HeimdaLLM)"**: skipped. It is a third-party derivative, not a DeepSeek release.
- **No new releases** with documentation from DeepSeek, xAI, Qwen, Z.ai or Xiaomi in the window. Qwen4-Max still has no model card.

## Task 3: Citation mining

- **GPT-6.2 in ChatGPT card**: cites the GPT-6.2 System Card (in the DB), the Preparedness and Frontier Governance frameworks (policies, not model docs), and HealthBench/MentalHealthBench (benchmark papers).
- **Ling-3.2-air**: cites Ling-3.0-flash-VL, which is in the DB.
- **Yesterday's LingSante adds**: already mined.
- Nothing new to propose.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked-URL escalations

`blocked_escalations` is empty, and `phase_a_summary.blocked` and `not_found` are both empty. Nothing to check.

## Task 6: Document updates

I took the top five in order, plus the one other new entry:
- **google-deepmind-gemini-4-hydrogen-system-card v1304** (3795 substantive lines): **noise**.
  - The previous PDF extraction interleaved U+200B zero-width spaces, and this one drops them. The diff is truncated at 245 lines.
  - I compared the two stored texts in data/text: the TOC, the executive summary figures (CWE-bench v2 68.1%, ExploitBench 84.6%), the CCL table rows and the 200,312-trajectory monitoring table are identical, at line offsets shifted by about 5.
  - This was a sampled check, not a full diff (see friction).
  - Separately, the row's publication_date is null; the report says only "November 2026", so I left it.
- **fangcun-ai-deepseek-v4-1-flash-1017-independent-eval v1056**: already judged stale, not re-read.
- **openai-gpt-live-1-1-system-card v1307**: **substantive**. Annotated (#3) and model_names updated (#4).
- **deepseek-deepseek-v4-1-flash-model-card v773** and **deepseek-deepseek-v4-1-flash-1017-model-card v1170**: already judged stale, not re-read.
- **apollo-research-glm-5-3-independent-eval v1309** (new, outside the top five): **noise**. Only the "More papers" sidebar teasers rotated, plus a sidebar retitle ("Training-Run Evaluations" became "Training-Run Assessments").

## Task 7: Friction logged

- `recurrence` (of 2026-11-18T06:28:28Z): already-judged stale entries still occupy the updated_docs top 5.
- `recurrence` (of 2026-11-12T06:27:23Z): invisible-character-only changes (here, dropped U+200B in the Hydrogen PDF) are still scored as substantive. This one topped the queue at 3795 lines.
- `tooling`: the Bash guard blocks process substitution and scratch Python scripts, so I couldn't run a normalized full-text comparison of two stored versions. The friction entry suggests a read-only compare helper.

## Task 8: Proposals

None filed. The stale queue and the noise classification are covered by existing PROPOSALS.md entries, and the compare-helper idea is logged as friction for now.

A workaround note, not friction: deploymentsafety.openai.com HTML pages extract only a fragment. The `/<slug>/<slug>.pdf` path pattern gives the full card, as it did for GPT-6.2 Astra/Sol.
