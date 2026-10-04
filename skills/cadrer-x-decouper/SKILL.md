---
name: cadrer-x-decouper
description: "Découper une fonctionnalité en tâches. À lancer quand sa spec est validée (et sa maquette, si elle a des écrans) mais qu'elle n'a pas encore son `taches.md`, ou quand la spec a changé et que les tâches sont à refaire. Écrit `taches.md` : des tranches fines qui traversent tout ce dont elles ont besoin, chacune prouvée par un test, rangées par récit, avec ce qui peut se construire en même temps. Ne code pas."
disable-model-invocation: true
argument-hint: "<numéro ou nom de la fonctionnalité>"
---

# cadrer-x découper — the tasks

You cut the approved spec into tasks the builders take one at a time, often several at once, each
in its own worktree, never seeing each other. One file, `taches.md`, from `templates/taches.md`. Each
task's block is that builder's whole brief: its boxes are its done-when, its `Fichiers :` the only
files it may touch. The reviewer reads **À surveiller**; `/cadrer-x-examiner` reviews a story once all
its tasks are built. No code.

Talk, and write the file's text, in the person's language, every message included (the short notes between steps too); in French, *tu* or *vous* as they write,
*vous* when you can't tell, and never both. File names, headings, labels and ids stay exactly as
written here and in the template, in every language: the later skills find them by these names.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which feature, and where

Read first: `cadrer-x.yml` (`docs:`, default `docs`; `commands.checks`), `git worktree list`,
`git branch --list 'feature/*'`.

- **The feature.** The argument's number or slug; a near miss (`devis` for `defis`, `001-defis`) with
  one close feature: that one, said in one line. No argument: the feature of the worktree you are
  in, else the one feature with a validated spec and no `taches.md`; several: ask which, one question.
- **Where you work.** Its worktree `.worktrees/feature.<slug>`; else the current checkout when it is on
  `feature/<slug>`; else `git worktree add .worktrees/feature.<slug> feature/<slug>` (`.worktrees/` in
  `.git/info/exclude` first, the untracked `.env*` files copied in). `{feature}` is
  `{docs}/features/NNNN-<slug>/` there.
- No `spec.md`, or its **Statut** is not `validée`: say `/cadrer-x-affiner <slug>` comes first, and stop.
- `écrans : oui` in `decisions.md` and no `passation.md`: the same, for the prototype.
- An old cadrer `tranches.md` there and no `taches.md`: the build started under cadrer. Its ticked slices
  are built: read their code, and write each scenario it already proves as a ticked `[x]` task under its
  story (its files those that hold it, `Risques :` as the code guards them); cut only what is left.
- `taches.md` already there: a revision. A `{feature}/verification.md` newer than the tasks: its
  findings for `/cadrer-x-decouper` are what changes, never asked again; else ask what changed (usually
  the spec). Keep every task already ticked `[x]` as it is, with its id, and cut what changed as new
  tasks numbered after the last one.

## Read, in this order

1. `{feature}/spec.md`: the stories, their scenarios, the exigences `EF<n>`. The person approved it:
   never edit it; a story you think is wrong is a question to them.
2. `{feature}/a-trancher.md`: an answered question is settled; plan on it.
3. `{feature}/decisions.md`: **Décisions**, **Impact archi**, **Données et risques**, **Stack**. What
   it settles stays settled: never asked again, never undone by an option you recommend.
4. `{docs}/constitution.md`: the numbered rules `M<n>`.
5. `{docs}/architecture.md` → **Modules**: each module, what it owns, its paths. Read `cadrer-x-modules`. Then open the code it points to, so every path you name
   is real, or sits where the map puts that module's new files (a new module: where
   `../cadrer-x-modules/references/structure.md` puts it). Code not yet laid out that way (**À
   faire** names `/cadrer-x-ranger`): the feature's new code still goes where the layout puts it and
   calls the old code where it is. Moving old code is `/cadrer-x-ranger`'s, never a task's: say so in
   one line.
6. `{feature}/passation.md`, with screens: each `SC<n>`, its stories, its page, its states.
7. The tests the project already has, and how `cadrer-x.yml` runs them.

Facts are looked up, never asked: what the repo, the code or the docs answer is yours.

## Cut

- **Tracer bullets.** Each task is a thin path through every layer it needs (what is kept, the rule,
  what a person sees) that a test proves. Never a layer alone ("la table", "les routes"): a layer
  proves nothing on its own, and its builder guesses what the next one needs.
