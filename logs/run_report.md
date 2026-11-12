# cardtrack agent run — 2026-11-12 (run id 2026-11-12T06:17Z-local)

- **Lookback:** the last agent success was 2026-11-11T06:27:34Z, so the 72 h minimum applied (2026-11-09 to 11-12).
- **Weekly retrospective sweep:** not run. It is a Thursday.
- **Open issues:** `fetch_ok: true` with no open issues, so task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | OpenAI misalignment report "Signing up for disposable emails and searching GitHub for leaked API keys" (`other`, 09-16). Tagged cyber, loss_of_control; `restricted`. Cap-deferred on 11-10 and 11-11. | **written**: `openai-openai-internal-research-model-other-11` (doc 460) |
| 2 | "Daybreak Red is now available in AWS GovCloud (US-East)" (`access_policy`, 11-04, GPT-5.6 Cyber). No tags; `restricted`. AWS What's New copy recorded as `co_published`. | **written**: `openai-gpt-5-6-cyber-access-policy` (doc 461) |
| 3 | "A thousand fewer paths to root" (`other`, 11-04): GPT-6 Cyber's Linux kernel pipeline, with 948 LPE exploits, 1,724 reproduced vulnerabilities, kernelCTF results and costs. Tagged cyber; `restricted`. | **written**: `openai-gpt-6-cyber-other` (doc 462) |
| 4 | "Securing our frontier model training environment" (`other`, 10-23): a red-team of OpenAI's training containment using GPT-6 Astra Cyber and an internal frontier model, covering microVM escapes, egress and covert channels. Tagged cyber, loss_of_control; `restricted`. | **written**: `openai-gpt-6-astra-cyber-other` (doc 463) |
| 5 | "Measuring how AI agents handle everyday wet-lab science" (BioBasicsBench, `other`, 11-06): results for 7 named OpenAI models. `has_safety_evals: false`, no tags; `closed`. | **written**: `openai-gpt-6-astra-other-6` (doc 464) |

Every proposed document was fetched and read with read_doc before proposing.

**Calls worth checking:**
- **#1, URL:** the slug is `searching-github-for-leaked-api-keys`, not a slug built from the title. The title-based guess returned 404. The real URL came from yesterday's cap friction entry.
- **#2-#5, dates:** the extracted text of openai.com/index pages carries no date. All four dates come from `<pubDate>` in openai.com/news/rss.xml. For #2, AWS's own What's New item is dated 10-30, but OpenAI's post is 11-04.
- **#3, model name:** the post only says "an upcoming cyber model". GPT-6 Cyber's 11-05 launch post says it produced the 948 Linux exploits, which is how the model was identified.
- **#4, name and openness:** the post names "GPT-6 Astra Cyber", which I used verbatim. It may be the pre-launch name of GPT-6 Cyber, so the operator may want to normalize it. Red-team results are mostly qualitative (CVEs, channel types, no success rates).
- **#5, scope:** admitted under the precedent of `openai-gpt-6-astra-other-2` (low-resource programming languages), which is also a capability eval of named models. It is not tagged cbrn: the tasks are routine lab analysis, with only a closing biosafety remark.

## Phase A candidates (first seen 11-12)

Earlier candidates were triaged in previous runs. The deferred #7 from 11-11 was re-proposed (#1).

**Skipped:**
- **AlphaGenome 2 (DeepMind blog):** a DNA-sequence prediction model. Per covered_model_class it is an auxiliary/domain model with no safety evals.
- **Grok Bot 1.0 (xAI, 11-02):** a product/agent feature launch with no model documentation.
- **nvidia/Kimi-K3.1-Pro-NVFP4 and its discussion:** a quantized re-upload of a catalogued model.
- **inclusionAI ZoomGain-4B/9B, GGUFs, collection, datasets, bench:** research VLM checkpoints for a perception paper, outside the Ling/LLaDA scope, with no outside coverage.
- **MiniMax-H3-Image discussions:** an image model, out of scope per the scope note.
- **tencent KaLM-Embedding discussion:** an embedding model.
- **Profile pages:** YanshekWoo, juhim, elvischenv, SZhanZ.

