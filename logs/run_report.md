# cardtrack run report — 2026-08-23T06:22Z-local

**Corpus at start:** 250 documents (246 active, 3 removed, 1 moved). **Written this run:** nothing.
**Proposed this run:** nothing — `propose_doc.py` was not invoked, so there are no validator verdicts to
report. **Filed as needs-review:** none. **Open issues:** `[]`, again not verifiable from inside the
sandbox — see task 4. **Blocked-URL escalations:** none in `candidates.json`.

A zero-write run. The finding is that it is a *verified* zero rather than an assumed one: Phase A failed
totally today, so the run began with no usable input, and I rebuilt the sweep by hand to establish that
there was genuinely nothing to add.

## Phase A failed totally, for the sixth time and the second in three runs

```
checked: 247, ok: 0, not_found: 0, blocked: 0, errors: 247, moved: 0, marked_dead: 0,
fingerprint_checked: 38, new_versions: 0, candidates: 2688, budget_exhausted: false, candidates_new: 0
```

`ok: 0` against `checked: 247`. `candidates_new: 0` here does not mean "a quiet day"; it means the phase
never ran. This is the failure the 2026-08-21 proposal describes in full, recurring unchanged — and the
three derived zeros are as uninformative as that entry predicted: `marked_dead: 0` and `blocked: 0` are
not observations because no active document was link-checked, and `fingerprint_checked: 38 /
new_versions: 0` cannot be distinguished from 38 failed fetches, so the silent-revision sweep also did not
happen while appearing to.

The fetch layer itself was healthy. Between 08:25Z and 08:38Z I made **39 successful fetches across 24
hosts** from my own tools without a single transport failure. Whatever breaks Phase A is inside Phase A.

`candidates.json` was still written, and still reports 2688 candidates — all of them previously
adjudicated links, newest `first_seen` 2026-08-22. There was nothing in it to triage (task 1) and
`blocked_escalations` is empty (task 5).

## What I did instead: the index sweep, redone by hand

I re-checked **every publisher and evaluator on the allowlist** — 17 publishers, 12 evaluators, 29 orgs —
against 29 index pages, and read 10 documents in full where an index entry looked like it might qualify.

**Fetched clean and found nothing new (25 orgs).** Anthropic (`/news`, `/research`,
`/transparency/model-report`), OpenAI (`deploymentsafety.openai.com`), Google DeepMind (`/models/model-cards/`,
`/discover/blog/`), Meta, Mistral, Cursor, Alibaba Qwen, DeepSeek, Tencent Hunyuan, NVIDIA, Xiaomi,
Moonshot AI, StepFun, InclusionAI, poolside, Thinking Machines, METR, UK AISI, Apollo Research, Epoch AI,
SecureBio, Transluce, US CAISI, SaferAI, FAR.AI, Palisade, Redwood.

**Bot-blocked to me as well as to the pipeline (3 orgs).** `x.ai/news` (403, both with and without the
trailing slash), `openai.com/news/` (403), and RAND's Project Canary page (403). Covered by
site-restricted search instead, which is index-lagged rather than direct — a document published at any of
these three in the last day or two would be invisible to Phase A *and* to me. Logged to friction.
Incidentally, `sources.yaml`'s note that Meta's blog bot-blocks scripted fetches is now stale: it served
me fine.

Everything the sweep surfaced was already in the corpus. The near-misses, and why each was skipped:

| surfaced | date | disposition |
|---|---|---|
| `transluce.org/scaling-activation-oracles` | 08-20 | **skipped** — methods research; the oracles are the thing evaluated, the named models are activation donors |
| `transluce.org/elicitation-scaling-laws` | 08-19 | **skipped** — same; safety-relevant results *about a method*, on a named subject model (Qwen3.6-27B) |
| `securebio.substack.com/p/building-a-three-day-early-warning` | 08-21 | skipped — grant announcement, no model |
| `securebio.substack.com/p/securebio-detection-updates-august` | 08-20 | skipped — biosurveillance ops, no model (also skipped 08-21) |
| `mistral.ai/news/agentic-search` | 08-20 | skipped — retrieval product, not a model (also skipped 08-21) |
| `anthropic.com/research/riemann-zeta` | 08-10 | **skipped** — capability showcase, and the model is "an unreleased research version of Claude", unnamed |
| `anthropic.com/news/claude-text-watermark` | 08-14 | skipped — product/feature explainer, not model-specific |
| `blog.redwoodresearch.org/p/ai-swarms-are-starting-to-pose-indirect` | 08-12 | skipped — takeover-risk essay, no named model assessed |
| `metr.org/blog/2026-08-14-funding-update` | 08-14 | skipped — org funding announcement |
| `cursor.com/blog/joining-spacex` | 08-14 | skipped — corporate announcement |
| `epoch.ai` — 5 August items | 08-06→08-14 | skipped — labour-market and chip-economics data insights; no named-model evals |
| `huggingface.co/tencent/UI-Mate-9B`, `UI-Mate-democua-27B` | 08-14 | already covered — the existing `ui-mate-27b` row lists all three names |
| `huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0` | 08-03 | already in corpus (id from 08-03) |
| `huggingface.co/moonshotai/Kimi-K3` | 07-27 | already in corpus; HF "updated 3 days ago" is a repo revision, i.e. fingerprint-sweep work that did not run today |
| `huggingface.co/inclusionAI/*` — Ling-3.0 base/midtrain/30T, `-dspark`, `SingGuard-2b` | 08-20/21 | already covered, or excluded as checkpoint/draft variants (draft-model gap logged 08-22) |
| `huggingface.co/XiaomiMiMo/MiMo-V2-Flash` | — | **out of scope** — HF API `createdAt` 2025-12-16, before the 2026-01-01 floor. See below. |

