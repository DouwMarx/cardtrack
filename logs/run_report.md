# cardtrack run 2026-09-15T08:11Z-local

Corpus at start: 311 documents. Written this run: **3 adds, 5 version annotations**.
No status changes, no field updates, no issue comments.

Phase A:

```
{"checked": 279, "ok": 266, "not_found": 0, "blocked": 12, "errors": 1, "moved": 1,
 "marked_dead": 0, "fingerprint_checked": 42, "new_versions": 5, "candidates": 243,
 "budget_exhausted": false, "candidates_new": 29, "updated_docs": 20}
```

Thirteen fetch failures and one move, none of them escalated to me — see §5.

## 1. Phase A candidate triage

29 new links (`first_seen` 2026-09-15T08:15:10Z). Three were proposed, all three written.
The 214-link backlog was triaged in full by the 2026-09-13 and 2026-09-14 runs and nothing
in it has changed status; I did not re-triage it.

**Proposed:**

| lead | publisher | verdict |
|---|---|---|
| `securebio.substack.com/p/securebio-gpt-6-astra-pre-release` | securebio | `written` — doc 312, `securebio-gpt-6-astra-independent-eval` |
| `far.ai/blog/jailbreaking-alibaba-qoders-cyber-safeguards` | far_ai | `written` — doc 313, `far-ai-qwen3-8-max-independent-eval` |
| `huggingface.co/papers/2609.12945` (StepAudio 3 Gen) | stepfun | `written` — doc 314, `stepfun-stepaudio-3-gen-model-card` |

**Could not triage (1):** `rand.org/pubs/research_reports/RRA5112-1.html`, *Open-Weight AI Models
May Increase Biological Misuse Risks*, from the Project Canary index. On its face this is exactly
the kind of document the corpus is for. `rand.org` returns 403 to my fetcher on every path I tried
and no search engine surfaces the report. I proposed nothing rather than attest criteria I could
not verify. Escalated in §8 — **this one needs an operator fetch.**

**Skipped (25):**

| lead(s) | publisher | reason |
|---|---|---|
| `huggingface.co/kekekeke`, `/Aragonaa`, `/dibyajyotic` | tencent, nvidia | HF user profiles, not documents |
| `tencent/WeMM-Embedding-2B` discussion | tencent_hunyuan | embeddings — excluded by the `tencent_hunyuan` scope note |
| `papers/2609.13141` (SAS) + `tencent/Simple-Attention-Sparsification` | tencent_hunyuan | an attention-sparsification method, no generative model released |
| `nvidia/Muse-Glimmer-30B-NVFP4` (+ its discussion) | nvidia | NVFP4 quantization of Meta's Muse Glimmer 30B, already doc `meta-muse-glimmer-model-card`; quantization variants fail `distinct_model_release` |
| `datasets/nvidia/compute-eval`, `datasets/nvidia/earth2studio-assets` discussion | nvidia | datasets, and the latter is weather-model scorecards — auxiliary under the `nvidia` scope note |
| `papers/2609.13287` (LLaDA-UI) | inclusion_ai | the paper for doc 310, whose `related_urls` already carry the same paper as a GitHub PDF; not a new document. See the note below |
| 11 × `inclusionAI/*-singprobe` repos | inclusion_ai | probe artifacts (2–10 MB) attached to third-party base models (Qwen, Gemma, Llama, Step); "guardrail classifiers, tiny size variants" are excluded by the `inclusion_ai` scope note, and they carry no announcement, no evals and no notability outside the HF org page |
| `epoch.ai/data-insights/near-daily-ai-use-doubled` | epoch_ai | AI-adoption survey statistics (8% → 19% of US adults), not documentation of a named model. Consistent with the 09-14 skip of the AI Chip Users Explorer |
| `securebio.org/blog/gpt-6-astra-pre-release-testing-report/` | securebio | same-publisher copy of doc 312; recorded as a `related_url` rather than catalogued twice |
| `securebio.org/fcoi-policy` | securebio | org conflict-of-interest policy, names no model |
| `huggingface.co/spaces/stepfun-ai/StepAudio-3-Music` | stepfun | demo Space for doc 314; recorded as a `related_url` |

On the LLaDA-UI arXiv link: adding `arxiv.org/abs/2609.13287` to doc 310's `related_urls` would be a
small improvement, but a `related_urls` `field_update` requires the exact stored objects, and
`state_summary.py` flattens them to bare URL strings — the only read path is to burn a proposal on a
deliberately-wrong `old` (friction entry 2026-09-14, `tooling`). Not worth it for a paper the row
already links in another form.

## 2. Targeted search

