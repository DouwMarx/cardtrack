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

## 2026-08-18 — The corpus can hold a superseded edition and never find out

Yesterday's entry asked for `alt_urls` on the grounds that one document often lives at two URLs.
Today's evidence sharpens the problem: for three Anthropic documents the corpus canonical URL is
not a co-equal surface but an **older edition**, and the publisher's revised edition sits at a
different URL that the pipeline never fetches. Both URLs return 200, so link-checking sees
nothing wrong, and fingerprinting compares the stale file against itself forever.

Verified this run by fetching and paginating both copies of each:

| document | corpus URL | live revised URL | difference |
|---|---|---|---|
| System Card: Claude Mythos Preview | `www-cdn…/8b838020…pdf` (244 pp) | `www-cdn…/08ab9158…pdf` (245 pp) | changelog Apr 8 2026: model-name typos, a §7.9 quote removed because it was misattributed to Mythos Preview but came from Opus 4.6, corrected Eleos AI Research findings |
| Alignment Risk Update: Claude Mythos Preview | `www-cdn…/79c2d46d…pdf` (59 pp) | `anthropic.com/claude-mythos-preview-risk-report` (61 pp) | changelog Apr 10 2026: §§1, 10.2, 5.3.2 revised |
| Risk Report: February 2026 | `www-cdn…/08eca275…pdf` (104 pp) | `anthropic.com/feb-2026-risk-report` (106 pp) | changelog May 26 2026: language METR's pilot external review flagged in §3.4 |
| Claude Opus 5 System Card | `www-cdn…/c5fbac3f…pdf` (193 pp) | `www-cdn…/b514064a…pdf` (194 pp) | repagination only — full word-diff shows no content change |

The fourth row matters as much as the first three: a curation agent can tell a corrected
misattribution from a moved page number, and a byte comparison cannot.

Suggested change, in priority order:

1. **Prefer the publisher's stable named URL as canonical when one exists.** Anthropic serves every
   current system card from `anthropic.com/<slug>-system-card` and redirects it to whichever CDN
   hash is current; the corpus is split between named URLs (Opus 4.7, Opus 4.8, Sonnet 4.6,
   Fable 5/Mythos 5) and frozen hashes (Opus 5, Sonnet 5, Mythos Preview ×2, Opus 4.6, Feb risk
   report). The named URL is self-updating; the hash is a snapshot with a publication date attached
   to it.
2. **Let `field_update --field canonical_url` move a document to a verified newer edition without a
   fingerprint match**, on agent attestation that both URLs are the same document, demoting the old
   URL into `alt_urls`. The current fingerprint-match requirement makes exactly the case that
   matters — the content changed — the one case it forbids.
3. Failing both, at minimum **link-check and fingerprint every URL a document has**, so a revision
   published to a sibling surface raises a new version rather than silence.

Evidence: friction line `canonical_url_holds_superseded_edition` this run; the four documents above,
all fetched and page-counted at 07:45Z; `cardtrack/propose.py` `_handle_field_update`
(`canonical_url` branch) and `_handle_new_version`, which rejects any URL not already on a document
with `unknown_document: … use action=add` — so the revised edition can only enter as a duplicate row
or not at all.

## 2026-08-19 — Two gaps this run: row granularity for multi-size families, and no way to detect coverage holes

### 1. Nothing in the pipeline asks "what has this org published that we don't hold?"

Following a base-model citation out of the `tencent/EVIE-Preview-4.5B` card added on 2026-08-17, I
found that **the entire Qwen3.5 generation is absent from the corpus** — eight post-trained sizes
released 2026-02-16 to 2026-02-28, each with its own HuggingFace card:

| model | created | downloads | likes |
|---|---|---|---|
| Qwen3.5-397B-A17B | 2026-02-16 | 279,886 | 1,552 |
| Qwen3.5-122B-A10B | 2026-02-24 | 2,152,062 | 609 |
| Qwen3.5-35B-A3B | 2026-02-24 | 2,396,631 | 1,489 |
| Qwen3.5-27B | 2026-02-24 | 2,838,192 | 1,029 |
| Qwen3.5-9B | 2026-02-27 | 13,835,311 | 1,834 |
| Qwen3.5-4B | 2026-02-27 | 7,643,691 | 830 |
| Qwen3.5-2B | 2026-02-28 | 3,099,095 | 366 |
| Qwen3.5-0.8B | 2026-02-28 | 2,948,046 | 668 |

`huggingface.co/Qwen` is a configured `index_url` and has been fetched successfully on every run.
The generation was missed anyway, because **Phase A diffs index pages for _new_ links**, and a
February release stopped being a new link in February. Six months of runs, no signal. It surfaced
only because a card added two days ago happened to cite one of these as its base model.

The corpus is thin in the same way elsewhere: 4 Qwen rows total, jumping from Qwen3-era models
straight to Qwen3.6-35B-A3B in April.

Suggested change: a periodic **coverage reconciliation** pass, separate from index diffing. For
each allowlisted org with a machine-readable release surface — the HuggingFace API covers ten of
them and exposes `createdAt`, `downloads` and `likes` directly — enumerate everything published
since the scope floor, subtract what the corpus holds, and write the residue into
`candidates.json` with `source: coverage_gap`. Rank by downloads so the agent triages a
13.8M-download model card before a 200-download SAE probe. This is a query, not a crawl; it is
cheap, and it is the only thing that would have caught this.

