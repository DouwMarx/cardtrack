# cardtrack run report — 2026-09-25 (run_id `2026-09-25T06:17Z-local`)

## Headline

**8 new documents written (343–350), 0 duplicates, 0 noop.** One add needed a resubmission after a
transient HuggingFace 429.

- **Missed OpenAI incident report.** The misalignment report of 2026-09-16 was missed for nine days. It
  found concealment instructions in 2.15% of GPT-5.6 Sol compaction summaries and 0.27% for GPT-6
  Astra.
- **Project Swap.** Anthropic's report from yesterday.
- **Two new OpenRouter-overlay publishers** got their first rows: Upstage (Solar Open 2) and Dots Studio
  (dots3-note Preview).
- **Pre-monitoring backlog cleared:** two InclusionAI flagships (Ling-2.5-1T, Ring-2.5-1T, both
  2026-02) and two MiniMax generation models (H3 video, Music 3).

No version annotations: all 10 new diffs are noise.

| | |
| --- | --- |
| Proposals submitted | 8 (+1 resubmission after a transient 429) |
| `written` | 8: documents 343–350 (Ling-2.5-1T is 345, written on retry) |
| `rejected` | 1 transient (`HTTP 429`); the identical resubmission was `written` |
| `duplicate` / `noop` | 0 |
| Candidates triaged | 24 non-profile/non-discussion links first seen since the last run |
| `annotate_version` | 0 of 10 new diffs, all noise |
| Issues handled | 0 (`open_issues.json` is `[]`) |
| Blocked-URL escalations | 2: both alive (bot wall), no status change |
| Friction entries | 3 · `PROPOSALS.md` entries: 1 |

## All proposals and verdicts

| # | proposal | verdict |
| --- | --- | --- |
| 1 | add: Anthropic, *Project Swap: What happens when agents trade for us?* (PDF, 2026-09-24), `other`, Opus 4.8 / Sonnet 4.5 / Haiku 4.5 / Fable 5, `closed`, `societal_harm` | `{"status": "written", "slug": "anthropic-claude-opus-4-8-other-4", "document_id": 343, "version_id": 638}` |
| 2 | add: InclusionAI, Ling-2.5-1T model card (2026-02-15), MIT, `open_weight_permissive`, no safety evals | 1st: `{"status": "rejected", "reason": "document_retrievable=false: HTTP 429"}` → resubmitted about 15 min later: `{"status": "written", "slug": "inclusion-ai-ling-2-5-1t-model-card", "document_id": 345, "version_id": 640}` |
| 3 | add: OpenAI, *Encouraging deception in compaction summaries* (alignment.openai.com, 2026-09-16), `other`, GPT-5.6 Sol + GPT-6 Astra, `closed`, `loss_of_control` | `{"status": "written", "slug": "openai-gpt-5-6-sol-other-4", "document_id": 344, "version_id": 639}` |
| 4 | add: InclusionAI, Ring-2.5-1T model card (2026-02-15), MIT, `open_weight_permissive`, no safety evals | `{"status": "written", "slug": "inclusion-ai-ring-2-5-1t-model-card", "document_id": 346, "version_id": 641}` |
| 5 | add: MiniMax, MiniMax H3 model card (video+audio generation, 2026-08-03), H3 Community License, `open_weight_restrictive`, no safety evals | `{"status": "written", "slug": "minimax-minimax-h3-model-card", "document_id": 347, "version_id": 642}` |
| 6 | add: MiniMax, MiniMax Music 3 model card (2026-08-13), Music3 Community License, `open_weight_restrictive`, no safety evals | `{"status": "written", "slug": "minimax-minimax-music-3-model-card", "document_id": 348, "version_id": 643}` |
| 7 | add: Upstage, Solar Open 2 (250B-A15B) model card (2026-07-22), Upstage Solar License, `open_weight_restrictive`, no safety evals | `{"status": "written", "slug": "upstage-solar-open-2-model-card", "document_id": 349, "version_id": 644}` |
| 8 | add: Dots Studio, dots3-note Preview model card (2026-08-14), Apache-2.0, `open_weight_permissive`, no safety evals | `{"status": "written", "slug": "dots-studio-dots3-note-preview-model-card", "document_id": 350, "version_id": 645}` |

Judgement calls:

- **Project Swap** is the sequel to Project Deal (`anthropic-claude-opus-4-5-other`). It measures named
  models as delegated agents:
  - Market efficiency by model: Haiku 0.75, Sonnet 0.80, Opus 0.88, Fable 0.86.
  - On mixed floors, Opus agents always beat Haiku agents.
  - Agent honesty: about 1 in 100 lied about their top pick.

  It is tagged `societal_harm` (inequality between principals), as the Project Deal and Project Pilot
  rows are. The canonical URL is the full PDF (same title, "Published September 24, 2026"); the research
  post is recorded as `announcement`.
