# Standing report, 21 November 2026 snapshot: cyber access policies at Anthropic, OpenAI and Google changed scope again without a change log, OpenAI's GPT-6 Astra card revised four times with notice, and a biology score understated 3.7-fold across five OpenAI documents

As of the 2026-11-21 snapshot, cardtrack holds 1,145 versions of 458 documents from 35 publishers. 119 version pairs are substantive publisher edits; 57 carry the safety flag set by the classifier, a language-model sub-agent that labels every diff. A-ids index the appendix; vN are stored version ids. Ranked by consequence for a safety reader:

1. **Cyber access gating: Anthropic's Cyber Verification Program (CVP), OpenAI's Daybreak, Google's Fairwind** ([CVP article](https://systemcards.org/docs/anthropic-claude-opus-access-policy.html), A44 to A112; [Claude Mythos page](https://systemcards.org/docs/anthropic-claude-mythos-5-1-access-policy.html), A68 to A101; [Daybreak overview](https://systemcards.org/docs/openai-gpt-5-6-sol-access-policy.html), A40 to A116; [Fairwind Program](https://systemcards.org/docs/google-deepmind-gemini-4-argon-access-policy-2.html), A87, A113). These programmes decide who gets frontier models with cyber refusals reduced. The four pages hold 19 of the 119 edits and 18 of the 57 safety-flagged ones; none logs its edits, and the CVP article still reads "Updated October 6, 2026" after its 15 November rewrite (v1045→v1188). That rewrite named Mythos 5.2 (announced 10 November, A101), added seat caps and per-tier evidence requirements, kept the US-government review for Specialized Access, and deleted the section "Why might an organization not have access?", Anthropic's stated reasoning, which had promised "a more cautious approach" for customers serving "military, intelligence, or law enforcement". OpenAI (v1027→v1237) opened GPT-5.6 Cyber to every Daybreak Red organisation, where it had needed separate approval, added GPT-6 Cyber under separate approval and GPT-6.2 Astra and Sol, and restricted GPT-5.5-Cyber to existing holders.
2. **GPT-6 Astra System Card, OpenAI** ([document](https://systemcards.org/docs/openai-gpt-6-astra-system-card.html); A38, A50, A61, A99). Most-revised system card: four dated change-log revisions since the 3 September launch. The alignment section was renamed and hedged, a comparison plot removed, a HealthBench score corrected, and appendices added covering two further models and the always-on GPT-6 Astra agents OpenAI calls "dots", including monitor-evasion results.
3. **GPT-5.5 protein-binding score, five OpenAI documents** ([GPT-5.5 card](https://systemcards.org/docs/openai-gpt-5-5-system-card.html), v8→v387, A19; also A4, A11, A14, A22). The pass@4 row of the hard-negative protein-binding evaluation (pass@k: success within k attempts) carried the pass@1 value, 0.4%, from the 23 April card until a change log dated 19 August replaced it with 1.48%. The error understated capability; the corrected value stays below GPT-5.4-thinking's 3.46%.
4. **Gemini 4 Argon Safety & Security Report, Google DeepMind** ([document](https://systemcards.org/docs/google-deepmind-gemini-4-argon-system-card.html), v834→v901, A77). The only edited system card or safety report in the corpus with no change log: published 13 October, changed by 21 October, no revision date. A footnote on "we avoid training directly against our monitors" now cross-references a disclosure that early reinforcement-learning runs let a reward-hacking penalty read the model's thoughts. "We mitigated as if at CCL regardless" (Critical Capability Level) left the CBRN (chemical, biological, radiological, nuclear) evaluation-awareness subsection.
5. **Capability scores changed after publication** ([Muse Wonder card](https://systemcards.org/docs/meta-muse-wonder-model-card.html), v815→v973, A84; [SecureBio report](https://systemcards.org/docs/securebio-gpt-6-astra-independent-eval.html), v569→v1030, A91; [Inkling 2 Small card](https://systemcards.org/docs/thinking-machines-inkling-2-small-model-card.html), v1163→v1239, A117). Meta's ExploitGym value fell from 92 to 20 after a harness fix and SecureBio's World-Class Biology score for GPT-6 Astra from 61.6% to 59.2%, both with dated notes. Thinking Machines rescored the whole 13-model Tax Agent Bench row without a note (Inkling 2 Small 65.8 to 38.9), the card's second score revision without a note in a week (A109, the open-weights release).
6. **Claude Fable 5.2 announcement, Anthropic** ([document](https://systemcards.org/docs/anthropic-claude-fable-5-2-access-policy.html), v1121→v1206, A115). A dated "Edit 11 November" withdrew the claim that 1,000 Fable 5.2 agents formalised Fermat's Last Theorem using "no mathematical references"; a footnote now says they were given 60 statements, a route sketch, definitions and 47 proved lemmas.

| Cyber access step (detected) | Page, versions (A-id) | What changed |
|---|---|---|
| 2026-09-26 | Daybreak v563→v646 (A52) | Tier matrix: Blue gives reduced refusals on GPT-5.5, GPT-5.6 Sol, GPT-6 Sol and Luna; Red adds GPT-5.5-Cyber and Astra; GPT-5.6-Cyber needs separate approval; FIDO2 key rule |
| 2026-09-29 | CVP article v581→v671 (A57) | Safeguards article "doesn't apply to Claude Opus 5.5 or Sonnet 5.5": no verification route yet for the newest models |
| 2026-10-08 | CVP article v671→v774 (A66); Mythos page v678→v780 (A68) | Three tiers covering Opus 5.5, Sonnet 5.5 and Mythos 5.1; US-only caveat removed |
| 2026-10-18 | Daybreak v742→v869 (A76) | GPT-6.1-Sol and Astra Minor added; the separate-approval row leaves the tier list |
| 2026-10-28 | Fairwind v835→v1001 (A87) | "Fill in our form" becomes "contact your Cloud account team" |
| 2026-10-31 | Daybreak v869→v1027 (A90) | GPT-6.1 Terra: reduced refusals only when set per request |
| 2026-11-10 | Mythos page v1049→v1116 (A101) | Retitled Mythos 5.2; price cut; Fable 5.1 safeguard specifics dropped |
| 2026-11-15 | CVP article v1045→v1188 (A112) | Mythos 5.2 named in every tier; eligibility-factors section deleted; seat caps of 75 (Red Team) and 25 (Specialized) |
| 2026-11-16 | Fairwind v1047→v1193 (A113) | "Gemini 4 Argon" becomes "Gemini for cyber models"; "over 650" becomes "thousands of partners" |
| 2026-11-19 | Daybreak v1027→v1237 (A116) | GPT-5.6 Cyber for all Red organisations; GPT-6 Cyber under separate approval; GPT-6.2 Astra and Sol added; GPT-5.5-Cyber deprecated 2027-02-01 |

![Substantive edits to access-policy pages by detection date. The CVP article and the Daybreak overview were each edited about every two weeks from mid-September.](figures/fig_access_timeline.png)

## Corrections: 14 published numbers changed after publication, 7 without any note

![The 13 numeric corrections with a legible before and after value, as relative change. Not charted: Google's rate revisions (A77) and three Grok 4.6 scores whose old values are not printed. The six without a note: three Hugging Face cards, one Mistral announcement, one Thinking Machines card.](figures/fig_corrections.png)

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
| A117 | Thinking Machines Inkling 2 Small model card | 2026-11-05 | none | 2026-11-19 |

- The classifier flags 28 pairs as corrections; the non-numeric ones change wording: Anthropic's Fermat claim (A115); Redwood's "we argue that this achieves near-maximal safety" became "we speculate" (A74); METR's "all vulnerabilities patched" became "most patched, one fix in progress" after feedback from OpenAI (A89).

## Where edits happen: 87 of 458 tracked documents, access policies most volatile, system-card edits from two publishers only

| Document type | Tracked | With a substantive edit | Substantive edits | Safety-flagged edits |
|---|---|---|---|---|
| Model card | 167 | 47 (+2 since removed, A16, A21) | 61 | 10 |
| Independent evaluation | 109 | 17 | 17 | 10 |
| Other (blogs, incident reports) | 99 | 5 | 5 | 5 |
| Access policy | 37 | 11 | 26 | 22 |
| System card | 35 | 6 | 9 | 9 |
| Addendum | 11 | 1 | 1 | 1 |

- All nine system-card edits are safety-flagged and come from OpenAI (8) and Google DeepMind (1).
- Model-card edits are mostly serving recipes, training-content links and licence notes; Xiaomi added "Use Restrictions" sections barring military and malicious-cyber use to three cards (A96, A97, A104). Google's [Gemini 4 Hydrogen card](https://systemcards.org/docs/google-deepmind-gemini-4-hydrogen-model-card.html) (A118) swapped four "coming soon" placeholders for links once its safety report appeared.
- 22 of OpenAI's misalignment incident reports gained training-data canary strings, detected 12 to 18 November; on 21 November all 24 tracked alignment.openai.com pages moved to openai.com/safety-alignment.

![Substantive edits per detection week. 10 of the 28 corrections fell in the first two weeks, half of them OpenAI's protein-binding fix.](figures/fig_timeline.png)

## Tracker reliability: outage-free since 22 September; openai.com answered its first probe in 50 days on 21 November; Hugging Face rate-limits a quarter of content re-checks

| Measure (whole history unless stated) | Value |
|---|---|
| Daily runs / monitor outages (every link check errored; last one 22 September) | 108 / 22 |
| Clean runs since the last outage | 64 |
| Documents reachable in every valid probe, of all documents ever probed | 418 of 484 |
| Consecutive days on which every openai.com probe got HTTP 403, 2 October to 20 November | 50 |
| openai.com and help.openai.com pages answering the 21 November probe | 22 of 22 |
| Content re-checks of those hosts answered 403: whole history / since 1 November / since 15 November | 31 of 196 / 22 of 54 / 1 of 21 |
| alignment.openai.com pages redirected permanently to openai.com on 21 November; move recorded the same day | 24 |
| Hugging Face content re-checks answered HTTP 429 (rate limited): since 29 September / since 1 November / since 15 November | 222 of 820 / 98 of 319 / 16 of 113 |
| Hugging Face cards with no successful content fetch in the last 14 days | 9 of 104 |
| Proposals rejected as unretrievable after HTTP 429 | 19 |
| Pages ever serving a redirect stub with HTTP 200 / a permanent redirect / a 404 | 2 / 37 / 2 |
| Content re-check gap, median / 90th percentile (days) | 6.1 / 12.4 |
| Discovery lag, median days: all (n=204) / citation-led (n=21) | 1.3 / 19.7 |

- One run is not a trend; the cause may be OpenAI's edge or the tracker's exit address. 19 of the 22 pages had a successful content read within the previous ten days.
- Palisade's two reports (A33, A34) served a redirect stub with HTTP 200 from 6 September; the move was recorded 17 days later.
- The tracker's own per-pair note "extractor drift, not a publisher deletion" was wrong on three of the seven pairs carrying it this week, including the Daybreak rewrite (A116); a wrong note hides a substantive edit.

![Link-probe outcome per document and daily run. Grey columns are monitor outages. Orange: every openai.com probe refused from 2 October to 20 November. Purple: permanent redirects, three Anthropic URL renames from October and 24 alignment.openai.com pages on 21 November.](figures/fig_heatmap.png)

## Method, caveats and provenance

- Source: a read-only snapshot of the cardtrack database taken 2026-11-22T02:00Z; last daily run 21 November. Numbers trace to `out/results.json`, `out/standing_figs.json`, the tables above and queries recorded in `out/RUN_SUMMARY.md`.
- Every consecutive version pair is diffed on extracted text and labelled by the classifier (655 pairs; 537 high, 110 medium, 8 low confidence). 40 pairs are the tracker's own URL migrations and are excluded. Substantive means content minor, content major or replacement. 34 labels carry verified overrides from raw-capture checks.
- The safety flag is the classifier's; the ranking rests on diffs read by the author (items 2 to 4 in earlier runs of this report). Change dates are detection dates and lag the edit by up to one re-check interval.
- Outage runs are excluded from availability statistics. Hugging Face hosts 104 tracked documents; a 429 on re-check hides an edit for weeks.
- Written by Claude Fable 5.1 without human review.

## Appendix: every substantive change, A1 to A119

Version ids are `document_versions` rows; summaries are the classifier's text.

