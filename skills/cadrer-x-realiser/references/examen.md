# Review a story — by someone who did not build it

The reviewer's procedure, for one story of `taches.md`. Followed by a reviewer `realiser` starts (its
prompt says *Launched by realiser*), or, with no subagents, by `realiser` itself in a session that
built none of the story (`/cadrer-x-realiser <slug> US<n>`).

Each task passed its builder's tests, written from the builder's reading of the spec: a misreading
passes them. You ask what they cannot: is this the story the person approved, and would its tests fail
if the behaviour broke? Read-only on the code: never edit, fix or refactor. You write one file,
`{feature}/audit.md`, the story's section, from `<skills folder>/cadrer-x-realiser/templates/audit.md`;
`/cadrer-x-realiser US<n>` fixes what you found.

Talk and write the audit in the person's language, every message included; in French, *tu* or *vous* as
they write, *vous* when unsure, never both. Headings, labels, prefixes and ids stay as written here and
in the template: realiser and rendre find them by these names.

**Helpers.** *read `cadrer-x-<name>`* = open `<skills folder>/cadrer-x-<name>/aide.md` (the folder that
holds `cadrer-x-realiser/`), read it whole, follow it. Not there: go on without it. Read as files,
never through the Skill tool.

**Launched by realiser** (its prompt says so): same work, file and commit; the person is not here, so
ask no one. A question only they can answer is an `Info :` line, in your last message (for realiser):
the verdict, the count of `Bloquant :` and `À corriger :`, each whole as `audit.md` has it, what you
could not judge, the questions. No next step.

## Which story, and where

Read first: `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **Feature.** The number or slug realiser names (its prompt or argument; one close near miss: that
  one, said in one line), else the worktree's feature, else the one whose `taches.md` has a story
  built and not yet `validé`; several: ask, one question.
- **Story.** The `US<n>` of the prompt or the argument.
- **Where.** `.worktrees/feature.<slug>`; else the current checkout if on `feature/<slug>`; else `git
  worktree add .worktrees/feature.<slug> feature/<slug>` (`.worktrees/` in `.git/info/exclude` first,
  untracked `.env*` copied in, `commands.install` run once). Uncommitted changes there: not yours to
  judge or keep; say so, stop.
- **Ready** = every `[US<n>]` task of `taches.md` is `[x]` on the feature branch, and so is every task
  they are `Après :` that has no story (Fondations): review those with the first story standing on
  them. A task unticked, or a story's `tache/<slug>-t<nn>` branch unmerged: say which, stop.
- **Re-review.** The story has an `audit.md` section with `Bloquant :` or `À corriger :` findings and a
  `correctifs US<n>` commit came after: see "Tour 2 and later".

## Read, in this order

Order matters: form your own view before reading anyone's account.

1. `{feature}/spec.md`: the story, each scenario, its `EF<n>`, the **Cas limites**. Scenarios are the truth.
2. `{feature}/taches.md`: the story's tasks, boxes, `Risques :`, `Fichiers :`, the **À surveiller**
   lines pinned to them, the story's **Couverts** rows.
3. `{feature}/decisions.md`, `{feature}/a-trancher.md` (answered = settled), `{docs}/constitution.md`
   (each `M<n>`), `{docs}/architecture.md` → **Modules**, `{docs}/glossaire.md`. Read `cadrer-x-securite`,
   `cadrer-x-modules`, `cadrer-x-tdd`.
4. With screens: `{feature}/passation.md` (each `SC<n>` whose `Récits :` names the story), its
   `maquette/` pages, `{feature}/contenu.md`. Read `cadrer-x-design-system`, `cadrer-x-textes`. On the
   short path, no `passation.md`: the page a box names, as `ecrans.md`, which realiser named, says.
5. Code and tests: each file on the tasks' `Fichiers :` as the feature branch has it now, and what they
   call. How it got there: `git log --oneline <main>..feature/<slug>`, then `git log -p` of the story's
   commits (`T<nn> — …`): a test strict in one commit and loosened later is how a bar gets lowered.
   `git diff <main>...feature/<slug>` for anything touched outside the tasks' files.
6. Run the whole check command of `cadrer-x.yml` once, fresh, in the feature's worktree; read the exit
   code. A failure in a test no task of this story owns: one `Info :` line, no finding.

Write your findings from these alone. **Only then** read what builders said: the commits' `Choix :`
lines and messages, the previous tour of `audit.md`. Check a claim against what you found: code and
command output are evidence, a message is not.

## The Spec axis (`### Spec`)

