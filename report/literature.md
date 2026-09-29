# Literature baselines: link rot, content drift, bot blocking, AI-doc edits

Compiled 2026-09-22. Figures checked against primary text where marked [P]; [S] = taken from a secondary summary or fetch summary, not re-read in the primary. Numbers are quoted as reported; nothing is extrapolated except in the last section, which is labelled as derived.

## 1. Link rot over time

1. Zittrain, J., Albert, K., Lessig, L. (2014). "Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations." Harvard Law Review Forum 127:176. https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/ [P]
   - 555 URLs in US Supreme Court opinions (1996-2011): 49.9% no longer served the cited material (data collected 2012-09-07).
   - Law journals 1999-2012: Harvard Law Review 73.2%, Harvard JOLT 65.8%, Harvard Human Rights Journal 70.1% of URLs affected by link rot or reference rot.
   - Definitions: link rot = URL serves nothing; reference rot = URL resolves but cited content is gone or changed.

2. Klein, M., Van de Sompel, H., Sanderson, R., Shankar, H., Balakireva, L., Zhou, K., Tobin, R. (2014). "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot." PLOS ONE 9(12):e115253. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253 [S, abstract-level P]
   - >3.5M STM articles (arXiv, Elsevier, PMC; 1997-2012), ~1M web-at-large URI references.
   - One in five articles suffers reference rot; among articles that cite web resources, seven in ten.
   - Link rot for references in 2012 articles: arXiv 1%, Elsevier 3%, PMC 4%. For 1997 articles: 25% / 65% / 75%.
   - Only ~25-40% of references had an archived copy within one year of publication; <5% within one day.

3. Jones, S.M., Van de Sompel, H., Shankar, H., Klein, M., Tobin, R., Grover, C. (2016). "Scholarly Context Adrift: Three out of Four URI References Lead to Changed Content." PLOS ONE 11(12):e0167475. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0167475 [P]
   - 1,059,742 URI references from 3.5M articles (1997-2012). 313,591 (~30%) had a verifiably representative archived snapshot.
   - Of 241,091 references analysable for drift, 184,065 (76.35%) had changed content by 2015.
   - Drift grows with age: roughly a quarter of references in 2012 articles were still unchanged by Aug 2015; for 2003-2005 articles ~10% or less. [S for the per-year values]
   - Drift measured with Simhash, Jaccard, Sørensen-Dice and cosine similarity on extracted text.

4. Zittrain, J., Bowers, J., Stanton, C. (2021). "The Paper of Record Meets an Ephemeral Web: An Examination of Linkrot and Content Drift within The New York Times." Harvard Library Innovation Lab; summary in Columbia Journalism Review. https://www.cjr.org/analysis/linkrot-content-drift-new-york-times.php ; https://dash.harvard.edu/handle/1/37367405 [P via CJR]
   - 553,693 NYT articles (1996 to mid-2019), 2,283,445 external links, 72% deep links.
   - 25% of deep links completely inaccessible; 53% of articles with deep links had at least one dead link.
   - By article year: 6% of 2018 links rotted, 43% of 2008, 72% of 1998.
   - Content drift: of 4,500 sampled links that still resolved, 13% had drifted significantly; 4% for 2019 articles, 25% for 2009.

5. Stox, P. (2024-02-02). "At Least 66.5% of Links to Sites in the Last 9 Years Are Dead (Ahrefs Study on Link Rot)." Ahrefs blog. https://ahrefs.com/blog/link-rot-study/ [P]
   - 2,062,173 domains, links seen since January 2013.
   - 66.5% of links dead; 74.5% when temporary crawl errors (6.45%) and indexing issues (1.55%) are included.
   - Causes: page dropped 47.7%, link removed from page 34.2%, crawl errors 6.45%, 301/302 redirect 5.99%, 404 4.11%, non-canonical 0.82%, noindex 0.73%.
   - Note: SEO-industry study, not peer reviewed; "dead" includes links removed by the linking page, so it overstates target-side rot.

