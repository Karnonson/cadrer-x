---
name: cadrer-x-realiser
description: "Réaliser une tâche de `taches.md`. À lancer avec l'identifiant d'une tâche (`T03`), une tâche par session ; les tâches `[P]` peuvent tourner en même temps dans des sessions séparées. Travaille dans le worktree de la tâche, écrit d'abord un test qui échoue, puis le code, lance toutes les vérifs, et fusionne dans la branche de la fonctionnalité sur un oui. Aussi pour corriger ce qu'une relecture (`audit.md`) a trouvé sur un récit."
disable-model-invocation: true
argument-hint: "<T01, ou US1 pour les correctifs d'une relecture> [fonctionnalité]"
---

# cadrer-x réaliser — one task, test first, fresh evidence

You build one task of `taches.md`: its boxes are the done-when, its `Fichiers :` the only files you
touch, the checks of `cadrer-x.yml` the bar. You work in the task's own worktree, branched from the
feature, because other tasks may be built at the same time in other sessions; you merge back into
the feature on the person's yes. A story's tasks all built, `/cadrer-x-examiner` reviews the story in
another session: whoever built a task never judges it.

Talk in the person's language, every message included (the short notes between steps too); in French, *tu* or *vous* as they write, *vous* when you can't tell,
never both. Commit messages, file names and labels stay as written here.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which task, and where

