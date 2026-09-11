# cardtrack agent run — 2026-09-11 (run id `2026-09-11T06:16Z-local`)

Phase A checked 272 documents: 272 OK, 0 not-found, 0 blocked, 0 errors, 5 new versions,
250 candidate links carried (32 first seen today), 20 documents in the update queue.
No open GitHub issues, no blocked-URL escalations.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | `add` | Anthropic — *Measuring tactical intelligence targeting and conventional weapons capabilities of AI models* (2026-09-10) | **written** → `anthropic-claude-mythos-preview-other-9` (doc 305, v548) |
| 2 | `add` | Anthropic — *Detecting and countering misuse of AI: September 2026* (2026-09-10) | **written** → `anthropic-claude-opus-other` (doc 306, v549) |
| 3 | `add` | Redwood Research — *An operationalization of opaque serial depth* (2026-09-10) | **written** → `redwood-research-gemma3-1b-independent-eval` (doc 307, v550) |
| 4 | `field_update` | `deepseek-deepseek-v4-1-flash-model-card` `related_urls` | **written** (doc 303) |
| 5 | `field_update` | `anthropic-claude-opus-4-8-other-3` `related_urls` | **rejected** — the URL is already this document's own alt_url |

Five proposals, four written, one rejected. The rejection was correct and I did not retry it: I
proposed adding `anthropic.com/research/automated-researchers-mitigate-alignment-failures` as a
`web_version` of the CDN-hosted PDF row, and the validator replied that the URL is already carried
as an alt_url on document 266 — i.e. the pipeline had already recorded the same-content
relationship, and `related_urls` is for companions, not mirrors. Nothing was missing; my
citation-mining check was simply blind to `alt_urls`, which `state_summary.json` does not expose.
Worth knowing for future runs rather than worth a friction line.

## 1. Phase A candidate triage

250 candidate links, 32 of them new since the last run. Three of the new ones were proposed, one
produced a `related_urls` update, and the remainder resolved below. The 218 carried-over links were
all adjudicated by earlier runs and their reasoning still holds; I re-checked only the two that
today's work touched (`api-docs.deepseek.com/news/news260910`, `blog.redwoodresearch.org`).

**Proposed**

- `anthropic.com/research/intelligence-targeting-conventional-weapons-capabilities` (2026-09-10) —
  Frontier Red Team dangerous-capability report covering six named models: Claude Mythos Preview,
  Mythos 5, Opus 5 and Sonnet 5, plus the open-weight Kimi K3 and GLM 5.2. Two workstreams. On
  intelligence targeting, models were scored on cross-platform identity correlation over dossiers
  whose "median sample is about 37,000 words", on photo geolocation — "Mythos Preview and Mythos 5
  beat even the strongest human baseline on median distance error, scoring 37.0 km and 47.2 km
  across 6,000 photos" — and on text geolocation, where "135 users (8% of those in the corpus) were
  reliably placed within 1 km of their assessed home location by at least one model". On weapons
  development, "Opus 5 strikes on 80% of its launches, Mythos Preview on 70%, Mythos 5 on 53%"
  against parked high-visibility drone targets, degrading sharply with movement and camouflage;
  under wind, "Opus 5 is the only model that succeeds with any regularity… It hits 28% of its
  sorties"; and under GPS denial it "typically ends up fifteen to twenty meters from the
  destination". `openness: restricted` — Mythos Preview and Mythos 5 are vetted-access only.
  Tagged `societal_harm` only; see §8 for why the weapons half is untagged.
- `anthropic.com/threat-intelligence-report-september-2026` (2026-09-10) — the Threat Intelligence
  team's periodic report on eight months of disrupted misuse, organised into seven harm categories
  with named threat-group case studies: GTG-20006 (Russian espionage, 20+ organisations across
  Ukraine, Europe and Asia), GTG-50014 (ShinyHunters, breaches completed in hours, over a terabyte
  exfiltrated from a technology provider, tens of millions of airline passenger records),
  GTG-10007 (~50 organisations, vulnerability research against security products), GTG-54002
  (8,913+ articles across 70 fabricated news sites in 20 languages), GTG-84005 (~1,000 fake
  accounts around a Malaysian election). Catalogued as `doc_type: other` alongside the corpus's
  existing first-party risk reporting (`aug-2026-risk-report`). Two honest caveats, both recorded
  in `notes` and both escalated as friction: the report names Claude *families* and no version
  numbers, and the 9+ MB PDF exceeds my fetch limit so four of the seven sections could not be
  read, which is why `risk_domains` carries only `cyber` and `harmful_manipulation`.
