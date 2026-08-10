# cardtrack evaluator backfill — run `evaluator-backfill-2026-08-10`

Corpus went from 171 to 174 documents. Three written, zero routed to issues, zero rejected.

The session's headline is a negative one, and it is the useful result: **four of the five
priority evaluators are now genuinely exhausted, and I can say exactly why for each.** I
enumerated every 2026 publication of epoch_ai, securebio, transluce, us_caisi and rand from
their own indexes (not from `candidates.json`, which is nav chrome for all five), dated every
item, and fetched every one that could plausibly assess a named model. Epoch AI yielded two
documents and SecureBio one. Transluce, US CAISI and RAND yielded nothing, because everything
they published in 2026 that is not already catalogued is methodology, policy, or an
organisational announcement.

The second finding is for the loop supervisor: **the three tier-2 evaluators added in the last
commit are sitting on real named-model evaluations that this session's priority list did not
authorise me to touch.** See "Handoff" below.

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 2228 across 28 publishers |
| Candidates triaged | 593 — the eight evaluators in scope (epoch_ai 61, securebio 97, transluce 31, us_caisi 130, rand 65, metr 82, uk_aisi 91, apollo_research 36). The 1635 publisher candidates were skipped per the priority list |
| Index/archive pages enumerated | 26 |
| Documents fetched and read | 32 (in full, or far enough for an unambiguous verdict) |
| Proposals submitted | 3 |
| Written as rows | 3 (ids 172–174) |
| Routed to review issues | 0 |
| Rejected | 0 |
| Tier-2 proposals filed | 0 of the 3 permitted (see Handoff) |
| Open GitHub issues to investigate | 0 (`logs/open_issues.json` is `[]`) |
| Blocked-URL escalations | 0 (empty in `candidates.json`) |

Evaluator counts after the run, safety-eval flag count in parentheses: uk_aisi 16, metr 12,
**epoch_ai 7**, **securebio 6**, rand 5, transluce 4, apollo_research 3, us_caisi 3.

## Proposals and validator verdicts

| # | Document | Publisher | Date | Safety | Verdict |
|---|---|---|---|---|---|
| 1 | **SecureBio's pre-release assessment of OpenAI's GPT-5.5** | securebio | 2026-04-23 | yes | `written` id 172 |
| 2 | Can AI Learn From Experience? EBR-Bench Results | epoch_ai | 2026-07-01 | no | `written` id 173 |
| 3 | **OpenAI accidentally hacked Hugging Face — should we have seen it coming?** | epoch_ai | 2026-07-22 | yes | `written` id 174 |

1. `securebio.substack.com/p/securebios-pre-release-assessment` — two pre-release GPT-5.5
   checkpoints, accessed 2–9 April 2026 with API-level biological content filtering disabled.
   Static expert-biology evaluations (checkpoints at or near the top of all models tested,
   above every expert human score), the agentic ABC-Bench and ABLE dual-use protein-design
   suites, and a manual dual-use probe of refusal and redirection behaviour. Same document
   class as the already-catalogued GPT-5.6 Sol pre-release testing report, and the only
   uncatalogued 2026 model-specific item in SecureBio's whole archive.
2. `epoch.ai/publications/earthborne-rangers-benchmark` — EBR-bench, 10 or 30 repeated
   playthroughs of an obscure board game to test learning from experience. Per-model numbers
   for GPT-5.5, Claude Opus 4.8, GPT-5 and Claude Opus 4.1; GPT-5.5 and Opus 4.8 beat the
   older pair on initial score but show no more on-the-fly learning. `has_safety_evals: false`
   — the report notes that on-the-fly learning would complicate pre-release dangerous-capability
   testing, but runs no safety evaluation itself.
