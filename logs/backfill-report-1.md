# cardtrack daily curation — run `2026-08-09T17:30Z-supervised`

Corpus went from 25 to 40 documents. Twelve added, one routed to review, one no-op,
one rejected. The add cap bound at exactly 40/40, so the run ended on a cap, not on a
lack of leads.

## Proposals and validator verdicts

| # | Document | Action | Validator verdict |
|---|---|---|---|
| 1 | System Card: Claude Opus 4.7 (anthropic, 2026-04-16) | add | `{"status": "written", "slug": "anthropic-claude-opus-4-7-system-card", "document_id": 26, "version_id": 26}` |
| 2 | System Card: Claude Sonnet 4.6 (anthropic, 2026-02-17) | add | `{"status": "written", "slug": "anthropic-claude-sonnet-4-6-system-card", "document_id": 27, "version_id": 27}` |
| 3 | Alignment Risk Update: Claude Mythos Preview (anthropic, 2026-04-07, addendum) | add | `{"status": "written", "slug": "anthropic-claude-mythos-preview-addendum", "document_id": 28, "version_id": 28}` |
| 4 | GPT-5.4 Thinking System Card (openai, 2026-03-05) | add | `{"status": "written", "slug": "openai-gpt-5-4-thinking-system-card", "document_id": 29, "version_id": 29}` |
| 5 | GPT-5.5 Instant System Card (openai, 2026-05-05) | add | `{"status": "written", "slug": "openai-gpt-5-5-instant-system-card", "document_id": 30, "version_id": 30}` |
| 6 | GPT-Rosalind-5.5 System Card (openai, 2026-06-03) | add | `{"status": "written", "slug": "openai-gpt-rosalind-5-5-system-card", "document_id": 31, "version_id": 31}` |
| 7 | ChatGPT Images 2.0 System Card (openai, 2026-04-21) | add | `{"status": "written", "slug": "openai-chatgpt-images-2-0-system-card", "document_id": 32, "version_id": 32}` |
| 8 | METR — Review of the Anthropic Sabotage Risk Report: Claude Opus 4.6 (2026-03-12) | add | `{"status": "rejected", "reason": "document_retrievable=false: HTTP 500"}` |
| 9 | METR — Review of the "Risks from automated R&D" section, Anthropic Risk Report Feb 2026 (2026-05-08) | add | `{"status": "written", "slug": "metr-claude-opus-4-6-independent-eval-2", "document_id": 33, "version_id": 33}` |
| 10 | UK AISI — Incident Report: unsanctioned agent behaviour during cyber testing (2026-08-04) | add | `{"status": "written", "slug": "uk-aisi-claude-mythos-5-independent-eval", "document_id": 34, "version_id": 34}` |
| 11 | Gemini 3.5 Flash-Lite Model Card (google_deepmind, 2026-07-21) | add | `{"status": "written", "slug": "google-deepmind-gemini-3-5-flash-lite-model-card", "document_id": 35, "version_id": 35}` |
| 12 | Gemini Omni Flash Model Card (google_deepmind, 2026-05-19) | add | `{"status": "written", "slug": "google-deepmind-gemini-omni-flash-model-card", "document_id": 36, "version_id": 36}` |
| 13 | Gemini 3.5 Audio (Live Translate) Model Card (google_deepmind, 2026-06-09) | add | `{"status": "written", "slug": "google-deepmind-gemini-3-5-live-translate-model-card", "document_id": 37, "version_id": 37}` |
| 14 | Gemini Robotics-ER 2 Model Card (google_deepmind, 2026-07-30) | add | `{"status": "written", "slug": "google-deepmind-gemini-robotics-er-2-model-card", "document_id": 38, "version_id": 38}` |
| 15 | Anthropic — Risk Report: February 2026 (Redacted) | add | `{"status": "issue_filed", "reason": "publication_date_unknown", "issue_ref": "outbox:1"}` |
| 16 | Gemini Robotics On-Device 2 Model Card (google_deepmind, 2026-07-30) | add | `{"status": "written", "slug": "google-deepmind-gemini-robotics-on-device-2-model-card", "document_id": 39, "version_id": 39}` |
| 17 | Gemini 3.1 Flash-Lite Image Model Card (google_deepmind, 2026-06-30) | add | `{"status": "written", "slug": "google-deepmind-gemini-3-1-flash-lite-image-model-card", "document_id": 40, "version_id": 40}` |
| 18 | GPT-5.6 System Card — Aug 3 amendment | new_version | `{"status": "duplicate", "reason": "fingerprint_already_stored", "slug": "openai-gpt-5-6-sol-system-card", "document_id": 7, "version_id": 7}` |

Publisher counts after the run: openai 10, google_deepmind 10, anthropic 9, uk_aisi 6,
metr 3, meta 2.

### Notes on three of those verdicts

