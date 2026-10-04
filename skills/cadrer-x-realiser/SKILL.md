---
name: cadrer-x-realiser
description: "Construire une fonctionnalité, de ses tâches à ses récits relus. À lancer quand `taches.md` est validé. Construit chaque tâche dans son worktree, test d'abord, deux à la fois quand c'est possible ; fusionne chacune dans la branche de la fonctionnalité ; fait relire chaque récit construit par un agent qui ne l'a pas construit ; corrige ce que la relecture trouve ; ne s'arrête que pour les questions de la personne. Aussi pour un seul récit (`US1`) ou une seule tâche (`T03`)."
disable-model-invocation: true
argument-hint: "[fonctionnalité | US1 | T03]"
---

# cadrer-x réaliser — every task built, every story reviewed

You run the build of a feature to its end: each task built test first by a builder in its own
worktree, merged into `feature/<slug>`; each story, once built, reviewed by a reviewer who did not
build it; each finding fixed and checked again. You build nothing and review nothing yourself: you
start builders and reviewers as subagents, merge their work, and ask the person what only they can
answer. You read `taches.md`, `audit.md` and their reports, never the code: that keeps this session
light enough for a whole feature.

Talk in the person's language, every message included (the short notes between steps too); in French,
*tu* or *vous* as they write, *vous* when you can't tell, never both. Commit messages, file names and
labels stay as written here.

`<skills folder>` is the folder that holds this skill's folder, as an absolute path.

## What to build

