# cardtrack run report — 2026-08-18T07:25Z-local

**Corpus at start:** 228 documents (224 active, 3 removed, 1 moved). **Written this run:** 2 adds
(ids 229, 230). **Proposals rejected or filed as issues:** none. **Open issues:** none.
**Blocked-URL escalations:** none.

## Phase A failed completely again — everything below came from a hand sweep

Phase A recorded `checked: 225, ok: 0, not_found: 0, blocked: 0, errors: 225, candidates_new: 0`
at 07:25:12Z. I re-fetched all 43 configured `index_urls` from the same venv at 07:35Z and got
**43/43 HTTP 200**, so this was another total transient outage, not a publisher problem — the
fourth since 2026-08-14. Consequences: no link-check, no dead-URL detection and no fingerprinting
ran for any of the 225 active documents, and `candidates.json` is byte-identical to yesterday's
(newest `first_seen` 2026-08-17). Curiously the same line reports `fingerprint_checked: 34` with
`ok: 0`, i.e. it counts work it cannot have done. Logged as friction.

To cover the gap I re-swept the 43 index pages by hand, extracted every outbound link, and diffed
against the union of `candidates.json` (2,613 links) and the 228 corpus URLs: 396 links unseen,
151 after dropping static assets, of which everything actionable is below.

## Added (2)

Both from the hand sweep of `huggingface.co/tencent`, cross-checked against the HF API for
creation dates. Tencent had read 34 days silent before this run.

