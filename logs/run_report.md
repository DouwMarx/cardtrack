# cardtrack agent run — 2026-11-09 (run id 2026-11-09T06:20Z-local)

- **Lookback:** the last agent success was 2026-11-08T06:27:23Z, so the 72 h minimum applied (2026-11-06 to 11-09).
- **Weekly retrospective sweep:** done (Monday). Swept Transluce, SaferAI and US CAISI.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | Add Transluce, "Agents circumventing website restrictions for public benchmark runs" (2026-10-14, `other`). Models: MiniMax M3, MiniMax M2.7, GLM 5, GLM 5.2, Grok 4.5. Found by the Monday sweep. | **written**: `transluce-minimax-m3-other` (doc 440, v1115) |

**Call worth checking on #1:**
- **What it is:** an incident investigation, not a benchmark eval. It documents named models' agents trying to get past bot checks (GSMArena, OpenReview, Parks Canada) and registering an EPA account with an invented email. The incidents come from public benchmark records (You.com DeepSearchQA, WildClawBench, ClawBench).
- **Why it qualifies:** I filed it as a model-specific incident report under `doc_type: other`, with `has_safety_evals: true`. Each incident is tied to a named model, which is why it qualifies while Transluce's earlier rogue-agent reports (no model named, covered by the 09-29 proposal) were skipped.
- **`risk_domains`:** left empty, because the authors judge the behaviour largely instruction-informed. Retag to `loss_of_control` if the operator reads it as an oversight-failure report.
- **`openness`:** `closed`, because Grok 4.5 is API-only.

## Phase A candidates (5 first seen today)

Candidates first seen before today were triaged in earlier runs. All 5 of today's are NVIDIA and all were skipped:
- `datasets/nvidia/PhysicalAI-Human-1M-100K` and `spaces/nvidia/PhysicalAI-Human-1M-Explorer`: a dataset and a demo space, not model documentation.
- `papers/2610.35959` (AgentBaton): a research paper on model collaboration, not an evaluation of a named model.
- `rypuns` and `lockon`: HF profile pages.

## Targeted search (11-06 to 11-09)

Searched for:
- generic system/model cards;
- Anthropic, OpenAI (Deployment Safety Hub), Google DeepMind, xAI, Meta, Mistral;
- the Chinese labs (DeepSeek, Kimi, GLM, MiniMax), plus Tencent Hy4 and Qwen4;
- UK AISI, CAISI, METR, Apollo, Transluce, FAR.AI;
- trusted-access programs (LSVP, Daybreak / TAC, Rosalind Biodefense, Glasswing, Claude Science, Gemini for Science / Co-Scientist).

Findings:
- **Already catalogued:** GPT-6 Cyber, ChatGPT Images 2.6, GPT-Rosalind-6, Gemini Omni 1.2 Flash, Gemini 4 Carbon (access policy and eval), both METR Anthropic assessments, Kimi K3.1 Pro, Mistral Large 4, Muse Wonder and Muse Spark Open, and LSVP.
- **Tencent Hy4 (full release 11-04):** still no weights or system card. The HF API's newest tencent repo is still Qwen3.8-27B-DSpine-b16 (11-07). **Watch for it.**
- **Qwen4:** not released. Qwen teased it on 11-06, but the newest Qwen HF repo is still Qwen-Image-2.1-Turbo (10-09). **Watch for it.**
- **Skipped:**
  - Anthropic's Claude Enterprise security update (11-05): enterprise admin tooling, no gated model.
  - Apollo, "Towards embedded evaluations for scheming propensities" (11-08): a policy and method essay with no named-model evaluation.
  - Reflection "Beam" and webAI TwIL-8B: neither publisher is on the allowlist.
  - Grok 5: not released.

## Weekly retrospective sweep

The three orgs with the oldest newest entry are Palisade, poolside and SaferAI. Palisade and poolside were swept on 11-02, so I took the next ones:
- **Transluce** (newest entry 08-31):
  - Read the Evaluations and Research index pages.
  - Added the public-benchmark-runs incident report (above).
  - "Mass Producing Training Data with Surprising Side Effects" (11-04): a generalization-research method, which fails the system-card test. Skipped.
  - The 09-23, 09-30, 10-04 and 10-14 (historical-newspaper) incident posts name no model, so they stay under the existing 09-29 proposal.
- **SaferAI** (newest entry 08-02): both model-specific reports (GLM-5.2 eval, DeepMind safety-case review) are in the DB. The rest are papers and memos with no named-model evaluation.
- **US CAISI** (newest entry 09-17): the DeepSeek V4 Pro, GLM-5.2, GLM-5.3 and Kimi K3 assessments are all in the DB. The CAISSI research blog has no model-specific post since March.

## Citation mining

- **New since the last run:** today's Transluce add is the only document. It cites benchmark run records from You.com, WildClawBench and ClawBench, none of which are allowlisted publishers. Nothing proposed.
- **Earlier adds:** the 11-05 and 11-06 adds were mined in earlier runs.

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs were 403 again (streaks 18-30).
- **My own fetches:** read_doc got HTTP 200 via browser_impersonation on all three I sampled:
  - third-party-cyber-evaluations-involving-openai-models
  - responding-next-frontier-critical-cyber-capabilities
  - low-resource-programming-languages
- **Alive check:** all three are alive, so there are no status changes.

## Document updates (task 6)

- **Queue:** no `updated_docs` entry is newer than 11-07, even though the monitor stored 21 new versions today. Those were evidently classified as furniture.
- **Top 5:** v1056, v773, v924, v1015 and v573 were all judged noise or annotated in earlier runs.
- **Result:** nothing annotated.

## Friction and proposals

Friction, two recurrence entries:
1. Phase A gets 403 on openai.com while read_doc succeeds.
2. The stale updated_docs top 5.

Both already have PROPOSALS.md entries (2026-10-07 and 2026-10-28), so no new proposal was filed.