6. Pew Research Center (2024-05-17). "When Online Content Disappears." https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/ ; PDF https://www.pewresearch.org/wp-content/uploads/sites/20/2024/05/pl_2024.05.17_link-rot_report.pdf [P]
   - ~1M Common Crawl pages (~90k per year, 2013-2023), checked October 2023.
   - 25% of all sampled pages inaccessible; 38% of 2013 pages; 8% of 2023 pages (i.e. within roughly a year). 16 points were individual pages gone on a live domain, 9 points dead root domains.
   - Government pages: 21% contain at least one broken link; 6% of all links dead. News pages: 23% contain a broken link; 5% of external links dead. Wikipedia: 11% of reference links dead, 54% of pages have at least one.
   - "Inaccessible" = one of nine HTTP error codes indicating the page or host no longer exists.
   - 18% of tweets sampled March-April 2023 were gone by June 2023.

7. Garg, K., Alam, S., Ayala, D., Nelson, M.L. (Old Dominion University + Internet Archive), blog post by Weigle, M. (2024-09-20). "Some URLs Are Immortal, Most Are Ephemeral." https://ws-dl.blogspot.com/2024/09/2024-09-20-some-urls-are-immortal-most.html ; dataset paper: Garg et al. (2025) "Longitudinal Sampling of URLs From the Wayback Machine", arXiv:2507.14752. [P via blog]
   - 27.3M URLs, 3.8B Wayback captures, 1996-2021.
   - Checked in 2023: 35.3% alive, 64.7% dead (25.1% HTTP 4xx, 39.6% other errors).
   - Median lifespan of URLs that died: 2.3 years overall; root URLs 8.8 years; deep links 1.3 years. Almost half of 4.8M deep links were dead within one year. Nearly half of root URLs persisted over a decade.

## 2. Content drift and page change frequency

8. Cho, J., Garcia-Molina, H. (2000). "The Evolution of the Web and Implications for an Incremental Crawler." VLDB 2000. https://www.vldb.org/conf/2000/P200.pdf [S, as restated in Fetterly et al. 2004 which I read]
   - 720,000 pages crawled daily for 4 months; change = MD5 checksum change.
   - 40% of pages changed within a week; ~50 days for half of all pages to change.
   - ~23-25% of .com pages changed daily; 11 days for half of .com pages; 4 months (whole study) for half of .gov pages.

9. Fetterly, D., Manasse, M., Najork, M., Wiener, J. (2004). "A large-scale study of the evolution of Web pages." Software: Practice and Experience 34(2):213-237. https://marc.najork.org/papers/spe2004.pdf [P]
   - 150,836,209 HTML pages crawled weekly for 11 weeks (Nov 2002 to Jan 2003).
   - 65.2% of week-to-week page pairs did not differ at all (shingle-based similarity). Larger pages change more; .com changes more than .edu/.gov.
   - Availability: only 49.2% of URLs returned HTTP 200 in all 11 weeks; 33.6% in 10 weeks; 17.2% in nine or fewer. Useful baseline for transient fetch failures in a weekly monitor.

10. Ntoulas, A., Cho, J., Olston, C. (2004). "What's New on the Web? The Evolution of the Web from a Search Engine Perspective." WWW 2004. https://snap.stanford.edu/class/cs224w-readings/ntoulas04evolution.pdf [P]
   - 154 popular sites crawled weekly for 51 weeks (Oct 2002 to Oct 2003).
   - 8% of pages are new each week; only 20% of pages available today are still accessible after one year.
   - Of pages that survive, about half do not change at all in a year; of those that change, 50% differ by less than 5% (TF.IDF distance) even after a year. 25% of links are new each week.

11. Adar, E., Teevan, J., Dumais, S.T., Elsas, J.L. (2009). "The Web Changes Everything: Understanding the Dynamics of Web Content." WSDM 2009 (best student paper). http://www.cond.org/wsdm09-change-camready.pdf [P]
   - 55,000 pages that real users revisited, crawled hourly for 5 weeks from 2007-05-24.
   - 34% (18,971) showed no change over 5 weeks; 66% changed at least once. Changing pages changed on average every 123 hours with mean Dice similarity 0.794 between versions.
   - 97.4% of DOM elements persist after 1 day, 91.7% after 1 week, 84.3% after 5 weeks (mean). Motivates fingerprinting on extracted text rather than raw HTML.

