# cardtrack run report — 2026-09-06 (run id `2026-09-06T06:15Z-local`)

Last successful agent run: `2026-09-05T06:35:44Z`. Search lookback: since that run, floored at
72 h. Today is a Sunday, so the Monday retrospective sweep was not due.

Headline: nine documents written, six of them OpenAI pages that previous runs recorded as
unreadable. The `openai.com/index/` HTTP 403 wall turned out to be agent-side only — the
validator fetches those URLs fine — so the whole **Trusted Access for Cyber** programme lineage
(the framework behind every `-Cyber` model tier, later rebranded Daybreak) had been invisible
including its programme root. That is now closed. Details in `logs/PROPOSALS.md`.

## Proposals and validator verdicts

| # | Action | Target | Verdict |
|---|--------|--------|---------|
| 1 | `add` | OpenAI — *Path to Astra: critical capabilities and frontier safeguards* (2026-09-01) | **written** → `openai-gpt-6-astra-other` (doc 291, v515) |
| 2 | `add` | OpenAI — *Pacing model development in an era of cyber-critical capabilities* (2026-08-20) | **written** → `openai-astra-other-2` (doc 292, v516) |
| 3 | `add` | Anthropic — *Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders* (2026-08-21) | **written** → `anthropic-claude-mythos-5-access-policy-2` (doc 293, v517) |
| 4 | `add` | OpenAI — *Introducing Trusted Access for Cyber* (2026-02-05) | **written** → `openai-gpt-5-3-codex-access-policy` (doc 296, v520) |
| 5 | `add` | OpenAI — *Trusted access for the next era of cyber defense* (2026-04-14) | **written** → `openai-gpt-5-4-access-policy` (doc 294, v518) |
| 6 | `add` | OpenAI — *Scaling Trusted Access for Cyber with GPT-5.5 and GPT-5.5-Cyber* (2026-05-07) | **written** → `openai-gpt-5-5-access-policy` (doc 295, v519) |
| 7 | `field_update` `related_urls` | `openai-gpt-6-astra-system-card` — add *Safety overview: GPT-6 Astra* | **rejected** first attempt (`invalid_value: related_urls note must be a string <= 500 chars`), then **written** with a shortened note (doc 283) |
| 8 | `field_update` `related_urls` | `palisade-research-gpt-5-4-independent-eval` — record moved URL | **written** (doc 190) |
| 9 | `field_update` `related_urls` | `palisade-research-grok-4-grok-4-0709-independent-eval` — record moved URL | **written** (doc 191) |
| 10 | `annotate_version` | `google-deepmind-gemini-3-7-flash-model-card` v513 | **written** |
| 11 | `annotate_version` | `inclusion-ai-ling-3-0-flash-model-card` v491 | **written** |
| 12 | `annotate_version` | `nvidia-nvidia-nemotron-3-ultra-550b-a55b-model-card` v494 | **written** |

The only rejection was my own formatting error (over-long `related_urls` note); the retry with a
trimmed note was accepted. No duplicates, no noops.

## 1. Phase A candidate triage

175 candidate links reviewed. Everything substantive from the last two index diffs was **already
catalogued by the 2026-09-05 run** — verified against the state summary rather than assumed:

- `deploymentsafety.openai.com/gpt-6-astra` → `openai-gpt-6-astra-system-card`
- `deepmind.google/models/model-cards/gemini-3-8-flash/` → `google-deepmind-gemini-3-8-flash-model-card`
- `blog.google/…/3-8-flash-and-3-8-flash-cyber/` → `google-deepmind-gemini-3-8-flash-cyber-access-policy` (Fairwind-gated)
- `research.meta.ai/blog/introducing-muse-spark-1-3` → `meta-muse-spark-1-3-other`
- `huggingface.co/tencent/Hy4-preview-FP8` → `tencent-hunyuan-hy4-preview-model-card` (FP8 is a quantisation variant)
- `inclusionAI/LLaDA2.2-*`, `LLaDA-Image*`, `UI-Venus-2` → existing rows; `LLaDA2.2-mini` is a size variant
- `nvidia/Cosmos3-Super-*`, `Cosmos3-Nano-Policy-DROID` → already in `model_names` of `nvidia-cosmos3-super-model-card` / `-edge-other`
- `blog.redwoodresearch.org/p/brief-independent-investigation-of` → already a `related_url` of `redwood-research-gpt-5-6-sol-independent-eval`
- `ai.google/gemini-for-science/`, `labs.google/science` → already `related_urls` of `google-deepmind-gemini-co-scientist-access-policy`
- `blog.google/…/build-with-gemini-omni-1-1-flash/` → `google-deepmind-gemini-omni-flash-model-card` already lists Gemini Omni 1.1 Flash

