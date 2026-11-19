# cardtrack agent run — 2026-11-19 (run id 2026-11-19T06:18Z-local)

- **Lookback:** last agent success 2026-11-18T06:29:09Z, so the 72 h minimum applied (2026-11-16 to 11-19).
- **Weekly retrospective sweep:** not due (Thursday).
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | add `google-deepmind-gemini-4-neon-model-card`: *Gemini 4 Neon — Model Card* (PDF, 2026-11-18; Phase A lead). Neon is a new mid-tier model adapted from Gemini 4 Carbon. The HTML card is recorded as web_version and the launch blog as announcement.<br>**Safety content:** content-safety deltas vs Hydrogen, plus an FSF Material Capability Change assessment (below threshold, so T/CCL determinations are carried forward from Argon: bio CCL and cyber CCL cannot be ruled out; LoC stealth TCL cannot be ruled out).<br>**Tags:** cbrn, cyber, loss_of_control. Closed. | **written** (doc 481) |
| 2 | add `google-deepmind-gemini-4-neon-other`: the Neon model-evaluation PDF (methodology and results; the evals-methodology URL redirects to it). Same pattern as the Argon, Carbon and Hydrogen `-other` rows. Capability benchmarks, including cyber and Gray Swan IPI; has_safety_evals false and no tags, consistent with the sibling rows. Closed. | **written** (doc 482) |
| 3 | add `google-deepmind-genie-4-model-card`: *Genie 4 — Model Card* (PDF, 2026-11-18; Phase A lead). Released alongside the Project Genie / Ultra availability post. Includes red-teaming and process description plus an inherited FSF assessment (unlikely to reach any T/CCL). has_safety_evals true, no tags. Closed: a paid Ultra tier is not vetting. Distinct from the existing `google-deepmind-genie-4-access-policy` row (10-27 research blog). | **written** (doc 483) |
| 4 | add `google-deepmind-gemini-4-neon-access-policy`: the *Introducing Gemini 4 Neon* blog (11-18). It names "Gemini 4 Neon for cyber", rolling out to trusted defenders via the Fairwind Program (request through the Cloud account team). This mirrors the Carbon access-policy precedent. The post reports misalignment-monitor, cheating, honesty, IPI and cyber results. Tags: cyber, loss_of_control. Restricted. | **written** (doc 484) |
| 5 | add `openai-astra-for-law-access-policy`: *Astra for Law leads in legal intelligence* (11-17; search lead). Updated Astra for Law (a GPT-6.2 Astra configuration). Trusted Access now expanded to all ChatGPT Enterprise customers and the API. Gating: business verification, a signed Legal Technology and Trust Addendum, and lawyers-only use (help article recorded as related). Capability results only. Restricted. | **written** (doc 485) |
| 6 | add `openai-astra-for-law-access-policy-2`: *Introducing Astra for Law* (2026-09-17). Backfill found while handling #5: the program launch post (Trusted Access for selected law firms). The pipeline never surfaced it, as Phase A cannot read openai.com. Restricted. | **written** (doc 487) |
| 7 | add `metr-claude-opus-5-5-independent-eval-2`: METR, *Measuring alignment eval tells* (11-16; search lead). Investigator agents in 19 alignment and 36 capability environments: Opus 5.5 ranks every alignment eval above every capability eval, and Astra recognises a simulated safety scenario. This is evaluation-awareness content of the kind found in system cards. Tag: loss_of_control. Closed.<br>**Caveat:** the note says only "Astra"; I recorded GPT-6 Astra (the 6.x line) and said so in the justification. | **written** (doc 486) |

## Phase A candidates (new today, first_seen 11-19)

- **Added:**
  - **Gemini 4 Neon model card and announcement:** #1, #2, #4.
  - **Genie 4 model card and availability post:** #3.
