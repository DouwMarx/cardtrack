# cardtrack agent run — 2026-10-27 (run id 2026-10-27T06:19Z-local)

- **Lookback:** the last agent success was 2026-10-26T06:30:25Z, so the 72 h minimum applied (2026-10-24 to 10-27).
- **Weekly retrospective sweep:** not run. Today is Tuesday, and Monday's sweep ran in the 10-26 run.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | OpenAI "Addendum to GPT-6 Astra System Card: GPT-6.1 Terra" (PDF, 2026-10-26) | **written** → `openai-gpt-6-1-terra-addendum` (doc 413, v998) |
| 2 | add | SecureBio "ReproBAIT: A Benchmark for Reproducing Biological AI Tools" (substack, 2026-10-26) | **written** → `securebio-claude-opus-5-independent-eval` (doc 414, v999) |
| 3 | add | UK AISI "Can AI coding agents rebuild biological AI tools from a paper?" (2026-10-26) | **written** → `uk-aisi-claude-opus-5-independent-eval` (doc 415, v1000) |
| 4 | field_update | `securebio-gemini-4-argon-independent-eval`: add the securebio.org copy as related_urls `web_version` | **written** |
| 5 | annotate_version | `anthropic-claude-opus-access-policy` v990 (CVP help article) | **written** |

### #1 GPT-6.1 Terra addendum
- **Lead:** Phase A (deploymentsafety.openai.com index).
- **Read:** the landing page and the full PDF, both read via read_doc. The announcement (openai.com/index/introducing-gpt-6-1-terra/) was readable today via browser impersonation.
- **Canonical URL:** the PDF, with the HTML page as `web_version` and the announcement as `announcement`. This follows the GPT-6.1 Sol addendum row.
- **Contents:**
  - Treated as Critical in cyber and High in bio/chem.
  - Evals: ExploitBench, Sandbox Bench and self-improvement evals; alignment evals (auto-review, honeypot, blocker deception, Codex deployment simulation); CoT controllability and monitor evasion; U18 and mental-health benchmarks.
- **Flags:**
  - Tags: cbrn, cyber, loss_of_control, societal_harm (same as the Sol addendum).
  - `closed`: the model is on the public API as gpt-6.1-terra, plus ChatGPT and Codex.

### #2 and #3 ReproBAIT (co-published)
- **What it is:** a bio dangerous-capability eval, built by SecureBio with UK AISI. Four named coding agents (Claude Opus 5, GPT-5.6 Sol, Kimi K3, Qwen3.8-2.4T) tried to rebuild biological AI tools in a sandbox.
- **Results:** ProteinMPNN reproduction fidelity was 96.5%, 91.3%, 86.3% and 73.4% for the four agents respectively. No agent rebuilt RFdiffusion3, and most successful rebuilds cost under $20.
- **Criteria:** it passes the system-card test, the same way the VCT v2 row did.
- **Two rows:** both orgs are allowlisted, so each org's own copy is its own row (co-publication rule), cross-referenced in notes and `co_published` related URLs. AISI's post is a shorter summary of the same work.
- **Preprint:** arXiv 2610.19810 (submitted 10-14, different title) is recorded as `paper`. It isn't the same document, so it is not the canonical URL. The securebio.org mirror is recorded as `web_version` on the SecureBio row.
- **Flags:** tagged `cbrn`; `closed` (the most restricted of the four models is closed).

### #4 SecureBio Argon related URL
- **Why:** Phase A surfaced securebio.org/blog/gemini-4-argon-biology-capabilities-assessment/. Its text is identical to the existing substack row, so it is a mirror and gets no add.
- **What I did:** recorded it as `web_version`, following the GPT-6 Astra SecureBio row.

### #5 CVP v990
- **What changed:** CVP managed-service applications are now open, while customer-facing products are at the expression-of-interest stage only. Approval now has to be assigned to a workspace, role or account before it takes effect. Google Cloud access now requires the Advanced AI Safety Addendum and enabling data sharing.
- **Note:** this row's status is `moved` with no publication date. I didn't investigate this run.

