# cardtrack agent run — 2026-11-02 (run id 2026-11-02T06:15Z-local)

- **Lookback:** the last agent success was 2026-11-01T06:24:23Z, so the 72 h minimum applied (2026-10-30 to 11-02).
- **Weekly retrospective sweep:** run, because today is Monday (UTC).
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| Proposal | Verdict |
|---|---|
| add `https://alignment.openai.com/how-we-detect-frontier-model-misalignment/` (OpenAI, `other`, 2026-10-29) | **written** → `openai-gpt-6-astra-other-3` (doc 425, v1043) |

About this add:
- **What it is:** OpenAI's own report on its four-layer misalignment-monitoring system.
- **Why it passes the system-card test:**
  - It reports quantitative monitor-recall evals with intervals: real incidents, synthetic incidents, Sneaky Sandbox Escape, and Monorepo Sabotage.
  - It compares GPT-5.6 Luna, Terra and Sol as monitor models (20.4% vs 63.4% vs 79.6% recall on real incidents).
  - It replays the Hugging Face incident.
  - It describes the external-deployment safeguard for Astra-class models.
- **Fields set:**
  - model_names: GPT-6 Astra and the three GPT-5.6 models
  - openness: closed
  - risk_domains: loss_of_control
  - has_safety_evals: true

## Phase A candidates (9 first seen today)

All 9 were skipped:
- **3 Hugging Face user profiles:** An998, onepiece1999, qcf568.
- **Tencent HF papers:** WeFair (query rewriting) and Wizard (world manipulation). Both are research papers, not model documentation.
- **NVIDIA HF paper:** "Lost in Latent Space". It is a 2025 physics-emulation study and predates the scope floor.
- **inclusionAI papers:**
  - Venus-DefakerOne2 is a forensics detector, which is an auxiliary model class.
  - TextSleuth is from 2024.

Everything first seen before today was triaged in earlier runs.

## Targeted search (10-30 to 11-02)

The new add came from search. Everything else I found was already in the DB:
- GPT-Rosalind-6 addendum
- GPT-6 Luna 10-29 addendum
- GPT-6.1 Terra
- Gemini 4 Carbon (evaluation and access policy) and Fairwind
- Gemini 4 Argon card, safety report and evaluation
- Nano Banana 2.1
- Kimi K3.1 Pro
- Mistral Large 4 OSS
- Epoch's GLM-5.3 patch-gap and Cyber ECI work
- Apollo's GLM-5.3 work
- The AISI posts up to 10-26
- The Fangcun DeepSeek-V4.1-Flash-1017 eval (its HF paper, 2610.35671, is already a related URL)
- The METR and Redwood red-teams of OpenAI monitoring

Indexes checked: the OpenAI Deployment Safety hub (newest is 10-30), the DeepMind model-card index (newest is Argon, 10-13), the AISI blog (newest 10-26), and Epoch latest (newest is a 10-30 data insight on bioRxiv LLM acknowledgements, which is not model-specific).

Skipped:
- **OpenAI Model Spec update and the GPT-6 sycophancy change:** reported in newsletters. The Model Spec is not model-specific. The sycophancy item corresponds to the Luna 10-29 addendum, which is already in the DB.
- **"DeepSeek V4.1 Flash Cyber":** the DeepSeek news and API docs have no such release. It is the community re-host that was excluded on 11-01.
- **Still unreleased:**
  - Grok 5: no card.
  - Kimi K3.1 Pro weights: due by 11-04. Watch for a moonshotai Hugging Face card.
- **Restricted-access polling:** nothing new on any program beyond what is catalogued. Programs polled:
  - LSVP and CVP (CVP's Mythos 5.1 tiers were already covered 10-06)
  - Rosalind
  - Daybreak
  - Glasswing
  - Fairwind
  - Gemini for Science
  - CodeMender
- **Silent orgs:** handled by the retrospective sweep below.

## Weekly retrospective sweep

These are the orgs whose newest entry in the DB is oldest:

**palisade_research (newest 05-07)**
- `/research` lists 15 reports.
- Both post-floor reports (self-replication and robot shutdown resistance) are in the DB.
- Everything else predates 2026-01-01.

**poolside (newest 07-13)**
- The blog has nothing newer than 07-28. The Laguna M.1/XS.2 technical report PDF is already a related URL on `poolside-laguna-m-1-model-card`.
- "Through the looking glass of benchmark hacking" (05-11): skipped. I read it in full; it is about benchmark and environment hygiene. It describes reward hacks found during a Laguna M.1 RL training run, but has no quantified eval of a released model.
- "Long context update" (05-26): skipped. It is a context-window update to existing models, with no new release and no safety content.

**thinking_machines (newest 07-31)**
- Nothing new on the blog or news index.
- The safety research grants, Tinker posts and the text-to-SQL post do not evaluate a named model.

**Result:** no new proposals.

## Citation mining

- **Today's add cites:**
  - the METR and Redwood red-teams of OpenAI's monitoring, both in the DB (`metr-gpt-5-5-independent-eval`, `redwood-research-gpt-5-5-independent-eval-2`)
  - OpenAI's misalignment reports, which are in the DB
- **Recent runs:** no other adds to mine.

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs returned 403 (streaks 30, 27, 17 and 11).
- **Agent-side check:** today read_doc.py and WebFetch both got 403 on path-to-astra and accelerating-cyber-defense-ecosystem.
- **Alive anyway:** path-to-astra is still indexed by search with its title. A 403 is a bot block, not a removal.
- **Result:** no status changes. This is the known split in PROPOSALS.md (2026-10-07).

## Document updates (task 6)

- **Top 5:** v773, v924, v1015, v573 and v578 were all judged noise in earlier runs and were not re-read.
- **v1033 (inclusion-ai-ling-2-6-1t-model-card):** the only version new since the last run. It is pure furniture: the HF "use this model" snippet plus download and Spaces counters.
- **Annotations:** none.

## Friction and proposals

Friction, three recurrences:
1. The alignment.openai.com index gap (recurrence of 2026-10-13T06:27:43Z).
2. The stale updated_docs top 5, plus a leak of the HF snippet into substantive_lines (recurrence of 2026-11-01T06:24:00Z).
3. The openai.com 403s on the agent side (recurrence of 2026-10-30T06:25:31Z).

**No new proposals.** Adding alignment.openai.com as an index URL is already filed in PROPOSALS.md.
