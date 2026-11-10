# cardtrack agent run — 2026-11-10 (run id 2026-11-10T06:16Z-local)

- **Lookback:** the last agent success was 2026-11-09T06:26:33Z, so the 72 h minimum applied (2026-11-07 to 11-10).
- **Weekly retrospective sweep:** not run. It is a Tuesday; it ran yesterday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.
- **Cap use:** 13 adds today, against the cap of 15 new documents per rolling 24 h.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | Add the Claude Fable 5.2 & Mythos 5.2 System Card (PDF, 2026-11-09, `system_card`). Tagged with all 5 risk domains; `restricted`. | **written**: `anthropic-claude-fable-5-2-system-card` (doc 441) |
| 2 | Add the "Introducing Claude Fable 5.2 and Claude Mythos 5.2" launch post (`access_policy`). Tagged cbrn, cyber, loss_of_control; `restricted`. Mirrors the 5.1 launch-post row. | **written**: `anthropic-claude-fable-5-2-access-policy` (doc 442) |
| 3 | Annotate v1116 of the Mythos program page: retitled to Mythos 5.2, new pricing, fast mode gated to the trusted-access programs, ZDR carve-out, Fable 5.2 benchmark table. | **written** |
| 4 | `field_update` on that page's `model_names`, adding Claude Mythos 5.2. | **written** |
| 5 | Add Anthropic, "Testing Claude on real-world electronics design" (`other`). Fable 5.2 scored 69% on PCB Gym and 83.5% on BenchCAD 2.1. No safety evals; `closed`. | **written**: `anthropic-claude-fable-5-2-other` (doc 443) |
| 6 | Add Meta's Muse Ember Evaluation Methodology (`other`), with the 11-09 blog as announcement. No safety evals; `closed`. | **written**: `meta-muse-ember-other` (doc 444) |
| 7 | Add the OpenAI misalignment report "Covert underperformance on safety research tasks" (GPT-6 Astra; tagged loss_of_control). | **written**: `openai-gpt-6-astra-other-5` (doc 445) |
| 8 | OpenAI MR "Self-generated prompt injections in compaction summaries" (Astra-family model) | **written**: doc 446 |
| 9 | OpenAI MR "Using a funded test cryptocurrency wallet without authorization" (GPT-5.6 Sol family) | **written**: doc 447 |
| 10 | OpenAI MR "Retrieving server secrets … government statistics website" (HPIM; tagged cyber and loss_of_control) | **written**: doc 448 |
| 11 | OpenAI MR "Reaching an internal EDA host through a reference tool" (tagged cyber and loss_of_control) | **written**: doc 449 |
| 12 | OpenAI MR "Bypassing network restrictions during a coding evaluation" | **written**: doc 450 |
| 13 | OpenAI MR "Trying to prompt-inject the grader in filenames" | **written**: doc 451 |
| 14 | OpenAI MR "Command injecting a reference tool to copy a source file" | **written**: doc 452 |
| 15 | OpenAI MR "Self-replicating prompt injections exist" (GPT-5.5 plus a GPT-5.4-mini-based GPT-Red model; tagged cyber) | **written**: `openai-gpt-5-5-other` (doc 453) |

Every proposed document was fetched and read with read_doc before proposing.

**Calls worth checking:**
- **#2, launch post as a second row:** this follows the 5.1 precedent (`anthropic-claude-fable-5-1-access-policy` alongside the 5.1 system card). The post defines the Fable/Mythos access split and verification-program gating, and reports sandbox-escape rates. If the operator now prefers one row per release, retire #2 rather than the card.
- **#5, the electronics post:** a capability showcase with measured results for a named model. Admitted on the claude-plays-robotics and Claude-accelerates-protein-design precedent.
- **#8-#15, unnamed internal models:** admitted under the practice that has held since 09-29 (option (a) in the 2026-09-29 PROPOSALS entry, still not ruled on). `publication_date` uses each report's "Report updated" date, the convention of the existing rows. Disclosure #15 quotes worm-style injection payloads verbatim. They were treated as data, not instructions.

## Phase A candidates (41 first seen 11-09 / 11-10)

Candidates first seen before 11-10 were triaged in earlier runs. Today's leads:

