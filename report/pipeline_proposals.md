# Pipeline proposals from the report (evidence-backed, not yet implemented)

All numbers below come from the 2026-09-22 snapshot; the experiments were run read-only against
`data/raw/` in the cardtrack repo. Nothing in the repo was changed.

## 1. Why only 15 % of documents are content-checked per run, and why that can go

The rotation is a design choice, not a rate limit: `config/settings.yaml` sets
`cadence.fingerprint_fraction: 0.15  # ~weekly full coverage of silent updates`, and the fetch budget
(`max_total_fetch_bytes_per_run: 500 MB`) and `max_new_versions_per_run: 30` were sized around it.

What full coverage would cost:

| quantity | value |
|---|---|
| bytes to re-fetch every tracked document once | 376 MB (316 MB of it PDF; largest single file 29 MB) |
| current Phase A wall time (15 % rotation, 44 to 137 MB) | 2 to 6 min |
| current fetch budget per run | 500 MB |
| link probe today | already one Range GET per document per run (HTTP 206) |

So a full daily re-fetch fits inside the existing budget and would take roughly 10 to 15 minutes on a
home connection. Request count does not change at all: the link probe already touches every URL daily;
only the bytes do. The only site that rate-blocks is openai.com (12 of 27 documents saw a 403 at least
once, on 8 of 22 healthy runs, in bursts of 3 or 12), and that is per-request, not per-byte.

Better than brute force: conditional requests. The fetcher sends no `If-None-Match` /
`If-Modified-Since` headers today (grep of `cardtrack/*.py` finds none). Sending the stored ETag or
Last-Modified for each document turns an unchanged PDF into a 304 with zero body bytes; a changed
document costs one full fetch, which is exactly what we want. Fallback for servers without validators:
compare `Content-Length` from the probe with the stored size before downloading.

Consequences: edits are dated to the day (today they lag by up to a re-check interval, 7 days median,
17 days at the 90th percentile); the `max_new_versions_per_run` cap should be raised or made per-day
adaptive, since a template change at Hugging Face can legitimately mint dozens of versions in one day.

## 2. Soft 404s: pages that go quiet behind an HTTP 200 (issue 3)

The two Palisade pages now serve this 751-byte body with status 200:

```html
<title>Redirecting&hellip;</title>
<link rel="canonical" href="https://palisaderesearch.org/research/self-replication">
<script>location="https://palisaderesearch.org/research/self-replication"</script>
<meta http-equiv="refresh" content="0; url=https://palisaderesearch.org/research/self-replication">
<meta name="robots" content="noindex">
<h1>Redirecting&hellip;</h1>
```

Three independent signals, any one of which is enough: `meta http-equiv="refresh"` with a URL,
`link rel="canonical"` pointing to a different host path, and a body under 1 KB where the previous
version was tens of KB. Proposed rule in the monitor, applied to every fetched HTML body:

1. If the body carries a `meta refresh` (or a `rel=canonical` that differs from the canonical URL), treat
   it exactly like a 301: follow once, record `redirect_permanent` with the target, and let the existing
   `moved` status logic run (`canonical_url` move requires same content at the new URL, which holds here).
2. If the extracted text collapses to under 10 % of the previous version's length, record a
   `content_collapsed` outcome and raise it in `updated_docs.json` for the agent, instead of minting a
   silent new version.

Both are a few lines in `monitor.py` / `fetch.py`; the second needs a new `link_checks.outcome` value.

## 3. Footnotes dropped by the extractor (issue 4)

Root cause, verified on the three affected pairs (versions 274, 276, 323): between 9 and 17 August
Anthropic changed the wrapper of its footnote block from
`<div class="page-wrapper">` to `<div class="page-wrapper PostDetail-module-scss-module__UQuRMa__postFooter">`.
trafilatura 2.2.0 discards any element whose class contains "footer", so the whole footnote block is
treated as page chrome. The raw HTML of both versions contains identical footnotes; only the extracted
text differs. No trafilatura setting recovers them (`favor_recall`, `include_comments`,
`include_formatting`, `deduplicate=False` all tested).