3. `epoch.ai/gradient-updates/openai-accidentally-hacked-hugging-face` — Epoch's assessment of
   whether the Hugging Face incident was predictable from existing cyber evidence, assembled
   per model: UK AISI's finding that Mythos 5 and GPT-5.6 Sol both consistently compromise
   realistic corporate networks, Irregular's FrontierCyber zero-day results for GPT-5.6 Sol,
   the ExploitBench result for Mythos, and Epoch's own Cyber ECI, on which both are a break in
   trend. Catalogued on the same precedent as the existing `are-mythos-cyber-capabilities-overhyped`.

## Judgement calls I did not paper over

- **Two Epoch skips a reviewer could reverse**, both in friction. `data-insights/cve-severity-spike`
  (2026-07-02) is the direct predecessor of the catalogued July update — same series, same
  measurement, same model — so I kept only the update. `epoch.ai/MirrorCode` (2026-06-26) is a
  benchmark landing page with a continuously-updated leaderboard whose underlying report is
  already catalogued, so I treated it as a living page rather than a document.
- **METR's copy of the MirrorCode report is not a second row.** `metr.org/blog/2026-04-10-mirrorcode-preliminary-results/`
  is the same co-published report as Epoch's catalogued one. Noted in friction that the corpus
  is currently inconsistent here: the joint UK AISI/CAISI Kimi K3 assessment *is* catalogued
  twice, once per institute. That needs a maintainer ruling, not an agent's guess.
- **CAISI's red-teaming blog post is the closest call I rejected.** `blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition`
  (2026-03-23) reports that 250,000+ attack attempts by 400+ participants found at least one
  successful hijack against all 13 target frontier models, that robustness differed sharply
  between them, and that attacks transfer asymmetrically from robust to weak models. It is real
  comparative security measurement — but the post names none of the 13 models, and the artifact
  is a Gray Swan-led joint paper. It fails the system-card test on the naming point alone.
- **I did not treat "evaluator published it" as sufficient.** Epoch's `where-autonomy-works`
  robotics report, its 1,196-model biological-AI database, AISI's Frontier AI Trends Report
  summary and METR's transcript-based uplift estimate are all substantial evaluation work that
  names no model under assessment. They are research about models, not assessments of one.

## What is now exhausted, and how I verified it

- **epoch_ai** — enumerated all 261 publications/data-insights/gradient-updates with dates from
  the section indexes' prehydrated JSON (69 are 2026), plus `sitemap-index.xml`. Fetched the
  nine plausible items. Everything else 2026 is compute economics, chips, data centres, energy,
  adoption surveys, forecasting or benchmark-launch announcements. `FrontierMath: Open Problems`
  (2026-01-27) is a benchmark release with no model results.
- **securebio** — the substack archive is 12 posts total and `securebio.org/blog` mirrors it.
  Five were catalogued, one is now id 172, and the other six are methodology
  (`securebios-principles-and-practices`, `the-role-of-evals-in-the-biorisk`), a dashboard
  launch, org news, wastewater metagenomics, and the `preparing-for-the-bio-mythos-moment`
  policy essay (which discusses Mythos and Fable but is an argument for biosecurity assurance
  infrastructure, not an evaluation).
- **transluce** — `/news` lists every item with a date and `/docent/blog` adds nothing new. All
  four 2026 research/demo items are catalogued; the rest of 2026 is three vision essays
  (`foundation-models-for-oversight`, `behavior-science`, `building-technology-to-drive-ai-governance`),
  the Analysis Plans framework, and `oversight-assistants` (2026-01-06). **Closed.**
- **us_caisi** — checked both the blog (4 posts; `accelerating-ai-innovation-through-measurement-science`
  and `cheating-ai-agent-evaluations` are both 2025-12-02, below the floor; `analyzing-transcripts-ai-agent-evaluations`
  2026-02-18 is transcript-review methodology) and the full CAISI news tag `2810121`. The three
  catalogued assessments (DeepSeek V4 Pro, GLM-5.2, Kimi K3) are CAISI's only public
  model-specific 2026 output; everything else 2026 is a CRADA/MoU announcement, an RFI, or a
  methodology report. A web search confirmed CAISI's 40+ other assessments are unpublished.
  **Closed.**
