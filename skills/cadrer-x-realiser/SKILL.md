---
name: cadrer-x-realiser
description: "Construire une fonctionnalité, de ses tâches à ses récits relus. À lancer quand `taches.md` est validé. Construit chaque tâche dans son worktree, test d'abord, deux à la fois quand c'est possible ; fusionne chacune dans la branche de la fonctionnalité ; fait relire chaque récit construit par un agent qui ne l'a pas construit ; corrige ce que la relecture trouve ; ne s'arrête que pour les questions de la personne. Aussi pour un seul récit (`US1`) ou une seule tâche (`T03`)."
disable-model-invocation: true
argument-hint: "[fonctionnalité | US1 | T03]"
---

# cadrer-x réaliser — every task built, every story reviewed

You run a feature's build to its end: builders (subagents) build each task test first in its own
worktree, merged into `feature/<slug>`; a reviewer who did not build reviews each built story; each
finding is fixed and rechecked. You build and review nothing yourself: start subagents, merge, ask the
person what only they can answer. Read `taches.md`, `audit.md` and the reports, never the code: that
keeps this session light enough for a whole feature.

Talk in the person's language, every message included; in French, *tu* or *vous* as they write, *vous*
when unsure, never both. Commit messages, file names and labels stay as written here.

`<skills folder>`: the folder holding this skill's folder, absolute path.

## What to build

