# cardtrack backfill drain — run `backfill-drain-6`

Corpus went from 107 to 122 documents. Fifteen written, one routed to a review issue,
zero rejected. The headline is that **anthropic was not exhausted, and the reason is
structural**: `sources.yaml` points Phase A at `anthropic.com/news` and `/transparency`,
neither of which surfaces a single Frontier Red Team or Alignment publication. The whole
series lives under `anthropic.com/research/`, and it held ten uncatalogued 2026
model-specific safety evaluations after three consecutive runs had closed the publisher.
Nine of them are now rows. Every one of them has `has_safety_evals: true`, which is the
signal this database exists to carry.

Second finding, for the loop supervisor rather than the next agent: **this session's
priority list was stale.** It named thinking_machines, deepseek, moonshot_ai,
tencent_hunyuan, xiaomi and nvidia as "tier-1 newcomers with zero coverage" and called the
Inkling model card a known gap. All six were already covered, and the Inkling card has been
in the corpus since 2026-07-15. I triaged against `state_summary.json` instead and proposed
nothing that already existed.

## Counts

| | |
|---|---|
| Candidates in `logs/candidates.json` | 1695 across 19 publishers; 1694 not already catalogued by URL |
| Candidates triaged | all 1695, grouped by publisher; ~35 documents fetched and read in full |
| Proposals submitted | 16 |
| Written as rows | 15 (ids 108–122) |
| Routed to review issues | 1 (outbox:11, tier-2) |
| Rejected | 0 |
| Open GitHub issues to investigate | 0 (`logs/open_issues.json` is `[]`) |
| Blocked-URL escalations | 0 (empty in `candidates.json`) |

Publisher counts after the run, with the safety-eval flag count in parentheses: nvidia 24 (1),
**anthropic 21 (21)**, google_deepmind 20 (17), openai 14 (14), **uk_aisi 11 (11)**,
tencent_hunyuan 7 (0), metr 7 (7), moonshot_ai 4 (0), meta 4 (3), xiaomi 3 (0),
thinking_machines 3 (3), deepseek 3 (0), apollo_research 1 (1).

## Proposals and validator verdicts

| # | Document | Publisher | Date | Safety | Verdict |
|---|---|---|---|---|---|
| 1 | NVIDIA Isaac GR00T N1.7 | nvidia | 2026-04-17 | no | `written` id 108 |
| 2 | Nemotron-Labs-Diffusion technical report (3B/8B/14B/VLM-8B) | nvidia | 2026-05-21 | no | `written` id 109 |
| 3 | C-RADIOv4 (H + SO400M) | nvidia | 2026-01-27 | no | `written` id 110 |
| 4 | Audio Flamingo Next (Instruct/Think/Captioner) | nvidia | 2026-04-13 | no | `written` id 111 |
| 5 | Cosmos-H-Dreams | nvidia | 2026-07-23 | no | `written` id 112 |
| 6 | **LLM-discovered 0-days** (Opus 4.6) | anthropic | 2026-02-05 | yes | `written` id 113 |
| 7 | **Assessing Claude Mythos Preview's cybersecurity capabilities** | anthropic | 2026-04-07 | yes | `written` id 114 |
| 8 | **Discovering cryptographic weaknesses with Claude** | anthropic | 2026-07-28 | yes | `written` id 115 |
| 9 | **Project Pilot: Can AI Control a Drone?** | anthropic | 2026-07-24 | yes | `written` id 116 |
| 10 | **How Claude Performs on Robotics Tasks** | anthropic | 2026-07-09 | yes | `written` id 117 |
| 11 | **Project Fetch: Phase Two** | anthropic | 2026-06-18 | yes | `written` id 118 |
| 12 | **Teaching Claude why** | anthropic | 2026-05-08 | yes | `written` id 119 |
| 13 | **Measuring LLMs' impact on N-day exploits** | anthropic | 2026-06-08 | yes | `written` id 120 |
| 14 | **Measuring LLMs' ability to develop exploits** | anthropic | 2026-05-22 | yes | `written` id 121 |
| 15 | **AISI Control Red Team: stress-testing frontier monitors** | uk_aisi | 2026-07-23 | yes | `written` id 122 |
| 16 | Qwen-AgentWorld-35B-A3B | alibaba_qwen | 2026-06-23 | no | `issue_filed` tier_2_publisher, outbox:11 |

### The Anthropic research vein, and how to enumerate it

Three enumeration traps cost previous runs this publisher, all now in friction:

1. `anthropic.com/research` (the human-facing index) **does not list every post.** Both
   `zero-days` and `mythos-preview` are absent from it, and those are the two largest cyber
   capability reports of the first half of 2026.
