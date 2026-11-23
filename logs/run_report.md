# Run report — 2026-11-23T06:18Z-local

Last agent success: 2026-11-22T06:26Z. Search window: the 72 h minimum (since 2026-11-20). Today is a Monday, so I also ran the weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | `inclusion-ai-lingsante-3-1-flash-model-card`: https://huggingface.co/inclusionAI/LingSante-3.1-flash (560B/25B-active medical MoE on Ling-3.1-flash, MIT, has_safety_evals false) | **written** (doc 491, v1301) |
| 2 | add | `inclusion-ai-lingsante-3-1-air-vl-model-card`: https://huggingface.co/inclusionAI/LingSante-3.1-air-VL (124B/5.5B-active medical VLM on Ling-3.0-flash-VL, MIT, has_safety_evals false) | **written** (doc 492, v1302) |
| 3 | field_update | `saferai-glm-5-2-independent-eval` related_urls += SaferAI landing page | **rejected**: the URL is already one of the row's own URLs. The verdict is correct, so I did not retry. |

Notability for #1 and #2:
- Ant Ling announced both on X on 2026-11-22 (x.com/AntLingAGI/status/2124523916819648945).
- Fathom/dev.to, CellCog and OrcaRouter covered the release.
- The precedent is Ling-3.0-flash-Sante, which is already its own row.

## Task 1: Phase A candidates (first_seen 2026-11-23)

- **LingSante-3.1-flash and LingSante-3.1-air-VL**: proposed (see above).
- **LingSante-3.1-flash-MXFP4**: skipped. It is a quantization of #1, and I recorded it as a related `weights` URL on #1.
- **LingSante MedGuard** (collection plus HF paper 2611.25509): skipped. It is a medical guardrail classifier at 4B/9B/27B, and the inclusion_ai scope excludes guardrail classifiers.
- **LingSante-Pulse-1.0** (first seen 11-21, re-checked today because of the new announcement): skipped. It is a physiological-signal encoder, which is auxiliary.
- **tencent/WePocketModel1.0-2B/4B (+GGUF)**: skipped. It is a WeChat AI on-device VLM, embedding and decision model, outside the Hunyuan line that the tencent_hunyuan scope covers.
- **www.minimax.io/blog/minimax-m3**: already cataloged as a related URL of `minimax-minimax-m3-model-card`.
- **Other MiniMax links** (x.com, LinkedIn, Discord, docs, status, careers), the HF org page, and HF user profiles (KivingY, cafe3310): site furniture, skipped.

## Task 2: Targeted web search

Queries:
- system cards Nov 22
- model releases Nov 21–23
- trusted/restricted access programs
- Hy4 system card PDF (two queries)
- Qwen4-Max model card
- GLM-5.3-Flash
- xAI Grok model card Nov 2026
- Xiaomi MiMo Nov 2026
- AISI/METR/Apollo pre-deployment reports
- LSVP / Claude Science / GPT-Rosalind / Daybreak
- independent evals of Kimi K3.1 Pro / Hy4 / Qwen4-Max / GPT-6.2

Results:
- **Already cataloged**: Fable/Mythos 5.2, the Fairwind program, GPT-6 Cyber, GPT-6.2 (including the UK AISI results in its system card), Gemini 4 Neon, GLM-5.3-Flash, MiniMax M3 and the LSVP page.
- **Qwen4-Max** (Nov 16): skipped. It is API-only, and press says Alibaba has published no model card.
- **Grok 4.8 / Grok 5**: not released and no card exists. MiMo has had no release since V2.6 (Sep 22, already in the DB).
- **Anthropic "Open call for guest investigators in the life sciences"** (2026-10-22): skipped. It is a research-collaboration call with no named model or access gate.
- **Artificial Analysis scores** for Qwen4-Max, Kimi K3.1 Pro and Hy4: skipped. Artificial Analysis is not on the allowlist.
- **Hy4 System Card**: still unreadable, so not proposed. hy.tencent.ai/Hy4_system_card.pdf (also the HN submission target) still returns the 6314-byte SPA shell, and the HF tencent/Hy4 file list has only READMEs.
- **Silent-org check (>14 days)**: a jq query on newest publication_date per publisher flagged zai, xai, alibaba_qwen, xiaomi, upstage, us_caisi and cursor as silent. Searches found no new documentation for xai, qwen, xiaomi or zai. Upstage, US CAISI and Cursor got no dedicated search today.

