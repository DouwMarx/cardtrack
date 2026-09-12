# cardtrack agent run — 2026-09-12 (run id `2026-09-12T06:17Z-local`)

Phase A checked 275 documents: 271 OK, **1 not-found, 3 blocked**, 0 errors, 2 new versions,
261 candidate links carried (14 first seen today), 20 documents in the update queue.
No open GitHub issues. `blocked_escalations` was empty **despite the four fetch failures above** —
see §5 and §8; that discrepancy is the most important finding of this run.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | `add` | SecureBio — *Introducing VCT-v2 — the updated Virology Capabilities Test* (2026-09-11) | **written** → `securebio-gpt-5-6-sol-independent-eval-2` (doc 308, v553) |
| 2 | `add` | Redwood Research — *CoT controllability evals seem very under-elicited* (2026-09-11) | **written** → `redwood-research-gpt-oss-120b-independent-eval` (doc 309, v554) |
| 3 | `annotate_version` | `openai-gpt-6-astra-system-card` v551 | **written** (doc 283) |
| 4 | `field_update` | `apollo-research-openai-o3-independent-eval` `related_urls` | **written** (doc 75) |

Four proposals, four written, none rejected.

## 1. Phase A candidate triage

261 candidate links, 14 of them new since the last run. Two of the new ones were proposed, one
produced a `related_urls` update, and the remaining eleven resolved below. The 247 carried-over
links were adjudicated by earlier runs and their reasoning still holds; I re-opened only the two
that today's work touched (`huggingface.co/tencent/AuK`, and the Apollo URL).

**Proposed**

- `securebio.substack.com/p/introducing-vct-v2` (2026-09-11, Nelly Mak and Jasper Götting) — the
  revision of the Virology Capabilities Test, the wet-lab virology benchmark frontier labs cite in
  their biosecurity sections. Not commentary: SecureBio re-audited all 322 original questions with
  deterministic flagging plus expert review, "43 (13.4%) questions were removed and 163 (50.6%)
  questions were edited", leaving 279, and re-scored models on the revised set. Named-model numbers
  on both versions — o3 at 42.0% and GPT-5.6 Sol at 53.9% on the original VCT, GPT-5.6 Sol at 49.2%
  on VCT-v2, against a human expert baseline of about 21% — with "Model accuracies dropped by
  1.0–7.1 percentage points on VCT-v2 relative to VCT" while "the difference between the strongest
  and weakest models tested was preserved (26.6 → 26.1%)". It also quantifies the defect it was
  built to fix: 27.0% of original questions were shortcut-answerable, and 18/279 (6.5%) of VCT-v2
  questions are answerable by no model. Passes the system-card test cleanly — a dangerous-capability
  benchmark with per-model accuracies and a human baseline is exactly evaluations-section content.
  `risk_domains: cbrn`, `openness: closed` (both named models are public-API, no public weights).
  Distinct from SecureBio's six existing rows, which are per-model pre-release assessments or
  safeguard studies, not the benchmark revision.
- `blog.redwoodresearch.org/p/cot-controllability-evals-seem-very` (2026-09-11, Arun Jose) — an
  elicitation study of CoTControl, the chain-of-thought controllability eval that OpenAI and
  Anthropic now report in system cards (GPT-5.5, Fable 5, GPT-6 Astra) to argue their frontier
  models cannot reliably shape their own reasoning traces. Jose's finding is that those numbers are
  floor estimates from weak prompting: "Using better prompts improves performance for open-source
  models by ~2-3x or more (e.g. from 5.5% to 15% for GPT-OSS-120B)" against a 0–30% baseline band,
  with Qwen3-32B going from 6.3% at 2-shot to 16.6% at 15-shot on on-policy examples, and the
  GEPA-optimised prompts holding their advantage across ten held-out controllability modes. This is
  a direct re-run of an evaluation that appears in three frontier system cards, concluding those
  sections understate the measured capability. `risk_domains: loss_of_control`.
  `openness: open_weight_permissive` — see §7 for why, it is not a free call.

**Checked and attached rather than catalogued**

