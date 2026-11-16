# cardtrack agent run — 2026-11-16 (run id 2026-11-16T06:18Z-local)

- **Lookback:** last agent success 2026-11-15T06:25:02Z, so the 72 h minimum applied (2026-11-12 to 11-16).
- **Weekly retrospective sweep:** done (Monday). Palisade and poolside were swept on 11-02, and Transluce, SaferAI and US CAISI on 11-09, so today covered the next-oldest orgs: **RAND** (newest 08-11), **Dots Studio** (08-14) and **Z.ai** (08-28). typesafe has zero rows but was settled as out of scope on 10-05.
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | add `nvidia-nemotron-labs-audio-visual-flamingo-model-card`: NVIDIA Nemotron-Labs-Audio-Visual Flamingo (AVF-Instruct) HF card (Phase A lead, first_seen 11-16). It is an audio-visual LLM with a Qwen2.5-7B backbone and text output, so it is a covered omni/VLM class. Notability: the NVIDIA/UMD tech report arXiv 2607.16107. No safety evals; open_weight_restrictive (NVIDIA OneWay Noncommercial). The repo was created privately on 04-15 and first went public around 11-15 (HF lastModified), so publication_date is 2026-11-15; the reasoning is in the notes. | **written** (doc 468) |
| 2 | add `rand-gpt-oss-120b-independent-eval`: RAND CAST RR-A5112-1, *Open-Weight AI Models May Increase Biological Misuse Risks* (PDF, published 2026-09-14). It is a bio-misuse eval of GPT-OSS-120B, Qwen3.5-397B, Qwen3-235B, DeepSeek-V3.1 and Kimi K2.5 under anti-refusal SFT, RL capability enhancement and abliteration, against Gemini 3.1 Pro and GPT-5.4 baselines, using the SecureBio suite and an influenza pathway eval. Tagged cbrn; openness closed (most restricted named model is public-API). **Recovered lead:** lost on 09-15 to agent-side 403s (friction 09-15/09-25/09-26, PROPOSALS 09-15); read_doc fetched the full PDF today. | **written** (doc 469) |
| 3 | field_update `related_urls` on `thinking-machines-inkling-2-small-model-card`: added the official HF weights repo (`weights`) and kept the news page (`announcement`). The HF page carries the same card text as the catalogued thinkingmachines.ai card, which already states open weights / Apache 2.0, so an add would be a mirror. | **written** |

## Phase A candidates (new today, first_seen 11-16)

- **nvidia/nemotron-labs-audio-visual-flamingo-hf:** added (#1).
- **Skipped:** the nilayc and cfahlgren1 profile pages, and the nvidia/USDCraft-10K dataset discussion. None is documentation.
- **Older candidates:** triaged in earlier runs.

## Targeted search (11-12 to 11-16)

- **Inkling 2 Small HF card:** handled as #3.
- **DeepSeek news261113 (11-13):** API features (web search, file input, URL reading, ASR/TTS, safety checks) for the existing V4.1-Flash. No new model and no card.
- **OpenAI Daybreak Red Team / Defense Factory (11-12):** read both, plus the Daybreak hub, with read_doc. They are product pages that name no model, so they fail the access_policy named-model gate. Daybreak is already covered by three access-policy rows. Skipped.
- **Ling 3.2 Flash (inclusionAI, on OpenRouter 11-13):** no card; the HF repo returns 401.
- **Restricted-access programs** (Rosalind, Glasswing/Mythos, LSVP, CVP, Claude Science, Gemini for Science/Co-Scientist, Flash Cyber/CodeMender, Isomorphic bioresilience): nothing new in the window.
- **Watch:**
  - **Gemini 4 Hydrogen S&S report:** still "coming days".
  - **Grok 4.8:** no card.
  - **Qwen4-Max-Preview:** no card; retires 11-25.
  - **Tencent Hy4:** repo still 401.
  - **Muse Spark 1.4:** leak only.

## Weekly retrospective sweep

- **RAND:** read both CAST index pages. Added RR-A5112-1 (#2). Everything else since August is policy or commentary with no named-model eval: AIxBio workshop, recursive self-improvement, mirror life, life-science framework, SL3 weight security, Select Agent volumes, data-center siting, DOE RFI.
- **Z.ai:**
  - Nothing newer than GLM-5.3 / 5.3-Flash, which are both catalogued.
  - GLM-5.3 FlashX / FlashX-Legal (11-02) are pricing/speed tiers.
  - GLM-5-Turbo (about 2026-03-15) was skipped. Its only primary doc is an undated docs.z.ai API page with one vendor benchmark (ZClawBench) and no method or safety content, so it is a product launch without documentation; this is consistent with the 09-25 Upstage decision. A future GLM-5-Turbo tech report or HF card would qualify.
- **Dots Studio:** the HF org has only dots3-note-prev (catalogued), its fp8 copy, and the dots.tts / dots.mocr models (TTS and OCR, so auxiliary). The dots3 tech report is not out yet.

## Citation mining

The AVF card cites OmniVinci, Audio Flamingo 3/Next, AF-Whisper and Qwen2.5. These are pre-floor or already catalogued (AF-Next). The RAND report's model subjects are labs' own releases, not third-party evals. Nothing to propose.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 20 openai.com / help.openai.com URLs (16 at streak 30, 1 at 25, 3 at streak 4).
- **My own fetches:** read_doc fetched introducing-gpt-rosalind, path-to-astra, low-resource-programming-languages and hugging-face-model-evaluation-security-incident with HTTP 200 via browser_impersonation. Yesterday's run fetched the streak-4 group the same way.
- **Verdict:** alive and bot-blocked; no status changes.

## Document updates (task 6)

Top 5 in order:
- **v1056** (FangCun eval): already judged in earlier runs. Skipped.
- **v773** (DeepSeek-V4.1-Flash HF card): already judged in earlier runs. Skipped.
- **v1170** (DeepSeek-V4.1-Flash-1017 HF card): already judged furniture. Skipped.
- **v924** (Mythos Preview other-3): already judged in earlier runs. Skipped.
- **v1015** (Mythos Preview red-team post): re-read today. It is extraction noise: section headings were restored ("Our scaffold", "Finding zero-day vulnerabilities", ...) and footnote markers changed, with no content change. Skipped.

No new versions entered the queue today.

## Friction and proposals

- **Friction:** 2 recurrence entries.
  1. The OpenAI Phase A 403s, with read_doc working.
  2. The stale updated_docs head.
- **PROPOSALS.md:** no new entry. The stale-queue issue is already filed (2026-10-28). The RAND recovery shows that point 1 of the 2026-09-15 proposal (an agent read path) is now in place via read_doc.
