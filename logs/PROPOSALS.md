# Agent proposals

Append-only. The daily agent's only self-improvement channel: dated entries
suggesting process/schema/criteria changes, with evidence from
`logs/friction.jsonl`. Humans read and decide; agents never modify code, schema,
prompts, or criteria. (Lives under logs/ so the sandboxed agent's atomic-write
tools can create their temp files next to it.)

Format:

```
## YYYY-MM-DD — short title
Problem: …
Suggested change: …
Evidence: …
```

---

## 2026-08-09 — Candidate lists surface navigation, not documents; backfill depth ends up decided by the add cap rather than by editorial judgment

Problem: `logs/candidates.json` carried 1694 links this run, of which ~186 survived a keyword
filter and perhaps 20 were actual documents. None of the twelve documents I added today came
from reading that list end to end — they came from fetching four publisher index pages
directly (Anthropic's Transparency Hub Model Report page, OpenAI's Deployment Safety Hub,
DeepMind's model-cards index, AISI's work page), each of which lists title + date + URL in
one place. Meanwhile the add cap bound at exactly 40/40 and I left at least six
verified-qualifying DeepMind cards unproposed. The cap is currently doing the job editorial
triage should be doing: what gets in is a function of the order I happened to check things
in, not of what matters most.

Suggested change: two parts, both small.
(1) Add an optional `document_index_urls:` key per publisher in `sources.yaml`, separate from
    `index_urls:`, for pages that are *listings of documents* rather than news feeds — e.g.
    `https://www.anthropic.com/transparency/model-report`,
    `https://deploymentsafety.openai.com/`, `https://deepmind.google/models/model-cards/`.
    Phase A would surface links from those pages as a distinct, small, high-precision
    `document_candidates` array, leaving the noisy nav-link diff where it is. That turns the
    first part of every run from filtering into deciding.
(2) When the add cap is hit, have the rejection reason carry the remaining slot count, and
    let the run record the verified-but-unproposed backlog in a machine-readable
    `logs/backlog.json` so the next run starts from it instead of rediscovering it. Today's
    backlog survives only as prose in a friction line.

Evidence: `logs/friction.jsonl` entries `cap_exhausted` and `unverifiable_third_party_claim`
(2026-08-09). Candidate-list arithmetic: 1694 links → 186 keyword hits → ~20 documents; of
the 12 documents written this run, none were identifiable as documents from `link_text`
alone. Anthropic's CDN links in particular render as bare hashes with link text "system
card" — no model name, no date, no way to tell the Opus 4.7 card from the Sonnet 4.6 card
without fetching each. The four publisher index pages gave title, date and model
immediately, in every case.

## 2026-08-09 — Write/Edit cannot append to PROPOSALS.md: atomic writes need a temp file in a read-only directory

Problem: `PROPOSALS.md` is documented as one of the agent's four write targets, but the
Write and Edit tools both fail on it with `EROFS: read-only file system, open
'/…/PROPOSALS.md.tmp.2.<hex>'`. They write atomically via a sibling temp file, and the repo
root is read-only in the sandbox even though `PROPOSALS.md` itself is writable. The same
tools work fine under `logs/`, where creating a sibling file is allowed. Today this entry
only exists because a shell append was available; in the headless configuration
(`agent.cmd` restricts Bash to `propose_doc.py` and `comment_issue.py`) the agent's
self-improvement channel would be silently unwritable — and the failure surfaces as an
opaque EROFS on a filename the agent never chose.

Suggested change: make the repo root writable for the `*.tmp.*` pattern, or move the channel
to `logs/proposals.md` (or an append-only `logs/proposals.jsonl`) so it sits in a directory
that already supports atomic writes. Either way, prefer a location where the documented
permission and the tool's actual write mechanism agree.

Evidence: two consecutive tool failures this run, one Edit and one Write, both
`EROFS … PROPOSALS.md.tmp.2.<hex>`, against a file the run contract lists as writable;
`logs/friction.jsonl` was written successfully by the same tool moments earlier.

