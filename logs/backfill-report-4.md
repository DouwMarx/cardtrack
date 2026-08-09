# cardtrack backfill drain — run `backfill-drain-3`

Corpus went from 75 to 93 documents. Eighteen written, four routed to review, zero
rejected. No cap bound. The headline of this run is that **three publishers the previous
session declared exhausted or unreadable were not** — nvidia, uk_aisi and openai each
yielded in-scope documents, and meta was closed for the first time in three runs. The
common cause is triage by title or by a single fetch tool's failure rather than by
fetching the document.

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 1708 (down from 1716), across 19 publishers |
| Candidates triaged | all 1708 by publisher; the 89 `aisi.gov.uk/blog` URLs were fetched individually, plus ~45 documents read in full |
| Proposals submitted | 22 |
| Written as rows | 18 |
| Routed to review issues | 4 (outbox:5–8) |
| Rejected | 0 |
| Skipped with a reason class | see the skip table below |

Publisher counts after the run: google_deepmind 19, **nvidia 18** (was 7), openai 11,
uk_aisi 9 (was 6), anthropic 9, tencent_hunyuan 6 (was 4), metr 6, moonshot_ai 4,
**meta 3** (was 2), deepseek 3, xiaomi 2, thinking_machines 2, apollo_research 1.

## Proposals and validator verdicts

| # | Document | Publisher | Date | Verdict |
|---|---|---|---|---|
| 1 | Nemotron 3 Nano Omni 30B-A3B Reasoning | nvidia | 2026-04-28 | `written` id 76 |
| 2 | Nemotron-Cascade-2-30B-A3B | nvidia | 2026-03-19 | `written` id 77 |
| 3 | LocateAnything-3B | nvidia | 2026-05-26 | `written` id 78 |
| 4 | Alpamayo 2 Super | nvidia | 2026-08-04 | `written` id 79 |
| 5 | Alpamayo-1.5-10B | nvidia | 2026-03-19 | `written` id 80 |
| 6 | Nemotron-Labs-Audex (30B-A3B + 2B) | nvidia | 2026-06-08 | `written` id 81 |
| 7 | NemotronLabs VoiceChat 11B | nvidia | 2026-08-03 | `written` id 82 |
| 8 | Nemotron 3.5 ASR Streaming 0.6B | nvidia | 2026-06-04 | `written` id 83 |
| 9 | Nemotron Parse 2.0 | nvidia | 2026-08-03 | `written` id 84 |
| 10 | Nemotron OCR v2 | nvidia | 2026-04-15 | `written` id 85 |
| 11 | Nemotron 3 Nano 4B | nvidia | 2026-03-16 | `written` id 86 |
| 12 | HY-World 2.0 | tencent_hunyuan | 2026-04-16 | `written` id 87 |
| 13 | HY-Embodied-0.5 | tencent_hunyuan | 2026-04-09 | `written` id 88 |
| 14 | **GPT-5.3 Instant System Card** | openai | 2026-03-02 | `written` id 89 |
| 15 | **Muse Spark 1.2 & Muse Code Evaluation Methodology** | meta | 2026-08-05 | `written` id 90 |
| 16 | Evaluating whether AI models would sabotage AI safety research | uk_aisi | 2026-04-27 | `written` id 91 |
| 17 | How fast is autonomous AI cyber capability advancing? | uk_aisi | 2026-05-13 | `written` id 92 |
| 18 | RealityTest: do AI systems disclose their identity when asked? | uk_aisi | 2026-06-08 | `written` id 93 |
| 19 | Hy-Embodied-RxBrain-1.0 (RxBrain) | tencent_hunyuan | null | `issue_filed` publication_date_unknown, outbox:5 |
| 20 | Model Card: Grok 4.5 | xai | 2026-07-14 | `issue_filed` tier_2_publisher, outbox:6 |
| 21 | Laguna XS.2 and M.1: A Deeper Dive | poolside | 2026-04-28 | `issue_filed` tier_2_publisher, outbox:7 |
| 22 | Ling-3.0-flash Model Card | inclusion_ai | null | `issue_filed` publication_date_unknown, outbox:8 |

### The four that matter most

**#14, GPT-5.3 Instant (2026-03-02), was hiding in plain sight.** Two consecutive runs
concluded that everything below the Deployment Safety Hub's "View more" fold predated the
scope floor. `https://deploymentsafety.openai.com/sitemap.xml` enumerates the whole hub in
one fetch. Date-checking all 24 slugs found exactly one in-scope miss — this one, a real
system card with disallowed-content Production Benchmarks (including candidly reported
regressions against gpt-5.2-instant on sexual content and self-harm) and HealthBench.
**openai is now genuinely exhausted**, verified slug by slug rather than assumed.

**#15 closed meta after three runs of failure.** The previous two sessions searched
`ai.meta.com/blog`, which still shows nothing after 2026-07-27. Muse Spark 1.2 and Muse
Code launched 2026-08-05 on **`research.meta.ai`**, a host absent from `sources.yaml`.
I read the linked four-page PDF in full. Worth stating plainly: it contains
**no safety content at all** — only Terminal-Bench 2.1, DeepSWE v1.1, GDPVal-AA v2, MCP
Atlas and an internal coding bench. Meta's two earlier Muse Spark documents are both
safety and evaluation reports, so `has_safety_evals: false` here is a real finding, not a
gap in my reading. I used `doc_type: other` rather than `system_card` for the same reason.

