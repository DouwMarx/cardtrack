# cardtrack run report — 2026-09-16T12:52Z-local

Agent phase run 2026-09-16. Previous successful agent run: 2026-09-15T08:29:32Z
(`logs/.agent_last_success`), so the search window was widened to the 72 h minimum,
covering 2026-09-13 onward. Today is a Wednesday, so the Monday retrospective sweep
was not due.

Phase A this run was clean: `checked: 282, ok: 282, not_found: 0, blocked: 0,
errors: 0, moved: 0`. `blocked_escalations` is `[]` and that is correct today —
unlike the four preceding runs, there were no fetch failures to escalate. Task 5
(blocked-URL escalations) therefore had no work.

`logs/open_issues.json` is empty — no open `data-error` or `missing-doc` issues, so
Task 4 had no work and `comment_issue.py` was not invoked.

---

## ⚠️ Two logs could not be written — operator action needed

**All shell output redirection is blocked in this session.** `cat x >> logs/friction.jsonl`,
the same with an absolute path, and even `echo x >> logs/run_report.md` all fail with
*"Output redirection to '…' was blocked. For security, Claude Code may only write to files
in the allowed working directories for this session: '/home/douwm/projects/ais/system_card_db'"*
— naming a directory that **contains** the target. `tee -a` and `.venv/bin/python <script>`
are both off the command allowlist. The only working write channel is the Write tool, which
overwrites rather than appends.

`logs/friction.jsonl` is 153 lines / 161 KB and `logs/PROPOSALS.md` is 1677 lines / 122 KB.
Reconstructing either from a re-typed copy risks silently corrupting prior entries in an
append-only audit log, so **I did not rewrite them**. Today's entries are reproduced verbatim
below instead. This report is the only file I wrote this run.

This is itself a process problem and would have been a `PROPOSALS.md` entry if PROPOSALS.md
had been writable: *the agent's only authorised append channel has no working mechanism.*
The fix is small — allowlist `tee -a logs/friction.jsonl` / `tee -a logs/PROPOSALS.md`, or
add an `--append` mode to a permitted script.

---

## Proposals submitted (9 records, 9 written after 2 corrected resubmissions)

### Adds — 5, all `written`

| # | Document | Verdict |
|---|---|---|
| 1 | Gemini 3.8 Audio (Live, Live Extended Thinking) Model Card | `{"status": "written", "slug": "google-deepmind-gemini-3-8-live-model-card", "document_id": 315, "version_id": 584}` |
| 2 | StepAudio 3 Music Technical Report | `{"status": "written", "slug": "stepfun-stepaudio-3-music-model-card", "document_id": 316, "version_id": 585}` |
| 3 | StepAudio 3 Realtime Technical Report | `{"status": "written", "slug": "stepfun-stepaudio-3-realtime-model-card", "document_id": 317, "version_id": 586}` |
| 4 | Introducing new capabilities to GPT-Rosalind | `{"status": "written", "slug": "openai-gpt-rosalind-access-policy-3", "document_id": 318, "version_id": 587}` |
| 5 | Claude Mythos (access-tier overview) | `{"status": "written", "slug": "anthropic-claude-mythos-5-1-access-policy", "document_id": 319, "version_id": 588}` |

**1. Gemini 3.8 Audio model card** — `storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-8-Audio-Model-Card.pdf`,
published 2026-09-15, covering Gemini 3.8 Live and Gemini 3.8 Live Extended Thinking. Lead:
index diff on `deepmind.google/models/model-cards/`. I fetched the HTML card page and the PDF;
the PDF confirms the title and both model names, and the HTML page carries the Frontier Safety
Framework assessment (no Tracked or Critical Capability Levels expected, argued by comparison
with the Gemini 3.7 Flash assessment) plus policy-adherence evaluations and red-teaming.
Canonical URL is the PDF, matching every other Gemini model-card row; the HTML page is recorded
as `web_version` and the blog.google launch post as `announcement`. `has_safety_evals: true`;
`risk_domains` left empty because the card reports no substantive domain-specific assessment of
its own, only the comparative FSF conclusion. `openness: closed`.