Last success `2026-09-14T06:32:59Z`, so the ~72 h floor applies (window from 2026-09-12).
**Two new qualifying documents**, both already listed in §1 — they came in through the index diff
and search confirmed rather than found them. Everything else resolves against the corpus:

- **OpenAI** — Deployment Safety Hub newest is still ChatGPT Images 2.5 (09-08) and GPT-6 Astra
  (09-03), both held.
- **Anthropic** — `anthropic.com/news` has nothing after the 09-10 threat-intelligence report,
  already a row. The 09-01 `enterprise-frontier-safeguards` post remains a backlog skip.
- **Google DeepMind** — model-cards index newest is Gemini Omni Flash (08-27) and Gemini 3.5 Audio
  (08-26) on the fetch I got today; Gemini 3.8 Flash (09-02) and the Fairwind / 3.8 Flash Cyber
  access policy are held.
- **Meta** — `research.meta.ai/blog` newest is *How We Built Safety Into Muse* (09-08), held.
- **Mistral** — three September posts, all out of scope: a €3B funding round (09-08), a Cloudera
  partnership (09-10) and a Fortran-migration developer tutorial (09-09). None evaluates a named
  model; `doc_type: other` scope discipline excludes all three.
- **xAI** — Grok 4.7 has now missed two announced dates. Musk said 09-11, then "needs a few more
  days to cook". Still no card, model page, API id or price. `x.ai/news` 403s my fetcher.
- **Evaluators** — METR (`/blog` newest 08-31), UK AISI (`/work` newest 08-27), Apollo (07-21),
  Transluce (08-31), Palisade (`/research`, newest 2026-05-07 — the corrected index from yesterday's
  PROPOSALS entry, checked directly), Epoch (09-14, skipped above), Redwood (09-10 and 09-11 posts
  held), SecureBio (the new add), FAR.AI (the new add), SaferAI, Thinking Machines, US CAISI,
  poolside, RAND (see §8).

**Restricted-access sweep.** Polled the standing program list: GPT-Rosalind / Rosalind Biodefense,
Daybreak Blue/Red, Project Glasswing, Claude Mythos access, the Life Sciences Verification Program,
the Cyber Verification Program, Claude Science, Gemini for Science, Fairwind, DeepMind–Isomorphic
Bioresilience. **No new primary documents.** The LSVP search returned only coverage of the 08-27
announcement (10,000 scientist seats; first Mythos life-sciences participants enrolled), which is
already a row, and the Mythos 5 access policy's own page still reads "we have now enrolled our first
participants" unchanged — see §6. Nothing has opened a dedicated LSVP program page yet.

**Orgs silent >14 days**: `xiaomi`, `stepfun` (broken today by the StepAudio 3 Gen add),
`palisade_research`, `poolside`, `apollo_research`, `thinking_machines`, `us_caisi`, `saferai`,
`mistral`, `uk_aisi`, `metr`, `cursor`. `far_ai` and `securebio` both came off that list today.

## 3. Citation mining

Today is **Tuesday**, so no retrospective sweep.

Yesterday's run made no adds, so the two newest rows (310 LLaDA-UI, 311 Epoch long-context latency)
were already mined on 2026-09-14 and I did not repeat it. Instead I mined the largest recent primary
document, the **GPT-6 Astra system card** (09-03), for external evaluators:

| credited evaluator | standalone publication? |
|---|---|
| SecureBio | **yes** — found and added today as doc 312 |
| UK AISI (alignment, monitorability) | no — `/work` index ends at 08-27; findings exist only inside OpenAI's card |
| Apollo Research (strategic deception, sabotage) | no — newest post 07-21 |
| Gray Swan (IPI Arena, arXiv:2603.15714) | not an allowlisted evaluator; already covered by the 2026-09-09 PROPOSALS entry, not re-raised |
| Irregular (cyber capabilities) | same — not allowlisted, same PROPOSALS entry |

The card's other outbound references are OpenAI's own material (GPT-5.6 Sol and GPT-5.5 system
cards, the Model Spec, the Hugging Face incident technical report, HealthBench Professional) or
third-party benchmark papers that fail the system-card test because they introduce a benchmark
rather than evaluate a named model (ExploitGym arXiv:2605.11086, GPT-Red arXiv:2607.26115,
chain-of-thought monitoring arXiv:2603.05706). Nothing further to propose.

I also checked the new SecureBio report's own references: VCT, VCT-v2, HPCT, World-Class Bio,
ReproBAIT and BioTIER are all benchmarks, not model documentation.

## 4. Open issues

