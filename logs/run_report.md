# cardtrack agent run — 2026-11-08 (run id 2026-11-08T06:19Z-local)

- **Lookback:** the last agent success was 2026-11-07T06:25:10Z, so the 72 h minimum applied (2026-11-05 to 11-08).
- **Weekly retrospective sweep:** not run. Today is Sunday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

None. Every in-scope document I found is already catalogued.

## Phase A candidates (10 first seen today)

Candidates first seen before today were triaged in earlier runs. All of today's were skipped:
- **tencent/Qwen3.8-27B-DSpine-b16:** read. It is a 5-layer speculative-decoding draft model for Qwen3.8-27B, with only speedup and acceptance tables. Auxiliary model, out of scope.
- **Qwen3.8 discussions:** 2.4T-A95B, 2.4T-A95B-FP8 and Flash-Next-FP8 each got a "response template" discussion. Repo housekeeping.
- **NVIDIA:**
  - GR00T-N1.7 SimplerEnv / DROID license discussions: housekeeping.
  - video-to-data-GR00T-N1.7 tissue-box fine-tune: a task fine-tune. GR00T N1.7 is already in the DB.
- **The rest:** HF profile pages.

## Targeted search (11-05 to 11-08)

Searched for:
- generic system/model cards;
- Anthropic, Google DeepMind, OpenAI, xAI, Meta and Mistral;
- the Chinese labs (DeepSeek, Qwen, GLM, MiniMax, Kimi, MiMo) and Tencent Hy4;
- UK AISI, CAISI, METR, Apollo, Epoch, Transluce, FAR.AI and Palisade evals;
- trusted-access programs (LSVP / Cyber Verification Program / Claude Science, Mythos, Daybreak / TAC, Rosalind Biodefense / GPT-Rosalind-6, Gemini for Science).

Findings:
- **Already catalogued:** GPT-6 Cyber, ChatGPT Images 2.6, GPT-Rosalind-6 addendum, GPT-6.1 Sol/Terra, Gemini Omni 1.2 Flash, the METR Anthropic AI R&D assessment and its Risk Report review, Muse Spark Open / Muse Wonder, Mistral Large 4, Kimi K3.1 Pro (card and SecureBio eval), and LSVP / Mythos 5.1 access.
- **Tencent Hy4:** still API-only. The HF API's newest tencent repo is the DSpine draft model; the weights and system card are still "in the coming days". **Watch for it.**
- **Qwen4:** announced at Apsara on 10-29, but there is no HF repo or card yet (the newest Qwen repo is Qwen-Image-2.1-Turbo from 10-09). **Watch for it.**
- **"DeepSeek V4.1 Flash Cyber":** not a DeepSeek release. The name is a third-party label for refusal-removed or hosted variants of V4.1-Flash-1017, and the DeepSeek HF org has nothing newer than V4.1-Flash-1017 (in DB). Skipped.
- **GPT-Rosalind-6 "dual-track" access (secondary coverage dated 10-31 / 11-01):** traces to the addendum, which is in DB. The GPT-Rosalind help article is already a related URL on existing Rosalind rows, and I found no separate dated access post. Nothing proposed.
- **Grok 5:** not released. GLM-5.3 FlashX Legal is an API variant with no card found.

**Silent-org check (>14 days, via jq):**
- Silent: palisade, poolside, saferai, rand, dots, zai, transluce, far_ai, us_caisi, cursor, xai, qwen, xiaomi, upstage.
- Searched zai, qwen, xiaomi, us_caisi, xai and the evaluators. Nothing new and in scope was found.

## Citation mining

- **Recent adds:** the 11-05 and 11-06 adds were mined in the 11-06 run. Today I re-mined the METR AI R&D acceleration assessment (raw HTML links). It cites:
  - the Opus 5.5 and Haiku 5.5 system cards (in DB; Haiku via the CDN copy that is already a related URL);
  - METR's Risk Report review (in DB);
  - RSP v3.4 (a policy document, not model documentation);
  - METR's "~100-page Full Report", which is not linked publicly.
- **The two assets.claude.com "system card" PDFs from 11-06:** read their headers. They are the Opus 4.8 and Opus 4.7 system cards, both already in DB at their stable anthropic.com URLs (hashed CDN copies). No action.

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs were 403 again (streaks 17-30).
- **My own fetches:** read_doc got HTTP 200 via browser_impersonation on all four I tried:
  - scaling-trusted-access-for-cyber-defense
  - path-to-astra
  - expanding-daybreak-as-the-cyber-defense-window-narrows
  - accelerating-cyber-defense-ecosystem
- **Alive check:** the pages are alive, so there are no status changes.

## Document updates (task 6)

No new entry in updated_docs since yesterday. Today's 7 new versions were all filtered as furniture by the monitor. The top 5 (v1056, v773, v924, v1015, v573) were judged noise or annotated in earlier runs. Nothing annotated.

## Friction and proposals

Friction, two recurrence entries:
1. Phase A gets 403 on openai.com while read_doc succeeds.
2. The stale updated_docs ranking.

No new proposal.

**Workaround note:** ad-hoc `.venv/bin/python /tmp/x.py` needs approval, but `jq` over state_summary.json works for the silent-org check.