**#16–18 mean uk_aisi was not exhausted.** The previous run dismissed the remaining ~90
AISI blog URLs as methodology, policy and tooling with no named model. I fetched all 89
individually. Three are 2026 model-specific evaluations with quantitative per-model
results, and all three read as methodology from their titles alone — which is exactly how
they were missed. Title-based triage does not work for AISI.

**#20 means xai is readable.** The previous run logged the publisher as invisible after a
403. That 403 is specific to one fetch path; plain curl with a browser UA gets 200 on
`/news`, `/news/grok-4-5` and `/safety`. `x.ai/safety` links a genuine 27-page Grok 4.5
model card with cyber (CyberGym, HackerBench), bio/chem (VCT, WMDP, LAB-Bench, ProtocolQA,
BixBench), jailbreak, child-safety, CBRN-refusal, mental-health and sycophancy sections.
Tier 2, so it became a review issue, but the publisher is no longer a blind spot.

### Judgement calls I did not paper over

- **#11 Nemotron 3 Nano 4B** is the weakest `distinct_model_release` attestation in this
  batch. The corpus holds Nemotron 3 Super and Ultra, so a 4B is arguably another size
  tier. I attested it distinct because the Nano tier is a separate architecture lineage
  (Mamba-2 hybrid compressed from Nano-9B-v2 via Elastic, not a scaled Super), released on
  its own date with its own card and eval table — and said so in the justification. A
  reviewer may reasonably disagree.
- **#6 Audex** has a date conflict I flagged rather than smoothed: both cards say
  "Release Date: June 8, 2026" while the repos were created 2026-07-06 and the tech report
  is a July arXiv. I used the card's own date per the criteria.
- **#18 RealityTest** lists only GPT-5.1 and GPT-4o in `model_names` even though the study
  covers 23 systems, because those are the only two I could verify per-model figures for.
  Better a short honest list than a transcribed roster I did not confirm.

## What is now exhausted, and how I verified it

- **openai** — all 24 hub slugs enumerated via sitemap and date-checked. Everything except
  GPT-5.3 Instant is 2025 or earlier. Done.
- **google_deepmind** — re-checked `deepmind.google/models/model-cards/`; newest entries
  are Lyria 3.5 (07-29) and the two Robotics cards (07-30), all catalogued. Confirms the
  previous run. **Do not re-triage.**
- **anthropic** — transparency hub lists eleven system cards, every 2026 one catalogued;
  nothing dated August 2026 or later. The RSP, Usage Policy, Constitution and the
  political-even-handedness eval are not model-specific.
- **moonshot_ai, deepseek, xiaomi** — HF API shows 4, 3 and 2 in-scope 2026 releases
  respectively; all catalogued. The rest are DSpark/DFlash/eagle3 draft models, `-Base`
  repos and quantizations.
- **metr** — `/blog` and `/research` both re-checked. The 2026 items not in the corpus
  (Expenditure Horizon 07-21, MirrorCode 04-10, the productivity survey 05-11, Task
  Substitution 05-08, propensity-investigation 07-28) name no specific model.
- **apollo_research** — the "System Card Evaluations" list on its research page is Apollo's
  contributions *inside other orgs' system cards*, which are already catalogued as those
  orgs' documents, not separate Apollo publications. Its only standalone 2026 output is
  the one already in the corpus. The scheming-precursor research note is 2025-07-03.
- **thinking_machines** — newest post is "A Safe Path to Open Weights" (07-31), an essay,
  not a model release. Both Inkling cards remain the only documentation.
- **uk_aisi** — now actually exhausted: all 89 blog candidates fetched and date-checked.

## Skipped, by reason class