- `blog.redwoodresearch.org/p/an-operationalization-of-opaque-serial` (2026-09-10) — NLS depth, a
  measure of how much serial computation a model can do between interpretable text outputs.
  Gemma3-1B is worked end to end (22 sliding-attention layers plus 4 global, ~1,954 gates), Figure 1
  plots depth against layer count across open-source models, and DeepSeek-V4-Pro and Kimi-K3 are
  flagged as outliers with "significantly higher NLS depth per layer than the other more standard
  transformers"; no open-source CoT model exceeds 17,000. Admitted under
  `criteria.yaml policy.when_uncertain: admit_and_flag` — it is a metric definition whose per-model
  numbers come from architecture specs rather than from running anything, which is the whole of the
  case against it. Flagged in §7. `openness: open_weight_restrictive`, set by Gemma3-1B's terms.

**Attached rather than catalogued**

- `api-docs.deepseek.com/news/news260910` and the tech-report PDF inside the model repo — the dated
  release note for DeepSeek-V4.1-Flash (552B MoE, asymmetric: 8B active for input and 16B for
  output, native vision, KV cache cut to a quarter of HBM and an eighth of SSD, `deepseek-flash`
  endpoint, `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` temporarily redirected, price
  change effective 2026-09-10) plus `DeepSeek_V41_Tech_Report.pdf`. Both are companions of the row
  added yesterday, which carried only the changelog index, so they went into `related_urls`
  (proposal 4) rather than becoming rows.

**Skipped, with the reason**

- `blog.redwoodresearch.org/p/proposal-for-tracking-the-effects` (2026-09-10) — the governance half
  of the same-day Redwood pair (Greenblatt, Westover, Finnveden). It recommends that labs report
  opaque-serial-depth figures, run monitorability stress tests and publish their performance/
  monitorability tradeoff policy, and its appendix sketches methods, but it reports no results on
  any model. Fails the system-card test cleanly; recorded as a related URL on proposal 3 instead.
- `alignment.anthropic.com/2026/modular-pretraining/` (2026-07-08, found by citation mining) —
  introduces GRAM (gradient-routed auxiliary modules) for isolating dangerous knowledge, with real
  quantitative safety results (compute ratios ~0.9–1.0 on retained capabilities, robustness under
  adversarial fine-tuning where MaxEnt degrades to the all-data baseline, a widening forgotten-domain
  gap from 50M to 5B parameters). Skipped anyway: every model is a custom-trained transformer from
  26M to 5B parameters, so there is no named model and `about_a_specific_model_or_eval` fails. This
  is a method paper, not a model evaluation.
- `anthropic.com/news/position-open-weights-models` (citation mining) — a policy position with no
  named model.
- `mistral.ai/news/mistral-x-cloudera` (2026-09-10, both URL variants) — a partnership
  announcement, explicitly out of scope for `doc_type: other`.
- `mistral.ai/news/spaces/` (2026-03-31) — an engineering post about a CLI; also predates nothing
  relevant, it simply resurfaced in the index diff.
- `cursor.com/blog/projects` and `cursor.com/changelog/projects` (2026-09-10) — product feature.
- `huggingface.co/nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis`, `nvidia/RE-USE`
  (audio-to-audio), `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` discussion threads — auxiliary media
  and speech models plus discussion pages, out under the NVIDIA `scope` note.
- `huggingface.co/nvidia/DeepSeek-V4-Pro-0813-nvfp4-DSpark`, `nvidia/GLM-5.3-Flash-NVFP4` —
  quantised re-uploads of other labs' models, out under `distinct_model_release`. Noted in passing
  that the second implies a GLM-5.3-Flash release upstream; Z.ai/Zhipu is not on the allowlist, so
  there is nothing to propose and this is not a monitoring gap on our side.
- `huggingface.co/papers/2609.10712` (*An Open Recipe for IMO Gold*) with
  `nvidia/Nemotron-3-Labs-Ultra-Math-SFT` / `-RL` and the IMO-2026 collection, plus
  `papers/2609.07941` and `papers/2609.10226` — HF paper pages, math-specialised checkpoints of an
  already-catalogued base model, and benchmark datasets. Out under `distinct_model_release` and the
  per-publisher scope notes, consistent with every prior run.
