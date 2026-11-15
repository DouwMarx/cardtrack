# cardtrack agent run — 2026-11-15 (run id 2026-11-15T06:18Z-local)

- **Lookback:** last agent success 2026-11-14T06:25:43Z, so the 72 h minimum applied (2026-11-12 to 11-15).
- **Weekly retrospective sweep:** not run (Sunday).
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | annotate_version `anthropic-claude-opus-access-policy` v1188 (CVP support article). The page was rewritten: it names Claude Mythos 5.2 alongside Mythos 5.1, Opus 5.5 and Sonnet 5.5; adds a tier table with seat caps (Red Team up to 75, Specialized up to 25) and the prohibited activities; says Specialized Access is reviewed with the US government; and from 2026-12-15 Defense Access requires phishing-resistant MFA and no long-lived API keys. Checked against the live page with read_doc (HTTP 200). | **written** |
| 2 | field_update `model_names` on `anthropic-claude-opus-access-policy`, adding "Claude Mythos 5.2", which the live page now lists in every tier. | **written** |

No adds today.

**Operator note:** this row has status `moved`. The canonical (`/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet`) now redirects to `/14604842-cyber-verification-program`. Canonical changes are operator-only, so I proposed nothing for it.

## Phase A candidates (new today, first_seen 11-15)

All 4 new candidates were skipped:
- Tencent Qwen3.8-27B-DSpine-b16 discussion #6 (a config fix on a draft model);
- the xingyoujunnv profile page;
- the NVIDIA PhysicalAI-Robotics-NuRec dataset discussion;
- the NVIDIA AeroZoo dataset.

None of them is model documentation. Older candidates were triaged in earlier runs.

## Targeted search (11-12 to 11-15)

Nothing new to propose:
- **Already in the DB:** GPT-6 Cyber, ChatGPT Images 2.6, Gemini 4 Carbon and Hydrogen, Fable/Mythos 5.2, Kimi K3.1 Pro (lab card plus FAR and SecureBio evals), Muse Ember, Inkling 2 Small, and the METR 11-05 AI R&D acceleration assessment.
- **Gemini 4 Hydrogen Safety & Security Report:** still "coming soon" on the live model card (read today). Keep watching.
- **Grok 4.8:** still no model card or API (coverage dated 11-13).
- **Qwen4-Max-Preview** (preview 11-11 to 11-25): no model card, benchmarks or weights.
- **Tencent Hy4:** `huggingface.co/tencent/Hy4` still returns 401; weights and system card are still "in the coming days".
- **Muse Spark 1.4:** only leaks (a GitHub PR from 11-13); Meta has not announced it.
- **MiniMax H3 Image (11-10):** skipped. It is an image model, and the sources.yaml MiniMax scope excludes image models.
- **Trusted-access programs:** the CVP three-tier coverage and Mend.io's CVP/Daybreak enrollment add nothing new beyond the catalogued program pages (the CVP page revision is handled as #1/#2).
- **Watch next:** Hydrogen S&S report, Grok 4.8, Qwen 4, Hy4 weights and card, Muse Spark 1.4.

## Citation mining

- **Gemini 4 Hydrogen model card (newest add):** it cites the Argon and Carbon S&S reports (both catalogued) and the still-unpublished Hydrogen S&S report. Nothing new to propose.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on 20 openai.com / help.openai.com URLs (16 at streak 30, 1 at 24, 3 at streak 3).
- **My own fetches:** read_doc fetched 5 of them with HTTP 200 via browser_impersonation today: daybreak-red-aws-govcloud, a-thousand-fewer-paths-to-root, securing-our-frontier-model-training-environment, measuring-how-ai-agents-handle-wet-lab-science, and the Daybreak help-center overview. That covers all 3 streak-3 URLs plus one from the streak-30 group.
- **Verdict:** alive and bot-blocked; no status changes.

## Document updates (task 6)

Top 5 in order:
- **v1056** (FangCun eval): judged noise or handled in earlier runs. Skipped.
- **v1188** (CVP page): substantive. Annotated (#1).
- **v773** (DeepSeek-V4.1-Flash HF card): judged noise or handled in earlier runs. Skipped.
- **v1170** (DeepSeek-V4.1-Flash-1017 HF card): yesterday's run judged it pure HF furniture. Skipped.
- **v924** (Mythos Preview other-3): judged noise or handled in earlier runs. Skipped.

## Friction and proposals

Friction (2 recurrence entries):
1. The OpenAI Phase A 403s again, with read_doc working.
2. The stale updated_docs head (v1056).

No new PROPOSALS.md entry.
