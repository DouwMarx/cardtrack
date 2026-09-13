# cardtrack run 2026-09-13T07:04Z-local

Corpus at start: 309 documents (274 active, 32 removed, 3 moved).
Written this run: 2 adds, 5 version annotations. No status changes, no field
updates, no issue comments.

## Run condition: Phase A failed completely

`logs/run-20260913-070456Z.log`:

```
{"checked": 277, "ok": 0, "not_found": 0, "blocked": 0, "errors": 277, "moved": 0,
 "marked_dead": 0, "fingerprint_checked": 42, "new_versions": 0, "candidates": 259,
 "candidates_new": 0, "updated_docs": 20}
[run_daily] MONITOR OUTAGE: all link checks errored (network down?)
```

Every fetch errored. This is the recurring transient-outage pattern (2026-08-14,
08-18, 08-21, 08-25). The explicit `MONITOR OUTAGE` line is **new** and is what
the 2026-08-21 proposal asked for at the log level — worth recording as a partial
fix. It does not yet reach the agent's inputs: `candidates.json` was written
anyway with `candidates_new: 0` and no `degraded` flag.

Consequences for today:

- No link-checking, so no dead- or moved-URL detection across 277 active documents.
- No fingerprinting, so no revision detection. (`fingerprint_checked: 42` with
  `ok: 0` again reports work that cannot have happened.)
- The index diff contributed nothing. Both adds came from the stale candidate
  backlog and from a hand sweep.

My own fetches all succeeded from ~07:15Z onward, so the outage was transient. I
re-swept the highest-yield index surfaces by hand to compensate: OpenAI
Deployment Safety Hub, DeepMind model-cards index, `research.meta.ai/blog`,
`epoch.ai/latest`, `metr.org/research`, `apolloresearch.ai/research`,
`transluce.org/news`, `far.ai/blog`, `thinkingmachines.ai/blog`, `aisi.gov.uk/work`,
`docs.mistral.ai/models/model-cards`, NIST CAISI research blog,
`safer-ai.org/research`, `anthropic.com/news`, and the HuggingFace API sorted by
`createdAt` for Qwen, moonshotai, deepseek-ai and tencent. `openai.com/news` and
`x.ai/news` returned 403 to my fetcher (alive, bot-walled — the known agent-side
wall, covered by search instead).

## 1. Phase A candidate triage

`candidates.json` carried 259 links, `candidates_new: 0` (see above). I triaged
the full backlog rather than the empty tail. Almost everything already resolves
against the corpus:

Already catalogued, no action — GPT-6 Astra system card, ChatGPT Images 2.5
system card, Gemini 3.8 Flash model card, the Gemini 3.8 Flash Cyber /
Fairwind access policy, Muse Spark 1.3, DeepSeek `news260910` (V4.1-Flash),
`tencent/Hy4-preview-FP8`, `inclusionAI/LLaDA-Image-Turbo`,
`claude.com/programs/team-plan-for-scientists`,
`anthropic.com/news/enterprise-frontier-safeguards`, and the Apollo
contrastive-belief-updates post — each is already a row or already a
`related_urls` entry on one.

**Proposed:**

| document | verdict |
|---|---|
| `huggingface.co/inclusionAI/LLaDA-UI` | `written` — `inclusion-ai-llada-ui-model-card`, doc 310, v555 |
| `epoch.ai/publications/long-context-latency-scaling-gpt-vs-claude` | `written` — `epoch-ai-gpt-5-6-terra-independent-eval`, doc 311, v556 |

**LLaDA-UI** (created 2026-09-06) is a ~16.7B MoE block-wise diffusion
vision-language GUI agent on the LLaDA2.0-mini-base backbone — a computer-use
agent, inside `covered_model_class` and inside InclusionAI's `sources.yaml`
scope, and the first LLaDA-line GUI agent in the corpus. Notability evidence
outside the repo: project page at `inclusion-ai.org/LLaDA-UI`, a public GitHub
repo carrying the technical report, and an inclusionAI-run demo Space. No safety
evals (`has_safety_evals: false`), no risk domains. Weights are public but the
repo declares no license, so `openness` was omitted rather than guessed.

**Epoch latency report** — admitted under `when_uncertain: admit_and_flag` and
flagged as a reversible call; see §7.

**Skipped, with reasons:**