| Reason class | Examples |
|---|---|
| Below the 2026-01-01 scope floor | all pre-2026 OpenAI hub slugs (4o image gen, chatgpt-agent, deep-research, gpt-5, gpt-5.1, gpt-5.1-codex-max, gpt-5.2, gpt-5.2-codex, gpt-5-codex, gpt-oss, o3, sora-2, sensitive-conversations); Apollo's 2025 research notes; most AISI blog posts |
| Not about a specific model or eval | `ai.meta.com/static-resource/Meta_Advanced-AI-Scaling-Framework-v2` and xAI's Frontier AI Framework (both frontier-safety policies); AISI methodology/tooling/partnership posts; METR's 2026 non-model research; Anthropic's RSP and Constitution |
| Same release already covered by another document | `research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf` — real and in scope, but the Cosmos 3 release is already represented by the Cosmos3-Super and Cosmos3-Edge cards, so `distinct_model_release` would be false |
| Quantization / precision / checkpoint / base variant | `Nemotron-3-Nano-Omni-*-FP8/NVFP4`, `Nemotron-3-Nano-4B-FP8/GGUF`, `Hy3-FP8`, `Hy-MT2-*-GGUF`, `Ling-3.0-flash-fp8/int4/fp4`, all `*-Base` repos |
| Third-party re-upload of another org's model | `nvidia/Kimi-K2.7-Code-NVFP4`, `nvidia/GLM-5.2-NVFP4`, `nvidia/Qwen3.6-27B-NVFP4`, `nvidia/MiniMax-M3-NVFP4`, `nvidia/Gemma-4-*-NVFP4`, `nvidia/diffusiongemma-26B-A4B-it-NVFP4`, `nvidia/gpt-oss-puzzle-88B` |
| Marketing / product page without documentation | `poolside.ai/models` (no date, no methodology — I proposed the technical deep dive instead); xAI partner and integration posts; Meta customer-story posts |
| Not notable enough to catalogue | NVIDIA `Ising-*`, `NV-JEPA-DNA-*`, `Privasis-Cleaner`, `ArtiFixer`, `nvDock`, `CWIP-1.0`, `corrdiff-cosmo-era5`, the `gr00t17-lerobot-*` and `Kimodo-*` task checkpoints; Tencent `POINTS-*`, `Youtu-*`, `Penguin-VL-*`, `StableToken`, `HiLS-Attention-7B`; inclusionAI `SingGuard-*`, `ZwZ-*`, `AReaL-*` |
| Date undeterminable, not proposed | `tencent/Covo-Audio-Chat` (7B audio LLM, arXiv:2602.09823, 101 likes — no dateline anywhere in the card, and unlike RxBrain no org project page to corroborate; two null-date Tencent review issues in one run would be noise); `tencent/HunyuanOCR` (unchanged from last run); `nvidia/GR00T-N1.7-3B` and the `Nemotron-Labs-Diffusion-*` family (cards have an empty "Release Date:" field) |
| Scope question unresolved | `aisi.gov.uk/blog/how-our-new-control-red-team-is-stress-testing-frontier-monitors` (2026-07-23) — see friction; it red-teams monitors, not models |

## Things the next session should know

1. **NVIDIA cards have an explicit `Release Date:` field. Grep it before touching
   `createdAt`.** This single trick resolved every date question the previous run got
   stuck on: Alpamayo2-Super (card 08/04/2026 vs repo createdAt 05-27), LocateAnything-3B
   (card 05/26/2026 vs createdAt 03-02), Alpamayo-1.5-10B, ASR streaming, Lyra 2.0.
   `curl -sL https://huggingface.co/<id>/raw/main/README.md | grep -iA4 "release date"`.
2. **nvidia is still not exhausted.** I proposed the eleven I could verify as distinct,
   dated and genuinely used. Left on the table with real signal but unresolved dates or
   marginal notability: `Nemotron-Labs-Diffusion-3B/8B/14B/VLM-8B` (a family, 152/53/39
   likes, empty Release Date fields), `Lyra-2.0` (2026-04-14, 339 likes, research 3D world
   gen), `PiD` (2026-04-28, 401 likes), `Nemotron-Labs-TwoTower-30B-A3B` (2026-04-11, 138
   likes), `nemotron-ocr` predecessors and `Nemotron-3-Content-Safety` (2026-03-06, the
   predecessor of the catalogued 3.5). Also `NVIDIA-Nemotron-Parse-v1.2` (2026-02-18, 207k
   downloads), which I skipped as an incremental point release of a 2025 model.
3. **Two `sources.yaml` index gaps caused most of the misses this run**, both logged as
   friction: meta needs `https://research.meta.ai/blog/`, and openai would be better served
   by `https://deploymentsafety.openai.com/sitemap.xml` than by the 403-ing
   `openai.com/safety/`. Neither is something I can change from here.
4. **Do not trust "publisher X is unreadable" without retrying with a browser UA.** xai was
   written off on a single tool's 403 and turned out to publish full model cards.
5. **Tier-2 status.** Slots went to xai, poolside and inclusion_ai, all previously at zero
   coverage; the cap of three was reached exactly. Every tier-2 publisher now has at least
   one review issue filed except **stepfun**, whose Step-3.7-Flash issue (outbox:4) is
   still open from last run — its `Step-3.5-Flash` (2026-02-01, 830 likes) and
   `Step3-VL-10B` (2026-01-13, 411 likes) are the obvious next candidates. **mistral** and
   **alibaba_qwen** each have one issue open and no rows.
6. `logs/open_issues.json` is empty, so there were no issues to investigate and no comments
   filed. `blocked_escalations` in `candidates.json` is empty; no document was found dead.

## Friction and proposals

Six entries appended to `logs/friction.jsonl`: xAI's false-negative bot wall; the two
index_url gaps (meta's research host, OpenAI's sitemap); the AISI title-triage failure; the
unresolved scope question for monitor red-teaming; and NVIDIA's Release-Date field
alongside the Audex date conflict.

Nothing appended to `PROPOSALS.md`. The two index_url gaps are concrete and evidenced, but
they are instances of the same `document_index_urls:` request two previous runs have
already filed; a third restatement would be noise rather than new evidence.
