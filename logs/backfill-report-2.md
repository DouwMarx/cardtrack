# cardtrack backfill drain — run `backfill-drain-2`

Corpus went from 64 to 75 documents. Eleven written, three routed to review, zero
rejected. The add cap (250, temporary drain setting) did not bind — this run ended
because I ran out of documents I could verify, not out of budget.

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 1716, all distinct URLs; none of them is the canonical URL of a document already in the corpus, so Phase A appears to pre-filter known documents |
| Candidates triaged | all 1716, by publisher; ~40 fetched and read in full |
| Proposals submitted | 14 |
| Written as rows | 11 |
| Routed to review issues | 3 (outbox:2, outbox:3, outbox:4) |
| Rejected | 0 |
| Skipped with a reason class | see the skip table below |

Publisher counts after the run: google_deepmind 19, openai 10, anthropic 9, nvidia 7,
uk_aisi 6, metr 6, tencent_hunyuan 4, moonshot_ai 4, deepseek 3, xiaomi 2,
thinking_machines 2, meta 2, apollo_research 1.

**apollo_research went from zero to one**, so every tier-1 publisher and evaluator in
`sources.yaml` now has at least one document.

## Proposals and validator verdicts

| # | Document | Publisher | Verdict |
|---|---|---|---|
| 1 | DeepSeek-OCR-2 Model Card (2026-01-27) | deepseek | `{"status": "written", "slug": "deepseek-deepseek-ocr-2-model-card", "document_id": 65}` |
| 2 | Hy-MT2 Model Card, 1.8B/7B/30B-A3B (2026-05-21) | tencent_hunyuan | `{"status": "written", "slug": "tencent-hunyuan-hy-mt2-1-8b-model-card", "document_id": 66}` |
| 3 | Hy3 preview Model Card (2026-04-23) | tencent_hunyuan | `{"status": "written", "slug": "tencent-hunyuan-hy3-preview-model-card", "document_id": 67}` |
| 4 | Hy-Embodied-VLM-1.0 Model Card (2026-07-15) | tencent_hunyuan | `{"status": "written", "slug": "tencent-hunyuan-hy-embodied-vlm-1-0-model-card", "document_id": 68}` |
| 5 | Nemotron 3.5 Content Safety Model Card (2026-06-02) | nvidia | `{"status": "written", "slug": "nvidia-nemotron-3-5-content-safety-model-card", "document_id": 69}` |
| 6 | Nemotron 3 Embed Model Card, 8B + 1B (2026-07-16) | nvidia | `{"status": "written", "slug": "nvidia-nemotron-3-embed-8b-model-card", "document_id": 70}` |
| 7 | Nemotron Labs 3 Puzzle 75B-A9B Model Card (2026-07-06) | nvidia | `{"status": "written", "slug": "nvidia-nvidia-nemotron-labs-3-puzzle-75b-a9b-model-card", "document_id": 71}` |
| 8 | Review of the Anthropic Sabotage Risk Report: Claude Opus 4.6 (2026-03-12) | metr | `{"status": "written", "slug": "metr-claude-opus-4-6-independent-eval-3", "document_id": 72}` |
| 9 | Red-Teaming Anthropic's Internal Agent Monitoring Systems (2026-03-26) | metr | `{"status": "written", "slug": "metr-claude-opus-4-6-independent-eval-4", "document_id": 73}` |
| 10 | Early work on monitorability evaluations (2026-01-22) | metr | `{"status": "written", "slug": "metr-gpt-5-independent-eval", "document_id": 74}` |
| 11 | Measuring Reward-Seeking via Contrastive Belief Updates (2026-07-21) | apollo_research | `{"status": "written", "slug": "apollo-research-openai-o3-independent-eval", "document_id": 75}` |
| 12 | Mistral Small 4 (2026-03-16) | mistral | `{"status": "issue_filed", "reason": "tier_2_publisher", "issue_ref": "outbox:2"}` |
| 13 | Qwen3.6-35B-A3B Model Card (2026-04-15) | alibaba_qwen | `{"status": "issue_filed", "reason": "tier_2_publisher", "issue_ref": "outbox:3"}` |
| 14 | Step-3.7-Flash Model Card (date null) | stepfun | `{"status": "issue_filed", "reason": "publication_date_unknown", "issue_ref": "outbox:4"}` |

Three of these deserve a note.

**#8 is the retry of last run's only rejection.** The previous session was told
`document_retrievable=false: HTTP 500` for a page it had just read in full, and logged
it as an unfetchable-but-alive friction entry asking the next run to retry. I re-fetched
and re-read the live page first, then resubmitted unchanged, and it was accepted on the
first attempt. The rejection was a transient upstream 5xx, not a dead link. That means
the validator has no retry-on-5xx, and the "never retry a rejected proposal" rule turns
one bad upstream response into a permanently lost lead unless a friction entry carries it
across sessions. Logged again.