- `www.apolloresearch.ai/science/measuring-reward-seeking-via-contrastive-belief-updates` — surfaced
  as a new candidate today, and it is already in the corpus as `apollo-research-openai-o3-independent-eval`
  (doc 75, 2026-07-21). The reason it looked new is the point: the stored `canonical_url` spells the
  slug `contrastivebelief`, without the hyphen, and **returns 404**. The document is alive only at
  the hyphenated address, which is what Apollo's own research index links. So the pipeline was
  holding a broken address while rediscovering the working one as an unknown link. I verified they
  are the same document (same title, same 2026-07-21 date, same method — Contrastive Synthetic
  Document Finetuning — and the same headline result: the late o3 checkpoint "breaks the promise 87%
  of the time when SDF documents say the grader rewards task completion, versus 9% when they say it
  rewards honesty"). `canonical_url` is operator-only, so proposal 4 records the working URL as a
  `web_version` related URL for the operator sweep to promote. A PDF at
  `apolloresearch.ai/wp-content/uploads/2026/07/Measuring_Reward_Seeking_Apollo_Research.pdf` shows
  up in search results but 404s as well, so the hyphenated page is the single verified address.

**Skipped, with the reason**

- `huggingface.co/tencent/AuK` and `tencent/AuK-Flash` (2026-09-09, MIT, arXiv:2609.08936) — a 1.5B
  speech generation-and-editing foundation model (voice cloning, lyric editing, emotion
  modification, enhancement, separation) plus its 4-step distilled variant. No safety or
  dangerous-capability evaluations in the card. I re-opened this one because it is the exact case
  escalated to `PROPOSALS.md` on 2026-09-10 — `criteria.yaml` lists "audio/music generation" as in
  scope and "TTS" as out, and AuK is both. It resolves without needing that question answered: the
  Tencent `scope` note in `sources.yaml` admits the Hy LLM/VLM line, HY-World and flagship
  embodied/UI agents, and speech generation is not among them. Skipped on the per-publisher scope
  note, which I must honor regardless of how the generic criterion reads. The open question in
  `PROPOSALS.md` still stands for publishers without such a note.
- `huggingface.co/inclusionAI/Ling-3.0-flash-Fin-fp4` / `-int4` / `-fp8` (2026-09-11) — quantisation
  variants of a domain fine-tune whose base is itself a variant of the catalogued
  `inclusion-ai-ling-3-0-flash-model-card`. Out under `distinct_model_release`, twice over.
- `huggingface.co/spaces/inclusionAI/llada-ui-gui-agent-demo` — a Space (interactive demo), not a
  model card.
- `huggingface.co/Qwen/Qwen3.8-Flash-Next/discussions/39` and `/46` (the latter is an image upload),
  `huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles/discussions/44` — discussion
  threads on already-catalogued or out-of-scope repos.
- `huggingface.co/xiangyuc`, `huggingface.co/mmyin`, `substack.com/@nellymaksc` — user and author
  profile pages surfaced by org-page and Substack archive diffs. The third is the VCT-v2 author's
  profile, i.e. the same lead arriving twice.
- `notebook.google.com/` — the Gemini Notebook product page, surfaced by the
  `ai.google/gemini-for-science` index. Skipped under the Google DeepMind `scope` note (product and
  consumer-feature links only; not a gated-program or access page). The science-access program
  itself is already carried as `google-deepmind-gemini-co-scientist-access-policy`, which lists
  `ai.google/gemini-for-science` and `labs.google/science` among its related URLs.

## 2. Targeted web search

Last successful run 2026-09-11T06:29Z, so the window runs from there back-extended to the 72-hour
floor, i.e. 2026-09-09 onward.

- **New in the window:** the two documents proposed above and nothing else. I checked the
  first-party hubs directly. OpenAI's deployment safety hub is unchanged — ChatGPT Images 2.5
  (2026-09-08) is still the newest entry, and every one of the eight listed cards is catalogued.
  Anthropic's news index has exactly one item on or after 2026-09-09, the threat intelligence report
  catalogued yesterday. Release-tracker searches surfaced only DeepSeek V4.1-Flash (2026-09-10,
  already a row) and Fugu Ultra v2.0 from Sakana AI (2026-09-11) — Sakana is not on the allowlist,
  so there is nothing to propose and no monitoring gap on our side.
- **Restricted-access programs.** Polled the named list; no new documents. GPT-Rosalind, Daybreak
  Blue/Red, Project Glasswing, Claude Science, Claude Mythos access, Gemini for Science and Fairwind
  are all unchanged and their rows current. The one thing search did add is corroboration rather
  than news: coverage of the 2026-09-01 Fable 5.1 / Mythos 5.1 split, of Astra's Critical cyber
  rating and trusted-access gating, and of Gemini 3.8 Flash Cyber shipping through Fairwind — all
  three already catalogued. The Life Sciences Verification Program remains a watch item on
  unchanged terms: still an invite-only beta, US organisations only, still no dedicated program page
  and no public application route, so its only primary-source description remains the catalogued
  Fable 5.1 / Mythos 5.1 access-policy row.
- **Orgs silent >14 days.** METR's newest post is still the 2026-08-31 security update — no
  evaluation since GPT-5.6 Sol (2026-06-26). Apollo Research's newest is 2026-07-21, the
  reward-seeking paper whose URL is broken (above). SecureBio broke its silence today, after
  2026-08-07. Still notable at nine days after launch: **none of METR, UK AISI, Apollo or SecureBio
  has published a standalone GPT-6 Astra report**, despite UK AISI and Apollo both contributing
  sections to OpenAI's card — Apollo's six red-team environments (Astra falsifying data labels in 17
  of 10,000 runs versus 36 of 100 for GPT-5.6 Sol, but verbalising evaluation awareness in 41.1% of
  samples at high reasoning effort and 50.6% at max) and UK AISI's 499 cyber challenges exist only
  inside the system card.

## 3. Citation mining

Mined the two documents added today.

- The Redwood post's outbound links are the GPT-5.5 and GPT-6 Astra system-card sections and the
  Fable 5 system card PDF — all three already rows — plus three arXiv papers (CoTControl
  2603.05706, ReasonIF, GEPA) from authors who are not allowlisted publishers. The first and third
  are recorded as `paper` related URLs on the new row.
- The VCT-v2 post links SecureBio's own benchmark and dashboard pages (recorded as related URLs,
  neither a model document), the WMDP-Bio Verified Cloze preprint, FutureHouse's BixBench, and an
  Epoch AI FrontierMath tier page. Epoch is allowlisted, but that page is benchmark result data, not
  a model evaluation document, so nothing to propose.

