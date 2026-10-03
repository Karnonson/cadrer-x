# cadrer-x evals

2026-10-03. Each skill has its case in `skills/<name>/evals/`: a fixture project, one request, shell checks
and judge lines. `baseline.md` beside it records what the model did with no skill installed.

```sh
FLEET_SKILLS_SRC=~/Dev-FullStack/cadrer-x/skills \
  python3 ~/Dev-FullStack/dotfiles/claude/scripts/fleet.py skills eval cadrer-x-<name> --engine claude|codex [--baseline|--behaviour]
```

Run one eval at a time: two runs started in the same second share a stamp and overwrite each other's
results. Results land in `~/.claude/fleet/evals/<skill>/<stamp>-<engine>.json`.

## Results

Claude: Opus, effort high. Codex: gpt-6-sol, effort high. The last run of each, after the fixes below.

| Skill | Checks | Judge lines | Claude | Codex | Baseline (no skill) |
|---|---|---|---|---|---|
| init | 4 | 5 | pass | pass | fail |
| choisir | 4 | 6 | pass | pass | — |
| affiner | 9 | 8 | pass | pass | fail |
| decouper | 10 | 7 | pass | pass | fail |
| realiser | 13 | 6 | fail (an English note) | pass | fail |
| examiner | 10 | 6 | pass | pass | fail |
| rendre | 13 | 6 | pass | pass | fail |
| verifier | 7 | 6 | pass | pass | fail |

`realiser` was cut from 2,044 to 1,056 words, its test rules moved to `cadrer-x-tdd`. Its case now
places its helpers (`"with"`) and adds a mutation check: `evals/mutants.py` flips each comparison and
turns each refusal into a silent return in the new `signup/api.py`, runs the task's tests on each, and
passes when at least 80% fail. The new version: 5/6 caught on Claude, 6/7 on codex. Its Claude run
failed only on one progress note written in English, a failure the old version also had twice.

The helpers (`tdd`, `securite`, `debug`, `modules`, `design-system`, `textes`) have no case of their
own. A case places the ones it needs with `"with"` (only `realiser` does so far); without it, a helper
is absent. A run with every skill installed showed `examiner` opening `cadrer-x-securite` and
`cadrer-x-modules` by path.

## What the runs changed

| Run | What failed | The fix |
|---|---|---|
| realiser, codex | the test went red first, but the reply never showed it | the report shows each red run's failing line: the person never saw the terminal |
| realiser, codex | the pre-existing failure named, its folder not said to be untouched | name it by its exact test name, and the folder left untouched |
| examiner, codex | `my_sign_ups` held against M3 instead of as `non demandé` | list each function, route, page and table the story adds, and match each to what asks for it |
| examiner, codex | the border finding did not name the function to call instead | a border finding names the other module's entry function |
| examiner, codex | the reply counted every finding to fix as `Bloquant` | the reply counts `Bloquant :` and `À corriger :` apart, from the committed audit |
| examiner, all skills | helpers never loaded ("load … when installed" was ignored) | each skill opens `../cadrer-x-<name>/SKILL.md` by path, at the step that needs it |
| realiser, both | test rules spread through a 2,044-word skill | `cadrer-x-tdd` (after Matt Pocock's `tdd`): through the entry, no tautology, one test at a time, mocks at the edges |
| decouper, claude | the judge called a task's rate limit an unrequested feature | judge line: a protection on a task's `Risques :` line is not out of scope |

## Harness notes

- A fixture is committed as one commit, so `main` equals the feature branch and there is no history:
  `examiner` reviews the tasks' `Fichiers :` instead of a diff.
- `init` is `disable-model-invocation: true`, yet its quiet trigger prompts count as "fired" on Claude:
  in a near-empty fixture, Claude reads the skill's files as repo content, and the harness counts that read.
- A Claude run before dotfiles `7747260` could end with an empty final message and fail `test -s "$OUT"`
  with every judge line passing (`choisir`, 03:30).