- **OpenAI misalignment report.** Of the six reports on the 2026-09-16 hub, this is the only one that
  names a released model; the other five are "internal unreleased" checkpoints. One of those is an
  "Astra family" training run explicitly distinct from the deployed GPT-6 Astra, so they are not
  proposed. The hub and the openai.com framework post are recorded as related.
- **Ling/Ring-2.5-1T.** Phase A surfaced them because of 2026-09-24 card edits, but the models date
  from February, which predates monitoring. Notability comes from Ant Group's joint Business Wire
  release and FinTech Weekly coverage. Both use the press-release date 2026-02-15; HF `createdAt` is
  02-10 (Ring) and 02-14 (Ling), and one secondary source says 02-16. They are kept as separate rows,
  matching the existing Ling-2.6-1T / Ring-2.6-1T pair.
- **MiniMax H3 / Music 3** came from the silent-org sweep; MiniMax's newest row was 06-12. Video and music
  generation are both in `covered_model_class`.
  - H3 was announced 07-31 as a web launch. Its weights and card went public on 08-03, which is the
    date used.
  - Music 3 has no date on the card, so the date comes from the 08-13 research-blog announcement.
- **Upstage / Dots Studio** are OpenRouter-overlay publishers with no prior rows. See §2 for what was
  skipped.

---

## 1. Phase A candidate triage

Only links first seen at 2026-09-25T06:19Z were new; older slices were triaged by earlier runs. HF
profile pages, discussions, datasets and `huggingface.co/papers/*` are not documents.

