# cardtrack agent run — 2026-10-06 (run id 2026-10-06T06:20Z-local)

The last agent success was 2026-10-05T06:25:33Z, so the search used the 72 h minimum lookback (from 2026-10-03).
- Today is Tuesday, so the weekly retrospective sweep did not run.
- `open_issues.json` returned `fetch_ok: true` with no open issues, so there was nothing to investigate.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add `access_policy` | OpenAI "Accelerating the cyber defense ecosystem that protects us all" (GPT-5.4-Cyber, 2026-04-16) | **written**: `openai-gpt-5-4-cyber-access-policy` (doc 364, v749) |
| 2 | add `independent_eval` | Redwood "Frontier models state different decision theory preferences depending on who's asking" (2026-09-30) | **written**: `redwood-research-claude-fable-5-1-independent-eval` (doc 365, v750) |
| 3 | add `access_policy` | Anthropic "Developing Enterprise Frontier Safeguards with our customers" (Fable 5 / 5.1, 2026-09-01) | **written**: `anthropic-claude-fable-5-access-policy` (doc 366, v751) |

Notes:

- **#1** was flagged as unreadable in the 10-05 run.
  - I read it with `read_doc.py`; browser impersonation returned HTTP 200.
  - It is the follow-up to the 04-14 GPT-5.4-Cyber launch row: participant list, $10M grant credits, and GPT-5.4-Cyber access for CAISI and UK AISI.
  - `restricted`, no evals, no risk tags.
  - The page text has no date. 2026-04-16 comes from same-day BankInfoSecurity coverage.
- **#2** is a Phase A candidate, first seen today.
  - It reports measured sycophancy / "audience awareness" results for Claude Fable 5.1, Fable 5, Opus 5, Opus 5.5, Sonnet 5 and GPT-6 Astra (100 samples per condition).
  - Tagged `harmful_manipulation`, `closed`.
  - It is a cross-post of a LessWrong post dated 2026-09-30.
- **#3** I found through the related-content block of a monitored Anthropic page.
  - It sets enterprise access conditions for the named Mythos-class models: 30-day retention from Fable 5 onward, the EFS customer-held monitoring path, and an interim ZDR grant for Fable 5 and 5.1. There is a request-access form.
  - This is a **borderline** `access_policy`, admitted under admit-and-flag (stated in `notes`). The gate is safeguard and data terms rather than a vetting program. If the operator disagrees, it is a single revert.
  - Date 2026-09-01 is from coverage.

## Phase A candidates (58)

