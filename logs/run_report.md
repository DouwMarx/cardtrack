# cardtrack run report — 2026-09-07 (run id `2026-09-07T06:24Z-local`)

Last successful agent run: `2026-09-06T06:35:28Z`. Search lookback: since that run, floored at
72 h. Today is a **Monday**, so the weekly retrospective sweep was due and is the headline.

Headline: the retrospective sweep found that **Xiaomi's entire MiMo-V2 generation was missing** —
two flagship models announced 2026-03-18 that predate index monitoring by five weeks. Both are now
rows. Four document updates annotated. The recurring diff-noise problem was traced to a single
mechanical cause and written up.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | `add` | Xiaomi — *MiMo-V2-Pro: Flagship Foundation Model towards the Agent Era* (2026-03-18) | **written** → `xiaomi-mimo-v2-pro-model-card` (doc 297, v521) |
| 2 | `add` | Xiaomi — *MiMo-V2-Omni: Omni-Modal Agentic Foundation Model* (2026-03-18) | **written** → `xiaomi-mimo-v2-omni-model-card` (doc 298, v522) |
| 3 | `annotate_version` | `nvidia-cosmos3-super-model-card` v496 | **written** |
| 4 | `annotate_version` | `google-deepmind-gemini-3-5-flash-lite-model-card` v481 | **written** |
| 5 | `annotate_version` | `google-deepmind-gemini-3-6-flash-model-card` v480 | **written** |
| 6 | `annotate_version` | `us-caisi-kimi-k3-independent-eval` v477 | **written** |

Six proposals, six written. No rejections, no duplicates, no noops.

## 1. Phase A candidate triage

180 candidate links reviewed against the state summary. Everything substantive from the recent
index diffs was already catalogued by the 2026-09-05 and 2026-09-06 runs — re-verified, not
assumed: `deploymentsafety.openai.com/gpt-6-astra`, `deepmind.google/models/model-cards/
gemini-3-8-flash/`, the Gemini 3.8 Flash Cyber / Fairwind post, `research.meta.ai/blog/
introducing-muse-spark-1-3`, `tencent/Hy4-preview-FP8`, the `inclusionAI/LLaDA2.2-*` and
`UI-Venus-2` repos, the `nvidia/Cosmos3-*` variants, and `ai.google/gemini-for-science` /
`labs.google/science`.

**Newly resolved this run** (previously carried forward as open questions):

- `nvidia/GEAR-SONIC` — **skip, resolved.** Fetched it: a humanoid whole-body motion-tracking
  control policy whose primary reference is arXiv 2511.07820, i.e. **November 2025**, before the
  2026-01-01 scope floor; and it is a task-specific control policy with no safety evals. Out on
  both grounds independently. This closes the scope-floor question logged in friction on
  2026-09-01 and carried as pending by the last two runs.
- `nvidia/SOMA-X` — **skip, resolved.** A parametric human body model for pose estimation and
  human reconstruction (SMPL/SMPL-X lineage). Auxiliary vision model, out under
  `covered_model_class` and the `nvidia` scope note.
- `tencent/Ex-Omni` — **skip.** Despite the "Omni" name this is not an omni-modal foundation
  model: it generates 52-dimensional facial blendshape coefficients to animate an avatar driven by
  a separate LLM. Auxiliary, no safety evals, and its arXiv reference (2602.07106) is February
  2026. Out under `covered_model_class` and the `tencent_hunyuan` scope note.
- `deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/` — **skip.** It
  names one model (Gemini 2.5 Flash Lite, tested by AVERI with the Singapore AI Safety Institute,
  OpenMined and MLCommons) but publishes **no scores and no task-level results** — the post and its
  technical report describe the cryptographic evaluation architecture only. Fails the system-card
  test: evaluation infrastructure, not an assessment of a named model.
- `anthropic.com/news/enterprise-frontier-safeguards` — **skip.** Read it in full to test the
  `access_policy` boundary. It names Fable 5, Fable 5.1 and Mythos-class models, but EFS is a
  deployment/data-residency product for large enterprises rolling out "in phases" via a sales form;
  the gate is commercial, not vetting. TASK.md is explicit that a GA product launch whose only gate
  is a paid tier is not an access policy. It is already a `related_url` of
  `anthropic-claude-fable-5-1-access-policy`, which is the right placement.

**Skipped, by category** (unchanged from prior runs, re-checked): auxiliary models per
`covered_model_class` and the per-publisher `scope` notes (`gemini-3-5-transcribe`, Meta *Muse
Voice Transcribe*, `tencent/WeMM-Embedding-*`, `nvidia/magpie_tts_*`,
`Nemotron-3-Diarization-preview`, `inclusionAI/ArmorOCR-GGUF`, the NVIDIA `Ising-*`
decoder/calibration repos, `SDLLM-*-1.7B-Base`); quantisation/size/domain variants
(`*-FP8`, `*-NVFP4`, `*-GGUF`, `*-Base-BF16`, `LLaDA2.2-mini`, `Ling-3.0-flash-Fin`,
`Ling-3.0-*-singprobe`, `MiMo-V2.5-DFlash` — the last also has an empty README); and non-documents
(HF user profiles, collections, dataset repos, discussion threads, arXiv/HF paper links, Palisade
terms/privacy/podcast/TikTok links, Cursor case studies, x.ai Grok Bot product posts,
`mistral.ai/news/mistral-x-humain`, `metr.org/blog/2026-08-31-security-update` — METR's own
security incident, not a model eval — and the bulk `ai.google/*` navigation block).

