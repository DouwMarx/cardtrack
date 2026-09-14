# cardtrack run 2026-09-14T06:17Z-local

Corpus at start: 311 documents (276 active, 32 removed, 3 moved).
Written this run: **5 version annotations, 2 field updates**. No adds, no status
changes, no issue comments.

Phase A recovered from yesterday's outage and ran clean:

```
{"checked": 279, "ok": 278, "not_found": 1, "blocked": 0, "errors": 0, "moved": 0,
 "marked_dead": 0, "fingerprint_checked": 42, "new_versions": 7, "candidates": 265,
 "budget_exhausted": false, "candidates_new": 8, "updated_docs": 20}
```

So unlike 2026-09-13, today's inputs are trustworthy — with one exception noted in §5.

## 1. Phase A candidate triage

8 new links (`first_seen` 2026-09-14T06:20:36Z). All 8 are noise; none proposed.

| lead | publisher | verdict |
|---|---|---|
| `huggingface.co/BoJack` | tencent_hunyuan | HF user profile, not a document |
| `huggingface.co/papers/2609.08936` (AuK Technical Report) | tencent_hunyuan | speech generation/editing/TTS; consistent with the 09-09 and 09-10 skips |
| `huggingface.co/amrn` | nvidia | HF user profile |
| `hf.co/collections/nvidia/medtech-open-models` | nvidia | collection page, not a document |
| `huggingface.co/linjohnss` | nvidia | HF user profile |
| `huggingface.co/papers/2509.22653` (See, Point, Fly) | nvidia | external authors, UAV navigation framework, no NVIDIA model released |
| `huggingface.co/papers/2512.23709` (Stream-DiffVSR) | nvidia | video super-resolution, auxiliary under the `nvidia` scope note |
| `hf.co/collections/inclusionAI/singprobe` | inclusion_ai | collection page |

The 257-link backlog was triaged in full by the 2026-09-13 run and nothing in it
has changed status; I did not re-triage it.

## 2. Targeted search

Last success `2026-09-13T07:17:04Z`, so the ~72 h floor applies (window from
2026-09-11). **No new qualifying documents.** Everything the searches surfaced
resolves against the corpus:

- OpenAI — Deployment Safety Hub newest is ChatGPT Images 2.5 (09-08) and GPT-6
  Astra (09-03), both held. `third-party-cyber-evaluations-involving-openai-models`
  is already a row.
- Anthropic — `anthropic.com/news` has nothing after the 09-10 threat-intelligence
  report, which is already a row. Fable 5.1 / Mythos 5.1 (09-01) held.
  `expanding-project-glasswing`, `claude/mythos` and the Glasswing initial update
  are all already rows or related_urls.
- Google DeepMind — model-cards index newest is Gemini 3.8 Flash (09-02), held;
  the Fairwind / 3.8 Flash Cyber access policy is held. WeatherNext 3, AlphaGenome
  Atlas and "agentic video understanding in Gemini" are in the backlog and stay
  skipped (domain forecasting model, genomics tool, product feature — none is a
  general-purpose generative model and none reports safety evals).
- xAI — Grok 4.7 has still slipped its window with no card, no model page and no
  API id. `docs.x.ai` ends at grok-4.6.
- Meta — `research.meta.ai/blog` newest is 09-08, held.
- Evaluators — METR (`/research`, and `/risk-assessment`, newest 08-26), UK AISI
  (`/work`, newest 08-27), Apollo (newest 07-21), Transluce (newest 08-31),
  Redwood (both 09-10 and 09-11 posts held), Epoch (newest 09-09, the AI Chip
  Users Explorer — a compute-data tool, not model documentation), SecureBio
  (substack archive, newest 09-11 VCT-v2, held), FAR.AI, Thinking Machines,
  US CAISI, poolside. RAND's research-and-commentary index returned 403 to my
  fetcher; covered by search instead, nothing new.

