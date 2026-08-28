# cardtrack run report — 2026-08-28T07:28Z-local

**Corpus at start:** 264 documents (259 active, 4 removed, 1 moved). **At end:** 265.
**Inputs:** 183 Phase A candidates, **0 of them new** — the file is a pure replay of links first seen
2026-08-17 through 2026-08-27, all of which prior runs already triaged. 0 blocked-URL escalations.
`open_issues.json` was `[]` **and that was wrong**: there are four open issues (see §4).
**Written this run:** 1 `add`, 1 `new_version`, 2 `field_update`. 1 proposal routed to needs-review,
3 `new_version` probes returned `duplicate` (already stored — the correct answer). Caps not approached.

**Phase A failed completely this run.** Its summary line reads
`checked: 260, ok: 0, not_found: 0, blocked: 0, errors: 260, fingerprint_checked: 39, new_versions: 0,
candidates: 183, candidates_new: 0`, and Phase B logged `error connecting to api.github.com` twice.
Everything below was found by hand. I verified the outage was transient and not link rot: 8 randomly
sampled active canonical URLs (epoch.ai, far.ai, huggingface.co/inclusionAI, metr.org, ai.google.dev,
aisi.gov.uk, huggingface.co/stepfun-ai, ai.meta.com) all returned HTTP 200 to a plain curl, and ~30 of
my own fetches succeeded, including the GitHub API on the first try.

---

## 1. Proposals and validator verdicts

| # | Action | Document | Verdict |
|---|---|---|---|
| 1 | `new_version` | xAI — Grok 4.6 model card (Revision 2026-08-17) | `{"status": "duplicate", "reason": "fingerprint_already_stored", "slug": "xai-grok-4-6-model-card", "version_id": 357}` |
| 2 | `add` | Cursor — Grok 4.6 model card, launch-day edition | `{"status": "issue_filed", "reason": "content_duplicate_of:xai-grok-4-6-model-card", "issue_ref": "outbox:1"}` |
| 3 | `new_version` | Google DeepMind — Gemini Omni Flash model card | `{"status": "written", "slug": "google-deepmind-gemini-omni-flash-model-card", "document_id": 36, "version_id": 432}` |
| 4 | `field_update` | same row, `model_names` += *Gemini Omni 1.1 Flash* | `{"status": "written", "slug": "google-deepmind-gemini-omni-flash-model-card", "document_id": 36}` |
| 5 | `add` | Tencent Hunyuan — **Hy4 preview** model card | `{"status": "written", "slug": "tencent-hunyuan-hy4-preview-model-card", "document_id": 265, "version_id": 433}` |
| 6 | `field_update` | xAI Grok 4.6 row, `notes` — byte-identity claim corrected | `{"status": "written", "slug": "xai-grok-4-6-model-card", "document_id": 203}` |
| 7–9 | `new_version` ×3 | OpenAI GPT-5.6 Preview / GPT-5.5 / GPT-5.6 system cards | all `{"status": "duplicate", "reason": "fingerprint_already_stored"}` (version_ids 360, 387, 348) |

### Tencent Hy4 preview (5) — the substantive find

A 770B-total / 49B-activated MoE with 1M context, Apache-2.0, released 2026-08-27 and positioned by
Tencent as its new open-source flagship; successor to `Hy3 preview` and `Hy3`, both already held. I read
the full card: 78 layers, 256 routed experts + 1 shared, Gated DeepSeek Sparse Attention with IndexCache,
identity Hyper-Connections, native MTP layer. Notability is not in question — 113 likes within a day, an
official Tencent release announcement, independent coverage, and a reported blind side-by-side in which
163 internal experts rated 203 engineering tasks at 2.99 for Hy4 preview against GLM 5.3 at 2.92 and
Kimi K3 at 2.94. `Hy4-preview-FP8` is the quantization of the same release and is covered by this one
entry per the size/quantization rule. `openness: open_weight_permissive` (Apache-2.0 in both the HF
metadata and the card). **`has_safety_evals: false`**, checked deliberately: the card is architecture +
a benchmark-image appendix + a "Known Limitations" paragraph about over-long reasoning and
over-verification + deployment instructions, and a grep of the full README for
safety/red-team/risk/jailbreak/harm/bio/cyber returns nothing.

**It was not in `candidates.json` at all**, and `huggingface.co/tencent` is a configured index_url. One
call to `huggingface.co/api/models?author=tencent&sort=createdAt` returned it at the top. That is the fix
the 2026-08-13 PROPOSALS entry asked for, and the failure that entry predicted has now recurred on a
bigger model. The same API sweep across all eight HF-indexed publishers took under a minute and confirmed
nothing else new: only FP8/NVFP4/base re-uploads (Qwen3.8-Flash-Next-FP8,
Qwen3.8-2.4T-A95B-NVFP4, Nemotron-3 Super/Nano base and quantized variants), all correctly excluded as
size/quantization variants of rows already held.