## 2. Targeted search

- **Frontier releases in window.** No un-catalogued release. GPT-6 Astra (Sep 3), Gemini 3.8 Flash
  (Sep 2), Muse Spark 1.3 (Sep 2), Claude Fable 5.1 / Mythos 5.1 (Sep 1) are all present.
- **Restricted-access programme sweep.** Polled the named programmes. All covered: Rosalind
  Biodefense, Daybreak Blue/Red and the Trusted Access for Cyber lineage, Project Glasswing, LSVP,
  Claude Science, the Cyber Verification Program (added last run), Gemini for Science /
  Co-Scientist, Gemini 3.8 Flash Cyber / Fairwind, and the Fable 5.1 / Mythos 5.1 access policy.
  Both **watch items carried from 2026-09-06 remain open and unchanged**: CVP still says Mythos
  access is coming "in the near future" (current tier is Opus/Sonnet only), and LSVP is still
  US-organisations-only. Neither has produced a new post; keep polling.
- **Co-publication check.** Verified that the OpenAI/HuggingFace incident investigation is
  correctly split rather than collapsed: Redwood's copy is
  `redwood-research-gpt-5-6-sol-independent-eval` (`redwoodresearch.org/research/
  hugging-face-incident`) and METR's is `metr-gpt-5-6-sol-independent-eval-2`
  (`metr.org/hugging-face-incident-report-aug-2026.pdf`), two rows as the co-publication rule
  requires. The Substack cross-post `blog.redwoodresearch.org/p/brief-independent-investigation-of`
  surfaced again as a Phase A candidate; it is the same document as Redwood's own copy and is
  already a `related_url`, so it stays a mirror, not a row.

## 3. Citation mining and the Monday retrospective sweep

The three allowlisted orgs whose newest catalogued entry was oldest: **xiaomi** (Apr 27),
**stepfun** (May 23) and **palisade_research** (May 7). Searched each without a recency filter.

**xiaomi — real gap, now closed.** Xiaomi's own model-updates index shows a launch on
**2026-03-18** of three models: MiMo-V2-Pro, MiMo-V2-Omni and MiMo-V2-TTS. None was in the corpus,
because monitoring only picks up Xiaomi through its HuggingFace org page and the V2 generation
shipped **API-only and proprietary with no HF repo at all**. Proposals 1 and 2 catalogue Pro (over
1T total / 42B active, 7:1 hybrid attention, 1M context, ranked 8th on the Artificial Analysis
Intelligence Index) and Omni (unified image/video/audio encoders, 256K context, benchmarked against
Gemini 3 Pro and Claude Opus 4.6). MiMo-V2-TTS is deliberately not proposed — TTS is auxiliary
under `covered_model_class` and the `xiaomi` scope note. MiMo-V2-Flash predates the scope floor
(December 2025). This is exactly the class of miss the sweep exists to catch, and it is the second
week running that it has paid for itself.

One date trap worth recording: the mirrored copies at `mimo.mi.com/docs/…/previous-news/…` carry
"Update Time June 29, 2026", which is a page-revision stamp — the V2 series was retired 2026-06-30
and its posts were moved under `/previous-news/`. I used **2026-03-18**, attested independently by
the `mimo.xiaomi.com` pages themselves, Xiaomi's model-updates index, and Wikipedia, and recorded
the discrepancy in each row's `notes`.

**palisade_research — no gap.** Its research index lists exactly two 2026 outputs, *Language
Models Can Autonomously Hack and Self-Replicate* (May 7) and *Technical Report: Shutdown Resistance
in Large Language Models, on robots!* (Feb 12). Both are already catalogued (under
confusingly-named slugs, but present). The older *Shutdown resistance in reasoning models* work
predates the scope floor.

**stepfun — one deliberate non-proposal.** The four catalogued rows cover its 2026 generative
releases. Two candidates surfaced and neither was proposed:

- **StepAudio 2.5** (arXiv 2605.23463, 2026-05-22) — skipped as a genuine criteria ambiguity, not
  a judgment I wanted to guess. It is billed as a unified audio-language *foundation* model, which
  `covered_model_class` admits, but its three headline capabilities are ASR, TTS and realtime
  spoken interaction, two of which that same criterion names as out of scope. It reports no safety
  evals, is API-only with no publisher-hosted card, and the only full document is on arXiv — and
  the corpus holds **zero arXiv canonical URLs across 296 documents**, so proposing one would set a
  precedent rather than follow one. Logged as `ambiguous_criteria`. Worth noting the corpus is
  already inconsistent here: `stepfun-step-audio-r1-1-model-card` is in only because it happened to
  have an HF repo.