Read `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **Feature**: the argument's number or slug (one close near miss: that one, said in one line), else
  the worktree you are in, else the one feature whose `taches.md` has open tasks; several: ask. Its
  worktree `.worktrees/feature.<slug>` (else `git worktree add` it, `.worktrees/` in
  `.git/info/exclude` first, untracked `.env*` copied in, `commands.install` run once). `{feature}` =
  its `{docs}/features/NNNN-<slug>/`.
- **Scope**: no argument or the feature: every story. `US<n>`: that story. Either way, a story whose
  latest `audit.md` section is `à corriger` starts with its fix round, or, if a `correctifs US<n>`
  commit came after that section, with its next review. `T<nn>`: that task alone (*One task by hand*).
- **Commands.** Each command of `cadrer-x.yml` (`install`, each check, `dev.run`) missing from
  `.claude/settings.json` → `permissions.allow`: add it as `Bash(<the command>)` and say so in your
  first message (else a builder waits on a prompt at each run). Git commands are there when
  `install.sh` installed cadrer-x in the project; after a global install, say once that each git
  command will ask and that `./install.sh` run in the project allows them.
- **State** lives in the files, so a stopped run resumes: tasks `[x]` on the feature branch are built;
  a story with a `validé` section in `audit.md` is done, unless a task of it is still `[ ]` (one
  `rendre` added for a flaw in a package): that task is built, then the story reviewed again; a leftover `tache/<slug>-*` branch is a
  builder's unmerged work (merge it as below if its report said `fait` and its commit ticks the task,
  else restart it).

**Then one message, and go.** (Short path, `voie : courte`: two lines, the tasks and that the story is
reviewed before the end.) Say what gets built (stories, number of tasks, waves), that tasks run two at
a time when they can, that each story is reviewed by someone who did not build it and its findings
fixed, and that you stop only for their questions and at the end. They launched the build: start
right away; they can stop you.

## Builders

A task is **ready** when every task on its `Après :` is `[x]` on the feature branch. Start ready tasks
in `taches.md` order, **at most two at once** (or the person's number). Two run together only if they
share no `Fichiers :` file and at most one has an `Écrans :` line (one browser).

A builder is a subagent with a fresh context and this prompt only: « Read
`<skills folder>/cadrer-x-realiser/references/tache.md` whole and follow it, for task `T<nn>` of the
feature `<NNNN-slug>`. The repo's top: `<path>`. Launched by realiser. » Never the Skill tool (skills
are the person's to launch): the builder reads the file. Its last message is its report.

- **`fait`**: merge it (below), then start what it made ready.
- **`question`**: ask the person, one question per message, with the builder's recommendation and one
  line of context (task, purpose). Other builders go on. The answer goes back to that builder (resume
  it, else a new builder whose prompt adds the answer). An answer settling what the spec leaves open is
  written to `{feature}/a-trancher.md` as a question with its **Réponse**, committed on the feature
  branch: the reviewer reads it as settled.
- **`bloqué`**: say what blocks, ask what to do, with your recommendation.

## Merge into the feature branch

Merging a task into `feature/<slug>` is local and undone with one command: no yes needed. A reviewer
reads the feature branch, so do not move it under them: while one runs, hold that feature's task merges
until its audit is committed.

1. In the task's worktree: `git merge feature/<slug>` (brings in other tasks' merges). Conflict in the
   task's own files: back to its builder (resume, or a new one with the conflict named). In another
   task's file: stop, ask the person. Then the whole check command there; red: back to its builder.
2. In the feature's worktree: `git merge --ff-only tache/<slug>-t<nn>`; refused: step 1 again.
3. From the repo's top, never from inside it: `git worktree remove .worktrees/tache.<slug>-t<nn>`; then
   `git merge-base --is-ancestor tache/<slug>-t<nn> feature/<slug>` and on yes `git branch
   -D tache/<slug>-t<nn>` (`-d` checks the main branch, where it is not merged yet). Never push.

## Reviews

A story is **built** when its tasks and the Fondations tasks they stand on are `[x]` on the feature
branch. Review it then, while other stories' builders go on. A reviewer is a fresh-context subagent,
never one that built, with this prompt only (never a builder's report: it forms its own view): « Read
`<skills folder>/cadrer-x-examiner/SKILL.md` whole and follow it, for story `US<n>` of the feature
`<NNNN-slug>`. The repo's top: `<path>`. Launched by realiser. » A story with screens is reviewed
while no builder with an `Écrans :` line runs.

- **`validé`**: one short message: the story works now, what they can try, the captures
  (`{feature}/captures/`), the `Détail :` lines. Go on.
- **`à corriger`**: fix round. A new builder, prompt « … for the fix round of `US<n>` … », merged like a
  task (branch `tache/<slug>-us<n>-correctifs`, worktree `.worktrees/tache.<slug>-us<n>-correctifs`,
  in place of `-t<nn>`), then a new reviewer for the next tour. The first review is tour 1; the fix
  round and its re-review are tour 2. Still `à corriger` after tour 2: stop for the person: what is
  left, in plain words, your recommendation.
- Its questions: ask them as a builder's.

## The end

Every story `validé`: one message with, per story, its verdict and what it does now, the captures, the
`Détail :` lines left, the questions answered. Then delivery: `/cadrer-x-rendre <slug>` writes the
docs, merges into the main branch and puts it online, each on their yes. Go on with it here, said in
one line (they can stop you): open `<skills folder>/cadrer-x-rendre/SKILL.md`, read it whole, follow it
for this feature. It asks its own yes before any merge or push.

## One task by hand

`/cadrer-x-realiser T<nn>`: build it yourself, here, following `references/tache.md` (you are the
builder; the person is here, so ask them directly). Merge as above. If its story is now built, review
it as above. Another person may build another task meanwhile, in another session.

## No subagents

Codex starts subagents when asked: this file asks. With no way to start one, build the tasks one after
another yourself, each following `references/tache.md`, merged as above. A review needs a mind that did
not build: when a story is built, stop and give the person `/cadrer-x-examiner US<n>` for a new session,
then `/cadrer-x-realiser <slug>` again: it resumes from the files.

## Red flags

| Thought | Instead |
|---|---|
| "The builder noted a missing text; the review will catch it." | A gap a person would see is a question now. |
| "I'll tell the reviewer what the builder did." | Its prompt names the story, nothing more. |
| "Two screen tasks at once, it's faster." | One browser: one at a time. |
| "Tour 2 still à corriger; one more round." | Two tours, then the person decides. |
| "The Skill tool refused; I'll stop." | Builders and reviewers read the file, never the Skill tool. |
| "`git branch -d` failed: not merged." | It checks the main branch: `merge-base --is-ancestor` on the feature, then `-D`. |