- **Neon Safety & Security Report:** announced as "coming soon". `gemini_4_neon_safety_report.pdf` returns 404 today. Watch for it, following the Argon/Carbon/Hydrogen pattern.
- **Skipped:**
  - **Anthropic "Claude solves two open problems in black-hole physics":** a capability showcase with no measured model results.
  - **Anthropic IPO pricing:** corporate news.
  - **NVIDIA Qwen3.8-27B-NVFP4-QAD and its discussion:** a quantization artifact, out of scope per NVIDIA's scope note.
  - **inclusionAI LingSante collection:** its only model, Ling-3.0-flash-Sante, is already catalogued.
  - **LingSante-MedGuard:** a dataset.
  - **Code World Model 2.0:** a paper.
  - **Tencent WeMM-Ecom collection:** empty.
  - **Tencent paper and profile links:** not documentation.
  - **MiniMax ecosystem space:** not documentation.
  - **Apollo Trust Center:** not documentation.
  - **Epoch data insights:** compute and inference-capacity charts, no named model.
  - **Thinking Machines status page:** not documentation.
- **Older candidates:** triaged in earlier runs.

## Targeted search (11-16 to 11-19)

- **OpenAI "Our first phase of embedded assessments":** skipped. Read via read_doc. It announces agreements with Apollo, METR, Transluce and Goodfire, but names no model and reports no results; this is consistent with the 11-17 skip of Apollo's pilot post. Watch for the resulting assessor reports.
- **Astra for Law:** see #5 and #6.
- **METR alignment-eval tells:** see #7.
- **Restricted-access programs:** nothing new beyond Neon for cyber/Fairwind (#4) and Astra for Law.
  - CVP/Glasswing tiers (Oct), LSVP, Rosalind (incl. the GPT-Rosalind-6 addendum) and Co-Scientist are already catalogued.
  - The ChatGPT for Academic Researchers expansion (applications open 11-23) is a GA grant program, skipped as before.
  - No news on Claude Science, Gemini for Science or Isomorphic.
- **Watch list:**
  - **Grok 4.8:** still no card (search confirms none as of 11-16).
  - **Qwen4-Max:** no new primary documentation.
  - **Neon Safety & Security Report:** pending.
  - **Embedded-assessment reports:** pending.

## Citation mining

- **Neon model card:** points to the evals-methodology page (added as #2) and to the Argon/Carbon Safety & Security reports, which are already catalogued.
- **Neon blog:** cites Vals, Artificial Analysis, Surge, Zapier, Andon Labs and Gray Swan results. These are leaderboards, not standalone reports.
- **Genie 4 post:** links a "model research overview", which is the 10-27 blog already catalogued.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 20 openai.com / help.openai.com URLs (16 at streak 30, 1 at 28, 3 at 7).
- **My own fetches:** today read_doc got HTTP 200 via browser_impersonation on all four I sampled: hugging-face incident, the Daybreak help article, wet-lab-science and introducing-gpt-rosalind. The new Astra for Law, embedded-assessments and help pages also fetched fine.
- **Verdict:** all are alive. No status changes.
- **Three HF 429s** (Hy4-flash, ERNIE-5.5-Flash-Base, ERNIE-Image; streak 1): transient rate limiting, no action.

## Document updates (task 6)

- **Top 5:** v1056, v773, v1170, v924 and v1015 again. All were judged in earlier runs as noise or already handled. Skipped.
- **New entry `dots-studio-dots3-note-preview-model-card` v1238:** noise. It is a multimodal quickstart snippet, reordered eval-result badges and a download counter. Skipped, no annotation.

## Friction and proposals

- **Friction:** 2 recurrence entries.
  1. OpenAI 403s in Phase A while read_doc's impersonation works. Two OpenAI documents were found only by search.
  2. Stale updated_docs head.
- **PROPOSALS.md:** no new entry.
  - The missed Astra for Law posts are further evidence for the existing 2026-10-07 entry (Phase A vs impersonation fetcher) and the 2026-11-12 entry (watch openai.com/news/rss.xml).
  - The stale queue is covered by the existing 2026-10-28 entry.
