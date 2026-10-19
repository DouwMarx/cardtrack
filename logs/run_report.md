# cardtrack agent run — 2026-10-19 (run id 2026-10-19T06:16Z-local)

- **Lookback:** last agent success was 2026-10-18T06:22:50Z, so the search used the 72 h minimum (2026-10-16 to 10-19).
- **Weekly retrospective sweep:** run (Monday). Orgs: Moonshot AI, Thinking Machines, SaferAI. Palisade and poolside have older newest entries but were swept on 10-05 and 10-12 (Apollo on 10-12), so I rotated to the next three.
- **Open issues:** `fetch_ok: true`, no open issues. Task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | add (other) | Kimi K3 technical report, 2026-07-27, https://raw.githubusercontent.com/MoonshotAI/Kimi-K3/main/k3_tech_report.pdf (open_weight_restrictive; has_safety_evals true; cyber) | **written** (`moonshot-ai-kimi-k3-other`, doc 396, v877) |
| 2 | add (other) | Kimi K2.5 technical report, 2026-01-30, https://raw.githubusercontent.com/MoonshotAI/Kimi-K2.5/master/tech_report.pdf (open_weight_permissive; has_safety_evals false) | **written** (`moonshot-ai-kimi-k2-5-other`, doc 397, v878) |

### #1 Kimi K3 technical report

- **What it is:** a 47-page PDF in the official GitHub repo, linked as "Full Report" from the README. It is a separate document from the catalogued HF card.
- **Date:** the first commit is 2026-07-27, the same day as the weights. The PDF was revised 07-28 and 08-06.
- **Safety content:** section 6.2.2, Cyber Security Evaluation, covers two tiers:
  - vulnerability discovery: 16 previously unknown vulnerabilities confirmed;
  - a 36-task exploit-development suite: 14/36 solved vs 8/36 for GLM-5.2, with the kernel track mostly unsolved.

  The HF card has no comparable section.
- **Citations:** the report cites the joint UK AISI/CAISI Kimi K3 assessment, which is already catalogued (both copies, plus SecureBio's).
- **Openness:** the Kimi K3 License requires a separate agreement for Model-as-a-Service operators above USD 20M revenue, so open_weight_restrictive.

### #2 Kimi K2.5 technical report

- **What it is:** the same pattern: a "Full Report" PDF in the official repo, first committed 2026-01-30.
- **Safety content:** none. CyberGym is only one row in the coding benchmark table, so has_safety_evals is false and no domains are tagged.
- **Openness:** the "Modified MIT" license adds only a display-attribution clause, so open_weight_permissive. I couldn't read the existing K2.5 card row's openness to cross-check it, so an operator may want to confirm the two are consistent.
- **Not proposed:** the K2.6 repo 404s, and the K2.7-Code card links no report. The arXiv "An Independent Safety Evaluation of Kimi K2.5" (2604.03121) is by authors outside the allowlist.

## Phase A candidates

- **Already triaged:** everything first seen 10-06 to 10-18 was triaged in earlier runs.
- **New today:**
  - Anthropic "Investing in the public benefit" (public-benefit-fund): skipped. It is corporate governance and equity, with no model.
  - FAR.AI "Telling FIBS" (/fibs): skipped. It is a deception-probe and monitoring method plus a dataset; Qwen3.5-397B and Opus 5.5 appear only as subjects or baselines, so it fails the system-card test.
  - 11 NVIDIA `cosmos3-nano-libero10-sdg-export-*` repos: skipped. They are experiment checkpoints with no announcement, i.e. checkpoint drops.

## Targeted search (10-16 to 10-19)

- **Already in the DB:** GPT-Live-1.1 system card; DeepSeek V4.1-Flash-1017; Gemini 4 Argon card and safety report; Haiku 5.5; the GPT-6 Sol/Luna October update; the Rosalind Academic Plan.
- **Nothing new found:**
  - Access programs: Glasswing/CVP (merger already catalogued), LSVP, Claude Mythos, Claude Science, Daybreak, Rosalind Biodefense, Gemini Flash Cyber/CodeMender, Gemini for Science.
  - xAI: no Grok 5 card.
  - Astra Minor: still leak coverage only.
  - Chinese open-weight labs.
  - UK AISI and METR. METR's 10-14 posts are policy and methods pieces, triaged earlier.
- **Watch:** a TestingCatalog report says Claude Fable 5.5 has reached partners ahead of an imminent release. There is no first-party document yet. `gpt-rosalind-discovery` is still only on the pricing page.

## Retrospective sweep

- **Moonshot AI:** the HF cards for K2.5, K2.6, K2.7-Code and K3 were all catalogued, but the two GitHub technical reports were not. Both are now proposed (#1, #2).
- **Thinking Machines:** the news index lists nothing in scope since Inkling-Small. The newer posts are Tinker anniversary, text-to-SQL RL and safety research grants; all four Inkling/TML rows are present.
- **SaferAI:** the GLM-5.2 evaluation and the DeepMind safety-case review are both present. Nothing newer is model-specific. The research index is client-rendered (256 chars via read_doc), so I checked by site search.

## Citation mining

- **K3 report:** its safety citations (AISI/CAISI, SecureBio) are already in the DB. Artificial Analysis, Vals and Arena are not allowlisted.
- **K2.5 report:** no safety citations.
- **Yesterday's DeepSeek add:** already mined.

## Blocked-URL escalations (task 5)

- **Streaks:** 15 openai.com/help.openai.com rows, at streak 18 (13 for accelerating-cyber-defense-ecosystem, 3 for the Rosalind Academic Plan).
- **Spot checks:** read_doc.py fetched introducing-the-rosalind-academic-plan, accelerating-cyber-defense-ecosystem and hugging-face-model-evaluation-security-incident with HTTP 200 via browser_impersonation.
- **Status:** all alive. No status changes proposed.

## Document updates (task 6)

- **Nothing to annotate:** no new versions since the last run. All 20 queued entries were fetched on or before 2026-10-18T06:17Z and judged in earlier runs: the 10-18 Epoch and inclusionAI diffs were judged noise yesterday, and the rest even earlier.

## Friction and proposals

- **Friction, two entries:**
  - a `recurrence` of the openai.com 403 false-alarm (2026-10-06T06:29:51Z);
  - an `ambiguous_criteria` entry: no written rule says whether a lab technical report next to a catalogued HF card is its own row or a related_url. The corpus does both (NVIDIA rows vs DeepSeek related_url); today I followed the NVIDIA and document-unit precedent.
- **No new proposals.**
