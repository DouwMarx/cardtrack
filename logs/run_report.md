# cardtrack run report — 2026-09-23 (run_id `2026-09-23T06:15Z-local`)

## Headline

Phase A recovered: `checked: 302, ok: 299, blocked: 3, errors: 0` after five days of total fetcher
failure, delivering **266 genuinely new candidates** — the first real index diff since 09-18.

It landed on a big release day (Claude Opus 5.5, Grok 4.7 and MiMo-V2.6 all shipped 2026-09-21/22),
and **the agent got three of fifteen add slots**, because the 12-document Z.ai/MiniMax backfill had
already consumed the rest of the rolling 24 h cap. Three adds `written`, three annotations `written`,
and **three verified-in-scope documents left unwritten**. See §7 — this is the run's main finding and
is filed in `PROPOSALS.md`.

| | |
| --- | --- |
| Proposals submitted | 7 |
| `written` | 6 (documents 335, 336, 337; versions 605, 608, 613, 614) |
| `rejected` | 1 (cap, not merit) |
| `duplicate` / `noop` | 0 |
| Candidates triaged | 266 (today's crop) |
| `annotate_version` | 3 of 20 diffs; 17 skipped as noise |
| Issues handled | 0 (none open) |
| Blocked-URL escalations | 0 (`blocked_escalations: []`) |
| Process defects filed | 1 (`PROPOSALS.md`), 4 friction entries |

---

## 1. Phase A candidate triage

`logs/candidates.json`: 519 entries, of which **266 first seen `2026-09-23T06:18:27Z`**. The older
slices (09-09 → 09-19) were triaged by prior runs; I worked today's crop. The volume is inflated
because Z.ai and MiniMax were allowlisted this week, so their entire HuggingFace org pages enumerated
at once (~200 of the 266 are `zai` / `minimax` HF user profiles, GitHub repo links, dataset cards and
discussion threads).

### Written

| document | verdict |
| --- | --- |
| xAI — *Model Card: Grok 4.7* (2026-09-21), `model_card` | `{"status": "written", "slug": "xai-grok-4-7-model-card", "document_id": 335, "version_id": 615}` |
| Anthropic — *System Card: Claude Opus 5.5* (2026-09-22), `system_card` | `{"status": "written", "slug": "anthropic-claude-opus-5-5-system-card", "document_id": 336, "version_id": 616}` |
| METR — *Summary of METR's predeployment evaluation of Claude Opus 5.5* (2026-09-22), `independent_eval` | `{"status": "written", "slug": "metr-claude-opus-5-5-independent-eval", "document_id": 337, "version_id": 617}` |

**Grok 4.7** — read in full (28 pp., from `x.ai/safety`). Tagged `cbrn`, `cyber`,
`harmful_manipulation`, `societal_harm` on the strength of dedicated sections: cyber capabilities and
safeguards (CyberGym, CVE-Bench, HackerBench v0.3, CathedralBench); biological and chemical
capabilities and safeguards (BioSecBench, VCT, Biosecurity VCT, BioUseBench, WMDP, LAB-Bench,
ProtocolQA, BixBench); behaviors (MASK-Rectified, sycophancy); child safety, CBRN refusals and
self-harm refusals. `loss_of_control` deliberately **omitted**: the card's autonomy claims sit in the
coding-capability sections, with no scheming, sandbagging or AI-R&D-acceleration evaluation.
`closed` (public API via console.x.ai, no weights).

**Claude Opus 5.5** — written with an explicit caveat recorded in the row. The PDF exceeds my fetch
tool's 10 MB limit and **I could not read its body**; title and date are confirmed by the PDF's
indexed metadata, by METR's post citing this exact URL, and by the launch announcement. Risk domains
(`cbrn`, `cyber`, `loss_of_control`, `societal_harm`) are drawn from the announcement (biology
capability exceeding Opus 5; Gray Swan prompt-injection work; 85% reduction in containment-boundary
circumvention; usage-policy, wellbeing and bias-and-integrity evaluations) and are deliberately
conservative — **`harmful_manipulation` is left off and should be re-checked**, since Anthropic system
cards normally carry a sycophancy section. Canonical URL follows the existing convention: every other
Anthropic system card in the corpus is catalogued under its `www-cdn.anthropic.com` address, and
`anthropic.com/document/claude-opus-5-5-system-card` is a 307 redirect to it, not a second document.

**METR Opus 5.5** — read in full; AI R&D acceleration across five tasks (Budget NanoGPT Speedrun,
LMCA, Train a Program, Gaming Bot, Sunlight). Tagged `loss_of_control` per the AI-R&D convention. The
post states it did **not** cover time horizons or sabotage.

### Co-publication check

`TASK.md` asks for one search per model card. Cursor co-published the Grok 4.5 and 4.6 cards
(`cursor.com/blog/grok-4-5-model-card`, `cursor.com/resources/grok-4-6-model-card.pdf`) and Grok 4.7
ships as a Cursor default model — but `cursor.com/blog` links straight out to `x.ai/news/grok-4-7`,
and `cursor.com/docs/models/grok-4-7` is product documentation, not a card. **No Cursor copy exists
for 4.7.** Nothing to propose or record.

### Checked and deliberately skipped

- `deploymentsafety.openai.com/chatgpt-images-2-5` — already `openai-chatgpt-images-2-5-system-card`.
- `securebio.org/blog/evaluating-superhuman-biological-capabilities/` (2026-09-22) — fetched and read.
  A **methodology essay** on evaluating past-human-expert biology capability (chess analogy, VCT
  trendlines); names Claude Opus 4, GPT-5 and Gemini 2.5 only in passing, with no per-model results.
  Fails the system-card test.
- `securebio.org/blog/introducing-vct-v2/` and `.../tracking-pathogen-variants-...` — the first is
  already catalogued under its Substack URL (same-publisher mirror, no proposal per `TASK.md`); the
  second is wastewater metagenomics, no model content.
- `anthropic.com/news/accenture-embedded-evaluation` — partnership announcement, no named model.
- `x.ai/news/grok-voice-transcribe-2` — transcription model; auxiliary task model, out of
  `covered_model_class` absent safety evals. `x.ai/news/grok-bot-customer-support` — product post.
- `epoch.ai/publications/the-plunging-price-of-thought`,
  `epoch.ai/data-insights/math-preprints-disclosed-ai-use` — cost/adoption trend analysis, no named
  model evaluated.
- `safer-ai.org/research/open-problems-in-ai-risk-modeling...` — workshop report, no model results.
- `mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier` (funding round),
  `.../legacy-code-modernization` (customer solutions post) — both out of Mistral's scope note.
- `minimax.io/blog/minimax-h3`, `.../minimax-speech-28`, `.../minimax-music-3-0` — video, speech and
  music models, explicitly excluded by the `minimax` scope note. `minimax.io/models/text/m27` and
  `/m3` are already catalogued (`minimax-minimax-m2-7-model-card`, `minimax-minimax-m3-model-card`).
- `zai` HF/docs crop — `GLM-5.3-Flash` and `GLM-5.3` are already catalogued; `GLM-5.3-Flash-BF16`,
  `GLM-5.2-FP8` are quantised re-uploads, `GLM-OCR`/`GLM-ASR`/`GLM-TTS`/`CogVideo`/`CogView` are
  excluded by the scope note; the rest is HF user profiles, benchmark repos, spaces and nav.
- `nvidia` crop — `Cosmos-H-Surgical` is already catalogued; `Kumo-Anomaly`/`Kumo-Forecast`
  (anomaly/forecast), `Qwen3.8-27B-NVFP4` (quantisation re-upload), Nemotron-Labs math SFT/RL
  checkpoints and datasets are all excluded by the scope note.
- `tencent` crop — `EVIE-8B`/`EVIE-4.5B` (visual document retrieval), `Hy-MT2-1.8B-GGUF` (machine
  translation, quantised) excluded by the scope note; the remainder are arXiv paper links.
- HF user profiles, discussion threads, dataset cards, `huggingface.co/papers/*` links and
  social/nav links across all publishers — not documents.

---

## 2. Targeted search (window 2026-09-20 → 2026-09-23)

`.agent_last_success` = `2026-09-21T07:03:58Z`, so the 72 h floor governs: searched back to 09-20.

**Restricted-access program sweep** — polled the named programs. Two apparent finds, **both already
catalogued**, which is a good sign for the pipeline:

- Anthropic's *Introducing the Life Sciences Verification Program* (2026-09-17) → already
  `anthropic-claude-mythos-5-1-access-policy-2` (added by the 09-21 run).
- OpenAI's *Expanding Daybreak as the Cyber Defense Window Narrows* and the Daybreak trusted-access
  help-centre overview → both already in the corpus, cross-referenced to each other.
- GPT-Rosalind left research preview on 2026-09-11 and `gpt-rosalind-research` was added to the
  Trusted Access Program; the three existing `openai-gpt-rosalind-access-policy*` rows cover this.
  No new document surfaced for the expansion itself.
- No news on an Anthropic **Cyber Verification Program** launch, Project Glasswing, or LSVP expansion
  beyond US organisations. Nothing new from Gemini for Science / Co-Scientist / labs.google.

**Frontier releases** — Gemini 3.8 Flash (09-02), GPT-6 Astra, Claude Fable/Mythos 5.1, DeepSeek
V4.1-Flash all confirmed already present. Nothing found from UK AISI, Apollo, Transluce, US CAISI,
SaferAI, Palisade or FAR.AI inside the window.

---

## 3. Citation mining + retrospective sweep

Today is a **Wednesday**, so the no-recency-filter retrospective sweep did not run (last ran 09-21:
palisade_research, apollo_research, poolside — no misses).

Citation mining on this week's adds: METR's Opus 5.5 post cites only the Anthropic system card
(written today, cross-linked both ways). The Opus 5.5 announcement cites Frontier Design and Gray
Swan — neither is an allowlisted publisher and neither has a standalone evaluation document; noted
rather than proposed, per the co-publication rule. The Grok 4.7 card's 28-page reference list is
benchmark citations (CursorBench, CyberGym, VCT, WMDP, MASK), not predecessor cards or third-party
evals. **No citation leads worth proposing.**

---

## 4. Open issues

`logs/open_issues.json` is `[]`. Nothing to investigate, nothing to comment. Phase A ran cleanly this
run (`errors: 0`), so unlike 09-13 and 09-21 the empty list is credible rather than an artefact.

## 5. Blocked-URL escalations

`blocked_escalations` is `[]` while Phase A reported `blocked: 3` and `moved: 2` — the sixth
consecutive run where fetch failures did not reach the agent through the documented channel (logged
repeatedly since 09-12, already in `PROPOSALS.md`). With `ok: 299` the affected rows are a small
minority and I have no list to act on. **No `status_change` to `dead` proposed.** Separately, every
URL I fetched by hand today was alive.

---

## 6. Document update summaries

20 entries in `logs/updated_docs.json`; **3 annotated, 17 skipped as noise.**

| diff | verdict |
| --- | --- |
| `anthropic-claude-fable-5-1-access-policy` v605 | `written` — new methodology disclosure: Fable 5.1 was evaluated with production safeguards enabled; Fable 5.1 and Fable 5 scored **zero on OSWorld 2.0** where safeguards intervened, Fable 5 zero on AutomationBench, and cyber/biology tasks were completed instead by Claude Opus 4.8 and Claude Opus 5. Verified verbatim on the live page. The rest of that diff *is* noise (footnote bodies and eight Further-reading link labels collapsed to bare numerals, `1 of 22` → `1`) and is excluded from the summary. |
| `stepfun-stepaudio-3-realtime-model-card` v608 | `written` — the arXiv report was **revised to v2 on 19 Sep 2026** (v1 937 KB → v2 367 KB). Abstract and headline scores unchanged, so the body changed silently; worth flagging for anyone citing the launch-day version. |
| `nvidia-cosmos3-edge-model-card` v614 | `written` — NVIDIA **narrowed the card to Cosmos3-Edge alone**, deleting the family release history and per-model parameter counts. Verified against the live card. |
| `nvidia-cosmos3-super-model-card` v613 | `written` — the same edit on the sibling card, leaving only `Cosmos3-Super: 64B`. |
| `poolside-laguna-m-1-model-card` v606 (336+/58−) | **skipped — extraction noise, despite being the largest diff.** The "additions" are site chrome the extractor previously stripped (`Skip to content`, logo/press-kit block, nav duplicated, `Menu`) plus links split onto their own lines; the "removals" are benchmark chart labels. No prose or score changed. |
| `deepseek-v4-pro` v573, `deepseek-v4-flash-0731` v578, `tencent-hunyuan-hy3` v609, `nvidia-nemotron-3-ultra` v611, `nvidia-nemotron-3-super` v612, `xiaomi-mimo-v2-5-pro` v610, `inclusion-ai-ling-3-0-flash` v607 | **skipped — HuggingFace widget churn.** Download counters, "Spaces using" counts, re-templated Transformers/vLLM snippets, and Evaluation-results rows reordering (the `chat/completions` → `completions` curl rewrite is HuggingFace's own snippet template, identical on both DeepSeek cards). Applying the 09-21 discriminator: leaderboard rows swap in and out — MMLU-Pro and Long-Horizon-Terminal-Bench appearing on DeepSeek-V4-Pro and Nemotron-3-Ultra, SWE-bench Multilingual vanishing from Nemotron-3-Super and Hy3, MathArena AIME 2026 appearing on Nemotron-3-Super — across **seven cards from six unrelated publishers in one fetch window**. That is HF-side model-index linkage churn, not six publishers revising their cards on the same morning. |
| `metr-gpt-5-independent-eval` v589 and the remaining 09-16/09-18 entries | skipped previously as copyedits/chrome; unchanged assessment. |

⚠️ **Data-quality flag for the operator** (not actionable by me — `model_names` on an existing row is
a judgement call I would rather not make unilaterally): the two Cosmos3 rows now **overstate what
their documents cover**. `nvidia-cosmos3-edge-model-card` lists four `model_names` and
`nvidia-cosmos3-super-model-card` lists five, but each card now documents exactly one checkpoint. The
other variants may have moved to their own repos; I did not verify that, so I annotated the versions
and left `model_names` alone.

---

## 7. The cap — main finding

`propose_doc.py` rejected my fourth add:

```
{"status": "rejected", "reason": "cap_exceeded: max_new_documents_per_run (rolling 24h)",
 "run_id": "2026-09-23T06:15Z-local"}
```

after **three** agent proposals. `_count_recent_actions` counts changelog `add` rows over 24 h with
no actor dimension, so the 12-document Z.ai/MiniMax backfill left the agent 3 of 15 slots, and there
is no way to see the remaining budget before spending it. I ranked correctly by luck, not design.

**Not written, all verified in scope, all re-findable from `candidates.json`:**

1. **Xiaomi MiMo-V2.6** family card — `huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL`, 2026-09-22, MIT,
   Pro 1.02T-A42B + Flash 309B-A15B, announced at `mimo.mi.com/docs/en-US/updates/model`.
   `open_weight_permissive`, `has_safety_evals: false` (capability benchmarks only). *Submitted and
   rejected by the cap — the proposal is at `/tmp/p_mimo26.json` if the operator wants to replay it.*
2. **Alibaba Qwen-Image-2.1** — `huggingface.co/Qwen/Qwen-Image-2.1`, unified text-to-image and image
   editing, 7B, Qwen Research License (`open_weight_restrictive`), announced at
   `qwen.ai/blog?id=qwen-image-2.1`. Image generation is explicitly inside `covered_model_class`.
   No safety evaluations on the card.
3. **Redwood Research — *Astra is much better at reasoning with filler tokens than previous models***
   (2026-09-23) — independent eval of GPT-6-Astra, Claude Opus 4.5, Claude Opus 5, GPT-5.6-Sol and
   DeepSeek-V3.2 on reasoning with filler tokens under a no-chain-of-thought instruction. Astra goes
   ~10% → ~50% on 4-hop reasoning and ~60% → ~90% on AIME with filler tokens while the others stay
   flat; the authors read this as substantial unverbalised cognition that complicates monitoring.
   `loss_of_control`, `has_safety_evals: true`, `closed`.

Filed in `PROPOSALS.md` with three suggested fixes: give the cap an actor dimension; expose
`adds_remaining` so a run can rank before spending; and make the rejection name the numbers.

---

## 8. Friction logged

Four entries appended to `logs/friction.jsonl`:

- `cap_starvation` — the above.
- `unfetchable_but_alive` — the Opus 5.5 system card PDF exceeds the 10 MB fetch limit, so a frontier
  system card was catalogued without its body being read, and `harmful_manipulation` is likely
  under-tagged as a direct result. Third recurrence of the >10 MB Anthropic PDF wall. Phase A has a
  50 MB limit and does not share it — if it stored text for document 336, tomorrow's run can finish
  the tagging from `data/text/`.
- `tooling` — heredoc/inline JSON still refused (all 7 writes went via `/tmp/*.json` + `--json <path>`);
  compound Bash commands and `for` loops refused; Bash has no network. **Correction to the 09-21
  run's conclusion:** appending to `friction.jsonl` and `PROPOSALS.md` *is* possible via the 09-11
  `Edit`-the-last-line recipe, which is how today's entries were written.
- `duplicate_cdn_url` — xAI serves the Grok 4.7 card from at least two hashed CDN stems
  (`card4p7-3a96f40b.pdf`, linked from `x.ai/safety` and the one I catalogued, vs
  `4p7card-5eccc980.pdf` from search). I did not fetch or propose the second; `canonical_url` is
  operator-only and I cannot tell a mirror from a revision here.

**Still unmerged from 09-21:** `logs/friction_pending_2026-09-21.jsonl` (5 entries) and
`logs/PROPOSALS_pending_2026-09-21.md` (2 proposals, including the monitor-fetcher misdiagnosis).
They were staged behind `cat >>` commands on the belief that no append route existed. Two days stale.