12. Visualping (2026-04, vendor data, low confidence): 40% of monitored pages register at least one change in any given month. Cited only via search snippet; no primary URL verified. Treat as anecdotal.

## 3. Bot blocking and crawler restrictions, 2024-2026

13. Longpre, S. et al. (49 authors) (2024). "Consent in Crisis: The Rapid Decline of the AI Data Commons." arXiv:2407.14933; NeurIPS 2024 Datasets and Benchmarks. https://arxiv.org/abs/2407.14933 [P abstract]
   - 14,000 domains audited, 2023-2024.
   - robots.txt restrictions now cover 5%+ of all C4 tokens and 28%+ of the most actively maintained "head" sources; Terms of Service restrict 45% of C4. Growth began mid-2023 after GPTBot and Google-Extended appeared.

14. Tomé, J. (Cloudflare) (2025-07-01). "From Googlebot to GPTBot: who's crawling your site in 2025." https://blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/ [P]
   - Of the top 10,000 domains, 3,816 had a robots.txt (checked 2025-06-06); ~14% of those had AI-crawler-specific directives. GPTBot most often disallowed: 312 domains (250 fully, 62 partial).
   - May 2025 AI-crawler share of crawl requests: GPTBot 7.7%, ClaudeBot 5.4%, Amazonbot 4.2%, Bytespider 2.9%.
   - Cloudflare made "block AI crawlers" the default for new domains on 2025-07-01 (Cloudflare press/blog; separate post). Search-summary figures of ">1M customers blocking" and "2.5M sites disallowing AI training (Aug 2025)" come from Cloudflare's managed-robots.txt post and were not re-read: https://blog.cloudflare.com/control-content-use-for-ai-training/ [S]

15. Gundelach, R., Mühlhauser, M., Herrmann, D. (2026-06-12). "Detecting Bot Detection: Prevalence, Techniques, and Implications for Web Measurement Research." arXiv:2606.14525. https://arxiv.org/html/2606.14525v1 [P]
   - Tranco top 10,000 sites, 4 browser configurations, 40,000 visits.
   - Soft-block rate (HTTP 403/429/503): headless Chromium 15.2%, headed Chromium 7.2%, headless Firefox 6.8%, headed Firefox 6.8%.
   - Sites behind Cloudflare: 37.0% block rate; Akamai 26.4%; providers without default bot detection 0-16%.
   - 82% of blocks attributable to bot detection; 75% of headless-only blocks triggered by header signals alone (HeadlessChrome brand, User-Agent). Only 5% of 81 surveyed measurement papers report blocking rates.
   - This is the closest published analogue to a "fraction of sites returning 403 to an automated fetcher" number.

16. HTTP Archive (2025). Web Almanac 2025, SEO chapter. https://almanac.httparchive.org/en/2025/seo [S]
   - 403 returned for 0.5% of sites to the HTTP Archive crawler (a real Chrome with a standard UA), showing that block rates depend heavily on how bot-like the client looks.

17. Fastly (2025-08-19). "Q2 2025 Threat Insights Report" press release. https://www.fastly.com/press/press-releases/new-fastly-threat-research-reveals-ai-crawlers-make-up-almost-80-of-ai-bot [S]
   - AI crawlers ~80% of AI bot traffic (mid-April to mid-July 2025); Meta 52%, Google 23%, OpenAI 20% of crawler volume. Fetcher bots (ChatGPT, Perplexity) exceeded 39,000 requests/minute at peaks.

