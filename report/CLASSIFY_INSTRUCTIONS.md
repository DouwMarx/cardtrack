# Version-change classification task

You are classifying what changed between two stored versions of a tracked AI-model document
(system cards, model cards, independent evaluations) in the cardtrack database.

Input: a batch JSON file (list of records). Each record has: slug, publisher, doc_type, title,
url, content_type, prev_version, version, prev_fetched, fetched, prev_lines, lines, added, removed,
diff_lines, diff_path (a unified diff of the extracted TEXT of the two versions, context=2),
change_summary (an earlier agent's note; may be null or wrong; verify against the diff yourself).

For EVERY record, read the diff file at diff_path (use Read; for diffs over ~1500 lines, read the
first 400 and last 200 lines and sample the middle; you may also grep the diff for numbers, "%",
"License", "Update", "Correction", "errata", section headings). Then output one JSON object.

## Taxonomy (choose exactly one `category`)

- `furniture`: ONLY dynamic page chrome changed: Hugging Face download counters, "Spaces using",
  eval-widget leaderboard rows, sidebars, related-article footers, cookie banners, share buttons,
  "last fetched"/access-date stamps, navigation menus, ads, comment counts. The document body is unchanged.
- `extraction_noise`: the underlying document is the same but text extraction differs (PDF
  re-extraction with different line breaks/ligatures/ordering, encoding artifacts, whitespace-only,
  hyphenation). No semantic content change.
- `metadata_minor`: small non-substantive edits to the document itself: typo fixes, formatting,
  link targets, author list/affiliation tweaks, citation formatting, date labels, table of contents,
  added "updated on" notes without content change.
- `content_minor`: small substantive edits: a clarification sentence, a corrected number or
  footnote, a caveat added, a paragraph reworded with changed meaning, a small added/removed row.
- `content_major`: large substantive changes: new sections, new evaluation results or benchmark
  scores, new model versions/sizes added to a card, license or usage-policy change, retraction or
  correction notice, restructuring of the document, a new document revision (e.g., v1 -> v2).
- `replacement`: the URL now serves a different document or a non-document (login wall, 404 text,
  redirect landing page, placeholder, index page), or the whole document was replaced by another.

## Additional flags (booleans)

- `score_change`: at least one benchmark/evaluation number in the DOCUMENT BODY changed or was added
  (NOT the HF eval-widget sidebar).
- `license_change`: license or terms-of-use text changed.
- `safety_related`: the change touches safety evaluation, risk, red-teaming, mitigation, or policy
  sections (not just a mention).
- `model_scope_change`: the set of models/variants/sizes documented changed.
- `correction`: the change reads as an erratum / correction / retraction of an earlier claim.
- `growth_direction`: one of `grew`, `shrank`, `same` (net document body length, ignoring furniture).

## Output

Write a JSON list to the output path given in your prompt, one object per input record:
{"slug": ..., "version": <int>, "category": ..., "score_change": bool, "license_change": bool,
 "safety_related": bool, "model_scope_change": bool, "correction": bool, "growth_direction": ...,
 "summary": "<= 25 words, concrete, what actually changed>",
 "notable": "<one sentence if this change is interesting to a reader tracking AI documentation transparency, else empty string>",
 "confidence": "high|medium|low"}

Rules: be skeptical of the provided change_summary. If the diff shows only HF widget lines, it is
`furniture` even if the summary claims more. Numbers in `- llamaindex/... leaderboard 73.4` style
lines are widget furniture, not document scores. Return the full JSON list. Do not skip records.
