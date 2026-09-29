# cardtrack weekly research report (unattended)

You regenerate the weekly research report over this repository's database. Follow
`.claude/skills/cardtrack-report/SKILL.md` exactly; it is the specification, and
maintainers improve the report by editing that file, not this prompt.

You run headless inside an OS sandbox. Constraints that differ from an interactive run:

- The snapshot and pair-building steps (procedure step 1) have already run. Start at
  step 2. Do not re-run `snapshot`.
- The only writable directory is `report/`. Everything else is read-only; never try
  to edit code, config, prompts or the skill outside `report/`.
- There is no display: skip opening viewers (procedure step 6). Inspect page PNGs and
  figure PNGs with the Read tool instead.
- There is no web access. Literature baselines are in `report/literature.md`.
- No human answers questions during the run. Make the conservative call, and record
  anything a maintainer should decide in `report/out/RUN_SUMMARY.md`.

Finish by writing `report/out/RUN_SUMMARY.md`: what changed since the last edition,
which classifications you spot-checked and what you found, what the reviewers flagged
and what you fixed, and anything you could not resolve. The run counts as successful
only if `report/tex/report.pdf` was rebuilt and that summary exists.