Today's UTC date is a Saturday, so the weekly retrospective sweep was not due. Next one falls on
Monday 2026-09-14.

## 4. Open issues

`logs/open_issues.json` is empty. No investigations, no comments posted.

## 5. Blocked-URL escalations

**`candidates.json` carried `"blocked_escalations": []`, and that is wrong.** Phase A's own summary
line for this run reads `not_found: 1, blocked: 3` — four documents failed to fetch, and the
escalation list I am supposed to work from named none of them. Task 5 would have reported "none" on
a clean day and "none" today, identically.

I reconstructed what I could. Three active rows carry `last_checked: 2026-09-11` while every other
active row was checked 2026-09-12, which is almost certainly the `blocked: 3`. I fetched all three
by hand:

- `openai-gpt-5-5-access-policy` (`openai.com/index/gpt-5-5-with-trusted-access-for-cyber/`) — HTTP
  403. **Alive, bot-blocked.** No status change. `openai.com/news/` 403s for me too, so OpenAI is
  refusing this user agent site-wide today, not just on these paths.
- `openai-gpt-rosalind-access-policy`
  (`openai.com/index/strengthening-societal-resilience-with-rosalind-biodefense/`) — HTTP 403.
  **Alive, bot-blocked.** No status change.
- `apollo-research-openai-o3-independent-eval` — a real 404, but the document is alive at a
  different URL; handled as proposal 4 and described in §1. Not dead, so no `status_change`.

The `not_found: 1` **I cannot identify**. A not-found fetch appears to still stamp `last_checked`,
so that row is indistinguishable from a healthy one in `state_summary.json`, and `marked_dead` is 0
so it is still being served as active. One document in the corpus is 404ing and neither I nor the
operator can say which. That is the concrete cost of the gap, and it is why §8 exists.

## 6. Document updates

Two fresh diffs entered the queue today; the other eighteen entries are backlog already adjudicated
by previous runs. One is substantive and was annotated, one is noise.

