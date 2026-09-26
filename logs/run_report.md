# cardtrack run report — 2026-09-26 (run_id `2026-09-26T06:17Z-local`)

## Headline

**3 proposals, all `written`; 0 new documents.** It was a quiet news window. The main finding is
that OpenAI's Daybreak help article (`openai-gpt-5-6-sol-access-policy`) was substantively revised:

- The tiers are remapped, with GPT-6 Sol and Luna now in Daybreak Blue.
- Astra's reduced refusals are available in Daybreak Red only.
- There is a new approval tier for GPT-5.6-Cyber.
- Individual users need a FIDO2 hardware key by Oct 1, 2026.

That change got a version annotation and a `model_names` update.

| | |
| --- | --- |
| Proposals submitted | 3 |
| `written` | 3 (2 `annotate_version`, 1 `field_update`) |
| `rejected` / `duplicate` / `noop` | 0 |
| Candidates triaged | 12 links first seen at 2026-09-26T06:19Z (older slices were triaged by earlier runs) |
| `annotate_version` | 2 of 5 new diffs; the 3 others are noise (see §6) |
| Issues handled | 0 (`open_issues.json` is `[]`) |
| Blocked-URL escalations | 8: all alive (openai.com bot wall), no status change |
| Friction entries | 2 · `PROPOSALS.md` entries: 0 |

## All proposals and verdicts

| # | proposal | verdict |
| --- | --- | --- |
| 1 | annotate_version: `openai-gpt-5-6-sol-access-policy` v646, the Daybreak tier restructure and the FIDO2 requirement | `{"status": "written", "slug": "openai-gpt-5-6-sol-access-policy", "document_id": 271, "version_id": 646}` |
| 2 | field_update: `openai-gpt-5-6-sol-access-policy` `model_names` changed from [GPT-5.5, GPT-5.6 Sol, GPT-5.6-Cyber] to add GPT-5.5-Cyber, GPT-6 Sol, GPT-6 Luna and GPT-6 Astra | `{"status": "written", "slug": "openai-gpt-5-6-sol-access-policy", "document_id": 271}` |
| 3 | annotate_version: `nvidia-nvidia-nemotronlabs-voicechat-11b-model-card` v650. The references list was replaced by a citation of the model's own arXiv technical report (2609.21967) | `{"status": "written", "slug": "nvidia-nvidia-nemotronlabs-voicechat-11b-model-card", "document_id": 82, "version_id": 650}` |

Judgement call on #2: the current page's "Reduced refusals behaviour by model" table defines access
for all seven models. "Astra" on the page was recorded as GPT-6 Astra, which is how the model is named
elsewhere in the database. Evidence is the pipeline's stored v646. openai.com and help.openai.com
return 403 to my fetcher, so I could not re-read the live page.

---

## 1. Phase A candidate triage

These 12 links were first seen today. None was proposed:

- **`anthropic.com/research/yes-claude-can-do-nine-loops` (09-25).** A science showcase: Fable 5.1 in
  Claude Science computes a nine-loop N=4 SYM amplitude. There is no benchmark or safety content, so it
  is a capability demo and out of scope. This matches the earlier skip of the 09-17 biomolecular-modeling
  post.
- **Also skipped:**
  - `cursor.com/en-US/cookie-policy`: navigation.
  - HF profile `AdinaY`: not a document.
  - Three `huggingface.co/papers/*` (Tencent GAE, WorldCrafter, SLCA-GRPO): research papers, not
    model documentation.
  - `datasets/XiaomiMiMo/MiMo-V2.6-RL-oss`: a dataset.
  - Two `nvidia/OpenH-RF` discussions: not documents.

## 2. Targeted search (window 2026-09-23 → 2026-09-26)

`.agent_last_success` = `2026-09-25T06:29:51Z`, so the 72 h floor governs.

- **Release trackers** (llm-stats, digitalapplied): nothing after the 09-22 cluster (Opus 5.5, GPT-6
  Sol/Luna, MiMo-V2.6, Solar Mini 4), all of which are handled.
  - GPT-6 Sol/Luna have no standalone card. They are covered by the 09-22 appendix to the GPT-6 Astra
    system card (`openai-gpt-6-astra-system-card`).
  - The other 09-23/24 items are skipped:
    - Gemini 3.8 Flash TTS: TTS is an auxiliary model.
    - Fireworks Ember-1 and BFL FLUX 3 Action: not allowlisted.
    - Gemini 3.8 Live Avatar: a feature launch.
- **OpenAI, "priorities and principles for third-party assessments".** A policy statement that names no
  model, so it is skipped.
- **Restricted-access sweep.** Nothing new:
  - LSVP, CVP, Glasswing, Daybreak, Rosalind Biodefense and Fairwind are all catalogued.
  - The CVP opening for Mythos-class models is still not announced.
  - "Scaling trusted access for cyber defense" is already catalogued.
- **Carried-over lead, RAND RR-A5112-1** (open-weight bio misuse): still 403 on the HTML and PDF paths,
  and I can't verify its date or named models. Not proposed; friction logged for the second day.
- **Silent orgs (>14 days).** The full background sweep ran yesterday (09-25) and was not repeated.
  Today's spot checks of DeepSeek, Qwen, Moonshot, Z.ai and Xiaomi found their latest releases already
  catalogued (DeepSeek-V4.1-Flash, Qwen3.8, Kimi K3, GLM-5.3, MiMo-V2.6-Pro).
  - Limitation: I could not run an ad-hoc script to compute each publisher's newest date, because only
    `propose_doc.py` is runnable in this sandbox.

## 3. Citation mining

No documents were added in this run. Yesterday's adds (343–350) were citation-mined yesterday. Today
is Saturday, so there is no retrospective sweep.

## 4. Open issues

`open_issues.json` is `[]`.

## 5. Blocked-URL escalations

All 8 are openai.com or help.openai.com URLs that return 403 to my fetcher as well. Each is **alive**:
every one is currently indexed by search under its own title (Path to Astra, Introducing Trusted
Access for Cyber, Rosalind Biodefense, Introducing GPT-Rosalind, new GPT-Rosalind capabilities, the
Daybreak TAC overview, the HF security incident, and third-party cyber evaluations). The Daybreak
article also shows a fresh substantive revision in our own store (v646). No status change was proposed.

## 6. Document update summaries

There were 5 new diffs today (v646–v651). The 09-23→25 entries in `updated_docs.json` were judged by
earlier runs.

- **Annotated (2):**
  - v646: the Daybreak restructure (#1).
  - v650: VoiceChat's tech-report citation (#3).
- **Noise (3):**
  - `metr-claude-opus-4-8-independent-eval` v651: US spelling edits only ("judgment", "Acknowledgments").
  - `nvidia-alpamayo-1-5-10b-model-card` v649: download counter and model-tree widget.
  - `openai-gpt-5-5-access-policy` v647: the access-level table disappeared and "(opens in a new window)"
    text appeared. This looks like extractor drift, and I can't verify it against the live page (403),
    so it was not annotated. Logged as friction.

## 7. Friction and proposals

Two entries were appended to `logs/friction.jsonl`:

- `unfetchable_but_alive`: RAND RR-A5112-1, for the second day.
- `diff_ambiguity`: GPT-5.5 access-policy v647.

There are no new `PROPOSALS.md` entries. The RAND block fits the existing agent-fetcher-403 pattern;
if it persists, it may warrant a proposal to have Phase A attach a text snapshot to candidate leads.

Proposal JSON was staged in `/tmp/cardtrack_p*.json` and passed with `--json <path>`. Shell
redirection into `logs/` was blocked, so friction was appended with the Edit tool.