2. `red.anthropic.com` looks like a separate site and serves an empty `sitemap.xml`, but
   `red.anthropic.com/2026/<slug>/` 301-redirects into `anthropic.com/research/<slug>`. The
   two `red.anthropic.com` URLs sitting in `candidates.json` were the thread I pulled.
3. The reliable enumerations are **`https://www.anthropic.com/sitemap.xml`** (149
   `/research/` URLs) and the team pages
   **`/research/team/frontier-red-team`** and **`/research/team/alignment`**, which list
   their own publications with datelines. Use those, not the index.

These are real safety documents, not blog filler. A sample of what is now catalogued:
Mythos Preview producing 181 working Firefox JavaScript exploits against 2 for Opus 4.6;
8 full Windows-kernel privilege-escalation chains in six hours at ~$2,200 each; 21 of 41
V8 CVEs reaching arbitrary code execution on ExploitBench where no other model reached one;
$35M of smart contracts exploited on SCONE-bench; a HAWK lattice automorphism cutting
HAWK-256's breaking cost from 2^64 to 2^38; and blackmail rates falling from up to 96% to
zero across the Claude 4 → Mythos Preview line.

### Judgement calls I did not paper over

- **#2 is a technical report, not a card, and that was deliberate.** All four
  Nemotron-Labs-Diffusion cards lack any date and their repositories span 2026-03-02 to
  2026-05-08, so no card date would represent the family. The report's title page says
  2026-5-21. Filed as `doc_type: other` with all four model names.
- **#4 has two defensible dates and I picked one.** The AF-Next cards carry no date, and
  the project page `afnext-umd-nvidia.github.io` is dead (GitHub Pages 404). I used
  2026-04-13, the v1 date of NVIDIA's own paper; the three repositories were created
  2026-04-05. A reviewer preferring repository creation would move it a week earlier. Both
  are in scope.
- **#5 Cosmos-H-Dreams is the weakest notability attestation in this batch.** 12 likes and
  354 downloads. I attested `notable_release: true` on the strength of the org's own
  announcement (NVIDIA published an article on it under its Hugging Face org on
  2026-07-27) and its own `isaac-for-healthcare` GitHub repository, and said so in the
  justification rather than leaning on adoption numbers it does not have.
- **#11 and #10 are two documents about one research programme.** Project Fetch: Phase Two
  is a longitudinal re-run of the 2025 ball-retrieval experiment; Claude Plays Robotics is
  the cross-embodiment benchmark. They were published five weeks apart with different model
  rosters, so I catalogued both and cross-referenced each in the other's justification. A
  reviewer who thinks that is one row too many should merge #11 into #10.
- **#9 and #14 list only the models whose per-model figures I could verify.** Project Pilot
  scores fifteen systems and the exploit report covers unnamed competitor models; I did not
  transcribe rosters I had not confirmed.
- **#15 resolves the previous run's open scope question** rather than deferring it again.
  See friction: the corpus already holds METR's monitor red-teaming as an `independent_eval`,
  so excluding AISI's was inconsistent.

## What is now exhausted, and how I verified it

- **google_deepmind** — fetched `deepmind.google/models/model-cards/` and date-checked every
  entry. Each of the fourteen 2026 cards is catalogued. The only 2026-dated item not in the
  corpus is Veo 3, whose card shows "Updated 13 January 2026" for a model released in 2025;
  that is a modification date, not a publication date, so it stays out. **Do not re-triage.**
- **openai** — re-enumerated `deploymentsafety.openai.com/sitemap.xml`: 24 slugs, of which 11
  are catalogued and the other 13 are all 2025. The three `openai.com/index/` posts through
  2026-08-07 are catalogued and nothing newer exists. Done.
- **metr** — `/blog`, `/research` and `/risk-assessment` all re-checked. `/evaluations/`
  redirects into `/risk-assessment/` and contains no 2026 report; every 2026 blog item is
  either catalogued or names no specific model.
- **apollo_research** — `/science` pages 1 and 2 and `/blog` enumerated. The only 2026
  science item is the one already catalogued; `/blog/apollo-update-may-2026` is an org update.
- **meta** — `research.meta.ai/blog/` has four posts. Muse Spark 1.2 / Muse Code links only
  the methodology report (catalogued), and
  `/blog/introducing-next-generation-unified-media-generation-model` 307-redirects to the
  Muse Image / Muse Video post the previous run already read and found undocumented.
