# cardtrack agent run — 2026-10-08 (run id 2026-10-08T06:19Z-local)

- **Lookback:** the last agent success was 2026-10-07T06:27:16Z, so the search used the 72 h minimum lookback (from 2026-10-05).
- **Weekly retrospective sweep:** not run (today is Thursday).
- **Open issues:** `open_issues.json` has `fetch_ok: true` and no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add `system_card` | Anthropic "System Card: Claude Haiku 5.5" (2026-10-07) | **written**: `anthropic-claude-haiku-5-5-system-card` (doc 371, v781) |
| 2 | add `addendum` | OpenAI "GPT-6 Sol and GPT-6 Luna: October 2026 update" (2026-10-07) | **written**: `openai-gpt-6-sol-october-addendum` (doc 372, v782) |
| 3 | add `independent_eval` | Epoch AI "InnovationEval" (2026-10-07) | **written**: `epoch-ai-claude-fable-5-independent-eval` (doc 373, v783) |
| 4 | add `independent_eval` | Epoch AI "EBR-bench update" (2026-10-07) | **written**: `epoch-ai-gpt-6-astra-independent-eval-3` (doc 374, v784) |
| 5 | annotate_version | `google-deepmind-gemini-3-8-live-model-card` v779 | **written** |

Notes:

- **#1 Haiku 5.5**
  - Canonical URL is the stable `anthropic.com/claude-haiku-5-5-system-card`, which redirects to the CDN PDF (dated October 7, 2026, 13 MB). The CDN PDF and the announcement are recorded as related_urls.
  - Tagged with all five domains:
    - `cbrn`: CB-1/CB-2 evals.
    - `cyber`: ExploitBench, CyScenarioBench, BEB and ExploitGym.
    - `loss_of_control`: AI R&D/AECI, alignment-risk update, SHADE-Arena/LinuxArena and CoT controllability.
    - `harmful_manipulation`: behavioral-audit sycophancy and delusion metrics.
    - `societal_harm`: child safety, mental health, bias and elections.
  - `closed`.
- **#2 GPT-6 October**
  - Canonical URL is the PDF; the deploymentsafety HTML is the `web_version` and "GPT-6 for everyone" is the `announcement`.
  - Model names follow the precedent of the GPT-5.6 August addendum: "GPT-6 Sol (October)" and "GPT-6 Luna (October)".
  - Tagged `cbrn`, `cyber`, `loss_of_control` and `societal_harm`:
    - Bio tables at both High and Critical thresholds.
    - ExploitBench and SEC-Bench Pro.
    - Alignment tests on obeying restrictions and auto-review, plus deception.
    - Under-18 and mental-health evals.
  - `closed`.
- **#3 InnovationEval**
  - End-to-end AI R&D evaluation, with main results on Fable 5 and GPT-5.6 Sol and contaminated results on Fable 5.1 and GPT-6 Astra.
  - Documents misleading claims (seed farming and undisclosed run selection). Tagged `loss_of_control`.
  - The validator named the slug after the first model.
- **#4 EBR-bench update**
  - New results under the card ban for Fable 5.1, Opus 5, GPT-5.6 Sol and GPT-6 Astra, plus a multi-agent scaffold experiment.
  - `loss_of_control` follows the tag on the original EBR-bench row (`epoch-ai-gpt-5-5-independent-eval-2`), which is linked as `other`.
- **#5 Gemini 3.8 Live v779:** adds Gemini Enterprise Agent Platform as a channel for the two TTS models. The rest is PDF page numbers.

