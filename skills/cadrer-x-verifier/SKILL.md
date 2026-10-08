---
name: cadrer-x-verifier
description: "Vérifier une fonctionnalité avant d'écrire le code, dans une session neuve. Facultatif : après la spec seule, ou après les tâches (la spec et les tâches). Cherche ce que les lints ne voient pas : un scénario qu'on ne peut pas vérifier sans code, une décision restée en route, une contradiction avec la constitution, une case qui ne dit plus ce que dit son scénario, un risque sans tâche. Écrit `verification.md`. Ne corrige rien : chaque constat nomme l'étape qui le corrige."
disable-model-invocation: true
argument-hint: "[numéro ou nom de la fonctionnalité]"
---

# cadrer-x vérifier — a second look before any code

`choisir` checked the spec and the tasks as it wrote them, against its own reading. You read the
feature cold, as the builders will, and look for what would make them build the wrong thing: a scenario
nobody can check, a decision lost on the way, a rule broken on paper, a box that drifted from its
scenario. You fix nothing and edit no file but `{feature}/verification.md`, from
`templates/verification.md`. Each finding names the stage that fixes it: `→ spec` for the spec,
`→ tâches` for the tasks.

Talk, and write the file's text, in the person's language, each note between tool calls too; in
French, *tu* or *vous* as they write, *vous* when you can't tell, never both. File names, headings,
labels and ids stay exactly as written here and in the template, in every language: `choisir` reads
them by these names.

**Retour.** In the main session (never as a subagent), before the message that ends this run (the
stop, the next command given, or the person stopping): open `../cadrer-x-retour/SKILL.md`, beside
this skill's folder, → *When*, and follow it. Not there: go on without it.

## Which feature, and how far

Read first: `cadrer-x.yml` (`docs:`), `git worktree list`, `git branch --list 'feature/*'`.

- **The feature.** The argument's number or slug (a near miss with one close feature: that one, said in
  one line), else the feature of the worktree you are in, else the one feature with a validated spec and
  no task built yet; several: ask which, one question.
- **Launched by choisir** (its prompt says so): the same work, the same file and commit; ask no
  one. Your last message is for choisir: the verdict, then each finding whole, as `verification.md`
  has it. No next step.
- **Where.** Its worktree `.worktrees/feature.<slug>`, else the checkout on `feature/<slug>`, else `git
  worktree add .worktrees/feature.<slug> feature/<slug>` (`.worktrees/` in `.git/info/exclude` first).
- **How far.** No `spec.md`, or not `validée`: say `/cadrer-x-choisir <slug>` comes first, and stop. A `taches.md`:
  **spec et tâches**; none: **spec**. A task already `[x]`: say the build has started, that you check
  what is not built yet, and that the review (`/cadrer-x-realiser`) judges the rest.

## Read

`{feature}/brief.md`, `decisions.md` (each `D<n>`, each **Précisions** answer, **Données et risques**,
**Impact archi**), `spec.md`, `a-trancher.md`, `passation.md` and `contenu.md` when there are screens,
`taches.md` when there is one; `{docs}/constitution.md`, `{docs}/architecture.md` (**Modules**), `{docs}/glossaire.md`.
Then run the form checks the earlier steps left, when their skills are installed beside this one:
`python3 <skills folder>/cadrer-x-choisir/scripts/lint.py spec {feature}/spec.md` (and `passation`,
`taches` for `{feature}/taches.md`). A line they
print is a finding as it stands; you look for what they cannot see.

## The spec

- **Checkable without code.** Each scenario: someone who doesn't code can do it and see the result.
  Its **Étant donné** sets a state, its **quand** is one action, its **alors** something seen, with the
  values that make it pass or fail. A word with no measure (« rapidement », « facilement », « clair »,
  « bien ») is not checkable: say what number or what sight would settle it.
- **Every decision lands.** Each `D<n>` and each **Précisions** answer of `decisions.md`, and each
  answered question of `a-trancher.md`: in a story, an `EF<n>`, **Supposé**, or **Pas encore**. Lost, or
  turned into something else, is a finding.