- *Not model documentation:* Anthropic Model Hardware Standard preview,
  Fermat's Last Theorem post (internal model identified only by comparison —
  fails the named-model requirement), econ-scenarios; Mistral funding round,
  Cloudera partnership, legacy-code-modernization; every `x.ai/news/grok-bot-*`
  item; all Cursor product and changelog posts; Meta agentic-AI explainers;
  DeepMind AlphaGenome Atlas; RAND `PEA4957-1` and `WRA5251-1` (policy analysis,
  no named model); METR's own security-incident update; Palisade podcast pages;
  Transluce tool/trust-center pages.
- *Methodology with no named-model results:* DeepMind
  `piloting-the-worlds-first-double-blind-ai-evaluations` (fetched — an
  architecture announcement; names Gemini Flash Lite as the pilot subject but
  reports no results), AISI `optimal-stopping` (fetched — introduces `optstop`,
  names no models), Redwood `proposal-for-tracking-the-effects` (fetched — a
  transparency proposal, no models evaluated).
- *Auxiliary or out-of-publisher-scope:* `tencent/AuK` and `AuK-Flash` (speech
  generation/editing/TTS; consistent with the 2026-09-10 skip and the open scope
  question in that PROPOSALS entry), `tencent/Ex-Omni` (fetched — external
  authors, Feb 2026 paper, outside the Hy line), `tencent/EVIE-8B` and
  `EVIE-4.5B` (visual document retrieval), `tencent/Hy-MT2-1.8B-GGUF` (machine
  translation), `tencent/ContextPilot-*` (context-management RL models, not
  flagship), Meta Muse Voice Transcribe (ASR), `nvidia/RE-USE`,
  `NemotronLabs-AI-for-Media-Sports-Tennis`, `magpie_tts_*`,
  `inclusionAI/ArmorOCR-GGUF`.
- *Variants of covered models:* every `-NVFP4`/`-FP8`/`-fp4`/`-int4`/`-GGUF`
  repo (including NVIDIA's quantizations of other orgs' models),
  `LLaDA2.2-mini`, `Ling-3.0-flash-Fin` and its precision siblings,
  `Ling-3.0-flash-VL-*`, `nvidia/Nemotron-3-Labs-Ultra-Math-SFT`/`-RL` (olympiad
  fine-tunes of Nemotron-3 Ultra, already covered).
