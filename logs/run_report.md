# cardtrack agent run — 2026-11-18 (run id 2026-11-18T06:19Z-local)

- **Lookback:** last agent success 2026-11-17T06:29:07Z, so the 72 h minimum applied (2026-11-15 to 11-18).
- **Weekly retrospective sweep:** not due (Wednesday). However, Baidu joined `sources.generated.yaml` today (origin openrouter) with zero rows, so I ran a scope-floor backfill for Baidu (see below).
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.
- **Process slip:** I ran one read-only `git log -- logs/run_report.md` early in the run to see recent report history. Nothing was modified, but this breaks the no-git rule and will not recur.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | add `openai-gpt-6-2-astra-system-card`: *GPT-6.2 Astra and Sol System Card* (PDF, 2026-11-17; Phase A lead). The HTML hub page is recorded as web_version and the openai.com announcement as related.<br>**Ratings:** both models Critical for cyber and High for bio/chem; Astra is OpenAI's first external model at High for AI self-improvement.<br>**External evals:** SecureBio, UK AISI (including a universal cyber jailbreak), Irregular, Epoch and Vals.<br>**Alignment and safety content:** evaluation awareness, CoT-monitorability regressions, blocker deception, and under-18 and mental-health benchmarks.<br>**Tags:** cbrn, cyber, loss_of_control, societal_harm. "Avoiding deceptive interactions with users" is agent misreporting, so it is tagged loss_of_control, not harmful_manipulation.<br>**Openness:** closed. Both models are on the public API; only the reduced-refusal cyber config is gated to Daybreak Red. | **written** (doc 473) |
| 2 | add `epoch-ai-claude-fable-5-2-independent-eval`: Epoch, *How good are Fable 5.2 and GPT-6.2 Astra at real work?* (11-17). Hand-graded Epoch Automation Reports results for six named models: Fable 5.2 scored 97.5% on data-center analysis, and GPT-6.2 Astra averaged 65%, 17 points below Fable 5.2. Capability only: has_safety_evals false, no tags, closed. | **written** (doc 474) |
| 3 | add `tencent-hunyuan-hy4-flash-model-card`: Tencent Hy4 flash (220B / ~12B active VLM, 1M context; 11-17). One family row covering flash and flash-base, with FP8 recorded as weights. Notability: PR Newswire release plus press. Tencent Hy License 1.0 (Apache-derived with MaaS commercial terms), so open_weight_restrictive. No safety evals. | **written** (doc 475) |
| 4 | add `baidu-ernie-5-5-flash-base-model-card`: HF card for ERNIE-5.5-Flash-Base (280B-A14B base, 11-05). The ernie.baidu.com tech blog is the announcement and the BF16 repo is recorded as weights. The license excludes the EU, UK and South Korea, so open_weight_restrictive. No safety evals. | **written** (doc 476) |
| 5 | add `baidu-ernie-5-5-flash-preview-model-card`: release post for ERNIE 5.5 Flash Preview (11-11), the post-trained model. API-only on Qianfan, so closed; Apache weights are promised. This is thin documentation: its benchmark numbers appear only in an image chart. Admitted under admit-and-flag because it is the model's only primary documentation. | **written** (doc 477) |
| 6 | add `baidu-ernie-5-0-other`: *ERNIE 5.0 Technical Report* (arXiv 2602.04705, 2026-02-04). Backfill. Unified multimodal model at trillion-parameter scale. A keyword scan found no safety content. Closed. | **written** (doc 478) |
| 7 | add `baidu-ernie-5-1-model-card`: ERNIE 5.1 official release post (2026-05-09). Backfill. Benchmarks plus elastic-subnetwork training details; no tech paper exists. Closed, no safety evals. | **written** (doc 479) |
| 8 | add `baidu-ernie-image-model-card`: ERNIE-Image HF card (8B DiT text-to-image, 2026-04-15). Backfill. Covers ERNIE-Image and ERNIE-Image-Turbo; Apache-2.0, so open_weight_permissive. No safety evals. | **written** (doc 480) |

## Phase A candidates (new today, first_seen 11-18)

- **Added:**
  - **GPT-6.2 system card:** #1.
  - **Epoch real-work post:** #2.
  - **Tencent Hy4-flash:** #3. Its FP8 and base repos and the collection links are covered by that one row.
  - **Baidu ERNIE-5.5-Flash-Base and BF16 repo:** #4.
