---
name: cadrer-x-realiser
description: "Construire une fonctionnalité, de ses tâches à ses récits relus. À lancer quand `taches.md` est prêt. Construit chaque tâche dans son worktree, test d'abord, deux à la fois quand c'est possible ; fusionne chacune dans la branche de la fonctionnalité ; fait relire chaque récit construit par un agent qui ne l'a pas construit ; corrige ce que la relecture trouve ; ne s'arrête que pour les questions de la personne. Aussi pour un seul récit (`US1`, ou refaire sa relecture) ou une seule tâche (`T03`)."
disable-model-invocation: true
argument-hint: "[fonctionnalité] [US1 | T03]"
---

# cadrer-x réaliser — every task built, every story reviewed

You run a feature's build to its end: builders (subagents) build each task test first in its own
worktree, merged into `feature/<slug>`; a reviewer who did not build reviews each built story; each
finding is fixed and rechecked. You build and review nothing yourself: start subagents (the tool's
general one: `general-purpose` in Claude Code, codex's default worker; never a registered or custom
agent type), merge, ask the person what only they can answer. Read `taches.md`, `audit.md` and the
reports, never the code.

Talk in the person's language, each note between tool calls too; in French, *tu* or *vous* as they
write, *vous* when unsure, never both. Commit messages, file names and labels stay as written here.

`<skills folder>`: the folder holding this skill's folder, absolute path. A reference you follow
yourself (`references/tache.md` by hand or with no subagents, `references/examen.md` in a review
session): after a summary of this conversation, read it again.

## What to build

