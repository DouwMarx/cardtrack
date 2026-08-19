# cardtrack run report — 2026-08-19T06:17Z-local

**Corpus at start:** 230 documents (226 active, 3 removed, 1 moved). **Written this run:** 6 adds
(ids 231–236) and 1 field update (id 229). **Proposals rejected or filed as issues:** none.
**Open issues:** none. **Blocked-URL escalations:** none.

## Phase A worked

`checked: 227, ok: 227, not_found: 0, blocked: 0, errors: 0, moved: 0, marked_dead: 0,
fingerprint_checked: 35, new_versions: 21, candidates: 2639, candidates_new: 26`. First clean run
since 2026-08-13 — the total-outage failure logged on 08-14, 08-15, 08-16 and 08-18 did not recur,
and every one of the 43 index pages diffed. All 26 new candidates are triaged below, so unlike the
last four runs nothing here came from a hand sweep.

Caveat carried forward, not re-filed: `new_versions: 21` against `fingerprint_checked: 35` is the
same ratio that the 2026-08-17 friction line
(`fingerprint_counts_page_furniture_as_revision`) established is mostly HuggingFace download
counters and related-post strips, not document revisions. Nothing new to add to that finding.

## Added (6)

### Anthropic's protein design and analytical chemistry release — 3 documents (ids 231–233)

Anthropic published one announcement plus two technical reports on 2026-08-18. All three were
fetched and read in full; the two PDFs were downloaded and text-extracted.