**Restricted-access sweep.** Polled Rosalind Biodefense, Daybreak Blue/Red,
Project Glasswing, Claude Mythos access, the Life Sciences Verification Program,
the Cyber Verification Program, Claude Science, Gemini for Science, Fairwind and
DeepMind–Isomorphic Bioresilience. No new primary documents — but two of the
existing rows changed substantively this week and are annotated in §6, which is
the correct channel for a program whose page updates in place rather than
re-publishing. The `help.openai.com` GPT-Rosalind article that search surfaced is
already a related_url on the Rosalind Biodefense row.

**Orgs silent >14 days**, with the reason where I established one: `xiaomi`,
`palisade_research`, `stepfun` (all three swept in depth — see §3), `poolside`
(newest post 2026-05-11), `apollo_research` (07-21), `far_ai`, `thinking_machines`
(07-31 is both the newest post and the newest row), `us_caisi` (research blog
newest 03-23), `saferai`, `mistral`, `uk_aisi`, `metr`, `cursor`, `rand`.

## 3. Citation mining and the Monday retrospective sweep

**Citation mining.** Fetched the two most recent adds plus the largest recent
primary document:

- Epoch's long-context latency report (doc 311) — references are a code repo and
  two pricing pages. It also names GLM-5.3-Flash, whose publisher (Z.ai/Zhipu) is
  not allowlisted. Nothing to propose.
- inclusionAI LLaDA-UI (doc 310) — references its own paper PDF, project page,
  GitHub repo and demo Space, plus the LLaDA2.0-mini-base backbone (a base variant
  of a covered family, not a distinct release). Nothing to propose.
- The Claude Fable 5.1 & Mythos 5.1 system card (09-01), read from
  `data/text/b0d59ed….txt`. External testing credits METR (§2.3.6, pre-deployment
  AI-R&D assessment), UK AISI and US CAISI, SecureBio, Deloitte and Signature
  Science (§7.2.1 CBRN), and Gray Swan for the indirect-prompt-injection benchmark
  (arXiv:2603.15714). I checked METR's `/research`, `/blog` and `/risk-assessment`
  indexes: METR has published **no** standalone Mythos 5.1 report — the card says
  "they shared the following findings with us", so the METR content exists only
  inside Anthropic's document. Gray Swan and Irregular are both non-allowlisted
  evaluators and are already the subject of the 2026-09-09 PROPOSALS entry; not
  re-raised.

**Weekly retrospective sweep** (today is Monday). Picked the three allowlisted
orgs whose newest corpus entry is oldest: `xiaomi` (2026-04-27),
`palisade_research` (2026-05-07), `stepfun` (2026-05-23). Searched each without a
recency filter.

- **xiaomi** — silence is real. `mimo.mi.com/docs/en-US/updates/model` (a release
  index the pipeline does not watch; `sources.yaml` watches the HF org) lists
  nothing in-scope after MiMo-V2.5 / V2.5-Pro on 2026-04-23, both held. The two
  later items are `mimo-v2.5-asr` (06-02) and the V2.5-TTS series, both excluded
  by the `xiaomi` scope note. `XiaomiMiMo/MiMo-V2.5-DFlash` on HF is not in the
  corpus and not on the release index; I fetched it — 311B, MIT, **empty README**,
  no technical report, no blog post, no safety evals. That fails `notable_release`
  under the HF-org rule (evidence outside the repo is required), so it is skipped
  rather than admitted. Worth re-checking if Xiaomi ever announces it.
- **palisade_research** — silence is **not** real; the watched index is broken.
  This is the sweep's find of the week and is written up in §8.
- **stepfun** — silence is real. Newest HF repo is Step-3.7-Flash and its
  FP8/NVFP4/GGUF variants (May–June 2026), all held or excluded as quantizations.
  No newer Step release exists.

## 4. Open issues

