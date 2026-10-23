# cardtrack agent run — 2026-10-23 (run id 2026-10-23T06:17Z-local)

- **Lookback:** the last agent success was 2026-10-22T06:25:57Z, so the search used the 72 h minimum (2026-10-20 to 10-23).
- **Weekly retrospective sweep:** not run. Today is Friday.
- **Open issues:** `fetch_ok: true`, no open issues. Task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | MiniMax-M3.1-Flash HF model card | **written** → `minimax-minimax-m3-1-flash-model-card` (doc 400) |
| 2 | add | METR, "Red-Teaming OpenAI's Internal Agent Monitoring Systems" (2026-10-22) | **written** → `metr-gpt-5-5-independent-eval` (doc 401) |
| 3 | add | Redwood Research co-published copy of #2 | **written** → `redwood-research-gpt-5-5-independent-eval-2` (doc 402) |
| 4 | add | Anthropic, "LLMs are making formal software verification feasible at a much larger scale" (2026-10-22) | **written** → `anthropic-claude-opus-5-5-other` (doc 403) |
| 5 | add | inclusionAI Ling-3.0-flash-Sante HF model card | **written** → `inclusion-ai-ling-3-0-flash-sante-model-card` (doc 404) |
| 6 | annotate_version | `nvidia-nemotron-3-5-super-vl-other` v920 | **written** |
| 7 | annotate_version | `metr-gpt-5-independent-eval` v921 | **written** |

- **#1 MiniMax-M3.1-Flash** (closes yesterday's watch item):
  - **What it is:** about 428B total / 23B active, multimodal MoE, 1M context. Announced on the MiniMax blog (minimax.io/blog/minimax-m31f, Oct 19), which is recorded as the announcement. The HF weights and card went public 10-23 (repo created 10-17 while private), so publication_date is 2026-10-23.
  - **Flags:** minimax-community license → `open_weight_restrictive`. `has_safety_evals: false`: the only cyber content is a CyberGym capability score (82.2) in a benchmark table, which matches how the Kimi K3 card row was tagged.
- **#2 / #3 METR + Redwood OpenAI monitoring red-team:**
  - **What it is:** a three-week, high-access, on-site stress test of OpenAI's internal misalignment monitoring.
  - **Findings reported:**
    - 75–94% of agentic Responses API traffic from models ≥ GPT-5.5 was eligible for monitoring.
    - RL rollouts were not covered when the exercise started.
    - About 10% of Codex traffic went unmonitored through compaction events.
    - A sandbox/Auto-Review bypass, headers that disable monitoring, and serialization-based monitor evasion.
  - **Precedent:** the METR Anthropic agent-monitoring red-team row (`metr-claude-opus-4-6-independent-eval-4`).
  - **Model names:** the subject is a safeguard system, not a model checkpoint. GPT-5.5 is recorded as the only model the post names (as the coverage threshold). The operator may want to review that choice.
  - **Co-publication:** both orgs are allowlisted, so each copy got its own row, cross-referenced in `notes` and `related_urls` (co_published). Tagged `loss_of_control`.
- **#4 Anthropic formal verification:**
  - **What it reports:** Claude proved no-crash properties at the RISC-V level for 239 entry points across 123 OSS-Fuzz libraries. On 36 tasks, "Opus 5.5 proves half of them with about 40% fewer tokens than Opus 5".
  - **Classification:** doc_type `other`, matching the precedent of Anthropic research posts that report measured results for named models. The work is defensive, so `has_safety_evals: false` with no tags.
- **#5 Ling-3.0-flash-Sante:**
  - **What it is:** a separately named healthcare post-train of Ling-3.0-flash (124B/5.1B, MIT). Notability comes from OpenRouter, Vercel, and other API listings.
  - **Flags:** `has_safety_evals: true` because the card reports two healthcare-safety benchmarks (AFUMED-Drug, AFUSAFE-MedSCE). risk_domains is empty because medical-advice safety is not one of the 5 domains.
  - **Borderline call:** it is a domain fine-tune of an existing model. I admitted it under `when_uncertain: admit_and_flag`.
- **#6 / #7 annotations:**
  - **Nemotron 3.5:** a revised edition dated 10-21. It adds a pointer to the mid-training recipe paper (arXiv 2610.22019) and about 15 authors.
  - **METR GPT-5:** one new footnote on human baseline times, plus renumbered footnotes.
  - **Evidence URLs:** for both, I passed a generic URL (the HF repo / metr.org) rather than the exact document URL. This is harmless for annotations, but worth noting.

