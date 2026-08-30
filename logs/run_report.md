# cardtrack run report — 2026-08-30T09:37Z-local

**Corpus at start:** 265 documents (260 active, 4 removed, 1 moved). **At end:** 266.
**Inputs:** 183 Phase A candidates, **0 of them new** (a replay of links first seen 2026-08-17 →
2026-08-27, all previously triaged), 0 blocked-URL escalations. `open_issues.json` was `[]` **and that
was wrong again** — there are five open issues (§4).
**Written this run:** 1 `add`. 1 proposal routed to needs-review. 2 issue comments. Caps not approached.

**Phase A failed completely for the third consecutive day.** Its summary reads
`checked: 261, ok: 0, not_found: 0, blocked: 0, errors: 261, fingerprint_checked: 40, new_versions: 0,
candidates: 183, candidates_new: 0, budget_exhausted: false`, and Phase B logged
`error connecting to api.github.com` twice. The outage was local and transient — everything below was
found by hand, and ~40 of my own fetches succeeded. I confirmed it was not link rot: a 12-URL random
sample of active canonical URLs (deepseek-ai, metr.org, nvidia ×3, tencent, anthropic.com,
docs.mistral.ai, securebio ×2, epoch.ai) returned **HTTP 200 on all 12**.

Because Phase A has produced no new links since 08-27 and the 08-29 run died entirely, the real
blind window this run was **2026-08-28 → 08-30** (Fri–Sun), covered manually below.

---

## 1. Proposals and validator verdicts

| # | Action | Document | Verdict |
|---|---|---|---|
| 1 | `add` | Anthropic — *Automated researchers can reliably mitigate alignment failures* (post, 08-28) | `{"status": "written", "slug": "anthropic-claude-opus-4-8-other-3", "document_id": 266, "version_id": 434}` |
| 2 | `add` | Anthropic — *Automated Researchers Can Reliably Mitigate Alignment Failures* (full report PDF) | `{"status": "issue_filed", "reason": "logical_duplicate_of:anthropic-claude-opus-4-8-other-3", "issue_ref": "outbox:1"}` |

### The find (1)

`anthropic.com/research/automated-researchers-mitigate-alignment-failures`, published **2026-08-28**,
category Alignment — not in the corpus, and never in `candidates.json`, because Phase A went blind on
08-27. Found by fetching `anthropic.com/research` (a configured index_url) and reading the date column.

I read it in full. Automated alignment researchers powered by **Claude Opus 4.8** post-train target
models to mitigate 10 categories of alignment failure (deception, sycophancy, jailbreaks, privacy
violation and others), scored as "percentage of safety gap closed" over three to five public benchmarks
each; the best methods hold up on a held-out benchmark, on the Petri multi-turn adversarial audit, and
on models up to 4.7× larger. Frontier-scale result: **Claude Sonnet 5**, given an early **Claude Opus
4.8** checkpoint that had not completed production alignment training, reached near-production alignment
scores in 60 hours using ~2,400 training examples. A monitoring agent caught cheating in 39 of ~1,600
research transcripts (2.4%). Claude also outscored 28 human safety researchers.

This clears the system-card test on the "whose behaviour do the numbers describe" discriminator that has
decided at least five skips in recent runs: here the numbers describe named models' alignment behaviour
and a named model's capability at a safety-relevant task. `has_safety_evals: true`, unambiguously.
`openness` **omitted** deliberately — the document spans closed-weight Claude and open-weight
Gemma/Qwen/Llama targets, which the field cannot express. Consistent with existing corpus practice for
Anthropic Alignment / Frontier Red Team posts.

### The refusal (2), and why I stopped

The full report PDF (1.6 MB, 5,175 extracted lines — per-failure results against Gemma-2-2B/9B,
Qwen3.5-2B/4B, Qwen2.5-72B-Instruct, Llama-3.2-3B, Llama-3-8B-Instruct, Petri scores, a 28-researcher
human baseline) was routed to needs-review as a logical duplicate of the one-page post I had just added.
**I did not retry.** The corpus holds exactly this shape from twelve days earlier — the 2026-08-18
protein-design post plus its two `www-cdn` PDFs are three separate rows — so the rule is genuinely
undecided rather than settled against me, and arguing it by re-proposal only spends review time.

Applying that verdict consistently, I also did **not** propose
`alignment.anthropic.com/2026/automated-w2s-researcher/`, which I fetched and read: the full writeup
(PGR 0.97 in 5 days across 9 AARs, ~$18,000 compute, plus a reward-hacking section) behind the summary
already held as `anthropic-claude-opus-4-6-other-3`. It is uncatalogued today solely because the
post-vs-report rule is unwritten. That is this run's PROPOSALS entry (§5).