- **By story.** Each task serves one story and carries its `[US<n>]`, under that story's `##` section,
  most useful story first, so each story works on its own once its tasks are in. **Fondations** holds
  only what the first story needs underneath and several tasks share (a migration, a module's folder,
  test tooling); `aucune` when nothing is.
- **Every scenario of the spec is a box of exactly one task**, worded as the check its test proves. A
  box no scenario asks for is out of scope; an `EF<n>` with no scenario still gets the task that makes
  it true on its `Exigences :` line.
- **Sized by files.** XS 1 file, S 1–2, M 3–5. More, or an « et » in the title: two tasks. A wide
  rename goes expand, migrate, contract: the new beside the old, the callers moved in batches, the old
  removed; every task leaves the checks green.
- **A screen is still a tracer bullet**: the page with its real data and every state its `passation.md`
  section names, not the markup alone. Too big for one task: cut by state or by story, each naming it
  on `Écrans :`. Every screen is named by at least one task.
- **`Après :`** names only what a task really stands on: the earlier tasks whose code it cannot be
  built or tested without. Never "the one before" by habit: every needless link is a session that
  waits. `aucune` when nothing.
- **`[P]`** marks a task that can be built at the same time as the one before it: its `Après :` does
  not name it, and they share no file. Parallelism comes from separate stories, and from separate
  states of one story once its first task is in.
- **A file several tasks change** (`package.json`, the lockfile, a test setup, a route index, a shared
  type) is on the `Fichiers :` line of each, and has one owner: the first task that names it. Every
  other task naming it is `Après :` that owner, directly or through another task.
