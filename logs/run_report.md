# cardtrack agent run — 2026-10-15 (run id 2026-10-15T06:17Z-local)

- **Lookback:** the last agent success was 2026-10-14T06:22:46Z, so the search used the 72 h minimum (2026-10-12 to 10-15).
- **Weekly retrospective sweep:** not run (today is Thursday).
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (model_card) | StepFun "Step 5 Preview — Model Card" (2026-10-15; open_weight_restrictive; no safety evals) https://huggingface.co/stepfun-ai/Step-5-Preview | **written** (`stepfun-step-5-preview-model-card`, doc 384, v847) |
| 2 | add (model_card) | inclusionAI "Ling-3.1-flash — Model Card" (2026-10-13; open_weight_permissive, MIT; no safety evals) https://huggingface.co/inclusionAI/Ling-3.1-flash | **written** (`inclusion-ai-ling-3-1-flash-model-card`, doc 385, v848) |

### #1 Step 5 Preview

- This is the open-weights release that earlier runs had been waiting for, announced for 10-15.
- The repo was an empty placeholder from the 09-20 API launch. HF `lastModified` is 2026-10-15.
- The model is a 600B/27B-active MoE with 1M context. The card has capability benchmarks and deployment recipes, and no safety content.
- **License:** StepFun Model License 1.0, "Apache-2.0-style with additional attribution and commercial-license conditions", so the row is `open_weight_restrictive`.
- **Notability:** StepFun's X launch post (recorded as `announcement`) and MarkTechPost coverage.
- The NVFP4 and BF16 repos are format variants and were not proposed. The third-party TypeSafeAI BF16 re-host flagged on 09-27 stays excluded.

### #2 Ling-3.1-flash

- The Phase A lead was HF repo creation on 10-13. The model is a 560B/25B-active hybrid-linear MoE that succeeds Ling-3.0-flash. The card has a capability evaluation section and no safety content.
- **License:** `license:mit` per the HF API, not gated.
- **Notability:** an API launch on 09-30 with wide independent coverage (OpenRouter, Dataconomy). There is no inclusionAI blog post.

## Phase A candidates

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-14.
- **New today (first seen 10-15):**
  - inclusionAI/Ling-3.1-flash led to #2.
  - stepfun-ai/Step-5-Preview-NVFP4 is a quant variant. It led to #1 through the base repo, which Phase A did not list (see Friction).
- **Skipped:**
  - **anthropic.com/news/2026-us-midterms:** an election-policy post. It reports a 99% political-evenhandedness score and a 0.002% election-violation rate across Claude 5.5 models. Election/policy updates are explicitly out of scope for `other`.
  - **anthropic.com/news/singapore-office-opening:** corporate news.
  - **research.meta.ai "Accelerating Scientific Research in Health Data Science With Muse Models" (10-14):** a capability showcase (10 manuscripts produced with Muse Spark 1.3 and Muse Wonder) with no model evaluation.
  - **x.ai/news/grok-voice-3 (10-14):** a product launch post. Its only content is an Artificial Analysis benchmark table and pricing. There is no model card (none found on data.x.ai) and no safety content. It is the first Grok Voice release seen, with no prior row to compare against.
  - **epoch.ai SpireClimb (Slay the Spire) benchmark launch:** a multi-model game-playing benchmark trend piece, not an evaluation of a specific model.

## Targeted search (10-12 to 10-15)

A subagent swept the lab indexes, the access-program list and the evaluator blogs. I verified each find myself.

- **New finds:**
  - #1 and #2 above.
  - **Irregular, "Assessing Gemini 4 Argon Against Offensive Security Benchmarks" (2026-10-13):**
    - I read it. Irregular ran Argon on CyScenarioBench as part of GDM's FSF assessment. Argon solved 12/12 scenarios end to end and passed 77/82 segments, against 5/12 for Gemini 3.8 Flash Cyber and 0/12 for Gemini 3.1 Pro.
    - It is squarely in scope, but **not proposable**: `irregular` is not on either allowlist. The allowlist fix was already proposed on 2026-09-09, so it was not re-filed. Logged as friction.
    - This corrects yesterday's note that no external Argon tester had published.
- **No new documents in window:**
  - OpenAI: the deployment-safety hub (latest 10-07) and misalignment reports. `gpt-rosalind-discovery` is still only on a pricing page.
  - Anthropic system cards (latest Haiku 5.5, 10-07) and the transparency hub.
  - Glasswing/Mythos and LSVP (no page newer than the 09-17 launch).
  - The 10-08 Cyber Mission post names no model, so it is not an access_policy.
  - GDM model cards (latest Argon, 10-13), Gemini for Science and CodeMender.
  - Mistral (Large 4 weights due end of October), Qwen, DeepSeek, Kimi, GLM, MiniMax, MiMo, Nemotron, Amazon and Microsoft.
  - UK AISI (no Argon report yet), CAISSI, METR (10-14 posts are methodology only), Apollo, Gray Swan, Palisade, FAR.AI, SecureBio, Epoch and RAND.
- **Still pending:**
  - Meta's full Muse Wonder safety report, still marked "available soon".
  - Mistral Large 4 weights.

## Citation mining

- **Today's two adds:** both are capability-only HF cards with no citations of predecessor cards or third-party evals.
- **Argon documents:** mined yesterday. Today's only new external Argon eval is Irregular's, which is not allowlisted.

## Blocked-URL escalations (task 5)

- All 14 openai.com/help.openai.com rows are treated as **alive**: 13 at streak 14, plus accelerating-cyber-defense-ecosystem at streak 9.
- I spot-checked two with read_doc.py, and both returned HTTP 200 via browser_impersonation:
  - accelerating-cyber-defense-ecosystem
  - the Daybreak help article
- No status changes were proposed.

## Document updates (task 6)

None were annotated.

- **New since the last run:**
  - **tencent-hunyuan-hy3 v840:** noise. It is a reordered HF eval-results widget, a download counter, and a sample-code `max_new_tokens` change.
  - **mistral-medium-3-5 v837:** noise. It removes a duplicated pricing/context furniture block.
- **Older queued diffs:** all were judged noise in earlier runs.

## Friction and proposals

- **Friction, three entries:**
  - a `recurrence` of 2026-10-06T06:29:51Z: the openai.com 403 false alarm, now at 14 runs.
  - `other`: the Irregular Argon eval was blocked by the allowlist.
  - `index_gap`: Phase A never listed the Step 5 base card, because the HF createdAt index misses placeholder repos that are filled later.
- **New proposal:** "HF index misses placeholder repos that are filled after creation (sort by lastModified too)".
- **HF rate limiting:** HF returned 429 to both read_doc.py and WebFetch early in the run (probably because a subagent was fetching at the same time). It cleared within minutes, and both proposals passed retrievability on the first try. No friction was logged.
