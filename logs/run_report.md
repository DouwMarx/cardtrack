# cardtrack agent run — 2026-11-11 (run id 2026-11-11T06:19Z-local)

- **Lookback:** the last agent success was 2026-11-10T06:29:52Z, so the 72 h minimum applied (2026-11-08 to 11-11).
- **Weekly retrospective sweep:** not run. It is a Wednesday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.
- **Cap:** reached on the 7th add. The rolling-24h window still counts yesterday's 13 adds.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | Add the Gemini 4 Carbon Safety & Security Report PDF (`system_card`, dated 11-10, the GA launch day). Tagged with all 5 domains; `closed`. | **written**: `google-deepmind-gemini-4-carbon-system-card` (doc 454) |
| 2 | Add the Gemini 4 Carbon Model Card PDF (`model_card`), with the HTML card as `web_version` and the GA post as `announcement`. Tagged societal_harm; `closed`. | **written**: `google-deepmind-gemini-4-carbon-model-card` (doc 455) |
| 3 | Add FAR.AI's Security Stress Test of Kimi K3.1 Pro (`independent_eval`, 11-09). Tagged cbrn, cyber; `open_weight_restrictive`. | **written**: `far-ai-kimi-k3-1-pro-independent-eval` (doc 456) |
| 4 | Add the Gemini Robotics 2.5 launch post (`other`, 11-10). Has safety evals but no tags; `restricted` (partner rollout only). | **written**: `google-deepmind-gemini-robotics-2-5-other` (doc 457) |
| 5 | OpenAI misalignment report "Unsanctioned Artifactory writes and cross-sample communication" (tagged loss_of_control). Deferred from 11-10. | **written**: `openai-openai-internal-research-model-other-9` (doc 458) |
| 6 | OpenAI misalignment report "Uploading files to the internet in order to cite them" (tagged loss_of_control). Deferred from 11-10. | **written**: `openai-openai-internal-research-model-other-10` (doc 459) |
| 7 | OpenAI misalignment report "Signing up for disposable emails and searching GitHub for leaked API keys" (tagged cyber, loss_of_control) | **rejected**: `cap_exceeded` (rolling 24 h). **Next run: re-propose; /tmp is wiped, so rebuild the JSON.** |
| 8 | Annotate v1142 of `google-deepmind-gemini-4-carbon-other` (the GA-day revision of the evaluation PDF) | **written** |

Every proposed document was fetched and read with read_doc before proposing.

**Calls worth checking:**
- **#1/#2, openness `closed`:** this follows the 10-14 Argon card and safety-report rows. Carbon is now on the public paid API, but its cyber tier stays gated to Fairwind verified defenders. Under the 09-04 "any vetted-access model" rule, the operator may prefer `restricted` here. Whatever is decided should apply to the Argon rows too.
- **#4, launch post as the document:** no Robotics 2.5 model card or safety PDF exists yet. Both guessed storage paths returned 404, and the model-cards index has no entry. It was admitted because the post reports measured capability and physical-safety results for a named model. **If a card appears, add it as the primary row and consider retiring this one.**
- **#3, openness:** the HF card releases the weights under a custom "Kimi K3.1 Pro License", so it was classed as restrictive.

## Phase A candidates (first seen 11-11)

Earlier candidates were triaged in previous runs.

