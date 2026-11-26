# Run report — 2026-11-26T06:17Z-local

Last agent success: 2026-11-25T06:28Z. Search window: the 72 h minimum (since 2026-11-23). Today is a Thursday, so there was no weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | `openai-gpt-6-2-other`: https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/ (GPT-6.2 / GPT-6 / GPT-5.6 protein-design capability report, wet-lab validated with Onava; `other`, closed, `cbrn`, has_safety_evals false) | **written** (doc 497, v1343) |
| 2 | add | `zai-glm-5-4-model-card`: https://docs.z.ai/guides/llm/glm-5.4 (GLM-5.4, Z.ai's first Loop Transformer flagship, 2026-11-23; closed, no risk domains, has_safety_evals false) | **written** (doc 498, v1344) |
| 3 | add | `google-deepmind-gemini-4-argon-other-2`: https://deepmind.google/blog/interpreting-mass-spectra-with-google-antigravity/ (three-arm Mass Spec Skills evaluation of Gemini 4 Argon, Gemini 4 Carbon and Gemini 3.8 Flash; `other`, closed) | **written** (doc 499, v1345) |
| 4 | add | `google-deepmind-gemini-4-neon-system-card`: https://storage.googleapis.com/deepmind-media/gemini/gemini_4_neon_safety_report.pdf (the full Gemini 4 Neon Safety & Security Report; `system_card`, closed, all five risk domains, `publication_date` null) | **written** (doc 500, v1346) |
| 5 | annotate_version | `google-deepmind-gemini-4-neon-model-card` v1338: the Safety & Security Report went from "coming soon" to a live link | **written** |

Notes on the adds:

- **#1** is a capability report, not a safety assessment, so `has_safety_evals` is false while `cbrn` is tagged: the measured content is dual-use biological design (322 minibinders against 5 targets, 35 hits; antibody-loop redesign 128/182 and 179/272; DockQ 0.05 → 0.28 → 0.57 across GPT-5.6 → GPT-6 → GPT-6.2), and the only risk content is one paragraph deferring to the Preparedness Framework. The companion preprint PDF on cdn.openai.com is **over the 50 MB fetch cap**, so I could not read it; it went in as a `full_document` related URL and the HTML post is the canonical row. Logged as friction.
- **#2**: the z.ai blog is a client-rendered 2 KB JS shell (as `sources.yaml` already records for this publisher), so the fetchable docs page is the canonical row and the blog is the announcement. Date 2026-11-23 comes from the announcement plus the blog's dated asset path; the docs page itself is undated and the z.ai release-notes index still listed GLM-5.3 as newest. No weights, no HF card, no arXiv report yet.
- **#3** is a product post that nonetheless passes the system-card test: it reports a controlled three-arm ablation (no internet/no skills, internet only, internet plus skills) over 100 Enamine REAL MS/MS compounds for three named Gemini models — under 4% accuracy from peak lists alone, about 97% with the skills, and token-cost reductions per model. The 10,000-scientist Antigravity offer in the same post gates a product usage tier, not a model, so it is not an `access_policy`.
- **#4** is the one that mattered: Google published Neon's safety report between our 2026-11-24 and 2026-11-26 fetches. It carries the FSF v3.1 Material Capability Change assessment (GCI v2 below threshold vs Argon, so determinations are carried forward: biological CBRN and cyber uplift CCLs cannot be ruled out, stealth/situational-awareness TCL cannot be ruled out, chemical/radiological/nuclear TCL, harmful manipulation and both ML R&D CCLs not reached), agentic-misuse results (0.09% misaligned action rate, 99.2% agent honesty, 2.45% coding shortcuts), mental-health and health policy adherence, adaptive IPI red-teaming (86% resistance over 150 attempts, 0% on Gray Swan's benchmark) and cyber results (70.7% CWE-bench v2, 90.5% SEC-bench Pro, 51.26% WebExploitBench v1.2, 48.3% ExploitGym at 10 h, 76% AutoBaxBench hard). `publication_date` is null because the PDF says only "November 2026", the landing page says only "Published: November 2026", and Wayback has no capture — the same handling as the Hydrogen safety report row.

## Task 1: Phase A candidates (first_seen 2026-11-26)