Evidence: friction line `index_diff_structurally_blind_to_backlog_gaps` this run; the table above,
from `huggingface.co/api/models?author=Qwen&sort=createdAt`, fetched 08:30Z.

### 2. When each size in a family has its own card, the criteria contradict the corpus

Having found the gap, I could not determine how many rows it should become, and this blocked seven
of the eight proposals above.

- `config/criteria.yaml` says `distinct_model_release` excludes "a size, quantization, checkpoint,
  or regional variant of a model already covered", and that "family cards → one entry, all
  model_names". That reads as **one row** for Qwen3.5.
- But there *is no family card*. Each of the eight is a distinct card with its own architecture
  table and its own benchmark tables. The rule's antecedent — one card covering several variants —
  simply does not hold here.
- And the corpus's own precedent reads the other way: it holds **Qwen3.8-27B** (2026-08-05) and
  **Qwen3.8-2.4T-A95B** (2026-08-08) as two separate rows, which is exactly the dense/MoE pairing
  one generation later. Same for Meta's `muse-glimmer` card/other pair and NVIDIA's Cosmos3 rows.

So the same publisher's releases are being catalogued under two incompatible readings, and a daily
run has no principled way to pick. I proposed only the Qwen3.5 flagship (id 236) and Qwen3.6-27B
(id 235, which has the direct Qwen3.8-27B precedent), and left the seven siblings alone rather than
commit a generation to a guess.

Suggested change: make the rule turn on **documents, not models**, since that is what the database
catalogues. One distinctly-authored card at its own URL is one row; `model_names` merges only what
that one card actually covers (hosted aliases, `-Base` twins, checkpoints listed in its own model
table — the `UI-Mate-27B` case I field-updated this run). Quantizations and re-uploads stay
excluded because they re-publish a card rather than author one. That rule is mechanical, matches
what the corpus already does for Qwen3.8, and would have given a clear answer here: eight rows.
Whatever is chosen, it should be written into `criteria.yaml` explicitly — the current phrasing
assumes a family card exists, and for most Chinese open-weight labs it does not.

Evidence: friction line `family_row_granularity_ambiguous_for_multi_size_open_weight_releases`;
corpus rows `alibaba-qwen-qwen3-8-27b-model-card` vs `alibaba-qwen-qwen3-8-2-4t-a95b-model-card`;
`config/criteria.yaml:12-14`.

### 3. Smaller: `has_safety_evals` asks about framing, not subject matter

Anthropic's protein-design technical report (id 231 this run) reports, with wet-lab validation by
Adaptyv Bio and Twist Bioscience, that Claude Opus 4.8 and Mythos Preview autonomously designed de
novo protein binders at a 27% hit rate against a 10–15% field baseline, and beat an open
competition on RBX1 by 28/90 designs to 9/245. On subject matter that is the strongest bio
dangerous-capability measurement in the corpus. On the letter of the criterion it scores `false`:
the 29-page PDF contains no risk framing, no mitigations and no red-teaming — grep finds no
occurrence of dual-use, biosecurity, misuse, bioweapon or safeguard. The dual-use assessment sits
in the companion announcement (id 233, `has_safety_evals: true`).

Net effect: the site's safety filter surfaces a four-paragraph blog caveat and hides the document
with the numbers in it. I attested honestly in both cases, because the criterion asks what the
document contains — but the split tracks where the publisher put the caveat, not where the safety
signal is. Worth considering a second soft flag (`measures_dangerous_capability`, by domain:
bio, cyber, autonomy, persuasion) so subject matter and framing can be recorded separately.

Evidence: friction line `has_safety_evals_undefined_for_dual_use_capability_report`; ids 231 and
233; `config/criteria.yaml:19-22`.

## 2026-08-20 — Row granularity is now inconsistent inside the corpus, and the system-card test has an unwritten discriminator

Two items. The first is a follow-up that changes yesterday's §2 from "the criteria are ambiguous" to "the
corpus has already answered the same question two different ways". The second is new. There is also one
piece of confirming evidence for yesterday's §1 that asks for nothing beyond what was already proposed.

### 1. The same kind of release is catalogued as one row in one place and two rows in another

Yesterday I reported that `criteria.yaml` gives no answer when each member of a model family has its own
card. Today the corpus itself contains both answers, and a daily run has no way to tell which is
authoritative.

- **One row.** NVIDIA's five Nemotron-Labs Teacher models (Chat, Competition-Coding, General-Reasoning,
  Instruction-Following, STEM; all 2026-08-14) are held as a single row, id 225, with all five names in
  `model_names`. They have five separately-authored cards of ~83 KB each, with different descriptions,
  different training narratives and different benchmark tables, and each card says the model is "released
  as a standalone checkpoint because it is a strong reasoning model in its own right".
- **Two rows.** NVIDIA's two GR00T-H surgical variants have two cards of exactly that kind, and I
  proposed them as ids 237 and 238 this run, on the grounds that they differ in base model
  (GR00T-N1.6-3B vs GR00T-N1.7-3B) and in license (OneWay Noncommercial vs NVIDIA Open Model License).

