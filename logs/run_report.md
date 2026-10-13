# cardtrack agent run — 2026-10-13 (run id 2026-10-13T06:20Z-local)

- **Lookback:** the last agent success was 2026-10-12T06:29:06Z, so the search used the 72 h minimum lookback (from 2026-10-10).
- **Weekly retrospective sweep:** not run (today is Tuesday).
- **Open issues:** `open_issues.json` has `fetch_ok: true` and no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (model_card) | Meta "Muse Wonder Model Card" (2026-10-12; Muse Wonder, Muse Wonder Full; closed; cbrn, cyber, loss_of_control) https://research.meta.ai/static/muse-wonder-model-card | **written** (`meta-muse-wonder-model-card`, doc 378, v815) |
| 2 | add (other) | Anthropic Frontier Red Team "AI models may be capable of self-replicating without access to a datacenter" (2026-10-12; GLM-5.2, Qwen3.5-9B, Gemma 4 26B A4B; loss_of_control) | **written** (`anthropic-glm-5-2-other`, doc 379, v816) |
| 3 | add (other) | OpenAI misalignment report "Obtaining public statistics with disallowed requests" (2026-10-09; internal research model; restricted; loss_of_control) | **written** (`openai-openai-internal-research-model-other-3`, doc 380, v817) |
| 4 | add (other) | OpenAI misalignment report "Sending disallowed web requests and reaching a public file service" (2026-10-09; internal research model; restricted; loss_of_control) | **written** (`openai-openai-internal-research-model-other-4`, doc 381, v818) |

Notes:

- **#1 Muse Wonder:** the PDF model card is linked as "our report" from the launch post; the launch post is recorded as its announcement.
  - It includes a Meta Superintelligence Scaling Framework risk assessment: high risk for Chem/Bio is not ruled out pre-mitigation, and cyber and loss-of-control are "moderate or lower".
  - It reports cyber, CBRN and LoC eval tables (CyberGym, ExploitGym, SecureBio, ABC Bench, BioTIER, MASK, Agentic Misalignment).
  - Openness is `closed`: Meta Model API, with Wonder Full for paid Muse Code subscribers.
  - The launch post says "a full report with additional safety evaluations will be available soon". That will be a separate document, so watch research.meta.ai.
- **#2 self-replication:** this is a measured evaluation of autonomous replication of named open-weight models on IoT and edge hardware. Only GLM-5.2 replicated reliably end to end.
  - It has the same report class as `anthropic-glm-5-3-other` and the catalogued Palisade self-replication report.
  - Openness was omitted because the licenses were not verified this run.
  - I did not tag `cyber`: the measured tasks are inference setup and replication, not exploitation.
- **#3 and #4 misalignment reports:** these are siblings of yesterday's add (#3 in the 10-12 report), posted the same day. Neither ever appeared in candidates; the search subagent found them. Both pages read "Report updated: Oct 9, 2026", and that date was used.

## Phase A candidates (152 listed)

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-12.
- **New today (first seen 10-13):**
  - research.meta.ai/blog/muse-wonder: led to #1. The blog post is not catalogued separately; it is the announcement for the PDF.
  - anthropic.com/research/self-replicating-ai: led to #2.
- **New today, skipped:**
  - anthropic.com/research/distillation-defenses: a post on anti-distillation safeguard methods and abuse metrics. It is not an assessment of a named model's capabilities or safety (GLM-5.3 is mentioned only in passing and is already covered by `anthropic-glm-5-3-other`).
  - aisi.gov.uk "Towards technical best practice for frontier AI development": a policy agenda with no named model.
  - RAND PEA5068-1 (recursive self-improvement, Expert Insights) and the RAND biosecurity Q&A: policy commentary. The RAND pagination link is index furniture.
  - x.ai/news/x-subscription: a product/subscription launch.
  - HF discussions (Qwen3.8-Flash-Next #74, DeepSeek-V4.1-Flash #34 and #48, GLM-5.3 #30, GLM-5.3-Flash #62, Ling-3.0-flash #19, Ling-3.0-flash-dspark #2, nvidia aisimulate dataset #17): community PRs, not documents.
  - HF user profiles (OzymandiasLiu, HvanAdelsberg), NVIDIA papers (2610.11291, 2610.11215) and the physical-ai collection: not model documentation.
  - nvidia/Qwen-Image-NVFP4: a quantized re-upload of a third-party model.
  - inclusionAI/LemonDecider: a 5B feature-extraction model. It is auxiliary, out of scope for inclusion_ai, and has no announcement.

## Targeted search (10-10 to 10-13)

A subagent swept the lab card indexes, deploymentsafety, misalignment-reports, the HF org lists, the evaluator blogs and the access-program list.

- **Leads:** #3 and #4.
- **Considered and skipped:**
  - Anthropic "Introducing the Anthropic Cyber Mission" (10-08): first seen in Phase A on 10-09 and triaged then. It names no specific model ("frontier Claude models"), and its Critical Infrastructure Defense Program is an interest form. The Cyber Verification Program page itself is already catalogued.
  - Microsoft-Decision-1 (Foundry GA 10-08): a decision-scoring model post-trained from Qwen3.5-9B. No canonical card URL was found, it has no safety evals, and it is a scorer rather than a general-purpose generative model. Not proposed.
- **Still pending:**
  - Meta's full Muse Wonder safety report: not yet published.
  - StepFun Step 5: not out (expected 10-15).
- **No in-window documents from:** gpt-rosalind-discovery, Daybreak, Glasswing/Mythos, LSVP, Claude Science or the Gemini science/cyber programs.

## Citation mining

- **Muse Wonder card:** cites the Claude Fable 5.1 and Opus 5.5 system cards (both present) and the Meta Superintelligence Scaling Framework (a framework, not a model document).
- **Self-replication post:** links the GLM-5.3 post, which is present.
- **OpenAI reports:** link only the misalignment-reports hub.

## Blocked-URL escalations (task 5)

- All 14 escalated openai.com/help.openai.com rows are treated as **alive**: 13 at streak 12, plus `openai-gpt-5-4-cyber-access-policy` at streak 7.
- I checked two today with read_doc.py, and both returned HTTP 200 via browser_impersonation:
  - accelerating-cyber-defense-ecosystem
  - the Daybreak trusted-access help article
- No status changes were proposed.

## Document updates (task 6)

None were annotated. No new entries were added to updated_docs.json since the 10-12 run (newest fetched_at is 10-11), and every queued diff was read and judged noise in earlier runs.

## Friction and proposals

- **Friction 1:** `recurrence` of 2026-10-06T06:29:51Z. The openai.com 403 streak is still a false alarm.
- **Friction 2:** `recurrence` of 2026-10-12T06:28:32Z. The misalignment-reports index is unwatched, and two more reports were missed for 4 days.
- **No new proposals:** adding that index URL and fixing the 403 false alarm are already filed in PROPOSALS.md.
