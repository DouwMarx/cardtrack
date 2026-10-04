# cardtrack agent run — 2026-10-04 (run id 2026-10-04T06:19Z-local)

The last agent success was 2026-10-03T06:27:35Z, so the search window used the 72 h minimum lookback (from 2026-10-01).
Today is Sunday, so there was no weekly retrospective sweep. There were no open issues.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add | Cursor's copy of "Model Card: Grok 4.7" (`cursor`, `model_card`, closed; cbrn, cyber, harmful_manipulation, societal_harm) | **written**: `cursor-grok-4-7-model-card` (doc 363) |
| 2 | add | Anthropic "Improving our alignment and security efforts" (2026-08-31, `other`, restricted, loss_of_control) | **duplicate**: fingerprint already stored as `anthropic-claude-mythos-5-other-3` |

Notes:
- **#1:** I found this by checking the Cursor co-publication pattern from the existing Cursor rows for Grok 4.5 and 4.6.
  - The PDF at `cursor.com/resources/grok-4-7-model-card.pdf` is dated September 21, 2026 (revision 2026-09-21).
  - Its counterpart row is `xai-grok-4-7-model-card`, and the notes say so.
  - I submitted it through CLI flags because stdin JSON is blocked (see friction). As a result, `related_urls` (co_published and announcement) were not set.
- **#2:** I found the lead in a related-content sidebar. Its URL is not in state_summary, but the validator matched the content to an existing row. I accept that verdict.

## Phase A candidates (23): none proposed

- **Claude Sonnet 5.5 System Card PDF:** already the `full_document` related URL of `anthropic-claude-sonnet-5-5-system-card`. Skipped.
- **anthropic.com "Claude-shaped science":** a guest science essay with no evaluation or access program. Skipped.
- **Barclays, Claude Frontier Academy:** corporate announcements. Skipped.
- **arXiv MASK (2503.03750):** a 2025 benchmark paper, below the scope floor and not an Anthropic publication. Skipped.
- **Meta "Developing Capable Models Responsibly":** an update to the scaling-framework policy that names no model. Skipped.
- **Meta "Solving Open Research Problems Together":** a math-collaboration showcase with Muse Spark and no evals. Skipped.
- **UK AISI "Building a more secure environment…":** an infrastructure/methodology blog with no model results. Skipped.
- **Redwood "Capabilities research expands the safety-usefulness Pareto frontier":** a general essay. Skipped.
- **Epoch ChatGPT usage explorer and agent-population estimate; RAND data-center siting:** not model documentation. Skipped.
- **xAI changelog:** navigation link. Skipped.
- **HF leads:**
  - DeepSeek V4.1-Flash chat-template discussion: already cataloged as `deepseek-deepseek-v4-1-flash-model-card`.
  - Papers and user pages: skipped.
  - NVIDIA PixelUMM and PixelDiT2-ImageNet: research checkpoints outside NVIDIA's scope note (Nemotron/Cosmos/GR00T only). Skipped.

## Targeted search (since 2026-10-01)

These were all checked and were already cataloged:

- **Recent launches:** GPT-6.1 Sol addendum; Sonnet 5.5 system card; Gemini 4 Argon (access policy, Fairwind, evaluation PDF); Grok 4.7 xAI card.
- **Access programs:** Mythos 5.1 / LSVP; Glasswing; Claude Science; "Expanding support for scientists"; Rosalind Biodefense; Path to Astra.
- **Muse Spark:** all reports.
- **Model cards:** Inkling and Inkling-Small; GLM-5.3; Laguna S 2.1; DeepSeek V4.1-Flash.
- **Sidebar leads:** Project Pilot / Drone-Bench; discovering-cryptographic-weaknesses; intelligence-targeting / conventional-weapons; the cyber-eval incident assessments.

Other findings:

- There is still no Gemini 4 Argon model card: `deepmind.google/models/model-cards/gemini-4-argon/` returns 404.
- I found no METR report on the Anthropic incidents yet. The investigation's initial term is 8 weeks from early September.
- The Apollo blog "Embedded evaluators are necessary…" (2026-09-29) is a policy essay that evaluates no model. Skipped.
- **Silent >14 days (checked):** Palisade, Poolside, Apollo, Moonshot, Thinking Machines, Mistral, MiniMax, NVIDIA, Z.ai. I found no uncatalogued first-party documents.
  - Kimi K3.1: still no card.
  - The Mistral "Magistral 1.2 (2509)" hits are 2025 releases, below the scope floor.

## Blocked-URL escalations (13 openai.com / help.openai.com)

- WebFetch still gets 403 on these URLs. I spot-checked `introducing-gpt-rosalind` and the Daybreak help article.
- Search engines still index the pages with current titles (Path to Astra, Rosalind Biodefense, etc.), so they are alive behind a bot wall.
- No `status_change` proposed.

## Document updates (summarized none)

I reviewed 12 diffs: v736, v735, v734, v733, v732, v731, v730, v729, v724, v723, v722, v721. They were all extraction noise:

- HF download/Spaces counters and reordered eval-result widgets (Qwen3.5-397B, Qwen3.8-2.4T, Qwen-Image-2.1 feedback blurb, MiMo-V2.6-Pro, Cosmos-H-Dreams snippet panel);
- Anthropic "Related content" sidebar rotation;
- dropped dateline strings on Anthropic research pages.

No annotate_version proposals were made. I did not open the 7 older entries (v705–v717).

## Friction / proposals

I added 3 friction lines:

- openai.com is still bot-blocked;
- the `--json -` stdin path is blocked by the Bash permission check, and the CLI flags cannot set `related_urls`;
- a URL-based dedup lookup missed a fingerprint duplicate.

No new PROPOSALS.md entry.
