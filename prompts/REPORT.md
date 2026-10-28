# cardtrack weekly briefing (unattended)

You write this week's edition of the research briefing over this repository's database. Follow
`.claude/skills/cardtrack-report/SKILL.md`; it holds the constraints and the freedom, and
maintainers improve the briefing by editing that file, not this prompt.

You run headless inside an OS sandbox. Constraints that differ from an interactive run:

- The snapshot and pair-building steps (procedure step 1) have already run. Do not re-run
  `snapshot`; start with the classification batches, if any.
- The only writable directory is `report/`. Everything else is read-only; never try to edit
  code, config, prompts or the skill outside `report/`.
- There is no display and no web access. Inspect figures and the converted
  `report/out/html/report.html` with the Read tool. Literature baselines are in
  `report/literature.md`.
- No human answers questions during the run. Make the conservative call, and record anything a
  maintainer should decide in `report/out/RUN_SUMMARY.md`.

Finish by writing `report/out/RUN_SUMMARY.md` (procedure step 6). The run counts as successful
only if `report/report.md` was rewritten, `report/run.sh html` passes, and that summary exists.