For each scenario, find the code that makes it true and the test that proves it. Type every gap:

- **manquant**: nothing does it;
- **partiel**: part does (the ordinary case without the refusal, one state of two);
- **contraire**: the code does otherwise;
- **non demandé**: code that no scenario, `EF<n>` or decision asks for.

Then the other way round: list each public function, route, page and table the story's files add and
match each to a scenario, `EF<n>` or decision. One matching none is `non demandé` (`À corriger :`,
removed or asked about), whatever else is wrong with it.

**Would the test fail?** A test that passes whatever the code does proves nothing. For each box, read
its test: does it assert the spec's own value, at the boundary the scenario names (the last seat, the
exact hour, the empty list), through the module's entry? For the scenarios that matter most (an `EF<n>`
that forbids something (« ne doit jamais »), each **À surveiller** line), prove it: in a throwaway
detached worktree outside the repo (`git worktree add --detach <a temp folder>/relecture-us<n>
feature/<slug>`), break the one line that makes it true, run that test alone, see whether it fails, then
`git worktree remove --force` it. Still green on broken code: `Détail :`, but `À corriger :` for
a security guard or a prohibition (`Bloquant :` if the behaviour it should guard is also wrong); no
test at all: `À corriger :`. Never break anything in the
feature's own worktree.

A spec's silence is not permission: what a reasonable person expects and the code breaks is a finding,
the **À surveiller** lines first. A scenario manquant or partiel is `Bloquant :`; the fix round adds
the missing work as a new task.

## The Rules axis (`### Règles`)

Each finding quotes its line.

- **A secret's value** in code, history or output: first finding, `Bloquant :`, with name, file:line and
  commit (`git log -S`), never the value; revoke it where issued; push no branch holding it until the
  history is cleaned.
- **Safe defaults**: an input used unchecked, a query built from text, a missing sign-in, a record
  read or changed without checking it is the person's own, a role checked only in the page, an error
  showing too much, personal data in a log.
- **Each risk** of the tasks' `Risques :`: its test exists, asserts the refusal **and** that nothing
  changed. None, or one passing without the guard: `À corriger :`; the guard missing: `Bloquant :`.
- **Constitution**: each `M<n>` the story touches. Broken: `Bloquant :`.
- **Module borders**: a module reading another's tables, going past its entry, a call the map does not
  list: quote the import or query, the **Modules** line it breaks, and the other module's entry
  function to call instead (`billing.api.get_invoice`), read from its entry file. A module the map
  lacks with no **Impact archi** line in `decisions.md`.
- **A lowered bar**: a moved threshold, a loosened assertion, a skipped or `try`-wrapped test, a
  silenced checker, a stub or TODO left, a dependency the constitution or `decisions.md` does not allow.
- **Words**: a name for a thing `{docs}/glossaire.md` names otherwise (« réservation » for
  « inscription »): `Détail :`.
- **Whose job.** `{docs}/architecture.md`, `{docs}/adr/`, `{docs}/security/`, `CHANGELOG.md` are
  `/cadrer-x-rendre`'s at ship time: their state is at most `Info :`; a task that edited them is `À
  corriger :` (another session may edit them too). A need no story asks for (a purge job, a new page)
  is an `Info :` and a question for the person, never a fix you demand.

## Screens

When realiser named `ecrans.md` (a screen in `passation.md`, a page a short path's box names, a
terminal app): read it whole and follow it. It feeds `Écrans :` in `### Non jugé` for `passation.md`'s
screens, else an `Info :` line of `### Spec`. Not named: no `Écrans :` line.

## One prefix per finding

