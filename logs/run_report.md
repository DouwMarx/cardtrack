# cardtrack agent run — 2026-10-25 (run id 2026-10-25T06:19Z-local)

- **Lookback:** last agent success 2026-10-24T06:22:09Z, so the 72 h minimum applied (2026-10-22 to 10-25).
- **Weekly retrospective sweep:** not run (Sunday).
- **Open issues:** `fetch_ok: true`, no open issues. Task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Action | Target | Verdict |
|---|---|---|---|
| 1 | add | Moonshot AI, "Kimi K3.1 Pro Tech Blog" (kimi.com/en/blog/kimi-k3-1-pro, 2026-10-23) | **written** → `moonshot-ai-kimi-k3-1-pro-model-card` (doc 408) |
| 2 | add | Tencent Hunyuan, Hy-Nomas model card (HF, repo created 2026-10-21) | **written** → `tencent-hunyuan-hy-nomas-model-card` (doc 409) |

- **#1 Kimi K3.1 Pro:** a post-trained Kimi K3, released with a Highspeed variant (both are in `model_names`). Found by web search; it wasn't in candidates (index gap: kimi.com/blog isn't an index URL).
  - **Cybersecurity section:** cyber data was removed from mid-training and RL. On xdev-bench-hard pass@3, the unmitigated checkpoint scores 90.5% and the released model 81.0%. ExploitBench and ExploitGym results are also reported, plus an open-weight principle of not extending the cyber frontier. Tagged `cyber`, `has_safety_evals: true`.
  - **Openness:** set to `closed`, because the model is API-only today. The blog says weights ship by Nov 4. **Watch item:** revisit openness and look for an HF card then.
  - **Co-publication check:** no HF or other copy exists yet.
- **#2 Hy-Nomas:** the Phase A watch item from the last run. It's an interactive video world model (world models are a covered class, and Tencent's scope note includes HY-World), Apache-2.0.
  - **Notability outside HF:** the official Tencent-Hunyuan GitHub repo, plus AlphaSignal and ShiftDelete coverage.
  - **Flags:** no safety evals, `open_weight_permissive`. The date is the HF createdAt, since the card itself isn't dated.

## Phase A candidates

- **Already triaged:** everything first seen before 10-25 was handled in earlier runs, apart from the Hy-Nomas watch item, which is now proposed (#2).
- **New today (3), all skipped:** an HF profile page (`shuver`), a README-update discussion on an NVIDIA robotics dataset, and a "Github repo/port" discussion on the NVIDIA RE-USE space.

## Targeted search (10-22 to 10-25)

- **Found:** Kimi K3.1 Pro (#1).
- **Already in DB:** Qwen3.6-27B (10-21), MiniMax M3.1 Flash, DeepSeek V4.1 Flash 1017, Muse Spark Open card and eval methodology, Muse Spark 1.1 eval report, METR 10-22 OpenAI monitoring red-team, Anthropic CVP / LSVP / Mythos pages, GPT-6 October update, GPT-6.1 Sol addendum.
- **Watch:**
  - The Muse Wonder full safety report is still unpublished.
  - Kimi K3.1 Pro weights are due by Nov 4.
- **Unread lead, not proposed:** OpenAI "Patch the Planet: global response coordination as agents uncover critical vulnerabilities" (openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/, about 10-21/22). It's a Daybreak-initiative post naming GPT-5.6 Sol.
  - Both read_doc.py and WebFetch got 403, so I couldn't read it.
  - It may only be a partnership/disclosure post, which would be out of scope. Retry next run.
  - The June Patch the Planet launch post (openai.com/index/patch-the-planet/) isn't in the DB either. It reportedly launched alongside GPT-5.5-Cyber, so check it against `openai-gpt-5-5-access-policy` when openai.com is readable.
- **Restricted-access programs:** nothing new beyond the CVP (October tiers update), LSVP, Fairwind, Daybreak and Rosalind, all already in DB.
- **Silent-org (>14 days) check (done this run, via jq group_by over state_summary):**
  - **Silent orgs:** palisade (05-07), poolside (07-13), thinking_machines (07-31), saferai, rand, dots_studio, zai (08-28), transluce, far_ai, us_caisi (09-17), cursor, xai (09-21), alibaba_qwen, xiaomi, upstage, mistral. Moonshot and Tencent were also silent before today's adds.
  - **Searched:** xAI, poolside, Thinking Machines and CAISI. Their latest releases (Grok 4.7, Laguna S 2.1, Inkling, CAISI GLM-5.3) are all already in DB. Nothing new found.

## Citation mining

- **Kimi K3.1 Pro blog (#1):** it cites:
  - In DB: the Opus 5.5 system card, the Fable 5.1 / Mythos 5.1 system card, GPT-6 Astra, DeepSeek V4.1-Flash-1017 and its news261017 page.
  - **Not in DB:** z.ai/blog/glm-5.3, the source for GLM-5.3's ExploitBench/ExploitGym scores. It isn't in the `zai-glm-5-3-model-card` related_urls. It's a client-rendered shell: read_doc.py extraction failed (598-byte HTML) and WebFetch saw an empty page. Not proposed because it was unread. **Lead for a later run:** it may be the GLM-5.3 release blog, which would be a `related_urls` announcement on the existing row.
- **Hy-Nomas (#2):** cites only its own GitHub repo and bench dataset, both recorded as related URLs.

## Blocked-URL escalations (task 5)

- **Status:** all 16 openai.com / help.openai.com rows are blocked (streak 24 for most; 19 for accelerating-cyber-defense-ecosystem, 9 for the Rosalind Academic Plan, 3 for low-resource-programming-languages).
- **Spot checks:** unlike recent runs, read_doc.py got HTTP 403 today on path-to-astra and strengthening-societal-resilience-with-rosalind-biodefense, and on the new Patch the Planet lead.
- **Conclusion:** search results still list these pages (e.g. introducing-gpt-rosalind came up in today's search), and 403 is bot-blocking, not removal. No evidence any of them is gone. All treated as alive, no status changes.

## Document updates (task 6)

None of the 20 queued versions was fetched since the last run. I re-checked two, and both were noise, so no annotations:
- **Mythos preview other-3 v924:** the newsletter teaser was dropped and section headings ("Summary of findings", "Simple settings") surfaced in extraction. The body text is unchanged.
- **Epoch GPT-5.6 Terra v870:** appendix headings changed from "Appendix A." to "Appendix A:", plus a new "Appendices" heading.

The other three of the top 5 (DeepSeek V4.1 Flash v773, V4 Pro v573, V4 Flash 0731 v578) were judged HF widget/snippet noise in earlier runs.

## Friction and proposals

- **Friction, one entry:** a `recurrence` of 2026-10-23T06:26:11Z. The openai.com 403 now defeats read_doc.py as well, which left the Patch the Planet lead untriaged.
- **No new proposals.**
