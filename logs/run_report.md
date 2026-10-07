# cardtrack agent run — 2026-10-07 (run id 2026-10-07T06:16Z-local)

- Last agent success was 2026-10-06T06:30:41Z, so the search used the 72 h minimum lookback (from 2026-10-04). Yesterday's run had already searched broadly through 10-06, so today's search focused on 10-06/07 releases plus a silent-org sweep (publications since 2026-09-20).
- Wednesday: the weekly retrospective sweep did not run.
- `open_issues.json`: `fetch_ok: true`, no open issues. Task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add `access_policy` | Anthropic "Expanding the Cyber Verification Program" (2026-10-06) | **written**: `anthropic-claude-opus-5-5-access-policy` (doc 367, v767) |
| 2 | add `model_card` | Google DeepMind Nano Banana 2.1 model card (2026-10-06) | **written**: `google-deepmind-nano-banana-2-1-model-card` (doc 368, v768) |
| 3 | add `model_card` | Mistral "Introducing Mistral Large 4" (2026-10-06) | **written**: `mistral-mistral-large-4-model-card` (doc 369, v769) |
| 4 | add `model_card` | Upstage "Solar Mini 4" blog (2026-09-23) | **written**: `upstage-solar-mini-4-model-card` (doc 370, v770) |
| 5 | field_update `related_urls` | doc 367: CVP Help Center overview + CVP security requirements (both `other`) | **written** |
| 6 | field_update `model_names` | `anthropic-claude-opus-access-policy`: + Opus 5.5, Sonnet 5.5, Mythos 5.1 | **written** |
| 7 | field_update `openness` → `restricted` | `anthropic-claude-opus-access-policy` (now names Mythos 5.1) | **written** |
| 8 | annotate_version | `mistral-leanstral-1-5-model-card` v753 (Public Preview → Deprecated, deprecation date 9/29/2026) | **written** |
| 9 | annotate_version | `palisade-research-gpt-5-4-independent-eval` v618 (redirect stub → report text at /research) | **written** |
| 10 | annotate_version | `palisade-research-grok-4-grok-4-0709-independent-eval` v619 (same) | **written** |

Notes:

- **#1 CVP expansion.**
  - Three vetted tiers: Defense, Red Team and Specialized. Specialized is reviewed with the US government, and Glasswing members move into it.
  - Names Opus 5.5, Sonnet 5.5 and Mythos 5.1, so it is `restricted`.
  - Tagged `cyber`, with `has_safety_evals: true`. The post reports a CyScenarioBench safeguard test per tier: every task blocked without CVP; 46/50 trials blocked in Defense; 34/50 completed with no blocks in Red Team, vs 67.6% with no safeguards.
  - The validator named the slug after the first model.
- **#2 Nano Banana 2.1.**
  - Image-generation card built on Gemini 3.6 Flash.
  - Safety content: human red-teaming results (child-safety launch thresholds met) and a Frontier Safety assessment that relies on the Gemini 3.1 Pro / 3.7 Flash evals. Tagged `societal_harm` for the child-safety red-team; this is a light tag.
  - The page says "Published: October 2026"; the day comes from the 10-06 launch coverage. `closed`.
- **#3 Mistral Large 4.**
  - The announcement is the canonical URL because the docs page (`docs.mistral.ai/models/mistral-large-4-0`, in related_urls) has only specs and pricing. This follows the Robostral Navigate precedent.
  - Reports Cybench 93% and an 82% vulnerability reproduce-and-patch result, so tagged `cyber`. Red-teaming with vetted partners at reduced moderation is mentioned, but no results are given.
  - Weights are due at the end of October. `closed` for now; the notes ask for a re-check once the weights license is verifiable.
- **#4 Solar Mini 4.** Found by the silent-org sweep; Upstage is an OpenRouter-overlay publisher. The blog is the card, as with Solar Pro 4. Capability benchmarks only, `has_safety_evals: false`, `closed`. The date is from Artificial Analysis and press.
- **#6/#7.** Help Center article 14604842 (row 304, status `moved`) has been renamed "Cyber Verification Program" and now covers the three tiers for the 5.5 / Mythos 5.1 models.

## Phase A candidates (67)

- **Already triaged in earlier runs:** items first seen 10-02 to 10-06, including corporate news, HF papers/user pages, NVIDIA PixelUMM/PixelDiT2, Epoch/RAND non-model items, the Meta posts, the xAI changelog, Mistral navigation links, Campus/Frontier Academy, the Redwood items and the Apollo testimony.
  - The Sonnet 5.5 PDF is already a related_url of `anthropic-claude-sonnet-5-5-system-card`.
  - Palisade /research links: only self-replication (2026-05-07) and robot shutdown resistance (2026-02-12) are on or after the floor. Both are catalogued. I re-checked the dates of all 13 others today; all are 2023–2025.
  - inclusionAI/AI-Transparency (EU Art. 53(1)(d) training-content summaries): skipped again, not a card or eval.