### Gemini Omni Flash (3, 4)

The card was republished 2026-08-27 and its Model Information section now reads verbatim *"This model
card describes Gemini Omni Flash and Gemini Omni 1.1 Flash."* Gemini Omni 1.1 Flash shipped the same day
with its own blog.google announcement, API surface and pricing, and has **no document of its own** — so a
new model became documented without producing a new document. Handled as `new_version` (the 08-27 edition,
version 432) plus a `model_names` extension, with `publication_date` left at 2026-05-19 because this is a
new edition of the same document. Identical to the Gemini 3.5 Audio case handled yesterday; the pattern
now has two instances in two days and is logged to friction with the cheap detector (the model-cards index
exposes an "Updated <date>" per card).

### Cursor's Grok 4.6 card (1, 2, 6) — and a mistake of mine

xAI has revised the Grok 4.6 card in place: md5 `7640cdde…`, "Revision: 2026-08-17", changelog listing
renumbered sections, added PartBench and DeepSearchQA results, KernelBenchInternal v1.1 and **"Corrected
eval results on HackerBench v0.2, Self-harm, MASK, LAB"**. Cursor still serves the unchanged launch-day
file (md5 `5faf54cc…`, "Revision: 2026-08-12"); word-diff similarity 0.705. Cursor's copy is now the only
public edition carrying the pre-correction numbers for those four safety and behavioural evals. The
corpus already holds the revised edition (probe 1 came back `fingerprint_already_stored`).

I proposed Cursor's copy as a co-publication and the validator routed it to needs-review as a content
duplicate — **which is exactly what happened on 2026-08-22**, complete with a PROPOSALS entry recording
that the run had deliberately not retried it. I retried it, and there is now a third needs-review issue
about one URL (#28, #31, today's outbox entry). That is a real cost paid by the human reviewer, and the
cause is structural: no input the agent receives lists prior rejections, and `open_issues.json` — which
would have shown #28 and #31 — was empty because the GitHub fetch had failed. I did three things about it:
commented the consolidated evidence on #31 asking that the three be adjudicated together (`logged_only`,
`gh` is unavailable in the sandbox); corrected the `notes` on `xai-grok-4-6-model-card`, which still
asserted the two copies were byte-identical; and wrote a PROPOSALS entry asking for rejection history in
`state_summary.json`. I did **not** re-argue the 2026-08-22 ask (make the duplicate check publisher-aware),
which stands as written.

---

## 2. Searched and skipped

Every allowlisted publisher was checked directly this run, since Phase A contributed nothing.

**Fetched, read and skipped on judgement:**

- `deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/` (2026-08-27) and its
  technical report — the closest call. It evaluates a named model (Gemini 2.5 Flash Lite) against the
  private MLCommons AILuminate AIRR 1.4 reserve set covering CBRNE, cyber, hate, self-harm and
  violent-crime prompts, in a confidential enclave with AVERI, Singapore AISI and OpenMined. I read the
  PDF in full: it reports **no scores, no violation rates, no findings about the model**. §3 is setup,
  §4 goes straight to procedural lessons. Fails the system-card test on the "whose behaviour do the
  numbers describe" discriminator. Its co-publishers are also all non-allowlisted (MLCommons is
  consciously excluded), so it could only ever have entered as a Google-copy-only add.
- `aisi.gov.uk/blog/optimal-stopping-spending-evaluation-compute-where-it-counts` (2026-08-27) — release
  of the `optstop` package; savings of 57–97% of planned runs on MATH, GPQA Diamond and WritingBench, no
  model under test named. Same discriminator.
- `anthropic.com/news/model-hardware-standard-research-preview` (2026-08-27) — a hardware-interface
  specification for agents operating lab and manufacturing instruments. Not model documentation.
- `anthropic.com/news/expanding-support-for-scientists` (2026-08-27) — seats-and-funding program
  announcement.
- `epoch.ai` "An update on AI's most important number" (2026-08-27) — lab revenue analysis.
- `palisaderesearch.org/blog/palisade-podcast-daniel-kokotajlo` (2026-08-25) — podcast episode.
- `nvidia/Nemotron-3-Diarization-preview` (2026-08-24) — **gated repo**; the API returns metadata but the
  README is auth-walled. I do not attest to documents I cannot read. Also thin: 3 downloads, 7 likes.
