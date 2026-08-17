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

## 2026-08-17 — The candidate list has no triage state, so a link missed on its first day is missed forever

Problem: `logs/candidates.json` is append-only and stateless. Phase A adds new links with a
`first_seen` stamp and never records what happened to them afterwards — proposed, skipped for a
stated reason, or never read at all are indistinguishable on disk. The agent-side effect is that
each run reads the tail (`first_seen == today`) and treats the other 2,577 entries as settled,
because there is nothing to suggest otherwise.

They are not settled. A keyword scan of the full backlog this morning — model-card /
system-card / technical-report / evaluation URL patterns, minus everything already in the
corpus, minus profile, discussion, dataset and asset noise — returned 176 links, and two of them
were in-scope documents that had been sitting untriaged since the seed sweeps:

- `thinkingmachines.ai/blog/interaction-models/` — **TML-Interaction-Small**, a 276B/12B-active
  from-scratch audio-video-text interaction model, published 2026-05-11, with a full comparative
  benchmark table against GPT-realtime, Gemini 3.1 Flash Live and Qwen 3.5 Omni and a safety
  section reporting Harmbench refusal rates. `first_seen` 2026-08-09T19:39:09Z. **98 days old,
  seen for 8, written today as id 227.** Thinking Machines is a tier-1 allowlisted publisher and
  `thinkingmachines.ai/blog/` is a configured `index_url` — the pipeline surfaced this link
  correctly on day one and every run since has stepped over it.
- `research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf` — the **Cosmos 3** family
  technical report, 2026-06-22, 613k characters, whose `has_safety_evals=false` (zero occurrences
  of "guardrail", "red team", "misuse" or "risk assessment") is exactly the kind of absence this
  corpus exists to make visible. Seen since 2026-08-10, written today as id 228.

This is a different failure from the `index_url` gap reported on 2026-08-14. That one was "we are
not looking at the right pages"; this one is "we looked, we saw it, and it fell on the floor."
Both of today's finds came from pages that are polled and working.

Suggested change: give each candidate a state and let unresolved ones come back.

- Record a per-candidate verdict at proposal time — `proposed:<slug>`, `skipped:<reason>`, or
  absent — written back to `candidates.json` (or a sibling `candidate_state.json`) by
  `propose_doc.py` and by an explicit skip call. A skip reason costs the agent one line and turns
  the backlog from an undifferentiated pile into a work queue.
- Have Phase A surface, alongside `candidates_new`, a small rotating sample of the oldest
  untriaged candidates — say 20 per run. At that rate the current backlog drains in a few months
  and nothing sits invisible for 98 days.
- Report `candidates_untriaged` in the Phase A JSON line. Today it would have read 2,577, which
  is the number that would have prompted this scan on 2026-08-10 rather than 2026-08-17.

Evidence: friction line `candidate_backlog_never_resurfaces` this run; written ids 227 and 228;
`logs/candidates.json` `first_seen` values 2026-08-09T19:39:09Z and 2026-08-10T08:46:59Z against
those two URLs; `config/sources.yaml` `thinking_machines.index_urls` and `nvidia.index_urls`,
both polled successfully in today's Phase A (`checked: 222, ok: 222, errors: 0`).

## 2026-08-17 — The run report is the first thing cut when the agent runs out of turns, and it is the only thing that explains the writes

Problem: the 2026-08-15 run wrote seven documents (ids 219–225) and three field updates, then
exited with `Error: Reached max turns (60)`. Writes had already landed and were committed and
deployed by Phase C. What never happened was `logs/run_report.md`, any `friction.jsonl` line and
any entry here. The next run (2026-08-16) hit a total network outage and also produced nothing.
So this morning the repository contained 225 documents while `logs/run_report.md` described a
corpus of 218 and a run three days earlier, and `friction.jsonl` ended on 2026-08-14 — two days
of silent drift between the database and its own audit trail. The only surviving account of why
ids 219–225 exist is the changelog rows and a one-line commit message.

