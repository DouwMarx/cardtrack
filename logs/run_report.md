# cardtrack agent run — 2026-10-14 (run id 2026-10-14T06:16Z-local)

- **Lookback:** the last agent success was 2026-10-13T06:28:15Z, so the search used the 72 h minimum lookback (from 2026-10-11).
- **Weekly retrospective sweep:** not run (today is Wednesday).
- **Open issues:** `open_issues.json` has `fetch_ok: true` and no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (model_card) | Google DeepMind "Gemini 4 Argon — Model Card" (2026-10-13; closed; cbrn, cyber, loss_of_control, harmful_manipulation, societal_harm) https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Argon-Model-Card.pdf | **written** (`google-deepmind-gemini-4-argon-model-card`, doc 382, v833) |
| 2 | add (system_card) | Google DeepMind "Gemini 4 Argon — Safety & Security Report" (2026-10-13; closed; all five domains) https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf | **written** (`google-deepmind-gemini-4-argon-system-card`, doc 383, v834) |

Notes:

- **Argon general availability:** Gemini 4 Argon rolled out broadly on 2026-10-13 after a Fairwind-only window that began 2026-09-30.
  - The existing Argon rows are the 09-30 access posts, the Fairwind page and the model-evaluation PDF.
  - Both new rows are `closed`: the model now has a public paid API.
  - The "Argon without cyber guardrails" tier is still gated through Fairwind, which is already catalogued.
- **#1 model card:** the PDF was chosen as canonical. The deepmind.google HTML card is recorded as `web_version` and the launch post as `announcement`.
  - It contains the FSF table. Bio CCL and cyber CCL cannot be ruled out, and safety cases were developed. The Stealth/Situational-Awareness TCL cannot be ruled out (14/15 challenges). Harmful manipulation and ML R&D CCLs are not reached.
  - It also has content-safety deltas against Gemini 3.1 Pro and child-safety red-teaming results.
- **#2 Safety & Security Report:** about 200 pages and 17 MB, linked as "full Safety and Security Report" from the safety blog post, which is recorded as `announcement`.
  - It is the frontier system card for Argon: CBRN, cyber (Irregular CyScenarioBench), harmful manipulation, loss of control (alignment assessment, honeypots, CoT monitorability), and misuse safeguards (Gray Swan cyber/bio red-teaming).
  - It also covers child safety, mental health and sycophancy.
  - External testers named: UK AISI, NIST CAISSI, Apollo Research, Gray Swan, Trajectory Labs and Irregular. None of them has published its own Argon report yet; watch AISI (a UK minister said on 10-12 that AISI is evaluating Argon) and Apollo.

## Phase A candidates

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-13.
- **New today (first seen 10-14):**
  - deepmind.google model-cards/gemini-4-argon, the gemini-4-model-safety-security blog post, and introducing-gemini-4-argon: led to #1 and #2. Neither blog post is catalogued separately; both are recorded as announcements.
- **New today, skipped:**
  - developers.googleblog.com "Gemini 4 Argon for robotics": a developer showcase of prompts and demos for an already-catalogued model. Its only metric is ERQA 87%; it is not a model document.
  - deepmind.google on-device-ai-scam-detection-mddi: a partnership post about a fine-tuned Gemma scam classifier. That is an auxiliary classifier and the post has no safety evals.
  - anthropic.com/legal/supported-regions: a legal page.
  - forms.gle (Antigravity research-tier application): a form, not a document. The program is described on the gemini-for-science page, which is already tracked as an index.
  - cursor.com changelog origin-app-marketplace: a product changelog.
  - nvidia/GR00T-N1.7-AppleToPlate-cosine40k-checkpoint-15000: a fine-tune checkpoint.

## Targeted search (10-11 to 10-14)

A subagent swept the lab card indexes, deploymentsafety, misalignment-reports, the evaluator blogs and the access-program list.

- **New finds:** only the two Argon PDFs (#1, #2). The Anthropic self-replication eval it also surfaced was added yesterday (`anthropic-glm-5-2-other`).
- **No new documents in window:**
  - OpenAI: the deployment-safety hub (latest 10-07) and misalignment reports (latest 10-09).
  - Anthropic system cards (latest Haiku 5.5, 10-07).
  - Mistral, Qwen, xAI, DeepSeek, Kimi, GLM, MiniMax.
  - METR, Apollo, Epoch, Gray Swan, Irregular.
  - Rosalind/Daybreak, Glasswing/Mythos, LSVP, Claude Science.
- **Still pending:**
  - Meta's full Muse Wonder safety report.
  - StepFun Step 5 (open weights expected 10-15).
  - `gpt-rosalind-discovery`, seen only on an OpenAI pricing page per press and not announced.
- **Fairwind:** the expansion to "hundreds of additional approved cybersecurity partners" is documented in the launch post and in §2.5.1 of the report. The Fairwind program page shows no visible date change; the monitor tracks it, so any content change will surface as a version.

## Citation mining

- **Argon model card:** cites only the Safety & Security Report (#2) and the evals-methodology page, which is already a related URL of `google-deepmind-gemini-4-argon-other`.
- **Safety blog:** cites the Fairwind page (present), the FSF blog post and the agent-control roadmap essay. The last two are frameworks and general essays, not model documents.
- **Safety report:** names third-party testers, but none of them has a standalone published Argon report. Irregular's CyScenarioBench (2025) is a benchmark paper, not a model evaluation.

## Blocked-URL escalations (task 5)

- All 14 escalated openai.com/help.openai.com rows are treated as **alive**: 13 at streak 13, plus `openai-gpt-5-4-cyber-access-policy` at streak 8.
- I spot-checked two today with read_doc.py, and both returned HTTP 200 via browser_impersonation:
  - path-to-astra
  - introducing-gpt-rosalind
- No status changes were proposed.

## Document updates (task 6)

None were annotated.

- **New since the last run:** kimi-k2-6 v826, mistral-small-4 v830 and qwen3-6-35b-a3b v831. All three are noise: HF download/Spaces counters, a reordered eval-results widget, a sample-code `max_new_tokens` tweak, and duplicated pricing/context furniture removed from the Mistral page.
- **Older queued diffs:** all were read and judged noise in earlier runs.

## Friction and proposals

- **Friction:** one `recurrence` of 2026-10-06T06:29:51Z. The openai.com 403 streak is still a false alarm, now at 13 runs.
- **No new proposals:** the 403 false-alarm fix is already filed in PROPOSALS.md.