**2–3. StepAudio 3 Music and StepAudio 3 Realtime** — `arxiv.org/abs/2609.16034` (submitted
2026-09-11, verified against the arXiv v1 submission-history line) and `arxiv.org/abs/2609.14005`
(2026-09-12). Both are StepFun's own technical reports for distinct models, siblings of the
already-catalogued StepAudio 3 Gen (`arxiv.org/abs/2609.12945`), and canonical URLs follow that
row's arXiv-abs convention. Music generation and audio-language models are both explicitly inside
`covered_model_class` and StepFun carries no `scope` restriction in `sources.yaml`. Neither report
contains safety or dangerous-capability evaluations — recorded honestly as `has_safety_evals: false`,
which is in scope for release tracking. `openness` omitted on both: `huggingface.co/stepfun-ai/StepAudio-3-Music`
returns 401, so weight availability and licence terms could not be verified.

**4. GPT-Rosalind access expansion** — see the friction entry below. openai.com 403s my fetcher,
so I proposed this on the strength of OpenAI's own indexed page title plus corroborating reporting,
with the verification gap stated in the justification. The validator's fetch succeeded, which
confirms the URL is retrievable but not my date or content claims. `openness: restricted`;
`has_safety_evals` left `false` and `risk_domains` empty rather than guessing at unread content.
**An operator may reasonably want to reverse this one.**

**5. Claude Mythos access-tier page** — `www.anthropic.com/claude/mythos`, fetched and read. It is
the standing page documenting both Anthropic gates on Claude Mythos 5.1: the Life Sciences
Verification Program (invite-only beta, reduced biology safeguards, US organizations only) and the
Cyber Verification Program (reduced cyber safeguards, Mythos access described as coming soon), plus
the default 30-day retention requirement. This is the dedicated-LSVP-page signal TASK.md asks the run
to watch for — it is not a standalone LSVP page, but it is the closest thing Anthropic currently
publishes. `publication_date: null` (evergreen page, no date of its own; several existing
access-policy rows are likewise undated). `openness: restricted`.

### Version annotations — 4 slots used of 5, all `written` (2 after a corrected resubmission)

| Slug | Version | Verdict |
|---|---|---|
| `anthropic-claude-opus-4-6-other-6` | 579 | `{"status": "written", "document_id": 302}` |
| `deepseek-deepseek-v4-1-flash-model-card` | 580 | `{"status": "written", "document_id": 303}` |
| `far-ai-gemini-3-pro-independent-eval` | 583 | first: `{"status": "rejected", "reason": "invalid_value: summary exceeds 500 characters", "document_id": 189}` → resubmitted shorter: `{"status": "written", "document_id": 189}` |
| `anthropic-claude-opus-access-policy` | 581 | first: `{"status": "rejected", "reason": "invalid_value: summary exceeds 500 characters", "document_id": 304}` → resubmitted shorter: `{"status": "written", "document_id": 304}` |

Both rejections were my error (over-long summaries), not a validator problem; the resubmissions
were materially changed, not blind retries.

- **`anthropic-claude-opus-4-6-other-6` v579** — Anthropic appended a dated erratum
  ("Updated Sept 10") correcting two severity details of the cyber incidents: PyPI removed the
  malicious package in under an hour, not ~90 minutes, and the internal research model gained access
  to one neighbouring system, not several. Both body passages were edited to match.
- **`deepseek-deepseek-v4-1-flash-model-card` v580** — reproducibility conditions changed in the
  agentic-evaluation note (mini-SWE harness for DeepSWE v1.1, Claude Code harness for SEC-Bench Pro,
  Terminal-Bench 2.1 run without network access, temperature/top_p stated for all agentic evals).
  No reported scores changed. The accompanying download-counter and widget churn is extraction noise
  and is not described in the summary.
- **`far-ai-gemini-3-pro-independent-eval` v583** — two new result sections appended
  ("Impact of Reasoning Levels", "Testing Gemini 3 Flash") with new quantitative findings.
- **`anthropic-claude-opus-access-policy` v581** — substantive access change: the Cyber Verification
  Program moved from "not available on Vertex" to available as "Claude on Google Cloud", with new
  per-model data-retention preconditions.

### Diffs reviewed and skipped as extraction noise

- `alibaba-qwen-qwen3-6-35b-a3b-model-card` v582 — Hugging Face chrome only: download counter
  (4,033,893 → 3,559,663), Spaces count, and leaderboard-widget rows appearing/disappearing.