| id | document | date | verdict |
|---|---|---|---|
| 231 | [Autonomous de novo protein binder design with Claude](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf) — 29 pp technical report, Opus 4.8 + Mythos Preview | 2026-08-18 | `{"status": "written", "slug": "anthropic-claude-opus-4-8-other", "document_id": 231, "version_id": 303}` |
| 232 | [Automated processing of raw NMR and LC-MS data with Claude Opus 5](https://www-cdn.anthropic.com/9f08da5189ac269b3242ca760de9823805c3f5f6.pdf) — 9 pp technical report | 2026-08-18 | `{"status": "written", "slug": "anthropic-claude-opus-5-other", "document_id": 232, "version_id": 304}` |
| 233 | [How Claude is accelerating protein design and analytical chemistry](https://www.anthropic.com/research/Claude-accelerates-protein-design) — the announcement | 2026-08-18 | `{"status": "written", "slug": "anthropic-claude-opus-4-8-other-2", "document_id": 233, "version_id": 305}` |

Why three rows rather than one. The two PDFs are separately authored (Amir Shanehsazzadeh; David
Kamber), separately dated, live at their own URLs, and contain the methods and results the post
only summarises. The announcement is precedented independently: the corpus already catalogues
Anthropic `/research/` evaluation posts including `making-claude-a-chemist` (2026-06-05), which is
a near-twin of id 232's subject. Each row's `notes` cross-references the other two.

Substance, since it is the strongest capability result in the corpus this month: Opus 4.8 and
Mythos Preview ran 24–48 h autonomous binder-design campaigns against 16 targets from a single
protocol prompt with **no human input into any design decision**; Adaptyv Bio and Twist Bioscience
independently synthesised and measured every design. 354 of 1,320 designs bound (27%) against 14
of 15 interpretable targets, versus a 10–15% field baseline; 49% of first-ranked designs bound. On
RBX1, 28 of Claude's 90 designs bound where an open competition managed 9 of 245, tightest at
K_D 3.9 nM against the winning entry's 45 nM on the same plate. Separately, Opus 5 processed a
contract lab's raw NMR and LC-MS files from a two-sentence prompt in 23 and 19 minutes, agreeing
with the lab's own operator within 0.08 ¹H and reporting 96.4% purity against the lab's 96.33%.

**The `has_safety_evals` split is the judgment call worth challenging in this run.** I attested
`true` for the announcement and `false` for both technical reports. The announcement carries an
explicit section — "Agentic biological discovery is dual-use" — stating the capability could
"enable bad actors to perform dangerous research, such as the development of bioweapons", that
protein design remains unavailable in Claude Fable 5 and blocked in the most capable model, and
that a gated scientist access program is planned. The 29-page report carries none of that: grep
for dual-use, biosecurity, misuse, bioweapon or safeguard returns nothing. So by the letter of the
criterion the document holding the actual dangerous-capability numbers scores `false` while the
blog section about it scores `true`. I attested what each document contains rather than what it is
about, which is what the criterion asks — but the result is perverse enough that I raised it in
`logs/PROPOSALS.md` §3 and `logs/friction.jsonl`. If a reviewer disagrees, id 231 is the row to flip.

### Citation mining found a six-month coverage hole at Qwen — 2 documents (ids 235, 236)

| id | document | date | verdict |
|---|---|---|---|
| 235 | [Qwen3.6-27B model card](https://huggingface.co/Qwen/Qwen3.6-27B) | 2026-04-21 | `{"status": "written", "slug": "alibaba-qwen-qwen3-6-27b-model-card", "document_id": 235, "version_id": 307}` |
| 236 | [Qwen3.5-397B-A17B model card](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | 2026-02-16 | `{"status": "written", "slug": "alibaba-qwen-qwen3-5-397b-a17b-model-card", "document_id": 236, "version_id": 308}` |

Mining base-model citations out of the two Tencent cards added on 08-14 and 08-17 led to both:
`UI-Mate-27B` cites `Qwen/Qwen3.6-27B`, `EVIE-Preview-4.5B` cites `Qwen/Qwen3.5-4B`. Neither was in
the corpus — and following the second showed **the entire Qwen3.5 generation is missing**, eight
post-trained sizes released 2026-02-16 to 2026-02-28, the 9B alone at 13.8M downloads.
`huggingface.co/Qwen` is a configured index page that has been fetched successfully every run; it
was missed because index diffing only ever sees *new* links, and a February release stopped being
a new link in February.

I proposed the Qwen3.5 flagship and Qwen3.6-27B and **deliberately left the seven Qwen3.5 siblings
unproposed**, because I could not determine how many rows they should be and did not want to commit
a generation to a guess in a daily run. The criteria say size variants don't qualify and family
cards collapse to one entry — but there is no family card here, each size has its own card with its
own architecture and benchmark tables, and the corpus's own precedent points the other way, holding
`Qwen3.8-27B` and `Qwen3.8-2.4T-A95B` as two separate rows for exactly this dense/MoE pairing one
generation later. Qwen3.6-27B was safe to propose because that precedent is direct. Both problems —
the undetectable coverage hole and the row-granularity contradiction — are written up in
`logs/PROPOSALS.md` §1 and §2, with a suggested HuggingFace-API reconciliation pass that would have
caught this in February.

### NVIDIA (id 234)

| id | document | date | verdict |
|---|---|---|---|
| 234 | [Context-Matched Distillation (CMD) model card](https://huggingface.co/nvidia/cmd) | 2026-08-13 | `{"status": "written", "slug": "nvidia-context-matched-distillation-cmd-model-card", "document_id": 234, "version_id": 306}` |

Six safetensors checkpoints (chunk-1/chunk-4 × short/long/camera-control) distilled from
Cosmos-Predict2.5 2B by NVIDIA Toronto AI Lab with Surrey's SketchX; NVIDIA OneWay Noncommercial
License, so `open_weight_restrictive`. Repo created 08-13, card revised 08-18, which is why it
surfaced now. Flagging honestly that this is the weakest `notable_release` attestation of the six:
**0 downloads and 7 likes**, and no NVIDIA blog announcement. It rests on being a first-party card
in NVIDIA's standard template with paper and code behind it, consistent with corpus precedent for
NVIDIA research releases (`LocateAnything-3B`, `Lyra-2.0`). Cosmos-Predict2.5 is not itself in the
corpus, so this is not a variant of a covered model. Easy revert if that reading is too generous.

## Field update (1)

`tencent-hunyuan-ui-mate-27b-model-card` (id 229), `model_names`
`["UI-Mate-27B", "UI-Mate-9B"]` → `["UI-Mate-27B", "UI-Mate-9B", "UI-Mate-democua-27B"]`.
Verdict: `{"status": "written", "slug": "tencent-hunyuan-ui-mate-27b-model-card", "document_id": 229}`.

`tencent/UI-Mate-democua-27B` appeared in today's index diff as its own repo (created 2026-08-14,
same release day, Apache-2.0). I fetched the family card and confirmed its Model Details table
lists three checkpoints, not two — UI-Mate-27B, UI-Mate-9B and UI-Mate-democua-27B
("demonstration-guided computer use"). It is a checkpoint variant, so under the family rule it does
not warrant its own row; it belongs in this one. Correcting the row also stops the repo being
re-triaged as uncatalogued on every future run.

## Checked and deliberately not proposed

- **Anthropic, Claude Opus 5 System Card at `…/b514064a…pdf`** — Phase A surfaced this from
  `/transparency/model-report`, which independently confirms yesterday's finding: the corpus row
  points at `…/c5fbac3f…pdf` (193 pp) while the transparency page now links a 194-pp file. I
  word-diffed both yesterday; repagination only, no content change. No proposal is possible —
  `new_version` rejects a URL not already on the document and a `canonical_url` update requires a
  fingerprint match that a revision by construction breaks. Already written up in `PROPOSALS.md`
  (2026-08-18); not re-filed.
- **`nvidia/Nemotron-Labs-Audex-2B`** — fetched; it is a compact dense variant trained on the same
  recipe as Audex-30B-A3B, same 2026-06-08 release. Already present in the existing row's
  `model_names`. Nothing to do.
- **`tencent/UI-Mate-9B`** — likewise already in id 229's `model_names`.
- **arXiv 2608.16393, "Security Assessment of DeepSeek Harness with A.I.G"** (submitted 08-17,
  revised 08-18) — the closest call among the skips. It is a real quantitative security evaluation
  (14,560 controlled executions, 16 indirect-content channels, 12 attack methods; peak attack
  success rates 25.5%, 17.0%, 16.0%), and indirect-prompt-injection resistance results would fit a
  system card's safety section. Skipped on three grounds: it assesses an agent *harness*, not a
  named model; it is an arXiv preprint rather than any allowlisted org's own publication surface,
  and the corpus holds **zero** arXiv URLs across 236 documents, so admitting one would set a new
  precedent unilaterally; and although it surfaced via `huggingface.co/tencent` and uses Tencent's
  AI-Infra-Guard, I could not confirm the authors' affiliation, so I could not attest a publisher
  without risking filing one org's work under another's key.
- **RAND ×4** — `RRA4999-1` (defence-in-depth biosecurity strategy), `PEA4952-1` (mirror biology
  governance), `RRA5043-1` (US/China AI developer firm dataset), `RRA5083-1` (PPE prioritisation).
  All fetched. Policy, governance and ecosystem research; none evaluates a named model, and RAND's
  allowlist entry is scoped to CAST / Project Canary eval output. Plus one pagination link.
- **METR, "Funding update"** (2026-08-14) — organisational announcement, no model content.
- **Cursor, "Git at any scale"** and the `origin-code-hosting` changelog — engineering essay and
  product changelog. Out of scope by the `other` scope-discipline rule.
- **HF `/papers/` links** (CoinVE-200K dataset, UniProbe hallucination detector), four `/discussions/`
  threads, five org-member profile pages, `datasets/nvidia/simready-dsx` — page furniture, method
  papers and a dataset.

## Targeted search and silent-org audit

Searches for documentation published in the last ~72 hours surfaced nothing from any allowlisted
publisher beyond the Anthropic release above. `deploymentsafety.openai.com` still lists nothing
newer than the 2026-08-06 GPT-5.6 August update, so **GPT-5.6-Cyber's promised full system card
has still not appeared — fifth consecutive run noting this**. `anthropic.com/system-cards` lists no
card the corpus lacks. A HuggingFace-API sweep by creation date across nine orgs found no
uncatalogued release other than `nvidia/cmd`: everything newer at Qwen, DeepSeek, Moonshot,
StepFun, InclusionAI, Xiaomi, Mistral and Tencent is an FP8/INT4/GGUF/NVFP4 re-upload, a
speculative-decoding drafter, or already held. Web search confirmed Qwen3.8-27B (2026-08-14 press
coverage) is the corpus's existing 2026-08-05 row, and GLM-5.3 remains out of scope (Z.ai is not
allowlisted).

Orgs silent >14 days, all re-checked and genuinely quiet: xiaomi (114 d), palisade_research
(104 d), stepfun (88 d), poolside (37 d), cursor (36 d — today's two links are not documentation),
metr (29 d — today's link is a funding note), apollo_research (29 d), us_caisi (27 d), moonshot_ai
(23 d), far_ai (21 d), thinking_machines / redwood_research / epoch_ai (19 d), saferai (17 d),
uk_aisi and mistral (15 d).

## Citation mining

Mined the outbound references of the four most recent adds — `tencent/UI-Mate-27B`,
`tencent/EVIE-Preview-4.5B`, `nvidia/NVIDIA-Nemotron-Labs-Teacher-General-Reasoning` — plus the
reference list of today's 29-page protein-design report. Yield: the two Qwen cards above. The
protein-design report's references are protein-design literature end to end, with no model card or
third-party evaluation among them; the Nemotron Teacher card's links are training-data corpora.

## Issues and escalations

`logs/open_issues.json` is `[]` and `blocked_escalations` is empty — nothing to investigate, no
comments posted. Phase A reached GitHub cleanly this run, so the empty list is trustworthy.

## Friction and proposals

Three friction lines appended: `has_safety_evals_undefined_for_dual_use_capability_report`,
`family_row_granularity_ambiguous_for_multi_size_open_weight_releases`,
`index_diff_structurally_blind_to_backlog_gaps`. One dated `PROPOSALS.md` entry with three sections
covering the coverage-reconciliation gap, the row-granularity contradiction, and the
`has_safety_evals` framing problem.