Both decisions are defensible and they contradict each other. I did not disturb id 225 — re-splitting a
settled row on a daily run is worse than the inconsistency — but that leaves the contradiction in place.

Note also where the id 225 decision is *recorded*: in that row's `notes`, as prose ("Sibling card URLs
covered by this entry: …"). It is not derivable from the criteria, not visible in
`state_summary.json`, and not machine-checkable. The concrete cost this run was a fetch and a diff of all
five Teacher cards before I found that sentence — and the failure mode if I had not opened the database
directly was four duplicate proposals.

Suggested change (unchanged from yesterday, now with a second instance behind it): make the rule turn on
documents rather than models — one distinctly-authored card at its own URL is one row, `model_names`
merges only what that card itself covers. Under that rule id 225 becomes five rows and GR00T-H stays two,
consistently. If instead the family-collapse reading is preferred, then `model_names` needs a companion
field holding the covered sibling URLs, so the decision is queryable rather than buried in prose.

Evidence: friction line `family_row_granularity_ambiguous_for_multi_size_open_weight_releases`
(2026-08-19 and 2026-08-20); corpus id 225 `notes`; ids 237 and 238 this run.

### 2. The system-card test's carve-out has a discriminator that is not written down

`criteria.yaml` says a document qualifies if it "assesses a NAMED model's capabilities or safety" and that
"research that merely uses models does not qualify". Two Transluce posts sit on opposite sides of that
line for reasons the text does not supply.

- **In the corpus:** `transluce.org/weirdchat`, catalogued as an independent eval of DeepSeek-V4-Flash.
  WeirdChat is a methodology contribution; the named model is where the method was pointed.
- **Skipped today:** `transluce.org/elicitation-scaling-laws` (2026-08-19), which trains oversight models
  at five sizes to recover prompts producing exact target responses from Qwen3.6-27B, reports joint power
  laws, and extrapolates the compute needed to match gold prompts (4×10²⁵ FLOPs ≈ $52M in-distribution,
  3×10²⁹ ≈ $376B out-of-distribution), with generalisation shown on WeirdChat's harmful-response prompts.

The rule I actually applied: **do the reported numbers describe a property of the named model, or a
property of the technique applied to it?** WeirdChat's numbers are DeepSeek's behaviours; the scaling
laws are the elicitor's learning curve, with Qwen3.6-27B as fixed substrate. I am reasonably confident
that is the intended reading, and I skipped accordingly — but it is inferable only from precedent, and
precedent is exactly what a daily agent is worst placed to reconstruct. One sentence in `criteria.yaml`
would settle it. If the opposite reading is intended, the elicitation post should be added and this is
the row to add.

Evidence: friction line `system_card_test_ambiguous_for_methods_papers_with_named_subject_model`;
corpus row `transluce-deepseek-v4-flash-independent-eval`; `config/criteria.yaml:8-11`.

### 3. Confirming evidence only — no new ask

Yesterday's §1 (nothing reconciles what an org has published against what the corpus holds) recurred at a
second publisher within 24 hours. Three NVIDIA-Medtech surgical cards — `GR00T-H` (2026-03-15),
`GR00T-H-N1.7` (2026-05-30) and `Cosmos-H-Surgical-Simulator` (2026-03-15) — had been missing for three
to five months and were added this run. None surfaced through a release event: `GR00T-H` entered the
candidate list only because someone edited its README on 2026-08-19, and the other two were found by
following that thread by hand. `huggingface.co/nvidia` is a configured `index_url` that has been fetched
successfully every run, and the corpus already held eight NVIDIA robotics and world-model rows, so this
was not an unmonitored corner. Two accidental discoveries in two consecutive runs, at different
publishers, is weak evidence that the accessible-by-accident subset is small relative to what is missing.
The proposed HuggingFace-API reconciliation pass would have caught all three. Nothing further requested.

## 2026-08-21 — Phase A fails silently in a way that looks like success; and one superseded-edition correction

### 1. `candidates_new: 0` is indistinguishable from `everything errored`, and today it was the latter

Phase A recorded `checked: 237, ok: 0, not_found: 0, blocked: 0, errors: 237, fingerprint_checked: 36,
new_versions: 0, candidates: 2660, candidates_new: 0` at 07:27:18Z. This is the **fifth** occurrence of
the pattern first logged 2026-08-14 (previous instances: 08-14, and 08-18 which called it the fourth).
At 08:05Z I re-swept all 43 configured `index_urls` by hand from the same venv via
`cardtrack.fetch(max_bytes=…, timeout=…)` and got **43/43 HTTP 200**, and every document fetch inside
this run's nine proposals succeeded. The fetch layer is healthy; the failure is transient and total.

Previous entries asserted the consequence. This one measured it. I redid the index diff by hand
against `candidates.json` ∪ corpus URLs and found **94 links present on the index pages and absent
from both**, of which five were content rather than page furniture:

| link | date | disposition |
|---|---|---|
| `research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2` | 2026-08-20 | capability showcase — skipped, but it links the item below |
| `research.meta.ai/static/muse-spark-1-2-multimodal-evaluation-methodology` | 2026-08-20 | **proposed** — 4-page first-party evaluation report, the best find of the run |
| `transluce.org/scaling-activation-oracles` | 2026-08-20 | skipped (methods research) |
| `transluce.org/foundation-models-for-oversight` | 2026-07-28 | skipped (research agenda) |
| `securebio.substack.com/p/securebio-detection-updates-august` | 2026-08-20 | skipped (biosurveillance ops report) |
| `mistral.ai/news/agentic-search` | 2026-08-20 | skipped (retrieval product, not a model) |

Two further losses are invisible in the log rather than merely unrecorded. `ok: 0` means **no active
document was link-checked at all today**, so no `dead` or `moved` link could have been detected — the
run reports `marked_dead: 0` exactly as it would on a clean day. And `fingerprint_checked: 36` with
`new_versions: 0` cannot be distinguished from 36 failed fetches, so the ~weekly silent-revision sweep
also did not happen while appearing to.

**Suggested change.** Make total failure loud and non-silent, in decreasing order of value:

1. **If `ok == 0` and `checked > 0`, treat the phase as failed**: do not write `candidates.json`, do not
   report `candidates_new`, and surface a non-zero exit or an explicit `"phase_a_status": "failed"` key
   that the agent prompt can read. A zero that means "nothing new" and a zero that means "nothing
   worked" must not be the same value.
2. **Retry the whole phase once** after a short backoff before giving up. Five occurrences, all
   transient, all recovering within forty minutes, is the profile of something a single retry fixes.
3. Emit `errors` broken down by exception class. Five runs in, nobody knows *what* fails, because the
   counter is all that survives.

Evidence: `logs/run-20260821-072718Z.log`; friction line `phase_a_total_failure_silent` this run and
2026-08-18, 2026-08-14; the 94-link hand diff described above; the Muse Spark 1.2 multimodal methodology
proposal (`outbox:2`), which exists only because the diff was redone by hand.

Related, same root cause of "an empty value that might mean failure": Phase B logged
`error connecting to api.github.com` twice, so `logs/open_issues.json` is `[]` **unverified** — with the
API unreachable, the fetch cannot distinguish "no open issues" from "could not ask". Suggest a
`fetch_status` field on that file so task 4 can be reported honestly. Both of this run's validator-filed
issues went to `logs/issues_outbox.jsonl` (`outbox:1`, `outbox:2`) rather than to GitHub.

### 2. Correction: the Claude Opus 5 System Card revision is substantive, not cosmetic

The 2026-08-18 entry's table cleared the fourth row — the Opus 5 pair — as "repagination only — full
word-diff shows no content change", and used it as the contrast case for the argument that "a curation
agent can tell a corrected misattribution from a moved page number, and a byte comparison cannot."
**That row was wrong.** Re-diffed today with `pdftotext`, standalone page-number lines stripped, and
`difflib.SequenceMatcher` over the word streams:

| | corpus edition `c5fbac3f…` (193 pp) | live edition `b514064a…` (194 pp) |
|---|---|---|
| Table 8.1.A, FrontierBench v0.1 row | `43.3 \| 18.7 \| 33.7 \| 37.5` | `43.3 \| 21.1 \| 33.8 \| 34.4` |
| FrontierBench attribution | absent | "FrontierBench results in this table are from Harbor's evaluations." |
| FrontierCode effort-decline note | absent | new ~128-word note: the grader penalises out-of-scope refactoring; a scope instruction recovers most of it; scores reported without it |
| §8 opening | "To … it, … used" | "In addition to evaluations by Harbor presented in Table 8.1.A, … our own evaluations on the …" |

The changed row moves Opus 4.8 from 18.7 to 21.1 and competitor GPT-5.6 Sol from 37.5 down to 34.4 in
the headline capability table. `anthropic.com/transparency/model-report` as fetched today links **only**
the 194-page edition; the orphaned hash still returns 200, so no link-check will ever notice. The corpus
and the public site are serving superseded benchmark numbers for a flagship system card.

This makes the 2026-08-18 ask stronger, not weaker, and sharpens it: the argument was "trust agent
attestation over byte comparison." Today's evidence is that **a naive word-diff is not a reliable
substitute for reading either** — pagination noise dominated the diff and an earlier run drew the wrong
conclusion from it. Nothing new is requested beyond item 2 of the 2026-08-18 entry (let
`field_update --field canonical_url` move a document to a verified newer edition on agent attestation,
demoting the old URL into `alt_urls`), but it is worth recording that the current gate produced its
designed outcome — my proposal became needs-review issue `outbox:1` — on a case where the correct answer
was determinable and determined.

### 3. `find_logical_duplicates` fires on house naming conventions

`research.meta.ai/static/muse-spark-1-2-multimodal-evaluation-methodology` (2026-08-20, 4 pp, covering
BabyVision / PerceptionBench / ZeroBench / WorldVQA / SimpleVQA / ERQA / OmniSpatial / CharXiv /
ChartMuseum / ChartQAPro / Wild Artifact Bench / Design Arena) was routed to needs-review as a suspected
duplicate of `meta-muse-spark-1-2-other` (`/static/muse-spark-1-2-methodology`, 2026-08-05, covering
Muse Code and the coding suite). Different URL, fifteen days apart, disjoint benchmark suites, both
linked by Meta from different blog posts, and the content fingerprint — the reliable duplicate test —
did not fire. What fired was Jaccard title similarity ≈ 5/7 = 0.71 against a 0.6 threshold, on the shared
tokens `muse spark 1.2 evaluation methodology`: exactly the words any publisher with a house naming
convention will always share across genuinely distinct documents.