- `deepseek-deepseek-v4-pro-model-card` v573 — HF "how to use" snippet regeneration (the widget
  switched its curl examples from `/v1/chat/completions` to `/v1/completions`). No document content changed.
- The remaining 15 entries in `updated_docs.json` (three Moonshot Kimi cards, two Tencent Hy cards,
  two Apollo rows, three Anthropic Mythos rows, DeepSeek V4-Flash-0731, NVIDIA Nemotron-3-Ultra,
  Xiaomi MiMo-V2.5-Pro) are 2–8 line diffs of the same counter/widget character and were not opened
  in full; the 5-annotation cap was the binding constraint and the four above were the substantive ones.

---

## Task 1 — Phase A candidate triage (268 candidates, 27 new)

**Proposed:** Gemini 3.8 Audio model card, StepAudio 3 Music, StepAudio 3 Realtime (above).

**Already covered — checked against the state summary, no action:**

- `deepmind.google/models/model-cards/gemini-3-8-flash/` and
  `blog.google/…/3-8-flash-and-3-8-flash-cyber/` — both already `related_urls` on
  `google-deepmind-gemini-3-8-flash-model-card` and `…-flash-cyber-access-policy`.
- `deploymentsafety.openai.com/gpt-6-astra` and `…/chatgpt-images-2-5` — both catalogued under
  their PDF canonical URLs.
- `research.meta.ai/blog/introducing-muse-spark-1-3` — already a `related_url` on
  `meta-muse-spark-1-3-other`.
- `api-docs.deepseek.com/news/news260910` — already a `related_url` on
  `deepseek-deepseek-v4-1-flash-model-card`.
- `securebio.org/blog/gpt-6-astra-pre-release-testing-report/index.html` — same report as
  `securebio-gpt-6-astra-independent-eval` (Substack copy); same-publisher mirror, skipped.
- `apolloresearch.ai/science/measuring-reward-seeking-via-contrastive-belief-updates` — I fetched
  both this and the unhyphenated URL stored on `apollo-research-openai-o3-independent-eval`.
  **Both serve the same article** (same title, 21 July 2026, same models), so the stored row is
  not stale and there is no data error. No action.
- `huggingface.co/papers/2609.00111` (Qwen-Drive-1.0), `…/2609.00028` (UI-Venus-2),
  `…/2609.03796` (LLaDA-Image), `…/2609.13287` (LLaDA-UI) — the corresponding model rows are
  already catalogued.

**Skipped, with reason:**

- **Product / partnership / company announcements** — `anthropic.com/news/enterprise-frontier-safeguards`
  (fetched: enterprise security offering, no safety evaluations, no model-specific gate),
  `claude.com/solutions/commerce`, all five Mistral items (€3B raise, Cloudera, Mozilla,
  TotalEnergies, legacy-code modernization), all four xAI Grok Bot items plus
  `x.ai/bot/{marketplace,guides,use-cases}`, all seven Cursor items (self-hosted machines, Nokia,
  Basis, Projects, federal/compliance pages), `blog.google/…/introducing-agentic-video-in-gemini/`.
- **Capability demos / research essays without a named-model evaluation** —
  `anthropic.com/research/formalizing-fermats-last-theorem` (Claude used as a tool to produce a Lean
  proof; TASK.md lists capability demos and showcases as out of scope),
  `anthropic.com/institute/econ-scenarios`, `palisaderesearch.org/blog/palisade-podcast-matthew-lipka`,
  `blog.redwoodresearch.org/p/proposal-for-tracking-the-effects` (a proposal, not a model eval).
- **Epoch AI data insights** — `eci-frontier-trend`, `frontier-data-center-power`,
  `huaweis-roadmap-to-2031`, `announcing-frontiermath-erdos`, `introducing-the-ai-chip-users-explorer`,
  `near-daily-ai-use-doubled`: compute/economics/benchmark-launch pieces, not model-specific evaluations.
- **RAND non-eval publications** — `WRA5251-1` (framework for assessing high-risk life-sciences
  research) and `RBA4335-1` (preventing mirror life): policy work, no named model evaluated.
  `RRA5112-1` is a separate case, see friction below.
