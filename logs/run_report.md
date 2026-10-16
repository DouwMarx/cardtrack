# cardtrack agent run — 2026-10-16 (run id 2026-10-16T06:16Z-local)

- **Lookback:** the last agent success was 2026-10-15T06:27:46Z, so the search used the 72 h minimum (2026-10-13 to 10-16).
- **Weekly retrospective sweep:** not run (today is Friday).
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (system_card) | OpenAI "GPT-Live-1.1 System Card" (2026-10-15; closed; safety evals; societal_harm, loss_of_control) https://deploymentsafety.openai.com/gpt-live-1-1/gpt-live-1-1.pdf | **written** (`openai-gpt-live-1-1-system-card`, doc 386, v852) |
| 2 | add (model_card) | Meta "Muse Spark Open Model Card" (2026-10-15; open_weight_restrictive; cbrn, cyber, loss_of_control) https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B | **written** (`meta-muse-spark-open-model-card`, doc 387, v853) |
| 3 | add (other) | Meta "Muse Spark Open Evaluation Methodology" (2026-10-15; cbrn) https://research.meta.ai/static/muse-spark-open-evaluation-methodology | **written** (`meta-muse-spark-open-other`, doc 388, v854) |
| 4 | add (independent_eval) | Apollo Research "GLM-5.3 Sometimes Considers How Train-Time Actions Shape Future Behavior" (2026-10-15; loss_of_control) | **written** (`apollo-research-glm-5-3-independent-eval`, doc 389, v855) |
| 5 | add (model_card) | NVIDIA Nemotron 3.5 Super VL 120B-A12B (BF16 card, 2026-10-15; open_weight_permissive; no safety evals) | **written** (`nvidia-nemotron-3-5-super-vl-model-card`, doc 390, v856) |
| 6 | add (other) | NVIDIA "Nemotron 3.5 Super VL and Lightning Technical Report" (2026-10-14; no safety evals) | **written** (`nvidia-nemotron-3-5-super-vl-other`, doc 391, v857) |
| 7 | add (model_card) | NVIDIA Nemotron 3.5 Bolt 74B-A9B 24GB (2026-10-15; open_weight_permissive; no safety evals) | **written** (`nvidia-nemotron-3-5-bolt-74b-a9b-24gb-model-card`, doc 392, v858) |
| 8 | add (access_policy) | OpenAI "Bringing GPT-Rosalind to academic research labs" (Rosalind Academic Plan, 2026-10-15; restricted) | **written** (`openai-gpt-rosalind-access-policy-5`, doc 393, v859) |

### #1 GPT-Live-1.1

- The deployment-safety hub page extracts to only a 1,100-character intro, so the PDF is canonical and the HTML page is recorded as `web_version`. This matches the GPT-Live-1 row, which is also a PDF.
- **Voice-native disallowed-content evals (production and synthetic):** OpenAI reports statistically significant regressions against GPT-Live-1 on sexual, mental health, emotional reliance and gore content.
- **Audio-converted alignment evals:** Respecting Warnings, Blocker Deception and Broken Search Tool, compared against GPT-5.6 Terra.
- **Preparedness:** a qualitative "not High" statement only, so it is not tagged cbrn/cyber.

### #2 and #3 Muse Spark Open

- Muse Spark Open is Meta's first open-weights Muse Spark: 816B/42B-active, under the Muse Model License, which requires attribution, imposes a usage policy, and requires a separate agreement for MaaS providers over $20M revenue. That makes it `open_weight_restrictive`.
- **Model card safety content:**
  - FORTRESS and StrongREJECT v2 results
  - cyber refusal: 99.2% internal, 94.8% on public benchmarks
  - chem/bio refusal: over 98% on BioTIER
  - loss of control: 98.1% honesty on MASK and 0% Agentic Misalignment
- **Methodology report:** a separate row, following the Muse Glimmer and Spark 1.3 precedent.
- **Still pending:** Meta says the full evaluation report is "available soon". Watch for it.

### #4 Apollo on GLM-5.3

- Apollo found unprompted "update-aware reasoning" (a precursor to alignment faking) in about 1 to 2 per 1,000 rollouts, on ImpossibleBench and shutdown-resistance reimplementations.
- `openness` is omitted: GLM-5.3 ships under a custom "glm-5.3" license I did not verify.

### #5–7 NVIDIA Nemotron 3.5

- **Notability:** NVIDIA's blog launch on 10-15, plus SiliconANGLE, HPCwire and Unite.AI coverage. The license is OpenMDW-1.1.
- **Distinctness:** Bolt is compressed from Super VL, but it is announced as its own named tier with its own architecture and training, so it gets its own card row.
- **Technical reports:**
  - The Super VL + Lightning report is a separate row, following the nvidia-nemotron-3-ultra-other precedent.
  - The Bolt technical report is a compression/quantization report with no safety content. It is recorded as a `paper` companion on the Bolt card rather than a separate row. An operator may want to split it out for consistency.