18. Nieman Lab (author not captured) (2025-10). "The Wayback Machine's snapshots of news homepages plummet after a 'breakdown' in archiving projects." https://www.niemanlab.org/2025/10/the-wayback-machines-snapshots-of-news-homepages-plummet-after-a-breakdown-in-archiving-projects/ [P text]
   - 100 major news homepages: 1.2M Wayback snapshots 2025-01-01 to 05-15 vs 148,628 from 05-17 to 10-01, an 87% drop. NYT homepage 122 snapshots/day to 16/day; CNN down 94%.
   - Cause stated as breakdown in IA's archiving projects and publisher blocking, not link rot per se, but it means Wayback cannot be relied on as a fallback source for 2025-2026 changes.

19. Nieman Lab (2026-01). "News publishers limit Internet Archive access due to AI scraping concerns." https://www.niemanlab.org/2026/01/news-publishers-limit-internet-archive-access-due-to-ai-scraping-concerns/ [P text]
   - 241 news sites in 9 countries explicitly disallow at least one of four Internet Archive bots in robots.txt; 226 (93%) disallow two; 87% of those sites are Gannett/USA Today Co. 231 also disallow OpenAI, Google AI and Common Crawl bots.
   - Internet Archive (Graham, M., 2026-09-15) confirmed rate-limiting (HTTP 429) of automated Wayback traffic: https://blog.archive.org/2026/09/15/an-update-on-wayback-machine-access/

## 4. Prior tracking of AI model/system cards and policy pages

Trackers
20. The Midas Project, "AI Safety Watchtower" (launched mid-2024). https://www.themidasproject.com/watchtower ; profile: Fast Company 2025 https://www.fastcompany.com/91304014/this-watchdog-is-tracking-how-ai-firms-are-quietly-backing-off-their-safety-pledges ; Wikipedia https://en.wikipedia.org/wiki/The_Midas_Project [P page scrape 2026-09-22]
   - Monitors "hundreds" of policy documents and web pages at 16 companies (Fast Company); the public page currently lists OpenAI, Anthropic, Google, Meta, xAI, Cohere, Cognition, Magic.dev. Entries tagged change/addition/removal/violation, minor/moderate/major, and disclosed/undisclosed.
   - My count of the public page: 74 dated entries (1 from 2022, 1 from 2023, 23 from 2024, 17 from 2025, 32 from 2026 through Sept 22). Roughly 20 tagged major, 30 moderate, 8 minor; 14 violations, 10 removals, 12 additions (tag-occurrence counts, approximate). Check frequency not stated.
   - Watchtower is the only continuous public change-log for these documents I found. It is manual and curated, not fingerprint-based, so it is a lower bound on edits.
21. The Midas Project, "Seoul Commitment Tracker" (Feb 2025). https://www.seoul-tracker.org/ [P] 16 signatories of the May 2024 Seoul Frontier AI Safety Commitments graded; per Wikipedia only Anthropic scored B-, others C or worse; 6 fulfilled, 4 partial, 6 none (page).
22. Stein-Perlman, Z., AI Lab Watch (2024-2025). https://ailabwatch.org/ [P] Scorecard of 7 companies; site states it stopped being maintained in September 2025 with work passing to METR, Guidelight and Midas. No update-frequency statistics published.
23. stampr_ai (2026, alpha v0.9.0a1). https://www.stampr-ai.com/ [P] Tracks "model card history" and model fingerprints; publishes timestamped copies of system cards (e.g. Claude Opus 4.6 stamped 2026-03-07). No aggregate change statistics published; operator unnamed.

Academic
24. Castaño, J., Cabañas, R., Salmerón, A., Lo, D., Martínez-Fernández, S. (2025). "How do Machine Learning Models Change?" ACM TOSEM (accepted; arXiv:2411.09645). https://arxiv.org/abs/2411.09645 [P abstract]
   - 680,000+ commits across 100,000 Hugging Face models; 2,251 releases from 202 models. Documentation changes cluster in releases rather than granular commits. No per-card update-rate figure in abstract.