Suggested change: require a third signal before `logical_duplicate` when the fingerprints differ —
publication dates within a launch window (say 7 days), **or** one URL redirecting to the other. Model
overlap plus title overlap alone will keep misfiring on well-organised publishers, which are precisely
the publishers this corpus most wants to track. I proposed the document under its true title rather than
perturbing it to slip past the check, and note that doing so is the only honest option available, which
means the check's false-positive rate is paid entirely in human review time.

Evidence: friction lines `logical_duplicate_false_positive_on_sibling_reports` and
`superseded_edition_misjudged_as_cosmetic` this run; `cardtrack/identity.py:50-91`
(`title_similarity`, `TITLE_SIMILARITY_THRESHOLD = 0.6`, `find_logical_duplicates`).

## 2026-08-22 — A launch-partner co-publication can only be catalogued if you catch it after the first party revises, and the corpus has no way to catch it then either

`propose_doc.py` routed today's Cursor copy of the Grok 4.6 model card to needs-review as
`content_duplicate_of:xai-grok-4-6-model-card` (`outbox:1`). The validator is right on its own terms —
the extracted-text fingerprints were identical — and I have not retried it. The problem is that the
dedup rule and the co-publication rule cannot both be satisfied for this class of document, and the
corpus already contains the pair that proves the class is real.

### 1. The proposable window is empty by construction

The prompt's rule is unambiguous: "each org's own copy at its own URL is a separate document … Never pick
one 'winner'. Copies are often not byte-identical (launch-day vs revised editions)." The corpus honours
it for Grok 4.5: `xai-grok-4-5-model-card` (id 180, Revision 2026-07-20) and `cursor-grok-4-5-model-card`
(id 202, the preserved 2026-07-14 launch-day edition) are two rows.

But consider the timeline a daily agent actually sees:

- **Launch day.** Both orgs publish the same bytes. Whichever copy is proposed second is a content
  duplicate of the first, and gets blocked. This is what happened on 2026-08-13: that run found
  `cursor.com/resources/grok-4-6-model-card.pdf`, verified md5 equality with xAI's copy, and — reasonably,
  facing the same block — recorded it in the xAI row's `notes` instead of cataloguing it.
- **After divergence.** The first party revises; the partner copy is now unique text. But the dedup check
  matches against *any stored version* of the sibling row, not just its current one, and the launch-day
  bytes are still sitting there as version 236. So the partner copy is blocked *permanently*, not just
  until divergence.

I verified the divergence today by downloading both: Cursor serves 524,224 B, md5
`5faf54cc75e26c987541719b7e2d56f1` — byte-identical to the corpus's stored version 236 — with cover
"Revision: 2026-08-12". xAI now serves 540,844 B, md5 `7640cdde745a18a2390cd5fbde55fd55`, "Revision:
2026-08-17". Cursor's copy is now **the only surviving public edition of the launch-day Grok 4.6 card**,
including the pre-correction HackerBench v0.2, Self-harm, MASK and LAB numbers that xAI's changelog says
it corrected. That is precisely the provenance a version-tracked corpus exists to hold, and it is the one
thing the validator will not let in.

Grok 4.5 is in the corpus as two rows only because it was caught after divergence *and* the launch-day
bytes had never been stored on the xAI row. That is luck, not process.

**Suggested change:** make the duplicate check publisher-aware. Identical content under a *different*
allowlisted publisher key is the signature of a co-publication, not a mirror — mirrors are re-hosts under
the *same* or an unaffiliated publisher. Concretely: skip the content-duplicate rejection when the
proposal's publisher differs from the matched document's publisher and both are on the allowlist, and
instead auto-link the two rows (the `notes` cross-reference both rows already carry by hand). If that is
too permissive, a narrower version: only skip it when the proposal names the matched row as its
co-published counterpart, which is checkable from the submitted record.

Either way the deeper issue is that "same bytes" is being used as a proxy for "same document", and for
co-publications it is exactly the wrong proxy: sameness of bytes is what makes them a *pair*, not what
makes them redundant.

**Evidence:** `outbox:1` this run; corpus ids 180, 202, 203 and the `notes` on 203 written 2026-08-13;
friction line `co_publication_indistinguishable_from_mirror_by_content_dedup`; both PDFs downloaded and
hashed this run.

### 2. Confirming evidence only — no new ask

The 2026-08-18 proposal ("The corpus can hold a superseded edition and never find out") now has a
concrete instance with safety content in it. xAI revised the Grok 4.6 card in place five days ago; the
corpus served the stale edition until I opened it by hand for citation mining and proposed version 357.
Phase A fingerprinted 37 of 244 active documents this run, so ~85% of the corpus went revision-unchecked,
and the drift here was not cosmetic — the changelog's substantive line is "Corrected eval results on
HackerBench v0.2, Self-harm, MASK, LAB", four safety and behavioural evals, one of which is quoted in
that row's own add justification. Nothing further requested beyond what that entry already proposes.

## 2026-08-25 — `max_new_versions_per_run` is not per run, and this run silently dropped 10 revision detections

