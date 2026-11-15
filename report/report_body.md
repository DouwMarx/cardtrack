# Standing report, 14 November 2026 snapshot: OpenAI's GPT-6 Astra card revised four times with notice, Google's Gemini 4 Argon safety report once without, and a biology score understated 3.7-fold across five OpenAI documents

As of the 2026-11-14 snapshot, cardtrack holds 1,051 versions of 435 documents from 34 publishers, watched by 101 daily runs since 11 August. 110 version pairs are substantive publisher edits; 53 carry the safety flag set by the classifier, a language-model sub-agent that labels every diff. A-ids index the appendix; vN are stored version ids. Ranked by consequence for a safety reader:

1. **GPT-6 Astra System Card, OpenAI** ([document](https://systemcards.org/docs/openai-gpt-6-astra-system-card.html); A38, A50, A61, A99). The most-revised system card in the corpus: four dated change-log entries since the 3 September launch (table below). The alignment section was renamed and hedged, a comparison plot removed, a HealthBench score corrected, and appendices added covering two further models and the "dots" always-on agents, including monitor-evasion results. Disclosed, but a reader of the launch PDF holds a different document.
2. **GPT-5.5 protein-binding score, five OpenAI documents** ([GPT-5.5 card](https://systemcards.org/docs/openai-gpt-5-5-system-card.html), v8→v387, A19; also A4, A11, A14, A22). The pass@4 row of the hard-negative protein-binding evaluation (pass@k: success within k attempts) carried the pass@1 value, 0.4%, from the 23 April card until a change log dated 19 August replaced it with 1.48%. It stood four months in the GPT-5.5 card, less in three later cards and an addendum; the corrected value stays below GPT-5.4-thinking's 3.46%.
3. **Gemini 4 Argon Safety & Security Report, Google DeepMind** ([document](https://systemcards.org/docs/google-deepmind-gemini-4-argon-system-card.html), v834→v901, A77). The only edited system card or safety report in the corpus with no change log: published 13 October, captured 14 October, changed by 21 October, cover still "October 2026". The edits are small. A footnote on "we avoid training directly against our monitors" now cross-references a disclosure already in the document that early reinforcement-learning runs let a reward-hacking penalty read the model's thoughts. "We mitigated as if at CCL regardless" (Critical Capability Level) left the CBRN (chemical, biological, radiological, nuclear) evaluation-awareness subsection, which already says the biological CCL cannot be ruled out. Evaluation-awareness rates changed with their denominators (35% of flagged runs to 37.8% of all runs in coding honeypots; 10%/11% to 8%/10% on new tasks).
4. **Cyber access gating, Anthropic and OpenAI** ([cyber safeguards article](https://systemcards.org/docs/anthropic-claude-opus-access-policy.html), 6 edits, A44 to A93; [Claude Mythos page](https://systemcards.org/docs/anthropic-claude-mythos-5-1-access-policy.html), 4 edits, A68 to A101; [Daybreak overview](https://systemcards.org/docs/openai-gpt-5-6-sol-access-policy.html), 5 edits, A40 to A90). None carries a change log; these 15 edits include 14 of the 53 safety-flagged ones. On 29 September Anthropic's article said it "doesn't apply to Claude Opus 5.5 or Sonnet 5.5" (v581→v671): no verification route to reduced cyber refusals yet existed for the newest models. By 8 October it had three tiers covering them and Mythos 5.1 (v671→v774). The Mythos 5.2 retitle (v1049→v1116, 10 November) cut the price, let eligible Cyber Verification Program customers keep zero data retention and dropped the Fable 5.1 safeguard specifics; the hedge "in an effort to ensure" added on 21 October (v780→v904) went with it. Daybreak relaxed its hardware-key rule (v646→v742) and changed tier coverage three times (A52, A76, A90).
5. **Capability scores corrected after evaluation errors** ([Muse Wonder card](https://systemcards.org/docs/meta-muse-wonder-model-card.html), v815→v973, A84; [SecureBio report](https://systemcards.org/docs/securebio-gpt-6-astra-independent-eval.html), v569→v1030, A91). Meta's ExploitGym table value fell from 92 to 20 after a harness fix; SecureBio's World-Class Biology score for GPT-6 Astra fell from 61.6% to 59.2% because web search had been enabled. Both carry dated notes and keep their risk conclusions.
6. **Detected in the runs of 9 to 14 November.** Google's [Gemini 4 Carbon evaluation PDF](https://systemcards.org/docs/google-deepmind-gemini-4-carbon-other.html) (v1019→v1142, A108) now says its cybersecurity results "reflect performance when accessed through the Fairwind Program", its trusted-access route. METR's [assessment of AI R&D acceleration at Anthropic](https://systemcards.org/docs/metr-claude-mythos-preview-independent-eval.html) (v1075→v1165, A110) corrected item 1.1 of the AI Evaluator Forum's AEF-1 checklist, "sufficient technical access", from Yes to No. Thinking Machines' [Inkling 2 Small card](https://systemcards.org/docs/thinking-machines-inkling-2-small-model-card.html) (v1073→v1163, A109) went open-weights with revised benchmark values and a conclusion that it "did not present risk of material uplift" beyond open-weight models; no note.

| GPT-6 Astra card revision (change-log date) | Versions | What changed | Detected |
|---|---|---|---|
| 9 September (A38) | v500→v551 | "Metagaming and Alignment Faking" renamed "Verbalized Metagaming and Oversight Gaming"; metric comparison plot removed; generalisation caveats added | 2026-09-12 |
| 22 September (A50) | v551→v620 | HealthBench values corrected after a misconfiguration (Professional 63.4 to 64.7); 35-page Appendix A on GPT-6 Sol and Luna; updated alignment evaluations | 2026-09-24 |
| 29 September (A61) | v620→v720 | 20-page Appendix B on "dots" always-on agents: prompt-injection red-teaming, monitor evasion, preparedness, safeguards | 2026-10-03 |
| 30 October (A99) | v720→v1057 | SecureBio's World-Class Biology score 61.6% to 59.2%; Preparedness text updated | 2026-11-04 |

## Corrections: 12 published numbers changed after publication, 5 without any note

![Every numeric correction verified in the diffs, as relative change of the printed value. The five without a note: four Hugging Face open-weight cards, one Mistral announcement.](figures/fig_corrections.png)

| Id | Document | Published | Note in document | Detected |
|---|---|---|---|---|
| A19 | OpenAI GPT-5.5 System Card (same fix in A4, A11, A14, A22) | 2026-04-23 | change log, 2026-08-19 | 2026-08-25 |
| A12 | xAI Grok 4.6 model card | 2026-08-12 | changelog, revision 2026-08-17 | 2026-08-22 |
| A6 | NVIDIA VoiceChat 11B model card | 2026-08-03 | none | 2026-08-20 |
| A2, A18 | inclusionAI Ling-3.0-tiny model card | 2026-08-10 | none | 2026-08-19, 2026-08-25 |
| A42 | Anthropic alignment assessment of cyber incidents | 2026-09-09 | correction note, 2026-09-10 | 2026-09-16 |
| A50 | OpenAI GPT-6 Astra System Card | 2026-09-03 | change log, 2026-09-22 | 2026-09-24 |
| A56 | inclusionAI Ling-3.0-flash-VL model card | 2026-09-04 | none | 2026-09-28 |
| A71 | Mistral Large 4 announcement | 2026-10-06 | none | 2026-10-14 |
| A77 | Google DeepMind Gemini 4 Argon safety report (rates, denominators changed; not in figure) | 2026-10-13 | none | 2026-10-21 |
| A81 | Epoch AI CVE post | 2026-07-31 | undated revision note | 2026-10-25 |
| A84 | Meta Muse Wonder model card | 2026-10-12 | update note, 2026-10-23 | 2026-10-26 |
| A91 | SecureBio GPT-6 Astra report | 2026-09-14 | correction banner, October 2026 | 2026-11-01 |

- The classifier flags 26 pairs as corrections; the non-numeric ones change wording: Redwood softened "we argue this achieves near-maximal safety" to "we speculate" (A74); METR changed "all vulnerabilities patched" to "most patched, one fix in progress" at OpenAI's request (A89); Anthropic corrected what a URL-length limit protects against (A75).
- xAI's [Grok 4.6 card](https://systemcards.org/docs/xai-grok-4-6-model-card.html) (v236→v357, A12) lists "Corrected eval results on HackerBench v0.2, Self-harm, MASK, LAB" without the old values; only HackerBench's is legible.

## Where edits happen: 82 of 435 documents, access policies most volatile, system cards only from two publishers

| Document type | Tracked | With a substantive edit | Substantive edits | Safety-flagged edits |
|---|---|---|---|---|
| Model card | 156 | 43 | 56 | 9 |
| Independent evaluation | 104 | 17 | 17 | 10 |
| Other (blogs, incident reports) | 97 | 5 | 5 | 5 |
| Access policy | 34 | 10 | 22 | 19 |
| System card | 33 | 6 | 9 | 9 |
| Addendum | 11 | 1 | 1 | 1 |

- All nine system-card edits are safety-flagged and come from OpenAI (8) and Google DeepMind (1). Two edited model cards were later removed from the corpus (A16, A21).
- Model-card edits are mostly serving recipes, training-content links and licence notes; Xiaomi added "Use Restrictions" sections barring military and malicious-cyber use to three cards (A96, A97, A104).

![Substantive edits per detection week. 10 of the 26 corrections fell in the first two weeks, as OpenAI's protein-binding fix propagated. Weeks before 28 September lost 2 to 4 runs to outages.](figures/fig_timeline.png)

![Four pages hold 19 of the 110 edits and 18 of the 53 safety-flagged ones: two cyber access-policy pages, the Mythos page and the Astra card.](figures/fig_edits_by_doc.png)

## Tracker reliability: outage-free since 22 September, but openai.com blocks every probe and Hugging Face rate-limits a third of content re-checks

| Measure (whole history unless stated) | Value |
|---|---|
| Daily runs / monitor outages (every link check errored; last one 22 September) | 101 / 22 |
| Clean runs since the last outage | 57 |
| Documents reachable in every valid probe, of all documents ever probed | 427 of 463 |
| openai.com and help.openai.com pages whose probe gets HTTP 403 (blocked), since 13 November | 20 of 20 |
| Content re-checks of those hosts answered 403: whole history / week of 2 November | 30 of 145 / 14 of 17 |
| Hugging Face content re-checks answered HTTP 429 (rate limited): since 29 September / since 1 November | 206 of 707 / 82 of 206 |
| Hugging Face cards with no successful content fetch in the last 14 days | 10 of 98 |
| Proposals rejected as unretrievable after HTTP 429 | 14 |
| Pages serving a redirect stub with HTTP 200 / permanent redirects / 404 | 2 / 11 / 2 |
| Content re-check gap, median / 90th percentile (days) | 6.3 / 12.5 |
| Discovery lag, median days: all (n=185) / citation-led (n=20) | 1.3 / 23.0 |

- Palisade's shutdown-resistance and self-replication reports ([one](https://systemcards.org/docs/palisade-research-grok-4-grok-4-0709-independent-eval.html), v195→v509, A34) served a two-line redirect stub with HTTP 200 from 6 September; the move was recorded 17 days later.
- Four OpenAI pages added on 12 November were probe-blocked from their first check. Citation-led finds include nine OpenAI internal misalignment incident reports found 26 to 57 days after publication; eight gained training-data canary strings between 9 and 14 November.
- The monitor's "extractor drift, not a publisher deletion" note was wrong on both pairs carrying it (A105, A109).

![Link-probe outcome per document and daily run. Grey columns are monitor outages, all before 23 September. Every openai.com probe has been refused since 2 October; purple rows are redirects.](figures/fig_heatmap.png)

## Method, caveats and provenance

- Source: a read-only snapshot of the cardtrack database taken 2026-11-15T02:00Z; last daily run 14 November. Numbers trace to `out/results.json`, `out/standing_figs.json` and the tables above.
- Every consecutive version pair is diffed on extracted text and labelled by the classifier (584 pairs; 473 high, 103 medium, 8 low confidence). 37 pairs are the tracker's own URL migrations and are excluded. Substantive means content minor, content major or replacement. 29 labels carry verified overrides from raw-capture checks.
- The safety flag is the classifier's; the ranking rests on diffs read by the author. Change dates are detection dates and lag the edit by up to one re-check interval.
- Outage runs are excluded from availability statistics. Hugging Face hosts 98 tracked documents; a 429 on re-check hides an edit for weeks.
- Written by Claude Fable 5.1 without human review.

## Appendix: every substantive change, A1 to A110

Version ids are `document_versions` rows; summaries are the classifier's text.

