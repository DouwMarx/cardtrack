# cardtrack agent run — 2026-10-17 (run id 2026-10-17T06:19Z-local)

- **Lookback:** the last agent success was 2026-10-16T06:24:04Z, so the search used the 72 h minimum (2026-10-14 to 10-17).
- **Weekly retrospective sweep:** not run (today is Saturday).
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (independent_eval) | Epoch AI "Open-weight models trail closed models in cyber capabilities by 6–7 months" (2026-10-16; restricted; cyber) https://epoch.ai/data-insights/open-closed-cyber-eci-gap | **written** (`epoch-ai-glm-5-3-independent-eval`, doc 394, v864) |
| 2 | annotate_version | `anthropic-claude-mythos-preview-other-10` v861 | **written** |

### #1 Epoch Cyber ECI open/closed gap

- **Findings:**
  - Cyber ECI scores for 57 models, fit over 35 cyber benchmarks and 324 results drawn from UK AISI, CAISI, Irregular and developer reports.
  - GLM-5.3 is the top open-weight model at 160. It sits above GPT-5.4 (157) and below Mythos Preview (165) and GPT-5.5 (162), which puts the open cyber frontier 6–7 months behind closed models.
  - Opus 5.5 and GPT-6 Astra lead at 171.
- **Precedent:** follows the claude-ds-eci and astra-eci-breakdown rows.
- **Openness:** `restricted`, because Claude Mythos Preview (limited access) is a named comparator. The validator assigned slug `…-glm-5-3-…`, after the first named model.
- **Date:** "Oct. 16, 2026" is on the page, by Jaeho Lee and Alexander Barry.

### #2 Mythos unintended-actions post (v861)

- Anthropic added a "Corrected Oct 12, 2026" note: the stated reason for the web-fetch URL-length limits changed from "prevent SQL/command injection" to "reduce the risk of data exfiltration".
- Everything else in the diff is copy edits and rotated related-content links.

## Phase A candidates

- **Already triaged in earlier runs:** everything first seen 10-06 to 10-16.
- **New today (55), all skipped:**
  - **Anthropic:**
    - "Claude reveals ECDSA curve origins" (Frontier Red Team): a capability showcase by an unnamed "internal research model" with no measured results.
    - "Designing more efficient quantum circuits with Claude": a science showcase.
    - Three Economics posts (expectations gap, employment, expectations for the future) and Claude for Google Workspace: out of scope.
  - **Epoch:** open-closed-cyber-eci-gap was **proposed (#1)**.
  - **METR Time Horizon 1.1:** already in the DB as `metr-claude-opus-4-5-independent-eval` (URL `2026-1-29` vs `2026-01-29`, so a mirror).
  - **SecureBio:**
    - "Response to Anthropic's update on independent evaluators": an organisational post. It notes Anthropic revised its tier description; there is no Anthropic row for that post.
    - "Nature Sets a Baseline, Not a Ceiling" (both URLs): a policy essay.
  - **NIST CAISSI/NSA/CISA "Key practices for incident readiness and response in SI training":** voluntary guidance that names no model.
  - **Redwood "Screwtape" adversarial transcript editing:** a monitor red-teaming method. Its target monitor is unnamed, and Opus 4.8 and Gemini 3.1 Pro are used only as proxy monitors, so it fails the system-card test.
  - **NVIDIA Nemotron Labs Dory1.0-4B (BF16/NVFP4/MXFP8/GGUF, released 10-16):** a general-purpose LLM and in NVIDIA's scope, but with no NVIDIA announcement outside HF. Search finds only the HF repos and an aggregator blog calling it "a quiet HF release", so it fails notability. **Watch** for a blog or tech report.
  - **NVIDIA, other:** GLM-5.3-Flash-FP4-Local is a quant artifact and lidarverse is out of scope.
  - **Tencent:**
    - Hy-Memory-30B-A3B: an auxiliary memory-writer model.
    - Qwen3-8B-DSpine and the DSpine collection: a speculative-decoding drafter.
  - **Not documents:** Cursor changelog, DeepSeek search guide, HF listing/profile/collection/discussion URLs.

## Targeted search (10-14 to 10-17)

- **Already in the DB:**
  - Haiku 5.5 system card
  - GPT-6 Sol/Luna October update
  - GPT-Live-1.1
  - Gemini 4 Argon (GA on 10-13)
  - Anthropic CVP three-tier expansion: news/cyber-verification-program, covered by The Hacker News on 10-07
  - LSVP: news/life-sciences-verification-program
  - Rosalind Academic Plan
- **No new documents in window:**
  - xAI: no Grok 5 card
  - Qwen, DeepSeek, Kimi, MiniMax, GLM
  - METR, Apollo, Transluce, UK AISI
  - Glasswing, Claude Science, Daybreak, Gemini for Science, Flash Cyber, CodeMender
- **Muse Spark Open full evaluation report:** still not published; keep watching.

## Citation mining

- **Today's Epoch add:** its sources are the CAISI GLM-5.3 assessment (already `us-caisi-glm-5-3-independent-eval`), UK AISI, Irregular and developer cards. There is nothing new to add.
- **Yesterday's adds:** already mined in the 10-16 run.

## Blocked-URL escalations (task 5)

- **Streaks:** 14 openai.com/help.openai.com rows are at streak 16 (11 for accelerating-cyber-defense-ecosystem). The Rosalind Academic Plan row is a fresh block at streak 1.
- **Change from earlier runs:** read_doc.py now also gets HTTP 403 on every URL I tried: accelerating-cyber-defense-ecosystem, introducing-the-rosalind-academic-plan, the Daybreak help article, path-to-astra, and introducing-gpt-rosalind twice. WebFetch also gets 403.
- **Why they are still treated as alive:** 403 is a bot block, not a 404, and web search still returns introducing-gpt-rosalind with current content. No status changes were proposed.

## Document updates (task 6)

- **Annotated:** one new version since the last run, Mythos v861 (#2).
- **Not annotated:** the other 19 queued entries were fetched before the last agent run and were judged noise then (HF widget, counter, sample-code and furniture churn).

## Friction and proposals

- **Friction, one entry:** a `regression` against RESOLVED.md row 17 (read_doc.py as the fix for openai.com 403s). Its browser-impersonation fetch, which worked on every run from 10-07 to 10-16, now gets 403 too.
- **Impact:** any new OpenAI document published while this lasts cannot be read, and therefore cannot be proposed.
- **No new proposals.** The 403 issue was already filed in PROPOSALS.md on 10-07.