| id | document | date | verdict |
|---|---|---|---|
| 229 | [UI-Mate-27B model card](https://huggingface.co/tencent/UI-Mate-27B) — GUI/desktop-automation agent, covers UI-Mate-27B and UI-Mate-9B | 2026-08-14 | `{"status": "written", "slug": "tencent-hunyuan-ui-mate-27b-model-card", "document_id": 229, "version_id": 280}` |
| 230 | [EVIE-Preview-4.5B model card](https://huggingface.co/tencent/EVIE-Preview-4.5B) — multilingual visual document retrieval | 2026-08-17 | `{"status": "written", "slug": "tencent-hunyuan-evie-preview-4-5b-model-card", "document_id": 230, "version_id": 281}` |

Both Apache-2.0 (`open_weight_permissive`), both `has_safety_evals: false` — UI-Mate carries only
operational deployment guidance (isolated environments, human confirmation for sensitive
operations), EVIE has no safety section at all. UI-Mate-9B is filed as a size variant on the 27B
entry per the family rule, with its URL in `notes` and evidence.

## Checked and deliberately not proposed

- **NVIDIA Nemotron-Labs-Teacher ×5** (2026-08-14) and **inclusionAI Ling-3.0-tiny** (2026-08-10) —
  both already catalogued; the teacher family is one row covering all five names.
- **Anthropic, "How Claude's text watermark works"** (2026-08-14, in yesterday's candidates) —
  fetched and read. A feature explainer with no named-model assessment and no quantitative results
  (the only numbers quoted are Google DeepMind's, about Gemini). Out of scope by the `other`
  scope-discipline rule.
- **Anthropic, "When AI builds itself"** (`/institute/recursive-self-improvement`) — genuinely
  borderline and worth recording: it does report quantitative measurements of named models (Opus 3
  ~4-minute tasks → Opus 4.6 ~12-hour tasks; Opus 4.5 51% vs Mythos Preview 64% at selecting
  research steps; ~3× vs ~52× code-optimisation speedups). But it is framed as a progress essay
  about recursive self-improvement rather than an assessment of any one model, its measurements are
  drawn from documents the corpus already holds, and its own date resolves only to "May 2026"
  in-text. Skipped as a research essay; flagging it here because a slightly different reading would
  admit it.
- **Z.ai GLM-5.3** (2026-08-14, from web search) — a real frontier-adjacent release, but Z.ai is not
  an allowlisted publisher. Catalogued only indirectly, via the UK AISI and SaferAI evaluations of
  GLM-5.2 already held.
- **Qwen3.8-27B-FP8**, `nvidia/Kimi-K3-NVFP4`, `Hy-MT2-30B-A3B-GGUF`, HF `/discussions/` threads,
  `/papers/` links, org-member profile pages — quantizations, re-uploads and page furniture.
- **Backlog re-scan**: 109 of the 2,613 stale candidates match model-card / system-card / report URL
  patterns and are not in the corpus. Every one is either pre-2026 (OpenAI's GPT-5.x line, METR's
  2024–25 evaluations, xAI's 2025 cards, the Gemma/Gemini 2.x cards), an alternate surface of a
  document already held (METR's Frontier Risk Report HTML twin of `metr.org/risk-report-feb-mar-2026.pdf`;
  Cursor's Grok 4.5 blog page vs its own PDF; the four SecureBio `securebio.org/blog/` mirrors), or
  methodology writing with no named model (UK AISI's Inspect series, CAISI's transcript-analysis
  posts). Unlike yesterday, no genuine in-scope document was sitting unproposed in the backlog.

## Targeted search and silent-org audit

Searches for documentation published in the last ~72 hours returned nothing from any allowlisted
publisher. `deploymentsafety.openai.com` still lists nothing newer than the 2026-08-06 GPT-5.6
August update, so GPT-5.6-Cyber's promised full system card has still not appeared (fourth run
noting this). `anthropic.com/system-cards` and `/transparency/model-report` list no card the corpus
lacks. `deepmind.google/models/model-cards/` produced no new card links — the only unseen DeepMind
URLs were utm-tagged duplicates of blog posts already held. A HuggingFace-API sweep by creation date
across nine orgs found real activity only at Tencent (the two adds above); everything newer at
NVIDIA, Qwen, DeepSeek, Moonshot, StepFun, InclusionAI, Xiaomi and Mistral is a quantization,
GGUF/NVFP4 re-upload or speculative-decoding drafter. Xiaomi (113 d), Palisade (103 d) and StepFun
(87 d) remain the longest-silent and remain genuinely quiet.

## Citation mining

I mined the outbound links of the Claude Opus 5 system card, the Gemini 3.7 Flash card, Meta's
Muse Spark 1.1 misconfiguration report, the DeepSeek-V4-Pro-0813 card and Anthropic's multiagent
report — including PDF link annotations, not just visible text. Yield: no uncatalogued third-party
evaluation, but the Opus 5 card's references exposed the edition problem below.

## The finding that matters: the corpus is holding superseded editions

Chasing four Anthropic URLs cited by the Opus 5 card, I found that in three cases the corpus
canonical URL serves an **older edition** of the document while the publisher's current link points
somewhere else. Both URLs return 200, so link-checking sees nothing, and fingerprinting keeps
comparing the stale file to itself.

- **System Card: Claude Mythos Preview** — corpus `…/8b838020…pdf` (244 pp, no changelog) vs live
  `…/08ab9158…pdf` (245 pp), whose Apr 8 changelog records a §7.9 quote removed because it was
  misattributed to Mythos Preview but actually came from Opus 4.6, plus corrected Eleos AI Research
  findings.
- **Alignment Risk Update: Claude Mythos Preview** — corpus `…/79c2d46d…pdf` (59 pp) vs
  `anthropic.com/claude-mythos-preview-risk-report` (61 pp, Apr 10 changelog revising §§1, 5.3.2, 10.2).
- **Risk Report: February 2026** — corpus `…/08eca275…pdf` (104 pp) vs `anthropic.com/feb-2026-risk-report`
  (106 pp, May 26 changelog revising language METR's pilot external review had flagged in §3.4).
  This fetch also identified that row, which the corpus holds with a null publication date and no title clue.
- **Claude Opus 5 System Card** — corpus `…/c5fbac3f…pdf` (193 pp) vs the currently linked
  `…/b514064a…pdf` (194 pp). Here I diffed the full extracted text word by word: repagination only,
  no content change. Worth stating because it is the control case — the difference between a
  corrected misattribution and a moved page number is exactly what a byte comparison cannot make.

I proposed no database change for these. `new_version` rejects any URL not already on a document,
and a `canonical_url` field update requires the new URL's content to fingerprint-match a stored
version, which by construction fails whenever the content was actually revised. Written up in
`logs/PROPOSALS.md` (2026-08-18) with a three-option fix, and in `logs/friction.jsonl`.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty — nothing to investigate, no
comments posted. Phase B could reach GitHub this run, so unlike 2026-08-14 and 2026-08-16 the empty
list is trustworthy.