Read `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **The feature**: the argument's number or slug (a near miss with one close feature: that one, said in
  one line), else the worktree you are in, else the one feature whose `taches.md` has open tasks;
  several: ask which. Its worktree `.worktrees/feature.<slug>` (else `git worktree add` it,
  `.worktrees/` in `.git/info/exclude` first, the untracked `.env*` files copied in, `commands.install`
  run once). `{feature}` is its `{docs}/features/NNNN-<slug>/`.
- **The scope**: no argument or the feature: every story. `US<n>`: that story. In both, a story whose
  latest section of `audit.md` is `à corriger` starts with its fix round, or, when a `correctifs US<n>`
  commit already came after that section, with its next review. `T<nn>`: that task alone (see *One task
  by hand*).
- **The commands it runs.** Each command of `cadrer-x.yml` (`install`, each check, `dev.run`) that
  `.claude/settings.json` → `permissions.allow` lacks: add it as `Bash(<the command>)`, and say so in
  your first message; a builder otherwise waits on a prompt for each run. The git commands are there
  when `install.sh` installed cadrer-x in this project; after a global install, say once that each
  git command will ask, and that `./install.sh` run in the project allows them.
- **The state** is in the files, so a run that stopped picks up where it was: tasks `[x]` on the feature
  branch are built; a story with a `validé` section in `audit.md` is done; a `tache/<slug>-*` branch
  left over is a builder's unmerged work (merge it as below when its report said `fait` and its commit
  ticks the task, else start it again).

**Then one message, and go.** (On the short path, `voie : courte`, the message is two lines: the tasks, and that the story is reviewed before the end.) What gets built (the stories, how many tasks, the waves), that tasks run
two at a time when they can, that each story is reviewed by someone who did not build it and its
findings fixed, and that you stop only for their questions and at the end. They launched the build:
start right away; they can stop you at any time.

## Builders

A task is **ready** when every task on its `Après :` is `[x]` on the feature branch. Start the ready
tasks in `taches.md` order, **at most two at once** (or the number the person gives). Two run together
only when they share no file on `Fichiers :` and at most one has an `Écrans :` line: there is one
browser.

Each builder is a subagent with a fresh context and this prompt, nothing more: « Read
`<skills folder>/cadrer-x-realiser/references/tache.md` whole and follow it, for task `T<nn>` of the
feature `<NNNN-slug>`. The repo's top: `<path>`. Launched by realiser. » Never the Skill tool: the
skills are the person's to launch; the builder reads the file. Its last message is its report.

- **`fait`**: merge it (below), then start what it made ready.
- **`question`**: ask the person, one question per message, with the builder's recommendation and one
  line of context (which task, what it is for). Other builders go on meanwhile. The answer goes back to
  that builder (resume it; else a new builder whose prompt adds the answer). An answer that settles
  what the spec leaves open is written to `{feature}/a-trancher.md` as a question with its **Réponse**,
  committed on the feature branch: the reviewer reads it as settled.
- **`bloqué`**: say what blocks, and ask what to do, with your recommendation.

## Merge into the feature branch

Merging a task into `feature/<slug>` is local and taken back with one command: no yes needed. A reviewer reads the feature branch, so do not move it under the reviewer: while one runs, hold the merges of that feature's tasks until its audit is committed.

1. In the task's worktree: `git merge feature/<slug>`, to bring in what other tasks merged. A conflict
   in the task's own files: back to its builder (resume it, or a new one with the conflict named). In
   another task's file: stop, and ask the person. Then the whole check command there; red: back to its
   builder.
2. In the feature's worktree: `git merge --ff-only tache/<slug>-t<nn>`; refused: step 1 again.
3. From the repo's top, never from inside it: `git worktree remove .worktrees/tache.<slug>-t<nn>`; then
   `git merge-base --is-ancestor tache/<slug>-t<nn> feature/<slug>` and, when it says yes, `git branch
   -D tache/<slug>-t<nn>` (`-d` checks the main branch, where it is not merged yet). Never push.

## Reviews

A story is **built** when its tasks, and the Fondations tasks they stand on, are `[x]` on the feature
branch. Start its review then, while builders of other stories go on in their worktrees. A reviewer is
a subagent with a fresh context, never one that built, and this prompt, nothing more (never a builder's
report: the reviewer forms its own view): « Read `<skills folder>/cadrer-x-examiner/SKILL.md` whole and
follow it, for story `US<n>` of the feature `<NNNN-slug>`. The repo's top: `<path>`. Launched by
realiser. » A story with screens is reviewed while no builder with an `Écrans :` line runs.

- **`validé`**: one short message to the person: the story works now, what they can try, the captures
  (`{feature}/captures/`), the `Détail :` lines. Then go on.
- **`à corriger`**: a fix round. A new builder, prompt « … for the fix round of `US<n>` … », merged
  like a task, then a new reviewer for the next tour. Still `à corriger` after its second tour: stop for
  the person: what is left, in plain words, and your recommendation.
- Its questions: ask them as a builder's.

## The end

Every story `validé`: one message, per story its verdict and what it does now, the captures, the
`Détail :` lines left, the questions answered on the way. Then delivery: `/cadrer-x-rendre <slug>`
writes the docs, then merges into the main branch and puts it online, each on their yes. Go on
with it here, said in one line (they can stop you): open `<skills folder>/cadrer-x-rendre/SKILL.md`, read it whole and follow
it for this feature. It asks for its own yes before any merge or push.

## One task by hand

`/cadrer-x-realiser T<nn>`: build it yourself, here, following `references/tache.md` (you are the
builder: the person is here, so ask them directly). Merge it as above. Its story now built: start its
review as above. A second person may build another task at the same time, in another session.

## No subagents

Codex starts subagents when asked: this file asks. With no way to start one, build the tasks one after
another yourself, each following `references/tache.md`, merged as above. A review needs a mind that
did not build: when a story is built, stop and give the person `/cadrer-x-examiner US<n>`, in a new
session, then `/cadrer-x-realiser <slug>` again: it picks up from the files.

## Red flags

| Thought | Instead |
|---|---|
| "I'll just write this task myself, it's small." | A builder builds; you merge and ask. |
| "Green: I'll ask before merging into the feature." | Local and reversible: merge. The main branch is rendre's, on a yes. |
| "The builder noted a missing text; the review will catch it." | A gap a person would see is a question now. |
| "I'll tell the reviewer what the builder did." | Its prompt names the story, nothing more. |
| "Two screen tasks at once, it's faster." | One browser: one at a time. |
| "Tour 2 still à corriger; one more round." | Two tours, then the person decides. |
| "The Skill tool refused; I'll stop." | Builders and reviewers read the file, never the Skill tool. |
| "`git branch -d` failed: not merged." | It checks the main branch: `merge-base --is-ancestor` on the feature, then `-D`. |
