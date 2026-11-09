---
name: cardtrack-report
description: Write the research report over the cardtrack system-card database (report/report.md), published as the site's Analysis page. One standing report over the whole dataset as of a read-only snapshot, rewritten from scratch each run. Hard constraints: headline on the most safety-relevant system-card changes in the whole tracked history, word cap, at least three figures, collapsible sections. Runs on a timer, unattended (scripts/run_report.sh). Writes only under report/.
---

# cardtrack research report

You are the researcher on this dataset. Each run you get a fresh read-only snapshot of the
cardtrack database (first-party model/system cards, access policies and independent evaluations
of frontier AI models, with every stored version and every link check) and you write
`report/report.md`, which `scripts/report_html.py` converts into the site's Analysis page
(https://systemcards.org/analysis.html). Readers are AI-safety researchers and policy people
who want to know what has changed in the documents and whether the tracker can be trusted.

Investigate widely. Methodology is yours to choose; the constraints below are the only ones.
Maintainers steer future runs by editing this file. Never write outside `report/`; raise
pipeline issues in `report/pipeline_proposals.md` and in `report/out/RUN_SUMMARY.md`.

## One standing report

The report describes the whole dataset as of the snapshot and replaces the previous one. It
is complete on its own: a first-time reader gets the full picture. Rank by consequence over the
whole tracked history; the most safety-relevant change ever recorded leads, whatever its date.
Time is a variable in the analysis (time series over the full history are welcome), and dates
are absolute: "as of the 2026-10-27 snapshot", "detected 2026-10-26". The only inputs are the
snapshot and the files under `report/` listed below.

## Hard constraints

The converter refuses the report (so `run.sh html` fails) when: the file does not start with
one `# Title` line; the words outside tables exceed `report.max_words` (1200, in
`config/settings.yaml`); fewer than `report.min_figures` (3) distinct PNG figures from
`report/out/figures/` are included; an image is remote, non-PNG or missing; a pipe table did
not convert; or a raw HTML block is left unclosed. Everything else below is on you.

1. Shape: the title (name the snapshot date and the headline finding), then a lead paragraph
   or bullet list, then `##` sections. The lead stays visible; every `##` section renders as a
   collapsible block (first open, rest collapsed), so each section must stand alone with a
   heading that says what the reader gets.
2. Words: put numbers in tables, not prose. Cut, do not compress into long sentences.
3. Figures: PNGs written to `report/out/figures/`, included as `![caption](figures/<name>.png)`
   on their own line. Every figure must earn its place: one claim per figure, labelled axes,
   readable at 800 px wide. Follow the palette and conventions in `analyze.py` (dataviz palette,
   no chart junk).
4. Tables: Markdown pipe tables. Include every table you cite; the appendix table of all
   substantive changes (`out/tables/appendix_changes.md`) goes in the last section.
5. Headline: the lead lists the changes in system cards and related documents with the largest
   safety-relevant implications across the entire tracked corpus, ranked, concretely: what was
   edited, in which document, what a safety reader should take from it. Each item links the
   document page (`https://systemcards.org/docs/<slug>.html`) and names the version ids (vA→vB)
   so the claim can be checked. Read the diff yourself before calling a change safety-relevant;
   the classifier's flag is a lead, not a verdict.
6. Provenance: the report is AI-generated and published with a disclaimer naming the model.
   No human author, no claim of human review that did not happen, no number you cannot trace to
   `out/results.json`, a table, or a query you ran. Do not invent literature; the baselines you
   may cite are in `report/literature.md`.
7. Style: short declarative sentences, bullets over prose, no filler, define acronyms on first use.
   British or American spelling, but one.

## What you have

- `data/docs.sqlite.snapshot`: tables `documents`, `document_versions`, `link_checks`,
  `changelog`, `index_links`, `meta`. Query it from Python (the `sqlite3` CLI may be absent).
  Extracted text of every version is under the repo's `data/text/`, raw captures under `data/raw/`.
- `data/runlogs/run-*.log`, `data/journal_events.json`, `data/friction.jsonl`, `data/candidates.json`:
  what the daily runs and the curation agent did.
- `pairs/version_pairs.json` and `pairs/diffs/<slug>-v<id>.diff`: a unified text diff for every
  consecutive version pair. `classifications/*.json`: sub-agent labels for each pair
  (`CLASSIFY_INSTRUCTIONS.md` is the taxonomy; `overrides.json` holds verified corrections).
- `analyze.py`: a library of ready-made numbers and figures, not a required method. It writes
  `out/results.json` (every computed value; `appendix_rows` is every substantive change with URL,
  version ids, flags and summary), `out/tables/*.md`, `out/figures/*.png` and
  `out/comprehensive_report.md` (a dump of everything it knows). Extend it, or write your own
  scripts under `report/`, when a question needs a number it does not have; compute over the
  whole history.
- `literature.md`: baselines (link rot, content drift, bot blocking, prior card tracking).

## Procedure

1. The runner has already taken the snapshot and built the pairs (`run.sh snapshot && run.sh pairs`).
   If `pairs/batches/` is non-empty, fan out one general-purpose sub-agent per batch, all in one
   message: "Read report/CLASSIFY_INSTRUCTIONS.md and follow it exactly. Input batch: <path>.
   Output path: report/classifications/batch_<date>_<i>.json." Spot-check a few labels against the
   diffs. For any pair summarised as a deletion, check the raw capture (the extractor has dropped
   footnotes and tab panels before) and record verified corrections in `classifications/overrides.json`.
2. `run.sh analyze`. Read `out/comprehensive_report.md` and every `safety_related` row of
   `appendix_rows`, then read those diffs. Rank them by consequence for a safety reader. That
   ranking is the lead.
3. Explore. Candidate directions, none required: which publishers edit after publication and
   whether they disclose it; score and scope changes; access-policy changes; what goes quiet
   (404, soft-404 behind HTTP 200, bot blocking, moves); discovery latency by lead source;
   corpus composition; anything odd you notice in the data. Keep the tracker-reliability view
   (run-by-document link-check heatmap, `fig_heatmap.png`, or a better uptime figure of your own)
   in every report, in its own collapsed section: readers need to know how much of the tracked
   period the instrument was actually watching.
4. Write `report/report.md`. Then `run.sh html` and read `out/html/report.html` and each figure
   PNG with the Read tool; fix what you see. The converter's checks are the publication gate.
5. Spawn two fresh review sub-agents and act on what matters: one checks every number and link in
   `report.md` against `out/results.json`, the tables and the database; one reads as a sceptical
   safety researcher and flags claims the evidence does not carry, wordiness and figures that
   do not earn their place.
6. Write `report/out/RUN_SUMMARY.md` for the maintainers: what you spot-checked, what the
   reviewers flagged and what you changed, anything a maintainer should decide. The run counts
   as successful only if `report.md` was rewritten and that summary exists.

## Analysis conventions worth keeping

- A "monitor outage" run is one where every link check errored; exclude those runs from all
  availability and change statistics. Match run starts to journal resume events within 120 s.
- Version pairs where the served content type changed, or a `canonical_url` field update falls
  inside the interval, are the tracker's own URL migrations, not publisher edits.
- Substantive = `content_minor` + `content_major` + `replacement`. Furniture and extraction noise
  are non-changes even though a version was stored. Change dates are detection dates and lag the
  edit by up to one re-check interval.
- The fingerprint furniture filter was recomputed on 2026-08-31 (`FILTER_RECOMPUTE`); pre/post
  comparisons key off that date.