- **No contradiction**: between the spec and `decisions.md`; between the spec and each `M<n>` of the
  constitution (a rule's words read as they are: « leurs ateliers » is not « tous les ateliers »);
  between two stories.
- **The person's words**: each thing named as `{docs}/glossaire.md` names it; a synonym is a finding (two words make
  two things in a builder's head).
- **What a reasonable person expects and no scenario says**: the boundary (the last seat, the exact hour,
  the empty list), the second person at the same moment, the person who should not see it. One line
  each, only where a builder would have to guess.
- **Personal data**: for each piece kept or shown, who sees it and who changes it is said.
- **Each story stands alone**: its **Test seul** can be done with only its own work and the stories
  before it.

## The tasks (spec et tâches)

- **Each scenario is one box, saying the same thing**: the same values, the same refusal, the same
  person. A box that changed a number or dropped a condition is a finding, quoting both lines. A box no
  scenario asks for is out of scope.
- **Each story has its tasks**; each task serves a story, or is `Après :` one (Fondations).
- **Each threat** of **Données et risques** and of the constitution's rules sits on a task's `Risques :`
  line with a protection. `aucun — <pourquoi>` on a task that handles another person's record, a role,
  or a form is a finding.
- **Couverts says true**: each row's tasks do cover it, read from their boxes, not from the row.
- **Files where the map puts them**: each path on `Fichiers :` is in its module's paths of **Modules**,
  or new in a module **Impact archi** or a `D<n>` of `decisions.md` announced; never a file the tasks
  may not touch.
- **Settled stays settled.** What a `D<n>`, a **Précisions** answer or an answered question of
  `a-trancher.md` asks for is never « non demandé »: a task that carries it out is asked for.
- **`Après :` real**: a task that needs another's code names it; a task that names one it does not need
  makes a session wait (a **Remarque**).

## Findings

Two kinds:

- `À reprendre :` a builder would build the wrong thing, or could not know when they are done: a
  scenario not checkable, a decision lost, a contradiction, a box that drifted, a threat with no task.
- `Remarque :` worth a look, and the build can start without it.

Each finding: `- <Préfixe> : <file:line> — <what is wrong, quoting the line> ; <what a builder or a person
would meet> ; → spec` (or `→ tâches`). Prefix: `À reprendre :` or `Remarque :`.

## Write it, then say it

`{feature}/verification.md` from the template: the title, `**Date** :`, `**Portée** :` (`spec` or `spec et
tâches`), `**Verdict** :` (`à reprendre` with any `À reprendre :` left, else `prête`), then `## Constats`
(`- aucun` when clean) and `## Vérifié` (each check you made and found holding, one line each: what a
second look covered). A new run replaces the file. Run `python3 <this skill's folder>/scripts/lint.py
verification {feature}/verification.md` until it prints nothing. Commit it alone on the feature branch: `vérification
— <Titre>`. Never push.

In your message: the verdict, each `À reprendre` in one line with the step that fixes it, the count of
remarks. Then the next step and nothing more (but *Retour*'s question):

- `à reprendre`: `/cadrer-x-choisir <slug>`, which folds them in and checks once more.
- `prête`: `/cadrer-x-choisir <slug>` after a spec-only check; `/cadrer-x-realiser <slug>` after spec et tâches.

## Red flags

| Thought | Instead |
|---|---|
| "The lints pass, so it's fine." | They check the form; you check what it says. |
| "This box says 48 h; I'll correct it to 24 h." | Fix nothing: a finding, `→ tâches`. |
| "« Rapidement » is clear enough." | No measure, no check: what number settles it? |
| "M3 says « leurs ateliers », close enough to all." | Read the rule as written: a contradiction. |
| "Let me also review the code that's there." | Built work is the review's (`/cadrer-x-realiser`). |
| "No scenario asks for these layout tasks." | Read `decisions.md`: a decision may. |
| "I'll ask the person what they meant." | Write the finding with your proposal; the fixing step asks. |