`logs/open_issues.json` is `[]`. Phase A completed all 279 link checks this run,
so unlike 2026-09-13 this empty list is meaningful rather than indistinguishable
from a network failure. No comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is `[]` — but Phase A reported `not_found: 1`, so one
document failed and was dropped before reaching me. Third run in a row for this
pattern. I identified it by elimination: of the 33 rows whose `last_checked` is
not 2026-09-14, 32 are `status: removed` and exactly one is active —
`apollo-research-openai-o3-independent-eval` (doc 75), `last_checked` 2026-09-12.

I fetched its `canonical_url`
`https://www.apolloresearch.ai/science/measuring-reward-seeking-via-contrastivebelief-updates`
and confirmed **HTTP 404**. This is the data error already logged on 2026-09-12:
the stored slug is missing the hyphen in `contrastive-belief`. The document is
alive at the hyphenated URL, which is already recorded as a `related_url`, so:

- **no** `status_change` to `dead` — the document is not gone, the address is wrong;
- **no** `canonical_url` proposal — that field is operator-only.

There is nothing further the agent can do here, which is exactly why the
escalation needs to reach the operator. Logged again as `monitor_gap`.

Useful side-finding: a `not_found` fetch does **not** stamp `last_checked`,
contradicting my 2026-09-12 guess. That is what made the elimination possible.

## 6. Document update summaries

20 pending diffs. Reviewed 13, annotated 5 (budget). Unusually good yield today —
three of the five are genuine access-policy changes rather than HuggingFace churn.

| slug | version | verdict |
|---|---|---|
| `openai-gpt-rosalind-access-policy-2` | 562 | `written` |
| `openai-gpt-5-6-sol-access-policy` | 563 | `written` |
| `openai-gpt-rosalind-access-policy` | 561 | `written` |
| `alibaba-qwen-qwen3-8-2-4t-a95b-model-card` | 557 | `written` |
| `moonshot-ai-kimi-k2-5-model-card` | 536 | `written` |

Substance:

- **GPT-Rosalind (v562)** — the significant one. The page gained a dated
  2026-09-11 update: Rosalind is **out of research preview and available globally
  to eligible organizations** through the trusted-access program, with published
  pricing effective 2026-10-05. The research-preview framing and the
  "will not consume existing credits or tokens" paragraph were removed.
- **Daybreak overview (v563)** — two new FAQ entries: reduced refusals on Astra
  are available to Daybreak **Red** but not Daybreak **Blue** customers (OpenAI
  says it is working on extending them), and Red is open only to approved business
  and enterprise organizations, with no individual application route.
- **Rosalind Biodefense (v561)** — the launch-partner paragraph for Fourth Eon
  Biosecurity and its quote were deleted, with nothing added. A change to the
  documented participant set of a gated program.
- **Qwen3.8-2.4T-A95B (v557)** — Terminal-Bench 2.1, previously blank, now reports
  86.6 (self-reported). Deep-SWE 56.6 and HLE 43.6 only moved position.
- **Kimi-K2.5 (v536)** — gained Apex Agents 14.4, SWE-bench Multilingual 73,
  SWE-bench Pro 50.7 and AIME 2026 95.83; lost the WildClawBench block
  (Overall 30.8, Avg Time 406, Avg Cost 6.6).

**Reviewed and skipped as substantive-but-over-budget** (worth annotating on a
future run if they are still pending): `alibaba-qwen-qwen3-5-397b-a17b` v560
(SWE-bench Verified 76.4 dropped, SWE-bench Multilingual 69.3 and ScreenSpot-Pro
65.6 added), `alibaba-qwen-qwen3-6-35b-a3b` v543 (SWE-bench Pro 49.5 and Verified
73.4 dropped for ParseBench), `moonshot-ai-kimi-k2-7-code` v538 (gained an entire
Evaluation results block: WildClawBench Overall 46.9, LHTB Solved 3),
`alibaba-qwen-qwen3-6-27b` v559 (benchmark set swapped, but every row is
figureless so there is nothing factual to quote).

