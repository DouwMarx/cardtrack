# Run report — 2026-11-20T06:17Z-local

Last agent success: 2026-11-19T06:27Z. Search window: the 72 h minimum (since 2026-11-17). Today is a Friday, so no weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | https://huggingface.co/tencent/Hy4 — Hy4 model card (tencent_hunyuan, model_card, Hy4 + Hy4 base, 2026-11-20, open_weight_restrictive, has_safety_evals=false) | **written** → `tencent-hunyuan-hy4-model-card` (doc 488, v1250) |
| 2 | annotate_version | `google-deepmind-gemini-4-hydrogen-model-card` v1247 | **written** |

## Task 1: Phase A candidates (first_seen 2026-11-20)

- **tencent/Hy4** (and Hy4-FP8 / Hy4-base): this is Tencent Hy's new 770B-A49B flagship and the full successor to Hy4 preview. KuCoin, BigGo Finance and others covered the launch. Proposed and written as one family row (FP8 is a quantization, base is the pretrained checkpoint). The card links a **Hy4 System Card PDF** at https://hy.tencent.ai/Hy4_system_card.pdf. Today that URL returns only the hy.tencent.ai client-rendered HTML shell (6314 bytes), both through read_doc and WebFetch. Since I couldn't read it, I didn't propose it, and I logged friction. **A later run should re-check this URL**: news reports say a safety-assessment system card shipped with the model.
- **tencent/WeMM-Video-{2B,4B,9B,35BA3B} + FP8/AWQ/GGUF/NVFP4 quants**, plus the WeMM-Video paper: skipped. WeMM is WeChat's multimodal line, not the Hunyuan Hy line that the tencent_hunyuan scope note covers. It's a multi-size checkpoint drop with no outside announcement, and the earlier WeMM-Embedding row was removed.
- tencent/WeVisForensics (detector), nvidia Riva-Translate-4B (translation), C-RADIOv4-H-AV (vision backbone), parakeet-tdt (ASR): all auxiliary models, out of scope.
- muse.ai/blog/security-and-safety-for-ai-agents…: the same post is already cataloged at its research.meta.ai URL (`meta-muse-other`). Skipped as a mirror.
- Also skipped: HF papers (research), datasets, buckets, spaces, user profiles, discussion threads (new_version pointers, chat-template fixes), and inclusionAI *-singprobe repos (probes, not models).
- Older candidates (first_seen before today) were triaged by earlier runs.

## Task 2: Targeted web search

Queries: system cards 18–19 Nov; open-weight releases this week; trusted/restricted access programs; AISI/METR/Apollo reports; Anthropic LSVP/CVP; xAI, Z.ai, Qwen, Xiaomi, Mistral recency; Qwen4-Max docs; Tencent Hy4.
- Already cataloged: GPT-6.2 Astra/Sol card, Gemini 4 Neon/Carbon/Hydrogen, Genie 4, ChatGPT Images 2.6, Fable/Mythos 5.2, the Anthropic CVP expansion and LSVP pages, METR "Measuring alignment eval tells" (2026-11-16), Mistral Large 4 ("Le Chonk"), and Grok 4.7.
- **Qwen4-Max** (2026-11-16, API-only): skipped. Alibaba published no model card or tech report. The qwen.ai blog renders client-side (unreadable via read_doc and WebFetch). The readable alibabacloud.com post is a press release with leaderboard ranks and a generic "safety by design" paragraph, with no evaluation results. If open-weight Qwen4 models ship with HF cards, Phase A will see them.
- **OpenAI embedded assessments** (Apollo, METR, Transluce, Goodfire; 2026-11-16): skipped. It's a process/partnership announcement with no evaluated model named. Any assessor reports it produces will be candidates.
- Not allowlisted, so not proposed: Shanghai AI Lab Sage S2.1 Flash, SenseTime SenseNova Loop-9B, RadixArk DaisyRose-27B, Runway Praxis-1, Reson8 Rumble-2-Flash (ASR).
- Orgs silent for more than 14 days (Palisade, Poolside, SaferAI, Z.ai, RAND, CAISI, xAI, Qwen, Xiaomi, StepFun, DeepSeek, and others): spot searches found no new in-scope documents. Z.ai's latest is still GLM-5.3 (cataloged). Grok 5 isn't released. Xiaomi's latest is MiMo-V2.6 (cataloged).

## Task 3: Citation mining

GPT-6.2 Astra/Sol system card (added 2026-11-17): its external evaluations are by SecureBio, UK AISI (cyber safeguards, alignment, monitorability) and Irregular. All of them appear only as hub sub-pages of the cataloged card. SecureBio's resources page still lists only the GPT-6 Astra report, and I found no standalone UK AISI post on GPT-6.2. Nothing new to propose.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked-URL escalations

Phase A again got 403 on all 20 standing openai.com / help.openai.com URLs (16 at streak 30, 1 at 29, 3 at 8). It also got 403 on two new ones at streak 1: astra-for-law and astra-law-6-2. read_doc fetched path-to-astra, a-thousand-fewer-paths-to-root, astra-for-law, astra-law-6-2 and the Daybreak help article with HTTP 200 via browser_impersonation. **All alive; no status changes.** The HF 429s (Hy4-flash, ERNIE-5.5-Flash-Base, ERNIE-Image, streak 2) are rate limits; read_doc fetched HF pages normally today.

## Task 6: Document updates (top 5 of 20)

1. `fangcun-ai-deepseek-v4-1-flash-1017-independent-eval` v1056: **skipped, noise**. It's PDF figure-label reflow, plus a TOC page number changing from 85 to 84.
2. `deepseek-deepseek-v4-1-flash-model-card` v773: **skipped, noise**. HF widget furniture: auto-generated usage snippets switched to chat/completions, download/Spaces counts, and community leaderboard widgets.
3. `deepseek-deepseek-v4-1-flash-1017-model-card` v1170: **skipped, noise**. Same HF widget furniture as #2.
4. `anthropic-claude-mythos-preview-other-3` v924: **skipped**. The diff is newly extracted section headings, a dropped newsletter banner, and the 11-task description table no longer extracted. The prose is unchanged, so this looks like an extractor/layout change rather than a revision.
5. `google-deepmind-gemini-4-hydrogen-model-card` v1247: **annotated**. The Safety & Security Report moved from "coming soon" to published and linked.
   - That report is already cataloged (`google-deepmind-gemini-4-hydrogen-system-card`). Its `publication_date` is null, and the PDF gives only "November 2026", so I left it null rather than guess.

## Task 7: Friction logged

- `recurrence` (of 2026-11-19T06:26:54Z): Phase A 403s on openai.com while read_doc reads the same pages fine.
- `other`: the Hy4 System Card PDF link serves only the hy.tencent.ai SPA shell, so it's unreadable and has no watching index.

## Task 8: Proposals

None filed.