Fix that works (tested): neutralise the token before extraction. Renaming `__postFooter` to
`__postfoot`, or stripping class tokens matching `/footer/i` from any element that contains a
descendant whose class matches `/footnote/i`, restores every footnote in all three cases
(extracted length 7,638 to 7,861; 20,762 to 21,095; 12,919 to 13,290 characters).

## 4. The more fundamental problem, and the fence around it

The tracker conflates three things: what the server serves (raw bytes), what the extractor keeps
(text), and what the publisher wrote (content). Versions are minted, fingerprinted and diffed on the
extractor's output alone; 61 % of stored versions and every false "deletion" in the report came from the
two layers the publisher does not control.

The obvious fix, fingerprinting on the full visible text of the raw capture, is wrong, and the current
design is right to avoid it. Boilerplate removal is the noise filter: raw pages carry navigation, related
posts, cookie banners, download counters and build hashes that change on every fetch. Even with the
extractor, 85 % of minted versions were furniture before the pattern filter (settings.yaml), and Hugging
Face pages still flag at 37 % per check today. A raw-text fingerprint would churn on every page and the
bullet-anchored furniture patterns, written against trafilatura output, would all need rewriting.

What survives:

- Keep the extractor as the basis for minting versions.
- Use the raw capture as a second opinion, asymmetrically: when the extracted diff contains a deletion,
  check whether the deleted text is still present in the new raw capture. If it is, record the version as
  extractor drift, not a content change. Cheap, needs no new fingerprint, and would have caught all three
  false deletions in the report.
- Protect known content containers (footnotes, tables, change logs) from the boilerplate remover by an
  allow-list or class-token pre-clean (section 3).
- Classify each diff at mint time and store the category and flags on the version row, so "silent score
  change" and "content collapsed" are queryable fields.

Order of work: fingerprint and extractor fixes first, then daily full coverage with conditional requests
(section 1), then raise or rethink `max_new_versions_per_run`. In that order daily coverage dates edits to
the day at the same request count; in the reverse order it mints furniture faster.

## 5. Additions from the 2026-09-29 edition

- **Soft 404s resolved by the publisher, not the tracker (section 2).** The two Palisade stubs kept
  returning HTTP 200 from 2026-09-06 until 2026-09-23, when Palisade replaced them with real 301s and the
  monitor marked them `moved`. The meta-refresh rule in section 2 would have caught them 17 days earlier.
  After the move the monitor stored the redirect target's content (versions 618, 619) as a new version of
  the old row; these read as "replacement" pairs. Consider re-pointing `canonical_url` on a verified move so
  post-move versions are not diffed against the stub.
- **Suspected footnote drop, same position (section 3), unverified.** anthropic-claude-fable-5-other
  v116 to v629 lost the DJI Tello / consent footnote just before the related-content block. `data/raw/` was
  not readable in the unattended sandbox, so this was reclassified conservatively
  (`classifications/overrides.json`, `"verified": false`); please count footnote markers in the raw
  HTML of 116/629/689. The section 3 pre-clean would settle it at the source.
- **Anthropic date lines and related-posts footers.** 21 of this week's Anthropic version pairs were
  furniture or metadata_minor, mostly a removed publication-date line (apparently a site template change)
  plus the rotating "related content" footer; none substantive. A furniture pattern
  for the related-posts block (or excluding it by container, as for footnotes) would stop these.
- **Run logs are no longer reaching the snapshot.** `logs/` holds no `run-*.log` after 2026-09-22 while the
  database records 9 further runs (three on 2026-09-29). The agent phase of those runs is therefore unknown
  in the report. Either the runner stopped writing the per-run log, or logs moved; `snapshot.sh` copies
  `logs/run-*.log` only.
- **`data/raw/` is not visible to the report runner.** The skill requires checking raw captures for any
  deletion; the unattended sandbox cannot. Either snapshot the raw files needed for new pairs (the
  `raw_path` of both versions of every pair in `pairs/batches/`) into `report/data/raw/`, or mount
  `data/raw` read-only in the sandbox.