**Reviewed and skipped as noise:** `anthropic-claude-mythos-5-other` v558 (the
diff is entirely rotating "Read more" teasers in the page's related-research
footer — Fermat's Last Theorem and the unauthorized-access assessment replacing
the protein-design and retraining teasers; the document body is unchanged),
`stepfun-step-3-7-flash` v544 (counter plus one row reorder),
`deepseek-deepseek-v4-pro-0813` v524 (counters plus one figureless row added),
`securebio-claude-opus-4-6-independent-eval-2` v523 (the extractor dropped the
title and subtitle lines; pure extraction noise). `tencent-hunyuan-hy3-preview`
v552, `nvidia-nemotron-3-ultra` v547, `xiaomi-mimo-v2-5-pro` v546 and
`tencent-hunyuan-hy3` v545 were assessed as noise by the 2026-09-13 run and are
unchanged; I did not re-review them.

The 2026-09-07 HuggingFace-widget-churn finding reproduces again: the suggested
fix (sort `Evaluation results` rows before diffing) would have made v557 and v560
legible as insert/delete instead of reorder-shaped churn, and collapsed v544 to
zero lines.

## 7. Field updates

Both came out of the Palisade retrospective sweep, and both preserve the existing
operator notes verbatim.

| slug | change | verdict |
|---|---|---|
| `palisade-research-gpt-5-4-independent-eval` | + `arxiv.org/abs/2605.06760` (kind `paper`) | `written` |
| `palisade-research-grok-4-grok-4-0709-independent-eval` | + report PDF (kind `full_document`), + GitHub repo (kind `code`) | `written` |

The arXiv entry is the same document as doc 190 — same title, same date
(2026-05-07), Palisade authors, same headline results (Qwen3.5-122B 6–19%,
Opus 4.6 81% when replicating Qwen weights) — and the `/research` page names it as
the report's canonical reference. Per TASK.md a full document found for an
existing HTML row goes in `related_urls`, not an `add` and not a `canonical_url`
change.

One honest limitation on doc 191: I confirmed
`palisaderesearch.org/assets/reports/shutdown-resistance-on-robots.pdf` exists
(application/pdf, 7.7 MB) but **could not read its text** — the agent fetch tool
cannot decode PDFs. So the title and date on its first page are unverified; the
filename and the linking page are the evidence. I recorded that caveat in the
entry's note rather than asserting a match I did not check. I also deliberately
did **not** record `arxiv.org/abs/2509.14260`, which the same page links: that is
the earlier September 2025 *Shutdown Resistance in Large Language Models* paper,
not this February 2026 robots report.

## 8. Friction and proposals

Three `friction.jsonl` entries: the unescalated `not_found` (§5); the stale
Palisade source config; and a tooling note recording the one read path that exists
for `related_urls` — submit a `field_update` with a deliberately wrong `old`, and
the validator's `stale_old_value` rejection prints the stored objects with their
kinds and notes. That works and mutates nothing, but it costs one proposal per
read, and it is only necessary because `state_summary.py` flattens `related_urls`
to bare URL strings.

One **PROPOSALS.md** entry, dated today: *Palisade Research's watched index no
longer lists its research reports.* `sources.yaml` watches
`palisaderesearch.org/blog`, which now carries only podcasts, a fundraiser and
policy commentary; every research report, including both 2026-eligible ones, is
listed exclusively at `/research`. Index diffing for this publisher can therefore
no longer surface a research report at all. Two rows already carry the damage —
docs 190 and 191 are catalogued under `/blog/<slug>` URLs that serve only a
`Redirecting…` stub, and versions 508 and 509 stored the stub instead of the
report, with prior runs' operator notes still unactioned.

Worth flagging for the operator: **nothing in the daily pipeline could have found
this.** Link-checking passes (the stub returns 200), the index diff produces
candidates (podcasts), and the org just looks quiet. It surfaced only because the
Monday sweep selects orgs by *oldest newest entry* — which is exactly the signal a
broken channel produces. The proposal suggests generalising that into a standing
check.