## Task 3: Citation mining and Monday retrospective sweep

- **Citation mining**: the LingSante cards reference only Ling-3.1-flash, Ling-3.0-flash-Sante and Ling-3.0-flash-VL, which are all in the DB.
- **Retrospective sweep**: I picked the three orgs whose newest entry is oldest: palisade_research (2026-05-07), poolside (2026-07-13) and saferai (2026-08-02). A subagent searched them without a recency filter. Nothing new qualifies:
  - Palisade's 2026 non-DB items are podcasts, media pieces and the frominside.ai interviews. The shutdown-resistance arXiv paper is from Sept 2025, before the scope floor.
  - Poolside's 2026 non-DB items are the Laguna long-context update (an update to models already covered), the launch post, an essay and a platform announcement.
  - SaferAI's 2026 non-DB items are methodology/policy papers and the company-level ratings tracker.
- **Follow-up (not proposed)**: the Palisade self-replication PDF (https://palisaderesearch.org/assets/reports/self-replication.pdf, verified 200, same title) could be added to `palisade-research-gpt-5-4-independent-eval` as `full_document`. I did not propose it, because a related_urls field_update replaces the whole list and the state summary doesn't show the kinds of the existing companions. That row is also in status `moved`. A future run with the kinds visible can propose it.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked-URL escalations

- `tencent-hunyuan-hy4-flash-model-card` (429, streak 5): read_doc returned HTTP 200 with 17.7k chars of card content. **Alive.**
- Fresh 429s at streak 1: `tencent-hunyuan-hy4-model-card`, `baidu-ernie-5-5-flash-base-model-card` and `baidu-ernie-image-model-card`. All return HTTP 200 to read_doc. **Alive.**
- I proposed no status changes.

## Task 6: Document updates

The already-judged stale top entries (v1056, v773, v1170, v924, v1015, plus v870, v922 and v979 from 11-22) are unchanged, so I didn't re-read them. I read the next five, and all were noise:
- `dots-studio-dots3-note-preview-model-card` v1238: HF usage snippet expanded, and the eval widget reordered with the same scores.
- `metr-gpt-5-independent-eval` v1139: footnotes now rendered under a "Footnotes" header with a different back-arrow glyph. The text is identical.
- `anthropic-claude-mythos-preview-other-7` v933: section headings newly extracted, and the newsletter banner and related-post teasers dropped. One Claude-authored callout paragraph also disappeared from extraction while the surrounding prose still refers to it, which looks like an embedded block that is no longer extracted rather than an edit.
- `nvidia-nemotron-3-5-super-vl-other` v1016: the PDF date line changed from 2026-10-21 to 2026-10-27, one contributor was added to the author list, and the list reflowed. There are no content or score changes.
- `deepseek-deepseek-v4-pro-model-card` v573: HF code-snippet churn, a download counter and eval-widget reordering.

## Task 7: Friction logged

- `recurrence` (of 2026-11-20T06:24:20Z): the Hy4 System Card PDF is still an SPA shell.
- `recurrence` (of 2026-11-22T06:25:40Z): the Phase A HF 429s persist and have spread to Hy4 and two ERNIE pages, while all four return 200 to the agent.
- `recurrence` (of 2026-11-18T06:28:28Z): already-judged stale entries still lead the updated_docs queue.

## Task 8: Proposals

None filed. The open problems are covered by existing PROPOSALS.md entries: the Hy4 unreadable PDF (the headless-render fallback proposal) and the stale queue (the 2026-10-28 proposal). A note for operators, not friction: the state summary's `related_urls` is a bare URL list without kinds, which makes safe related_urls field_updates on rows with existing companions impractical. If this blocks more additions it is worth a proposal.
