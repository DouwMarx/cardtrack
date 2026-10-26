# cardtrack agent run — 2026-10-26 (run id 2026-10-26T06:19Z-local)

- **Lookback:** the last agent success was 2026-10-25T06:28:00Z, so the 72 h minimum applied (2026-10-23 to 10-26).
- **Weekly retrospective sweep:** done (Monday). I chose RAND, dots_studio and Z.ai. Their newest entries are 08-11, 08-14 and 08-28. The three orgs with older newest entries were swept in the last two weeks: Palisade and poolside on 10-12, Thinking Machines and SaferAI on 10-19.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | NVIDIA Nemotron 3.5 Bolt E4B 4GB model card (HF, GA 2026-10-23) | **written** → `nvidia-nemotron-3-5-bolt-e4b-4gb-model-card` (doc 410, v976) |
| 2 | add | Z.ai GLM-Image model card (HF, released 2026-01-14) | **written** → `zai-glm-image-model-card` (doc 411, v977) |
| 3 | add | RAND RR-A3892-2, "AI agents put offensive cyber within reach of novices" (PDF, 2026-06-25) | **written** → `rand-claude-opus-4-6-independent-eval` (doc 412, v978) |
| 4 | annotate_version | `meta-muse-wonder-model-card` v973 | **written** |

### #1 Nemotron 3.5 Bolt E4B 4GB
- **Lead:** found by search on benchlm.ai. Phase A surfaced the HF repo on 10-24, and that run skipped it as "a size variant of Bolt 74B".
- **Why I reversed that:** it's a distinct model. It is post-trained from Gemma 4 E4B, a different base than Bolt 74B. It also has its own card, research page and technical report (dated 2026-10-23). Under the 10-05 document-unit rule in criteria.yaml, that makes it a separate row.
- **Canonical URL:** follows the Bolt 74B precedent. The HF card is canonical, with the research page (announcement) and the tech-report PDF (paper) as related URLs.
- **Flags:**
  - `has_safety_evals: false`. There are only boilerplate subcard pointers and an AdvBench subset inside VoiceBench.
  - `open_weight_permissive`, because the weights are under OpenMDW-1.1.

### #2 GLM-Image
- **Lead:** found by the retrospective sweep. The HF API listing of zai-org shows a repo created on 2026-01-08 that the pipeline had never seen.
- **What it is:** a 9B autoregressive + 7B diffusion text-to-image model, MIT license.
- **Notability:** VentureBeat and The Batch covered it.
- **Scope note:** the zai note names only the "GLM LLM/VLM line" and excludes CogView *point releases*. GLM-Image is a flagship GLM-branded release, so I admitted it under `admit_and_flag` and recorded the ambiguity in notes.
- **Date and blog:** the date is the public announcement (Jan 14). The z.ai tech blog is client-rendered and I didn't read it, so it isn't recorded.

### #3 RAND RR-A3892-2
- **Lead:** found by the retrospective sweep.
- **What it is:** the follow-up to RR-A3892-1, which is already in the DB. RAND Europe re-ran its CTF challenges with Claude Code on Sonnet 4.6 and Opus 4.6. Every challenge was solved in under an hour, for under $20 in total.
- **Flags:** passes the system-card test; tagged `cyber`; `closed`. The HTML landing page is recorded as the announcement.

### #4 Muse Wonder v973
- **What changed:** the ExploitGym result was corrected from 92 flags (21 intended) to 20 intended flags, after a harness fix described in a 23 Oct update note. Meta says its risk threshold is unchanged.
- **Caveats:**
  - This version was ranked 12th in the queue, outside the top 5. I read it because it had been fetched today.
  - The evidence URL I cited was the Muse Wonder blog post, not the card URL (research.meta.ai/static/muse-wonder-model-card).

## Phase A candidates

Eight were new today, and all were skipped:
- **Profile pages:** two HF profiles (zecongtanghku, Jy1112).
- **Ling-3.1-flash discussions (2):** code-fix PRs.
- **inclusionAI/LBS-27B:** the README is empty.
- **HiSTEVE 1.0 (Tencent paper):** a research Minecraft VLA agent, not a flagship agent.
- **Qwen/BabelArena:** a benchmark dataset.
- **MiniMax-M3 collection:** M3 is already in the DB.

Everything first seen before today was triaged in earlier runs.