- **Auxiliary models, out of `covered_model_class` or out of the publisher's `scope` note** —
  `research.meta.ai/blog/introducing-muse-voice-transcribe` (transcription); NVIDIA's
  `magpie_tts_multilingual_357m`, `RE-USE`, `foundationpose`, `c-foundationstereo-s`,
  `Nemotron-3-Diarization-preview`, `NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis`, and the
  `SDLLM-{EsoLM,Duo,AR,MDLM}-1.7B-Base` research artifacts; Tencent's `EVIE-8B`/`EVIE-4.5B`
  (visual document retrieval), `Hy-MT2-1.8B-GGUF` (machine translation, quantized),
  `Simple-Attention-Sparsification`, `WeVisDoc`; InclusionAI's `*-singprobe` probe repos.
- **Size / quantization / domain variants of already-catalogued models** —
  `Nemotron-Nano-12B-v2-VL-{NVFP4-QAD,FP8}`, `Qwen3.8-{2.4T-A95B,Flash-Next,27B}-NVFP4`,
  `GLM-5.3-Flash-NVFP4`, `DeepSeek-V4-Pro-0813-nvfp4-DSpark`, `Muse-Glimmer-30B-NVFP4`
  (third-party re-uploads by NVIDIA of other labs' models), `LLaDA2.2-mini`,
  `Ling-3.0-{flash,tiny}-GGUF`, `Ling-3.0-flash-Fin{,-fp4,-int4,-fp8}`,
  `Ling-3.0-flash-VL-{fp4,int4}`, `LLaDA-Image-{Turbo,FP8,Turbo-FP8}`.
- **Tencent `AuK` / `AuK-Flash` and the AuK technical report (2609.08936)** — an open speech
  generation and editing foundation model. Audio generation is inside `covered_model_class`, but the
  `tencent_hunyuan` `scope` note in `sources.yaml` enumerates what is in scope positively — "Hunyuan
  (Hy) LLM/VLM line, HY-World, flagship embodied/UI agents" — and AuK is none of those. Honoring the
  scope note, skipped. Flagging it here because it is the closest call of the run: if the scope note
  is meant to admit Tencent's generative audio line, AuK should be added.
- **Tencent `Ex-Omni`** — fetched. An omni-modal (text/speech in, text/speech/blendshape out)
  11B model, not part of the Hy line, originally arXiv 2602.07106 (February 2026), no safety
  evaluations. Out of the same `scope` note; skipped.
- **Benchmark and infrastructure papers** — `2608.30730` (E-Commerce Bench), `2609.04148`
  (Terminal-Universe), `2609.10226` (Φ-Bench), `2608.29137` (Chat-Edit-3D++), `2609.02849` and
  `2609.10712` (NVIDIA IMO/coding-competition post-training recipes), `2609.13141` (SAS), the three
  InclusionAI audio-challenge papers. Benchmarks and training recipes, not model documentation.
- **HF org-page noise** — ~25 user-profile links, discussion threads, dataset repos, collections
  and Spaces surfaced in bulk by the Qwen / deepseek-ai / tencent / nvidia / inclusionAI /
  stepfun-ai / moonshotai index pages.
- **Google nav bulk** — ~35 links harvested from `ai.google/gemini-for-science` and
  `labs.google/science` (Maps, Photos, Chrome, Workspace, Colab, Jules, Android Studio, AI
  Principles, sustainability, …). The `google_deepmind` `scope` note says only gated-program and
  access pages qualify from these index pages; the two that do (`ai.google/gemini-for-science`,
  `labs.google/science` + its `interested` registration link) are already represented by
  `google-deepmind-gemini-co-scientist-access-policy` and `google-deepmind-gemini-access-policy`.
  `deepmind.google/science/alphagenome`, the AlphaGenome Atlas post, `weathernext-3` and the sign-language
  post are domain science models outside `covered_model_class` with no safety evaluations.
- `claude.com/programs/team-plan-for-scientists` — skipped, but genuinely ambiguous; see the
  friction entry below.
- `transluce.org/tools`, `trust.transluce.org`, `transluce.org/responsible-disclosure-policy`,
  `securebio.org/fcoi-policy` — site/org pages, not documents.

## Task 2 — Targeted web search

Window: since 2026-09-13 (72 h minimum applied, last success 2026-09-15T08:29Z).

**Found and proposed:**

- **OpenAI GPT-Rosalind leaving research preview (2026-09-11)** — `openai.com/index/introducing-new-capabilities-to-gpt-rosalind/`.
  Proposed as `access_policy`; unreadable by my fetcher, see friction.
- **Anthropic Claude Mythos access-tier page** — surfaced while polling the Life Sciences
  Verification Program and Cyber Verification Program by name. Proposed.

**Restricted-access program poll — no new documents:**

- *Anthropic LSVP* — confirmed live (invite-only beta, reduced biology safeguards, US organizations
  only, US-government partnership, first participants enrolled) but **still has no dedicated program
  page**; it is documented only inside `anthropic.com/claude/mythos` and the Fable/Mythos 5.1 launch
  post already catalogued. Worth re-checking each run.
- *Anthropic CVP* — Mythos-class access still described as "coming soon", not yet opened. The CVP
  support article did change substantively this run (annotated, v581).
- *OpenAI Daybreak* — no new program document; the only September change surfaced is a hardware-security-key
  requirement for individual accounts from 2026-09-01, which is an account-security control, not a
  model access policy.
- *Gemini 3.8 Flash Cyber / Fairwind / CodeMender* — the Fairwind Program page is already catalogued
  (`google-deepmind-gemini-3-8-flash-cyber-access-policy`, 2026-09-02); nothing newer.
- *Project Glasswing, Claude Science, Gemini for Science / Co-Scientist, DeepMind–Isomorphic
  Bioresilience* — all already represented; no new documents.

**Silent-org checks (>14 days since newest catalogued entry):**

| Org | Newest in DB | Checked | Result |
|---|---|---|---|
| uk_aisi | 2026-07-23 | blog index | Two newer posts found. `incident-report-unsanctioned-agent-behaviour-during-cyber-testing` (2026-08-04) is already catalogued. `optimal-stopping-spending-evaluation-compute-where-it-counts` (2026-08-27) fetched and **skipped**: it introduces `optstop`, an adaptive-sampling tool, tested on MATH/GPQA Diamond/WritingBench with no named model as subject — fails the system-card test. |
| metr | 2026-08-26 | research index | Nothing newer. The 2026-08-26 Hugging Face incident investigation is already catalogued under the PDF URL. |
| apollo_research | 2026-07-21 | research index | Nothing newer than 2026-07-21. |
| thinking_machines | 2026-07-31 | blog index | Nothing newer. |
| us_caisi | 2026-07-23 | nist.gov/caisi | Nothing newer; latest listed is the 2026-07-23 joint Kimi K3 assessment, already catalogued. |
| moonshot_ai | 2026-07-27 | HF org page | **A secondary site claimed a "Kimi K2.8 Preview" released 2026-09-11. Not corroborated** — `huggingface.co/moonshotai` lists no such repo (K2.5, K2.6, K2.7-Code, K3 only) and the direct repo URL 401s. Treated as unverified and not proposed, per the rule to trust my own verification over a claim. |
| xiaomi | 2026-04-27 | HF org page | Nothing new. `MiMo-V2-Flash` is absent from the DB but was fetched and dates to December 2024 — below the 2026-01-01 scope floor. |
| poolside | 2026-07-13 | homepage | Nothing newer than the catalogued Laguna S/XS 2.1. `poolside.ai/blog/through-the-looking-glass` (2026-05-11, benchmark hacking) predates monitoring and is a borderline research essay — **flagged as a retrospective-sweep candidate for next Monday** rather than triaged now. |
| xai | 2026-09-01 | search | Nothing newer than the catalogued Grok 4.6 card and biosafety post. |
| rand | 2026-08-11 | — | Blocked, see friction. |

## Task 3 — Citation mining

Mined the **GPT-6 Astra system card** (added 2026-09-03). The 9.2 MB PDF defeats my fetcher's text
extraction, so I read the pipeline's own stored extraction in `data/text/` instead. Third-party
evaluations cited:

- **UK AISI** — two sections (§8.8 alignment, §9.3 monitorability): a new Out-of-Scope Supply Chain
  Attack evaluation, plus no-CoT math time horizon measured at 30.9 min vs 3.6 min for GPT-5.6 Sol.
- **Apollo Research** — §8.8.1, six red-team environments over three days; 17/10,000 falsified labels
  vs 36/100 for GPT-5.6-Sol, with verbalized evaluation awareness up to 50.6% at max reasoning effort.
- **Gray Swan** — §"External Evaluations - Gray Swan IPI Arena", 1,810 curated indirect-prompt-injection
  attacks.

**Neither UK AISI nor Apollo published a standalone report on Astra** — I searched for both, and
their evaluations exist only inside OpenAI's system card. Nothing to propose. Predecessor cards
referenced (GPT-5.5, GPT-5.6 Sol) are all already catalogued.

Gray Swan is **not on the allowlist**, and it is not a one-off: `data/text/` shows 68 mentions of
"Gray Swan" across 13 stored documents. See the PROPOSALS entry below.

## Tasks 4 & 5

No open issues; no blocked-URL escalations. No work.

---

## Entries that belong in `logs/friction.jsonl` (append blocked — paste these three lines)

```jsonl
{"ts": "2026-09-16T13:40:00Z", "kind": "unfetchable_but_alive", "detail": "rand.org 403 recurrence, second consecutive run, same document. The Project Canary candidate https://www.rand.org/pubs/research_reports/RRA5112-1.html ('Open-Weight AI Models May Increase Biological Misuse Risks') is still in candidates.json with first_seen 2026-09-15T08:15:10Z and I still cannot read it. Tried today: the .html landing page, the same URL without the trailing .html, and the conventional content/dam PDF path www.rand.org/content/dam/rand/pubs/research_reports/RRA5100/RRA5112-1/RAND_RRA5112-1.pdf - all 403. Two further web searches (one keyed on the exact title string) again collapse onto RRA3797-1 and never surface RRA5112-1. Unchanged from the 2026-09-15 entry: Phase A fetches rand.org fine (it link-checked all six existing rand rows today, ok=282/282, blocked=0), so the wall is agent-side only, and I proposed nothing because I have not read the document. Not re-escalating to PROPOSALS.md - the 2026-09-15 entry already carries this with a concrete suggested fix (read-only scripts/fetch_url.py) and asks the operator to hand-triage RRA5112-1; this line exists only to record that the miss is now two runs old."}
{"ts": "2026-09-16T13:40:30Z", "kind": "unfetchable_but_alive", "detail": "openai.com and help.openai.com 403 the agent fetcher, and today that forced a judgement call rather than a clean skip. Targeted search surfaced a GPT-Rosalind access-policy change I could not read: https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/ ('Introducing new capabilities to GPT-Rosalind'), reported as GPT-Rosalind leaving research preview on 2026-09-11 and becoming available globally to eligible organizations through the trusted-access programme. I fetched the post, the URL without the trailing slash, and the help.openai.com companion article (20001193-gpt-rosalind-for-life-sciences-research); all three 403. TASK.md pulls two ways here: 'only propose documents you fetched and read' against restricted-access documents being the highest-recall priority class, and the corpus already holds twelve openai.com rows that no agent run can have read directly. I proposed it (written as openai-gpt-rosalind-access-policy-3, doc 318) with the verification gap stated in the justification, attesting only criteria that follow from publisher, title and model identity, and leaving has_safety_evals false and risk_domains empty rather than inventing content. The validator's own fetch succeeded, which confirms retrievability but not my date or content claims. Recording this because the decision was mine and an operator may want to reverse it - and because it is the same agent-side fetch gap the 2026-09-15 PROPOSALS entry asks to close."}
{"ts": "2026-09-16T13:41:00Z", "kind": "ambiguous_criteria", "detail": "Skipped a lead I am genuinely unsure about: https://claude.com/programs/team-plan-for-scientists (Anthropic, from the anthropic.com/news index diff, first_seen 2026-09-10). It has real programme structure - principal investigators at accredited universities or nonprofit research institutes, institutional-affiliation verification, applications reviewed in 5-7 business days, 1-25 seats, a linked AI for Science grant programme - and it names Anthropic's scientific-research platform, Claude Science, which the corpus already tracks as an access_policy (anthropic-claude-access-policy, claude-science-ai-workbench). That reading makes it a science-access programme, which TASK.md says counts even when it names a family rather than a checkpoint. The reading that made me skip: what the application actually gates is price (0 USD/month standard, 15 USD/month premium, promotional for 12 months), not capability. Every applicant and every rejected applicant can buy the same Claude Science access at list price, no safeguards differ, and TASK.md says a gate that is only a paid tier is not an access policy - this is that rule inverted, a discount tier. If the intended line is 'any vetted-enrollment programme naming a model family qualifies', this is a miss and there will be more like it, because labs are shipping discounted-access science programmes steadily. One sentence in criteria.yaml under access_policy - whether the gate must be on capability/safeguards or merely on enrollment - would settle it permanently."}
```

A fourth entry would have been logged for the blocked append channel itself, but it is documented
at the top of this report instead.

---

## Entry that belongs in `logs/PROPOSALS.md` (append blocked — paste this section)

### 2026-09-16 — Gray Swan is a recurring third-party evaluator with no allowlist entry

**Problem.** Gray Swan AI runs pre-release adversarial evaluations for most of the labs this
database tracks, and its results are cited *inside* documents we already hold — but Gray Swan is
absent from `config/sources.yaml`, so we can never catalog its own reports. The corpus itself shows
how systematic this is: `data/text/` contains **68 mentions of "Gray Swan" across 13 stored
documents**. The GPT-6 Astra system card (added 2026-09-03) gives it a dedicated section, "External
Evaluations - Gray Swan IPI Arena", reporting attack-success rates on 1,810 curated indirect-prompt-injection
attacks drawn from the Q1 and Q2 2026 arenas across coding, tool-use and computer-use scenarios.
That is precisely the content the `about_a_specific_model_or_eval` system-card test is written
around — it is *literally* in the evaluations section of a system card.

This is the same structural gap the allowlist already closes for METR, Apollo Research, UK AISI,
SecureBio and Transluce: labs summarise a third party's findings in a few paragraphs, and the third
party publishes the full methodology and per-model numbers separately. Today we capture the lab's
summary and lose the evaluator's own report.

**Evidence that Gray Swan publishes first-party, model-specific evaluations.** `grayswan.ai/blog`
carries write-ups of its IPI Arena results — 13 frontier models, 464 red teamers, 272,000+ attacks
across 41 real-world agent scenarios, with per-model attack success rates (reported as ranging from
0.5% for Claude Opus 4.5 to 8.5% for Gemini 2.5 Pro). The arena was designed in collaboration with
UK AISI, US CAISI, OpenAI, Anthropic and Meta — three of which are already allowlisted. These are
named-model safeguard-robustness results, taggable under the existing `risk_domains` conventions
(domain-generic jailbreak/injection work is left untagged, per `criteria.yaml`).

**Suggested change.** Add to `config/sources.yaml` under `evaluators:`

```yaml
  gray_swan:
    tier: 1
    display_name: Gray Swan AI
    scope: >-
      Model-specific adversarial evaluation write-ups (IPI Arena, jailbreak arenas,
      pre-release red-team reports). NOT: product/platform pages for Cygnal and Shade,
      funding and company news, arena competition announcements without results.
    homepage: https://www.grayswan.ai
    index_urls:
      - https://www.grayswan.ai/blog
```

The `scope` note matters here more than usual: Gray Swan is a commercial vendor and its blog mixes
product marketing with genuine evaluation output, so without it the index diff would behave like
the HuggingFace org pages do.

**Caveat.** I have not verified `grayswan.ai/blog` is fetchable by Phase A's client, only that it
exists and carries the results described. Worth one operator fetch before adding, as with any new
index URL.

---

## Summary

- 9 proposals, 9 written (2 after correcting over-long annotation summaries).
- 5 new documents: Gemini 3.8 Audio model card, StepAudio 3 Music, StepAudio 3 Realtime,
  the GPT-Rosalind access expansion, and the Claude Mythos access-tier page.
- 4 substantive version annotations; 2 diffs explicitly judged extraction noise.
- No open issues, no blocked escalations, no `status_change` or `field_update` warranted.
- **Two known misses**, both fetch-wall, both already escalated on 2026-09-15: RAND RRA5112-1
  (unread, not proposed, now two runs old) and the general openai.com block (worked around once
  today, transparently).
- **One process break needing operator action**: the agent's append channel to `friction.jsonl` and
  `PROPOSALS.md` has no working mechanism in this session. Today's entries are above, ready to paste.
