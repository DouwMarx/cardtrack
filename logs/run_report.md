# Run report — 2026-11-22T06:19Z-local

Last agent success: 2026-11-21T06:26Z. Search window: the 72 h minimum (since 2026-11-19). Today is a Sunday, so no weekly retrospective sweep.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | annotate_version | `anthropic-claude-opus-access-policy` v1274 (CVP support article): Team plans limited to Defense Access; Red Team/Specialized now Enterprise and API only; constrained products now accepting Defense Access applications (data retention required); unconstrained products "Not yet available" | **written** (doc 304) |
| 2 | annotate_version | `inclusion-ai-llada2-2-flash-model-card` v980: the "SGLang deployment coming soon" placeholder was replaced by a full SGLang deployment section with JointThresholdInDel decoding defaults | **written** (doc 247) |

No add proposals today.

## Task 1: Phase A candidates (first_seen 2026-11-22)

- There was one new candidate: the nvidia/AeroZoo dataset "Update README.md" discussion. It's a dataset discussion thread, so I skipped it.
- Older candidates were triaged by earlier runs.

## Task 2: Targeted web search

Queries:
- "system card new AI model November 2026"
- open-weight model cards around Nov 20
- trusted-access programs Nov 2026
- UK AISI pre-deployment evaluation reports
- Apollo/Palisade/METR/Epoch evals of GPT-6.2 and Gemini 4 Neon
- Anthropic LSVP/CVP Mythos
- GPT-Rosalind / Daybreak / Gemini for Science / Claude Science access
- DeepSeek/Qwen/Mistral/xAI releases Nov 19–21
- Grok/Mistral/Nova model cards
- Hy4 system card

I also checked the nocode.mba and llmgateway release trackers for Nov 17–22.

- **Already cataloged**: GPT-6.2 Astra/Sol, Gemini 4 Neon/Hydrogen, Inkling 2 Mini, Kimi K3.1 Pro (plus the FAR.AI and SecureBio evals), Mistral Large 4, Grok 4.6/4.7, Muse Ember, and the Anthropic Mythos, LSVP and CVP pages.
- **Kimi K3.1 Pro Prime** (Nov 20): skipped. It is an Alibaba Model Studio hosting tier of the already-cataloged K3.1 Pro, not a distinct release.
- **Microsoft MAI Code 2 / MAI Cyber 2 Flash / MAI Realtime 1** (Nov 17): skipped. Microsoft is not in sources.yaml or the generated overlay.
- **Others skipped**: SenseNova-Loop-9B, Baseten bison-1/groundhog-1, Metric AI Ayb and Reson8 Rumble are non-allowlisted publishers. AssemblyAI STT is an ASR product, not catalog material.
- **Restricted access**: nothing new. The Reflection AI "Laser" program is still out of scope (publisher not allowlisted, and Laser is a tool rather than a named model). The OpenAI academic-researcher expansion was already skipped on 11-21.
- **Hy4 System Card** (Tencent, released 2026-11-20, 82 pp. per press): **still unreadable, not proposed**.
  - hy.tencent.ai/Hy4_system_card.pdf still returns the SPA shell.
  - The SPA bundle builds the PDF path at runtime (it has only `systemCardsTitle`/`systemCardsDesc` keys and a bare ".pdf" string), so I did not guess a CDN URL.
  - The HF tencent/Hy4 file list and the GitHub Tencent-Hunyuan/Hy4 tree still have no PDF.
  - KuCoin and OrcaRouter coverage give no direct link.
- **Silent-org check (>14 days)**: limited. I couldn't run a helper script over the state summary (the Bash guard asked for approval), so I only spot-checked xAI, Mistral, Meta, Moonshot and Google DeepMind with Grep. All have entries from late Oct or Nov.

## Task 3: Citation mining

There were no new adds this run. Yesterday's two adds (Inkling 2 Mini, METR Q4 2026 update) were mined on 11-21 and yielded nothing proposable. Nothing new today.

## Task 4: Open issues

`fetch_ok: true`, and there are no open issues.

## Task 5: Blocked-URL escalations

- `tencent-hunyuan-hy4-flash-model-card` (https://huggingface.co/tencent/Hy4-flash, 429, streak 4): read_doc got HTTP 200 (321 KB, 17.7k chars of card content). **Alive**, so no status change. Phase A has now been rate-limited on this URL for 4 runs, which I logged as friction.

## Task 6: Document updates

1. `anthropic-claude-opus-access-policy` v1274 (fetched today): **substantive, annotated** (see table).
2. `inclusion-ai-llada2-2-flash-model-card` v980: **substantive (section added), annotated**.
3. `epoch-ai-gpt-5-6-terra-independent-eval` v870: **skipped, noise**. Appendix headings went from "Appendix A." to "Appendix A:", plus an "Appendices" header. No numbers changed.
4. `anthropic-claude-mythos-preview-other-2` v922: **skipped, noise**. Section headings were newly extracted, and the newsletter banner, footnotes and related-post teasers dropped out of extraction. The prose is unchanged.
5. `inclusion-ai-ring-2-6-1t-model-card` v979: **skipped, noise**. HF usage-snippet expansion, download/Spaces counters and eval-widget reordering (same scores).

The stale top entries (v1056, v773, v1170, v924, v1015) were judged noise by earlier runs and are unchanged, so I didn't re-read them.

## Task 7: Friction logged

- `other`: Phase A gets a persistent HF 429 on tencent/Hy4-flash (4 runs) while the agent-side fetch gets 200.
- `recurrence` (of 2026-11-21T06:25:35Z): the Hy4 System Card PDF is still unreadable (SPA shell), and there is no alternate copy.
- `recurrence` (of 2026-11-21T06:25:33Z): already-judged stale entries still lead the updated_docs queue.

## Task 8: Proposals

None filed.
- The Hy4 unreadable-PDF case is covered by the existing PROPOSALS.md entry suggesting a headless-render fallback and `logs/unretrievable.jsonl`.
- The stale-queue problem is covered by the 2026-10-28 proposal.