| Prefix | When | Blocks |
|---|---|---|
| `Bloquant :` | wrong behaviour, a scenario manquant or partiel, someone else's data reachable, a secret, a constitution rule broken, a lowered bar hiding a wrong behaviour | yes |
| `À corriger :` | what else breaks a behaviour, leaks data or breaches a rule: a scenario or a risk with no test at all, a test of a security guard or a prohibition still green without it, code no scenario asks for, a border crossed, a bar lowered during the build, a text not `contenu.md`'s | yes |
| `Détail :` | ships as is: style, naming, a design token, any other weak test (it exists but would not fail) | no |
| `Info :` | what you checked and found right, what is someone else's, a question for the person | no |
| `Corrigé :` | a tour 2 finding the fix round closed | no |

Each finding: `- <Préfixe> : <file:line> — <manquant|partiel|contraire|non demandé, on the Spec axis> :
<what is wrong> ; <what a person meets because of it> ; correction : <the fix>`. Never soften one to
pass the story, never harden a detail.

## Write the audit

`{feature}/audit.md` from the template, created when absent. The story's section goes on top,
under the title: `## US<n> <titre>`, `**Tour** :`, `**Date** :`, `**Verdict** :` (`à corriger` if any
`Bloquant :` or `À corriger :` is left, else `validé`), then `### Spec`, `### Règles`, `### Non jugé`
(and `### Correctifs` from tour 2). A clean axis: `- aucun`. `### Non jugé` opens with `Vérifs :`
(`lancées — <the command, its exit code, the summary line>` or `pas lancées — <pourquoi>`) and, with
screens, `Écrans :` (`cliqués SC1 SC2` at each size, `pas cliqués — <pourquoi>`, or `cliqués SC1 ; pas
cliqués SC2 — <pourquoi>`); never claim more than you did. Then what you could not check (a real
outside service, a load), each with why. A previous tour's section of the same story is replaced, its
findings carried into `Corrigé :` or repeated.

Run `python3 <skills folder>/cadrer-x-realiser/scripts/lint.py audit {feature}/audit.md`; fix, rerun
until silent. Commit `audit.md` (and `captures/`) only, on the feature branch: `audit US<n> —
<verdict>`. Never push.

## Tell the person

One message: the verdict; per axis, the `Bloquant :` and `À corriger :` counts, from the audit.md you
just committed, named by those words; each in one line (what a person meets, the file); what you could
not judge; the questions only they can answer. Then the next step, nothing more:

- `à corriger`: `/cadrer-x-realiser US<n>`: fixes the findings, then has the story reviewed again.
- `validé`: the next story whose tasks are all built (`/cadrer-x-realiser <slug> US<m>`), or, when
  every story of `taches.md` has a `validé` section, `/cadrer-x-rendre`.

## Tour 2 and later

The fix round's commit (`correctifs US<n>`) answers the last tour's blocking findings. Check that, not
the whole story again: a review restarting every tour finds something new each time and never ends.

1. The last tour's `Bloquant :` and `À corriger :` findings, then the fix round's diff
   (`git diff <the last audit commit>..feature/<slug>`).
2. One line each, on its axis: `- Corrigé : <the finding, in a few words> — <file:line of the fix, the
   test that proves it>`, or the finding again, prefixed, with what is still wrong. Fixed where
   reported but left elsewhere of the same kind (same query, same missing check) is not fixed.
3. `### Correctifs`: the fix round's own lines. Wrong behaviour in them, or a test weakened to get
   through, is a finding like any other.
4. Anything else you meet is late: `Bloquant :` only with the concrete harm a person would meet (wrong
   or lost data, someone else's data, a secret, money, a constitution rule); less is `Info : tard —
   <file:line, what, the fix>`, and it passes.

## Red flags

| Thought | Instead |
|---|---|
| "The tests are green, so the story works." | Read each test against its scenario; break the line, see it fail. |
| "I'll fix this one-line bug while I'm here." | Read-only. A finding, with its fix; realiser does it. |
| "The commit says the race is handled." | A claim. Find the code and the test that prove it. |
| "The architecture doc wasn't updated: Bloquant." | `rendre`'s, at ship time: `Info :`. |
| "Tour 2: let me review the whole story again." | Check the fix round; anything else is late. |
| "The app needs a test user; I'll add one to the database." | `### Non jugé`, unless the project documents a way in. |
| "The browser is busy; I'll script Chrome myself." | Judge from the code; `Écrans : pas cliqués — navigateur occupé`. |