**Proposed:**
- the Gemini 4 Carbon model card, which led to the card PDF and the safety report (#1, #2);
- the "Gemini 4 Carbon is now available" post, recorded as `announcement` on #2 rather than as its own row (Argon precedent);
- FAR.AI's Kimi K3.1 Pro test (#3);
- Gemini Robotics 2.5 (#4).

**Skipped:**
- **FAR.AI SynthDeception:** probe-training dataset research, not an evaluation of a named model.
- **Redwood "We don't understand whether GDM intentionally trains on CoT":** commentary on the Gemini 4 safety report, which is already catalogued.
- **AlphaProof Code:** a verification-framework showcase that uses Carbon, with no measured evaluation of the model.
- **Anthropic IPO roadshow; Cursor Projects multiplayer; DeepMind blog page 20:** not model documentation.
- **MiniMax-H3-Image (repo, blog, Space, PE, discussions):** an image model, out of scope per the minimax scope note.
- **inclusionAI SingVL_S1_4B:** a small VLM outside the Ling/LLaDA scope, with no outside announcement.
- **NVIDIA:**
  - ESM2 re-uploads (protein LMs, auxiliary);
  - GR00T-N1.7 fine-tunes (fine-tune checkpoints of a catalogued family);
  - Aerial collection, Granary-v2, isaaclab-assets: datasets and assets;
  - rfd4-proteina Space;
  - profile pages.
- **tencent GroupAssistBench:** dataset, plus profile pages.

## Targeted search (11-08 to 11-11)

**Searched for:**
- generic "system card November 2026" (returned only trading-card noise);
- third-party Gemini 4 Carbon evals;
- METR / AISI reports on Mythos 5.2;
- trusted-access programs for November;
- release trackers for 11-09 / 11-10 (Qwen, DeepSeek, Grok, Mistral);
- Kimi K3.1 Pro government evals;
- LSVP expansion.

**Findings:**
- **New, now catalogued:** Gemini 4 Carbon GA (11-10) and its documents (#1, #2).
- **Already in the DB:**
  - Anthropic's UK AISI alignment assessment;
  - the GPT-6 Cyber launch;
  - the CVP and LSVP launch posts;
  - SecureBio's K3.1 Pro report.
- **No new LSVP expansion page found.**
- **Still not published (watch):**
  - METR / UK AISI reports on Mythos 5.2;
  - third-party Gemini 4 Carbon evals;
  - AISI / CAISI work on Kimi K3.1 Pro.
- **Release-tracker hit:** "DeepSeek V4.1 Flash 1017 Uncensored (HeimdaLLM)" is a third-party fine-tune. Skipped.
- **Artificial Analysis "trusted-access models in the Cyber Index":** the publisher is not allowlisted. Skipped.

## Citation mining

- **Fable 5.2 launch-post follow-ups:**
  - project-vend-2 is the Dec 2025 phase-two post (Sonnet 4.0/4.5), so it is before the 2026-01-01 floor. Skipped.
  - The model-hardware-standard post is not linked from the stored launch-post text. It was not pursued.
- **Gemini 4 Carbon card:** led to the safety report (#1).
- **Misalignment hub backlog:** 2 of the 3 deferred reports were added today. The third was stopped by the cap (#7).

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs got 403 again (streaks 20-30).
- **My own fetches:** read_doc got HTTP 200 via browser_impersonation on all four I sampled:
  - path-to-astra
  - low-resource-programming-languages
  - introducing-gpt-rosalind
  - trusted-access-for-cyber
- **Alive check:** all four are alive, so there are no status changes.

## Document updates (task 6)

- **Top 5 (v1056, v773, v924, v1015, v573):** unchanged from earlier runs, which judged them noise or already annotated. Skipped.
- **v1142 (Carbon evaluation PDF, recaptured on 11-11):** substantive wording changes, annotated (#8):
  - cyber results now scoped to Fairwind access;
  - FrontierSWE renamed FrontierSWE 2;
  - CWE-bench attribution revised.
- **v1139 (METR GPT-5):** only a footnote-block reformatting (↩ to ↩︎, plus a "Footnotes" header). Noise, skipped.

## Friction and proposals

Friction:
1. A recurrence of the Phase A openai.com 403 false alarm (of 2026-11-10T06:28:59Z).
2. A new `cap` entry: an in-scope add (#7) was rejected and deferred for the second time.

No proposal was filed. The add cap's interaction with backlog catch-up is already covered by the 2026-08-09 and 2026-09-23 PROPOSALS.md entries.