`logs/open_issues.json` is `[]`. No comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is `[]` **again**, but Phase A reported `blocked: 12, errors: 1, moved: 1`.
Thirteen failures, zero escalations — the fourth consecutive run of this pattern and by far the
largest. I identified the affected rows by elimination (blocked fetches, like `not_found`, do not
stamp `last_checked`): of the active rows not checked on 2026-09-15, **twelve are on `openai.com`
or `help.openai.com` and one is `anthropic.com/claude-fable-5-mythos-5-system-card`.**

**None is dead.**

- The Anthropic row is the `moved: 1` event. It now 307-redirects to
  `/document/claude-fable-5-mythos-5-system-card` and on to
  `www-cdn.anthropic.com/…/Claude Fable 5 & Claude Mythos 5 System Card.pdf`. I confirmed the
  redirect chain. Alive, and the document has simply been reorganised behind a `/document/` path.
- The twelve OpenAI rows (the Daybreak / trusted-access-for-cyber cluster, GPT-Rosalind,
  Rosalind Biodefense, the path-to-Astra and Hugging Face incident posts) are the bot wall that
  `config/sources.yaml` already documents for `openai.com`. They 403 my fetcher too, so I could not
  second-opinion them directly — but `deploymentsafety.openai.com` is reachable and the GPT-Rosalind
  access-policy page was annotated as *substantively updated on 2026-09-11* only two runs ago, which
  is positive evidence of life.

So: no `status_change` to `dead` for any of the thirteen. That is the right outcome, reached by
inference rather than through the channel that is supposed to deliver it. Logged as `monitor_gap`
and, for the first time, escalated to PROPOSALS (§8).

## 6. Document update summaries

20 pending diffs, 5 of them new this run. Reviewed 12, annotated 5 (budget).

| slug | version | verdict |
|---|---|---|
| `deepseek-deepseek-v4-flash-vision-exp-model-card` | 564 | `written` |
| `moonshot-ai-kimi-k2-7-code-model-card` | 538 | `written` |
| `alibaba-qwen-qwen3-5-397b-a17b-model-card` | 560 | `written` |
| `alibaba-qwen-qwen3-6-35b-a3b-model-card` | 543 | `written` |
| `alibaba-qwen-qwen3-6-27b-model-card` | 559 | `written` |

Substance:

- **DeepSeek-V4-Flash-Vision-Exp (v564)** — gained a *How to Run with vLLM* section (single
  4×GB300 docker command, DSpark speculative decoding with `num_speculative_tokens: 3` and adaptive
  verification) alongside the existing SGLang recipe, plus a figureless Toolathlon Verified entry in
  Evaluation results.
- **Kimi-K2.7-Code (v538)** — a card that previously reported no benchmark figures now reports two:
  WildClawBench Overall 46.9 and Long-Horizon-Terminal-Bench LHTB Solved 3. Carried over from
  yesterday's over-budget list.
- **Qwen3.5-397B-A17B (v560)** — SWE-bench Verified 76.4 withdrawn; SWE-bench Multilingual 69.3 and
  ScreenSpot-Pro 65.6 added; WildClawBench Avg Time 459 and Avg Cost dropped. Carried over.
- **Qwen3.6-35B-A3B (v543)** — SWE-bench Pro 49.5 and SWE-bench Verified 73.4 withdrawn, a
  figureless ParseBench entry added in their place. Carried over.
- **Qwen3.6-27B (v559)** — benchmark set reworked: SWE-bench Verified and all three WildClawBench
  rows dropped; SWE-bench Multilingual, SkillsBench v1.1 and Terminal-Bench 2.0 added. Every row on
  this card is figureless in both versions, and I said so in the annotation explicitly rather than
  implying scores moved. Yesterday's run skipped it for that reason; I judged "which benchmarks the
  publisher chooses to claim" to be a factual change worth recording, as long as the annotation is
  honest that no numbers are available.

**Reviewed and skipped as noise (7):**

- `anthropic-claude-mythos-5-access-policy` v566 — **entirely** rotating "Related content" teasers
  (Enterprise Frontier Safeguards and the alignment/security post displacing the wellbeing-grants
  teaser). The body, including the LSVP paragraph, is byte-identical. Worth stating plainly because
  this row is one of the restricted-access documents we watch most closely: *nothing about the
  program changed today.*
- `anthropic-claude-mythos-5-other-3` v565 — copyedits only: "Real time" → "Real-time", "evaluation
  set up" → "setup", "reward-hacking" → "reward hacking", "potentially-harmful" → "potentially
  harmful", "reward seeking behaviors" → "reward-seeking behaviors", "in real-time" → "in real
  time", plus the same related-content rotation. No substantive change in an otherwise
  substantive document.
