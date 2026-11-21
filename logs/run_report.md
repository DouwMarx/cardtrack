# Run report — 2026-11-21T06:19Z-local

Last agent success: 2026-11-20T06:27Z. Search window: the 72 h minimum (since 2026-11-18). Today is a Saturday, so no weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | https://thinkingmachines.ai/model-card/inkling-2-mini/ — Inkling 2 Mini Model Card (thinking_machines, model_card, 2026-11-20, open_weight_permissive / Apache 2.0, has_safety_evals=true, risk_domains cbrn/cyber/loss_of_control/societal_harm) | **written** → `thinking-machines-inkling-2-mini-model-card` (doc 489, v1264) |
| 2 | add | https://metr.org/blog/2026-11-20-q4-2026-capability-update/ — METR Q4 2026 capability update (metr, independent_eval, 2026-11-20, closed, has_safety_evals=true, loss_of_control) | **written** → `metr-claude-opus-5-5-independent-eval-3` (doc 490, v1265) |

## Task 1: Phase A candidates (first_seen 2026-11-21)

- **Inkling 2 Mini** (thinkingmachines.ai/news/inkling-2-mini/): this is a new open-weight looped MoE (26.4B total / 3.4B active, Apache 2.0) released 2026-11-20.
  - I proposed the dedicated model card as canonical. The news post (announcement) and the HF weights go in related_urls.
  - The card has a Safety and Alignment table (FORTRESS, StrongREJECT, internal misbehavior/covert/destructive, HoneyBench) and a safety section on CBRN/cyber uplift (with refusal-suppressed variants), loss-of-control (sabotage, deception), self-harm and sycophancy, plus CoT-monitorability tests. The tags follow the Inkling 2 Small row's precedent.
  - The research variant TML-d24-varloop-research is noted in `notes`, not proposed separately.
  - Press coverage exists (letsdatascience).
- **METR "AI R&D-relevant model capabilities are improving rapidly…"** (2026-11-20): this passes the system-card test. It gives per-model time-horizon estimates on TH1.1/TH2/MirrorCode (GPT-6 Astra ~40 h, Opus 5.5 ~39 h), human-percentile placements, reward-hack checks, and developer-specific trend analysis. It sits alongside the cataloged TH1.1 post. Proposed and written.
  - The validator generated the slug `metr-claude-opus-5-5-independent-eval-3` from the first model name. It is functional, but it doesn't describe the document well.
- inclusionAI/LingSante-Pulse-1.0: skipped. It is a physiological-signal (ECG) encoder, an auxiliary model.
- Anthropic IPO-close post: corporate news, skipped.
- nvidia Nemotron-3.5-Transcribe GGUF: ASR quant, skipped.
- Qwen2-VL-2B / Qwen2-1.5B: old pre-floor models, only metadata updated; skipped. Qwen/MiniMax discussion threads (new_version pointers, README fixes): skipped.
- HF papers, user profiles, and simready dataset discussions: skipped.
- Older candidates were triaged by earlier runs.

## Task 2: Targeted web search

Queries: "system card November 2026"; open-weight model cards around 20 Nov; trusted-access programs Nov 2026; AISI evaluation reports; Anthropic new model/system card; OpenAI GPT-6.2 addendum; Anthropic LSVP expansion; Apollo/Palisade/Epoch evals; Gemini/Grok/Mistral/DeepSeek/Kimi releases around 19 Nov; Hy4 system card.

- Already cataloged: GPT-6.2 Astra/Sol card (OpenAI revised its AI self-improvement wording on 11-17, which is for the version monitor), Fable/Mythos 5.2, Gemini 4 Neon/Carbon/Hydrogen, GPT-6 Cyber, Rosalind programs, accelerating-cyber-defense-ecosystem, the AISI unsanctioned-agent incident report, and the Anthropic LSVP pages. The LSVP search found no new expansion page.
- **OpenAI "Broadening access to AI for scientists"** (ChatGPT for Academic Researchers expansion): skipped. It grants free ChatGPT Plus to researchers. That is a general product, not a gated model, and GPT-Rosalind is only mentioned in passing (its access pages are cataloged).
- **Reflection AI** trusted access for "Laser" (Axios 11-17): skipped. Reflection is not allowlisted, and Laser is a pentest tool rather than a named model.
- **Hy4 System Card**: re-checked. hy.tencent.ai/Hy4_system_card.pdf still serves only the SPA shell. The HF repo file list and the Tencent-Hunyuan/Hy4 GitHub repo contain no PDF, and press articles don't link an alternate copy. **Still unreadable, so not proposed.** A later run should keep checking.

## Task 3: Citation mining

- The Inkling 2 Mini post cites Goodfire's early interpretability write-up on looped models. Goodfire is not allowlisted, and I found no link target in the page.
- The METR Q4 post cites the Anthropic AI R&D acceleration assessment and the Gemini 4 Argon Safety & Security Report. Both are already cataloged.
- Nothing new to propose.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked-URL escalations

- `tencent-hunyuan-hy4-flash-model-card` (https://huggingface.co/tencent/Hy4-flash, 429, streak 3): read_doc got HTTP 200 with full card content. **Alive.** It was an HF rate limit; no status change.
- The standing openai.com 403 escalations are absent from today's phase_a_summary (no blocked entries other than Hy4-flash), so Phase A apparently read openai.com fine this run.

## Task 6: Document updates

The top 5 (v1056, v773, v1170, v924, v1015) were all judged noise by previous runs and are unchanged, so I didn't re-read the first four. I read ranks 5–9 instead:

1. `anthropic-claude-mythos-preview-other` v1015: **skipped, noise**. Section headings newly extracted, footnote markers changed from [1] to 1, and the newsletter banner dropped.
2. `deepseek-deepseek-v4-pro-model-card` v573: **skipped, noise**. HF usage-snippet swap (chat/completions to completions), download counter, and eval-widget reordering.
3. `deepseek-deepseek-v4-flash-0731-model-card` v578: **skipped, noise**. Same HF snippet furniture.
4. `anthropic-glm-5-2-other` v974: **skipped, noise**. Headings newly extracted, the newsletter banner dropped, and one small table no longer extracted. The prose is unchanged.
5. `dots-studio-dots3-note-preview-model-card` v1238: **skipped, noise**. HF snippet expansion (processor and image example), download counter, and eval-widget reordering.

## Task 7: Friction logged

- `recurrence` (of 2026-11-19T06:26:55Z): the stale already-judged entries still fill the updated_docs top 5. The dismissal path is already proposed in PROPOSALS.md (2026-10-28).
- `recurrence` (of 2026-11-20T06:24:20Z): the Hy4 System Card PDF is still unreadable (SPA shell), and there is no alternate copy.

## Task 8: Proposals

None filed. The stale-queue problem is already covered by the 2026-10-28 proposal.
