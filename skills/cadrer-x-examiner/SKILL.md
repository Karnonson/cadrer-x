---
name: cadrer-x-examiner
description: "Relire un récit (`US1`) une fois toutes ses tâches construites, dans une autre session que celles qui l'ont construit. Vérifie que le code fait ce que dit chaque scénario de la spec, que ses tests échoueraient si le comportement cassait, et qu'il respecte la constitution, la sécurité et les frontières des modules ; clique les écrans quand il y en a. Écrit la section du récit dans `audit.md`. Ne corrige rien."
disable-model-invocation: true
argument-hint: "<US1> [fonctionnalité]"
---

# cadrer-x examiner — one story, reviewed by someone who did not build it

Every task of the story passed its own tests: its builder wrote them, from the builder's reading of
the spec, so a misreading passes them. You ask what those tests cannot: is this the story the person
approved, and would its tests fail if the behaviour broke? You are read-only on the code: you never
edit, fix or refactor anything. The one file you write is `{feature}/audit.md`, the story's section,
from `templates/audit.md`; `/cadrer-x-realiser US<n>` fixes what you found, in another session.

Talk, and write the audit's text, in the person's language, every message included (the short notes
between steps too); in French, *tu* or *vous* as they write, *vous* when you can't tell, never both.
Headings, labels, prefixes and ids stay exactly as written here and in the template: realiser and
rendre find them by these names.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which story, and where

Read first: `cadrer-x.yml` (`docs:`, `commands`), `git worktree list`, `git branch --list 'feature/*' 'tache/*'`.

- **The feature.** The second argument, else the feature of the worktree you are in, else the one
  whose `taches.md` has the story's tasks all ticked; several: ask which, one question.
- **Where you work.** Its worktree `.worktrees/feature.<slug>`; else the current checkout when it is on
  `feature/<slug>`; else `git worktree add .worktrees/feature.<slug> feature/<slug>` (`.worktrees/` in
  `.git/info/exclude` first, the untracked `.env*` files copied in, `commands.install` run once).
  Uncommitted changes there: not yours to judge or to keep; say so, and stop.
- **The story is ready** when every task `[US<n>]` of `taches.md` is `[x]` on the feature branch, and
  so is every task they are `Après :` that has no story of its own (Fondations): those you review with
  the first story that stands on them. A task not ticked, or a `tache/<slug>-t<nn>` branch of the story
  not merged: say which, and stop.
- **A second look.** The story already has a section in `audit.md` with `Bloquant :` or `À corriger :`
  findings, and a `correctifs US<n>` commit came after it: a re-review (section "Tour 2 and later").

## Read, in this order

The order is part of the job: you form your own view before reading anyone's account of the work.

1. `{feature}/spec.md`: the story, each scenario, the `EF<n>` it carries, the **Cas limites**. The
   scenarios are the truth.
2. `{feature}/taches.md`: the story's tasks, their boxes, `Risques :`, `Fichiers :`, the **À
   surveiller** lines pinned to them, the story's rows of **Couverts**.
3. `{feature}/decisions.md`, `{feature}/a-trancher.md` (an answered question is settled),
   `{docs}/constitution.md` (each `M<n>`), `{docs}/architecture.md` → **Modules** and **Mots**. Read `cadrer-x-securite` and `cadrer-x-modules`.
4. With screens: `{feature}/passation.md` (each `SC<n>` whose `Récits :` names the story), its pages in
   `maquette/`, `{feature}/textes.md`. Read `cadrer-x-design-system` and `cadrer-x-textes`.
5. The code and the tests: each file on the story's tasks' `Fichiers :`, as the feature branch has it
   now, and whatever they call. How it got there: `git log --oneline <main>..feature/<slug>`, then
   `git log -p` of the story's commits (`T<nn> — …`): a test strict in one commit and loosened in a
   later one is how a bar gets lowered. `git diff <main>...feature/<slug>` for anything the story
   touched outside its tasks' files.
6. Run the whole check command of `cadrer-x.yml` once, fresh, in the feature's worktree; read the exit
   code. A failure in a test no task of this story owns: one `Info :` line, never a finding against it.

Write your findings from these alone. **Only then** read what the builders said: the commits'
`Choix :` lines and messages, and the previous tour of `audit.md`. A builder's claim is checked
against what you found; the code and a command's output are evidence, a message is not.

## The Spec axis (`### Spec`)

For each scenario of the story, find the code that makes it true and the test that proves it. Every
gap is typed:

- **manquant**: nothing does it;
- **partiel**: part of it does (the ordinary case without the refusal, one state of two);
- **contraire**: the code does otherwise than the scenario says;
- **non demandé**: the story's code does something no scenario, `EF<n>` or decision asks for.

