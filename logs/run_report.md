# cardtrack agent run — 2026-10-31 (run id 2026-10-31T06:17Z-local)

- **Lookback:** the last agent success was 2026-10-30T06:26:09Z, so the 72 h minimum applied (2026-10-28 to 10-31).
- **Weekly retrospective sweep:** not run. Today is Saturday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | OpenAI "GPT-Rosalind-6 System Card Addendum" (PDF, 2026-10-30), addendum | **written** → `openai-gpt-rosalind-6-addendum` (doc 424, v1029) |
| 2 | field_update | `securebio-gpt-6-astra-independent-eval`: related_urls + SecureBio erratum page | **written** |
| 3 | annotate_version | `openai-gpt-5-6-sol-access-policy` v1027 (Daybreak help article) | **written** |

### #1 GPT-Rosalind-6 addendum
- **Canonical URL:** the PDF. The deploymentsafety HTML page is recorded as `web_version`.
- **Date:** 2026-10-30, from the Deployment Safety Hub index ("Oct 30, 2026"). The ChatGPT Business release notes confirm GPT-6 Rosalind Research began rolling out that day. The PDF itself only says "October 2026".
- **What it is:** trusted-access only. It uses the same weights as GPT-6 Astra but has a different refusal boundary and its own deployment. It is treated as a distinct named release, like the Rosalind-5.5 card, which is noted in `notes`.
- **Preparedness ratings:** High bio/chem. Critical cyber, inherited from Astra. Below High on self-improvement.
- **Bio/chem High evals:**
  - ProtocolQA 42.0%.
  - TroubleshootingBench 59.0%.
  - Biorisk cons@32 78.3%.
  - Multi-select Virology 59.9%.
  - After refusal adjustment, three of the four exceed their thresholds.
- **Bio/chem Critical evals:** all four are below threshold.
- **Biosecurity safeguard benchmarks:** Severe 98.1%, Sensitive 79.0%.
- **Cyber:** a historical-jailbreak regression on ExploitBench tasks (14.3%).
- **Alignment and monitoring evals:** blocker deception, sabotage, CoT controllability.
- **Flags:** risk tags cbrn, cyber, loss_of_control; openness `restricted`. Not tagged societal_harm, because the addendum has no such evals.
- **No openai.com announcement post was found.** Search turned up only the help-center release note and third-party coverage.

### #2 SecureBio erratum
- **The correction:** the GPT-6 Astra WCB score of 61.6% ± 0.6% was run with web search enabled. Corrected with search disabled, it is 59.2% ± 0.6%. SecureBio says its conclusions are unchanged.
- **Why not a new row:** it corrects an existing report, so it was added as a companion URL (kind `other`).
- **Existing companions kept,** with their kinds set to: PDF → `full_document`, securebio.org blog → `web_version`, OpenAI Astra hub → `other`.
  - I could not read the stored kinds (no DB access), so these may differ from what was there before.
- **Related upstream change:** search shows the GPT-6 Astra system card changelog also records the correction. The monitor should pick that up as a new version of the Astra row.

## Phase A candidates (21 first seen today)

- **Proposed:** the Rosalind-6 addendum (#1) and the SecureBio erratum (#2).
- **Skipped:**
  - **Epoch "biorxiv-llms-vs-ai-tools":** a data insight on LLM-use trends in preprints. It does not evaluate a model.
  - **Cursor security notice:** a malicious claude-code extension in Cursor's marketplace. This is a supply-chain incident, not model documentation.
  - **NVIDIA "nemotron-halloween":** an HF blog showcase of existing models with no evals. Also skipped: two Cosmos3 discussion threads, the DeepSeek-V4.1-Flash-1017-NVFP4 quant re-host, and one profile.
  - **Tencent:** the Youtu collection and the Youtu-Parsing-Omni paper. Document parsing is an auxiliary model class.
  - **inclusionAI:** the ZwZ2 4B/9B/27B GGUF quants. ZwZ2 is a GRPO perception fine-tune of Qwen3.6, outside the inclusion_ai scope note.
  - **MiniMax:** an M3.1-Flash community discussion and five navigation links (console, pricing, M Plan, blog, agent).
  - **DeepSeek:** an API docs markdown link.
- Everything first seen before today was triaged in earlier runs.

## Targeted search (10-28 to 10-31)

- **Rosalind-6:** the only new in-scope primary document found (#1).
- **Already in DB:** Mistral Large 4 open weights (10-29), Gemini 4 Carbon / Fairwind (10-28), GPT-6.1 Terra (10-26), and GPT-6 Sol/Luna October.
- **OpenAI Model Spec update (10-29):** a general behavior policy that does not evaluate a named model. Skipped under the doc_type `other` scope rule.
- **Microsoft MAI-Code-1.1-Flash** (press on 10-30/31 about a 3-bit local build):
  - Microsoft is not allowlisted, so I proposed nothing.
  - Search found 8 MAI model-card PDFs on microsoft.ai. I read the MAI-Code-1.1-Flash card: released 2026-08-11, with cyber safety evals. None of these cards are in the DB.
  - Filed as a proposal (below).
- **Still unreleased:** Qwen 4 (no card, weights or API as of 10-29) and xAI Grok 5 (no card).
- **Evaluators:** nothing new from METR, Apollo, AISI or CAISI in the window.
- **Restricted-access polling:**
  - Rosalind-6 Research is covered by #1. It does not broaden eligibility beyond earlier announcements such as the Rosalind Academic Plan.
  - The Daybreak changes are covered by #3.
  - Nothing new from LSVP, CVP, Glasswing, Claude Science, Gemini for Science or CodeMender.

## Citation mining

- **Rosalind-6:** cites the GPT-6 Astra system card and the GPT-Rosalind-5.5 system card. Both are in DB.
- **SecureBio erratum:** cites only its parent report.
- **Result:** no new leads.

## Blocked-URL escalations (task 5)

- **What Phase A reports:** all 16 openai.com / help.openai.com rows return 403 (streak 30; 25, 15 and 9 for the newer ones).
- **Today's agent-side check:** read_doc.py returned HTTP 200 via browser_impersonation on three pages, unlike the last few runs:
  - path-to-astra
  - trusted-access-for-cyber
  - strengthening-societal-resilience-with-rosalind-biodefense
  - It also reached help.openai.com.
- **Conclusion:** the pages are alive, so there are no status changes. This is the agent-side-OK / Phase-A-403 split already filed in PROPOSALS.md (2026-10-07).

## Document updates (task 6)

- **Top 5:** v773, v924, v1015, v573 and v578 were all judged noise in earlier runs and were not re-read.
- **openai-gpt-5-6-sol-access-policy v1027 (new today, rank 7):** substantive.
  - It adds a "Using GPT-6.1 Terra with Daybreak" section: reduced cyber refusals are available to Daybreak Red only, with explicit per-request enablement.
  - From gpt-6.1-terra on, omitting `access_programs.cyber` now gives standard refusals instead of the highest tier.
  - Annotated (#3).
- **Ranks 6 and 8-20:** all predate today and were handled in earlier runs. Not re-read.

## Friction and proposals

- **Friction, one recurrence:** the stale updated_docs top 5 (of 2026-10-30T06:25:31Z).
- **No openai.com 403 entry today:** the agent-side fetch succeeded.
- **New proposal:** "Microsoft AI publishes model cards (MAI-Code, MAI-Image) but is not an allowlisted publisher".
  - It suggests a `microsoft_ai` source entry with a scope note, followed by a backfill of the microsoft.ai/pdf cards.
  - PROPOSALS.md had no earlier Microsoft entry.