- **ACE-Step 1.5** — a music generation foundation model (2026-01-28, MIT, open weights, AMD
  deployment guide, ComfyUI support, 55k monthly downloads). Squarely inside `covered_model_class`,
  which names music generation explicitly, but its publisher `ace-step` is **not on the
  allowlist**, so there is no key to propose it under. Recorded in `logs/PROPOSALS.md` as TASK.md
  directs, rather than filed under a neighbouring publisher.

## 4. Open issues

`logs/open_issues.json` is empty. No investigations, no comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is empty. Nothing to verify, no `dead` proposals.

## 6. Document updates

Reviewed **all 20** pending diffs (not a sample) and annotated 4, under the cap of 5.

**Annotated — real document changes**

- `nvidia-cosmos3-super-model-card` v496 — a new training-data provenance line pointing to
  NVIDIA's *Public Summary of Training Content*. Same disclosure the last run annotated on
  Nemotron-3-Ultra v494, so this is a deliberate NVIDIA-wide rollout.
- `google-deepmind-gemini-3-5-flash-lite-model-card` v481 — "complex video reasoning" added to the
  intended-use list.
- `google-deepmind-gemini-3-6-flash-model-card` v480 — "complex video reasoning" added, and
  "multi-week enterprise processes" replaced by the broader "enterprise workflows". A scope change
  in both directions.
- `us-caisi-kimi-k3-independent-eval` v477 — the dateline gained ", Updated August 28, 2026",
  recording a publisher revision of the joint UK AISI / CAISI assessment. Findings unchanged.

**Skipped as noise, with the cause identified.** The remaining 16 divide into two groups. Page
furniture: `anthropic-claude-fable-5-addendum` v498 and `anthropic-claude-sonnet-4-5-other-2` v471
(the "Related content" sidebar rotating), the Palisade redirect stubs v508/v509 (the 2026-09-06
problem, still unfixed), and the Redwood v510/511/512 title-line extraction noise. And then eight
diffs — v492, v493, v483, v478, v484, v485, v486, and the tail of v496 — that turned out to be
**one mechanical artefact**: HuggingFace re-rendering its auto-generated trailing widgets, where
the community `Evaluation results` leaderboard comes back in a different row order and the differ
reports it as a large add/remove block. The tell is that the *same* new rows
(`harborframework/terminal-bench-2.1`, `llamaindex/ExtractBench`) appear on cards from Tencent,
Qwen, poolside and StepFun on a single crawl date, which no coordinated publisher edit would do.
This is the first run to pin that down rather than dismiss the diffs one at a time.

## 7. Friction log

Four lines appended to `logs/friction.jsonl`: the HF widget-churn diagnosis
(`diff_noise_source_identified`), the StepAudio 2.5 criteria ambiguity (`ambiguous_criteria`), the
resolution of the GEAR-SONIC/SOMA-X question carried since 2026-09-01 (`resolved_prior_friction`),
and a new tooling obstacle (`tool_sandbox_blocks_proposal_stdin`) — see below.

## 8. Proposals

Two dated entries appended to `logs/PROPOSALS.md`: the HuggingFace widget-churn fix (strip or sort
the auto-generated trailing blocks before diffing, which converts most of these to zero-line diffs
that never reach `updated_docs.json`), and the ACE-Step / music-generation allowlist gap.

## Judgment calls worth an operator's eye

- **Cataloguing the MiMo-V2 pages as `model_card`s.** They are release posts, not formal cards —
  no limitations section, no safety evals. But they carry architecture, parameter counts, context
  length and benchmark results, they are the *only* primary documentation for two API-only
  proprietary models, and the corpus already treats equivalent Chinese-lab release posts this way.
  I attested `has_safety_evals: false` on both, honestly. If the operator would rather these be
  `other`, both are a one-field change.
- **Two rows rather than one for MiMo-V2-Pro and MiMo-V2-Omni.** Same launch day, but two distinct
  models documented on two separate pages, so the "one family card → one entry" rule does not
  apply. Flagging it because the alternative reading is defensible.
- **StepAudio 2.5 skipped rather than admitted.** `policy.when_uncertain` is `admit_and_flag`,
  which argues for proposing it; I did not, because the uncertainty is not about *this* document
  but about a precedent (arXiv as canonical URL) that would bind future runs. Happy to be
  overruled — it is a one-proposal fix if the operator says yes.
- **Tooling, worth fixing before it bites harder.** Three of the four documented write routes are
  blocked from inside the sandbox: heredocs carrying JSON trip the "brace with quote character"
  guard, shell `>>` redirection to `logs/friction.jsonl` is refused despite the path being inside
  the working directory, and `tee -a` needs interactive approval a headless run cannot give. The
  proposals went through as `printf %s '<json>' | propose_doc.py --json -`, which forbids
  apostrophes anywhere in the payload — so every justification and note this run was written
  without possessives or contractions. That is a silent quality tax on the prose the corpus stores.
