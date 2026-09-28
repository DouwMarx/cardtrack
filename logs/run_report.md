# cardtrack run report — 2026-09-28 (run_id `2026-09-28T06:16Z-local`)

## Headline

**4 proposals, all `annotate_version`, all `written`. No adds.** There are no new catalog-worthy documents in
the window since the last success (2026-09-27T11:31Z; the 72 h floor applied, so the window runs from 09-25).
Monday retrospective sweep of Palisade, poolside and Apollo found nothing missing.

| | |
| --- | --- |
| Proposals submitted | 4 (4 written) |
| Candidates triaged | 10 links first seen 09-28; older slices were triaged by earlier runs |
| `annotate_version` | 4 of 10 new diffs; 6 are noise (see §6) |
| Issues handled | 0 (`open_issues.json` is `[]`) |
| Blocked-URL escalations | 11: all alive (openai.com bot wall), no status change |
| Friction entries | 1 · `PROPOSALS.md` entries: 0 |

## 1. Phase A candidate triage (10 new links)

- **XiaomiMiMo/MiMo-V2.6-Pro-MOPD and MiMo-V2.6-Flash-MOPD:** skipped. Both repos call themselves "the
  MOPD upgrade of the MiMo-V2.6-{Pro,Flash}-RL checkpoint", which makes them checkpoint variants.
  MiMo-V2.6 Pro/Flash is already catalogued (`xiaomi-mimo-v2-6-pro-model-card`, with the technical
  report as a related URL), so they are not a `distinct_model_release`. Neither repo has safety evals.
- **hf.co/collections/XiaomiMiMo/mimo-v26:** a collection page for the same family. Skipped.
- **nvidia/preference-asr-bench:** a dataset. **nvidia/OpenH-RF discussions #70 and #74:** dataset PRs.
  Skipped.
- **Qwen-Image-2.1 Space discussion #2** (ZeroGPU migration) and **YanZhanPKU** (user profile):
  navigation or noise.

## 2. Targeted search (window 2026-09-25 → 2026-09-28)

- **Labs:**
  - OpenAI: GPT-6 Astra system card; Rosalind GA 09-11.
  - Google DeepMind: Gemini 3.8 Audio card 09-15; 3.8 Flash Cyber / Fairwind.
  - Anthropic: LSVP 09-17; Opus 5.5 card.
  - xAI: Grok 4.7 card.
  - All are already catalogued. Nothing new dated 09-25 or later was found.
- **Evaluators:**
  - SecureBio's GPT-6 Astra report is catalogued, with its PDF and blog copies as related URLs.
  - Apollo's Astra alignment evaluation is a section of OpenAI's system card, not a standalone Apollo
    document.
  - METR's Opus 5.5 report is catalogued.
  - The UK AISI blog has nothing since 08-27, and that post is methodology.
  - No Grok 4.7 third-party evaluation was found.
- **Restricted-access sweep** (LSVP, CVP, Glasswing/Mythos, Daybreak, Rosalind, Fairwind/Flash Cyber,
  CodeMender, Gemini for Science):
  - Nothing new. The CVP opening for Mythos-class models is still only "near future".
  - Daybreak expansion / GPT-5.6-Cyber (08-10) is catalogued.
- **Silent orgs (spot checks):**
  - Moonshot: Kimi K3 on Bedrock 09-18, a distribution event.
  - MiniMax: Agent product 09-27, a product with no model documentation.
  - Mistral: no new model.
  - NVIDIA:
    - Nemotron 3 Diarization (09-23) is an auxiliary speaker-diarization model, out of scope under the
      NVIDIA scope note.
    - NV-Reason-CT is a 5B radiology VLM. It sits outside the Nemotron/Cosmos/GR00T scope and was
      triaged 09-25.
  - The Supersonic Labs "Julia 1" card is not an allowlisted publisher.

## 3. Citation mining and the Monday retrospective sweep

No documents were added since 09-24 (count 350), and those were mined by earlier runs.

Today is Monday, so I ran the retrospective sweep on the three orgs whose newest entries are oldest:

- **Palisade Research** (newest 05-07): the blog has only podcasts and news since July. The 2026
  self-replication and shutdown-on-robots reports are already catalogued. Nothing missing.
- **poolside** (newest 07-13):
  - The Laguna XS/S 2.1 cards and the Laguna deep dive are catalogued.
  - "Through the Looking Glass of Benchmark Hacking" (05-11) is a general research essay about reward
    hacking seen in Laguna M.1 RL training. It reports no final evaluation results, so it is out of scope
    for `other`. Skipped.
- **Apollo Research** (newest 07-21):
  - The 2026 research posts are catalogued or are essays (science of scheming, third-party training-run
    evaluations).
  - Its model evaluations (GPT-5.3-Codex through GPT-6 Astra, Muse Spark) are published inside the
    labs' system cards, not as standalone Apollo documents.
  - Nothing missing.

## 4. Open issues

None.

## 5. Blocked-URL escalations (11)

All 11 are openai.com or help.openai.com and still return 403 to my fetcher. I re-checked Path to Astra
directly (403). Search still indexes Expanding Daybreak under its own title, and it is widely cited.
Consistent with yesterday's full check, every URL is **alive** behind the bot wall. No status change was
proposed.

## 6. Document update summaries

There were 10 new diffs; 4 were annotated, all `written`:

- `inclusion-ai-ling-3-0-flash-vl-model-card` v662: the context window was corrected from 1M to 256K
  tokens, and a Training content summary section was added. Verified on the live card.
- `inclusion-ai-ring-2-6-1t-model-card` v661: a Training content summary section was added.
- `inclusion-ai-ling-2-6-flash-model-card` v660: the same section was added.
- `inclusion-ai-ling-2-6-1t-model-card` v659: the same section was added.

Skipped as noise (download/Spaces counters and a reshuffled HF "Evaluation results" leaderboard
widget):

- `moonshot-ai-kimi-k2-6` v666
- `moonshot-ai-kimi-k2-5` v665
- `moonshot-ai-kimi-k3` v664
- `deepseek-deepseek-v4-pro` v663
- `stepfun-step-3-5-flash` v658
- `alibaba-qwen-qwen3-8-27b` v657

## 7. Friction and proposals

One entry was appended to `logs/friction.jsonl` (`tooling`). The heredoc form of `propose_doc.py --json -`
and `<` redirection from /tmp are both refused by the shell sandbox. This is a known issue already
documented in PROPOSALS.md, where the workaround is `--json /tmp/<file>`. I used the CLI-flag form
instead. There are no new `PROPOSALS.md` entries.
