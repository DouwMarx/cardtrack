# cardtrack run report — 2026-08-20T06:18Z-local

**Corpus at start:** 236 documents (232 active, 3 removed, 1 moved). **Written this run:** 3 adds
(ids 237–239). **Proposals rejected or filed as issues:** none. **Open issues:** none.
**Blocked-URL escalations:** none.

## Phase A worked

`candidates: 2661, candidates_new: 24`, `blocked_escalations: 0`, `open_issues: []`. Second clean run
in a row. All 24 new links are accounted for below. The 08-19 batch was fully triaged by yesterday's
run and is not re-litigated here.

## Added (3) — NVIDIA's surgical robotics programme, missing for three to five months

Every card below was fetched and read in full, and the HuggingFace commit history checked to date the
document rather than the repository.

| id | document | date | verdict |
|---|---|---|---|
| 237 | [GR00T-H-N1.7 model card](https://huggingface.co/nvidia/GR00T-H-N1.7) | 2026-05-30 | `{"status": "written", "slug": "nvidia-gr00t-h-n1-7-model-card", "document_id": 237, "version_id": 327}` |
| 238 | [GR00T-H model card](https://huggingface.co/nvidia/GR00T-H) | 2026-03-15 | `{"status": "written", "slug": "nvidia-gr00t-h-model-card", "document_id": 238, "version_id": 328}` |
| 239 | [Cosmos-H-Surgical-Simulator model card](https://huggingface.co/nvidia/Cosmos-H-Surgical-Simulator) | 2026-03-15 | `{"status": "written", "slug": "nvidia-cosmos-h-surgical-simulator-model-card", "document_id": 239, "version_id": 329}` |

**How these surfaced, which is the story of the run.** `nvidia/GR00T-H` appeared in today's index diff
for one reason: someone edited its README three times on 2026-08-19. The model itself shipped in March.
Following that edit led to the whole NVIDIA-Medtech surgical line — the N1.7 successor and the
companion world model — none of it catalogued, all of it on `huggingface.co/nvidia`, a configured index
page fetched successfully every run, alongside eight NVIDIA robotics rows the corpus already holds.
That is yesterday's Qwen3.5 finding recurring at a second publisher within 24 hours; see §3 of the
`PROPOSALS.md` entry below.

**Substance.** GR00T-H-N1.7 is a vision-language-action model post-trained from Isaac GR00T N1.7
(Cosmos-Reason2-2B backbone) on the Open-H Embodiment dataset: 770 hours, 124,019 episodes,
119 datasets, 20 robot platforms, 50+ institutions in the full corpus, of which a 601-hour real-world
surgical subset across 7 platforms was used for post-training, with the CMR Versius contribution capped
at 20% of training steps. Its predecessor GR00T-H (March, base GR00T-N1.6-3B, 601.5 h / 58 datasets /
35 institutions) is research-only under the NVIDIA OneWay Noncommercial License; N1.7 carries the
NVIDIA Open Model License and was covered independently as the first commercially licensed surgical VLA
foundation model. Cosmos-H-Surgical-Simulator is the evaluation environment for the same programme: a
kinematic action-conditioned world model fine-tuned from Cosmos-Predict2.5-2B that takes a context
frame plus twelve 44-dimensional action vectors and predicts twelve frames, rolled out autoregressively
into full surgical trajectories. It is the only one of the three carrying its own metrics — aggregate
Frame Decay Score 0.184, tool consistency 0.472, tool centroid distance 67.03 px for the April 2026
checkpoint, broken down per procedure across prostatectomy, hernia, hysterectomy and cholecystectomy.

**`has_safety_evals` false on all three, and that is the finding.** These are models intended to drive
robot arms inside patients. Between the three cards the entire safety content is a boilerplate
Ethical Considerations paragraph, an intended-use disclaimer, and a Safety & Security subcard that is a
four-row questionnaire — its life-critical-application row reads "not tested or intended for clinical
or mission critical applications that require functional safety … Any real-world use requires
independent safety review and regulatory clearance". No quantitative safety evaluation, no red-teaming,
no risk assessment. Recorded honestly as absence, which is what the flag is for.

**Two judgment calls flagged for reversal if wrong.** (1) I proposed GR00T-H and GR00T-H-N1.7 as two
rows rather than one, on different base models and different licenses; the project's own README lists
them as two Model Variants on separate branches. That splits the same way the corpus does *not* treat
NVIDIA's Nemotron Teacher family — see the proposals entry. (2) GR00T-H (id 238) is the weakest
`notable_release` attestation of the three: superseded, research-only, 320 downloads and 20 likes. It
rests on the first-party announcement in the NVIDIA-Medtech News section and GTC-2026-era press
coverage of the surgical GR00T line. Easy curate-out if that is too generous.

`openness=open_weight_restrictive` on all three: weights are public, but under the NVIDIA Open Model
License or the OneWay Noncommercial License, neither of which is Apache/MIT/BSD-class. This matches the
corpus's existing treatment of `nvidia/Cosmos-H-Dreams`.

## Checked and deliberately not proposed

- **`nvidia/NVIDIA-Nemotron-Labs-Teacher-{Chat,Competition-Coding,Instruction-Following,STEM}`** — a
  HuggingFace-API sweep found four siblings of the corpus's General-Reasoning row, all created
  2026-08-14, none held as its own row. I fetched and diffed all five cards (~83 KB each; genuinely
  distinct descriptions, training narratives and benchmark tables) and was ready to propose four adds.
  I did not, because reading the database directly showed id 225 already lists all five in
  `model_names`, with its `notes` claiming the four sibling URLs as covered. That decision is recorded
  only as prose inside one row and is not visible in `state_summary.json` — this is a near-miss for
  four duplicate proposals, and it is §1 of today's proposals entry.
- **Transluce, "Scaling Laws for Exact String Elicitation"** (2026-08-19) — the closest call of the
  run, and the only allowlisted-evaluator publication in the window. It trains oversight models at five
  Qwen3.5 sizes to recover prompts producing exact target responses from Qwen3.6-27B, fits joint power
  laws, and extrapolates 4×10²⁵ FLOPs (~$52M) in-distribution and 3×10²⁹ (~$376B) out-of-distribution
  to match gold prompts, with OOD generalisation shown on WeirdChat prompts that elicit harmful
  responses. Skipped: the reported numbers describe the elicitor's learning curve, not Qwen3.6-27B's
  capabilities or safety, so it falls under the criterion's carve-out for research that merely uses
  models. Flagging that the corpus holds `transluce.org/weirdchat` as an eval of a named model on
  similar-looking grounds; the discriminator I used is written up in §2 of the proposals entry. If a
  reviewer reads it the other way, this is the row to add.
- **InclusionAI Ling-3.0 base checkpoints ×6** (`Ling-3.0-{flash,tiny}-base`, `-base-30T`,
  `-base-midtrain`) — fetched. The six share one card that states outright they are "a collection of
  checkpoints during the training process" (pretrained / mid-trained / WSM-merged) for
  `Ling-3.0-flash` and `Ling-3.0-tiny`, both already in the corpus, and directs readers to those rows
  for the post-trained models. Textbook checkpoint variants; excluded by `distinct_model_release`.
  Clean skip, no ambiguity.
- **`nvidia/Kimi-K3-NVFP4`, `Qwen/Qwen3.8-27B-FP8`** — quantization re-uploads of covered models.
- **`nvidia/Nemotron-Labs-Audex-2B`, `tencent/UI-Mate-9B`, `tencent/UI-Mate-democua-27B`** — re-checked
  and confirmed already inside existing rows' `model_names`; no action, same as yesterday.
- **xAI, "Grok 4.6 on Amazon Bedrock"** (2026-08-19) — availability announcement for a model whose card
  the corpus already holds. Out of scope by the `other` scope-discipline rule.
- **Cursor changelog `08-19-26`** ("Cloud Agents and Cursor Harness Improvements") — product changelog.
- **Anthropic `academy.claude.com`, `/company/leadership`** — site navigation.
- **HF `/papers/2608.13580` (Jais 2)** — surfaced under the `alibaba_qwen` index but is an unaffiliated
  Arabic-centric model paper; proposing it under Qwen's publisher key would file one org's work under
  another's. Not proposed, per the co-publication rule.
- **HF collections (`nvidia/earth-2`, `nvidia-aerial`, `inclusionAI/ling-30`), `datasets/nvidia/aerial-isac-srs-iq`, three `/discussions/` threads, four org-member profile pages** — page furniture.

## Targeted search and silent-org audit

Nothing published in the last ~72 hours by any allowlisted publisher qualified beyond the Transluce
post above. Checked directly: `deploymentsafety.openai.com` (most recent entry still GPT-5.6 August
Updates, 2026-08-06 — **GPT-5.6-Cyber's promised full system card has still not appeared, sixth
consecutive run noting this**); `anthropic.com/transparency/model-report` (most recent is the Opus 5
card the corpus holds); `aisi.gov.uk/work` (most recent is the 2026-08-04 incident report, already
id-matched in the corpus); `epoch.ai/gradient-updates` (two August posts, 2026-08-12 and 2026-08-14,
both general analysis with no named model evaluated); `securebio.substack.com/archive` (nothing since
the 2026-08-07 Kimi K3 assessment, already held). A HuggingFace-API sweep by creation date across ten
orgs (Qwen, DeepSeek, Moonshot, StepFun, InclusionAI, Xiaomi, Mistral, Tencent, NVIDIA, Meta) returned
nothing uncatalogued except the four Nemotron Teacher siblings resolved above.

Orgs silent >14 days, carried forward from yesterday's sweep with today's counts: xiaomi (115 d),
palisade_research (105 d), stepfun (89 d), poolside (38 d), cursor (37 d), metr (30 d),
apollo_research (30 d), us_caisi (28 d), moonshot_ai (24 d), far_ai (22 d), redwood_research (20 d),
thinking_machines (20 d), epoch_ai (20 d — re-checked directly today), saferai (18 d), uk_aisi and
mistral (16 d — both re-checked directly today). No new publication found at any of them.

## Citation mining

Mined the outbound references of yesterday's six adds. `nvidia/cmd` cites `Cosmos-Predict2.5-2B` —
fetched, but created 2025-07-23, below the 2026-01-01 scope floor, so out of scope; noted rather than
proposed. The two Qwen cards (ids 235, 236) reference only inference tooling, vLLM/SGLang pull
requests and the Qwen blog, no model documentation the corpus lacks. The Anthropic protein and NMR
reports were mined yesterday. The productive thread this run was not a citation but a README edit; see
the Added section.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty. Nothing to investigate, no comments
posted, no `status_change` warranted.

## Friction and proposals

Three friction lines appended: `index_diff_structurally_blind_to_backlog_gaps` (second instance in two
runs, at a second publisher), `family_row_granularity_ambiguous_for_multi_size_open_weight_releases`
(recurrence, now with the corpus holding both answers), and a new
`system_card_test_ambiguous_for_methods_papers_with_named_subject_model`.

One dated `PROPOSALS.md` entry with three sections: the row-granularity inconsistency now visible
inside the corpus and buried in one row's `notes`; the unwritten discriminator in the system-card test;
and confirming evidence for yesterday's coverage-reconciliation proposal that asks for nothing new.