Then the other way round: list each public function, route, page and table the story's files add, and
match each to the scenario, `EF<n>` or decision that asks for it. One that matches none is `non demandé`
(`À corriger :`, removed or asked about), whatever else is wrong with it too.

**Would the test fail?** A test that passes whatever the code does proves nothing. For each box, read
its test: does it assert the spec's own value, at the boundary the scenario names (the last seat, the
exact hour, the empty list), through the module's entry? For the scenarios that matter most (an
`EF<n>` that says NE DOIT JAMAIS, each **À surveiller** line), prove it: in a throwaway detached worktree
outside the repo (`git worktree add --detach <scratch>/examiner-us<n> feature/<slug>`), break the one
line that makes it true, run that test alone, and see whether it fails; then
`git worktree remove --force` it. A test still green on broken code is `À corriger :` (`Bloquant :` when
the behaviour it should guard is also wrong). Never break anything in the feature's own worktree.

A spec's silence is not permission: what a reasonable person would expect from the story and the
code breaks is a finding, the **À surveiller** lines first. A story manquant or partiel is
`Bloquant :`; the fix round adds the missing work as a new task.

## The Rules axis (`### Règles`)

Each finding quotes the line it is about.

- **A secret's value** in the code, the history or an output: the first finding, `Bloquant :`, with its
  name, file:line and commit (`git log -S`), never the value: it must be revoked where it was issued,
  and no branch holding it is pushed until the history is cleaned.
- **Safe defaults**: an input used unchecked, a query built from text, a missing sign-in, a record read
  or changed without checking it is the person's own, a role checked only in the page, an error that
  shows too much, personal data in a log.
- **Each risk** of the tasks' `Risques :` lines: its test exists, asserts the refusal **and** that
  nothing changed. No test, or one that would pass without the guard: `À corriger :` (`Bloquant :`
  when the guard itself is missing).
- **The constitution**: each `M<n>` the story touches. A rule broken is `Bloquant :`.
- **Module borders**: a module reading another's tables, going past its entry, a call the map does not
  list: quote the import or the query, the **Modules** line it breaks, and the other module's entry
  function to call instead (`billing.api.get_invoice`), read from its entry file. A module the map lacks,
  with no **Impact archi** line in `decisions.md`.
- **A lowered bar**: a threshold moved, an assertion loosened, a test skipped or wrapped in a `try`, a
  checker silenced, a stub or a TODO left, a dependency the constitution or `decisions.md` does not
  allow.
- **The words**: a name for a thing the **Mots** list names otherwise (« réservation » for « inscription »).
- **Whose job it is.** `{docs}/architecture.md`, `{docs}/adr/`, `{docs}/security/` and `CHANGELOG.md` are
  `/cadrer-x-rendre`'s, when the feature ships: their state is at most an `Info :`, and a task that
  edited them is `À corriger :` (another session may be editing them too). A need no story asks for (a
  purge job, a new page) is an `Info :` and a question for the person, never a fix you demand.

## Screens

