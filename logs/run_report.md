# cardtrack agent run — 2026-11-14 (run id 2026-11-14T06:16Z-local)

- **Lookback:** last agent success 2026-11-13T06:25:33Z, so the 72 h minimum applied (2026-11-11 to 11-14).
- **Weekly retrospective sweep:** not run (Saturday).
- **Open issues:** `fetch_ok: true`, no open issues; task 4 had nothing to do.

## Proposals (validator verdicts)

| # | Proposal | Verdict |
|---|---|---|
| 1 | field_update `related_urls` on `far-ai-claude-fable-5-independent-eval` (doc 187), adding `full_document` = leaderboard.far.ai/docs/report.pdf. It is the full technical report ("AI Security Leaderboard: Methodology, Results and Minimal Standard", July 2026) behind the 07-29 blog row: same four models, same jailbreak counts and costs. Found by citation mining. | **written** |
| 2 | field_update `related_urls` on `anthropic-claude-mythos-preview-system-card` (doc 5), adding `full_document` = anthropic.com/claude-mythos-preview-system-card. The stored canonical is the Apr 7 launch-edition hash. The named URL serves the revised edition, with changelog entries for Apr 8 (misattributed quote removed, Eleos findings corrected) and Apr 14 (an AI-acceleration note removed). | **written** |

No adds today. Everything was fetched with read_doc before proposing.

**Calls worth checking:**
- **#1:** the titles differ (blog announcement vs full report). I chose a `full_document` link over a second row; if the operator would rather not promote the PDF, `paper` is the alternative kind.
- **#2:** this applies the 2026-08-18 PROPOSALS.md "superseded edition" entry to one row. Opus 4.6 was checked the same way. Its named URL resolves to the same content hash (6a5fa276) as the stored canonical, so no change was needed.

## Phase A candidates (new today, first_seen 11-14)

- **Anthropic transparency page (16 assets.claude.com PDFs):** CDN copies of cards already in the DB: Fable 5 / Mythos 5, Fable 5.1 / Mythos 5.1, Mythos Preview (revised edition, see #2), Opus 4.6, Sonnet 4.6, Opus 5, the Mythos Preview alignment risk update, and the Feb risk report. The rest were the pre-floor 2025 Claude 4 and Opus 4 / Sonnet 4 cards, plus the RSP, which is a policy rather than model documentation. I spot-read 4 to confirm identity. Skipped as mirrors, out of scope or pre-floor; logged as friction (CDN migration noise).
- **Anthropic "Building strong safety evaluations":** a general methods essay that uses system-card examples but evaluates no named model. Skipped.
- **Epoch "Incident report: AI agents attempted exploits on our website":** describes Trajectory Labs' alignment-eval agents probing epoch.ai. It explicitly names no model or developer, so it fails the named-model test. Skipped. Worth re-checking if Trajectory or a lab later attributes the incident.
- **DeepSeek news261113 and build_a_chatbot:** an API feature launch (search, files, safety checks for V4.1-Flash). Product launch with no model documentation. Skipped.
- **Other skips:**
  - Cursor security-incident update (supply-chain incident, not a model);
  - Thinking Machines 4-bit training (research);
  - DeepMind weather datasets;
  - NVIDIA: the Nemotron-3.5-Parse discussion (OCR, auxiliary), dvlt (image-to-3D), the TTB paper, the SimReady blog, a dataset discussion;
  - inclusionAI Duo-1.0 / 1.2 checkpoints (research full-duplex models outside the Ling/LLaDA scope; the paper was skipped yesterday);
  - the luguoshan profile page.
- **Older candidates:** triaged in earlier runs.

## Targeted search (11-11 to 11-14)

- **OpenAI** (news RSS since 11-13): only ChatGPT Wallet and customer stories. Nothing to propose.
- **Anthropic** news index: nothing new since Fable/Mythos 5.2 and the S-1 filing.
- **DeepMind** model-card index: Hydrogen (in DB) is the newest. The **Gemini 4 Hydrogen Safety & Security Report is still "coming soon"**; keep watching.
- **xAI** news: no Grok 4.8 announcement yet.
- **Qwen4-Max-Preview:** still no card. **Tencent Hy4 official (11-04):** `huggingface.co/tencent/Hy4` still returns 401 and coverage says the weights and system card are "due in the coming days". Watch it; only the Hy4 Preview is in the DB.
- **Trusted-access programs** (Daybreak, CVP, Glasswing, LSVP, Fairwind): nothing new beyond catalogued items. Anthropic's 11-12 regional-availability rule (mainland China) is a usage policy, not a named-model access program.
- **Independent evaluators** (METR, AISI, CAISI, Apollo, SecureBio, FAR, Palisade, Transluce): nothing new found.
- **IBM Granite 4.1 previews (11-13):** IBM is not on the allowlist. Skipped.
- **Watch next:** Grok 4.8, Qwen 4 Max (~11-16), Muse Spark 1.4 (~11-19), Hydrogen S&S report, Hy4 weights and card.

## Citation mining

- **FAR.AI Kimi K3.1 Pro stress test (11-09):**
  - It cites the DeepSeek-V4-Pro stress test (already catalogued).
  - The July Kimi K3 test seems never to have been published separately (it isn't on far.ai search).
  - The Leaderboard full report PDF was linked as #1.
- **Recent Gemini 4 and SecureBio adds:** mined yesterday.

## Blocked-URL escalations (task 5)

- **Phase A:** 403 on the same 16 openai.com / help.openai.com URLs (streaks 23-30), plus 4 at streak 2.
- **My own fetches:** read_doc fetched path-to-astra and daybreak-red-aws-govcloud with HTTP 200 via browser impersonation today, so yesterday's read_doc regression appears transient.
- **Alive check:** the RSS feed still lists the posts. All are alive and bot-blocked; no status changes.

## Document updates (task 6)

- **v1056, v773, v924, v1015:** the stale entries earlier runs judged as noise or already handled. Skipped.
- **v1170 (DeepSeek-V4.1-Flash-1017 HF card, new today, position 3):** pure HF furniture (inference-widget snippets switched to chat/image examples, download and Space counts, community leaderboard links). Skipped as noise.
- No annotations today.

## Friction and proposals

Friction (3 entries):
1. A recurrence of the OpenAI Phase A 403s, noting that read_doc works again.
2. A recurrence of the stale updated_docs top 5.
3. `other`: the Anthropic CDN migration to assets.claude.com flooded candidates with copies of existing rows.

No new PROPOSALS.md entry. The superseded-edition and canonical-URL issue is already filed (2026-08-18).