- **rand** — the Canary project page lists the eval output, and pages 1–4 of CAST
  research-and-commentary cover Aug 2026 back to Jan 2026. All five Canary evaluation reports
  are catalogued; the rest is biosecurity policy, weights security, compute/energy, mirror-life
  and evaluation methodology (`PEA4886-1` open-weight evaluation approaches, `RRA4618-1`
  autograders, `WRA4869-1` RCT methodology). **Closed.**
- **metr** — `/blog`, `/research` and `/notes` re-enumerated. Six uncatalogued 2026 items, none
  qualifying: the Frontier Risk Report blog page duplicates the catalogued PDF; MirrorCode
  duplicates Epoch's; the rest are the AI-usage survey, task-substitution theory, the uplift
  experiment redesign, a NanoGPT-leaderboard evidence note, a Claude Code transcript uplift
  estimate, an incident-investigation proposal, and confidential-information policy.
- **uk_aisi** — thirteen uncatalogued in-scope-by-date blog posts fetched and name-scanned; zero
  named models in twelve, one incidental "Claude Code" in the agent-tools survey. See friction:
  AISI anonymises everything that is not a named model evaluation, which makes a name-scan a
  reliable single-pass triage for this publisher.
- **apollo_research** — `/monitoring` (the section the two catalogued 2026 items live in) has
  six entries; the three uncatalogued ones are a product vision, a research agenda, and the
  Watcher product launch, plus `what-makes-a-good-monitoring-prompt` (2026-07-23), which is a
  prompt-ablation study that runs gpt-5.4, sonnet-4.6 and gemini-2.5-flash as instruments and
  averages over them — the prompt is the subject, not the models.

## Skipped, by reason class

Counts are exact where I classified item by item, and marked approximate where a class was
disposed of in bulk from an index listing.