When `passation.md` gives the story a screen. You may start the app here, and only here: with
`commands.dev` in `cadrer-x.yml` and a browser tool, run it from the feature's worktree on a free port
(no other session's), wait until it answers, and stop it when you are done. Never install, never edit
a file or an environment variable to get in, never create an account in an outside service. Behind a
sign-in: a way in the project documents (a test member in its README), else the screen goes under
`### Non jugé`.

For each screen, at 390 then 1280 wide:

1. Reach each state its `États :` line names the way a person would (type, send, open, come back). A
   state you cannot cause from the page goes under `### Non jugé`, with why.
2. Do each scenario of the story on the screen: it works, or it is a Spec finding.
3. The texts against `textes.md`, word for word; each field's label; the order Tab follows; nothing
   scrolling sideways at 390 (`document.documentElement.scrollWidth <= innerWidth`); no console error.
4. Save one screenshot per screen and width of its main state, `{feature}/captures/SC<n>-<largeur>.png`
   (`-<état>` added for a state worth showing apart).

Findings: a state the app lacks is partiel (`Bloquant :`); a text that is not `textes.md`'s word for
word is `À corriger :`; a raw colour or size where a token holds it, or a part that is neither the
design system's nor a **Nouveauté** of `passation.md`, is `À corriger :`; a field with no label, a focus
that jumps, a tap target under the design system's size, sideways scrolling at 390 is `À corriger :`;
spacing that changes nothing a person can do is `Détail :`. From the code, always, and all there is
when the screens could not be clicked: each `textes.md` text found in the code (`grep -rn`), each state
its code path, the project's own components used.

## One prefix per finding

| Prefix | When | Blocks |
|---|---|---|
| `Bloquant :` | wrong behaviour, a scenario manquant or partiel, someone else's data reachable, a secret, a rule of the constitution broken, a lowered bar hiding a wrong behaviour | yes |
| `À corriger :` | to fix before it ships: a test that would not fail, a risk untested, a border crossed, a text not `textes.md`'s | yes |
| `Détail :` | may ship as it is | no |
| `Info :` | what you checked and found right, what is someone else's, a question for the person | no |
| `Corrigé :` | a tour 2 finding the fix round closed | no |

Each finding: `- <Préfixe> : <file:line> — <manquant|partiel|contraire|non demandé, on the Spec axis> :
<what is wrong> ; <what a person meets because of it> ; correction : <the fix>`. Prefix each finding for
what it is: never soften one to let the story pass, never harden a detail.

## Write the audit

`{feature}/audit.md` from `templates/audit.md`, created when absent. The story's section goes on top,
under the title: `## US<n> <titre>`, then `**Tour** :`, `**Date** :`, `**Verdict** :` (`à corriger` when
any `Bloquant :` or `À corriger :` is left, else `validé`), then `### Spec`, `### Règles`, `### Non jugé`
(and `### Correctifs` from tour 2). A clean axis is `- aucun`. `### Non jugé` opens with `Vérifs :`
(`lancées — <the command, its exit code, the summary line>` or `pas lancées — <pourquoi>`) and, with
screens, `Écrans :` (`cliqués SC1 SC2` at both widths, `pas cliqués — <pourquoi>`, or `cliqués SC1 ; pas
cliqués SC2 — <pourquoi>`); never more than you did. Then what you could not check (a real outside
service, a load), each with why. A previous tour's section of the same story is replaced, its
findings carried into `Corrigé :` or repeated.

Run `python3 <this skill's folder>/scripts/lint.py audit {feature}/audit.md`; fix and rerun until it
prints nothing. Commit on the feature branch, `audit.md` (and `captures/`) only: `audit US<n> — <verdict>`.
Never push.

## Tell the person

One message: the verdict; per axis, how many `Bloquant :` and how many `À corriger :`, counted in the
audit.md you just committed and named by those words; each of them in one line (what a person meets,
the file); what you could not judge, and the questions only they can answer. Then
the next step and nothing more:

- `à corriger`: `/cadrer-x-realiser US<n>`, in a new session; then `/cadrer-x-examiner US<n>` again.
- `validé`: the next story whose tasks are all built (`/cadrer-x-examiner US<m>`), or when every story
  of `taches.md` has a `validé` section, `/cadrer-x-rendre`.

## Tour 2 and later

The fix round's commit (`correctifs US<n>`) answers the last tour's blocking findings. Check that, not
the whole story again: a review that starts over every tour finds something new each time and never ends.

1. The last tour's `Bloquant :` and `À corriger :` findings, then the fix round's diff
   (`git diff <the last audit commit>..feature/<slug>`).
2. Each of them gets one line, on its axis: `- Corrigé : <the finding, in a few words> — <file:line
   where the fix is, the test that proves it>`, or the finding again, prefixed, with what is still
   wrong. Fixed where it was reported but left in another place of the same kind (the same query, the
   same missing check) is not fixed.
3. `### Correctifs`: the fix round's own lines. Wrong behaviour in them, or a test weakened to get
   through, is a finding like any other.
4. Anything else you come across is late: `Bloquant :` only with the concrete harm a person would meet
   (wrong or lost data, someone else's data, a secret, money, a rule of the constitution); anything
   less is `Info : tard — <file:line, what, the fix>`, and it passes.

## Red flags

| Thought | Instead |
|---|---|
| "The tests are green, so the story works." | Read each test against its scenario; break the line, see it fail. |
| "I'll fix this one-line bug while I'm here." | Read-only. A finding, with its fix; realiser does it. |
| "The commit says the race is handled." | A claim. Find the code and the test that prove it. |
| "Small thing, I'll mark it Détail so the story passes." | Prefix it for what it is. |
| "The spec doesn't say what happens at the last seat." | What a reasonable person expects, and the code breaks, is a finding. |
| "The architecture doc wasn't updated: Bloquant." | `rendre`'s, at ship time: `Info :`. |
| "Tour 2: let me review the whole story again." | Check the fix round; anything else is late. |
| "The app needs a test user; I'll add one to the database." | `### Non jugé`, unless the project documents a way in. |
| "Validé — I'll start the next story's review too." | One story per session; name the next step. |