- **Variants not proposed:** Super VL NVFP4/NVFP4-LiLiCorr/Base-BF16, and Bolt BF16/GGUF/LiLiCorr/LiLiCorr-GGUF.
- **Not yet released:** Bolt E4B 4GB is due 10-23. Watch for its card.

### #8 Rosalind Academic Plan

- Sourced from the background search. I read it via read_doc (browser impersonation) and confirmed the "October 15, 2026" date in the page HTML.
- It is a vetted-access tier for GPT-Rosalind: US academic labs, PI identity and institution verification, and an institutional safety contact. That makes it `restricted`, with no safety evals.

## Phase A candidates

- **Already triaged in earlier runs:** everything first seen 10-02 to 10-15.
- **New today (66), skipped:**
  - **anthropic.com/news/an-update-on-independent-evaluators (10-15):** a governance post about evaluator access tiers (METR embedded, SecureBio, Accenture/Faculty). It names no model, so it is not an access_policy.
  - **deepmind.google "Accelerating the search for antimicrobial peptides with Google Antigravity":** a product/science walkthrough with no model evaluation.
  - **mistral.ai Timestral:** a 209M time-series forecasting model, outside the Mistral scope note and outside `covered_model_class`. No card.
  - **securebio "Taking our core computational pipeline private" (both URLs):** an organisational policy post.
  - **RAND CFA4954-2 (bio-threat resilience conference proceedings):** policy proceedings with no model eval.
  - **HF papers, user profiles, datasets, collections and chat-template discussions (Qwen, Tencent, NVIDIA, zai, inclusionAI, stepfun):** not documents.
    - The Ling 3.1 collection holds only Ling-3.1-flash (added yesterday).
    - The Step-5-Preview collection was covered yesterday.
  - **NVIDIA:**
    - embed/rerank 8B/1B: auxiliary models.
    - Muse-Spark-Open-DFlash2 and Qwen3.8-Flash-Next-FP4-Local: drafter and quant artifacts.
    - Kimodo/ARDY motion models, GEM-X, VoMP, PixelDiT2: not Nemotron/Cosmos/GR00T releases with announcements.
    - Nemotron variants: covered by #5 and #7.

## Targeted search (10-13 to 10-16)

A background subagent swept the lab indexes, the access-program list and the evaluator blogs. I verified its one new find (#8) myself.

- **Already in the DB:**
  - GPT-6 Sol/Luna October update (10-07): `openai-gpt-6-sol-october-addendum`
  - Gemini 4 Argon card, safety report and broader-access post
- **No new documents in window:**
  - Anthropic: system cards, CVP/Glasswing, LSVP, Claude Science
  - GDM: Flash Cyber/CodeMender, Gemini for Science
  - xAI: Grok Voice 3 has no card
  - Amazon, Microsoft, Qwen, DeepSeek, Kimi, GLM, MiniMax, MiMo, Hunyuan
  - Evaluators: METR (latest 10-06), UK AISI (latest 10-12, a best-practice essay), CAISSI, SecureBio, Transluce, Epoch, Gray Swan, Palisade, FAR.AI, RAND, Redwood, SaferAI
- **Out-of-allowlist releases seen:** Upstage Solar Pro 4, Jais 3, FLUX 3, Kling 4.0. These are noted only; none is a lab already proposed for the allowlist.

## Citation mining

- **Muse Spark Open card:** cites MASK, Agentic Misalignment and SecureBio's BioTIER benchmark. These are benchmarks, not model-specific third-party reports, so there is nothing to add.
- **Apollo GLM-5.3 post:** builds on Palisade's shutdown-resistance eval, which is already in the DB as a Palisade row.
- **GPT-Live-1.1, the Nemotron cards and the reports:** no citations of uncatalogued predecessor cards or external evals.

## Blocked-URL escalations (task 5)

- All 14 openai.com/help.openai.com rows are treated as **alive**: 13 at streak 15, plus accelerating-cyber-defense-ecosystem at streak 10.
- I spot-checked path-to-astra and introducing-gpt-rosalind with read_doc.py, and both returned HTTP 200 via browser_impersonation.
- No status changes were proposed.

## Document updates (task 6)

None were annotated. Every queued entry was fetched before the last agent run (the newest is 10-15T06:18), and all were judged noise in earlier runs: HF widget, download-counter, sample-code and furniture churn. Nothing new needed reading.

## Friction and proposals

- **Friction, one entry:** a `recurrence` of 2026-10-06T06:29:51Z: the openai.com 403 false alarm, now at 15 runs.
- **No new proposals.** The 403 issue was already filed on 10-07.
- **Note for operators:** the background subagent reported that its Bash calls were denied, so it could not use read_doc.py and fell back to WebFetch, which openai.com blocks. I re-read its openai.com find myself, so no document was proposed unread.