**Problem.** Phase A detected 26 changed documents this morning, wrote 16, and had 10 rejected with
`reason: "cap_exceeded: max_new_versions_per_run (rolling 24h)"` — document ids 123–131 and 133, all
Anthropic research/news pages, because the cap fell at a publisher boundary in fetch order.

This is a cadence/window mismatch, not a burst of publisher editing. `config/settings.yaml` sets
`max_new_versions_per_run: 30`; the validator enforces it over a **rolling 24 h window**; and the
daily run drifts *earlier* each day. Yesterday's run wrote its versions at 06:22:03–06:22:20Z and
today's Phase A wrote its at 06:18:27–06:19:08Z — about three minutes short of 24 h, so all 14 of
yesterday's were still inside the window. I counted the rows directly: exactly 30 in
`document_versions` in the 24 h ending at the first rejection (14 from 08-24, 16 from today). A cap
whose name says "per run" can therefore be 47% spent before a run begins, and the fraction it starts
with depends on nothing more principled than cron drift.

**Why it matters, beyond the arithmetic.** Two distinct harms.

1. *It reports as a clean run.* The Phase A summary line is
   `{"checked": 247, "ok": 247, ..., "new_versions": 16, ...}`. There is no drop count, no
   `cap_exceeded` field, nothing. A run that lost 38% of its revision detections is indistinguishable
   in the log from one where only 16 documents changed. This is the 2026-08-14 proposal's disease
   ("a whole-sweep failure is indistinguishable from a quiet day") one layer down, and it is worse
   here because the run genuinely *did* work — the zeros that would tip an agent off are absent.

2. *Deferral is not the same as safety.* On this occasion the drops are recoverable: ids 123 and 124
   still carry `last_changed 2026-08-19T06:18:54Z` against `last_checked 2026-08-25T06:17:54Z`, so
   the stored fingerprint is still the old one and the next run will re-detect. But recovery is not
   guaranteed to converge. If the daily change rate sits near the cap, the same tail is re-rejected
   every run and which documents survive is decided by fetch order, not by importance. And if a page
   changes *twice* before its retry lands, the intermediate edition is gone with no record anywhere —
   which is precisely the silent-supersession failure the 2026-08-18 entry is about, arriving this
   time through the cap rather than through a missed check. The corpus would jump from the 08-19
   edition to whatever it eventually caught, and nothing would mark the gap.

**Suggested change**, cheapest first:

- **Report the drops.** Add `versions_rejected_by_cap` (or a general `rejected` breakdown by reason)
  to the Phase A summary JSON. One field, and the failure stops being invisible. Do this even if
  nothing else here is adopted.
- **Make the window match the cadence.** Either measure the cap from the previous run's start rather
  than a fixed 24 h clock, or make it genuinely per-run. If the rolling window is deliberate
  anti-runaway protection, size it for two runs (60) so a normal pair of runs cannot collide.
- **Defer instead of reject.** A cap-exceeded revision is not a bad proposal, it is a good one that
  arrived late. Persist the dropped document ids and have the next Phase A fetch them first, so the
  backlog drains deterministically instead of racing on fetch order.

Worth noting the cap did its job in one respect: nothing was corrupted and no bad data was written.
The complaint is only that it discarded work silently and non-deterministically.

**Evidence:** changelog rows for run `2026-08-25T06:17Z-local`, 10 with `action=reject` and
`reason=cap_exceeded: max_new_versions_per_run (rolling 24h)`, document ids 123–131, 133;
`select count(*) from document_versions where fetched_at > '2026-08-24T06:19:09Z' and fetched_at <=
'2026-08-25T06:19:09Z'` → 30; `config/settings.yaml` `caps.max_new_versions_per_run: 30`;
`logs/run-20260825-061717Z.log` Phase A line showing `new_versions: 16` and no drop count; friction
line `rolling_cap_silently_discards_revision_detections`.

## 2026-08-25 — Skip decisions live only in a prose log nothing reads, and today that flipped two published verdicts

**Problem.** The 2026-08-17 entry ("the candidate list has no triage state") and the 2026-08-22
friction line `candidate_list_replays_previously_adjudicated_links` both describe re-adjudication as
*wasted work*. Today it stopped being merely wasteful and started producing contradictions in the
public corpus.

Two links — `research.meta.ai/blog/multimodal-intelligence-of-muse-spark-1-2` and
`api-docs.deepseek.com/news/news260821` — were fetched, reasoned about at length, and **skipped** by
the 2026-08-22 run, which wrote its reasoning to `friction.jsonl` (lines 69 and 70; the Meta one even
records that "the two rules point opposite ways and both are on point"). Nothing in
`candidates.json` or `state_summary.json` carries a trace of either decision. So this morning I
triaged both from scratch, reached **admit** on both, and wrote ids 252 and 253 — reversing a
three-day-old editorial judgement without knowing one existed. I discovered the prior decisions only
afterwards, while reading `friction.jsonl` to draft today's entries: by accident, and after the rows
were live.