## Phase A candidates

- **Already triaged:** everything first seen before 10-23 was handled in earlier runs.
- **New today (31 links):** proposed #1–#5 above. Skipped the rest:
  - **Anthropic "Open call for guest investigators in the life sciences":** an 8–12-week research-collaboration program for academic and nonprofit PIs. It names no model or family, and it gates collaboration, not capability access. It points to LSVP, which is already in the DB.
  - **Anthropic "Donating Agent Skills to the Agentic AI Foundation":** governance/ecosystem post.
  - **xAI Frontier AI Framework PDF (dated 30 June 2026, now linked from x.ai/safety):** a general safety framework, not about a specific model.
  - **xAI "SpaceX Super Intelligence Partner Network" and /startups:** partnership and program marketing.
  - **DeepMind "Beyond tree cover: mapping the world's forest types":** an application showcase with no named-model eval.
  - **RAND PEA5394-1:** a DOE RFI response on power-grid security, not a model eval.
  - **NVIDIA RE-USE / RE-USE-laughter:** audio-to-audio models (auxiliary).
  - **NVIDIA Wan2.2 FP8:** a quantized re-host.
  - **Other NVIDIA leads:** the Cosmos-Embed1 discussion, a Foundation4D paper link, and a collection.
  - **inclusionAI Ming-3.0-tts-tiny discussion:** a README update for a TTS model.
  - **Rest:** HF profile pages (MiniMax, NVIDIA, inclusionAI).

## Targeted search (10-20 to 10-23)

- **Already in DB:** Haiku 5.5 card, GPT-6 October update, GPT-Live-1.1, Muse Spark Open card + methodology, Fairwind Program, METR Opus 5.5, Qwen3.6-27B.
- **Claude Duet watch item:** still no dedicated safety write-up. The X post repeats "We'll share more on our approach to safety in Claude Duet soon." Keep watching.
- **GLM-5.3 Fast:** a speed-optimized serving variant of GLM-5.3. It does not count as a distinct release, so I skipped it.
- **Restricted-access programs:** nothing new beyond the CVP, Daybreak, and Fairwind pages already in the DB.
- **Silent-org (>14 days) check:** not done. A /tmp helper that computes each publisher's newest date needed a Bash approval that wasn't available in this headless run.

## Citation mining

- **METR/Redwood post:** cites the Frontier Risk Report and the Hugging Face incident investigation, both already in the DB. It also cites "Our approach to working with AI companies", a policy essay, which I skipped.
- **Anthropic formal-verification post:** cites Theorem (collaborator, not allowlisted, and not a co-published copy).
- **MiniMax card:** cites no predecessor documents.
- Nothing new to propose.

## Blocked-URL escalations (task 5)

- **Status:** 15 openai.com/help.openai.com rows at streak 22 (17 for accelerating-cyber-defense-ecosystem, 7 for the Rosalind Academic Plan). low-resource-programming-languages is new at streak 1.
- **Spot checks:**
  - hugging-face-model-evaluation-security-incident: HTTP 200 via browser_impersonation.
  - Daybreak help article and low-resource-programming-languages: 403 from read_doc.py and from WebFetch. Both are bot blocks rather than gone pages. The help article is indexed in today's search results, and the low-resource post loaded yesterday.
- **Conclusion:** all alive. No status changes.

## Document updates (task 6)

- **Annotated:** Nemotron 3.5 v920 and METR GPT-5 v921 (see above).
- **Skipped as extraction noise:** three Anthropic pages refetched today: `anthropic-claude-mythos-preview-other-3` v924 (robotics), `-other-2` v922 (cryptography), `-other-7` v933 (BioMysteryBench).
  - All three show the same pattern: section headings now extracted, footnotes, related-post teasers and the newsletter box dropped, and some figure/table text (task table, a quoted Mythos analysis) no longer extracted.
  - The cause looks like an anthropic.com template change, not an edit to the content.
- **Older queue entries:** DeepSeek, Qwen, Kimi, GLM, and the others were judged in earlier runs.

## Friction and proposals

- **Friction, one entry:** `recurrence` of 2026-10-06T06:29:51Z (the openai.com 403 streak). This time read_doc.py was also blocked on 2 of 3 URLs.
- **No new proposals.**
