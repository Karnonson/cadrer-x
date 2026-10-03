---
name: cadrer-x-realiser
description: "Réaliser une tâche de `taches.md`. À lancer avec l'identifiant d'une tâche (`T03`), une tâche par session ; les tâches `[P]` peuvent tourner en même temps dans des sessions séparées. Travaille dans le worktree de la tâche, écrit d'abord un test qui échoue, puis le code, lance toutes les vérifs, et fusionne dans la branche de la fonctionnalité sur un oui. Aussi pour corriger ce qu'une relecture (`audit.md`) a trouvé sur un récit."
disable-model-invocation: true
argument-hint: "<T01, ou US1 pour les correctifs d'une relecture> [fonctionnalité]"
---

# cadrer-x réaliser — one task, test first, fresh evidence

You build one task of `taches.md`: its boxes are the done-when, its `Fichiers :` the only files you
touch, the checks of `cadrer-x.yml` the bar. Other tasks may be built at the same time in other
sessions, so you work in the task's own worktree and merge on the person's yes. Whoever built a task
never reviews it: `/cadrer-x-examiner` does, in another session.

Talk in the person's language, every message included (the short notes between steps too); in French,
*tu* or *vous* as they write, *vous* when you can't tell, never both. Commit messages, file names and
labels stay as written here.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## The task and its worktree

Read `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **The feature**: the second argument, else the worktree you are in, else the one whose `taches.md`
  (on `feature/<slug>`) holds the task; several: ask which.
- **The task**: `T<nn>` in `{feature}/taches.md` on the feature branch. Already `[x]`: say so, stop.
  A task named on its `Après :` line not yet `[x]` there: say which it waits for, stop. `US<n>`: a fix
  round (below).
- **The worktree**: `.worktrees/` in `.git/info/exclude`, then `git worktree add -b tache/<slug>-t<nn>
  .worktrees/tache.<slug>-t<nn> feature/<slug>` (lowercase), or reuse both. Copy the untracked `.env*`
  files from the repo's top (never commit them) and run `commands.install` there. Everything below runs
  in that worktree.

## Before any change

Read the task's block, its story in `{feature}/spec.md` (the scenarios are the truth), the
**À surveiller** lines pinned to it, `{docs}/constitution.md`, `{docs}/architecture.md` → **Modules**
and **Mots**. Read `cadrer-x-tdd`, `cadrer-x-modules`, and, when the task has a `Risques :` line or
opens a way in, `cadrer-x-securite`. With an `Écrans :` line, read `cadrer-x-design-system`.

Run the whole check command once. A failure now is not yours and not a stop: note the test's exact
name and build the task anyway.

## Build it, one test at a time

Follow `cadrer-x-tdd`: each box a test at the module's entry, named like the box, with the spec's
values, watched failing on its assertion before its code. Then each risk of `Risques :` and the abuse
tests of `cadrer-x-securite`. A bug met on the way: read `cadrer-x-debug`. Never lower a bar to get
green (a loosened assertion, a skip, a moved threshold, a silenced checker): fix the code.

A task with screens: its section of `passation.md`, its page in `maquette/` and `textes.md` are the
whole design; the words exactly as `textes.md` has them. With `commands.dev` and a browser tool, open
the screens at 390 and 1280 wide before you finish; otherwise say they were not opened.

## Stay in the task

- Touch only `Fichiers :`. A file outside it the task truly needs: ask, with your recommendation, and
  name it in the commit message.
- Never edit `spec.md`, `passation.md`, `maquette/`, `textes.md`, `cadrer-x.yml`, `{docs}/` or a lock
  file; in `taches.md`, only your task's `[ ]` → `[x]`. No dependency `decisions.md` or the
  constitution does not allow.
- Something worth fixing elsewhere: leave it, say it at the end.

**Decide, or ask.** A choice no one will see (a name, how a race is prevented): the smallest one, as a
`Choix :` line of the commit. A choice a person would see that no file settles: one question, with
your recommendation. Ask before anything destructive, anything touching a secret or a permission, and
anything outside this worktree.

## Done means fresh evidence

1. The whole check command, in this worktree; read the exit code.
2. Each box and each risk: its test, green in this run.
3. A failure you did not cause: named by its exact test name, one line on why it is not yours, its
   files left untouched.
4. Claim only what this run shows, never "should pass".
5. Tick your task `[x]` (its line and its boxes) and commit on the task branch: `T<nn> — <titre>`,
   with the `Choix :` lines in the body.

Then one message: each box and each risk with its test and the red run you saw before its code (the
failing assertion line, trimmed: the person never saw your terminal); the last whole-suite run; the
choices; what you noticed; one question: merge into `feature/<slug>` now?

## Merge — only after the yes

1. In the worktree, `git merge feature/<slug>` to bring in what other tasks merged. A conflict in your
   files: keep both behaviours. In another task's file: stop, say which. Then the checks again.
2. Where `feature/<slug>` is checked out: `git merge --ff-only tache/<slug>-t<nn>`; refused: step 1.
3. `git worktree remove .worktrees/tache.<slug>-t<nn>`, `git branch -d tache/<slug>-t<nn>`. Never push.
4. Next: the tasks now unblocked (`/cadrer-x-realiser T<nn>`, each in its own session); when the
   story's tasks are all `[x]`, `/cadrer-x-examiner US<n>` in a new session.

## A fix round

`/cadrer-x-realiser US<n>`: the story's `Bloquant :` and `À corriger :` findings in `{feature}/audit.md`.
Branch `tache/<slug>-us<n>-correctifs`, worktree `.worktrees/tache.<slug>-us<n>-correctifs`. Each
finding: a red test that reproduces it, then the fix. A missing behaviour becomes a new task at the end
of the story's section of `taches.md`, built and ticked here; never rewrite an old task. Commit
`correctifs US<n>`, each finding named; the same merge; then `/cadrer-x-examiner US<n>`, new session.

## Red flags

| Thought | Instead |
|---|---|
| "Code first, tests after." | One failing test, watched failing, then its code. |
| "Loosen this assertion and it's green." | The code is wrong. |
| "That failing test isn't mine; quick fix." | Name it, leave it. |
| "Green: I'll merge." | Ask first. Never push. |
| "I built it, I'll review it too." | `/cadrer-x-examiner`, another session. |