- `apollo-research-anthropic-auto-mode-independent-eval` v568 and
  `apollo-research-claude-haiku-4-5-independent-eval` v567 — identical site-chrome churn on both: a
  "Copy as Markdown" button added, and one sidebar teaser recategorised `Product` → `Research`.
- `inclusion-ai-ring-2-6-1t-model-card` v532, `inclusion-ai-ling-2-6-1t-model-card` v530,
  `inclusion-ai-ling-2-6-flash-model-card` v531 — download counters and one leaderboard row
  reordered in each; no figure changed anywhere.

**Not re-reviewed:** `anthropic-claude-mythos-5-other` v558, `stepfun-step-3-7-flash` v544,
`deepseek-deepseek-v4-pro-0813` v524 and `securebio-claude-opus-4-6-independent-eval-2` v523 were
assessed as noise on 2026-09-14; `tencent-hunyuan-hy3-preview` v552, `nvidia-nemotron-3-ultra` v547,
`xiaomi-mimo-v2-5-pro` v546 and `tencent-hunyuan-hy3` v545 on 2026-09-13. None has changed.

The HuggingFace-widget-churn finding (first logged 2026-09-07) reproduces for the fifth time: v560,
v559, v543, v532, v530 and v531 are all reorder-shaped, and sorting `Evaluation results` rows before
diffing would have collapsed three of them to zero lines and made the other three legible as
insert/delete.

## 7. Notes on the three adds

- **doc 312, SecureBio GPT-6 Astra** — the substantive find of the run, and the first standalone
  third-party evaluation of GPT-6 Astra to appear anywhere. Tagged `cbrn`,
  `has_safety_evals: true`, `openness: closed`. Canonical URL is the Substack copy rather than the
  full PDF because `securebio.org` 403s my fetcher; the PDF is filed as `related_urls`
  `full_document` for the operator sweep, per TASK.md. This also matches all seven existing
  `securebio` rows, which are likewise catalogued under `substack.com`.
- **doc 313, FAR.AI / Qwen3.8-Max** — tagged `cyber`. `openness: open_weight_restrictive`, not
  `closed`: FAR.AI accessed the model through the hosted Qoder CLI, but Qwen3.8-Max is the same
  checkpoint published as `Qwen/Qwen3.8-2.4T-A95B` under a custom use-restricted licence, and the
  existing corpus row for that repo lists both names. `publication_date` is 2026-09-14 from
  `far.ai/sitemap.xml` `lastmod` — the post itself carries no date anywhere, which is logged as
  friction; the sitemap agrees with the post being absent from the index on yesterday's run.
- **doc 314, StepAudio 3 Gen** — `has_safety_evals: false`, honestly. I read the arXiv HTML in full:
  a speech-and-voice-design generative model with no safety section, no misuse discussion and no
  voice-cloning risk assessment, which is itself the finding. `openness` omitted: the report does
  not state whether weights will be released or under what licence, and no StepAudio-3 repo exists
  on the `stepfun-ai` HF org yet, so the access class is unverifiable. In scope because
  audio/music generation is explicitly inside `covered_model_class` and `stepfun` carries no scope
  note excluding audio — the corpus already holds Step-Audio-R1.1 under this publisher. Distinct
  from that row: R1.1 is audio *understanding*, this is generation.

## 8. Friction and proposals

Four `friction.jsonl` entries: the `rand.org` block that lost a document; the `securebio.org` block
that forced the canonical-URL fallback; the thirteen unescalated fetch failures; and FAR.AI's undated
blog posts with the `sitemap.xml` `lastmod` workaround.

One **PROPOSALS.md** entry, dated today: *The agent's fetcher is blocked on domains Phase A reads
fine, and today that lost a document.* There are two fetch stacks in this system with different
reach and the weaker one is the agent's. `rand.org` serves Phase A and the validator without
trouble — six `rand` rows are link-checked every run — but 403s me on every path, so
`RRA5112-1` could not be triaged and is not in the corpus. `securebio.org` does the same, milder.
This is **not** the bot-wall case `sources.yaml` already documents: there the stated mitigation is
"agent web search covers the gap", which assumes the agent's reach is a superset of Phase A's. Here
it is a strict subset, so neither side covers. The proposal asks for a read-only
`scripts/fetch_url.py` that reuses Phase A's client (which would also close the 2026-09-14
PDF-reading gap), an `agent_fetch: blocked` marker in `sources.yaml` so future runs do not
rediscover the wall, and — most concretely — **an operator fetch of `RRA5112-1`.** The entry also
records the `blocked_escalations` gap in PROPOSALS for the first time, since it compounds the same
problem: a `blocked` result is exactly the case where the agent is meant to second-opinion the
fetch, and today it could not have.