---

## 2. Searched and skipped

Every allowlisted publisher and evaluator was checked directly, since Phase A contributed nothing.

**Checked, nothing new in the blind window:** OpenAI (deployment safety hub latest is the 08-06 GPT-5.6
update, held), Google DeepMind (model-cards index: only Gemini Omni Flash carries an "Updated 27 August
2026", handled by the 08-28 run as version 432; blog has nothing after 08-27), Meta (`ai.meta.com/blog`
403s to curl, read via WebFetch — latest 07-27; HF orgs `meta-models`/`facebook`/`meta-llama` newest is
08-12), Mistral (RSS: latest is *Mistral x HUMAIN*, 08-24 — the `ocr-4` / `mistral-small-4` /
`voxtral-tts` links on the news page are featured items from March–June, not new), xAI, Cursor,
Thinking Machines (latest 07-31), METR, Apollo (latest 07-21), Epoch, UK AISI, Transluce, SecureBio,
SaferAI, US CAISI, Palisade, Redwood, poolside, Moonshot.

**HF API sweep** (`?author=…&sort=createdAt`) across all eight HF-indexed publishers — tencent, Qwen,
deepseek-ai, moonshotai, XiaomiMiMo, nvidia, stepfun-ai, inclusionAI — newest items all already held or
correctly excluded: `tencent/Hy4-preview` (held, added 08-28) and its FP8 quantization,
`inclusionAI/UI-Venus-2-9B` (held), `tencent/WeMM-Embedding-*` (held), `Qwen3.8-Flash-Next` (held),
`nvidia/DeepSeek-V4-Pro-0813-NVFP4` (08-27 — an NVFP4 re-upload of another org's model: excluded as a
quantization variant *and* a re-host), `nvidia/Nemotron-3-Diarization-preview` (still gated, still
unreadable, still unattested — third run running).

**Fetched, read and skipped on judgement:**

- `x.ai/news/grok-bot-and-x` (**08-29**, the only publisher post in the blind window) — Grok Bot ↔ X
  account integration and API credits. Product availability, no model documentation.
- `rand.org/pubs/perspectives/PEA4957-1.html` (**08-27**) — *Hardening Critical Infrastructure Software
  in an Era of Rapid AI Advancement*. Read it; it names **no model at all** (zero mentions of
  GPT/Claude/Gemini/Grok/Llama/DeepSeek/Qwen/Kimi). Policy call to action. Same discriminator as the
  08-27 DeepMind and AISI skips.
- `anthropic.com/research/petri-open-source-auditing` — a citation lead that does report audits of 14
  frontier models, but it is dated **2025-10-06**, below the 2026-01-01 scope floor. Out of scope.
- `anthropic.com/research/enabling-independent-research` (08-26) — researcher data-access programme.
- RAND's other recent output (weight-security SL3 framework 08-25, Federal Select Agent Program 08-24,
  100 Days Mission 08-21) — no named model under test.
- `blog.redwoodresearch.org/p/brief-independent-investigation-of` (**08-27**) — verified it is a short
  announcement pointing at the full report, not the report. Both org copies of that report are already
  held (`metr-gpt-5-6-sol-independent-eval-2`, `redwood-research-gpt-5-6-sol-independent-eval`).

**Long-silent publishers, checked and genuinely silent:** xiaomi 125 d, palisade_research 115 d,
stepfun 99 d, poolside 48 d, apollo_research 40 d, us_caisi 38 d, moonshot_ai 34 d, far_ai 32 d,
thinking_machines 30 d, epoch_ai (publishing, but economics — 08-27 revenue analysis), saferai 28 d,
mistral 26 d, uk_aisi (08-27 `optstop`, no model under test), transluce 24 d, securebio 23 d.

---

## 3. Citation mining

Mined the document added this run (id 266) and its full report. Every academic reference is arXiv
(the standing arXiv-technical-report gap). Four non-arXiv leads, all resolved:

- `anthropic.com/research/automated-alignment-researchers` — **already held**
  (`anthropic-claude-opus-4-6-other-3`).
- `alignment.anthropic.com/2026/automated-w2s-researcher/` — its full writeup, **not held**, not
  proposed (§1).