## Targeted search (11-09 to 11-12)

**Searched for:**
- generic system-card / model-card releases for November;
- METR / AISI / CAISI reports;
- trusted-access programs (LSVP/CVP, Daybreak, Rosalind, Gemini Flash Cyber, CodeMender);
- the silent orgs xAI, Z.ai, US CAISI and Palisade.

**Already in the DB:**
- Fable/Mythos 5.2 documents;
- Gemini Omni 1.2 Flash card;
- ChatGPT Images 2.6 and GPT-Rosalind-6 cards;
- METR's 11-05 Anthropic AI R&D assessment;
- CAISI's GLM-5.3 report;
- Palisade's two 2026 reports.

**Skipped:**
- **Qwen4-Max-Preview (11-11):** coverage says no model card or tech report exists yet. Watch.
- **Grok 4.8:** reported trained but not announced. Watch.
- **GLM-5.4/5.5:** not announced.
- **ERNIE 5.5 Flash Preview:** Baidu is not allowlisted.
- **Anthropic FlashProve:** a provable-inference cryptography prototype, not model documentation.

**The main finding came from the OpenAI news RSS feed (openai.com/news/rss.xml).** It fetches directly and gives exact pubDates. Sweeping it from 10-21 to 11-12 found #2-#5. Other posts read and skipped:
- **broad-access-through-consistent-standards (10-21):** a partner/usage-policy update that names no gated model.
- **empowering-cyber-defenders (10-21):** a policy blueprint.
- **coordinated-disclosure-of-critical-vulnerabilities (10-21):** a PHP disclosure framework, not an evaluation.
- **scaling-ai-research-for-complex-biological-data:** a GPT-Rosalind showcase with no measured evaluation.
- **lifeval (11-02):** a benchmark intro with no named-model numbers in the text.
- **grid-protectors-program; control-room:** infrastructure.
- **daybreak-for-frontline-defenders (09-04):** an access subsidy program, but it names no model, only "Daybreak cyber models". It fails the named-model gate.

## Citation mining

- **GPT-6 Cyber launch post:** confirmed the model behind #3. It also cites 81 Firefox vulnerabilities (a Mozilla advisory, not allowlisted).
- **PHP disclosure post:** led to Daybreak for Frontline Defenders (skipped, see above).
- **Securing-environment post (#4):** cites the DNS-escape misalignment report, which is already catalogued and recorded as a related URL.

## Blocked-URL escalations (task 5)

- **Phase A:** the same 16 openai.com / help.openai.com URLs got 403 again (streaks 21-30).
- **My own fetches:** read_doc got HTTP 200 via browser_impersonation on three of them:
  - hugging-face-model-evaluation-security-incident;
  - the Daybreak help article;
  - pacing-model-development-cyber-capabilities.

  Ten other openai.com/index pages also returned 200 today.
- **Alive check:** all alive, so there are no status changes.

## Document updates (task 6)

- **Top 5 (v1056, v773, v924, v1015, v573):** unchanged stale entries that earlier runs judged as noise or already annotated. Skipped.
- **v1150 (METR GPT-5.5, the only version new today):** footnote back-arrow ↩ to ↩︎ plus an added "Footnotes" header. This is the same METR template change as v1139. Noise, skipped. No annotations proposed.

## Friction and proposals

Friction (4 entries):
1. `index_gap`: 4 OpenAI documents missed by Phase A. The RSS feed is the fix.
2. `diff_noise`: METR footnote variation-selector versions.
3. A recurrence of the openai.com 403 false alarm.
4. A recurrence of the stale updated_docs top-5.

Proposal filed: "Watch openai.com/news/rss.xml: plain-fetchable, dated, would have caught 4 missed OpenAI documents". It updates the existing 2026-08 openai.com/news index request with a concrete working URL.