## Phase A candidates (79)

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-07; see the 10-07 report. Nothing about those has changed.
- **New today:**
  - Haiku 5.5 (#1), GPT-6 October (#2), InnovationEval (#3) and EBR-bench update (#4).
  - Skipped:
    - Epoch "cyber incidents flat since Fable 5": a population poll, with no named-model evaluation.
    - UK AISI "Transect": eval-transcript tooling, with no model evaluated.
    - FAR.AI "AI-enabled terrorism" (UNGA 81, dated 09-22): an event recap.
    - NVIDIA HF blog on Nemotron IOI/IMO gold: competition fine-tunes of the catalogued Nemotron 3 Ultra, so it fails the distinct-release test.
    - `nvidia/music-flamingo-hf`: an old research model (page: "we have released a new checkpoint"), and the activity is only an update.
    - `nvidia/Cosmos-Embed1-448p-anomaly-detection`: auxiliary detector.
    - NVIDIA datasets, HF paper pages, HF user profiles and the `tencent/EVIE-4.5B` discussion thread: not documents.
    - `mistral.ai/javascript:openAxeptioCookies()/`: a cookie-consent link parsed as a URL.

## Targeted search

- A subagent swept 10-05 to 10-08: lab cards, evaluator blogs (METR, AISI, Apollo, Epoch, CAISSI, SecureBio, FAR.AI, Palisade, Gray Swan, Irregular, Transluce, SaferAI) and program polls (Rosalind, Daybreak, Glasswing/Mythos, LSVP, CVP, Claude Science, Gemini for Science/Co-Scientist, CodeMender). It found **no further in-scope documents**.
- **Third-party evals:** none yet of Haiku 5.5 or the GPT-6 October models.
- **Held leads:**
  - **StepFun Step 5:** no card in the stepfun-ai org. `SHSLab/Step-5-Preview-BF16` is a third-party, possibly leaked repo and must not be catalogued as StepFun's. Weights are expected 10-15.
  - **Ling-3.1-flash:** still trial-API only.
  - **Mistral Large 4:** the HF repo is an "Upcoming release" placeholder (ETA 2026-10-31) with no license. Row 369 stays `closed`; re-check openness after the release.
- **Watch: Reflection AI "Beam"** (blog 10-05). A 501B open-weight model with Apache 2.0 promised, and a card, tech report and safety evals promised for later in October. Reflection is not on either allowlist. Not proposed for allowlisting yet; revisit once the documentation exists.
- **Rejected:**
  - Anthropic "Claude discovers a novel enzyme system" (research announcement).
  - Epoch "Can AI automate AI R&D yet?" (appears to be the InnovationEval publication).
- **Coverage gap:** Meta, xAI, Cohere, AI21, IBM, Reka, poolside, Thinking Machines, Cursor, Hunyuan and MiMo were covered only by general searches today. Yesterday's silent-org sweep checked most of them.

## Citation mining

- **Haiku 5.5 card:** cites SecureBio VCT, Epoch ECI, Irregular CyScenarioBench and the Gray Swan IPI benchmark/Shade (with UK AISI and CAISSI). These are all benchmarks or tools, not evaluation reports, so there is nothing new to propose.
- **GPT-6 October update:** cites the GPT-6 Astra and GPT-5.6 cards, both already catalogued.

## Blocked-URL escalations (task 5)

- All 13 escalated openai.com/help.openai.com rows (streak 7) and `openai-gpt-5-4-cyber-access-policy` (streak 2) are **alive**.
- I sampled seven with `read_doc.py` and all returned HTTP 200 via browser_impersonation: accelerating-cyber-defense-ecosystem, introducing-new-capabilities-to-gpt-rosalind, introducing-gpt-rosalind, pacing-model-development-cyber-capabilities, trusted-access-for-cyber, hugging-face-model-evaluation-security-incident, and the Daybreak help article. The Rosalind capabilities page needed a second attempt, so the wall is intermittent.
- No status changes were proposed.
- The Rosalind page confirms access is still "through our trusted-access program", so `restricted` remains correct for the Rosalind rows.

## Document updates (task 6)

Top 5 by substantive_lines:

1. `deepseek-deepseek-v4-1-flash-model-card` v773: **noise**. HF snippet swap (completions → chat/completions with an image example), download/Spaces counters and a reordered eval-leaderboard widget. Skipped.
2. `deepseek-deepseek-v4-pro-model-card` v573: **noise**, as judged on 10-06/10-07. Skipped.
3. `deepseek-deepseek-v4-flash-0731-model-card` v578: **noise**, as judged on 10-06/10-07. Skipped.
4. `google-deepmind-gemini-3-8-live-model-card` v779: substantive but minor. Annotated (#5).
5. `anthropic-claude-mythos-5-other-3` v565: **noise** (hyphenation and teaser rotation), as judged on 10-06. Skipped.

The noise versions are never annotated, so they stay at the head of the queue every day.

## Friction and proposals

- **Friction 1:** `recurrence` of 2026-10-06T06:29:48Z. The furniture classifier still passes HF snippet/widget churn, now on v773, which was fetched today, so it is not a retroactivity gap.
- **Friction 2:** `recurrence` of 2026-10-06T06:29:51Z. Phase A's openai.com 403 streak is a false alarm, now at streak 7.
- **No new proposals.** The openai.com 403 issue was filed 2026-10-07. The furniture-classifier miss is in friction and does not yet need a separate proposal.
