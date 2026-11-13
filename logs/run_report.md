# cardtrack agent run — 2026-11-13 (run id 2026-11-13T06:17Z-local)

- **Lookback:** the last agent success was 2026-11-12T06:28:13Z, so the 72 h minimum applied (2026-11-10 to 11-13).
- **Weekly retrospective sweep:** not run. It is a Friday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | Gemini 4 Hydrogen Model Card (PDF, `model_card`, 11-12). It reports automated safety-eval deltas vs Gemini 3.8 Flash and an FSF assessment: an MCC check vs Argon plus targeted CBRN-bio and cyber CCL testing (CCLs not reached, alert thresholds reached in both). Tagged cbrn, cyber; `closed`. The HTML card is recorded as `web_version` and the launch post as `announcement`. | **written**: `google-deepmind-gemini-4-hydrogen-model-card` (doc 465) |
| 2 | Gemini 4 Hydrogen Model evaluation PDF (`other`, 11-12): harnesses and settings for capability benchmarks. `has_safety_evals: false`, no tags. | **written**: `google-deepmind-gemini-4-hydrogen-other` (doc 466) |
| 3 | SecureBio "Longitudinal Tracking of BioTIER Performance" (`independent_eval`, 11-12): measured post-release biosecurity-safeguard shifts. Opus 5.5 BioTIER-permit went from 37.3% to 56.7%; Grok 4.7 refuse went from 88.5% to about 80%; Gemini 3.1 Pro refuse went from 46% to 74%. Tagged cbrn; `closed`. The Substack post is canonical and the securebio.org copy is `web_version`, following the SecureBio convention. | **written**: `securebio-claude-opus-5-5-independent-eval` (doc 467) |
| 4 | annotate_version v1165, METR's Anthropic AI R&D assessment: a new Nov 6 Update log; AEF-1 item 1.1 corrected from Yes to No; template notes removed. | **written** |

Every proposed document was fetched and read with read_doc before proposing.

**Calls worth checking:**
- **#1, `publication_date`:** the card itself says only "Published: November 2026". The date comes from the launch post byline (Nov 12, 2026).
- **#1, risk tags:** the card summarizes the targeted CBRN and cyber assessments in a results table, and defers full results to a Safety & Security Report "coming soon". I tagged only cbrn and cyber. Manipulation and loss-of-control are only "carried forward from Argon", so I did not tag them.
- **#2, scope:** admitted under the precedent of `google-deepmind-gemini-4-carbon-other` (the Carbon evaluation PDF). If the operator would rather fold these into the card row, both should change together.
- **#3, slug and models:** the auto-slug reads as an Opus 5.5 eval, but the post covers three models. I listed them all in `model_names`.

**Watch:** the Gemini 4 Hydrogen Safety & Security Report is due "in the coming days". Propose it as its own `system_card` when it appears; the Carbon precedent is `gemini_4_carbon_safety_report.pdf` on storage.googleapis.com.

## Phase A candidates

Candidates first seen before 11-13 were triaged in earlier runs. New today:
- **Proposed:** Gemini 4 Hydrogen model card and blog (#1, with the blog as the announcement); SecureBio longitudinal BioTIER, both the org blog and Substack copies (#3).
- **Skipped:**
  - **NVIDIA:** GR00T E2E reference-workflow models and datasets, agile_wbc_unitree_h2, the Cosmos3-Edge-FP8 discussion, and the BirdDreams paper. These are robotics task checkpoints, datasets, a quant discussion and a research paper, with no model documentation.
  - **zai-org GLM-5.3-Flash discussion #72:** a repo housekeeping PR.
  - **inclusionAI:** the SingVL_S1 collection and GGUF (research VLM checkpoints outside the Ling/LLaDA scope) and the Duo paper.
  - **Profile pages:** jyseo, pd4mes, jaychempan.

## Targeted search (11-10 to 11-13)

**Searched for:**
- generic system-card / model-card releases;
- METR / UK AISI / CAISI / Apollo / Epoch / FAR / Palisade reports;
- trusted-access programs: LSVP, CVP, Glasswing, Claude Science, Gemini for Science, Rosalind, Daybreak;
- Qwen4-Max-Preview;
- the OpenAI news RSS feed from 11-10 to 11-13;
- the Anthropic news index.

**Already in the DB:**
- Fable/Mythos 5.2, Opus 5.5, Haiku 5.5;
- the CVP expansion (`anthropic.com/news/cyber-verification-program`) and the LSVP page;
- Muse Ember;
- METR's 11-05 Anthropic assessment.

**Skipped:**
- **Gemini Decision 1 / Decisions API (11-11):** a discriminative scoring and routing model. It has no model card (`deepmind.google/models/model-cards/gemini-decision-1/` returns 404) and no safety evals, so it counts as auxiliary under covered_model_class.
- **Qwen4-Max-Preview (11-11):** coverage confirms there is still no model card, tech report or weights. Watch for Qwen 4 Max, reportedly due around 11-16.
- **OpenAI RSS 11-10 to 11-13:** children-first-declaration, helping-caregivers, ai-effect-on-freelance-work, closing-ai-guidance-gap-education, cogent-security, chatgpt-plus-for-veterans, plus customer stories. These are policy, economics or customer posts with no named-model evaluation. They could not be opened anyway (see below), so the judgment rests on titles and summaries. None looked like model documentation.
- **CVP portal news ("managed-service cyber productization" applications, about 11-12):** seen only in third-party coverage. I found no new Anthropic primary page.
- **Grok 4.8, Muse Spark 1.4, Qwen 4 Max:** predicted for 11-16 to 11-19, not yet released.

## Citation mining

- **Hydrogen card:** cites the Carbon and Argon Safety & Security Reports, both already catalogued.
- **SecureBio post:** cites the BioTIER paper (already catalogued as `securebio-gemini-3-1-pro-independent-eval`) and the Fable/Mythos 5.2 card (catalogued). The BioTIER trends dashboard is a live dashboard, not a document, so it was not proposed.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 16 openai.com / help.openai.com URLs (streaks 22-30), plus 4 new ones with streak 1. The new ones are yesterday's adds: daybreak-red-aws-govcloud, a-thousand-fewer-paths-to-root, securing-our-frontier-model-training-environment and measuring-how-ai-agents-handle-wet-lab-science.
- **My own fetches:** unlike yesterday, read_doc also got 403 on everything I tried (introducing-gpt-rosalind, a-thousand-fewer-paths-to-root, measuring-how-ai-agents-handle-wet-lab-science, the Daybreak help article). WebFetch got 403 too.
- **Alive check:** openai.com/news/rss.xml fetched fine and still lists these posts, so they are bot-blocked, not gone. No status changes.

## Document updates (task 6)

- **Top 5 (v1056, v773, v924, v1015, v573):** the same stale entries earlier runs judged as noise or already annotated. Skipped.
- **v1165 (METR Anthropic AI R&D assessment, new today):** a substantive checklist correction. Annotated (#4).

## Friction and proposals

Friction (2 entries):
1. `regression` of the RESOLVED read_doc / openai.com row: read_doc impersonation now gets 403 on openai.com.
2. A recurrence of the stale updated_docs top-5.

No new proposals. The openai.com RSS index proposal was filed yesterday.