**#9 has a `model_names` caveat I did not paper over.** METR red-teamed *Anthropic's
monitoring stack*, not Claude Opus 4.6 itself; I put Opus 4.6 in `model_names` because
that release's Sabotage Risk Report (Appendix 8.4) is what scopes the exercise, and said
so in the justification. A reviewer may reasonably prefer that field empty.

**#14 was given a null date deliberately.** StepFun's card carries no dateline, the repo
was created 2026-05-23, and secondary coverage says 28 or 29 May without agreeing. Null
routes it to a human rather than guessing, which is the right trade for a tier-2 row that
was going to become an issue either way.

## What I checked, and what is now exhausted

**Enumerated to the bottom, nothing left in scope:**

- **google_deepmind.** Fetched `deepmind.google/models/model-cards/` and matched all 46
  listed cards against the corpus. Every 2026 card is already catalogued; everything
  unmatched is 2025 or earlier (Gemini 3 Pro/Flash/Pro Image, Gemini 2.x, Veo 3, Imagen 4,
  Gemma 1–3, EmbeddingGemma, ShieldGemma, PaliGemma, CodeGemma, RecurrentGemma). The
  six-item backlog the previous run left behind is fully drained. **Do not re-triage GDM.**
- **uk_aisi.** Fetched `aisi.gov.uk/work`. It lists five 2026 model-specific evaluations;
  all five are in the corpus, as is the cheating-behaviour report. The remaining ~90 blog
  URLs in `candidates.json` are methodology, policy, tooling (Inspect, ControlArena,
  HiBayes), partnership announcements and progress reports — no named model. **Exhausted.**
- **openai.** Fetched the Deployment Safety Hub. All eight documents it lists above the
  "View more" fold are in the corpus. The tail below the fold still refuses to enumerate
  through a plain fetch; GPT-5.3-Codex (2026-02-05) is the oldest 2026 item and is already
  catalogued, so anything further down is below the scope floor. Low priority.
- **moonshot_ai.** The HuggingFace API shows exactly four 2026 models (Kimi K2.5, K2.6,
  K2.7-Code, K3) and all four are catalogued. **Exhausted.**
- **thinking_machines.** Inkling and Inkling-Small are both catalogued — the "known gap"
  in the session brief is closed. The remaining `thinkingmachines.ai/blog/` URLs are
  research essays (LoRA, on-policy distillation, modular manifolds, nondeterminism in
  inference), not model documentation.

**Publishers where I could not close the gap, and why:**

- **meta.** Second run in a row with nothing to propose. Muse Image shipped 2026-07-07
  with a blog post I read in full that links no card, no system card and no evaluation
  report — unlike Muse Spark and Muse Spark 1.1, which both have
  `ai.meta.com/static-resource/…-evaluation-report` documents. Muse Spark 1.2 and Muse Code
  reportedly launched 2026-08-05 per several trackers, but `ai.meta.com/blog/` still shows
  nothing after 2026-07-27. **Next session: re-check `ai.meta.com/blog/` for Muse Spark 1.2
  and for a Muse Image evaluation report appearing late; do not propose the launch posts
  themselves, they are announcements without documentation.**
- **xai.** `x.ai/news/grok-4-5` returns HTTP 403. The whole publisher is unreadable by this
  agent, so nothing was proposed. Tier 2, so the cost is a missed review issue.
- **alibaba_qwen.** Its `index_urls` entry is dead: `qwenlm.github.io/blog/` has not been
  updated since 2025-09-23, and `qwen.ai/research` renders client-side and returns a page
  containing only the word "Qwen". Hub cards are the only readable primary source, and they
  carry no datelines — hence the repo-createdAt date on outbox:3.

## Skipped, by reason class