## 2026-08-12 — Primary sources that fetch "successfully" but carry no document, and ones that now fetch not at all

Problem: two failure modes hit the same run and both end with a real release going
uncatalogued, but only one of them is visible to the pipeline.

(1) **Hard block, correctly surfaced.** `openai.com/index/` now answers the validator and
    every agent-side fetcher with a Cloudflare JS challenge (HTTP 403, body "Enable
    JavaScript and cookies to continue"). My add for OpenAI's 2026-08-10 launch
    announcement of GPT-5.6-Cyber was rejected `document_retrievable=false: HTTP 403`.
    That is the validator working as designed — but it is a regression, not a stable
    property: three `openai.com/index/` documents were fetched and written on 2026-07-21,
    2026-08-04 and 2026-08-07. `deploymentsafety.openai.com` remains fetchable and carries
    no GPT-5.6-Cyber card, so a new frontier cyber model from a tier-1 publisher currently
    has zero first-party documentation in the corpus and no path to acquiring any.

(2) **Soft block, invisible.** `qwen.ai` returns HTTP 200 and an identical 94,358-byte
    client-rendered shell for every URL — `/blog`, `/blog?id=qwen3.8` and
    `/blog?id=qwen3.8-max-preview` are byte-identical and contain zero occurrences of
    "Qwen3.8". A retrievability check that tests status code, content-type and size passes
    on all three. Had I proposed Qwen3.8-Max (2.4T MoE flagship, launched 2026-08-03) from
    its blog URL, the likely outcome is a written row whose stored content is a JavaScript
    shell — a silent corruption, strictly worse than the OpenAI rejection.

Suggested change, in rough order of cost:

- Add a **content-sanity gate** to the validator alongside the existing retrievability
  check: reject when the extracted text is below a small floor (a few hundred characters),
  or when it is byte-identical to a fetch of the same host's index URL. That converts
  failure mode (2) from silent corruption into an honest rejection, and it generalises to
  every client-rendered publisher, not just Qwen.
- Give the fetcher a **headless-render fallback** for hosts flagged in `sources.yaml`
  (`render: js`), which is the only thing that would actually retrieve Qwen's posts and
  is likely to clear Cloudflare's challenge on `openai.com/index/` too.
- Failing that, record hard-blocked but verified documents in a machine-readable
  `logs/unretrievable.jsonl` (url, publisher, date, title, evidence urls) rather than
  letting a rejection be the end of the trail. A missed document is invisible; a rejected
  one at least knows its own name, and today that knowledge survives only as prose in
  `logs/friction.jsonl`.

Evidence, this run: rejection line `{"status": "rejected", "reason":
"document_retrievable=false: HTTP 403"}` for
`https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/`;
`curl` of the three `qwen.ai` URLs returning identical byte counts with no model string
present; `alibaba_qwen` reading 50 days silent in `state_summary.json` (last entry
2026-06-23) across two confirmed August releases. Related friction lines this run:
`rejected_proposal_fetch_blocked`, `index_unfetchable_publisher_silent`.

## 2026-08-13 — HuggingFace-indexed publishers are diffed by page order, not by creation date, and a flagship release sat undetected for five days

Problem: eight allowlisted publishers are indexed wholly or mostly through a HuggingFace org
page (`alibaba_qwen`, `deepseek`, `tencent_hunyuan`, `xiaomi`, `nvidia`, `moonshot_ai`,
`stepfun`, `inclusion_ai`). Phase A diffs the rendered HTML of those pages, which HuggingFace
orders by
recent activity rather than by creation date. A repo that is published and then not touched
does not necessarily appear in the visible listing, so it never enters the diff.

`Qwen/Qwen3.8-2.4T-A95B` — the 2.4T-parameter open-weight release of Qwen's Max-class
flagship, and the largest known hole in this corpus — was created on HuggingFace
**2026-08-08T01:50:52Z** and first appeared in `logs/candidates.json` with `first_seen`
**2026-08-13T06:21:57Z**. Five days. It entered the diff only because the repo was modified on
2026-08-12. During those five days two runs recorded `alibaba_qwen` as silent (51 days at the
start of today's run) and filed the release as unreachable, because both runs went looking for
it at `qwen.ai`, whose blog serves an identical JavaScript shell for every URL. The document
was fetchable the whole time, at a URL under an index we already poll.

The 2026-08-12 run did run a creation-date-sorted HF API sweep, and that is exactly the method
that would have caught this — but it was an ad-hoc agent-side sweep covering the five orgs the
agent happened to suspect (stepfun, moonshot, deepseek, tencent, xiaomi). Qwen was not among
them, because Qwen's gap had already been attributed to the `qwen.ai` fetch failure. The method
that works is not part of the pipeline, so its coverage depends on which orgs the agent guesses.

Suggested change: for publishers whose `index_urls` point at `huggingface.co/<org>`, have
Phase A call the HF API instead of diffing HTML:

    GET https://huggingface.co/api/models?author=<org>&sort=createdAt&direction=-1&limit=50

and emit each repo as a candidate with its `createdAt`, `likes` and `downloads` attached. That
is one request per org, returns JSON, is ordered by the field that actually defines "new", and
carries the popularity signal the `notable_release` judgement needs — which today has to be
recovered by a second API call per candidate anyway. It would also let the diff be keyed on
repo id rather than on link presence, so a release is detected the day it appears regardless of
whether anyone touches it afterwards.

Secondary benefit: the same JSON makes the quantization/variant filter mechanical. Of the four
Qwen and InclusionAI repos in this window, `-FP8`, `-int4` and `-fp4` siblings share a
`createdAt` minute with their parent and carry an order of magnitude fewer likes
(`Qwen3.8-2.4T-A95B` 600 likes vs `-FP8` 133; `Ling-3.0-tiny` 198 vs `-int4` 19 and `-fp8` 18).
That pattern is currently re-derived by hand every run.

Evidence: `logs/friction.jsonl` entry `hf_index_detection_lag` (2026-08-13). Creation dates via
the HF API: `Qwen/Qwen3.8-2.4T-A95B` 2026-08-08, first_seen 2026-08-13. `alibaba_qwen` last
catalogued document before today: 2026-06-23. Two prior runs' prose on this gap:
`logs/run_report.md` (2026-08-12) and the second entry dated 2026-08-12 in this file.

## 2026-08-14 — A whole-sweep failure is indistinguishable from a quiet day, and the run continues as if nothing were missing

Problem: Phase A this morning reported `checked: 203, ok: 0, errors: 203, candidates_new: 0`
and Phase B logged `error connecting to api.github.com` twice. Every single fetch failed —
a transient network outage during the 07:00:36Z window. The run did not stop, did not retry,
and did not mark its output as degraded. What it handed the agent was a `candidates.json`
whose newest `first_seen` is 2026-08-13 and an `open_issues.json` of `[]` that may or may not
reflect GitHub's actual state.

Both artefacts are *shaped exactly like a quiet news day*. Nothing in them says "I could not
see". I only knew because the `errors: 203` counter is in the run log, and I re-swept all 43
configured `index_urls` by hand at 07:05Z — 43/43 returned HTTP 200, five minutes after 203/203
had failed. The other half of the loss is invisible even in the log: `linkcheck:
all_active_every_run` and the 15% fingerprint sample did not run for any of the 202 active
documents, so today produced no dead-URL detection, no moved-URL detection and no new-version
detection at all.

Suggested change, in order of cheapness:

- **Retry the sweep before giving up.** If more than half of the index fetches error in a pass,
  sleep 60s and repeat the failed set, up to three times. A 30-second outage should not cost a
  day of monitoring.
- **Make degradation a field, not a log line.** Emit `"degraded": true` and
  `"index_fetch_failure_rate": 1.0` at the top level of `candidates.json`, and have the agent
  contract say: when `degraded` is true, sweep the index set yourself before concluding that a
  publisher is silent. Today I did that by accident; the next agent may not read the run log.
- **Fail loudly at 100%.** A pass where *every* fetch errors is never a real-world state. That
  should exit non-zero and leave the previous `candidates.json` in place rather than overwrite
  it with a no-op diff.

Evidence: `logs/run-20260814-070036Z.log` (the counters above and the two GitHub connection
errors); my re-sweep of the same 43 URLs at 07:05Z with `cardtrack.fetch` returning 200 for all
of them, including `www.anthropic.com/news`, `deploymentsafety.openai.com`,
`deepmind.google/models/model-cards/` and every HuggingFace org page; friction line
`phase_a_total_failure_silent`.

## 2026-08-14 — `index_urls` poll pages, not publication paths: three publishers file model documentation where nobody is looking

Problem: the allowlist gates *who* is in scope, and `index_urls` decide *where* we look for
them — but a publisher's `index_urls` are typically its blog, and several publishers file their
actual model documentation somewhere else entirely. Three separate cases surfaced in one run:

- **`mistral`** publishes canonical model cards at `docs.mistral.ai/models/<slug>`, catalogued
  at `docs.mistral.ai/models/model-cards/`. Neither is an `index_url`; only `mistral.ai/news/`
  is. Mistral read **108 days silent** this morning. That page listed **nine** in-scope 2026
  cards missing from the corpus; I proposed eight and all eight were written, including
  **Shieldstral 1.0**, a 3.8B open-weight moderation model released 2026-08-04 — ten days old,
  and a safety-tooling release at that. The corpus already holds `mistral-medium-3-5-26-04`
  from that exact catalogue, so a previous run reached it by hand without the pipeline
  learning the path.
- **`anthropic`** polls `/news`, `/research` and `/transparency/model-report`. **Project Deal**
  (`anthropic.com/features/project-deal`, 2026-04-24) is a 69-participant agentic-marketplace
  experiment measuring Claude Opus 4.5 against Claude Haiku 4.5 — a quantitative
  model-comparison study under `/features/`, which nothing polls. Undetected for 112 days; it
  surfaced only because yesterday's multiagent-systems report cites it.
- **`openai`**'s only `index_url` is `deploymentsafety.openai.com`. The GPT-5.6-Cyber launch
  and evaluation post is at `openai.com/index/…` (written this run as id 217), and the Deployment
  Safety Hub says explicitly that its system card comes "at a later date". The three OpenAI
  documents catalogued before it were all found by agent search on `openai.com/index/`, never by
  the pipeline.

Suggested change: treat "where does this publisher file model documentation?" as a maintained
field rather than an accident of whoever wrote the allowlist entry.

- Add the three known-missing paths now: `https://docs.mistral.ai/models/model-cards/`,
  `https://www.anthropic.com/features/`, `https://openai.com/news/` (or `/index/` if it
  enumerates).
- Add a `doc_index` marker distinguishing "blog/news feed" from "model-card catalogue" in
  `sources.yaml`. A catalogue page is worth diffing on every run and worth a louder alert when
  a new entry appears; a blog is mostly noise. Today's ratio makes the point: 43 index pages
  yielded two genuine leads, while one unpolled catalogue page yielded nine.
- Make prolonged silence trigger a path audit, not just a search. A publisher at >30 days
  silent should prompt "find this publisher's model-card catalogue and check it is in
  `index_urls`" — the silence signal was correct for Mistral for 108 days and nobody asked
  where the cards actually live. `xiaomi` (109 d), `poolside` (108 d) and `palisade_research`
  (99 d) are the next three to audit this way; today's HF-API sweep confirms `xiaomi` has
  published no new repo since 2026-04-27, so its silence looks real, but Mistral's looked real
  too.

Evidence: friction lines `index_url_incomplete` ×2 this run; written ids 208–216 (Mistral) and
218 (Project Deal); `config/sources.yaml` `mistral.index_urls` and `anthropic.index_urls`;
`logs/state_summary.json` last-publication dates per publisher.
