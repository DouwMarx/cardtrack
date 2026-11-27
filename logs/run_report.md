# Run report — 2026-11-27T06:20Z-local

Last agent success: 2026-11-26T06:36Z. Search window: the 72 h minimum (since 2026-11-24). Today is a Friday, so there was no weekly retrospective sweep.

## Proposals and validator verdicts

None. No lead qualified today, so the validator gave no verdicts.

## Task 1: Phase A candidates (first_seen 2026-11-27)

- **tencent/Hy-Embodied-Apexio-1.0**: not proposed. The repo is live (HTTP 200) but shows "No model card", and the HY-Embodied GitHub README has no Apexio entry yet. Apexio is Tencent's flagship embodied agent, announced at WAIC 2026, so it is in scope under the tencent_hunyuan scope note once a card appears. I logged it in friction as a pending release. **Re-check this card on the next runs.**
- **inclusionAI/Ming-Image-0.2-Design** (and its Space): skipped. It is a 6B text-to-image design model under MIT, outside the inclusion_ai scope (Ling/LLaDA LLM lines and flagship agents). The card also has no safety evals.
- **inclusionAI Skill-Venus collection**: skipped. The collection is empty ("This collection has no items"). Watch for a UI-Venus-style agent release.
- Skipped as furniture or papers: HF user profiles, discussion threads (Qwen3.8-Flash-Next #87, Nemotron-3.5-Rerank-8B #4, LingSante-3.1-air-VL #1/#2, MiniMax oss-ecosystem-data #1), and the ProxyGenBench, SPARC and SOLVE paper pages.
- Older carried-over candidates were triaged in earlier runs and not revisited.

## Task 2: Targeted web search

Queries:
- "system card November 26 2026"
- November 2026 open-weight model-card releases
- November 2026 trusted-access programs
- Anthropic Enterprise Frontier Safeguards
- the nocode.mba and ThursdAI November release trackers
- the riorundown Nov 24 roundup
- METR, UK AISI and Apollo on Fable 5.2, GPT-6.2 and Gemini 4 Neon
- Anthropic LSVP, Cyber Verification Program and Claude Science
- Gemini Flash Cyber, CodeMender, Co-Scientist, Bioresilience, GPT-Rosalind and Daybreak
- xAI, Mistral, Meta and Moonshot releases
- DeepSeek, Qwen, MiniMax, MiMo and StepFun releases
- Palisade, Transluce, SecureBio, FAR.AI and CAISI eval reports
- Tencent Apexio

Results:

- **Nothing new and qualifying.** Releases for Nov 24-26 came from orgs that are not allowlisted, or shipped without documentation: Amazon Transcribe Turbo, JetBrains Mellum2.1, NIO WorldModel 3.0, Sakana Namazu Small, SenseTime SenseNova-RoboRSI and U1.6, Amini Soma-1X Lite, Sand AI MAGI-2, Cognition SWE-2.1, XPENG WorldGPT and AWS Strands Decider v2.
- **Kimi K3.1 Pro Prime** (Nov 20): skipped. It uses the same weights as K3.1 Pro on a faster serving lane, so it is not a distinct model release. K3.1 Pro itself is already catalogued.
- **Anthropic EFS on the Bedrock Trusted Access API**: the EFS post is already catalogued. The Bedrock API announcement is an AWS page, and AWS is not allowlisted.
- **NUWA loss-of-control evaluation of five open-weight models** (Nov 24-25): not allowlisted, and only seen through a secondary index.
- **Grok 4.8** is still unshipped. **Qwen4-Max** still has no card. Mistral and Meta had nothing new.
- **Silent orgs**: the shell refused the per-publisher group-by over the state summary (a recurrence of a 2026-09-30 friction entry). The vendor-level searches above covered the long-silent tier-2 labs instead.

## Task 3: Citation mining

The four docs added on 2026-11-26 (497-500) were mined in that run. Today added nothing, so there was nothing new to mine.

## Task 4: Open issues

`fetch_ok: true`, and the list is empty.

## Task 5: Blocked URLs

`blocked_escalations`, `phase_a_summary.blocked` and `not_found` are all empty. Yesterday's seven HF pages that hit 429 have cleared.

## Task 6: Document updates

The top 5 in order are v1304, v1056, v773, v1170 and v924. Earlier runs judged all five as noise, and nothing new was queued (the newest fetch is 2026-11-24).
- **v924** (Mythos Preview robotics post): I re-checked it, and the change is extraction only. Section headings now come through, the newsletter box was removed and the task-description table was dropped. The body text is unchanged.
- **v1309** (Apollo GLM-5.3 eval, further down the queue): the "more papers" widget was reshuffled, which is furniture.

No annotations.

## Task 7: Friction logged

- `recurrence` (of 2026-11-25T06:28:12Z): the updated_docs top 5 holds only already-judged versions.
- `recurrence` (of 2026-09-30T08:02:00Z): the silent-org group-by is blocked by the shell.
- `other`: the Hy-Embodied-Apexio-1.0 repo exists but has no model card yet (a pending in-scope release).

## Task 8: Proposals

None filed. The stale-queue problem is already covered by the open 2026-10-28 PROPOSALS entry, which asks for a way to dismiss a version.