- `huggingface.co/inclusionAI/Ling-3.0-flash-VL-int4` / `-fp4` and the four SGLang-recipe discussion
  threads, `huggingface.co/tencent/AuK/discussions/1`, `huggingface.co/steven144`,
  `huggingface.co/wineandchord`, `huggingface.co/ejahangiri-nv`, `nvidia/aerial-isac-pusch-hest`,
  `nvidia/PhysicalAI-Autonomous-Vehicles`, `collections/nvidia/ai-for-media` — quantisation
  variants, user profiles, dataset repos, collections and discussion threads.
- `substack.com/@nathansheffield`, `substack.com/@lukasfinnveden` — author profile pages surfaced by
  the Redwood archive diff.

## 2. Targeted web search

Last successful run 2026-09-10T06:34Z, so the window runs from there back-extended to the 72-hour
floor, i.e. 2026-09-08 onward.

- **New in the window:** the three documents proposed above and nothing else. I checked the two
  first-party hubs that bot-block Phase A directly. OpenAI's deployment safety hub is unchanged
  since ChatGPT Images 2.5 on 2026-09-08 (already catalogued); Anthropic's news index shows the
  threat intelligence report as its only item after 2026-09-01. One thing worth recording: a
  secondary source reports that OpenAI **revised the GPT-6 Astra system card on 2026-09-09**, more
  prominently emphasising its measurement of metagaming as verbalised in chains of thought and
  adding CoT examples of flagged oversight gaming. Phase A fetched the Astra row today and produced
  no new version, so either the revision predates our first capture or it did not change the
  extracted text. Not actionable as a proposal — there is no stored version to annotate — but if a
  later diff surfaces it, that is what it is.
- **Restricted-access programs.** Polled the named list. No new documents. GPT-Rosalind, Daybreak
  Blue/Red, Project Glasswing, Claude Science, Gemini for Science and Fairwind are all unchanged
  and their rows current. Anthropic's Cyber Verification Program page was catalogued yesterday. The
  Life Sciences Verification Program remains a watch item on exactly yesterday's terms: confirmed
  live as an invite-only beta giving vetted life scientists Mythos 5.1 with reduced biology
  safeguards, US organisations only, still with no dedicated program page and no public application
  route, so its only primary-source description is inside the catalogued Fable 5.1 / Mythos 5.1
  access-policy row. Nothing to propose.
- **Orgs silent >14 days.** Checked the evaluators, where a miss costs most. METR has published no
  evaluation since GPT-5.6 Sol (2026-06-26) and nothing since the 2026-08-31 security update; UK
  AISI's newest work-index item is still the optional-stopping methodology post; Apollo Research
  (newest 2026-07-21) and SecureBio (newest 2026-08-07) are unchanged. Transluce's mental-health
  evaluation and SaferAI's GLM report both surfaced in search and both are already catalogued
  (`transluce.org/announcing-mental-health-evaluation`,
  `safer-ai.org/u/2026/08/SaferAI-GLM-Evaluation-Report.pdf`), which is a useful negative result:
  the searches that would catch a miss are returning documents we already hold. Thinking Machines'
  news page has nothing after 2026-08-27. Still notable, now eight days after launch: **none of
  METR, UK AISI, Apollo or SecureBio has published a standalone GPT-6 Astra report**, despite all
  contributing sections to OpenAI's card.

## 3. Citation mining

Mined the Frontier Red Team report added today, which is densely referenced. Its external citations
are open-source-intelligence and defence-analysis sources — Bellingcat, CSIS, NATO STO, RUSI,
Defense One, CTC West Point, US Army Press, the CMU GeoText corpus, YFCC100M and Haas et al. 2024 —
none of them model evaluations and none from allowlisted evaluators, so nothing to propose there.
Its internal citations were the productive part: `zero-days`, `exploit-evals`,
`alignment-assessment-cybersecurity-incidents` and `glasswing` are all already rows;
`formalizing-fermats-last-theorem` remains the deliberately-skipped case escalated on 2026-09-10;
`automated-researchers-mitigate-alignment-failures` and `modular-pretraining` were both new to me
and are resolved above (the first already an alt_url, the second skipped for want of a named model);
`position-open-weights-models` is a policy position.

Today's UTC date is a Friday, so the weekly retrospective sweep was not due.

## 4. Open issues

`logs/open_issues.json` is empty. No investigations, no comments posted.

## 5. Blocked-URL escalations

