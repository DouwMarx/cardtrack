# cardtrack agent run — 2026-09-30 (run id 2026-09-30T07:35Z-local)

Last agent success: 2026-09-29T07:55:49Z. The search window used the 72 h minimum lookback (from 2026-09-27).
Today is Wednesday, so there was no weekly retrospective sweep. There were no open issues.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (addendum) | OpenAI, "Addendum to GPT-6 Astra System Card: GPT-6.1 Sol" (deploymentsafety.openai.com/gpt-6-1-sol/gpt-6-1-sol.pdf, 2026-09-29) | **written**, `openai-gpt-6-1-sol-addendum` (doc 356, v707) |
| 2 | add (other) | Anthropic Frontier Red Team, "GLM-5.3 and the spread of advanced cyber capabilities" (2026-09-29) | **written**, `anthropic-glm-5-3-other` (doc 357, v708) |

Notes:
- **GPT-6.1 Sol.** I read the PDF cover and TOC directly. The PDF is the canonical URL; the deploymentsafety web page (web_version) and the openai.com launch post (announcement) are in related_urls.
  - openness `closed`: public API as `gpt-6.1-sol`.
  - risk_domains: cbrn, cyber and loss_of_control (Preparedness bio/chem, cyber and AI self-improvement; monitorability; alignment), plus societal_harm (U18 and mental-health evals).
  - A hashed CDN copy exists at cdn.openai.com/pdf/38e3efcf…/oai_GPT_6_1_Sol.pdf. I did not use it, because the stable URL is preferred.
- **GLM-5.3 cyber report.** This is a quantitative eval of a named third-party model: ExploitBench, an OSS-Fuzz exploitation benchmark, zero-day discovery, and safeguard-bypass/refusal benchmarks.
  - I used doc_type `other` because Anthropic is a lab, not an allowlisted evaluator. risk_domains: cyber.
  - openness is omitted: the GLM-5.3 license is a custom "glm-5.3" license I could not classify.

## Phase A candidates triaged

These are the new since last run (first_seen ≥ 2026-09-29):
- Proposed: deploymentsafety.openai.com/gpt-6-1-sol (#1), anthropic.com/research/glm-5-3-… (#2).
- Already in the database:
  - anthropic.com/claude-sonnet-5-5 (related URL of `anthropic-claude-sonnet-5-5-system-card`)
  - aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks… (related URL of `uk-aisi-gpt-6-astra-independent-eval`)
  - huggingface.co/papers/2609.25611, the Qwen3.8-Omni report (canonical of `alibaba-qwen-qwen3-8-omni-flash-model-card`)
- Skipped as out of scope:
  - anthropic.com/research/your-thoughts-on-ai: a societal-impacts survey, not a model eval.
  - mistral.ai/news/hallo-deutschland (both variants): a company office announcement.
  - mistral.ai/products/ai-cloud: a product page.
  - x.ai/news/team-bots: a product launch without documentation.
- Skipped as HF noise: user profiles (Svard, huaXiaKyrie, kailinjiang, KBlueLeaf, anwithkiran, chenmouxiang, alibaba-qwen, DVA13304, qingpei, whatseeker, Andyson, CFC); dataset discussions; Nemotron-RL datasets; and research papers that only use models (Draft-KV, Just MLPs, AdaTutoRank, TT-VidT, QwenGyre, OPD, reward-model alignment, Groupwise Agentic Grading, LongLive-Plug, Hindsight-Divergence).
- Skipped under the auxiliary-model rule (tabular/relational/medical-imaging/climate models, no safety evals): nvidia/Kumo-Tabular, Kumo-Relational, the Kumo blog post, NV-Generate-CT and cbottle.
- Skipped as a discussion thread: the Ling-3.0-flash-VL context-length discussion. It is not a document; the model card is the unit.
- Skipped on scope and notability grounds: inclusionAI/Ming-flash-omni-2.0. It is an MIT omni model released 2026-02-11, but the Ming line is not in the inclusion_ai scope note and I found no external announcement. Logged to friction.
- Older candidates (first_seen before 2026-09-29) were triaged by earlier runs and not re-reviewed.

## Targeted web search (window 2026-09-27 → now)

- **Queries:**
  - General: "system card September 2026"; "OpenAI DevDay 2026 system card addendum Codex"; open-weight model cards for Sep 28–29; "Gemini model card September 2026"; DeepSeek/Kimi/MiniMax/Grok technical reports.
  - Access programs: trusted/vetted access programs; LSVP/CVP/Mythos.
  - Third-party evals: AISI/CAISI/METR/Apollo on GPT-6.1 Sol and Sonnet 5.5; pre-deployment eval reports from Irregular, Apollo, Epoch and SecureBio.
- **Already in the database:** Claude Sonnet 5.5 system card, LSVP page, Claude Mythos page, Fairwind program, OpenAI TAC scaling post, Grok 4.7 card, Gemini 3.8 Audio card, MiMo-V2.6.
- **New:** only GPT-6.1 Sol, already proposed from Phase A.
- **Not yet published:** no third-party (METR/Apollo/UK AISI/SecureBio) reports for GPT-6.1 Sol or Sonnet 5.5, although the Sonnet 5.5 card credits UK AISI and Apollo as external testers. Worth re-checking in the next few days.
- **Silent-org check (>14 days):** not done systematically. I could not aggregate newest-entry dates per publisher with the permitted tools (friction logged).

## Citation mining

- GPT-6.1 Sol addendum: names no external evaluators.
- GLM-5.3 cyber report: related work (US CAISI GLM-5.3 eval, Z.ai card) is already catalogued.
- Sonnet 5.5 card: external testers have not published yet (see above).

## Open issues

None (`open_issues.json` is empty).

## Blocked-URL escalations

- `openai-gpt-rosalind-access-policy-3` (openai.com/index/introducing-new-capabilities-to-gpt-rosalind/): the agent fetch also returns 403. The page is still indexed by search under its original title and is cited by third-party coverage and OpenAI's X post, so it is **alive and bot-blocked** (openai.com blocks automated fetchers). No status change was proposed.

## Document update summaries

No annotate_version proposals. I read 8 diffs and all were extraction noise:
- poolside-laguna-xs-2-1 v706, xiaomi-mimo-v2-6-pro v687: download counts / Spaces count / eval-widget reorder.
- alibaba-qwen-qwen3-8-flash-next v705: the same, plus the GPQA widget value rendering.
- nvidia-gr00t-h v703: HF "how to use" widget and download count.
- anthropic-claude-fable-5-addendum v680, anthropic-claude-sonnet-4-5-other-2 v695, anthropic-claude-mythos-preview-other-9 v682, anthropic-claude-opus-4-1-other v696: rotating "Related content" teasers and a dropped date line.

The other 12 queued entries were not opened:
- nvidia-cosmos-h-surgical-simulator v704 and tencent-hunyuan-hy-world-2-0 v702 have the same +1/-7 shape as the GR00T-H HF widget diff.
- The remaining 10 are anthropic-*-other rows with the same +4/-3 related-content shape.

## Friction / proposals

- 3 friction lines appended: Anthropic related-content diff churn, the Ming-flash-omni scope ambiguity, and the missing per-publisher recency aggregate plus the heredoc sandbox refusal.
- No new PROPOSALS.md entry: the diff-churn issue is already covered by the 2026-09-07 entry.
