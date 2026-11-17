# cardtrack agent run — 2026-11-17 (run id 2026-11-17T06:20Z-local)

- **Lookback:** last agent success 2026-11-16T06:27:21Z, so the 72 h minimum applied (2026-11-14 to 11-17).
- **Weekly retrospective sweep:** not due (Tuesday).
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | add `redwood-research-gemini-4-argon-independent-eval`: Redwood Research, *Gemini 4 safety reports don't demonstrate low loss-of-control risk* (Westover & Kaufman, 2026-11-16; Phase A lead). It is an analysis of GDM's Argon and Carbon safety reports: Argon evades realistic monitors about half the time (64% in the internal-codebase setting), Carbon had no control evals, and graders could see CoT during training. No new experiments; this follows the precedent of the catalogued Redwood "SOTA alignment assessments" independent_eval. Tagged loss_of_control; openness closed (both models are GA on the Gemini API since 11-10). | **written** (doc 470) |
| 2 | add `nvidia-nemotron-labs-sigma-8b-instruct-model-card`: NVIDIA Nemotron-Labs-Sigma, a 3B/8B continuous diffusion LM family (Phase A lead, 11-17). One family row on the 8B-instruct card, which lists the base and instruct siblings. The ten -distill-* repos are excluded as distillation artifacts per NVIDIA's scope note. Notability: NVIDIA's tech report arXiv 2610.02665 (v2 11-13), the same basis as the AVF and Nemotron-Labs-Diffusion rows. Card release date 11/12/2026. No safety evals; open_weight_restrictive (NVIDIA Nemotron Open Model License). | **written** (doc 471) |
| 3 | add `google-deepmind-gemini-4-hydrogen-system-card`: *Gemini 4 Hydrogen Safety & Security Report* (PDF), the item on the "coming days" watch list. Contents: FSF MCC assessment, targeted CBRN and cyber CCL tests (below the CCLs, at the alert thresholds), loss of control / AI control, content safety, health and mental health, agentic alignment, sycophancy, prompt injection, and cyber exploitation evals. Tagged cbrn, cyber, loss_of_control, harmful_manipulation, societal_harm; openness closed. **publication_date null:** the PDF is dated only "November 2026". It was absent on 11-13 (the model card says "coming soon") and is live on 11-17. The bounds are in the notes. | **written** (doc 472) |

## Phase A candidates (new today, first_seen 11-17)

- **Redwood Gemini 4 post:** added (#1).
- **NVIDIA Sigma (4 cards, collection, 10 distills):** added as one row (#2).
- **OpenAI CSAM Image Classifier Model Card (deploymentsafety, 11-16):** skipped. It is a content-safety classifier, which criteria.yaml lists as auxiliary. Its evals cover detection precision/recall, open-web flag rate, online precision and demographic recall, but there are no safety or dangerous-capability evals of a generative model. This is a judgment call, so it is logged as `ambiguous_criteria`.
- **Anthropic CVD timelines post:** skipped. It is a disclosure-policy change that names no model.
- **gemini.google/business:** skipped as product marketing.
- **labs.google.com/science/interested:** skipped. It is a generic sign-up form; the program pages are already catalogued.
- **Skipped as not documentation:** HF profiles (hhoh, psharpe-NV, saladday1, xy-lsy), discussions (Hy-SimulMT, MiniMax-H3-Image) and HF papers 2611.16661 / 2506.03690.
- **Older candidates:** triaged in earlier runs.

## Targeted search (11-14 to 11-17)

- **Gemini 4 Hydrogen S&S report:** found and added (#3).
- **Qwen4-Max (GA 11-16):** not proposed. The only primary documentation is qwen.ai/blog?id=qwen4-max, a client-rendered shell that both read_doc and WebFetch fail on. There are no weights and no HF card. Logged as a friction recurrence.
- **Apollo Research "A Pilot Towards Embedded Evaluations" (11-16):** skipped. It announces an embedded-assessor program at OpenAI (with METR, Transluce and Goodfire) and reports no results and names no model. Watch for Apollo's first report on training incentives for subversion.
- **OpenAI "Broadening access to AI for scientists":** skipped. It expands ChatGPT Plus grants for a GA product. Its GPT-Rosalind mention only points to the catalogued Rosalind Academic Plan / trusted-access process.
- **Zhipu "Cybersecurity Trusted Access":** known only via Bloomberg/secondary reporting (startupfortune 11-17), with no primary page and no opening date. Watch.
- **GPT-6 Rosalind Research:** only an enterprise release-note line (10-30), already seen by the 10-31 run. No new primary document.
- **Other checks:**
  - Mistral Timestral (time-series forecasting) is auxiliary.
  - DeepSeek API features (11-13) were judged yesterday.
  - Restricted-access programs (Rosalind, Daybreak, Glasswing/CVP, LSVP, Claude Science, Gemini for Science, Flash Cyber/CodeMender, Isomorphic bioresilience): nothing new in the window.
- **Watch list:**
  - **Grok 4.8:** still no card.
  - **Muse Spark 1.4:** not released.
  - **Tencent Hy4:** open weights and system cards still "coming days".
  - **Qwen4-Max:** tech report or HF card if one appears.
  - **Apollo/OpenAI:** first embedded-evaluation report.

## Citation mining

- **Hydrogen report:** references GDM's own reports and Irregular's CyScenarioBench, used in-house; no separate third-party report is cited.
- **Redwood post:** cites the catalogued Argon and Carbon safety reports.
- **Sigma:** cites its own arXiv report (recorded as a related_url).

Nothing to propose.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 20 openai.com / help.openai.com URLs (16 at streak 30, 1 at 26, 3 at streak 5).
- **My own fetches:** read_doc fetched measuring-how-ai-agents-handle-wet-lab-science, a-thousand-fewer-paths-to-root, the Daybreak trusted-access help article and scaling-trusted-access-for-cyber-defense, all with HTTP 200 via browser_impersonation.
- **Verdict:** alive and bot-blocked; no status changes.

## Document updates (task 6)

The top 5 are again v1056, v773, v1170, v924 and v1015, all judged in earlier runs as noise or already handled. Skipped. No new versions entered the queue.

## Friction and proposals

- **Friction:** 4 entries.
  1. Recurrence: OpenAI Phase A 403s, with read_doc working.
  2. Recurrence: stale updated_docs head.
  3. Recurrence: qwen.ai unfetchable (Qwen4-Max).
  4. ambiguous_criteria: whether a safety classifier's own detection and fairness evals count as safety evals, using the OpenAI CSAM classifier card as the case.
- **PROPOSALS.md:** no new entry.