## Phase A candidates (48 new today)

- **Proposed:** GPT-6.1 Terra addendum (#1), the ReproBAIT SecureBio and AISI posts (#2, #3), and the SecureBio Argon mirror as a related URL (#4).
- **Skipped:**
  - **UK AISI "Pretraining data filtering in open-weight biological models":** safeguard research on ESM-2 protein models AISI retrained itself. It doesn't evaluate a released named model, so it fails the system-card test.
  - **Anthropic S-1 filing:** corporate, not model documentation.
  - **Cursor Agent SDK (blog + changelog):** product launch.
  - **Tencent Hy-SimulMT-30B-A3B (+FP8/GGUF/Interleave):** machine translation, excluded by the tencent scope note.
  - **WeVisOne-VL discussions, DiagSafe dataset:** discussions and a dataset, not model documentation.
  - **NVIDIA (excluded by the nvidia scope note):**
    - llama-nv-embed-reasoning-3b is an embedding model.
    - MotionBricks is a motion-generation component, not GR00T.
    - The FLORA paper is a paper link.
    - The isaacsim-assets repo and its discussion are assets.
  - **inclusionAI:**
    - ZwZ-2B is a tiny 2B VLM outside the Ling/LLaDA lines.
    - The *-singprobe repos are probes on other labs' models.
  - **MiniMax discussions (3):** doc renames.
  - **Qwen:** the Qwen-Image-PE paper and the BlenderWorld discussion, neither of which is model documentation.
  - **Epoch "AI impacts observatory":** a topic hub.
  - **Redwood "A basic case for accelerating conceptual reasoning capabilities":** an essay.
  - **Profile pages:** the substack and HF author profiles.
- Everything first seen before today was triaged in earlier runs.

## Targeted search (10-24 to 10-27)

- **GPT-6.1 Terra:** proposed (#1).
- **Nanbeige4.3-33B (HF, 10-25):** Nanbeige is not on either allowlist. Skipped.
- **METR 10-20 review of Anthropic's August Risk Report:** already in DB (`metr-claude-mythos-5-independent-eval`). METR's 10-22 agent-monitoring red-team post is also in DB.
- **Restricted-access polling:** nothing new in the window.
  - CVP / Glasswing merge (10-06), LSVP and Claude Science are in DB.
  - The GPT-Rosalind and Daybreak news is older and already handled.
  - Searches turned up nothing new for Gemini for Science or CodeMender.

## Citation mining

- **Terra addendum:** cites the GPT-6 Astra card and GPT-6.1 Sol, both in DB.
- **ReproBAIT:** its only new reference is the arXiv preprint, recorded as `paper`.

## Blocked-URL escalations (task 5)

- **What Phase A reports:** all 16 openai.com / help.openai.com rows return 403 (streak 26; 21, 11 and 5 for the newer ones).
- **Spot check:** read_doc.py got HTTP 200 via browser_impersonation today on hugging-face-model-evaluation-security-incident, pacing-model-development-cyber-capabilities, the Daybreak TAC help article and trusted-access-for-cyber.
- **Conclusion:** all are alive, so there are no status changes.

## Document updates (task 6)

- **Top 5:** v773, v924, v573, v578 and v974 were all judged noise in earlier runs and were not re-read.
- **Beyond the top 5, read because they were fetched today:**
  - **anthropic-claude-opus-access-policy v990:** substantive, annotated (#5).
  - **inclusion-ai-llada2-2-flash-model-card v980:** the "coming soon" SGLang note was replaced with deploy instructions. That is usage docs, not results or terms, so it is skipped.
  - **inclusion-ai-ring-2-6-1t-model-card v979:** a code-snippet expansion, reordered eval widgets and a download count. Noise, skipped.

## Friction and proposals

- **Friction, two recurrences:**
  - The openai.com 403 false alarm (of 2026-10-26T06:29:40Z).
  - The stale updated_docs top-5 window (of 2026-10-24T06:21:27Z).
- **No new proposals.**