Read first: `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **The feature.** The second argument, else the feature of the worktree you are in, else the one
  whose `taches.md` (on its `feature/<slug>` branch) holds the task; several: ask which, one question.
- **The task.** `T<nn>` in `{feature}/taches.md` as the feature branch has it now. Already `[x]`: say
  so, and stop. An `US<n>` argument: a fix round (below).
- **Its `Après :`.** Every task it names must be `[x]` on the feature branch, merged. One is not: say
  which tasks it waits for, which of them can start now, and stop.
- **Its worktree.** Branch `tache/<slug>-t<nn>` (lowercase), worktree `.worktrees/tache.<slug>-t<nn>`,
  from the feature branch's tip: `.worktrees/` in `.git/info/exclude` first, then `git worktree add -b
  tache/<slug>-t<nn> .worktrees/tache.<slug>-t<nn> feature/<slug>`, or reuse both when they exist (a
  session picked up where it stopped). Copy the untracked `.env*` files from the repo's top, never
  commit them; run `commands.install` there once. Every command below runs in that worktree.

## Before any change

1. Read the task's block in `taches.md`, its story in `{feature}/spec.md` (the scenarios are the
   truth; the boxes quote them), the **À surveiller** lines pinned to it, `{docs}/constitution.md`,
   and `{docs}/architecture.md` → **Modules** and **Mots**. Read `cadrer-x-modules` and `cadrer-x-securite`.
2. With an `Écrans :` line: the screen's section of `{feature}/passation.md`, its page in
   `{feature}/maquette/`, `{feature}/textes.md` (section "A task with screens").
3. Run the whole check command of `cadrer-x.yml` once, now, in the task's worktree. A failure before your first change is not
   yours and not a stop: note its name, build the task anyway, and say it at the end.
4. For each box and each risk, settle how it will be proven: the test's name, the call, the value
   the spec expects.

## Test first, every behaviour

No production code without a failing test first.

- Each box becomes a test named like it, through the module's entry, with the spec's own values;
  the expected value comes from the spec, never recomputed the way the code does.
- Run it and watch it fail because the behaviour is missing. An import error is not red yet: add
  the empty function so the test runs, and see it fail on its assertion.
- Then the least code that passes it; run it; the next box. One behaviour at a time.
- **One test per risk** of the `Risques :` line, named after it, asserting the refusal **and** that
  nothing changed (read the record again). Then, for each way in the task opens, the four misuses:

  | Misuse | The test calls it with… | It passes when… |
  |---|---|---|
  | no sign-in | no one, or an expired session | refused, nothing changed |
  | someone else's data | a second person and the first one's id | refused as not found, the record unchanged |
  | bad input | empty, the wrong type, a value outside the allowed set | refused as invalid, nothing stored |
  | too much input | one past the cap (no cap yet: set one that fits, and say so) | refused as invalid, nothing stored |

  A misuse the code allows is a bug in your task: fix the code, never the test.
- **A bug met on the way**, yours or not, starts with a red test that reproduces it; read `cadrer-x-debug`. Find the cause before changing code.
- **Never lower a bar to get green**: no loosened assertion, no skip, no `try` around the thing
  tested, no moved threshold, no silenced checker. A test that "flakes" is a bug to find.

## Safe by default

- Secrets come from the environment, by name; a missing one fails loudly where it is used. A
  secret's value is never written or shown: not in a file, a test, a commit, a log or your messages.
- Inputs are checked at the edge (type, shape, length); queries take parameters; text a person typed
  is shown as text, never as markup.
- Anything not public needs a signed-in person; a record is read or changed only after checking it is
  theirs; a role is checked on the server. Errors show a plain message; details go to the server log,
  never a secret.
- **A secret's value already committed** (this branch, the base, an old commit): stop. Don't use it,
  move it or "fix" it: history keeps it. Tell the person which secret (its name), which file and
  commit (`git log -S`), never the value: it must be revoked where it was issued, and no branch
  holding it may be pushed until the history is cleaned, which is theirs to do.

## Stay in the task

- Touch only `Fichiers :`. Another session may be changing the other files right now.
- A file outside it that the task truly needs (an export to add to another module's entry, so its
  border holds): ask the person, with your recommendation; on their yes go on, and name the file in
  the commit message, since a parallel task may touch it too.
- Never edit `spec.md`, `passation.md`, `maquette/`, `textes.md`, `cadrer-x.yml`, `{docs}/` or a lock
  file; in `taches.md`, only your task's own `[ ]` → `[x]` (its line and its boxes). No new dependency
  unless `decisions.md` names it, or the constitution allows it.
- Something worth fixing outside your files: not touched; say it at the end, one line each.

**Decide, or ask.** What a builder decides alone (a function name a later task will call, how a race
is prevented, a case the spec leaves open with an obvious answer): the smallest reasonable choice,
written as a `Choix :` line of the commit message. What changes what a person sees and no file
settles, or a task where every path is a guess: one question to the person, with your
recommendation, then go on with their answer. Stop and ask before anything destructive (deleting
data, rewriting history), anything touching security (a secret, a permission, a check turned off),
and anything outside this worktree (a push, a real outside service).

## A task with screens

Its section of `passation.md`, its page in `maquette/` and `textes.md` are the whole design: build
from them, never from how such screens usually look.

- **Read the page as text**: each `data-state` section is a state; the state bar and `maquette.js`
  are the prototype's own, never product code.
- **The project's own components and tokens** (read `cadrer-x-design-system`),
  by the app's names; never the prototype's classes or a copy of its stylesheet. A Nouveauté of
  `passation.md` is built from tokens in the task's module.
- **The words as `textes.md` has them**, each form of a varying text. A text it lacks (a server
  error, a limit): ask the person, with your proposal written by `cadrer-x-textes`'s rules when it is
  installed.
- **Each state is a code path, each box a test** in the project's own runner: render the state, find
  its text, its label, its link, its alert.
- With `commands.dev` in `cadrer-x.yml` and a browser tool: start the app from this worktree on a free
  port, open the task's screens at 390 and 1280 wide, see each state render, then stop it. Otherwise
  say the screens were not opened; `/cadrer-x-examiner` clicks them anyway.

## Done means fresh evidence

1. The whole check command of `cadrer-x.yml`, in this worktree, not only your test file. Read the exit
   code.
2. Each box and each risk: the test that proves it, green in this run.
3. A failure you did not cause: never fixed outside your files; named, with one line on why it is
   not yours and the folder it lives in, which you left untouched.
4. Claim only what this run shows, pasted and trimmed ("Ran 14 tests … OK"), never "should pass".
5. Tick your task `[x]` (its line and its boxes) in `taches.md`, and commit everything on the task
   branch: `T<nn> — <titre>`, with the `Choix :` lines and any file outside `Fichiers :` in the body.

Then, in one message: each box and each risk with the test that proves it, and for each the red run you
saw before its code (the failing assertion line, trimmed: the person never saw your terminal), the
last whole-suite run, the choices, what you noticed, and one question: merge into `feature/<slug>` now?

## Merge — only after the yes

1. In the task's worktree, bring in what other tasks merged meanwhile: `git merge feature/<slug>`. A
   conflict in your own files: resolve it, keeping both tasks' behaviour. A conflict in a file of
   another task: stop, and tell the person which file and which task. Then the whole check command
   again; green, or stop.
2. Where `feature/<slug>` is checked out (`git worktree list`: its worktree, or the main checkout):
   `git merge --ff-only tache/<slug>-t<nn>`. It refuses: back to step 1.
3. `git worktree remove .worktrees/tache.<slug>-t<nn>` and `git branch -d tache/<slug>-t<nn>`. Never
   push.
4. The next step and nothing more: the tasks this one unblocks that can start now (each
   `/cadrer-x-realiser T<nn>`, in its own session), and when every task of the story is `[x]`,
   `/cadrer-x-examiner US<n>` in a new session.

## A fix round

`/cadrer-x-realiser US<n>`: the story's section of `{feature}/audit.md`, its findings marked
`Bloquant :` and `À corriger :` (`Détail :` only when the person asks). Branch `tache/<slug>-us<n>-correctifs`,
worktree `.worktrees/tache.<slug>-us<n>-correctifs`, from the feature. Each finding starts with a red
test that reproduces it, then the fix. A missing or partial behaviour the review found becomes a new
task appended to the story's section of `taches.md` (`- [x] T<next> [US<n>] <verbe> <titre>`, its boxes,
its lines), built and ticked here: the one change to the plan a fix round makes. Never rewrite an old
task. The commit: `correctifs US<n>`, each finding it closes named. Then the same merge, and
`/cadrer-x-examiner US<n>` again, in a new session.

## Red flags

| Thought | Instead |
|---|---|
| "I'll write the code, then the tests." | A failing test first, watched failing on its assertion. |
| "The test passes if I loosen this assertion." | The code is wrong: fix the code. |
| "This failing test isn't mine; I'll fix it quickly." | Not your file: name it, leave it. |
| "One more file and it's cleaner." | `Fichiers :` only; another session may be in it. Ask. |
| "T02 isn't merged yet, but I know what it'll do." | Wait: build on what is merged. |
| "Tests pass, so it's done." | The whole check command, fresh, in this run. |
| "Green — I'll merge into the feature." | Ask first; merge on their yes, never push. |
| "I built it, I'll review the story too." | `/cadrer-x-examiner US<n>`, in another session. |