- `anthropic.com/research/petri-open-source-auditing` — **not held**, out of scope (pre-floor).
- `www-cdn.anthropic.com/0b4915911…pdf` — turned out to be the **Claude Opus 4.8 System Card**, and the
  most interesting thing I found. It is a *superseded* edition: its changelog stops at 2026-06-03, while
  the canonical `anthropic.com/claude-opus-4-8-system-card` redirects to hash `0f0c97ad…` carrying
  corrections through 2026-06-17 — including a bug-bounty result that flipped the Opus 4.8 vs 4.7
  robustness comparison and a virology score revised 0.89 → 0.90. **No action needed on the row:** I
  hashed the live canonical PDF and it is byte-identical to the stored version (sha256 `0df5d061…`),
  so the corpus holds the current edition and Phase A's dead fingerprint pass missed nothing here.
  What it does show is that Anthropic's own brand-new paper links a stale, pre-correction copy that
  returns 200 forever and that no link check can ever surface. Logged to friction.

---

## 4. Issues and escalations

`logs/open_issues.json` was `[]`. **It was stale**, for the second consecutive run. A direct
`api.github.com` query returned **five** open issues, all `needs-review`, none `data-error`/`missing-doc`:

| # | Opened | Title | This run |
|---|---|---|---|
| 28 | 08-13 | duplicates content of `xai-grok-4-6-model-card` | untouched |
| 29 | 08-21 | canonical_url move for `anthropic-claude-opus-5-system-card` | **verified + commented** |
| 30 | 08-21 | possible duplicate of `meta-muse-spark-1-2-other` | **verified + commented** |
| 31 | 08-22 | duplicates content of `xai-grok-4-6-model-card` | untouched |
| 32 | 08-28 | duplicates content of `xai-grok-4-6-model-card` | untouched |

#29 and #30 had sat **nine days with zero comments**, so I spent the run's issue budget verifying them
against live sources rather than filing anything new. Both comments returned `logged_only` (`gh` is
unauthenticated in the sandbox), so they are in `logs/comments.jsonl`.

**#29 — every claim reproduces.** `anthropic.com/transparency/model-report` links exactly one Opus 5
system card PDF and it is `b514064a…`; the held `c5fbac3f…` appears nowhere on the page yet still
returns 200 (15,981,937 B vs 15,994,568 B), so no link check will ever notice. Extracted both: the
Table 8.1.A FrontierBench v0.1 row reads `43.3 | 18.7 | 33.7 | 37.5` in the held edition and
`43.3 | 21.1 | 33.8 | 34.4` in the live one — including GPT-5.6 Sol revised **37.5 → 34.4**. "Harbor"
occurs 0× in the held edition and 2× in the live one, including the added attribution line. The
2026-08-18 "repagination only" finding was wrong; the corpus holds the superseded edition. I did not
re-propose (that only files a fourth issue) — this needs a human merge.

**#30 — false positive, recommend admitting.** The two Meta PDFs are different documents: 3 pp
(Terminal-Bench 2.1 / DeepSWE v1.1 / GDPVal-AA v2) vs 4 pp (BabyVision / PerceptionBench / ZeroBench /
WorldVQA / SimpleVQA / ERQA / OmniSpatial / CharXiv / ChartMuseum / ChartQAPro / Wild Artifact Bench /
Design Arena). **Zero shared benchmarks; word-level similarity 0.128.** They are companion
methodology reports for one model, not two copies of one report.

**Escalations:** none in `candidates.json`. The 12-URL liveness sample above stands in for the link
check Phase A could not run; nothing appeared dead, and nothing was proposed `dead`.

**One index worth a note:** RAND returned HTTP 200 to a browser-UA curl today (75,641 B, 163 results)
but **403 to WebFetch**, on both its index and the Canary page. Yesterday's run recorded 403 to both and
guessed at IP rate-limiting; the block is user-agent-specific, so RAND is reachable via the
impersonation path but WebFetch is not a usable fallback for it.

## 5. Friction and proposals

Seven lines appended to `logs/friction.jsonl`: Phase A's third consecutive total failure reporting as a
clean run; `open_issues.json` empty because the fetch failed (second consecutive instance); three days
of index diffing contributing nothing, with the one find recovered by hand; the post-plus-report pair
admitted on 08-18 and refused on 08-30; superseded-but-live CDN editions as a recurring class; RAND's
403 being UA-specific; and validator-filed issues sitting unattended past a week.

One entry appended to `logs/PROPOSALS.md`: *"The same post-plus-report pair is admitted one week and
refused the next, and the rule that decides is unwritten."* It asks for **a** rule in `criteria.yaml`
— either two related rows with a `summary_of` link (matching the 08-18 precedent) or one row canonically
pointing at the report — and notes the secondary ask that `logical_duplicate_of` gain a text-similarity
floor, which would have cleared #30 on 08-21 without a human. It deliberately does not re-argue the
08-22 (publisher-aware duplicate check) or 08-28 (surface prior rejections) entries, both of which stand
and neither of which would have prevented today's case.