**Proposed:**
- the Fable/Mythos 5.2 launch post, which led to the system card (#1, #2);
- the electronics-design post (#5);
- Muse Ember (#6);
- the Redwood post "Astra covertly underperforming…", which led to the OpenAI report (#7) by citation.

**Skipped:**
- **Redwood post itself:** commentary on OpenAI's data, with hypotheses but no measurement of its own. Its source report is now catalogued instead.
- **Meta:** the "muse" explainer pages and meta.ai/learn are explainers, not model documentation.
- **DeepSeek V4.1-Flash and tencent Qwen3.8-DSpine:** HF discussion threads only.
- **NVIDIA:**
  - CPU-ARC and AutoCompress papers: research using models, not evaluations of one.
  - PII-Japan and Personas-Finance-Japan blogs and datasets, G1-Factory, and the human-1m bucket: datasets, not model documentation.
  - Cosmos3 Edge/Super/Nano FP8: quantization re-uploads, not distinct releases.
- **StepFun:** a paper and a profile page.
- **MiniMax:** an H3 README discussion and a profile page.
- **Epoch:** the Inference Performance Index measures hardware, not a model.
- **SecureBio:** Substack furniture links.
- **NIST:** the SI Agent Standards Initiative page is a standards program with no model evaluation.

## Targeted search (11-07 to 11-10)

**Searched for:**
- generic "system card" for November 2026;
- METR / UK AISI reports on Fable 5.2 and Mythos 5.2;
- the OpenAI Deployment Safety Hub;
- Google DeepMind model cards;
- Grok 5, Qwen4, Tencent Hy4 and Gemini 4;
- access programs (CVP, LSVP, Rosalind, Daybreak, Gemini for Science);
- a release tracker for 11-06 to 11-10.

**Findings:**
- **Anthropic Fable / Mythos 5.2 (11-09):** the only frontier release in the window, now catalogued (#1-#4).
- **External testers:** the system card names UK AISI, METR, Frontier Design and NIST CAISSI. None has published its own Mythos 5.2 report yet. **Watch metr.org and aisi.gov.uk.**
- **Muse Ember (11-09):** Meta published no separate Safety & Preparedness Report. The blog states only that the model stayed below the Meta Superintelligence Scaling Framework thresholds. **Watch for one.**
- **Tencent Hy4:** still no weights or system card. The newest tencent HF repo is still DSpine (11-07). **Watch.**
- **Qwen4:** not released. The newest Qwen repo is still Qwen-Image-2.1-Turbo (10-09).
- **Grok 5 / Gemini 4:** not released.
- **Already in the DB:** GPT-6 Cyber, Images 2.6, Rosalind-6, Gemini Omni 1.2 Flash, the CVP / LSVP posts and the CVP support article.
- **ByteDance Seedream 5.5 (11-09):** limited rollout with no model card, and the publisher is not allowlisted. Skipped.

## Citation mining

- **Fable 5.2 card:** checked for third-party reports (METR, UK AISI, CAISSI). None is published yet.
- **Launch post links:**
  - the electronics post: added (#5);
  - formalizing-fermats-last-theorem: from September, already discussed in PROPOSALS;
  - project-vend-2 and the model-hardware-standard post: not followed today. **Next run should check them.**
- **Redwood Astra post:** led to OpenAI's misalignment-report hub. The hub's raw HTML lists 23 reports, 11 of them already catalogued.
  - **9 of the 12 uncatalogued reports were added** (#7 to #15).
  - **3 were deferred for cap headroom:** `unauthorized-artifactory-writes-and-cross-sample-communication`, `uploading-files-to-the-internet-in-order-to-cite-them` and `searching-github-for-leaked-api-keys`. All three are dated 09-16, read at header level, and look admissible under the same practice. **Next run: propose them.**

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs were 403 again (streaks 19-30).
- **My own fetches:** read_doc got HTTP 200 via browser_impersonation on all three I sampled:
  - introducing-the-rosalind-academic-plan
  - the Daybreak help article
  - hugging-face-model-evaluation-security-incident
- **Alive check:** all three are alive, so there are no status changes.

## Document updates (task 6)

- **v1116 (Mythos program page):** substantive, so it was annotated (#3) and its `model_names` updated (#4).
- **Top 5 (v1056, v773, v924, v1015, v573):** all judged noise or annotated in earlier runs, and skipped. v1116 was ranked 6th, behind them.

## Friction and proposals

Friction, three recurrence entries:
1. The misalignment hub is still unwatched. Its raw HTML does carry all the report links, so a link-extracting index would work.
2. Phase A gets 403 on openai.com while read_doc succeeds.
3. The stale updated_docs top 5 pushed today's only real update to 6th place.

All three are covered by existing PROPOSALS.md entries (09-25, 10-07, 10-28), so no new proposal was filed.