25. Liang, W. et al. (2024). "What's documented in AI? Systematic Analysis of 32K AI Model Cards." Nature Machine Intelligence; arXiv:2402.05160. https://arxiv.org/abs/2402.05160 [S] 32,111 Hugging Face model cards; static snapshot, no longitudinal drift figures.
26. "AI Transparency Atlas: Framework, Scoring, and Real-Time Model Card Evaluation Pipeline" (2025-12). arXiv:2512.12443. https://arxiv.org/abs/2512.12443 [S] Documentation for 5 frontier models plus 100 HF cards: 947 distinct section names; usage information under 97 labels. Argues version-level changes cannot be assessed reliably today. No drift rate reported.
   - Gap: I found no peer-reviewed study that measures how often frontier system cards are edited after publication. Watchtower and the vendors' own changelogs are the only sources.

Concrete dated cases of post-publication edits or delays (all with source)
27. OpenAI GPT-4o: model launched 2024-05-13; system card published 2024-08-08 (https://cdn.openai.com/gpt-4o-system-card.pdf). Watchtower: author removed from the card 2024-08-30.
28. OpenAI o1: Watchtower logs "substantial changes throughout the o1 system card, not announced" on 2025-01-17, and a webpage relabel "o1" to "o1-preview" on 2025-01-14. https://www.themidasproject.com/watchtower
29. OpenAI Deep Research: launched 2025-02-02; system card 2025-02-25 (https://openai.com/index/deep-research-system-card/), i.e. 23 days later.
30. OpenAI GPT-4.1: shipped 2025-04-14 with no system card at all; OpenAI said it was "not a frontier model" (TechCrunch coverage; https://techcrunch.com/2025/04/16/openais-latest-ai-models-have-a-new-safeguard-to-prevent-biorisks/ ; https://cyberscoop.com/openai-gpt-4-1-safety-report-splxai-test-results/).
31. OpenAI Preparedness Framework v2 (2025-04-15): dropped the commitment to safety-test fine-tuned models and dropped pre-release persuasion evaluations; the fine-tuning change was omitted from OpenAI's own change list (S. Adler, https://x.com/sjgadler/status/1912242577723781258 ; TechCrunch https://techcrunch.com/2025/04/15/openai-says-it-may-adjust-its-safety-requirements-if-a-rival-lab-releases-high-risk-ai).
32. OpenAI o3/o4-mini system card page (2025-04-16): benchmark results for Charxiv-r and Mathvista revised for a system-prompt change; SWE-Lancer results revised 2025-07-28. Disclosed as notes on the announcement page. https://openai.com/index/introducing-o3-and-o4-mini/ [S]
33. OpenAI GPT-6 Astra (2026-09-03): Fortune (Forlini, E., 2026-09-04) documented the launch post's hallucination rate changing 4.2% to 2% to 4.2% within hours, and other benchmark figures changing post-launch; Watchtower logs the Astra system card edited 2026-09-09 to hedge misalignment claims (disclosed). https://fortune.com/2026/09/04/openai-quietly-boosts-some-of-astras-evaluation-metrics-amid-rare-delay-in-publication-of-the-modeblog-post-announcement/ [P fetch summary; exact per-benchmark values not independently verified]
34. Google Gemini 2.5 Pro: preview released 2025-03-25; six-page model card ~2025-04-16 (Fortune, Nolan & Kahn, 2025-04-09 and 2025-04-17; TechCrunch 2025-04-17 https://techcrunch.com/2025/04/17/googles-latest-ai-model-report-lacks-key-safety-details-experts-say/); fuller model card "updated June 27, 2025" (https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Pro-Model-Card.pdf); 60 UK lawmakers called the delay a "breach of trust" 2025-08-29 (Fortune https://fortune.com/2025/08/29/british-lawmakers-accuse-google-deepmind-of-breach-of-trust-over-delayed-gemini-2-5-pro-safety-report). Google model-card PDFs carry a "Model card published/updated" date line, which your fingerprinting can key on.
35. Google Gemini 3.7 Flash model card: Watchtower logs undisclosed post-publication language changes in the Frontier Safety Assessment "Key Results" column, 2026-08-14.
36. Google Frontier Safety Framework: v2 2025-02-04 (dropped unconditional adherence), v3 2025-09-22, v3.1 2026-04-17 (Watchtower; DeepMind blog https://deepmind.google/blog/strengthening-our-frontier-safety-framework/).
37. Anthropic: removed the White House voluntary commitments from its transparency hub 2025-02-27 (Midas detection; TechCrunch, Wiggers, K., 2025-03-05 https://techcrunch.com/2025/03/05/anthropic-quietly-removes-biden-era-ai-policy-commitments-from-its-website). Anthropic said it remained committed and would add a section citing where its progress aligns.
38. Anthropic Claude Opus 4.6 system card (Feb 2026): carries a dated changelog with four post-publication revisions: 2026-02-06 (terminology), 2026-02-10 (MMMU-Pro 70.7% to 70.6%; commitment wording changed to "all future frontier models"), 2026-02-17 (HLE-with-tools 53.1% to 53.0%), 2026-03-06 (BrowseComp 83.97% to 83.73%, multi-agent 86.81% to 86.57%). https://www-cdn.anthropic.com/6a5fa276ac68b9aeb0c8b6af5fa36326e0e166dd.pdf [P] Note the earlier PDF hash (14e4fb01...) contains only the Feb 6 entries, so the same card exists at more than one CDN URL with different content.
39. Anthropic Claude Opus 4.8 system card (2026-05-28): changelog entries 2026-06-03 (token-budget wording) and 2026-06-17 (virology task score 0.89 to 0.90 after a tool-use error; bug-bounty figure revised after competition ended; evaluation scale 1-5 not 0-5). https://www-cdn.anthropic.com/0f0c97ad20d8005706296bd92aa1c27c6b2f4f61/Claude-Opus-4.8-System-Card.pdf [P]
40. Anthropic RSP: v3.0 effective 2026-02-24 removed the hard pause commitment (https://www.anthropic.com/responsible-scaling-policy/rsp-v3-0 ; GovAI analysis https://www.governance.ai/analysis/anthropics-rsp-v3-0-how-it-works-whats-changed-and-some-reflections); Watchtower logs further minor revisions 2026-03-24, 04-02, 04-29, v3.3 05-26, v3.4 07-08, plus a 2026-04-07 "slight update" to the Claude Mythos Preview system card.
41. xAI: Grok 4 system card and Risk Management Framework changes with "immediate quiet redactions" 2025-08-22; Grok 4.5 card edited with persistent errors 2026-07-20; Grok 4.6 card revised with a changelog 2026-08-17 (Watchtower).

## Derived expectations for a 6-week, ~300-URL monitor (my arithmetic, not published figures)

- Link death: Pew's 8% for pages under one year old implies ~1% per 6 weeks; the ODU deep-link median lifespan of 1.3 years implies 1-exp(-ln2 * 6/67.6) = ~6% of deep links dying in 6 weeks, root URLs (8.8 y) ~0.9%. NYT 2018 links at 6% per ~1 year gives ~0.7%. So 0.5-6% dead links over 6 weeks is the published range; corporate documentation pages should sit at the low end.
- Content change: Adar's 66%-changed-in-5-weeks applies to actively visited, dynamic pages and is an upper bound. Ntoulas' "half of surviving pages unchanged after a year" and Fetterly's 65% weekly-identical pairs are closer to static documentation. Zittrain's 4% drift within a year for 2019 NYT links is the closest "significant content drift" baseline, i.e. under 1% per 6 weeks.
- Bot blocking: 7-15% soft-block rate on top-10k sites for automated browsers, 37% on Cloudflare-fronted sites (Gundelach 2026), versus 0.5% for a browser-like crawler (HTTP Archive). Anything between 1% and 15% of your 300 URLs returning 403 is consistent with the literature; the value depends more on your client fingerprint than on the sites.
- Redirects: Ahrefs attributes ~6% of lost links over 9 years to 301/302 redirects, i.e. well under 0.1% per 6 weeks.