- **New today:**
  - CVP: #1.
  - Nano Banana 2.1: #2.
  - Mistral Large 4: #3.
  - EmbeddingGemma 2 blog and model card: skipped, embeddings are auxiliary.
  - Cursor "Remote control for local agents": product changelog, skipped.
  - METR "AI systems could cover up misbehavior" (10-06): skipped. It is a proof-of-concept XSS in the Inspect transcript viewer, not an evaluation of a named model.
  - Epoch semiconductor / Chinese AI revenue publications: not model evals, skipped.
- **Also skipped:**
  - "Claude-shaped science" (guest essay on BootLoops; evaluates no model).
  - UK AISI "Building a more secure environment for evaluating dangerous capabilities" (evaluation-infrastructure security; no named model).
  - Meta "Developing Capable Models Responsibly" (Superintelligence Scaling Framework update; no named model).

## Targeted search

- **Searches run:**
  - Generic searches: system cards, model releases on 10-06, AISI reports, OpenAI system cards.
  - Program polls: LSVP, Claude Science, Gemini for Science, GPT-Rosalind, CVP.
  - METR/Apollo evals of Opus 5.5 / GPT-6.1 Sol.
  - A subagent sweep of 24 orgs whose newest row is older than about 14 days (Chinese open-weight labs, xAI, Meta, Thinking Machines, poolside, Upstage, Apollo, Transluce, SaferAI, FAR.AI, SecureBio, RAND, CAISI, Epoch, Palisade).
- **Already catalogued:** GPT-6.1 Sol, GPT-6 Luna/Sol, Grok 4.7, MiMo-V2.6, Opus/Sonnet 5.5, the METR Opus 5.5 report, all the GPT-Rosalind rows (GA pricing 10-05 is press-only) and LSVP. No LSVP expansion or new program page was found.
- **Found but not proposed:**
  - **StepFun Step 5 Preview** (2026-09-20): the only primary doc is an 850-character Chinese platform guide covering capabilities and how to connect, with no results. StepFun says weights ship 2026-10-15. Watch for the HF card then and propose that.
  - **InclusionAI Ling-3.1-flash** (09-30): no primary card. The HF repo returns 401, and it is API-trial only, with open source promised after a two-week trial. Hold.
  - **Moonshot Kimi K2.8 Preview** (09-11): only a Kimi Code changelog entry. No card, blog or weights.
  - **Transluce "Early rogue AI agent activity… on urlquery.net"** (~09-23): an incident report on an unnamed OpenAI agent swarm. It names no model, so it fails the named-model gate. This class is already the subject of the 2026-09-29 proposal, so it is not re-filed.
  - MiniMax-M3.1-Flash-Preview: no model card. GLM-5.3-FlashX: same weights as GLM-5.3-Flash. Hy Image 3.5 preview: not investigated beyond the sweep; low priority.
- **No new documents:** DeepSeek, Z.ai, NVIDIA, Meta, Thinking Machines, poolside, Apollo, SaferAI, FAR.AI, SecureBio, RAND, CAISI (rebranded CAISSI), Epoch, Palisade.

## Citation mining

- The CVP post links its Help Center tier details. I read both Help Center pages and added them as related_urls (#5). The overview article was already row 304, so I updated it instead (#6, #7).
- Nano Banana 2.1 cites the Gemini 3.6 Flash, 3.7 Flash and 3.1 Pro cards, all already catalogued.
- Mistral Large 4 cites Artificial Analysis and Cybench, which are third-party benchmarks rather than evaluator reports.

## Blocked-URL escalations (task 5)

- All 13 escalated openai.com / help.openai.com rows (streak 6), plus `openai-gpt-5-4-cyber-access-policy` (streak 1), are **alive**.
- `read_doc.py` returned HTTP 200 via browser_impersonation for path-to-astra, accelerating-cyber-defense-ecosystem and the Daybreak help article.
- No status changes were proposed.
- This is a monitor false alarm, the second run in a row: logged as `recurrence`, and a proposal was filed (below).

## Document updates (task 6)

I took the top 5 by substantive_lines:

1. `deepseek-deepseek-v4-pro-model-card` v573: **noise**. HF code-snippet widgets switched chat→completions examples, the download count changed, and leaderboard widget rows were reordered. Skipped.
2. `deepseek-deepseek-v4-flash-0731-model-card` v578: **noise** (same widget churn, download/Spaces counts). Skipped.
3. `mistral-leanstral-1-5-model-card` v753: substantive, the model was deprecated. Annotated (#8). The page is still live, so no status change.
4. `palisade-research-gpt-5-4-independent-eval` v618: a redirect stub replaced by the real page text after the /blog→/research move. Annotated as a capture artifact, not a revision (#9).
5. `palisade-research-grok-4-grok-4-0709-independent-eval` v619: same (#10). The stub versions (v508/v509) predate the current queue. The 2026-09-06 proposal on redirect stubs already covers this, so it is not re-filed.

## Friction and proposals

- Friction: `recurrence` of 2026-10-06T06:29:51Z (Phase A reports live openai.com pages as 403).
- Proposal filed: "Phase A's per-document check reports openai.com rows as 403 that the pipeline's own impersonation fetcher reads fine". The monitor should take the impersonation fallback before counting a block streak. Today these rows also never get new versions.