- The x.ai (Grok Bot plan availability, 08-26), Mistral (HUMAIN, 08-24) and Cursor (08-27 "Start from
  scratch, without a repo") posts — availability, company and product items.

**Checked, nothing new:** OpenAI (deployment safety hub latest is the 08-06 addendum, already held; the
08-19 changelog corrections on three cards are already stored — probes 7–9), Meta (latest 08-20, held),
METR, Redwood, Transluce (latest 08-20, skipped by prior runs on the same discriminator), Apollo,
Epoch, Thinking Machines, FAR.AI, SaferAI, US CAISI, SecureBio (latest 08-20, already adjudicated),
DeepSeek, Moonshot, Qwen, InclusionAI, NVIDIA, Xiaomi, StepFun, poolside.

**One index I could not reach:** RAND's research-and-commentary page returned **HTTP 403** to both a
browser-UA curl and WebFetch. I substituted a domain-scoped web search, which surfaced no RAND
publication after 2026-08-25 evaluating a named model — a weaker check than an index diff, and logged to
friction, since `sources.yaml` records this URL as browser-UA-reachable and RAND links were flowing into
candidates as recently as the 08-26 batch.

**Long-silent publishers, genuinely silent** (checked, not forced): xiaomi 123 d, palisade_research
113 d, stepfun 97 d, poolside 46 d, apollo_research 38 d, us_caisi 36 d (latest CAISI blog post is
2026-03-23), moonshot_ai 32 d, far_ai 30 d, thinking_machines 28 d, epoch_ai 28 d (publishing, but
economics rather than model evals), saferai 26 d, uk_aisi 24 d, mistral 24 d, transluce 22 d,
securebio 21 d. cursor closed this run (via the Grok 4.6 card, pending review); google_deepmind,
tencent_hunyuan and xai closed or refreshed.

---

## 3. Citation mining

Cleared the carry-over from yesterday: the two Anthropic PDFs added 2026-08-18 could not be mined last
run because the fetch summarizer cannot read binaries. Downloaded and extracted both with `pdftotext`
this run —
`www-cdn.anthropic.com/30bf50e2…` (*Autonomous de novo protein binder design with Claude*) and
`…/9f08da51…` (*Automated processing of raw NMR and LC-MS data with Claude Opus 5*). Every external
reference is biology or chemistry literature (bioRxiv, Zenodo, proteinbase.com, FreeBind, IPSAE); **no
model or system cards, no third-party evals**. Nothing to propose.

Also mined the OpenAI *Hugging Face Incident: Technical Report* (id 263, added yesterday). The only
third-party assessment it cites is the METR/Redwood investigation, both copies of which are already held
(ids 259, 260). The one other URL in the document is an illustrative example of the agents' encoded
inter-agent messages, not a real page. Hy4 preview's card cites only architecture papers on arXiv (Gated
DSA, IndexCache) — the standing arXiv-technical-report gap, already logged.

---

## 4. Issues and escalations

`logs/open_issues.json` was `[]`. **It was stale.** I queried `api.github.com` directly (HTTP 200, first
try) and found four open issues, all `needs-review`, none `data-error` or `missing-doc`:

| # | Opened | Title |
|---|---|---|
| 28 | 2026-08-13 | needs-review: proposed URL duplicates content of `xai-grok-4-6-model-card` |
| 29 | 2026-08-21 | needs-review: canonical_url move with different content for `anthropic-claude-opus-5-system-card` |
| 30 | 2026-08-21 | needs-review: possible duplicate of `meta-muse-spark-1-2-other` |
| 31 | 2026-08-22 | needs-review: proposed URL duplicates content of `xai-grok-4-6-model-card` |

These are validator-filed adjudication requests, not user reports, so there was nothing to verify against
a live source and no correction to propose. I commented on #31 only — the one my own duplicate proposal
bears on — with the md5/revision evidence and a request to treat #28, #31 and today's outbox entry as one
thread (`{"status": "logged_only", "issue": 31}`; `gh` is unavailable inside the sandbox, so it is in
`logs/comments.jsonl` rather than on GitHub). #29 and #30 are prior runs' judgement calls awaiting a human
and I did not touch them.

No blocked-URL escalations. The 8-URL liveness sample above stands in for the link check Phase A could not
complete; nothing appeared dead.

## 5. Friction and proposals

Eight lines appended to `logs/friction.jsonl`: Phase A's total failure reporting as a clean run (third
instance); `open_issues.json` empty because the fetch failed rather than because there is nothing there;
a rejected proposal re-filed because validator rejections are invisible to later runs; a flagship release
(Hy4 preview) missed by index diffing that one HF API call found; Google shipping new models by editing
existing cards; a gated model card that cannot be attested; two more skips on the unwritten
"whose behaviour do the numbers describe" discriminator; and RAND's index_url now 403ing.

One entry appended to `logs/PROPOSALS.md`: *"The agent cannot see what the validator already refused, and
today that cost a third review issue on one URL."* The ask is small and the data already exists — surface
recent non-`written` proposal outcomes in `state_summary.json`, make a failed `open_issues.json` fetch
look failed, and optionally have `propose_doc.py` hard-stop a proposal whose URL already has an open
`issue_filed` outcome. It is deliberately scoped not to re-argue the 2026-08-22 co-publication ask.
