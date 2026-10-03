# cardtrack agent run — 2026-10-03 (run id 2026-10-03T06:18Z-local)

The last agent success was 2026-10-02T06:21:44Z, so the search window used the 72 h minimum lookback (from 2026-09-30).
Today is Saturday, so there was no weekly retrospective sweep. There were no open issues and no blocked-URL escalations.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | annotate_version | `openai-gpt-6-astra-system-card` v720 | **written** (doc 283) |
| 2 | annotate_version | `metr-claude-opus-4-6-independent-eval-4` v725 | **written** (doc 73) |
| 3 | add | Gemini 4 Argon Model Evaluation PDF (google_deepmind, `other`, restricted) | **written**: `google-deepmind-gemini-4-argon-other` (doc 360) |
| 4 | add | OpenAI misalignment report "Preparing for a restart after reading Slack" (HPIM, `other`, restricted, loss_of_control) | **written**: `openai-hpim-openai-highly-persistent-internal-model-other-2` (doc 361) |
| 5 | add | Upstage "Solar Pro 4" launch documentation (`model_card`, closed) | **written**: `upstage-solar-pro-4-model-card` (doc 362) |

Notes:
- **#1:** the 2026-09-29 revision adds Appendix B "dots", covering the always-on agents built on GPT-6 Astra. It includes:
  - prompt-injection red-teaming: no scored successes in 100 bulk rollouts or in 2,638 iterative attempts;
  - alignment results across simulated-time budgets;
  - monitor-evasion tests, plus preparedness and safeguards sections.

  I verified it on the live deploymentsafety page. Dots is a product harness on the existing model, so it gets no separate row.
- **#2:** the METR page now carries a section "Results from the Exercise (added May 2026)". It quotes the Frontier Risk Report findings, including the 59% best score on the attack-ideation eval. Verified live.
- **#3:** this is a 5-page first-party evaluation document: methodology plus a results table against GPT-6 Astra, Fable 5.1 and Opus 5.5 on 18 benchmarks.
  - Location: `deepmind.google/models/evals-methodology/gemini-4-argon` redirects to the PDF.
  - Date: coverage on 2026-09-30 cites it, so it shipped at launch.
  - It has capability benchmarks only, so `has_safety_evals` is false.
  - Precedent: Meta's Muse Spark evaluation-methodology rows.
  - Still no Argon model card.
- **#4:** HPIM is a recurring named identity with 3 existing rows, so this passes the named-model gate under either reading.
- **#5:** Solar Pro 4 launched 2026-08-11, before Upstage joined the allowlist (OpenRouter overlay, 2026-09-22, no index_urls). Precedent for a launch post serving as the model card: `mistral-robostral-navigate-model-card`.

## Phase A candidates triaged (22)

All skipped:
- **Already triaged on 2026-10-02 and still skipped:** claude-shaped-science (guest essay), Barclays (customer story), AISI secure-evaluation-environment (infrastructure, no named-model results), Epoch ChatGPT usage explorer, NVIDIA PixelUMM and PixelDiT2, 4 HF paper pages, 3 HF user profiles, and the DeepSeek-V4.1-Flash chat-template discussion.
- **Sonnet 5.5 System Card PDF** (www-cdn): already in the related_urls of `anthropic-claude-sonnet-5-5-system-card`.
- **arxiv 2503.03750 (MASK):** a 2025 benchmark paper cited on Anthropic's model-report page. It predates the scope floor and is not an Anthropic publication.
- **anthropic.com/news/claude-frontier-academy:** a training-investment announcement.
- **Meta "Developing Capable Models Responsibly"** (2026-10-02): an update to the Meta Superintelligence Scaling Framework (containment during training and evaluation; CBRN proliferation framing). It names no model, so it is a generic framework/policy update and fails the named-model gate.
- **Meta "Solving Open Research Problems Together"** (2026-10-02): a math-collaboration showcase using Muse Spark 1.1/1.2, with no evaluation.
- **x.ai/changelog/bot:** a changelog page.
- **Epoch "estimating the agent population"** (2026-10-02): a hardware-capacity economics estimate with no model evaluation.
- **RAND RRA5050-1** (data-center siting): outside RAND's CAST/Canary scope.
- **Redwood "Capabilities research expands the safety-usefulness Pareto frontier"**: a conceptual essay.