The ordering is backwards. Proposals are irreversible-ish (a row is live on the public site
within the same run); the report is cheap and is what makes the row reviewable by a human later.
Under a turn cap the expensive irreversible half completes and the cheap explanatory half is what
gets dropped.

Suggested change:

- Write `logs/run_report.md` incrementally rather than once at the end: a stub with the run id
  and inputs at the start, one appended line per proposal as the validator answers. A truncated
  run then leaves a partial-but-true report instead of a stale one.
- Have `run_daily` detect the mismatch — if the changelog has rows for `$CARDTRACK_RUN_ID` but
  `run_report.md` does not name that run id, say so loudly in the run log instead of committing
  quietly as if the run were clean.
- Consider whether 60 turns is the right cap given the contract's seven tasks. It was not
  obviously wrong on 2026-08-15 — that run did the work — but a cap that truncates the record
  rather than the work is worth at least an explicit "reserve the last N turns for the report"
  instruction in the prompt.

Evidence: `logs/run-20260815-082217Z.log` line 9 (`Error: Reached max turns (60)`) against commit
`66538a4` (`add 7, 3 field update(s)`); `logs/run-20260816-132126Z.log` (`checked: 222, ok: 0,
errors: 222`); `logs/run_report.md` as found this morning, headed `run 2026-08-14T07:00Z-local`
and reporting 218 documents; last line of `logs/friction.jsonl` dated 2026-08-14; friction line
`run_report_lost_to_turn_cap` this run.

## 2026-08-17 — One document, two live URLs, and no field to say so

Problem: publishers routinely serve the same document from two surfaces, and the corpus can only
hold one. `documents.alt_urls` exists in the schema, `identity.find_doc_by_url` already dedups
against it, and `propose_doc.py` offers no way to put anything in it. `field_update` accepts
`title`, `notes`, `model_names`, `publication_date`, `canonical_url`, `safety_evals` and
`openness`; the only path that touches `alt_urls` is a `canonical_url` move, which demotes the old
URL — and that path additionally requires the content at the new URL to match a stored version
fingerprint, which can never hold when the twin is a different format.

Three instances in one run:

- **Gemini 3.7 Flash** (written today as id 226) exists as an HTML card at
  `deepmind.google/models/model-cards/gemini-3-7-flash/` and as a PDF at
  `storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-7-Flash-Model-Card.pdf`. Both
  HTTP 200, verified this run. The same twinning holds for Gemini 3.6 Flash and 3.5 Flash-Lite,
  and the corpus is split on which surface it treats as canonical — ids 13 and 14 point at PDFs,
  ids 35–40 at the HTML pages, with no principle distinguishing them.
- **SecureBio** mirrors every Substack post at `securebio.org/blog/<slug>/index.html`. Four such
  mirrors of already-catalogued documents are sitting in the candidate backlog right now
  (Kimi K3 biology assessment, GPT-5.5 pre-release assessment, the Anthropic unredacted CB
  review, and the biosecurity-safeguard piece).
- **xAI** serves cards from both `media.x.ai` and `data.x.ai`.

Two costs. Monitoring: only the catalogued URL is link-checked and fingerprinted, so a revision
published to the twin is invisible — and for the PDF/HTML pairs the PDF is usually the one that
gets revised. Dedup: the guard is URL-based, so the twin is one plausible proposal away from
becoming a duplicate row. My own add of id 226 went through without the validator noticing that
its sibling rows point at the other surface of the same card.

Suggested change: accept `alt_urls` on `add` (a list the agent has actually fetched) and add an
`alt_url_add` / `alt_url_remove` field action that appends without disturbing `canonical_url`.
Fingerprint-match should not gate it — an alt URL makes no claim about which surface is
authoritative, only that both are the same document, which is precisely the claim a curation
agent is positioned to make and a byte comparison is not. Then link-check every URL a document
has, not just the canonical one.

Evidence: friction line `no_field_for_alternate_surface` this run; `cardtrack/propose.py`
`_handle_field_update` (the `canonical_url` branch's `content_fingerprint` requirement) and
`cardtrack/identity.py:38-45`; `notes` on id 226, where this had to be recorded as prose instead.