## Targeted search (10-23 to 10-26)

- **New and proposed:** Bolt E4B (#1).
- **Already in DB or handled:** Kimi K3.1 Pro, MiniMax M3.1 Flash, Gemini 4 Argon (all rows plus Fairwind), Haiku 5.5, the GPT-6 October update, and the CVP/LSVP pages. Mistral Voxtral 3 was skipped on 10-21 as an ASR/TTS family.
- **openai.com was readable today** (read_doc, browser_impersonation). That let me clear last run's unread lead.
  - **"Patch the Planet: global response coordination…" (coordinated-disclosure post):** skipped. It is a disclosure-framework and partnership post, with no measured evaluation. GPT-5.6 Sol is only named as the tool Calif used.
  - **June "Patch the Planet" launch post:** skipped. It's a partnership with Trail of Bits, HackerOne and Calif, and it gates no named model.
  - **"Daybreak for Frontline Defenders" ($1B subsidized Daybreak access):** skipped. It's an access expansion, but it names no model or model family, only "Daybreak cyber models". That fails the named-model gate, which is already discussed in PROPOSALS.md.
- **Restricted-access programs:** nothing new. Gemini for Science, Co-Scientist and CodeMender (Argon partner access from 10-13) are covered by existing rows.

## Weekly retrospective sweep

- **Z.ai:** I compared all 2026 repos in the HF API with the DB.
  - **Added:** GLM-Image (#2).
  - **Skipped:** SCAIL-2, an MIT research character-animation model outside the GLM line, from a github.io project page. The rest are -FP8/-BF16 re-uploads or GLM-OCR.
- **dots_studio:** nothing new. Every 2026 repo apart from dots3-note is OCR or TTS (auxiliary). The dots3-note card still says "Full Report (coming soon)". **Watch item:** the technical report.
- **RAND:**
  - **Added:** RR-A3892-2 (#3).
  - **Skipped:** RR-A3797-1 (bio benchmarking), published Nov 2025, before the scope floor.
  - **Already in DB:** RR-A4741-1/-2, RR-A4591-1, RR-A3892-1, RR-A5000-1 and RR-A5055-1.
  - **Out of scope:** the "Open-Weight AI Models Require Proportional Evaluation" perspective is a policy essay.

## Citation mining

- **RR-A3892-2:** its references are UK AISI's Mythos Preview cyber evaluation (in DB), red.anthropic.com/2026/mythos-preview (redirects to anthropic.com/research/mythos-preview, which is in DB as `anthropic-claude-mythos-preview-other`), and RR-A3892-1 (in DB).
- **Bolt E4B report:** cites Bolt 74B and Gemma 4 E4B, both in DB.
- **GLM-5.3 blog lead (z.ai/blog/glm-5.3):** still client-rendered, not retried.

## Blocked-URL escalations (task 5)

- **What Phase A reports:** all 16 openai.com / help.openai.com rows return 403 (streak 25 for most, 20 for accelerating-cyber-defense-ecosystem, 10 for the Rosalind Academic Plan, 4 for low-resource-programming-languages).
- **Spot check:** read_doc.py got HTTP 200 today on path-to-astra, low-resource-programming-languages, introducing-the-rosalind-academic-plan, the Daybreak help article and strengthening-societal-resilience-with-rosalind-biodefense. The content was intact.
- **Conclusion:** all are alive. The 403 is bot-blocking, so there are no status changes.

## Document updates (task 6)

- **Top 4 (DeepSeek V4.1 Flash v773, Mythos preview other-3 v924, V4 Pro v573, V4 Flash 0731 v578):** judged noise in earlier runs and not re-read.
- **#5, GLM-5.2 other v974 (Anthropic Frontier Red Team, the IoT self-replication post):** noise. The newsletter teaser was dropped, section headings ("Introduction", "A. Inference setup", "Appendix" and so on) surfaced in extraction, and one small window-time table no longer extracts. The body text is unchanged. No annotation.
- **Beyond the top 5:** Muse Wonder v973 was substantive and is annotated (#4).

## Friction and proposals

- **Friction, two recurrences:**
  - The openai.com 403 false alarm (of 2026-10-25T06:26:44Z).
  - The stale updated_docs queue, where noise-judged versions keep occupying the top-5 window (of 2026-10-24T06:21:27Z).
- **No new proposals.**
