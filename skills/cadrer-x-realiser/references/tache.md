# Build one task — test first, fresh evidence

The builder's procedure, for one task of `taches.md` or one fix round of `audit.md`. Followed by a
builder `realiser` starts (its prompt says *Launched by realiser*), or by `realiser` itself when the
person names one task (`/cadrer-x-realiser T03`). The task's boxes are the done-when, its `Fichiers :`
the files you touch, the checks of `cadrer-x.yml` the bar. Other tasks may be built at the same time,
so you work in the task's own worktree. Whoever built a task never reviews it.

Talk, and write, in the person's language; in French, *tu* or *vous* as they write, *vous* when you
can't tell, never both. Commit messages, file names and labels stay as written here.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `<skills folder>/cadrer-x-<name>/SKILL.md`
(the folder that holds `cadrer-x-realiser/`) at that moment; read it whole and follow it. Not there: go
on without it. Never through the Skill tool: read the file.

**Launched by realiser.** You never merge, never push, never ask the person: they are not here (run by hand with the person present, ask them directly and merge as realiser's *Merge* says). What
you would ask goes in your report, and your last message is that report (the end of this file).

## The task and its worktree

Read `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`.

- **The task**: `T<nn>` in `{feature}/taches.md` on `feature/<slug>`. Already `[x]`: say so, stop. A
  task on its `Après :` line not yet `[x]` there: say which it waits for, stop.
- **The worktree**: `.worktrees/` in `.git/info/exclude`, then `git worktree add -b tache/<slug>-t<nn>
  .worktrees/tache.<slug>-t<nn> feature/<slug>` (lowercase), or reuse both. Copy the untracked `.env*`
  files from the repo's top (never commit them) and run `commands.install` there. Everything below runs
  in that worktree.

## Before any change

Read the task's block, its story in `{feature}/spec.md` (the scenarios are the truth), the
**À surveiller** lines pinned to it, the answered questions of `{feature}/a-trancher.md`,
`{docs}/constitution.md`, `{docs}/architecture.md` → **Modules**, `{docs}/glossaire.md`. Read `cadrer-x-tdd`,
`cadrer-x-modules`, and, when the task has a `Risques :` line or opens a way in, `cadrer-x-securite`.
With an `Écrans :` line, read `cadrer-x-design-system`. With a text a person reads that `contenu.md`
lacks, read `cadrer-x-textes`.

Run the whole check command once. A failure now is not yours and not a stop: note the test's exact
name and build the task anyway.

## Build it, one test at a time

Follow `cadrer-x-tdd`: each box a test at the module's entry, named like the box, with the spec's
values, watched failing on its assertion before its code. Then each risk of `Risques :` and the abuse
tests of `cadrer-x-securite`. A bug met on the way: read `cadrer-x-debug`. Never lower a bar to get
green (a loosened assertion, a skip, a moved threshold, a silenced checker): fix the code.

A task with screens: its section of `passation.md`, its page in `maquette/` and `contenu.md` are the
whole design; the words exactly as `contenu.md` has them. With `commands.dev` and a browser tool free,
open the screens at 390 and 1280 wide before you finish; the browser held, or no tool: say they were
not opened, and never write a browser driver of your own.

## Stay in the task

- Touch only `Fichiers :`. Two exceptions, each a `Choix :` line of the commit: the setup the tests
  need to run cleanly (`"type": "module"` in `package.json`, the runner's config), and a test helper the
  task's own tests share. Any other file outside it the task truly needs: a question.
- Never edit `spec.md`, `passation.md`, `maquette/`, `contenu.md`, `cadrer-x.yml`, `{docs}/` or a lock
  file; in `taches.md`, only your task's `[ ]` → `[x]`. No dependency `decisions.md` or the
  constitution does not allow.
- Something worth fixing elsewhere, out of the task: leave it, put it under `À savoir`.

**Decide, or ask.** A choice no one will see (a name, how a race is prevented): the smallest one, as a
`Choix :` line of the commit. A choice a person would see that no file settles, or a gap they would
see that no box covers (a text, a state, a wait, a number shown): a question now, with your
recommendation, never a note at the end; a gap left for later comes back as a review finding and a
fix round. Ask before anything destructive, anything touching a secret or a permission, and anything
outside this worktree. Launched by realiser: build all that does not hang on the answer, then report
with `Statut : question`.

## Done means fresh evidence

1. The whole check command, in this worktree; read the exit code.
2. Each box and each risk: its test, green in this run.
3. A failure you did not cause: named by its exact test name, one line on why it is not yours, its
   files left untouched.
4. Claim only what this run shows, never "should pass".
5. Tick your task `[x]` (its line and its boxes) and commit on the task branch: `T<nn> — <titre>`,
   with the `Choix :` lines in the body.

## A fix round

For `US<n>`: the story's `Bloquant :` and `À corriger :` findings in the latest section of
`{feature}/audit.md`. Branch `tache/<slug>-us<n>-correctifs`, worktree
`.worktrees/tache.<slug>-us<n>-correctifs`. Each finding: a red test that reproduces it, then the fix.
A missing behaviour becomes a new task at the end of the story's section of `taches.md`, built and
ticked here; never rewrite an old task. A finding you think is wrong: a question, never skipped. Commit
`correctifs US<n>`, each finding named.

## The report

Your last message, in the person's language, these labels as written:

```
Statut : fait | question | bloqué
Tâche : T<nn> — <titre>  (or: Correctifs : US<n>)
Branche : tache/<slug>-t<nn>, <commit>
Cases :
- <the box> — <its test> — rouge vu : <the failing assertion line, trimmed>
Risques :
- <the risk> — <its test> — rouge vu : <…>
Vérifs : <the command> — code <n> — <its summary line> ; échecs pas à moi : <test names, or aucun>
Choix :
- <each Choix line>
Questions :
- <the question, in plain words> — Conseil : <your recommendation, why>
À savoir :
- <what a person or the next task should know>
```

`fait`: ticked and committed, nothing asked. `question`: what remains hangs on the answers. `bloqué`:
the checks still red after three fixes that did not hold (`cadrer-x-debug`), a conflict in another task's file, or
something only the person can unblock; say what, under `Questions`. A section with nothing says
`aucun`.