**Skipped, with reason:**

- Out of scope by `covered_model_class` (auxiliary models): `gemini-3-5-transcribe`, Meta *Muse
  Voice Transcribe*, `tencent/WeMM-Embedding-*`, `nvidia/magpie_tts_*`,
  `Nemotron-3-Diarization-preview`, `inclusionAI/ArmorOCR-GGUF`, NVIDIA `Ising-*`
  decoder/calibration repos, `SDLLM-*-1.7B-Base` research checkpoints. Honours the per-publisher
  `scope` notes in `sources.yaml`.
- Quantisation / size / domain variants of catalogued models: all `*-FP8`, `*-NVFP4`, `*-GGUF`,
  `*-Base-BF16` repos, `Ling-3.0-flash-Fin`, `Ling-3.0-*-singprobe`.
- Not model documentation: HF user profiles, collections, dataset repos, discussion threads,
  arXiv/HF paper links, `palisaderesearch.org` terms/privacy/podcast/TikTok/press-kit links,
  Cursor customer case studies and changelog entries, `x.ai` Grok Bot product posts,
  `mistral.ai/news/mistral-x-humain` (partnership), `metr.org/blog/2026-08-31-security-update`
  (METR's own security incident, not a model eval), Anthropic *wellbeing research grants* /
  *Fermat's Last Theorem* / *Model Hardware Standard* (a device spec, no named model evaluated),
  `blog.google/…/introducing-weathernext-3/` (weather model, no safety evals), the large block of
  `ai.google/*` navigation links the `gemini-for-science` index emits in bulk.
- `aisi.gov.uk/blog/optimal-stopping-…` — evaluation-methodology tooling (`optstop`), assesses no
  named model, fails the system-card test.
- `anthropic.com/news/enterprise-frontier-safeguards` — already a `related_url` of
  `anthropic-claude-fable-5-1-access-policy`.
- `nvidia/GEAR-SONIC`, `nvidia/SOMA-X` — left pending as before; the `GEAR-SONIC` scope-floor
  question is already logged (friction, 2026-09-01) and unresolved, so I did not guess.

## 2. Targeted search

- **Frontier releases in window.** Cross-checked a September-2026 release timeline: GPT-6 Astra
  (Sep 3), Gemini 3.8 Flash (Sep 2), Muse Spark 1.3 + 1.3 Contributor (Sep 2), Claude Fable 5.1 /
  Mythos 5.1 (Sep 1), Qwen3.8 27B (Sep 2). All already in the corpus. No un-catalogued release.
- **New this run, from search:** the three OpenAI Astra-adjacent documents (proposals 1, 2, 7) and
  the three Trusted Access for Cyber documents (proposals 4–6).
- **Restricted-access programme sweep.** Polled the named programmes. Anthropic's **Cyber
  Verification Program** had *no row at all* despite being one of its two named trusted-access
  programmes — closed by proposal 3, with the undated help-centre article specifying eligibility
  (free, application-based, Opus/Sonnet only, two-business-day decision, identity verification,
  ZDR organisations ineligible) recorded as a `related_url` rather than a null-date row. Also
  confirmed already-covered: Rosalind Biodefense, Daybreak Blue/Red, Project Glasswing, LSVP
  (`expanding-support-for-scientists`), Claude Science, Gemini for Science / Co-Scientist,
  Gemini 3.8 Flash Cyber / Fairwind.
  - **Watch item:** the Claude Mythos page states the Cyber Verification Program "will include
    Mythos access in the near future", and LSVP is US-organisations-only "though we're working to
    expand access". Both are the kind of policy change that gets its own post — worth polling.
- **Orgs silent > 14 days** (newest catalogued document older than 2026-08-23): apollo_research
  (Jul 21), cursor (Aug 12), epoch_ai (Jul 31), far_ai (Jul 29), mistral (Aug 4), moonshot_ai
  (Jul 27), nvidia (Aug 14), palisade_research (May 7), poolside (Jul 13), rand (Aug 11), saferai
  (Aug 2), securebio (Aug 7), stepfun (May 23), thinking_machines (Jul 31), uk_aisi (Aug 4),
  us_caisi (Jul 23), xiaomi (Apr 27). Searched the highest-yield of these — Apollo, UK AISI,
  METR, Mistral, Moonshot, Thinking Machines — and found nothing catalogue-worthy. UK AISI's
  newest is the Aug 27 `optstop` methodology post (skipped, above); Apollo has publicly shifted
  its agenda from scheming evals to "science of scheming" research, which partly explains the
  silence. No third-party pre-deployment eval of GPT-6 Astra has been published independently:
  UK AISI's Astra work appears as **section 8.8 of OpenAI's system card**, not as a UK AISI
  document, so it is not a separate row.

## 3. Citation mining

Followed references out of the recently added Astra and Fable 5.1 material. That is what surfaced
the Trusted Access for Cyber lineage (proposals 4–6) and the Anthropic CVP document (proposal 3).
The Monday retrospective sweep was not due today; the three oldest-newest-entry orgs for next
Monday are xiaomi (Apr 27), stepfun (May 23) and palisade_research (May 7).

## 4. Open issues

`logs/open_issues.json` is empty. No investigations, no comments posted.

## 5. Blocked-URL escalations

`blocked_escalations` is empty. Nothing to verify, no `dead` proposals.

**Related finding, from the diff review rather than the escalation list:** Palisade Research moved
`/blog/<slug>` → `/research/<slug>`, and the old URLs now serve an HTML redirect stub that the
pipeline stored as the newest version of **both** Palisade rows. Both documents are alive at the
new URLs — I confirmed the redirect target and found both entries with unchanged titles and dates
on `palisaderesearch.org/research`. `canonical_url` is operator-only, so I recorded the new URLs
as `related_urls` (proposals 8–9) for the operator sweep. Until they are promoted, the site shows
a two-line stub as the current content of both documents. Written up in `logs/PROPOSALS.md`.

## 6. Document updates

Reviewed 12 of the 20 pending diffs, annotated 3 (cap is 5), skipped the rest as noise:

**Annotated**

- `google-deepmind-gemini-3-7-flash-model-card` v513 — card now credits the model with "support
  for agentic video understanding"; intended-use list adds "complex video reasoning". A real
  capability-scope change, matching Google's agentic-video announcement.
- `inclusion-ai-ling-3-0-flash-model-card` v491 — vLLM instructions switched from InclusionAI's
  own fork (`vllm-ling-v3`, "Install our vLLM") to upstream `vllm-project/vllm`: mainline support
  has landed.
- `nvidia-nvidia-nemotron-3-ultra-550b-a55b-model-card` v494 — one new training-data disclosure
  line pointing to a Public Summary of Training Content.

**Skipped as noise** (said so rather than annotating)

- `tencent-hunyuan-hy3-preview-model-card` v514 — download counter, one leaderboard row reordered.
- `redwood-research-*` v510 / v511 / v512 — only the Substack title and subtitle lines stopped
  being extracted; body text unchanged. Extraction noise, not a document change.
- `palisade-research-*` v508 / v509 — the redirect-stub problem above, not a content revision.
- `anthropic-claude-fable-5-addendum` v498 — the "Related content" sidebar links rotated. Page
  furniture, not the addendum.

## 7. Friction log

Three lines appended to `logs/friction.jsonl`: the bot-wall workaround and its asymmetry
(`publisher_bot_wall_workaround`), the redirect-stub problem
(`publisher_url_restructure_stores_redirect_stub`), and an `openness` ambiguity
(`ambiguous_criteria`) — the definition keys on the *model's* availability, but the standard shape
is now a public tier plus a vetted-access capability tier (Astra + Daybreak Blue, Opus/Sonnet +
CVP, Gemini 3.8 Flash + Flash Cyber), and the same model can land either way depending on which
run catalogues it. I set `restricted` on the 2026-09-04 policy's stated intent and recorded the
reasoning in each row's `notes`.

## 8. Proposals

Two dated entries appended to `logs/PROPOSALS.md`: the agent-side-only nature of the openai.com
bot wall (with the proxy workaround, and a suggestion to expose the pipeline's own fetcher to the
agent instead of routing attested content through a third party), and the redirect-stub guard.

## Judgment calls worth an operator's eye

- **`openness: restricted` on the six cyber-tier documents.** Defensible either way; see the
  friction line. Each row's `notes` states the reasoning so a correction is cheap.
- **Two publication dates rest on secondary reporting alone** — `2026-02-05` for *Introducing
  Trusted Access for Cyber* and `2026-04-14` for *Trusted access for the next era of cyber
  defense*. The pages carry no visible date and the proxy strips date metadata. Both are recorded
  as such in `notes`. The other four have a primary or near-primary anchor (Wikipedia citation,
  same-day TechCrunch coverage, same-day community/HN postings).
- **`Safety overview: GPT-6 Astra` was made a `related_url`, not a row.** It is a standalone
  seven-point safety summary, but it covers the same release and the same evaluations as the
  catalogued system card, so the "never catalogue an announcement and its full report as two rows"
  rule applies. That field update also assigned `kind` values to the two pre-existing
  `related_urls` (`web_version`, `announcement`), since a `related_urls` update replaces the list.