- **deepmind.google mass-spectra post**: proposed (#3).
- **anthropic.com/research/migrating-api-to-rust**: skipped, engineering blog.
- **nvidia/Nemotron-3.5-Rerank-1B-BF16**: skipped, text ranking is excluded by NVIDIA's scope note.
- **nvidia/NV-Reason-PathWSI**: skipped. A pathology whole-slide-image VLM for report generation and slide QA — a domain task model outside the Nemotron/Cosmos/GR00T scope, with no safety evals. Same call as BioReason-Pro-2 yesterday.
- **tencent/WePocketModel1.0-2B-MLX and -4B-MLX**: skipped, MLX re-uploads of the on-device models already ruled out of scope on 2026-11-23.
- **cursor.com/en-US/legal**, HF user profiles, the `tencent/wepocketmodel` collection, NVIDIA's Nemotron-Parse blog and its Synthetic-Tables/Synthetic-Charts/OCR-Synthetic datasets, the Baidu ERNIE 5.5 Flash Space, and the AIRIS / Agentic LongLive / VisualCreation paper pages: skipped as furniture, datasets or research papers. The VisualCreation paper (2611.31358) is already a related URL on doc 495.
- Older carried-over candidates were triaged in earlier runs and not revisited.

## Task 2: Targeted web search

Queries: system card Nov 25-26 2026; new model-card/open-weight releases November 2026; trusted-access programs November 2026; Nov 25 AI news roundups (riorundown, theneuron); Qwen 4 Max model card; GLM-5.4 / Grok 4.8; UK AISI / METR / Apollo on Fable 5.2 and GPT-6.2; "Gemini 4 Neon Safety & Security Report"; Anthropic LSVP / Cyber Verification Program / Project Glasswing; OpenAI Daybreak / GPT-Rosalind.

Results:

- **GLM-5.4** (Z.ai, 2026-11-23) was uncatalogued: proposed (#2). Z.ai's last entry was 2026-08-28, so this also closed out the longest-silent tier-1 lab.
- **OpenAI protein-design report** (2026-11-24): proposed (#1).
- **Qwen4-Max**: still API-only with no model card, technical report or weights — unchanged from previous runs.
- **Grok 4.8**: still not shipped; no card.
- **Daybreak Blue policy changes** (individual API access removed 2026-11-20, session training from 2026-11-29): communicated to users by email and covered only by third parties. The public surface is the Daybreak overview help article, which is already catalogued (`openai-gpt-5-6-sol-access-policy`) and carries no dated change notice, so there is nothing to add; the monitor will pick up the page revision.
- **OpenAI "Broadening access to AI for scientists"** (2026-11-24): skipped. The expanded ChatGPT for Academic Researchers program gates a free ChatGPT Plus grant, not a model or model family; the Rosalind Academic Plan it references is already catalogued.
- **Anthropic Cyber Verification Program / Project Glasswing merge and LSVP**: no change since the October and September posts already in the database.
- **Already cataloged**: Fable 5.2 (card, access policy, risk report), GPT-6.2 Astra/Sol and GPT-6.2 in ChatGPT, Gemini 4 Neon model card and evals methodology, GPT-Rosalind-6, METR's Anthropic risk-report reviews.
- **Not allowlisted / out of scope**: PrismML Ternary Bonsai 2.5 27B, Midjourney Niji V8, Agnes 2.5 Pro Theta, Zyphra ZONOS3-Mini, Runway Praxis-1, the White Circle post-training competition, Anthropic's neuron-interpretability research and the Axios story.

## Task 3: Citation mining

- **Neon safety report** cites the Gemini 4 Argon safety report and the Fairwind Program announcement (both in the database); its external benchmarks come from Gray Swan, Collinear AI, Artificial Analysis and AgentCyberRange, none allowlisted — already covered by the 2026-09-09 PROPOSALS entry, so not re-filed.
- **OpenAI protein report** cites RFdiffusion, ProteinMPNN, SolubleMPNN, Boltz-2, OpenDDE, ESMFold2, ESM2-650M, MotifBench, PoseBusters and the Scarpino set: academic tools, no allowlisted publisher.
- **GLM-5.4 docs** cite the GLM-5.3 technical blog (in the database) and the 2018 Universal Transformer paper.
- Nothing new to propose.

## Task 4: Open issues

`fetch_ok: true`, and the list is empty.

## Task 5: Blocked URLs

`blocked_escalations` is empty. `phase_a_summary.blocked` lists the same seven HF pages at HTTP 429, now on streak 2: tencent/Hy4-flash, tencent/Hy4, baidu/ERNIE-5.5-Flash-Base, baidu/ERNIE-Image, inclusionAI/LingSante-3.1-flash, LingSante-3.1-air-VL and Ling-3.2-air. I re-fetched all seven with read_doc and every one returned HTTP 200 with its full card, so they are alive and this is transient rate limiting on the monitor's own fetch. No `status_change` proposed. `not_found` is empty.

## Task 6: Document updates

Top 5 in order: v1304 (Hydrogen system card — judged U+200B noise 2026-11-25), v1056 (Fangcun eval — judged PDF layout noise 2026-11-04), **v1338 (Gemini 4 Neon model card — new, substantive, annotated as #5)**, v773 (HF widget noise, 2026-10-08) and v1170 (furniture, 2026-11-14). The four already-judged entries were not re-read; they hold the queue because there is no way to dismiss a version, which is the open 2026-10-28 PROPOSALS entry.

## Task 7: Friction logged

- `recurrence` (of 2026-11-22T06:25:40Z): Phase A's HF 429 is back on the same seven pages while read_doc gets HTTP 200.
- `tooling`: the pipeline's own 50 MB fetch cap, not just WebFetch's 10 MB, blocks the OpenAI protein-biology preprint, so the document carrying the evaluation tables cannot be read or catalogued at all.
- `recurrence` (of 2026-08-18T07:55:20Z): another undated DeepMind safety report, so another `publication_date: null` row.

## Task 8: Proposals

One filed: **"Promised companion documents ('safety report coming soon') are tracked only in prose, and both recent catches were luck."** Hydrogen's report was found four days late by hand-carried watch notes across three run reports; Neon's was found today only because its model-card diff happened to rank third in `updated_docs`. The entry asks for a derived `pending_documents` watch (probe the sibling `<model>_safety_report.pdf` URL each run) and for storing the last-404 / first-200 bounds, which would also date these otherwise-undated reports.
