# cardtrack agent run — 2026-11-07 (run id 2026-11-07T06:16Z-local)

- **Lookback:** the last agent success was 2026-11-06T06:28:24Z, so the 72 h minimum applied (2026-11-04 to 11-07).
- **Weekly retrospective sweep:** not run. Today is Saturday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| Proposal | Verdict |
|---|---|
| field_update `openai-gpt-6-cyber-system-card` related_urls (+ `announcement` https://openai.com/index/introducing-gpt-6-cyber/, existing `web_version` kept) | written (doc 434) |

The GPT-6 Cyber announcement went unrecorded at add time (11-06) because openai.com returned 403. read_doc fetched it today. It is the same release: ExploitGym 48.5% vs 32.1% for GPT-5.6 Cyber, a Critical cyber classification, and Daybreak Red-only access.

No adds.

## Phase A candidates (21 first seen today)

Candidates first seen before today were triaged in earlier runs. All of today's were skipped:
- **SecureBio + RAND "Why Didn't LLMs Uplift Novices in the Lab?"** (borderline): mainly a reanalysis of the 2025 Active Site human uplift RCT, which used mid-2025 models.
  - It includes a secondary replay of participant transcripts through GPT-5.6 Sol, DeepSeek V4 Pro and GPT-OSS on fragment selection. Results are shown in figures only; Opus 5.5 and Gemini 3.8 Flash were left out because of refusals.
  - I judged it uplift-methodology research rather than a model eval, so it fails the system-card test. Skipped on "when in doubt, skip".
  - Revisit if the RAND-reviewed final version reports per-model results as the main finding.
- **Meta "Bringing Specialized Models to Muse and Meta AI":** a product post about unnamed "specialized models" trained with Muse Wonder. It has a few product metrics but no named model or card.
- **Anthropic:**
  - "Teaching AI to build scientific models": a guest essay from AI for Science grantees.
  - "The components of agent memory": an engineering and research essay on memory and dreaming, not a model eval.
- **Palisade "Announcing frominside.ai":** an interview project.
- **NVIDIA:**
  - Nemotron-Parse-3.5 space: parse/OCR, out of scope under the scope note.
  - GR00T-1.7 G1-Factory / PushButton-DSRL: task-specific fine-tunes of GR00T N1.7, which is already in the DB.
  - Nemotron-Terminal-Corpus, video-full-duplex-benchmark, VESPER: datasets.
- **Other:**
  - StepFun paper 2611.04386: a paper.
  - Epoch Huawei compute-gap piece: not model documentation.
  - Cursor voice chat: product changelog.
  - The rest: HF profiles and Substack author pages.

## Targeted search (11-04 to 11-07)

Searched for:
- generic system/model cards;
- Anthropic, Google DeepMind, xAI, the Chinese labs (Qwen, DeepSeek, GLM, MiniMax, MiMo, StepFun), Meta and Mistral;
- UK AISI, METR, Apollo and Epoch evals;
- trusted-access programs (Daybreak, Glasswing/Mythos, Fairwind, LSVP / Claude Science).

Findings:
- Everything found is already catalogued: GPT-6 Cyber, ChatGPT Images 2.6, Gemini Omni 1.2 Flash, Inkling 2 Small, the METR assessment, Gemini 4 Carbon (access post and evals page), Mythos 5.1 access rows, and LSVP.
- **Tencent Hy4:** still API-only. Weights and the system card are still promised "in the coming days". **Watch for it**: only Hy4-preview is in the DB.
- **Grok 5:** not released.
- **Anthropic "Open call for guest investigators in the life sciences":** a research-collaboration call where Anthropic runs the models. It is not a gate on model access, so not an access_policy. Skipped.
- **Xiaomi "MiMo Model Safety Analysis Report":** dated 2025-12-22, before the 2026-01-01 scope floor. Skipped.
- **Artificial Analysis "trusted-access models" cyber index:** publisher not allowlisted.

## Citation mining

- Yesterday's adds were mined in the 11-06 run.
- Today I read the GPT-6 Cyber announcement. It cites the system card (in DB), Mozilla's Firefox advisories, and partner use (Cisco, Calif, CodeRabbit). None of these are model documentation.

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs returned 403 again (streaks 16-30).
- **My own fetches:** read_doc got **HTTP 200** via browser_impersonation on all five I tried:
  - introducing-gpt-rosalind
  - introducing-the-rosalind-academic-plan
  - low-resource-programming-languages
  - the Daybreak trusted-access help article
  - hugging-face-model-evaluation-security-incident
- **Alive check:** the pages are alive, so there are no status changes.

## Document updates (task 6)

- **v1082 (`metr-claude-3-7-sonnet-independent-eval`):** the only new version. It is noise: a "Footnotes" heading was added and the footnote back-arrow glyph changed. Not annotated.
- **Older entries:** the other entries (top five: v1056, v773, v924, v1015, v573) were judged noise or annotated in earlier runs. Skipped.

## Friction and proposals

Friction, two recurrence entries:
1. Phase A still gets 403 on openai.com while read_doc succeeds today.
2. The stale updated_docs ranking.

No new proposal.