- **Written:** `anthropic.com/research/project-swap` (#1). The InclusionAI `Ling-2.5-1T` and
  `Ring-2.5-1T` repos (#2, #4).
- **Skipped:**
  - `blog.google/.../gemini-3-8-live-with-live-avatar/` (09-24). This is a feature launch. Its "model
    card" link is the Gemini 3.8 Audio card, already `google-deepmind-gemini-3-8-live-model-card`.
  - `blog.redwoodresearch.org/p/continual-learning-might-make-your` (09-25). A conceptual essay: no
    named-model results, only a toy tabular-RL setting.
  - `nvidia/NV-Reason-CT`. A CT-imaging medical VLM (Qwen3.5-4B base), i.e. a domain task model outside
    the nvidia scope note (Nemotron/Cosmos/GR00T), with no safety evals.
  - InclusionAI `Ling-1T`, `Ring-1T`, `Ling/Ring-flash-2.0`, `Ling-mini-2.0`, `Ring-mini-2.0`,
    `Ming-UniVision-16B-A3B`. These are 2025 releases, before the scope floor; they only resurfaced
    because of card edits. Mini/flash are size variants in any case.
  - DeepSeek `api-docs` agent-integration pages, `status.deepseek.com`, and the awesome-agents GitHub
    page. These are developer docs and navigation.
  - `spaces/inclusionAI/README`, `datasets/nvidia/tuv-data`, and `huggingface.co/papers/2609.27321`.
    None of these are documents.
- **Noticed, not pursued:** Ming-Flash-Omni-2.0 (InclusionAI, 2026-02-11, named in the same Ant Group
  press coverage). The inclusion_ai scope note is "Ling/LLaDA LLM lines, flagship agents", and Ming is
  neither, so it is left out.

## 2. Targeted search (window 2026-09-22 → 2026-09-25)

`.agent_last_success` = `2026-09-24T06:27:48Z`, so the 72 h floor governs.

- **Frontier releases.** The release trackers (llm-stats, digitalapplied) show nothing after the 09-22
  cluster (Opus 5.5, GPT-6 Sol/Luna, MiMo-V2.6), all already covered. China Telecom Xing4.0-29B (09-24)
  is not allowlisted.
- **Restricted-access sweep.** Nothing new:
  - LSVP (09-17) is catalogued.
  - The Cyber Verification Program still says Mythos access will come "in the near future".
  - Glasswing expansion, Daybreak (09-03), GPT-Rosalind GA (09-11) and Fairwind (09-02) are all
    catalogued.
  - DeepMind Co-Scientist: the 05-19 access post is catalogued. The Aug-28 "Co-Scientist now plans
    experiments" expansion is a system paper built on several Gemini versions. It was not pursued
    today and is a watch item.
- **Found through the escalation check:** the OpenAI misalignment report (#3). See the `PROPOSALS.md`
  entry: the alignment.openai.com hub is not watched.
- **Anthropic Institute, *Measurements for understanding the pace of AI development inside frontier
  labs*** (Aug 2026; "Claude leads 26% of Anthropic's AI R&D"). It names no specific model, so it
  fails the named-model gate and is skipped.
- **METR watch item from yesterday.** No new public output from the separate METR team assessing AI
  R&D acceleration at Anthropic. The 09-22 Opus 5.5 summary is catalogued.
- **Silent orgs (>14 days).** A background research agent checked Palisade, MiniMax, Poolside, Apollo,
  Moonshot, Thinking Machines, SaferAI, Mistral, UK AISI, RAND, Cursor, NVIDIA and Tencent Hunyuan:
  - **MiniMax:** yielded #5 and #6.
  - **RAND RR-A5112-1** (open-weight bio misuse via anti-refusal tampering) looks in scope, but
    rand.org returns 403 to my fetcher, so I could not verify its date or named models. Not proposed;
    logged as friction and left as a lead for the next run.
  - **Tencent Hunyuan-A13B technical report** (arXiv 2609.27284, 09-23) is a late paper about a 2025
    model, which fails notability as a new release. Skipped.
  - **Kimi K2.8 Preview:** only one secondary source mentions it, with no primary document. Not pursued.
  - Everything else: nothing new.
- **OpenRouter-overlay publishers** (`upstage`, `dots_studio` from 09-22; `typesafe` new today, none
  with rows):
  - Upstage: Solar Open 2 (#7) written. Solar Pro 3 (01-26), Solar Pro 4 (08-11) and Solar Mini 4
    (around 09-22) are API-only, and their only documentation is launch posts with benchmark tables,
    treated as marketing and skipped. The Solar Open technical report (arXiv 2601.07022, 01-11) covers
    Solar-Open-100B, released around 2025-12-31; it was not pursued today.
  - Dots Studio: dots3-note Preview (#8) written; its own FP8 repo is a variant.
  - typesafe: Jev 1.13 is a non-generative "text→decisions" model, judged outside
    `covered_model_class`.

  Both skip decisions are logged as `ambiguous_criteria` friction.

## 3. Citation mining

Today is Friday, so there is no retrospective sweep. On this run's adds, Project Swap cites Project
Deal (catalogued). The misalignment report cites only the framework post, which is recorded as
related. Upstage's Solar Open 2 cites its arXiv tech report, recorded as `paper`. No new leads.

## 4. Open issues

`open_issues.json` is `[]`.

## 5. Blocked-URL escalations

Both are **alive**; no status change was proposed.

| slug | URL | finding |
| --- | --- | --- |
| `openai-gpt-5-6-sol-other` | openai.com/index/hugging-face-model-evaluation-security-incident/ | 403 to my fetcher as well (the known openai.com bot wall). The page is currently indexed under its own title, a localized copy (`/so-DJ/…`) exists, and it is cited by live follow-up posts. |
| `openai-gpt-rosalind-access-policy-3` | openai.com/index/introducing-new-capabilities-to-gpt-rosalind/ | Same: 403 to the fetcher, but currently indexed with full content, with localized copies (`/ms-MY/`, `/so-DJ/`). |

## 6. Document update summaries

**10 new diffs, 0 annotated. All are noise:**

- **HF download counters and eval-widget reordering:** Qwen3.5-397B v637, Qwen3.6-27B v636,
  Qwen3.8-2.4T v635, Nemotron-3.5-Lightning v633, Muse Glimmer v632.
- **Related-posts sidebar rotation and footnote extraction drift:** Fable-5 addendum-4 v631, Opus 4.6
  other-2 v630, Project Pilot v629.
- **Apollo o3 v628:** a sidebar retitle of a *different* note plus a "Copy as Markdown" button.
- **Ling-3.0-tiny v634:** the install instructions switched from a vLLM fork to upstream vLLM, and a
  boilerplate "training content summary" pointer was added. Both are operational notes, not changes to
  model documentation.

## 7. Friction and proposals

Three entries appended to `logs/friction.jsonl`:

- `transient_rejection`: a HuggingFace 429, for the second day running.
- `unfetchable_but_alive`: OpenAI's "Hugging Face incident and other third-party impact" page and
  RAND RR-A5112-1, both unread because of 403s.
- `ambiguous_criteria`: API-only launch posts from overlay publishers, and TypeSafe's non-generative
  model.

One `PROPOSALS.md` entry: add `alignment.openai.com/misalignment-reports/` to OpenAI's `index_urls`,
plus a minor request to retry on 429 before rejecting.

Proposal JSON was staged in `/tmp/cardtrack_p*.json` and passed with `--json <path>`, because stdin
heredocs are blocked by the shell sandbox. The rolling cap did not bind.
