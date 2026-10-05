# Resolved friction

Which clusters in `logs/friction.jsonl` have been addressed, by which commit, and
the signal that proves the fix holds. The agent reads this before logging: a
problem listed here that comes back is `kind: regression`, not a rediscovery.
Entry counts are from the 2026-10-04 analysis of 177 entries (2026-08-09 to
2026-10-01). Add a row when a fix lands; never delete rows.

| Cluster | Entries (range) | Fix | Commit | Proof it holds |
|---|---|---|---|---|
| Phase A total outage reported like a quiet day (ok=0, errors=checked, "no changes" commit); laptop resumed from suspend before Wi-Fi | 12 (08-14 to 09-22) | outage flag in the commit message; `wait_for_network.py` gate + systemd retry | ea760057, 752ee7b7 | every run since 09-23 has `errors: 0`; a `[monitor outage]` commit tag would be the regression |
| Validator turned 5xx into `document_retrievable=false` | part of 5 (08-09 to 09-25) | sleep-and-retry on 5xx | 0c91b326 | no `transient_rejection` on a 5xx since |
| Index URLs missing for Anthropic /research, OpenAI deployment hub, Meta research, xAI /safety, Epoch, Qwen HF | part of 19 | index URLs added | 0c91b326 | candidates from those pages appear |
| `openness` had no rule for tiers and derivatives | part of 45 | openness policy in TASK.md, 24 rows backfilled | 866806c0 | `ambiguous_criteria` about openness stopped after 09-12 |
| Extractor drift, footnotes and redirect stubs minted versions | part of 7 | drift and stub detection | 642d5b31 | `extractor_drift` counted separately in the monitor summary |
| Appends to friction.jsonl / PROPOSALS.md impossible from the sandbox; scratch files left in logs/ and committed | 13 tooling (08-09 to 10-01) + the 09-21 pending files | `scripts/log_note.py` (allowlisted), scratch in /tmp, `git add` by named path, logs/ allow-listed in .gitignore | pending (this branch) | no `tooling` entry about appends; no untracked file ever shows in a run commit |
| Agent's WebFetch blocked (403) on openai.com, rand.org, securebio.org; PDFs over 10 MB refused; cards proposed unread | 27 (08-09 to 09-29) | `scripts/read_doc.py` (allowlisted): the pipeline's own fetcher + extractor | pending (this branch) | no `unfetchable_agent_side` entry for a URL Phase A reads; no "proposed without reading" in run reports |
| Page furniture (teasers, date lines, HF widgets) minted versions; 470 of 605 versions never summarised; real revisions buried under the 20-entry cap | 7 (08-17 to 09-30) | furniture versions classified in the monitor, dropped from the queue; queue sorted by changed lines | pending (this branch) | `updated_docs.json` shrinks below 20 within a week; agent reads no furniture diffs |
| HF org pages list by page order, not creation date (Qwen3.8 found 5 days late); Palisade and CAISI index URLs stale | 19 (08-09 to 10-01) | HF API `?sort=createdAt` as an index source; URLs corrected | pending (this branch) | new HF repos in candidates within 24 h of `createdAt`; Palisade candidates reappear |
| Blocked / not-found fetches invisible to the agent until a 3-run streak | 5 (09-12 to 09-15) | `phase_a_summary` in candidates.json every run | pending (this branch) | task 5 of TASK.md never sees an empty list while Phase A counted failures |
| `open_issues.json` `[]` indistinguishable from a failed `gh` call | 7 (08-21 to 09-13) | `{"fetch_ok": false, ...}` on failure | pending (this branch) | agent reports "issues unknown" instead of "no issues" on a gh outage |
| Proposal caps shared with operator backfills (09-23: 3 verified docs not written) | 3 (08-09 to 09-23) | caps count per actor (agent, human and monitor each have their own window) | pending (this branch) | no `cap` entry on a day with a human backfill |
| 429 went straight to impersonation with no pause | part of 5 | 429 gets the 5xx sleep-and-retry, honouring Retry-After up to 15 s | pending (this branch) | no `transient_rejection` on a 429 |
| Apollo doc 75 kept a typo canonical URL after the publisher fixed the redirect | 1 (09-15) | canonical repointed, status active, operator writes via propose_doc.py on the host (a DB write, not a code commit) | committed by the next daily run | monitor reports doc 75 `ok` with zero redirects |
| Criteria silent on family vs per-card rows and on speech/omni models | 7 of ~45 (08-12 to 09-30) | two clarifying sentences in criteria.yaml (2026-10-05); the other questions stay the agent's call under `when_uncertain: admit_and_flag` | pending (this branch) | `ambiguous_criteria` on those two questions stops |
