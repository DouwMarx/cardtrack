# cardtrack run report — 2026-09-24 (run_id `2026-09-24T06:17Z-local`)

## Headline

**8 distinct proposals, all `written`** (one needed a resubmission after a transient 429): five new
documents (338–342), one annotation and two field updates. The three verified-in-scope documents that yesterday's rolling cap blocked
(MiMo-V2.6, Qwen-Image-2.1, Redwood's Astra filler-token eval) are now catalogued. The restricted-access
sweep found a missed access program from 08-28: **OpenAI's Rosalind Workbench**. Two corrections to
existing rows came from reading full text: **GPT-6 Sol and GPT-6 Luna** are now listed on the GPT-6
Astra system card, since its 09-22 revision added an appendix covering them and OpenAI published no
separate card. **`harmful_manipulation`** is now tagged on the Opus 5.5 system card, closing the gap
flagged yesterday.

| | |
| --- | --- |
| Proposals submitted | 8 (+1 resubmission after a transient 429) |
| `written` | 8 — documents 338, 339, 340, 341, 342; version 620 annotated; 2 field updates (283, 336) |
| `rejected` | 1 transient (`HTTP 429`); the identical resubmission was `written` |
| `duplicate` / `noop` | 0 |
| Candidates triaged | 30 new (first seen 2026-09-24) + 3 carried over from 09-23 |
| `annotate_version` | 1 of 5 new diffs; 4 skipped as noise |
| Issues handled | 0 (`open_issues.json` is `[]`) |
| Blocked-URL escalations | 0 (`blocked_escalations: []`) |
| Friction entries | 4 · `PROPOSALS.md` entries: 0 |

## All proposals and verdicts

| # | proposal | verdict |
| --- | --- | --- |
| 1 | add — Redwood Research, *Astra is much better at reasoning with filler tokens than previous models* (2026-09-23), `independent_eval`, `loss_of_control`, `closed` | `{"status": "written", "slug": "redwood-research-gpt-6-astra-independent-eval", "document_id": 338, "version_id": 623}` |
| 2 | add — Xiaomi, MiMo-V2.6-Pro-RL model card (family: V2.6-Pro, V2.6-Flash; 2026-09-22), MIT, `open_weight_permissive`, no safety evals | `{"status": "written", "slug": "xiaomi-mimo-v2-6-pro-model-card", "document_id": 339, "version_id": 624}` |
| 3 | add — Alibaba Qwen, Qwen-Image-2.1 model card (2026-09-20), Qwen Research License, `open_weight_restrictive`, no safety evals | 1st: `{"status": "rejected", "reason": "document_retrievable=false: HTTP 429"}` → resubmitted about 15 min later: `{"status": "written", "slug": "alibaba-qwen-qwen-image-2-1-model-card", "document_id": 341, "version_id": 626}` |
| 4 | add — Epoch AI, *AI has improved significantly at reasoning about IKEA furniture assembly* (2026-09-23), `independent_eval`, capability only | `{"status": "written", "slug": "epoch-ai-gpt-6-astra-independent-eval-2", "document_id": 340, "version_id": 625}` |
| 5 | add — OpenAI, *Meet Rosalind Workbench* (2026-08-28), `access_policy`, GPT-Rosalind family, `restricted` | `{"status": "written", "slug": "openai-gpt-rosalind-access-policy-4", "document_id": 342, "version_id": 627}` |
| 6 | annotate_version — `openai-gpt-6-astra-system-card` v620 | `{"status": "written", "document_id": 283, "version_id": 620}` |
| 7 | field_update — `openai-gpt-6-astra-system-card` `model_names` += GPT-6 Sol, GPT-6 Luna | `{"status": "written", "document_id": 283}` |
| 8 | field_update — `anthropic-claude-opus-5-5-system-card` `risk_domains` += `harmful_manipulation` | `{"status": "written", "document_id": 336}` |

Notes on the judgement calls:

- **The 429 retry** was not an "unchanged retry of a rejected proposal" in the sense TASK.md forbids.
  The rejection was a HuggingFace rate limit caused by my own parallel fetches. The document was
  verified live twice (model page and models API). Logged as friction.
- **Redwood Astra.** Read in full: filler tokens lift Astra from ~10–20% to ~50% on 4-hop reasoning and
  from 60–70% to ~90% on old AIME, while Opus 4.5, Opus 5, GPT-5.6-Sol and DeepSeek-V3.2 stay flat. It is
  a monitorability result, so it is tagged `loss_of_control`. The LessWrong cross-post is recorded as
  `co_published` and the code repo as `code`.
- **MiMo-V2.6.** The Xiaomi model-updates log dates the release to 2026-09-22 (pro, flash, pro-ultraspeed).
  HF `createdAt` is 09-21. `has_safety_evals: false`: the RL "adversarial screening" text is about
  training against reward hacking, not a safety eval.
- **Qwen-Image-2.1.** The date comes from the official GitHub README ("2026.09.20: We released
  Qwen-Image-2.1!"). HF `createdAt` (09-14) is the private-repo creation date.
- **Epoch IKEA.** GPT-6 Astra 80%, Claude Fable 5.1 70%, Claude Opus 5 61%, Claude Opus 4.5 28%; Kimi K3
  is the best open-weight model, about 7 months behind. Per-model capability benchmarks, consistent with
  existing Epoch rows (Earthborne Rangers, long-context latency). Gemini and Qwen appear without version
  names, so they are left out of `model_names`.
- **Rosalind Workbench** (sweep find, predates the daily window). Explore mode uses the user's
  ordinary ChatGPT models. Research mode, i.e. GPT-Rosalind for complex biology, is limited to
  verified organization members on request; enterprise and government access goes through approved
  or trusted-access pathways. That is real program structure around a named family, so it is an
  `access_policy`. It is distinct from the three existing GPT-Rosalind access rows (launch, Biodefense,
  new capabilities). ⚠️ **The page carries no date.** 2026-08-28 comes from consistent contemporaneous
  third-party coverage and is disclosed in the justification and friction log.
- **Opus 5.5 `harmful_manipulation`.** Phase A stored the card's full text
  (`data/text/7311c9c6….txt`, "System Card: Claude Opus 5.5 / September 22, 2026"), so the 10 MB fetch
  wall from yesterday no longer mattered. §5.1.3 is a malicious agentic influence-campaign eval
  against the FCF harmful-manipulation tiers ("demonstrates operational capability in running
  influence campaigns"; Tier 2 inconclusive). §6.4.3 reports behavioral-audit scores for
  sycophancy, user deception and encouragement of delusion. Clearly substantive.
- **GPT-6 Astra card → Sol/Luna.** OpenAI launched GPT-6 Sol and Luna on 09-22. The Deployment Safety
  Hub lists no separate card for them (checked: newest entries are ChatGPT Images 2.5 on 09-08 and
  Astra on 09-03). The Astra card's own change log adds "an Appendix with information about GPT-6 Sol
  and GPT-6 Luna" (Appendix A, pp. 119–152: safety, robustness, health, alignment, monitorability,
  Preparedness). Listing them makes the row findable by model name.

---

## 1. Phase A candidate triage

`candidates.json` holds 30 entries first seen `2026-09-24T06:20:15Z`; older slices were triaged by
earlier runs. The 3 carried-over items from 09-23 are covered above. Written from today's crop:
Epoch IKEA (#4).

Checked and skipped:

- `transluce.org/agent-activity` (09-23), *Early rogue AI agent activity and attempts to hack found
  on urlquery.net*. Read in full. A forensic incident report (SQLi, path-traversal and XSS probes
  against three organisations, activity back to 2026-03-06), attributed to OpenAI agent swarms, but
  **it names no model**. That fails the named-model gate. The related Hugging Face incident is already
  catalogued under METR and Redwood rows that do name GPT-5.6 Sol. If Transluce or OpenAI later
  attribute it to a model, it becomes proposable.
- `far.ai/blog/jailbreaking-qoders-cyber-safeguards` is already catalogued as
  `…/jailbreaking-alibaba-qoders-cyber-safeguards` (same post, retitled slug). No proposal.
- `apolloresearch.ai/science/we-need-3rd-party-training-run-evaluations` is a position essay dated
  2026-07-05, with no model results.
- `blog.redwoodresearch.org/p/latent-reasoning-architectures-would` (09-23) is an argument essay that
  cites Astra and Mythos only as supporting evidence. Fails the system-card test.
- `research.meta.ai/blog/bringing-your-muse-to-life` (09-23) announces Muse Realtime Avatar, a
  product feature with a latency/preference comparison against Runway and HeyGen and no model card.
  It was a borderline call: the model is a new real-time video generator. It is a feature launch, not
  model documentation, so it is skipped. Re-check if Meta publishes a card.
- `blog.google/.../gemini-3-8-text-to-speech` (09-23): Gemini 3.8 Flash TTS and Flash-Lite TTS are
  TTS models, auxiliary and out of `covered_model_class` absent safety evals. Its "model card" link
  points to the Gemini 3.8 Audio card, which is already `google-deepmind-gemini-3-8-live-model-card`.
- `anthropic.com/news/claude-discovers-novel-enzyme-system` and `/features/ebola-response` are science
  and use-case showcases with no named model and no program structure.
- `deepmind.google/.../private-ai-compute…` is infrastructure. Cursor `improved-token-efficiency` and
  `rollouts-and-security-reviewer` are product posts.
- NVIDIA Nemotron-3-Diarization and sortformer are diarization/ASR (excluded by scope). Datasets, HF
  profiles, discussions and `huggingface.co/papers/*` are not documents. InclusionAI
  Ming-Image-0.1-Design only has a demo Space and a discussion in the crop, not the model card; not
  pursued.

## 2. Targeted search (window 2026-09-21 → 2026-09-24)

`.agent_last_success` = `2026-09-23T06:31:42Z`, so the 72 h floor governs.

- **Frontier releases.** Per release trackers: 09-21 Grok 4.7; 09-22 Opus 5.5, GPT-6 Sol, GPT-6 Luna,
  MiMo-V2.6 Pro/Flash. All are now covered (Sol/Luna via the Astra card appendix).
- **Qwen3.8-Omni-Flash** (09-18, API-only) is in scope but has no fetchable primary document:
  qwen.ai renders client-side and there is no HF card. Not proposed; logged as friction.
- **Restricted-access sweep.** Rosalind Workbench (written, #5). The LSVP (opened 09-17) is already
  catalogued. Cyber Verification Program: Mythos-class access is still "in the near future", and
  US-only per Anthropic's page and SecurityWeek. No dedicated launch post yet. Nothing new on Project
  Glasswing, Daybreak, GPT-Rosalind global availability (09-11, covered), Gemini for Science,
  Co-Scientist or CodeMender.
- **Independent evaluators.** UK AISI's 09-22 post with EvalEval is about benchmark-reproducibility
  infrastructure, not a model eval. No new Apollo, METR, CAISI, Transluce (beyond the candidate
  above), SaferAI or Palisade evals inside the window. Two Astra no-CoT write-ups surfaced from
  non-allowlisted authors: Neel Nanda (personal capacity, AF, 09-10) and Christine Corry (Second Look
  Fellowship, 09-14). Neither is on the allowlist and neither is a co-publication, so nothing is
  proposed.

## 3. Citation mining

Today is Thursday, so no retrospective sweep. On this week's adds, the Opus 5.5 card cites METR
(already catalogued), CAISI testing (no public CAISI output found), and Gray Swan / Irregular /
Frontier Design (not allowlisted). **Watch item:** the card says a separate METR team's AI R&D
acceleration assessment inside Anthropic will produce "further public outputs … in the coming weeks".
The Redwood Astra post cites only the Astra card. No new leads.

## 4. Open issues / 5. Blocked URLs

`open_issues.json` is `[]`; `blocked_escalations` is `[]`. Nothing to act on. Every URL I fetched by
hand today was alive, except `openai.com/index/…` and `openai.com/rosalind/`, which return 403 to my
fetcher (bot-blocking; they are known live pages).

## 6. Document update summaries

5 new diffs (first fetched 09-24); **1 annotated, 4 skipped.** The older entries were assessed by
earlier runs and are unchanged.

| diff | verdict |
| --- | --- |
| `openai-gpt-6-astra-system-card` v620 (1196+/353−) | `written`. The 09-22 change log adds Appendix A for GPT-6 Sol and GPT-6 Luna, corrects the Astra HealthBench values for a misconfiguration, and updates several alignment evals. |
| `palisade-research-gpt-5-4-independent-eval` v618, `…grok-4…` v619 | **Skipped, noise.** The previous version was a JS redirect stub; the new one is the followed target plus Palisade's research listing. The document is unchanged. The rows are correctly `moved`. |
| `anthropic-claude-mythos-preview-other-9` v622 | **Skipped, noise.** A one-word copyedit ("capable of" → "show") plus rotation in the related-posts sidebar. |
| `alibaba-qwen-qwen-drive-1-0-4b-model-card` v621 | **Skipped, noise.** HF download counter and model-tree widget. |

## 7. Friction and proposals

Four entries appended to `logs/friction.jsonl`: `transient_rejection` (429 reported as not
retrievable), `unfetchable_but_alive` (API-only Qwen releases are structurally invisible),
`ambiguous_criteria` (undated Rosalind Workbench page), and `diff_noise` (stub → followed-target
transitions get past the 642d5b31 filter). None rises to a `PROPOSALS.md` entry today.

The rolling cap did not bind this run: 5 adds, no cap rejections.