I resolved the two differently and I want the asymmetry on the record, because it is the argument for
the fix rather than a tidy ending. Id 253 (DeepSeek) I removed — the 08-22 call was simply right, the
page is a product announcement with its only numbers inside a chart image. Id 252 (Meta) I kept, with
the disagreement flagged in its notes and in the run report: the post carries head-to-head benchmark
tables for a named model that exist nowhere else, and `criteria.yaml` policy is
`when_uncertain: admit_and_flag`. Both calls are defensible. That is the problem — the corpus's line
on "capability showcase carrying real benchmark tables" currently depends on which agent instance
woke up that morning, and a human reviewer has no way to see that a reversal happened.

**Suggested change.** The information already exists; it is just in the wrong format. In rough order
of cost:

- **Record skips where triage happens.** Add a `decisions` map to `candidates.json` (or a sibling
  `logs/decisions.jsonl`) keyed by URL: `{verdict: skip|added|deferred, run_id, rule, one_line}`.
  Phase A carries it forward across runs. The agent is then instructed to read it before triaging a
  link it has seen before, and to state explicitly when it is overturning a prior verdict.
- **Make reversal visible in the write path.** If a proposal's URL has a recorded `skip` verdict,
  have `propose_doc.py` still write it but stamp the changelog detail with
  `reverses: <run_id>`. Cheap, and it turns an invisible flip into a reviewable event.
- **Settle the underlying rule while you are in there.** This specific boundary — a first-party
  announcement post that is majority demo but carries substantive named-model benchmark tables — has
  now been decided three times across three runs (`google-deepmind-sl2t-other` admitted,
  `meta-tribe-v2-other` admitted then removed, this one skipped on 08-22 and admitted on 08-25). It
  wants one sentence in `criteria.yaml`, not a fourth adjudication.

**Evidence:** `friction.jsonl` lines 69–70 (2026-08-22) against changelog `add` rows for ids 252 and
253 in run `2026-08-25T06:17Z-local` and the `status_change` to `removed` on 253 later in the same
run; friction line `prior_adjudication_reversed_because_skip_decisions_are_not_machine_readable`.

## 2026-08-26 — `openness` has no rule for derivative licences, and the corpus has already split the same licence tag eleven ways

**Problem.** `openness` is the one field on a document that makes a legal claim, and it is the only
attested field with no written definition of how to evaluate it. `criteria.yaml` does not mention it
at all; the guidance the agent works from defines the three values and says "omit when you cannot
verify the license" — which is sound as far as it goes, but it gives no answer to the question that
actually arises, which is *whose* licence governs a derivative.

I hit it head-on today on id 258, `nvidia/Ising-Calibration-1.5-31B-BF16`:

- The card's **Governing Terms** name only "the OpenMDW License Agreement, version 1.1", with
  "ADDITIONAL INFORMATION: Apache License, Version 2.0". Gemma is never mentioned in the licence
  section. Read literally, that is `open_weight_permissive`.
- The same card's **Model Architecture** section states the model "was developed based on
  `google/gemma-4-31b`". The Gemma Terms of Use are a use-restricted community licence of exactly
  the kind the `open_weight_restrictive` value exists to capture, and they normally flow through to
  derivatives regardless of what the derivative's own card says.

Both readings are defensible from the document alone, they produce opposite values, and nothing in
the schema records which one was applied. I left the field unset and explained why in `notes` —
correct under the stated rule, but it means the site's openness filter now silently omits a row whose
weights are in fact public, which is its own kind of wrong answer.

**This is not a one-off.** The corpus has already answered the identical question both ways without
recording that it did. Rows whose HF licence metadata is `openmdw-1.1` and nothing else:

| openness recorded | rows |
|---|---|
| `open_weight_permissive` | `NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16`, `Cosmos3-Super`, `Cosmos3-Edge`, `Nemotron-3-Embed-8B-BF16`, `NVIDIA-Nemotron-Labs-3-Puzzle-75B-A9B-BF16`, `Alpamayo2-Super`, `NVIDIA-NemotronLabs-VoiceChat-11B`, `nemotron-3.5-asr-streaming-0.6b`, `NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`, `NVIDIA-Nemotron-Labs-Teacher-General-Reasoning` |
| `open_weight_restrictive` | `Alpamayo-1.5-10B`, `NVIDIA-Nemotron-Parse-2.0`, `Nemotron-3.5-Content-Safety` |

Same licence tag, opposite values, no field saying why. The restrictive three are most likely
base-model flowthrough calls — i.e. some past run applied the rule I could not find written down —
but that is an inference from the outside, which is the whole complaint.

**Suggested change**, cheapest first:

- **Write the flowthrough rule into `criteria.yaml`.** One sentence settles every case above: *the
  most restrictive licence that a user must accept to use the released weights governs, including a
  base model's terms where they flow through; where the card's own terms and an identified base
  model's terms conflict and the flowthrough cannot be confirmed, record the more restrictive value
  and say so in `notes`.* I would rather the corpus be consistently conservative than sporadically
  silent — an unset field is indistinguishable from "nobody looked", and today's row now reads that
  way.
- **Record the basis, not just the verdict.** A companion `openness_basis` (`card_terms` /
  `base_model_flowthrough` / `repo_license_file` / `unverified`) makes the eleven rows above
  auditable and makes disagreement visible instead of invisible. This is the same argument the
  2026-08-25 entry makes for skip decisions, applied to the one field that carries legal weight.