- **Baidu HF org page:** this is Baidu's first index pass, so roughly 90 links were surfaced.
  - **Added:** ERNIE-Image (#8).
  - **Skipped as auxiliary OCR:** Unlimited-OCR / Unlimited-OCR-2, Qianfan-OCR.
  - **Skipped as pre-floor 2025 releases:** Qianfan-VL-8B/70B, ERNIE-4.5-VL-28B-A3B-PT, ernie4.5 blog.
  - **Skipped as not documentation:** profiles, spaces, papers, GitHub/X/nav links, blog listings, ERIA-1K dataset, ERNIE-Image-Aes.
  - **Left for a later run (not judged today):** NAVA, an audio-video generator from about June 2026, with a paused Space.
- **Apollo "pilot towards embedded evaluations":** skipped. It was already judged on 11-17 (no model, no results).
- **Skipped as other non-documentation:**
  - RAND mirror-life guide and electrical-equipment brief: no model.
  - Redwood "defining capabilities activities": an essay.
  - xAI Grok Bot accounting: product.
- **Skipped as distillation/quant artifacts per NVIDIA scope:** NVIDIA draft models (Llama-3.2-1B / Qwen3.5-0.8B / Qwen3.5-4B Qwen3.8-27B drafts) and Qwen3.8-Flash-Next-NVFP4-QAD.
- **Skipped as not documentation:** inclusionAI invoker-render-1.0 and the SingVL discussion (no announcement evidence; HF repos only), HF profiles, and discussions.
- **Older candidates:** triaged in earlier runs.

## Targeted search (11-15 to 11-18)

- **GPT-6.2 external evals:** none published separately yet. securebio.org/resources/gpt-6-2-astra-assessment.pdf returns 404; the SecureBio, UK AISI, Irregular and Apollo results appear only inside the system card for now.
- **NVIDIA "Nemotron for Science" (SC26, 11-16):** skipped. It is an open toolkit (Nemotron 3.5 Super VL, LitmusBench v0.2 dataset, RL recipes). The model's card and tech report are already catalogued, and the toolkit has no gating, so it is not an access policy.
- **Restricted-access programs:** nothing new in the window.
  - Daybreak changes for GPT-6.2 are documented in the system card (§2.2.8).
  - CVP's three-tier expansion (Oct) and LSVP are already catalogued.
  - Rosalind's next grant round opens 11-23; this is a GA academic-grant program and was skipped earlier.
  - No news on Claude Science, Gemini for Science, Flash Cyber/CodeMender or Isomorphic.
- **Watch list:**
  - **Grok 4.8:** still no card.
  - **Qwen4-Max:** no card or tech report; qwen.ai is still unfetchable.
  - **Tencent flagship Hy4:** open weights to follow.
  - **ERNIE 5.5 Flash Preview:** Apache weights and HF card to come.
  - **SecureBio GPT-6.2 Astra:** pre-release report.
  - **Apollo/OpenAI:** first embedded-evaluation report.

## Citation mining

- **GPT-6.2 card:** cites SecureBio, UK AISI, Irregular, Epoch, Vals, Apollo and Gray Swan. Epoch's real-work piece is now added (#2). No other standalone report exists yet.
- **Epoch post:** cites Kezins et al. 2026 (a paper, out of scope).
- **Hy4 flash / ERNIE:** no third-party evals cited.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 20 openai.com / help.openai.com URLs (16 at streak 30, 1 at 27, 3 at streak 6).
- **My own fetches:** today read_doc also got 403 on all four I sampled: hugging-face incident, introducing-gpt-rosalind, securing-frontier-training-environment and the Daybreak help article. It also got 403 on the GPT-6.2 announcement.
- **Verdict:** today's web searches still return these pages (e.g. the Daybreak help article and the Rosalind Academic Plan), so they are bot-blocked, not gone. No status changes.

## Document updates (task 6)

The top 5 are v1056, v773, v1170, v924 and v1015 again. All were judged in earlier runs as noise or already handled. Skipped. The queue has no new entries.

## Friction and proposals

- **Friction:** 2 recurrence entries.
  1. OpenAI 403s; read_doc is also blocked today.
  2. Stale updated_docs head.
- **PROPOSALS.md:** no new entry.
  - Today's Baidu backfill is further evidence for the existing 2026-10-03 proposal: overlay publishers join with no backfill.
  - The stale-queue issue is covered by the existing 2026-10-28 proposal.