- **Access table dropped from OpenAI GPT-5.5 access policy (v647)** at the same time as "(opens in a new
  window)" link-text markers appeared: probably an extractor/markup change (classified extraction_noise,
  low confidence); the raw check above would confirm.
- **107 written versions are missing from `document_versions` (found in the second 2026-09-29 run).**
  The changelog has 346 `new_version` events. Of these, 107 have no row with the same document and content hash,
  and 106 of them predate the 2026-08-31 fingerprint recompute. Only 12 are accounted for by the
  documented Anthropic footnote purge. Unless the deletions are recorded, the pre/post filter comparison
  undercounts the "before" side, and a reader cannot reproduce those diffs from the database. Please record
  purges or dedups in the changelog (for example `action = "purge_version"` with the version id and a reason).
  Alternatively, keep deleted rows with a `purged_at` column. Then `analyze.py` can say what was removed and why.

## 6. Additions from the 2026-10-04 edition

- **Footnote artefacts survive the pre-clean (section 3).** Two stored Anthropic versions still lack
  footnotes that their own raw captures contain: anthropic-claude-fable-5-other v629/v689 (DJI Tello /
  consent footnote, present twice in each raw file, absent from the text) and
  anthropic-claude-opus-4-6-other-2 v630 (two footnotes, present in raw as `<li id="footnote-N">`). Either
  these texts were extracted before the fix and never re-extracted, or the new `footnote-N` list markup
  escapes the pre-clean. Proposal: re-extract both from `data/raw/`, and add these two raw files as
  extractor regression fixtures. Both are recorded as verified overrides.
- **The suspected fable-5-other deletion from the last edition is settled:** extractor artefact, not a
  publisher deletion (raw of v116, v629 and v689 all hold the footnote). `data/raw/` was readable this run
  at the repo path, so the previous "raw not visible" item is resolved for now; `snapshot.sh` still does
  not copy raw files.
- **Palisade extractor drift.** palisade-research-gpt-5-4 v718 and grok-4-0709 v719 dropped the page
  title, "Additional ways to view" and the related-posts list from the extracted text while raw HTML of both
  versions still holds them. The 2026-10-03 run log reports `"extractor_drift": 2`, so the drift detector
  caught both, yet both were still stored as new versions. Consider not minting a version (or tagging it)
  when drift is detected and the raw capture still contains the dropped lines.
- **Host migration lost the outage evidence.** The tracker now runs on a different host (git history around
  2026-10-01). The snapshot has run logs only from 2026-10-02 and a journal with service starts but no
  suspend/resume events, so the report can no longer re-derive why 22 runs were outages; Appendix B now says
  so and cites the previous edition. Proposal: keep `logs/run-*.log` in a persistent location that survives
  host moves (or commit a per-run JSON summary), and export the old host's suspend/resume events once into
  a committed file if the attribution should stay reproducible.
- **Backdated section label (METR, v73 to v725).** METR's red-teaming page gained a section headed
  "Results from the Exercise (added May 2026)"; the page was fingerprinted unchanged at every successful
  content check from 2026-08-09 to 2026-09-29 and changed by 2026-10-03. Not a pipeline issue, but an
  example of why detection dates from a daily full-coverage fetch (section 1) matter for dating edits.
- **Tab panels are skipped by the extractor (new, verified).** Two pairs that earlier editions reported as
  undisclosed publisher deletions are extractor artefacts: openai-gpt-5-6-cyber-other v250 to v482 (the
  Keychain/Chrome-cookie prompt-response table and a customer quote) and openai-gpt-rosalind-access-policy
  v462 to v561 (the "Fourth Eon" launch partner). In both, the newer raw HTML still holds the content
  inside a `role="tabpanel"` element (the panel's class changed between captures, for example from a
  `transition-opacity` class to `class=""`). The extractor should keep every tab panel's text. Both pairs
  are now overrides (`extraction_noise`). Other substantive deletions cited in the report body were
  checked against raw and hold (NVIDIA VoiceChat v317, Gemini Omni v432, Cosmos3 v613/v614, UI-Mate v376,
  Mistral Small 4 v461).