- **Already triaged on 10-04** (first seen 10-02/10-03): corporate news, HF papers/user pages, Epoch/RAND non-model items, NVIDIA PixelUMM/PixelDiT2, Meta posts, the xAI changelog, and the Sonnet 5.5 PDF (already a related_url of `anthropic-claude-sonnet-5-5-system-card`). Not re-litigated.
- **Palisade (14 links from the now-working /research index):** only the self-replication (2026-05-07) and robot shutdown-resistance (2026-02-12) reports are on or after the scope floor. Both are already catalogued; those rows' related_urls already hold the /research URLs. All others are 2025 or earlier, which I verified from the dated index listing, or are /blog. Skipped as below the floor.
- **Redwood decision-theory post:** proposed (#2). The two Substack author profiles are skipped.
- **inclusionAI/AI-Transparency (created 2026-09-24):**
  - The first fetch returned 429; the retry returned 200.
  - It holds EU AI Act Art. 53(1)(d) training-content summaries for 11 Ling/Ring/Ming lines. These are neither cards nor evals.
  - Skipped, with a `schema_gap` friction line.
- **Skipped as not documentation:**
  - Anthropic Campus and Frontier Academy program pages: training programs, no model gate.
  - Ten Mistral site navigation links.
  - Apollo's Senate testimony post.
  - Epoch "openai-coding-agent-spending".

## Targeted search (2026-10-03 → 2026-10-06)

**Coverage:**
- About 16 searches across labs (Anthropic, OpenAI, Google DeepMind, Meta, xAI, Mistral, Chinese open-weight labs) and evaluators (UK AISI, METR, CAISI, Apollo, Transluce, SecureBio, FAR.AI, Epoch).
- Polls of the access programs: LSVP, Cyber Verification Program, Glasswing, Daybreak, GPT-Rosalind, Gemini for Science / Co-Scientist, CodeMender, Fairwind, Isomorphic bioresilience.
- I read the **OpenAI news RSS feed** (`openai.com/news/rss.xml`) directly; it returned 200 with pubDates.

**Results:**
- No new card, addendum or eval was published in the window. Every hit was already catalogued: GPT-6.1 Sol addendum, Opus 5.5 / Sonnet 5.5, METR Opus 5.5, Gemini 3.8 Flash / Live / Flash Cyber (Fairwind), Muse Spark 1.1, Grok 4.6 / 4.7, LSVP, GPT-5.4 TAC.
- LSVP: no new program page or non-US expansion found beyond the Sep 2026 launch coverage.
- Cyber Verification Program: still "Mythos access in the near future".
- GPT-Rosalind pricing took effect on 10-05 (press only).

**OpenAI posts read via `read_doc.py` and skipped:**
- "Our approach to EU text provenance rules" (10-05): provenance policy; the detector-access gating is for a watermark detector, not a model.
- "Disrupting a coordinated model-distillation campaign" (09-30): a security incident with no named OpenAI model evaluated.
- "OpenAI extends cyber access to Ukraine" (09-23): a Daybreak access extension that names no model. Same named-model gate as the 10-03 "Daybreak for Frontline Defenders" skip.
- Help article 20001326 ("Additional safety checks…", flagged on 10-05): generic safeguard FAQ, no named model.

## Citation mining

- The related-content block on the Anthropic incidents post (v565) led to **#3**.
- "Previewing the Model Hardware Standard" (an agent–device spec research preview) and "Claude discovers a novel enzyme system" (a showcase) were skipped as not model documentation.
- Last run already mined the recent rows (Sonnet 5.5, GPT-6.1 Sol addendum, Argon, AISI Astra); I did not repeat that.

## Blocked-URL escalations (13 openai.com / help.openai.com, streak 5)

- **All alive.** `read_doc.py` fetched `trusted-access-for-cyber`, `path-to-astra` and the Daybreak help article, each HTTP 200 via browser_impersonation with full current text.
- No `status_change` proposed.
- The monitor's 403 streak is a false alarm (friction line).
- **Recipe for future runs:** use `read_doc.py`, not WebFetch, for openai.com. The 10-03 to 10-05 runs logged this wall as `agent_fetch_blocked` even though the RESOLVED fix (c0680ef1) already covered it.

## Document updates

I took the top 5 in queue order, plus 2 more to check the pattern. **All were noise; none annotated.**

- **v573** DeepSeek-V4-Pro and **v578** V4-Flash-0731: HF usage-snippet swap (chat/completions → completions), download/Spaces counters, reordered eval widget.
- **v618 / v619** Palisade self-replication / robot shutdown: a stored "Redirecting…" stub replaced by the moved page's text. This is a URL-move artifact, not a revision.
- **v565** `anthropic-claude-mythos-5-other-3`: hyphenation copyedits ("real time" → "real-time", etc.) and rotated related-content teasers.
- **v678** Mythos 5.1 access page: dates dropped from the announcement list.
- **v609** Hy3: download counters and eval-widget reorder.
- **Not opened:** the remaining 13 entries (all ≤ 9 substantive lines, mostly HF cards of the same pattern).

This contradicts the RESOLVED furniture fix, so I logged it as a regression.

## Friction / proposals

I added 4 friction lines:
- `regression`: the furniture classifier lets HF snippet/widget churn, stub replacement and copyedits into the queue (RESOLVED row a4706386).
- `other`: Phase A's 403 streak on 13 OpenAI URLs that the pipeline's own fetcher reads fine.
- `index_gap`: the two access-policy posts added today never surfaced in candidates. It suggests `openai.com/news/rss.xml` as a cheap, dated OpenAI index URL.
- `schema_gap`: EU AI Act training-content summaries.

No PROPOSALS.md entry: none of these needs more than a friction line yet.