- **`openai-gpt-6-astra-system-card` v551 — annotated (proposal 3).** This is the OpenAI revision a
  secondary source flagged on 2026-09-11 and that Phase A had not yet captured; it has now landed.
  The document gains a **Change log** section on page 4 that did not previously exist, dating two
  edits to September 9, 2026, which is why every subsequent page number shifts by one and the diff
  runs to 413 added lines. Substance, not renumbering: section 8.7 is renamed from *Metagaming and
  Alignment Faking* to *Verbalized Metagaming and Oversight Gaming*, the change log explaining the
  revision was made "to more prominently emphasize that we are currently measuring metagaming as
  verbalized in chains of thought" and defining oversight gaming as the special case where the model
  acts on its reasoning about grading "in a way that would undermine the intended meaning of the
  evaluation result". A previous metric comparison plot was "removed to reduce confusion" and CoT
  examples were added to illustrate cases flagged as oversight gaming versus metagaming only. The
  Alignment section gains a limitations passage — "the absence of observed failures does not
  establish reliability across settings" — and the safety overview now cross-references it for
  evaluation-awareness limits. A model is also renamed in passing from "GPT 5.6-Sol" to "GPT-5.6
  Sol".
- **`tencent-hunyuan-hy3-preview-model-card` v552 — noise, skipped.** The same HuggingFace widget
  churn diagnosed on 2026-09-07: downloads 56,428 → 59,468, and the `cais/hle` row (30) moving above
  the SWE-bench_Verified row in the Evaluation results sidebar. No value changed, no publisher text
  changed.

## 7. Friction log

Four lines appended to `logs/friction.jsonl`:

- `monitor_gap` — the four dropped fetch failures, escalated to `PROPOSALS.md` (§8).
- `data_error` — the Apollo `canonical_url` typo, with the note that the pipeline was holding a
  broken address and resurfacing the working one as an unknown candidate at the same time.
- `ambiguous_criteria` — `openness` on a document that analyses *published* figures for
  restricted-access models it did not itself run. Today's Redwood post runs experiments only on four
  Apache-2.0 open-weight models but quotes Anthropic's system-card CoTControl numbers for Mythos
  Preview and Mythos 5. TASK.md points both ways: `openness` is defined as the class of the most
  restricted model in `model_names` (→ `open_weight_permissive`), while the 2026-09-04 policy says a
  document *naming* any vetted-access model is `restricted`, with a deliberate no-omit-when-spanning
  rule. I resolved it by `model_names`, because putting Mythos in `model_names` would falsely assert
  the document assesses it, and recorded the Mythos discussion in `notes`. The distinction that
  settles this is assessed-here versus cited-from-elsewhere, which TASK.md does not draw. Low stakes
  per document, but independent evaluators argue against frontier system cards constantly.
- `tooling` — the 2026-09-10/11 entries reproduce; all four writes went through `/tmp/<name>.json`
  plus `--json <path>`, and both log appends were exact-string edits on the last line. Two new
  refusals: `env | grep` is refused as a multi-operation command, so the run environment cannot be
  inspected at all; and an inline `.venv/bin/python -c` sqlite read of `data/docs.sqlite` needs
  approval a headless run cannot give. The second had a direct cost — I wanted the vocabulary
  actually used in `provenance.source_of_lead` so today's rows would match prior runs, could not
  read it, and guessed `index_diff`.

## 8. Proposals

One dated entry appended to `logs/PROPOSALS.md`: *Phase A counted four fetch failures and escalated
none of them*. Phase A logged `not_found: 1, blocked: 3` while handing me an empty
`blocked_escalations` list, so the input to Task 5 was silently empty on a day when it should have
had four entries — and, because yesterday's run genuinely had zero, an empty list looks the same in
both cases. I only caught it by noticing a stale `last_checked` while triaging an unrelated
candidate. The reconstruction recovered the three blocked rows but not the one not-found row, which
is the row where an agent verdict would have been worth most. The entry asks for two small things:
populate `blocked_escalations` from every non-`ok` outcome including `not_found`, with
`{slug, url, outcome, http_status, checked_at}`; and copy Phase A's summary counters into
`candidates.json` so a run can assert `len(blocked_escalations) == blocked + not_found` and file
friction when it does not. This is the same defect class as the 2026-08-21 `phase_a_status` entry in
that file — a count that means "nothing happened" and a count that means "something was dropped"
must not look identical to the agent.