None in `candidates.json`. Phase A reported 0 blocked, 0 not-found and 0 errors across 272
documents.

## 6. Document updates

Five fresh diffs entered the queue today; the other fifteen entries are backlog already adjudicated
by previous runs. I read all five. **All five are noise — no annotations proposed.**

Every one is the HuggingFace widget churn first diagnosed on 2026-09-07, and today's batch is an
unusually pure example of it: each diff is a download counter moving, a "Spaces using" count
moving, and rows in the Evaluation results sidebar changing order without changing value.

- `nvidia-nvidia-nemotron-3-ultra-550b-a55b-model-card` v547 — downloads 238,253 → 213,329;
  "Collection including" → "Collections including" (HuggingFace pluralising its own label); the
  terminal-bench-2.1 row (56.4) moved above the GPQA Diamond row (87). No value changed.
- `xiaomi-mimo-v2-5-pro-model-card` v546 — downloads 36,183 → 25,107; the SWE-bench_Pro row (57.2)
  moved above SWE-bench_Verified (78.9).
- `tencent-hunyuan-hy3-model-card` v545 — downloads 12,449 → 12,650; Spaces 23 → 25; GPQA Diamond
  (90.4) and SWE-bench_Verified (78) reordered; a benchflow/skillsbench row replaced by an
  internlm/WildClawBench row, both community leaderboard entries with no score shown.
- `alibaba-qwen-qwen3-6-35b-a3b-model-card` v543 — downloads 5,567,036 → 4,033,893; Spaces 67 → 70;
  two community leaderboard rows (SWE-bench_Pro 49.5, SWE-bench_Verified 73.4) replaced by a
  llamaindex/ParseBench row.
- `stepfun-step-3-7-flash-model-card` v544 — downloads 87,266 → 17,288; Spaces 27 → 24;
  terminal-bench-2.1 (59.5) moved above SWE-bench_Pro (56.3).

No publisher text, no benchmark number, no licence term and no safety content changed in any of the
five. Annotating reordered sidebar rows would make the version history read as if results were being
revised, which is the opposite of what the annotation field is for.

## 7. Friction log

Five lines appended to `logs/friction.jsonl`:

- `schema_gap` — conventional-weapons capability has no `risk_domains` tag, escalated to
  `PROPOSALS.md` (see §8).
- `unfetchable_but_alive` — the threat intelligence PDF is alive but returns
  `maxContentLength size of 10485760 exceeded`, a harder stop than the 2026-09-09 PDF-decoding
  entry because no bytes arrive at all. Direct cost: four of seven harm sections unread, so four
  `risk_domains` left off document 306 rather than attested blind.
- `ambiguous_criteria` — the family-named-model question. `criteria.yaml` scopes the model-FAMILY
  exception to `access_policy` only, but first-party misuse reporting has the same property for a
  structural reason (threat-intel teams do not attribute disrupted operations to checkpoints), and
  Anthropic publishes these on a cadence, so the question will recur on schedule.
- `ambiguous_criteria` — the Redwood NLS-depth admit, with the case against it stated as plainly as
  the case for, since I would rather be overruled than keep re-deciding it.
- `tooling` — the 2026-09-10 entry reproduces, and the blast radius is wider than it looked: the
  brace-plus-quote refusal also closes every shell append route into `logs/`, so both the friction
  log and `PROPOSALS.md` had to be extended by exact-string edits on their last line. `/tmp` plus
  the allowed entry points is the whole usable surface for this run.

## 8. Proposals

One dated entry appended to `logs/PROPOSALS.md`: *conventional-weapons capability has no home in
`risk_domains`*. Today's Frontier Red Team report is half surveillance (tagged `societal_harm`) and
half kinetic weapons uplift — drone terminal guidance, payload delivery under wind, GPS-denied
navigation — which is not CBRN, not cyber, not loss of control and not manipulation, and which
`societal_harm` would only dilute. So the most severe finding in the document is invisible to the
site's risk filters. The same day's threat intelligence report carries conventional weapons as one
of seven harm categories, and both Anthropic and OpenAI now run standing workstreams here, so this
is a trickle rather than an exception. The entry asks for one of two things, either acceptable: add
a sixth key (`conventional_weapons`), or state in `criteria.yaml` that the five-term EU CoP mirror
is a hard commitment and say where kinetic findings should go instead. Adding a key is a config
change and therefore operator-only; the agent cannot route around it.