- **Never in a task's files**: `spec.md`, `taches.md`, `passation.md`, `maquette/`, `contenu.md`
  (affiner's and yours), and `{docs}/architecture.md`, `{docs}/adr/`, `{docs}/security/`, `CHANGELOG.md`
  (`/cadrer-x-rendre` folds the feature in when it ships).
- **Tests in the runner the project has.** A builder never adds a test runner or a package on its own.
  A box about how a screen looks at a width stays a box: the test proves its text, its link, its state,
  and the review clicks the rest at 390 and 1280.
- **Every rule that asks this feature for a test or a tool has a task that owns it.** Read each `M<n>`
  against the feature. Tooling the project lacks is a task of its own in **Fondations** (its config,
  `package.json`, the lockfile on its `Fichiers :`), and the tasks that need it are `Après :` it. The
  setup the first tests need to run cleanly (`"type": "module"` in `package.json`, the runner's config)
  is on the first task's `Fichiers :`. A rule
  the approved spec or the project's tools force you to break: a question to the person (it needs an
  ADR), and `- Règles en conflit : M<n> — T<nn> — <pourquoi>` meanwhile.

## Each task's risks

One `Risques :` line per task: `<domaine> — <menace> → <protection>`, `;` between them. Threats only:
someone, or a bot, doing what they shouldn't. Each becomes one abuse test. Read `cadrer-x-securite`. Walk each task through:

| Domaine | Ask | Usual protection |
|---|---|---|
| connexion | Reachable without signing in, or by the wrong role? | sign-in required; role checked on the server |
| données d'un autre | Can changing an id or a link reach another person's record? | owner check; unguessable, expiring link |
| saisies | What comes from outside (form, address, file, webhook, AI output)? Too long, wrong type, markup, a price? | checked at the edge; the server sets amounts |
| secrets | Which keys, where, can the browser see one? | environment, by name; server only |
| paiements | Fake, replay, pay less, refund twice? | provider signature checked; idempotent; amount from the server |
| données personnelles | Can someone who shouldn't (another person, a log, a third party) see a person's data? | only who needs it; nothing extra in logs |
| abus | Can one person or a bot do it a thousand times, or hold everything? | a count or a rate limit; holds that expire |

A domain that does not apply is skipped; one that does gets a protection the stack really offers
(look it up). None: `aucun — <pourquoi>`. A bug (a time zone, an order) is a box, not a risk; how long
data is kept is `decisions.md`'s, not a risk. Never a secret's value.

## After the tasks

From the template, in this order:

- **Ordre**: the template's four lines, then the waves: `- Vague 1 : T01`, `- Vague 2 : T02, T05`…,
  each wave the tasks whose `Après :` the earlier waves cover. That is what can be built at once.
- **À surveiller**: up to five cases the spec implies and no box tests (the same moment, a boundary, a
  hostile value, an empty list), each pinned to the task that owns the code, the one most likely to
  hurt a person first. `- aucun` only after you looked.
- **Couverts**, your last step, the plan's own check: a row per story, per `EF<n>`, and per `M<n>` this
  feature needs a test or a tool for, each naming the tasks that cover it; every task in some row;
  every scenario a box in exactly one task; every screen on an `Écrans :` line; every shared file with
  one owner. A task that would break a rule changes now. Then `- Règles en conflit :`.

## Questions

Rare: the spec and the decisions settled the *what*. Ask only what changes the plan and that no file
answers (a rule in conflict, a tool the project lacks and that costs something, a story you think is
wrong), one per message, with your recommendation a plain "oui" accepts. One left for later goes to
`{feature}/a-trancher.md` as `## Q<n> · plan · <question>`, with `- Options :`, `- Effets :`,
`- Conseil :`, `- Réponse :`. What you decide alone a builder would also have to decide: write it on the
task's lines, never in an essay.

**What the person chooses here is written down.** A layout, a scope, a tool they settle while you cut
(« le code dans src/, un module par fonctionnalité ») becomes the next `D<n>` of `decisions.md` →
**Décisions**, with **Impact archi** when it moves the map, committed with `taches.md`. A choice left in
the chat is lost to every later step: the check flags its tasks, and the next cut undoes it.

## Show it, then save

Write `{feature}/taches.md`, comments removed, then run `python3 <this skill's folder>/scripts/lint.py
taches {feature}/taches.md`; fix and rerun until it prints nothing. Commit it (and `decisions.md`,
`a-trancher.md` when you wrote to them) on the feature branch: `tâches — <Titre>`. The branch is the
draft: nothing is built from it before the person's yes.

**A second look, fresh.** When `cadrer-x-verifier` is installed beside this skill and you can start a
subagent, start one with a fresh context and this prompt, and nothing of yours: « Read
`<skills folder>/cadrer-x-verifier/SKILL.md` whole and follow it for the feature `<NNNN-slug>`, in
`<the feature's worktree>`. Launched by decouper. » Do not use the Skill tool for it: read the file.
Meanwhile, wait. Its findings, from `verification.md`:

- For `/cadrer-x-decouper`: yours; fold each in.
- For `/cadrer-x-affiner`, with one fix the files already settle (a word the prototype or the glossary
  uses, a value a decision or an answered question gives): fix `spec.md` there, its lint run again,
  and name each change in your message.
- Anything that needs a choice: a question in your message, with your recommendation.

No subagent: say in one line that `/cadrer-x-verifier`, in a fresh session, can check the spec and the
tasks first.

**Show it.** One message: one line per task (id, `[P]`, story, title, size, `Après :`), the waves, the
**À surveiller** lines, what the second look found and what you changed for it, and the questions.
Ask what they would change; each change is folded in, the lint run again, until a clear yes ("oui",
"ok", "ça va", "c'est bon"; a hedge or a change asked for keeps it open).

On the yes: commit what changed since (`tâches — <Titre>`; `spec — <Titre> : corrections de la
vérification` for the spec). Then the build: `/cadrer-x-realiser <slug>` builds every task, has each
story reviewed by someone who did not build it, and stops only for the person's questions. Say it runs
best in a fresh session (`/clear`, then the command); they say go on here: open
`../cadrer-x-realiser/SKILL.md`, read it whole and follow it for this feature.

## Red flags

| Thought | Instead |
|---|---|
| "T01 the table, T02 the routes, T03 the page." | Each task cuts through every layer it needs. |
| "T03 comes after T02, to be safe." | `Après :` only what it stands on: each needless link is a session that waits. |
| "The builder will add a test runner." | Tooling is a Fondations task; the others are `Après :` it. |
| "A purge job would be tidy." | No scenario asks: out of scope. |
| "I'll update the data inventory in T02." | `docs/security/` is rendre's. |
| "Two tasks both edit the route index; fine." | One owner; the other is `Après :` it. |
| "Risk: the time zone." | A bug: a box. Risks are someone misusing it. |
| "This story is wrong; I'll fix the spec." | Never edit the spec: ask the person. Only the second look's one-answer drifts are fixed there. |
| "They said: modules in src/. Noted in my head." | A `D<n>` in `decisions.md`, committed with the tasks. |
| "The check says T01–T08 nobody asked for; I'll recommend dropping them." | A decision asked for them: the check missed it. Settled stays settled. |
| "While we're here, T02 moves the old code into modules." | Moving old code is `/cadrer-x-ranger`'s. |