Read `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **Feature**: the argument's number or slug (one close near miss: that one, said in one line), else
  the worktree you are in, else the one feature whose `taches.md` has open tasks; several: ask. Its
  worktree `.worktrees/feature.<slug>` (else `git worktree add` it, `.worktrees/` in
  `.git/info/exclude` first, untracked `.env*` copied in, `commands.install` run once). `{feature}` =
  its `{docs}/features/NNNN-<slug>/`.
- **Scope**: no argument or the feature: every story. `US<n>` (alone or after the feature): that
  story. Either way, a story whose latest `audit.md` section is `à corriger` starts with its fix round,
  or, if a `correctifs US<n>` commit came after that section, with its next review. `US<n>` built with
  no fix round due: its review, as *Reviews*. `T<nn>`: that task alone (*One task by hand*).
- **Commands.** Each command of `cadrer-x.yml` (`install`, each check, `dev.run`) missing from
  `.claude/settings.json` → `permissions.allow`: add it as `Bash(<the command>)` and say so in your
  first message (else a builder waits on a prompt at each run).
- **State** lives in the files, so a stopped run resumes: tasks `[x]` on the feature branch are built;
  a story with a `validé` section in `audit.md` is done, unless a task of it is still `[ ]` (*The end*,
  or a package's flaw) or the person typed its `US<n>`: such a task is built, then the story reviewed
  again; a leftover `tache/<slug>-*` branch is a builder's unmerged work (merge it as below if its
  report said `fait` and its commit ticks the task, else restart it).
- **Up to date.** Each run, before any builder or reviewer: `git -C <top>/.worktrees/feature.<slug>
  merge <main>`, then the whole check command there (`cd`). A conflict, or red: a builder, prompt
  « … to bring `feature/<slug>` up to date with `<main>` … »; its `fait` needs no merge.

**Then one message, and go.** (Short path, `voie : courte`: two lines, the tasks and that each story is
reviewed before the end.) Say what gets built (stories, tasks, waves), two tasks at a time when they
can, each story reviewed by someone who did not build it, and that you stop only for their
questions and at the end. They launched the build: start
right away; they can stop you.

## Builders

A task is **ready** when every task on its `Après :` is `[x]` on the feature branch. Start ready
tasks in `taches.md` order, **at most two at once** (or the person's number). Two run together only
if they share no `Fichiers :` file and at most one has an `Écrans :` line (one browser). Close each
subagent once its report is in and its work is merged or settled, before starting another: never
more than three open at once, builders and reviewers together (codex refuses a fourth).

A builder is a subagent with a fresh context and this prompt only: « You are cadrer-x-developpeur.
Read `<skills folder>/cadrer-x-realiser/references/tache.md` whole and follow it, for task `T<nn>`
of the feature `<NNNN-slug>`. The repo's top: `<path>`. Launched by realiser. » Never the Skill
tool: the builder reads the file. Its last message is its report.

- **`fait`**: merge it (below), then start what it made ready.
- **`question`**: one about code, tests or `taches.md` is yours: answer it from the feature's files,
  else take the builder's recommendation: the review judges it. Only what the person sees or does
  reaches them, one question per message, in plain words, with that recommendation. Other builders
  go on. The answer goes back to that builder (resume it, else a new builder whose prompt adds the
  answer). An answer settling what the spec leaves open is written to `{feature}/a-trancher.md` as a
  question with its **Réponse**, committed on the feature branch: the reviewer reads it as settled.
- **`bloqué`**: say what blocks, ask what to do, with your recommendation.

## Merge into the feature branch

A task merge is local and undoable: no yes needed. While a reviewer reads a feature branch, hold
its task merges until the audit is committed. Each git command names its folder with `-C` (`<top>`:
the repo's top); never a task merge or a reset in the main checkout.

1. `git -C <top>/.worktrees/tache.<slug>-t<nn> merge feature/<slug>`. Conflict in its own files: back
   to its builder, told the conflict; in another task's: stop, ask the person. Then the whole check
   command in that worktree (`cd`); red: back to its builder.
2. `git -C <top>/.worktrees/feature.<slug> merge --ff-only tache/<slug>-t<nn>`; refused: step 1 again.
3. `git -C <top> worktree remove .worktrees/tache.<slug>-t<nn>`; then `git -C <top> merge-base
   --is-ancestor tache/<slug>-t<nn> feature/<slug>` and on yes `git -C <top> branch -D
   tache/<slug>-t<nn>` (`-d` would check the main branch). Never push.

## Reviews

A story is **built** when its tasks and the Fondations tasks they stand on are `[x]` on the feature
branch. Review it then, while other stories' builders go on. A reviewer is a fresh-context subagent,
never one that built, with this prompt only (never a builder's report): « You are
cadrer-x-relecteur. Read `<skills folder>/cadrer-x-realiser/references/examen.md` whole and follow
it, for story `US<n>` of the feature `<NNNN-slug>`. Its screens:
`<skills folder>/cadrer-x-realiser/references/ecrans.md`. The repo's top: `<path>`.
Launched by realiser. » *Its screens* only when a task of the story has an `Écrans :` line, a box
names a page (short path), or `dev:` has no `url` (a terminal app). A story with screens is reviewed while no builder with an
`Écrans :` line runs.

- **`validé`**: two lines at most: what works now, what they can try; the rest waits for *The end*.
  Go on.
- **`à corriger`**: fix round. A new builder, prompt « … for the fix round of `US<n>` … », merged like a
  task (branch `tache/<slug>-us<n>-correctifs`, worktree `.worktrees/tache.<slug>-us<n>-correctifs`,
  in place of `-t<nn>`), then a new reviewer for the next tour. The first review is tour 1; the fix
  round and its re-review are tour 2. Still `à corriger` after tour 2: stop for the person: what is
  left, in plain words, your recommendation.
- Its questions: ask them as a builder's.

## The end

Every story `validé`: one message with, per story, its verdict and what it does now, the captures, the
`Détail :` lines left, the questions answered, then `/cadrer-x-rendre <slug>`, better in a new session
(`/clear`, then the command). Then stop: the delivery is theirs to start.

A change they ask once its story is `validé`, a text too, is a task: the highest `T<nn>` plus one,
last in its story's section, one box for the change, the other lines from the task that built that
part, `Après :` that task. A text: in `contenu.md` first, if it has one. Against a scenario or a
decision: ask once, plainly, whether it replaces it; the answer goes in `a-trancher.md`, and a yes
changes the scenario in `spec.md` (a no: no task). choisir's lint (`taches`) clean, committed. Then *State*.

## One task by hand

`/cadrer-x-realiser T<nn>`: build it yourself, here, following `references/tache.md` (you are the
builder; the person is here, so ask them directly). Merge as above. If its story is now built, review
it as above. Another person may build another task meanwhile, in another session.

## No subagents

Codex starts subagents when asked: this file asks. With no way to start one, build the tasks one after
another yourself, each following `references/tache.md`, merged as above. A review needs a mind that did
not build: when a story is built, stop and give the person `/cadrer-x-realiser <slug> US<n>` for a new
session, then `/cadrer-x-realiser <slug>` again: it resumes from the files. The `US<n>` session, having
built none of the story, reviews it itself: `references/examen.md`, with what *Reviews* names.

## Red flags

| Thought | Instead |
|---|---|
| "The builder noted a missing text; the review will catch it." | A gap a person would see is a question now. |
| "Only a text; I'll edit it myself." | A task: *The end*. |
| "Two screen tasks at once, it's faster." | One browser: one at a time. |
| "Tour 2 still à corriger; one more round." | Two tours, then the person decides. |
| "The Skill tool refused; I'll stop." | They read the file. |
| "`--ff-only` refused; I'll redo it here." | Step 1 again, `-C` and all. |