| Reason class | Count | Examples |
|---|---|---|
| Publisher (non-evaluator) candidates, out of scope this session | 1635 (exact) | all nvidia, anthropic, mistral, tencent_hunyuan, stepfun, deepseek, xai, google_deepmind, openai, xiaomi, inclusion_ai, meta, moonshot_ai, thinking_machines, poolside, alibaba_qwen entries |
| Navigation, hub chrome, topic and author pages | ~290 (approx.) | every `epoch.ai/topics/*`, `/data/*`, `/benchmarks/*`; the ~90 `nist.gov` site-wide nav links that make up most of the us_caisi candidate list; `substack.com/@author` profiles; RAND site furniture |
| Below the 2026-01-01 scope floor | ~200 (approx.) | the pre-2026 tail of every evaluator index — most of METR's `/blog` and `/notes`, the bulk of the AISI blog, all Transluce research before `oversight-assistants`, SecureBio's detection-side posts; individually named: CAISI `accelerating-ai-innovation-through-measurement-science` and `cheating-ai-agent-evaluations` (both 2025-12-02), Transluce `pcd` (2025-12-18) |
| Not about a specific model or eval (system-card test) | ~35 (approx.; also absorbs Epoch's 2026 compute, chips, energy, revenue and adoption items, which were classified from the index listing rather than fetched) | Epoch's robotics report, biological-AI-models database, `have-ai-capabilities-accelerated`, `keeping-up-with-the-gpts`, `gpt-4-longest-eci-lead`; all 13 AISI posts above; CAISI's red-teaming, transcript-analysis and measurement-science posts; METR's NanoGPT note and transcript uplift estimate; Apollo's monitoring-prompt ablation; SecureBio's methodology posts and the Bio Mythos essay; RAND's methodology and policy reports |
| Same evaluation already covered | 3 (exact) | `epoch.ai/data-insights/cve-severity-spike` (superseded by the catalogued July update); `epoch.ai/MirrorCode` (leaderboard page for the catalogued report); `metr.org/blog/2026-04-10-mirrorcode-preliminary-results/` (co-published copy) |
| Announcement, partnership, product or org news | 12 (exact) | CAISI's OpenMined CRADA and GSA MoU; AISI's ElevenLabs, Microsoft, Australian AISI and Google DeepMind partnerships and Engineering Playbook; Transluce's fundraiser and governance hire; SecureBio's "Leaving SecureBio AI in Good Hands"; Apollo's Watcher launch |
| Benchmark launch with no model results | 1 (exact) | `epoch.ai/latest/benchmarking-ai-on-unsolved-math-problems` (FrontierMath: Open Problems, 2026-01-27) |

## Handoff — what the next session should know

1. **The tier-2 evaluators are the biggest uncatalogued vein in the corpus right now, and I was
   not authorised to drain them.** Concretely, and all verified by fetching the index pages:
   - **saferai** — `safer-ai.org/research/glm-5-2-evaluation-report`, an independent risk
     evaluation of GLM-5.2 across the four EU Code of Practice systemic-risk areas, finding
     frontier-level cyber and biology capability without the safeguards frontier developers
     apply. Also an external Assurance-2.0 review of DeepMind's Gemini 2.5 Pro
     scheming-inability safety case.
   - **far_ai** — the AI Security Leaderboard (2026-07-29): safeguards of Claude Fable 5,
     GPT-5.6 Sol, Grok 4.5 and Gemini 3.1 Pro tested under identical conditions, with Grok 4.5
     and Gemini 3.1 Pro broken for under $300 each. Plus a DeepSeek-V4-Pro safeguard stress test.
   - **palisade_research** — "Language Models Can Autonomously Hack and Self-Replicate"
     (2026-05-07) and the robot shutdown-resistance technical report (2026-02-12).
   - **redwood_research** is the exception: its blog is commentary on other orgs' incidents and
     reports. Low yield; deprioritise it.
   These are tier-2, so they become review issues rather than rows — and `logs/issues_outbox.jsonl`
   holds **13 undelivered issues** against 3 in `issues_outbox.sent.jsonl`. Adding six more to a
   queue that is not being drained is worth a supervisor decision first, which is why I filed none.
2. **`logs/candidates.json` coverage of the evaluators is real but uneven, so do not treat it as
   the work list.** It is a new-links diff, so none of its 593 evaluator entries is an
   already-catalogued URL. Article coverage per publisher: uk_aisi 79 blog articles and metr 46
   (good), but epoch_ai only **8** — the ten items on the `/latest` front page — against 61
   entries, and us_caisi 130 entries of which ~90 are nist.gov site-wide navigation. Neither of
   this run's two Epoch finds beyond the front page was in the candidate list, and the SecureBio
   find was. The friction log carries the enumeration recipe for Epoch (section-index prehydrated
   JSON — its article pages carry no machine-readable date at all); the other four evaluators are
   small enough to enumerate from one index fetch each. If `sources.yaml` gains an `index_urls`
   entry for epoch_ai, `https://epoch.ai/publications` is the one to add: it lists all sections.
3. **Two rulings a maintainer should make**, both in friction: whether co-published reports get
   one row or one per publisher (MirrorCode is currently one, the UK AISI/CAISI Kimi K3
   assessment is currently two), and whether superseding data-insight updates retire their
   predecessors.
4. `logs/open_issues.json` is `[]` and `blocked_escalations` is empty, so no issues were
   investigated, no comments filed, and no documents found dead.

## Friction and proposals

Five entries appended to `logs/friction.jsonl`: the Epoch enumeration recipe and its missing
on-page dates; the two reversible Epoch skips; the co-publication inconsistency; the AISI
name-scan triage finding; and the tier-2 evaluator gap with the outbox backlog that blocks it.

Nothing appended to `PROPOSALS.md`. The one process problem worth escalating — that
`sources.yaml` gained four tier-2 evaluators whose output no session is allowed to file while the
issue queue stays undelivered — is a scheduling decision for the supervisor, and the friction
entry carries the specific URLs a maintainer needs.