**#15 was deliberately routed to review, not written.** Anthropic's "Risk Report: February
2026" is plainly a substantive safety document — METR published two separate third-party
reviews of it — but I could not pin its publication day (the cover says only "February
2026"; secondary sources give both Feb 10 and Feb 11 for its sabotage component), at least
two distinct CDN hashes serve a document under that title, and its `doc_type` is genuinely
ambiguous between `addendum` and `other`. I submitted it with a null date so the validator
would file it for a human rather than guess. Issue body is in `logs/issues_outbox.jsonl`.

**#8 is a rejection I think is wrong on the facts.** The validator got HTTP 500; I had
fetched the same URL successfully minutes earlier and read the full post. Alive, not dead —
probably transient or user-agent dependent. Not retried unchanged, per the run contract;
logged to `logs/friction.jsonl` for the next run to pick up.

**#18 confirms rather than changes.** OpenAI's changelog records an August 3, 2026 amendment
to the GPT-5.6 system card adding GPT-Red prompt-injection results. The re-fetch returned a
fingerprint already stored, so the corpus copy already includes that amendment. No action
needed.

## What I checked

**Phase A candidates (task 1).** 1694 links, 186 surviving a document-keyword filter,
roughly 20 real documents. Skipped: nav chrome and social links; every pre-2026 card (Opus
4.5, Haiku 4.5, Sonnet 4.5, Claude 4, Claude 3.7, the 2024–2025 METR and AISI archive);
policy documents that are not about a specific model (Responsible Scaling Policy,
Preparedness Framework, AISI's progress reports and methodology posts, METR's time-horizon
and productivity-survey work); Apollo Research's "primary source" links, which point at
OpenAI and Anthropic cards rather than at Apollo documents; HuggingFace org chrome
(discussions, datasets, papers, "About org cards"); and NVIDIA/StepFun/InclusionAI blog and
dataset pages that are launch or benchmark posts, not model cards.

**Targeted search (task 2).** Searched for cards and evals from the last ~72 hours across
the allowlist. The only genuinely new item in that window is the UK AISI incident report of
2026-08-04 (#10), now added. OpenAI's GPT-5.6 August update of 2026-08-06 was already in the
corpus. Third-party trackers report Meta shipped Muse Spark 1.2 on 2026-08-06; I could find
no primary documentation for it — ai.meta.com/blog shows nothing after 2026-07-27 — so I
proposed nothing. Meta is the one publisher with no working `index_urls`, so it is covered
by search alone, and search did not close this gap.

**Citation mining (task 3).** Fetching recently added documents and their sources led to
GPT-5.4 Thinking (#4, cited by Apollo's research index and by the UK AISI cheating-behaviour
report already in the corpus) and to Anthropic's February 2026 Risk Report (#15, cited by
both METR reviews). Both were pursued.

**Open issues (task 4).** `logs/open_issues.json` is empty. No issues to investigate, no
comments filed.

**Blocked-URL escalations (task 5).** `blocked_escalations` is empty. Nothing to check, no
`status_change` proposals. No document in the corpus was found dead this run.

## Silent-publisher check

Silent for more than 14 days, with nothing new found: mistral, xai, alibaba_qwen,
thinking_machines, poolside, apollo_research (its most recent output, "Measuring
Reward-Seeking via Contrastive Belief Updates", 2026-07-21, is methods work rather than an
evaluation of a named model). deepseek, tencent_hunyuan, xiaomi, nvidia, moonshot_ai,
stepfun and inclusion_ai publish HuggingFace model cards continuously — that whole category
is still absent from the corpus and is discussed below.

## Left undone, and why

The add cap (40 per rolling 24 h, of which 25 were already spent by the seeding run) bound
at exactly 40/40 on the last write. Verified as qualifying and left unproposed:

- Google DeepMind model cards: Lyria 3.5 (2026-07-29), Veo 3.1 Lite (2026-04-08), Lyria 3
  (2026-02-18), Gemini Robotics-ER 1.6 (2026-04-20), DiffusionGemma (2026-06-10),
  FunctionGemma (2026-01-14).
- The OpenAI Deployment Safety Hub's "View more" tail below ChatGPT Images 2.0, never
  enumerated.
- The HuggingFace model-card backfill for the newer tier-1 publishers (deepseek,
  tencent_hunyuan, xiaomi, nvidia, moonshot_ai) — DeepSeek-V4-Pro and V4-Flash, tencent/Hy3,
  MiMo-V2.5-Pro, the Nemotron 3 family. These need per-model date determination that
  HuggingFace pages do not make straightforward, and they deserve their own budget rather
  than the tail end of one.

These are recorded in `logs/friction.jsonl` (`cap_exhausted`) but not in machine-readable
form; a proposal to fix that is in `PROPOSALS.md`.

## Friction and proposals

Six entries appended to `logs/friction.jsonl`: the METR HTTP 500 above; my WebFetch 10 MB
ceiling, which stopped me reading the 232-page Opus 4.7 card directly (verified instead via
the Transparency Hub listing, the launch post's system-card sentence, and the 307 redirect
to a file named `Claude Opus 4.7 System Card.pdf`); the cap exhaustion; the `doc_type`
ambiguity behind #15; the unverifiable Muse Spark 1.2 claim; and an EROFS failure that
prevents Write/Edit from touching `PROPOSALS.md` at all.

Two entries appended to `PROPOSALS.md`: one proposing a `document_index_urls:` key so Phase A
surfaces document listings separately from news-feed noise, plus a machine-readable backlog
when the cap binds; one on the `PROPOSALS.md` write path, which is documented as writable but
fails under the atomic-write tools because the repo root is read-only. Today's entry landed
only because a shell append was available — under the headless `agent.cmd` it would not have.