**Third-party releases I could not propose:** Z.ai GLM-5.2 Turbo (2026-08-17) and ByteDance Seedance 2.5
(2026-08-08). Neither publisher is allowlisted. Noted, not proposed — same disposition as the GLM card
Mistral serves, recorded on 08-22.

### The one thing that looked like a real coverage hole, and was not

Xiaomi is the corpus's longest-silent publisher at 118 days, and two live repos in its HF org —
`MiMo-V2-Flash` and `MiMo-V2-Flash-Base` — have no row. Both show "Updated Jul 9", the same bulk
org-wide touch as the four catalogued MiMo-V2.5 repos, so from the index they look exactly like the
coverage hole the 2026-08-19 proposal asks for a detector for. They are not: the HF API gives
`createdAt: 2025-12-16T08:47:02Z` and the card's technical report is dated 2025. Correctly out of scope,
and the corpus is right to be silent on Xiaomi.

Worth flagging for whoever builds that detector: `lastModified` (2026-07-09) is what the HF index pages
display and what a detector built on them would key off; `createdAt` (2025-12-16) is what actually decides
scope. They are seven months apart here, and no part of the pipeline currently reads the latter.

## Citation mining (task 3)

Mined the five most recent adds and near-adds — the two SingGuard cards written on 08-22, Tencent
EVIE-Preview-4.5B (08-17), and Anthropic's `/research/Claude-accelerates-protein-design` (08-18) and
`/research/multiagent-systems` (08-13). **No leads.** The multiagent post cites no external evaluator at
all. The protein-design post cites Adaptyv Bio, Twist Bioscience and ProteinBase — wet-lab validation
partners, not model evaluators, and none allowlisted. EVIE-Preview cites the ViDoRe benchmark family and
Illuin's ColPali engine; SingGuard cites only its own arXiv paper (2606.22873) and its Qwen3-VL base.

The pattern across the last several runs is consistent: HuggingFace cards cite benchmarks and base
models, first-party research posts cite their own prior work, and the third-party evaluator references
that citation mining is designed to catch appear almost exclusively in frontier-lab system cards — of
which none were published in this window.

## Issues (task 4)

`logs/open_issues.json` is `[]` for the **third consecutive run**, and for the third consecutive run I
cannot tell whether that means "no open issues" or "could not ask". Re-confirmed today that `gh` in this
sandbox is unauthenticated (`You are not logged into any GitHub hosts`), so I have no independent read on
the backlog. The aggravating detail specific to today: total Phase A failure is the same condition under
which the 08-21 run logged `error connecting to api.github.com` twice, so the run in which the issue
fetch is most likely to have failed is also one where its failure leaves no trace.

**Task 4 is reported as completed against unverifiable input, not as completed-with-nothing-found.** No
issues were investigated and `comment_issue.py` was not called. Logged to friction; not re-proposed, since
the 2026-08-14 proposal and the closing paragraph of the 2026-08-21 entry already ask for exactly the
right fix (a `fetch_status` field distinguishing the two cases).

## Blocked-URL escalations (task 5)

`blocked_escalations` is empty. Note that this is *not* evidence of health today: with `ok: 0`, no
document link-check ran, so nothing could have been escalated. The three 403s I hit are index pages, not
corpus documents, and none of them indicate a dead document.

## Friction logged (6 lines)

`phase_a_total_failure_silent` · `empty_open_issues_list_is_indistinguishable_from_a_failed_issue_fetch` ·
`methods_research_with_named_model_harmful_elicitation_results` ·
`first_party_capability_showcase_with_no_named_model` ·
`pre_scope_floor_model_absent_from_corpus_reads_as_a_coverage_hole` ·
`allowlisted_publisher_index_bot_blocks_the_agent_fetch_too`

## Proposals filed

**None.** Every obstacle this run maps onto an entry already in `logs/PROPOSALS.md`: the Phase A failure
onto 2026-08-21 §1, the unverifiable issue list onto 2026-08-14 and 2026-08-21 §1's closing paragraph,
the Transluce judgement calls onto 2026-08-20's "unwritten discriminator", the draft-model and
pre-floor-re-upload cases onto 2026-08-22 and 2026-08-19, and the bot-blocked indexes onto 2026-08-14.
Re-filing any of them would add a dated restatement and no new ask. The 08-21 entry's three requested
fixes — fail loudly when `ok == 0 and checked > 0`, retry the phase once, break `errors` down by
exception class — are unchanged by today, except that the recurrence rate is now two runs in three.

One honest qualification on that entry's cost argument: on 08-21 the hand-redone sweep recovered a real
document that would otherwise have been lost. Today it recovered nothing. The silent failure cost zero
documents this run, and the case for fixing it rests on the days when it does not.

**Corpus at end:** 250 documents (246 active, 3 removed, 1 moved) — unchanged.
