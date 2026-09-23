---
name: cardtrack-report
description: Regenerate the research report over the cardtrack system-card database (corpus growth, discovery latency, link availability, change classification, tracker reliability). Use when asked to re-run, refresh or extend the "system card database report" after the database has grown. Read-only with respect to the cardtrack repo.
---

# cardtrack research report

The report lives OUTSIDE this repo, in `~/projects/ais/system_card_report/`, and reads a snapshot
of this repo's data. Never edit the cardtrack codebase as part of this task; raise pipeline issues
in the report's future-work section and in the final message instead.

Layout of `~/projects/ais/system_card_report/`:

- `snapshot.sh`            copies `data/docs.sqlite`, `logs/run-*.log`, friction/candidates files and exports
                           host journal events (suspend/resume + service starts) to `data/`
- `build_pairs.py`         writes text diffs for every consecutive version pair (`pairs/diffs/`), the manifest
                           `pairs/version_pairs.json`, and batches of still-unclassified pairs (`pairs/batches/`)
- `CLASSIFY_INSTRUCTIONS.md` taxonomy + output schema for the classification sub-agents
- `classifications/*.json` sub-agent outputs (one object per pair; kept, so only new pairs need classifying);
                           `classifications/overrides.json` holds hand-verified corrections with reasons
- `analyze.py`             all numbers, `out/macros.tex`, `out/tables/*.tex`, `out/figures/*.{pdf,png}`,
                           `out/results.json`, `out/comprehensive_report.md`
- `report/report.tex`      the polished report: a body under 4 pages plus appendices (A: every substantive
                           change with URL and version ids, for verification; B: tracker reliability, kept out
                           of the body because the science is about the documents, not the host);
                           contains NO hard-coded numbers, only `\input`s
- `out/pipeline_proposals.md` evidence-backed fixes for the tracker (full daily coverage with conditional
                           requests, soft-404 detection, footnote-safe extraction, raw-vs-extracted attribution)
- `run.sh`                 `snapshot | pairs | analyze | pdf | all`

## Procedure

1. `cd ~/projects/ais/system_card_report && ./run.sh snapshot && ./run.sh pairs`
   (`uv sync` once on a fresh clone; needs `latexmk`, `pdftoppm`, `pdfinfo`, `journalctl` optional).
2. If `pairs/batches/` is non-empty, fan out one general-purpose sub-agent per batch file, all in one
   message. Prompt: "Read CLASSIFY_INSTRUCTIONS.md and follow it exactly. Input batch: <path>. Output
   path: classifications/batch_<date>_<i>.json." Nine agents handled 176 pairs in about 5 minutes.
   Spot-check 3 furniture and 3 content labels against the diffs before trusting them. For any pair
   summarised as a deletion, check the raw capture in the repo's `data/raw/` (the extractor has dropped
   footnotes before); record verified corrections in `classifications/overrides.json`.
3. `./run.sh analyze && ./run.sh pdf`. Look at every `report/page-*.png` and every figure PNG; fix
   layout in `analyze.py` (figures) or `report.tex` (placement), never by typing numbers.
4. Spawn two fresh review agents (code correctness vs. results.json; prose/figures) and fix what matters.
5. Keep the body under 4 pages and lead with what changed in the documents; host and pipeline failures go
   to Appendix B and `out/pipeline_proposals.md`. Deliberately exclude corpus composition, the curation
   funnel and metadata churn from the body (they stay in `out/comprehensive_report.md`). Appendix A is
   generated (`out/tables/appendix_changes.tex`) and must list every substantive publisher-side pair with
   its canonical URL and version ids so readers can verify claims against the live page and the database.
6. `okular report/report.pdf &` to show the result.

## Analysis conventions worth keeping

- A "monitor outage" run is one where every link check errored; those runs are excluded from all
  availability and change statistics. Match run starts to journal resume events within 120 s.
- Version pairs where the served content type changed, or a `canonical_url` field update falls inside
  the interval, are the tracker's own URL migrations (`tracker_migration`), not publisher edits.
- Substantive = `content_minor` + `content_major` + `replacement`. Furniture and extraction noise are
  non-changes even though a version was stored.
- The fingerprint furniture filter was recomputed on 2026-08-31 (`FILTER_RECOMPUTE` in `analyze.py`);
  pre/post comparisons key off that date.
- Literature baselines and their citations are in `out/literature.md` and `report/refs.bib`.