- *Not notable / no outside-repo announcement:* `nvidia/SDLLM-*-1.7B-Base`.
- *Noise:* HF user profiles, dataset repos, discussion threads, collection
  pages, and the ~60 `ai.google/*` navigation links the Gemini-for-Science index
  surfaces in bulk (excluded by that publisher's `scope` note).

## 2. Targeted search

Lookback: last success `2026-09-12T06:30:58Z`, so the ~72 h floor applies.

No new qualifying documents. Checked and found nothing new: OpenAI (hub newest
is GPT-6 Astra, 09-03; the 09-09 card update is a revision the pipeline tracks),
DeepMind model-cards index (newest Gemini 3.8 Flash, 09-02), Anthropic news
(09-01 and 09-10, both held), Meta (09-02 and 09-08, both held), xAI (Grok 4.7
publicly slipped past its 09-11/09-12 window — no card, no model page, no API
id), Mistral, Epoch, METR, Apollo, Transluce, FAR.AI, SaferAI, US CAISI, AISI,
Thinking Machines, Moonshot, DeepSeek, Qwen, Tencent, Xiaomi, StepFun.

Orgs silent >14 days, with the reason where I established one: `xiaomi`
(no new HF repo since 2026-04-27 — silence is real), `stepfun` (newest release
still Step 3.7 Flash, May 2026), `moonshot_ai` (newest repo Kimi-K3,
2026-06-13), `apollo_research`, `far_ai`, `saferai`, `us_caisi`, `metr`,
`thinking_machines`, `uk_aisi`, `mistral` — index pages fetched, nothing newer
than what the corpus holds. `poolside`, `palisade_research`, `rand`, `cursor`,
`nvidia`, `tencent_hunyuan` not separately swept beyond their candidate entries.

Restricted-access sweep: polled Rosalind Biodefense, Daybreak, Project
Glasswing, Claude Mythos access, the Life Sciences Verification Program, the
Cyber Verification Program, Claude Science, Gemini for Science, Fairwind and
DeepMind–Isomorphic Bioresilience. All corresponding primary documents are
already catalogued. One near-miss worth naming: Bloomberg reported on 2026-09-10
that ENISA has been granted access to Mythos 5 and is testing it. I found **no
primary Anthropic post** for it — `anthropic.com/news` lists nothing between
09-01 and 09-10 — so nothing was proposed. If Anthropic publishes an EU-access
post, it is an `access_policy` add.

## 3. Citation mining

Fetched SecureBio's *Introducing VCT v2* (09-11) and Anthropic's
*conventional weapons capabilities* report (09-10). External references are to
FrontierMath, BixBench/FutureHouse, Phylo.bio, WMDP, DoD JP 3-60, GeoText and
YFCC100M — no allowlisted publisher's uncatalogued document among them. Redwood's
09-11 CoT-controllability post already carries its OpenAI sub-page reference as a
`related_urls` entry.

No retrospective sweep: today is Sunday.

## 4. Open issues

`logs/open_issues.json` is `[]`. **Unverified** — with all 277 Phase A fetches
failing there is no `fetch_status` field to distinguish "no open issues" from
"could not reach GitHub". I proceeded on the assumption of none and logged the
assumption. No comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is `[]`, consistent with `blocked: 0, not_found: 0` — but
only because `ok: 0`. Nothing was checked, so nothing could be found blocked.
Task 5 had no honest input today and the empty list should not be read as a
clean bill of health.

## 6. Document update summaries

20 pending diffs, all HuggingFace model cards. Reviewed 10, annotated 5 (budget).

| slug | version | verdict |
|---|---|---|
| `deepseek-deepseek-v4-flash-0731-model-card` | 539 | `written` |
| `moonshot-ai-kimi-k3-model-card` | 535 | `written` |
| `deepseek-deepseek-v4-pro-model-card` | 534 | `written` |
| `moonshot-ai-kimi-k2-6-model-card` | 537 | `written` |
| `alibaba-qwen-qwen3-8-27b-model-card` | 529 | `written` |

Substance: V4-Flash-0731 gained Terminal-Bench 2.1 82.7 and Toolathlon Verified
70.3 and filled in a blank Deep-SWE score at 54.4; Kimi-K3 gained ExtractBench
83.17/94.64/69.64 and dropped WildClawBench and MDPBench; V4-Pro filled in
SWE-bench Verified at 80.6 and added Multilingual 76.2 while dropping
WildClawBench Overall 43.7; Kimi-K2.6 gained SWE-bench Multilingual 76.7 and
dropped OmniDocBench 89.76/90.08; Qwen3.8-27B swapped ExtractBench for ParseBench
70.79/88.28/59.77.

**Skipped as noise:** `tencent-hunyuan-hy3-preview-model-card` v552 (download
counter 56,428 → 59,468 plus one leaderboard row reordered),
`nvidia-nvidia-nemotron-3-ultra-550b-a55b-model-card` v547 (counter down, one
row reordered, heading pluralised "Collection" → "Collections"),
`xiaomi-mimo-v2-5-pro-model-card` v546 (counter plus one reorder), and
`tencent-hunyuan-hy3-model-card` v545 (counter, Spaces count, and a leaderboard
reorder; the one real element — SkillsBench swapped for WildClawBench — carries
no reported figures, so there is nothing factual to quote). The remaining 10
diffs were not reached within the budget of 5 annotations.

This is the 2026-09-07 HF-widget-churn finding reproducing unchanged; the
suggested fix (sort the `Evaluation results` rows before diffing) would have
collapsed four of these to zero-line diffs *and* made the five real ones legible,
since in v529 and v534 the actual change is a score appearing where a blank row
was — easy to lose inside a reorder block.

## 7. Friction and proposals

Four `friction.jsonl` lines: `phase_a_total_failure_silent` (with the new
`MONITOR OUTAGE` log line noted as a partial fix), `monitor_gap` (tasks 4 and 5
had no verifiable input), `ambiguous_criteria` (the Epoch call), and
`diff_noise_source_identified` (confirming 2026-09-07).

One `PROPOSALS.md` entry, dated 2026-09-13: **the system-card test has no answer
for performance and cost studies of named models.** The Epoch latency report is
the subject of the measurement, so it clears the "merely uses models" carve-out,
but long-context serving latency is a deployment property rather than a
capability or a risk. I admitted it and flagged it in the row's `notes`; the ask
is one sentence in `criteria.yaml` settling the class, since Epoch produces this
shape several times a month. If the answer is "out of scope",
`epoch-ai-gpt-5-6-terra-independent-eval` is the only row to revert.

## Housekeeping

Proposal records were staged at `logs/.proposal_tmp.json` (the harness blocks
both heredocs into `--json -` and writes outside the working directory, so the
`/tmp` path recorded in the 2026-09-01 PROPOSALS entry was not available this
run). The file holds the last proposal submitted and can be deleted.