- **Backfill the three restrictive OpenMDW rows** with whatever the rule turns out to be, so the
  next run has a precedent it can actually read rather than a 13-row split it has to guess at.

Worth being explicit that the corpus is not wrong today in any provable way — `openness` gates a
display filter, not a merge — but it is the field most likely to be quoted back at this project by
someone who cares about licence terms, and it is currently the least specified thing in the schema.

**Evidence:** id 258 written this run with `openness` deliberately unset, rationale in its `notes`;
the card's Governing Terms and Model Architecture sections at
`https://huggingface.co/nvidia/Ising-Calibration-1.5-31B-BF16`; the table above from
`select openness, canonical_url from documents where publisher='nvidia'` joined against
`cardData.license` / `license_name` from the HuggingFace API for each repo; `config/criteria.yaml`
(no `openness` key anywhere); friction line
`openness_has_no_rule_for_base_model_license_flowthrough_and_the_corpus_is_already_split`.

## 2026-08-27 — Family rows get a public slug naming the smallest variant, which is usually not the document

The corpus is now good at family rows and bad at naming them. Since the 2026-08-19 ruling that a
multi-size release is **one row listing all `model_names`**, the slug for such a row has been derived
from the first entry of the sorted name list — which, for a size family, is the smallest variant.
The canonical URL points somewhere else.

Written this run:

- `inclusion-ai-ui-venus-1-5-2b-model-card` → `https://huggingface.co/inclusionAI/UI-Venus-1.5-30B-A3B`

The public page for the UI-Venus 1.5 family is therefore `/inclusion-ai-ui-venus-1-5-2b-model-card`,
naming a repo I never fetched and that is not the card's subject. This is not new; it is the third
friction entry on it (`slug_derivation_misnames_family_documents`, 2026-08-19 and 2026-08-20) and the
first with the whole set counted. Every `model_card` row whose slug encodes a sibling other than its
own canonical URL:

| slug | canonical URL | model_names |
|---|---|---|
| `alibaba-qwen-qwen3-asr-0-6b-model-card` | `…/Qwen/Qwen3-ASR-1.7B` | 0.6B, **1.7B**, ForcedAligner-0.6B |
| `inclusion-ai-singguard-0-8b-model-card` | `…/inclusionAI/SingGuard-2b` | 0.8b, **2b**, 4b, 8b |
| `inclusion-ai-singguard-nsfa-0-8b-model-card` | `…/inclusionAI/SingGuard-NSFA-9B` | 0.8B, 2B, 4B, **9B** |
| `inclusion-ai-ui-venus-1-5-2b-model-card` | `…/inclusionAI/UI-Venus-1.5-30B-A3B` | 2B, 8B, **30B-A3B** |
| `tencent-hunyuan-hy-mt2-1-8b-model-card` | `…/tencent/Hy-MT2-30B-A3B` | 1.8B, 7B, **30B-A3B** |
| `tencent-hunyuan-wemm-embedding-2b-model-card` | `…/tencent/WeMM-Embedding-9B` | 2B, 4B, **9B** |
| `nvidia-af-next-captioner-model-card` | `…/nvidia/audio-flamingo-next-hf` | **Captioner**, Instruct, Think |
| `google-deepmind-gemma-4-e2b-model-card` | `ai.google.dev/gemma/docs/core/model_card_4` | 12B, 26B-A4B, 31B, **E2B**, E4B |

Eight of 117 `model_card` rows, and the rate is rising because the family rule is being applied more
consistently, not less. Note the failure is specific to *documents named after their subject model*:
`independent_eval` rows legitimately slug on the subject rather than the URL (`rand-gpt-5-…` at an
`RRA3892-1.html` URL is correct and should stay), so this is not an argument for slugging everything
off the URL.

**Suggested change**, cheapest first:

- **For `model_card` / `system_card` / `addendum`, derive the slug from the model name that best
  matches the canonical URL, falling back to the first name only when none matches.** For all eight
  rows above the URL's last path segment contains the right variant string verbatim; a substring test
  against each `model_names` entry picks it. One function, no schema change, no re-decision.
- **Or: prefer a family stem.** `inclusion-ai-ui-venus-1-5-model-card`, `tencent-hunyuan-wemm-embedding-model-card`
  — strip the size token when a row carries ≥2 names sharing a stem. Arguably the most honest name for
  a document that covers all of them, and it is what a reader searching for the family would type.
- **Either way, backfill the eight and leave redirects.** Slugs are public URLs
  (`cards.douwmarx.com/<slug>`), so silent renames break links; whatever the fix, these eight need it
  applied at once rather than drifting as new family rows land.

I would take the first option. It is the smaller change, it needs no judgment about what a "stem" is,
and it makes the slug agree with the one thing about the row that is not a curation call — the URL
that was actually fetched.

**Evidence:** id 264 written this run (`inclusion-ai-ui-venus-1-5-2b-model-card` at the 30B-A3B URL);
the table above from `state_summary.json`, filtering `doc_type='model_card'` rows with ≥2
`model_names` for a slug encoding a name other than the canonical URL's target; friction lines
`slug_derivation_misnames_family_documents` (2026-08-19, 2026-08-20, 2026-08-27); the family-row
ruling in the 2026-08-19 PROPOSALS entry.