| Reason class | Count (approx.) | Examples |
|---|---|---|
| Hub/site chrome and org-member profiles | ~700 | `huggingface.co/<username>`, `/datasets/`, `/spaces/`, `/papers/`, `/collections`, login/pricing/careers/legal |
| Below the 2026-01-01 scope floor | ~250 | every pre-2026 METR and AISI post, Mistral 3 (2025-12-02), `NVIDIA-Nemotron-3-Nano-30B-A3B` (released 2025-12-15), `MiMo-V2-Flash` (2025-12-17), all Gemini 2.x and Gemma 1–3 cards |
| Not about a specific model or eval | ~180 | AISI methodology/policy/tooling posts, METR productivity and time-horizon work, Apollo governance/press pages, NVIDIA how-to blog posts |
| Quantization / checkpoint / base / distill variant | ~60 | `Hy-MT2-*-FP8/GGUF/2Bit`, `Hy3-FP8`, `MiMo-V2.5-Pro-FP4-DFlash`, `Nemotron-3-Embed-1B-NVFP4`, `DeepSeek-V4-*-DSpark`, `dflash_*`/`dspark_*`/`eagle3_*` draft models, `HunyuanImage-3.0-Instruct-Distil` |
| Third-party re-upload of another org's model | ~15 | `nvidia/Kimi-K2.7-Code-NVFP4`, `nvidia/GLM-5.2-NVFP4`, `nvidia/Qwen3.6-27B-NVFP4`, `nvidia/MiniMax-M3-NVFP4`, `nvidia/Mistral-Medium-3.5-128B-NVFP4` |
| Marketing / launch post without documentation | ~120 | `mistral.ai/products/*`, `x.ai/news/grok-<partner>`, Meta customer-story posts, `ai.meta.com/meta-ai/*` |
| Not notable enough to catalogue | ~40 | NVIDIA `Ising-*`, `NV-JEPA-DNA-*`, `Privasis-Cleaner`, `ArtiFixer`, `corrdiff-cosmo-era5`, `Cosmos-H-Dreams` (354 downloads); Tencent `POINTS-*`, `Youtu-*`, `Penguin-VL-*`, `StableToken`; `XiaomiMiMo/MiMo-V2.5-ASR` (2k downloads) |
| Date undeterminable, so not proposed | 3 | `tencent/HunyuanOCR` (repo predates 2026, now serves a HunyuanOCR-1.5 card), `tencent/Hy-Embodied-RxBrain-1.0` (card says only "[2026-07]"), `nvidia/GR00T-H-N1.7` (no date; also a surgical-robot post-train of Isaac GR00T N1.7, i.e. a derivative) |

The counts above are eyeballed per-publisher estimates, not a computed partition — the
classes overlap (a `-FP8` re-upload of a 2025 model is both a variant and out of scope)
and they do not sum to 1716. Only the "date undeterminable" row is exact.

## Things the next session should know

1. **Use the HuggingFace JSON API, not the org HTML page.** `https://huggingface.co/api/models?author=<org>&sort=createdAt&direction=-1&limit=60` returns only the org's own models with `createdAt`, `lastModified`, `downloads` and `likes`. It decided every include/exclude call I made, caught two models that looked 2026 but shipped in December 2025, and would have cut this run's triage cost by an order of magnitude. The scraped candidate lists for HF-indexed publishers are ~90% noise.
2. **`createdAt` is not the publication date.** Repos are routinely created days before the announcement — Hy-MT2 was created 05-11 and announced 05-21 per the card's own News section; Kimi K3 was created 06-13 and is dated 07-27 in the corpus. Prefer the card's own News/Updates line, and fall back to `createdAt` only when you say so in the justification.
3. **Unresolved, worth a look:** `nvidia/Alpamayo2-Super` and `nvidia/Alpamayo-1.5-10B` are real, reasonably-followed autonomous-driving foundation models (100 and 94 likes) but their dates are contradictory — the Alpamayo2-Super card says "published August 4, 2026" while the API gives `createdAt` 2026-05-27 and `lastModified` 2026-08-07. I skipped both rather than guess. Someone who can resolve NVIDIA's card-date semantics could add two rows.
4. **Also left on the table:** `tencent/HY-World-2.0` (2026-04-10) and `tencent/Hy-Embodied-RxBrain-1.0` (2026-07, day unknown) — both real Tencent releases I judged either not clearly notable or not datable. The remaining tier-2 publishers `poolside` and `inclusion_ai` are still at zero coverage and got no slot this run; `inclusion_ai`'s Ling-3.0-flash and LLaDA2.2-flash are the obvious flagship candidates there.
5. Two tier-2 slots went to mistral and alibaba_qwen and the third to stepfun; the cap of three per session was reached exactly.

## Friction and proposals

Six entries appended to `logs/friction.jsonl`: the transient-5xx retry that succeeded;
alibaba_qwen's dead index URLs; xAI's 403 bot wall; the HuggingFace candidate-quality
problem and the API that fixes it; the in-place version replacement at `tencent/HunyuanOCR`
that the schema has no way to express; and Meta's second consecutive undocumented release.

Nothing new appended to `PROPOSALS.md` — the HuggingFace API point is a concrete process
improvement, but it is the same underlying request as the previous run's
`document_index_urls:` proposal, and repeating it would be noise rather than evidence.

`logs/open_issues.json` is empty, so there were no issues to investigate and no comments
filed. `blocked_escalations` in `candidates.json` is empty; no document was found dead.