## Targeted web search (window 2026-09-30 → now)

- **Queries:**
  - System card and open-weight model card releases for October 2026.
  - Gemini 4 Argon model card / evals methodology.
  - OpenAI dots and the GPT-6.1 Astra withholding; OpenAI's Australia incident.
  - Anthropic enzyme discovery.
  - Ai2 Olmo-core 3.
  - Trusted/restricted access programs (LSVP, CVP, Glasswing, Rosalind, Daybreak, Gemini for Science, Claude Science).
  - METR, Apollo and AISI evaluations; the OpenAI misalignment-report hub.
  - Lab sweeps: Mistral, Qwen, DeepSeek, GLM, Kimi, MiniMax, xAI, NVIDIA, Upstage, StepFun, Tencent and inclusionAI.
- **Added:** #3, #4 and #5 above.
- **Skipped:**
  - Two other 2026-10-02 OpenAI misalignment reports (EDA host, reference-tool command injection). They name only an unnamed internal model; the gate is still unresolved (PROPOSALS 2026-09-29).
  - Apollo posts from 2026-09-30 and 2026-10-01 (embedded-evaluation principles, scheming-propensity framework, Senate testimony): frameworks with no named-model results.
  - Anthropic "Claude discovers a novel enzyme system": a capability showcase, not an evaluation.
  - Olmo-core 3: training infrastructure from Ai2, which is not allowlisted.
  - MiniMax M3.1-Flash-Preview: no card, weights or benchmarks.
  - Upstage Solar Mini 4 (2026-09-22): no fetchable first-party documentation; logged.
  - Solar Decide/Jev: a decision endpoint, i.e. an auxiliary model.
  - No Ling-3.1 repo exists on the inclusionAI HF org.
- **Not readable (openai.com 403):**
  - "How we will do better for Australia": per coverage the model is unnamed.
  - "Daybreak for Frontline Defenders" (2026-09-03): coverage names only tiers, no model.
  - GPT-6.1 Astra withholding: press only, no first-party document found.

  All three are logged in friction.
- **Access programs:** nothing new. LSVP and Glasswing are catalogued; CVP Mythos access is still "near future"; GPT-Rosalind pricing takes effect 2026-10-05 (not a new document).
- **Silent orgs:** I spot-checked Upstage (found Solar Pro 4), MiniMax, NVIDIA, Tencent (Hy4 preview already catalogued), StepFun and inclusionAI. Palisade, Poolside, Apollo, Moonshot and Thinking Machines were checked yesterday or today, with nothing new.

## Citation mining

New rows this run:
- The Argon evaluation PDF cites only public leaderboards and competitor system cards, which are already catalogued.
- The HPIM report links only to the hub.
- The Solar Pro 4 post cites Solar Open 2, which is catalogued.

No new leads.

## Open issues

None.

## Blocked-URL escalations

None.

## Document update summaries

I read the 6 newly queued diffs and annotated 2 (#1, #2). Skipped as noise:
- **alibaba-qwen-qwen-image-2-1 v724:** a feedback-form blurb plus download count.
- **xiaomi-mimo-v2-6-pro v723:** HF widget, Spaces count and leaderboard reorder.
- **nvidia-cosmos-h-dreams v722:** the HF "use this model" boilerplate was removed and the download count changed.
- **anthropic-claude-mythos-preview-access-policy-2 v721:** only the "Related content" sidebar rotated.

The older queued entries were reviewed in earlier runs.

## Friction / proposals

- 4 friction lines:
  - Argon has an evaluation PDF but still no model card.
  - The named-model gate is still unresolved; there are now 7 skipped reports.
  - openai.com is blocked to my fetcher, which left 3 leads unread.
  - Solar Mini 4 and MiniMax M3.1 have no documentation.
- 1 PROPOSALS entry: publishers from the OpenRouter overlay join with empty index_urls and no backfill. Solar Pro 4 went 7 weeks unseen. The entry suggests a one-off backfill search when a publisher is added, and seeding index_urls.