- **deepseek, moonshot_ai, xiaomi** — closed via the HF API rather than the candidate list.
  Every 2026 repository not already catalogued is a `-Base`, `-DSpark`, `-DFlash`, `eagle3`
  draft or FP4/FP8/GGUF quantization. Note in particular that `DeepSeek-V4-Flash` (2026-04-22,
  2.4M downloads) is deliberately **not** a row: it shipped the same day as the catalogued
  `DeepSeek-V4-Pro`, so it is a sibling within one release, and the separately catalogued
  `DeepSeek-V4-Flash-0731` is the later refresh.
- **thinking_machines** — `/news/` and `/blog/` both re-checked; the only model documentation
  remains the two Inkling cards and the open-weights essay, all catalogued.
- **uk_aisi** — the previous run fetched all 89 blog candidates; I re-opened only the one it
  left unresolved (now id 122) and spot-checked
  `stress-testing-asynchronous-monitoring-of-ai-coding-agents`, which is 2025-12-16 and
  below the floor.
- **anthropic** — now enumerated properly via sitemap and both team pages. See the handoff
  note below for what I deliberately left.

## Skipped, by reason class

| Reason class | Examples |
|---|---|
| Below the 2026-01-01 scope floor | `aisi.gov.uk/blog/stress-testing-asynchronous-monitoring-of-ai-coding-agents` (2025-12-16); `nvidia/music-flamingo-2601-hf` and `music-flamingo-think-2601-hf` (transformers-format re-releases of a model whose paper is arXiv:2511.10289, Nov 2025); the 13 pre-2026 OpenAI hub slugs; Veo 3 (2025 model, card merely updated 2026-01-13) |
| Not about a specific model or eval | `anthropic.com/research/off-switch-dual-use` (GRAM, 50M–5B research models, explicitly "not applied to any of the production models at Anthropic"); `anthropic.com/research/attack-navigator` (MITRE ATT&CK threat-intelligence mapping of 832 banned accounts, not a model evaluation); Apollo's May 2026 org update |
| Same release already covered | `nvidia/Cosmos3-Nano` (card states Release Date 05/31/2026, identical to the catalogued Cosmos3-Super); `deepseek-ai/DeepSeek-V4-Flash` (same launch day as the catalogued V4-Pro); `tencent/Hy-MT2-1.8B` and `-7B` (already listed in the catalogued Hy-MT2 family entry's `model_names`); thinkingmachines.ai `/news/introducing-inkling` and `/news/inkling-small` (announcements of catalogued cards) |
| Size / quantization / draft / base variant | all `-Base`, `-DSpark`, `-DFlash`, `eagle3_*`, `dflash_*`, `dspark_*` repos; `MiMo-V2.5-DFlash`, `MiMo-V2.5-Pro-FP4-DFlash`; `Hy3-FP8`, `Hy-MT2-*-GGUF/FP8`; `Nemotron-3-Nano-4B-FP8/GGUF`, `Nemotron-3-Super/Ultra-*-NVFP4/FP8` |
| Third-party re-upload of another org's model | `nvidia/Kimi-K2.7-Code-NVFP4`, `GLM-5.2-NVFP4`, `Qwen3.6-27B/35B-NVFP4`, `MiniMax-M3-NVFP4`, `Gemma-4-*-NVFP4`, `DeepSeek-V4-*-NVFP4`, `Mistral-Medium-3.5-128B-NVFP4`, `gpt-oss-puzzle-88B`, `Qwen-Image-Flash` |
| Regional variant | `nvidia/NVIDIA-Nemotron-Nano-9B-v2-Japanese`, `nvidia/parakeet-ctc-0.6b-Vietnamese` |
| Research component rather than a model release | `nvidia/PiD` (a latent-to-pixel diffusion decoder plus the VAE weights it plugs into; 401 likes but no dated card and no standalone release) |
| Not notable enough to catalogue | NVIDIA `Ising-*`, `NV-JEPA-DNA-*`, `Privasis-Cleaner-*`, `ArtiFixer`, `nvDock`, `CWIP-1.0`, `corrdiff-*`, `stormcast-conus`, `gr00t17-lerobot-*`, `Kimodo-*`, `ARDY-*`, `EGM-*`, `Nemotron-Terminal-8B/14B/32B` (39/11/36 likes), `Nemotron-3-Content-Safety` (predecessor of the catalogued 3.5, 18 likes); Tencent `POINTS-*`, `Youtu-*`, `Penguin-VL-*`, `R3-*`, `StableToken`, `HiLS-Attention-7B`, `Sequential-Hidden-Decoding-*`; inclusionAI `SingGuard-*`, `ZwZ-*`, `AReaL-*`, `DR-Venus-*` |
| Date undeterminable, not proposed | `tencent/Covo-Audio-Chat` and `tencent/HunyuanOCR` — unchanged from the previous run, and I did not re-litigate them |
| No fetchable primary document | Qwen3.8 Max (reported 2026-08-02 by third-party trackers; `qwen.ai` is client-side rendered and returns a chrome-only shell to curl); xAI `/news/composer-2-5` (announcement only, no card found) |

## Things the next session should know

1. **Anthropic's research vein is real but I did not drain it, deliberately.** I catalogued
   the nine documents that are unambiguously model-specific evaluations. Left on the table,
   in descending order of how likely I think they are to qualify:
   `next-generation-constitutional-classifiers` (2026-01-09, jailbreak-robustness numbers for
   a safeguard system rather than a model), `automated-alignment-researchers` (2026-04-14),
   `deprecation-updates-opus-3` (2026-02-25, about a specific model but a commitments update
   rather than an evaluation), `persona-selection-model` (2026-02-23) and
   `disempowerment-patterns` (2026-01-28). The sitemap also lists ~40 more `/research/` slugs
   I have not dated at all, including `exploit`, `cyber-toolkits-update`,
   `critical-infrastructure-defense`, `building-ai-cyber-defenders`, `making-claude-a-chemist`,
   `Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench`, `nuclear-safeguards-for-ai`,
   `biorisk`, `agents-in-biology`, `measuring-agent-autonomy`, `long-running-Claude`,
   `emergent-misalignment-reward-hacking`, `forecasting-rare-behaviors`, `smart-contracts`,
   `glasswing-initial-update` and `project-vend-2`. Several of those names look like exactly
   the CBRN and cyber evaluations this database wants. **Start there.**
2. **Use the Hugging Face API, not the candidate URLs, for HF-indexed publishers.**
   `https://huggingface.co/api/models?author=<org>&sort=createdAt&direction=-1&limit=300`
   returns every repo with `createdAt`, `likes` and `downloads` in one request. Diffing that
   against `state_summary.json` closed deepseek, moonshot_ai and xiaomi in three requests.
   `logs/candidates.json` for those orgs is ~90% hub chrome and is not a complete listing.
3. **The previous run's "grep NVIDIA cards for Release Date" trick only half works.** The
   field is missing or empty on Nemotron-Labs-Diffusion (all four), GR00T-N1.7-3B, PiD,
   audio-flamingo-next and Nemotron-Terminal. Two substitutes that worked: NVIDIA-authored
   articles at `huggingface.co/blog/nvidia/<slug>` carry a JSON-LD `datePublished`, and family
   technical reports carry a title-page date.
4. **nvidia is *closer* to exhausted but still not closed.** All 243 of its 2026 repositories
   were enumerated and classified this run. What remains uncatalogued and non-trivial is the
   Cosmos-H healthcare line (`Cosmos-H-Surgical` 2026-03-03, `Cosmos-H-Surgical-Simulator`
   2026-02-19 — both siblings of the now-catalogued Cosmos-H-Dreams), `RE-USE` (2026-03-18,
   speech enhancement, dated card), `NVIDIA-Nemotron-Parse-v1.2` (2026-02-18, 207k downloads,
   skipped twice now as an incremental point release of a 2025 model) and
   `Nemotron-Labs-TwoTower-30B-A3B-Base-BF16` (base-only, so likely out).
5. **Tier-2 status.** I used one of three slots. Every tier-2 publisher now has at least one
   open review issue: mistral (2), xai, poolside, stepfun, inclusion_ai, and alibaba_qwen (2,
   including outbox:11 from this run). I deliberately did not file the marginal ones —
   stepfun's `Step-3.5-Flash` (2026-02-01, 830 likes) and `Step3-VL-10B` (2026-01-13, 411
   likes) are the obvious next candidates, but stepfun already has an unresolved null-date
   issue open and a second one would be noise rather than signal. If the review queue gets
   drained, file those two.
6. `logs/open_issues.json` is `[]` and `blocked_escalations` is empty, so there were no issues
   to investigate, no comments filed and no documents found dead.

## Friction and proposals

Six entries appended to `logs/friction.jsonl`: the anthropic `/research` index gap with its
three enumeration traps; the stale priority list in the session prompt; the resolution of the
monitor-red-teaming scope question; the NVIDIA date workarounds; re-confirmation that
`qwen.ai` is unreadable and what it cost; and the Hugging Face API substitute for candidate
triage.

Nothing appended to `PROPOSALS.md`. The anthropic index-URL gap is the most consequential
process finding of this run and would normally warrant an entry, but it is another instance of
the `document_index_urls:` request that three previous runs have already filed, and a fourth
restatement is noise. The friction entry carries the specific URLs a maintainer needs.
