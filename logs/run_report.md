# Run report — 2026-11-28T06:16Z-local

Last agent success: 2026-11-27T06:26Z. Search window: the 72 h minimum (since 2026-11-25). Today is a Saturday, so there was no weekly retrospective sweep.

## Proposals and validator verdicts

| Action | Target | Verdict |
|---|---|---|
| annotate_version | thinking-machines-inkling-2-mini-model-card v1360 | **written** (document 489) |

## Task 1: Phase A candidates (first_seen 2026-11-28)

- **apolloresearch.ai/embedded-evaluations**: skipped. It is Apollo's position and program page on embedded evaluations: minimum access and disclosure standards, a verdict taxonomy, and an FAQ on the OpenAI pilot. It names no model and reports no results, so it fails the system-card test. When Apollo publishes its two pilot reports, those will be in scope.
- **Watcher case studies, Watcher blog, Watcher docs and the Apollo Substack root**: skipped as product and navigation furniture.
- Older carried-over candidates were triaged in earlier runs and not revisited.
- **tencent/Hy-Embodied-Apexio-1.0** (pending since yesterday): re-checked, and it still shows "No model card". **Re-check this card on the next runs.**

## Task 2: Targeted web search

Queries:
- "system card November 27 2026"
- November 2026 open-weight model-card releases
- November 2026 trusted-access programs
- the nocode.mba November tracker for Nov 25-28
- METR, UK AISI and Apollo November eval reports
- Anthropic LSVP, Cyber Verification Program and Claude Science
- DeepSeek, Qwen, Kimi, GLM and MiniMax reports
- Gemini model cards
- xAI, Mistral and Meta releases
- third-party evals of GPT-6.2 (Palisade, Transluce, CAISI, SecureBio)
- "SecureBio GPT-6.2 Astra assessment"
- "UK AISI GPT-6.2 Astra" (including a domain-restricted search on aisi.gov.uk)
- restricted-access and vetted-researcher signal phrases

Results:

- **Nothing new and qualifying.**
- **openai.com/index/broad-access-through-consistent-standards/**: read and skipped. It is a Usage Policies and partner-safeguards update (effective 2026-11-20). GPT-6 Astra is mentioned only in passing, and the post defines no access gate for a named model. That makes it a policy update, not an access_policy.
- **openai.com/index/expanding-chatgpt-for-academic-researchers/**: read and skipped. It describes free ChatGPT Plus grants on a first-come basis, which is a subsidy and not a capability gate. The Rosalind Academic Plan it mentions is already catalogued.
- **openai.com/index/our-first-phase-of-embedded-assessments/** (Nov 16): read and skipped. It announces future embedded assessments by Apollo, METR, Transluce and Goodfire, but contains no results and names no specific model. Watch for the resulting reports.
- **SecureBio and UK AISI on GPT-6.2 Astra**: their findings appear only as sections of OpenAI's GPT-6.2 system card, which is already catalogued. I found no standalone SecureBio or AISI GPT-6.2 report. AISI's GPT-6 Astra research page is the same report as an existing row (PDF canonical plus blog).
- **Already catalogued**: Gemini 4 Hydrogen, Neon, Carbon and Omni 1.2 Flash; Fairwind; GPT-6 Cyber; GPT-Rosalind; LSVP; Mistral Large 4; Inkling 2 Mini.
- **Not allowlisted or undocumented**: FoxBrain v2.1 (Nov 27), plus the Nov 25 batch already noted yesterday.

## Task 3: Citation mining

No documents were added in the last two runs, and docs 497-500 were mined on 2026-11-26, so there was nothing new to mine.

## Task 4: Open issues

`fetch_ok: true`, and the list is empty.

## Task 5: Blocked URLs

`blocked_escalations` and `not_found` are empty. `phase_a_summary.blocked` lists 8 HF model pages that returned 429 (streak 1). I re-fetched four of them and all returned HTTP 200 with full cards: tencent/Hy4, baidu/ERNIE-5.5-Flash-Base, inclusionAI/Ling-3.2-air and nvidia/Nemotron-Labs-Image-30B-A3B. This was transient HF rate-limiting, and the pages are alive.

## Task 6: Document updates

- The top 5 in order are v1304, v1056, v773, v1170 and v924. Earlier runs judged all five as noise, and nothing has changed since.
- **v1360** (Inkling 2 Mini model card, fetched today, rank 9): substantive, so I annotated it. Many previously blank comparison-model cells were filled in, and one comparison score was removed. Inkling 2 Mini's own scores are unchanged.

## Task 7: Friction logged

- `recurrence` (of 2026-11-25T06:28:12Z): the updated_docs top 5 holds only already-judged versions again. Today's new substantive version sat at rank 9.

## Task 8: Proposals

None filed. The stale-queue problem is already covered by the open 2026-10-28 PROPOSALS entry, which asks for a way to dismiss a version.
