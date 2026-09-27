# cardtrack run report — 2026-09-27 (run_id `2026-09-27T11:24Z-local`)

## Headline

**0 proposals; nothing warranted a write.** It was a quiet window. Two leads are new: an OpenAI
TAC-expansion post that the agent cannot read (403), and a suspicious third-party re-host of StepFun's
Step 5 Preview. Both are logged as friction and neither was proposed.

| | |
| --- | --- |
| Proposals submitted | 0 |
| Candidates triaged | 8 links first seen since the last success (09-26T06:24Z); older slices were triaged by earlier runs |
| `annotate_version` | 0 of 4 new diffs; all 4 are noise (see §6) |
| Issues handled | 0 (`open_issues.json` is `[]`) |
| Blocked-URL escalations | 11: all alive (openai.com bot wall), no status change |
| Friction entries | 2 · `PROPOSALS.md` entries: 0 |

## 1. Phase A candidate triage

There were 8 new links. None was proposed:

- **Qwen3Guard-Stream-0.6B/4B/8B, the 3 repos plus 3 "Fix KV cache reuse" discussions.** These are
  content-safety classifiers, which are auxiliary models excluded by `covered_model_class`. The repos
  were updated, not newly created; the Qwen3Guard line dates from 2025, before the scope floor.
- **Palisade Threads and Facebook links:** navigation.

## 2. Targeted search (window 2026-09-24 → 2026-09-27; 72 h floor governs)

- **Release trackers** (llm-stats, llmgateway): nothing after the 09-22 cluster, which is already
  handled. LLM Gateway "Smart Route" (09-25) is a router, not an allowlisted publisher.
- **METR:** its newest post is the Opus 5.5 predeployment summary (09-22), already catalogued.
- **Anthropic, "Claude discovers a novel enzyme system with CRISPR-like repeats" (~09-24):** a science
  capability showcase with no eval or safety content. Skipped, matching the earlier Nine Loops skip. It
  surfaced via the related-content box on the Mythos access page. The Accenture embedded-evaluation
  partnership post seen there is also skipped, as a partnership announcement.
- **Restricted-access sweep** (LSVP, CVP, Glasswing, Daybreak, Rosalind/Rosalind Biodefense, Fairwind,
  Gemini for Science):
  - Nothing new. LSVP, Glasswing expansion, Mythos, Fairwind, the real-time cyber safeguards article,
    "expanding support for scientists" and TAC/GPT-5.5 are all catalogued.
  - The CVP opening for Mythos-class models is still not announced.
  - **New lead, not proposed:** OpenAI, "Accelerating the cyber defense ecosystem that protects us
    all". It is a TAC expansion naming GPT-5.4-Cyber and a likely `access_policy`, but it returns 403 to
    the agent, so its date and content are unverified. Friction logged.
  - **Also not proposed:**
    - "Life Science Research Special Access Program" (help.openai.com 11826767): 403, names no model in
      search snippets, and likely predates 2026.
    - "Biodefense in the Intelligence Age" (~Apr 2026): a policy action plan, 403.
- **Spot checks on silent orgs:**
  - Mistral: Leanstral 1.5 (being retired 09-30) and OCR 4, which is out of scope per its note.
  - Meta: Muse Realtime Avatar at Connect (~09-23) is a feature launch with no model card found.
  - A bot-generated third-party PR claims MiniMax M3.5, Kimi K3.1 and StepFun Step-4 as open-weight
    releases. None exists on the orgs' HF pages (newest: MiniMax-Music3 08-07, Kimi-K3 06-13,
    Step-3.7-Flash 05-23). Treated as unreliable.
- **StepFun Step 5 Preview** (API launched 09-20; 600B/27B MoE):
  - The only primary doc is a platform.stepfun.ai product page with no benchmarks, safety content,
    date or license, so it was skipped as a launch without documentation.
  - StepFun's own HF repo is an empty shell, with weights promised for 10-15; re-check then.
  - `TypeSafeAI/Step-5-Preview-BF16` is an unaffiliated re-host ("Duplicated from SHSLab") claiming full
    weights. It was not proposed and was flagged in friction.
- **Unverified tracker mention:** "Atria Dawn Preview" has no identifiable allowlisted publisher, so it
  was ignored.

## 3. Citation mining

No documents were added since 09-25 (count 350), and those were already mined. Today is Sunday, so
there is no retrospective sweep.

## 4. Open issues

None.

## 5. Blocked-URL escalations (11)

All are openai.com or help.openai.com and return 403 to my fetcher as well. Each is **alive**, indexed
by search under its own title today:

- Path to Astra
- Responding to the next frontier of critical cyber capabilities
- Third-party cyber evaluations
- The HF security incident
- Scaling/Trusted Access for Cyber (both)
- Expanding Daybreak
- Rosalind Biodefense
- New GPT-Rosalind capabilities

Introducing GPT-Rosalind and the Daybreak TAC overview were confirmed yesterday; the latter was
substantively revised on 09-26 (v646). No status change was proposed.

## 6. Document update summaries

There were 4 new diffs since the last run, all noise:

- `anthropic-claude-mythos-5-access-policy` v653: only the "Related content" widget rotated (the
  enzyme, Accenture and LSVP posts replaced older ones). The body is unchanged.
- `deepseek-deepseek-v4-flash-vision-exp-model-card` v652: download and Spaces counters, plus a
  Terminal-Bench 2.1 leaderboard widget value.
- `alibaba-qwen-qwen3-8-flash-next-model-card` v655: counters, reordered HF eval-results widget
  entries, and an "Inference" nav item.
- `inclusion-ai-ui-venus-2-9b-model-card` v656: the download counter and an "Inference" nav item.

The older `updated_docs.json` entries were judged by earlier runs.

## 7. Friction and proposals

Two entries were appended to `logs/friction.jsonl`:

- `unfetchable_but_alive`: the OpenAI cyber-defense-ecosystem TAC post and the Life Science special
  access article.
- `ambiguous_criteria`: the TypeSafeAI Step 5 Preview re-host.

There are no new `PROPOSALS.md` entries. The openai.com 403 wall is already documented; if it keeps
hiding new access-policy leads, Phase A attaching text snapshots to candidate leads would address it.
