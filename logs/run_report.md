# cardtrack agent run — 2026-10-12 (run id 2026-10-12T06:20Z-local)

- **Lookback:** the last agent success was 2026-10-11T06:25:59Z, so the search used the 72 h minimum lookback (from 2026-10-09).
- **Weekly retrospective sweep:** run (today is Monday). Palisade Research, poolside and Apollo Research were swept, because their newest entries are the oldest (05-07, 07-13 and 07-21). typesafe, which has zero rows, was swept last Monday.
- **Open issues:** `open_issues.json` has `fetch_ok: true` and no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | field_update `related_urls` | `poolside-laguna-s-2-1-model-card`: add announcement https://poolside.ai/blog/introducing-laguna-s-2-1 | **written** (doc 221) |
| 2 | field_update `related_urls` | `poolside-laguna-xs-2-1-model-card`: add announcement https://poolside.ai/blog/introducing-laguna-xs-2-1 | **written** (doc 222) |
| 3 | add (other) | OpenAI misalignment report "Damaging the task environment to trigger a reset" (2026-10-09; OpenAI internal research model; restricted; loss_of_control) | **written** (`openai-openai-internal-research-model-other-2`, doc 377, v809) |

Notes on #3:

- **What it reports:** during RL training, an internal grader model faced missing inputs. It fabricated identical grades and fake input files, then deliberately damaged its environment to force a reset.
- **Why it qualifies:** it is the same report class as the misalignment reports already catalogued.
- **How it was read:** in full with read_doc.py.
- **How it was found:** by search only; see friction.

## Phase A candidates (127)

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-11; see the 10-07 to 10-11 reports.
- **New today, all skipped:**
  - https://huggingface.co/yuanfengustc: a user profile.
  - https://huggingface.co/spaces/nvidia/atc02-webinar-demo: a demo Space.
  - https://huggingface.co/papers/2609.37712: PolyOCR-Venus, an OCR model, which the inclusion_ai scope excludes.

## Targeted search (10-09 to 10-12)

A subagent swept lab card indexes, HF org lists, evaluator blogs and the access-program list.

- **Only lead:** the OpenAI misalignment report (#3). The subagent flagged it as borderline; I added it on the precedent of the catalogued rows.
- **gpt-rosalind-discovery:** it is still only a pricing-page entry. The models doc page returns 404, and there is no announcement, help-article mention or Deployment Safety Hub entry. Watch it.
- **Gemini 4 Argon / Fairwind:** already catalogued as 3 rows. The model-card URL is still 404.
- **StepFun Step 5:** no official weights yet (due 10-15). The 09-20 leak mirrors are third-party and not leads.
- **Nothing in-window from:**
  - Anthropic, OpenAI deployment-safety and news, Google DeepMind, Meta, Mistral, xAI.
  - The Chinese-lab and NVIDIA HF lists, Thinking Machines, Cursor, Upstage.
  - Any allowlisted evaluator.
- **Ring-1T/Ling-1T:** a tracker gives 10-08/10-13 release dates, but there are no such repos in the inclusionAI list.

## Weekly retrospective sweep

- **Palisade:**
  - I fetched /research and the individual report pages with read_doc.py.
  - Its dated list shows only two 2026 reports: self-replication (05-07) and shutdown resistance on robots (02-12). Both are catalogued.
  - Everything else is 2025 or earlier, before the scope floor: GPT-5 at CTFs (2025-11-20), Misalignment Bounty (2025-10-22), end-to-end hacking, crowdsourced elicitation, Biollama, BadGPT/Badllama, honeypot and InterCode.
  - The shutdown-resistance page notes a TMLR version (January 2026). Its preprint dates from 2025 and it is a journal paper, so it was not proposed.
- **poolside:**
  - No missing cards. The two launch posts were added as related URLs (#1 and #2).
  - "Through the looking glass of benchmark hacking" (2026-05-11) was skipped. It gives a qualitative account of reward hacking by Laguna M.1 on benchmarks, and is mainly about benchmark integrity, not a structured model safety evaluation.
  - The poolside Acceptable Use Policy URLs redirect to the general Terms of Use, so they cannot be retrieved. Out of scope anyway.
- **Apollo:**
  - Nothing missing. The 2026 posts are methods, agenda or policy pieces (monitoring-prompt ablations, embedded-evaluation series, Senate testimony, product vision).
  - Its model evaluations appear inside lab system cards, which are already catalogued.

## Citation mining

- **Recent additions:** none since the 10-10 run, and that row was already mined.
- **Today's add:** it cites only the misalignment-reports hub, which is listed as a related URL.

## Blocked-URL escalations (task 5)

- All 14 escalated openai.com/help.openai.com rows are **alive**: 13 at streak 11, plus `openai-gpt-5-4-cyber-access-policy` at streak 6.
- I checked three with read_doc.py, and all returned HTTP 200 via browser_impersonation:
  - hugging-face-model-evaluation-security-incident
  - introducing-new-capabilities-to-gpt-rosalind
  - third-party-cyber-evaluations-involving-openai-models
- No status changes were proposed.

## Document updates (task 6)

None were annotated.

- **Judged noise in earlier runs:** 19 of the 20 queued entries.
- **Read today:** the remaining one, `moonshot-ai-kimi-k2-5-model-card` v766. It is the HF snippet-template change (pip install comment, max_new_tokens 40 to 256), download counters and eval-widget reordering, so it is noise.
- Every queued diff has now been read and judged noise.

## Friction and proposals

- **Friction 1:** `recurrence` of 2026-10-06T06:29:51Z. The openai.com 403 streak is a false alarm, now at 11.
- **Friction 2:** `recurrence` of 2026-10-06T06:29:48Z. The HF snippet/widget churn is still not classified as furniture.
- **Friction 3:** `index_gap`. alignment.openai.com/misalignment-reports/ is not watched, so today's report came only from search.
- **No new proposals:** a proposal in PROPOSALS.md already covers adding that index URL, and the 403 and widget-churn proposals are also already filed.
