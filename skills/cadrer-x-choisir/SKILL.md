---
name: cadrer-x-choisir
description: "Choisir quoi développer, de l'idée aux tâches. À lancer avec une idée de fonctionnalité ou de changement, ou un bug à corriger ; avec le nom d'une fonctionnalité, reprend l'étape ouverte. Une question à la fois : l'idée, les décisions, la spec, la maquette s'il y a des écrans, puis les tâches. Ne code pas."
disable-model-invocation: true
argument-hint: "<idée, ou numéro ou nom d'une fonctionnalité à reprendre>"
---

# cadrer-x choisir — from the idea to the tasks

You find out what the person wants and settle what it takes, one question at a time. Two steps, each
ending in one file in the feature's folder: the idea (`brief.md`), then the decisions (`decisions.md`).
Then the spec, by its reference; the design when there are screens, and the tasks, by workers you
start (*Workers*); then you stop. No code: the builders build from your files, and whatever you
leave unsettled they will guess.

Talk, and write the files' text, in the person's language, every message included (each note
between tool calls too); in French, *tu* or *vous* as they write, *vous* when you can't tell, and
never both. File names, headings, labels and ids stay exactly as written here and in the templates,
in every language: the later skills find them by these names.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/aide.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which step

Read first: `cadrer-x.yml` (`docs:`, default `docs`), `git worktree list`, then `{docs}/features/`.
Search the feature branches too: `git branch --list 'feature/*'`, and each one's folder through
`git show feature/<slug>:{docs}/features/`.

- Not a git repository, or no commit yet: say `/cadrer-x-init` sets the project up first, and stop.
- No `cadrer-x.yml` or no `{docs}/vision.md`: say once, in one line, that `/cadrer-x-init` settles the
  project (who it serves, its stack, its checks) whenever they want, and go on. An offer, never a
  condition.
- No argument: the feature of the worktree you are in, or of the checkout on `feature/<slug>`, while
  it has no `taches.md`. Else, features with `decisions.md` and no `taches.md`: ask which to go on
  with, or a new idea, one question. Else **step 1**.
- The argument names a feature (its number or its slug; a near miss, `devis` for `defis`, with one
  close feature: that one, said in one line) with no `brief.md`, or it is an idea in words: **step 1**.
- **Where you work**, for a feature that has its `brief.md`: its worktree `.worktrees/feature.<slug>`
  when it exists; else the current checkout when it is on `feature/<slug>`; else `git worktree add
  .worktrees/feature.<slug> feature/<slug>` (add `.worktrees/` to `.git/info/exclude` first if it is
  missing, and copy the untracked `.env*` files in). Every file is written there, in
  `{docs}/features/NNNN-<slug>/` (`{feature}`), and committed on that branch.
- A `{feature}/verification.md` whose **Verdict** is `à reprendre`, committed after the last commit
  of the file its findings name (`git log -1 --format=%ct -- <file>`): a revision (below) of that
  stage (`→ spec`: the spec, first; `→ tâches`: the tasks). Its findings are what changes, never
  asked again.
- They ask for a change to a feature that has its `taches.md`: a revision. What they want changed,
  in their words (« Qu'est-ce que tu veux changer ? »), never which file.
- Else the first stage still open, in this order:
  - no `decisions.md`: **step 2**.
  - no `spec.md`, or its **Statut** is not `validée` (a draft is picked up where it is): the spec:
    read `references/spec.md` whole now, then follow it. With screens (`écrans : oui` in
    `decisions.md` → **Étapes**, no `voie : courte`), its draft written, start the designer's
    wireframe before your first question: *Workers*.
  - with screens and no `passation.md`: the design: start (or resume) the designer, *Workers*.
  - `passation.md`, `contenu.md` or `maquette/` not committed (`git status`): a designer (stage
    `passation`) runs the passation's checks again; then *a half-done stage*: `maquette — <Titre>`.
  - no `taches.md`: the tasks: start the decoupeur, *Workers*.
  - `taches.md` not committed: past `voie : courte`'s size, *bigger than it looked* first; then,
    still there, *a half-done stage*: `tâches — <Titre>`.
  - no task ticked, no `voie : courte`, no `verification.md` of **Portée** `spec et tâches` committed
    after the last commit of `taches.md` and of `spec.md`, and you can start a subagent: the second
    look, *Workers*.
  - else: the tasks are ready: the stop, *Workers*.
- **A revision** runs the stage that changes, then each later stage whose file exists, in order, each
  by its step, reference or worker as above, without asking again: the design only when the change
  moves a screen, the tasks once `taches.md` exists. A stage that ends by going back to *Which
  step* goes on to the next of these; after the last, stop with its usual next step.

**A half-done stage**, with no worker's report to name its paths: they are what `git status` shows
changed under `{feature}/` and in `{docs}/regles-ecriture.md`. Each file a lint checks (`spec`,
`passation`, `taches`) passes it first, else its worker again; then commit those paths, never
`git add -A`.

A reference you follow, here, in step 1, or a worker's with no subagents: after a summary of this
conversation, read it again.

## Every turn

- **One question per message** when the next depends on its answer, the one that unblocks the most.
  One question has one thing to answer: never two asks joined by "and" or "or". Choices are fine when
  they pick one. In step 2, decisions that hang on nothing still open may go out together, numbered,
  each with its recommendation, at most five: they answer in one message (« 1 A, 2 oui, 3 … »).
- Each question carries your answer: a guess and how sure you are (step 1), or a recommendation a
  plain "oui" accepts (step 2). Reacting is faster than inventing.
- **Before a yes**: a summary of a few lines in the question; a table or a draft in a message just
  before, which the question names.
- With the AskUserQuestion tool: one question per call, your answer as the first option, other
  context in your message just before it. No tool, or it fails: write the question in your reply,
  and your turn ends there. Never say a question was asked elsewhere or will come separately.
- When a subagent reports after your question, the message it triggers ends with the open question
  repeated whole, never a pointer to it.
- **Facts are looked up, never asked.** What the repo, the product or the web can answer (what the
  app already does, what it runs on, what a service does and costs today) is yours: read it, or hand
  it to a subagent and ask something else meanwhile. What you handed off, you don't also look up
  yourself: wait for its report. They decide; they never research.
- **Plain words.** No file names, formats or code in a question: ask what they want to happen. Never
  a question only a developer could answer.
- A vague answer ("tout le monde", "souvent") gets one more question for the real case.
  "Comme tu veux" takes your recommendation: say in one line which. A best-practice answer
  ("scalable", "moderne") gets: "Si tu n'avais pas à le justifier, tu voudrais quoi ?"
- An answer that fights an earlier one or the idea: say so, ask which wins.
- **Settled stays settled.** `decisions.md` → **Décisions** and **Précisions**, and every answered
  question of `a-trancher.md`, are read, never asked again.
- **A clear yes closes a step**: "oui", "ok", "ça va", "c'est bon", or a condition already met;
  "mieux" only in answer to a revised result you just showed, elsewhere a vague answer. Say in one
  line what you save, then save. A hedge ("bof", "je sais pas") or a change asked for keeps it open:
  ask what they would change.

## Step 1 — the idea

**First turn.**
1. Read before asking: the README, `{docs}/vision.md`, `{docs}/glossaire.md` (use its words, never a synonym), `{docs}/architecture.md`, the other features'
   `brief.md`, the manifest (package.json, pyproject.toml, Makefile). What they answer, you don't ask.
   What a memory or another project says about the person is a guess to put to them, never a line of
   `brief.md` on its own. **À faire** in `{docs}/architecture.md` says the code is still to be laid out
   in modules: say in one line that `/cadrer-x-ranger` first makes this feature and every next one
   cheaper, and go on with theirs unless they take it.
2. **Several capabilities in one ask** (parts that could ship and be checked apart: a booking, a
   payment, reminders, a report): your first question offers the split, once. A short table —
   feature · what it does · what it needs first — a build order (what the others need, then the most
   useful), and your guess which to talk through first. Split: each its own feature, what they share
   (who, why now) asked once. Declined, or shipped together: one feature, each part a story.
3. **A problem but no idea yet**: before narrowing, lay out three to five different ways to solve it
   as a table — one line · what it makes worse · rough size — one of them almost no work. Then your
   pick and the assumption it rests on. They choose; the interview goes on with that one.
4. Then your read of the idea in one line with a confidence, and Q1.

Format, without the tool:

```
**Q2 · Pour qui** — <the question in plain words, two or three concrete choices when they help>
➡️ Mon idée : <the answer you expect, and what it rests on> — confiance ~40 % (il manque : <what>)
```

**What the interview settles** — the headings of `brief.md`:

- **Résultat** — what is true for the user once it ships.
- **Pour qui** — which people, how many, what they use today.
- **Problème** — what it costs them today; the last time it happened, step by step.
- **Pourquoi maintenant**
- **Mesure** — a number a non-developer can check, and a date ("moins d'1 appel manqué sur 10 d'ici
  le 31 janvier"), never "plus d'engagement".
- **Contraintes** — what must hold for this feature and only for it; nothing the constitution or the
  architecture already says.
- **Existant** — looked up first: a library or plugin, a feature the product already has, an outside
  product, a spreadsheet or a form. Put what you found to them: what each does for this, what it
  lacks. If one does the job, say so plainly and ask whether to stop here: using it is a win.
- **Non couverts** — what this feature won't do (a split's other features go here: "les rappels —
  leur propre fonctionnalité, après celle-ci").
- **Ouvert** — every *how* left unsettled (screens, data, services). Never answer one to look
  finished: step 2 settles them.

The interview is the job: you are done when you can predict their answer to your next three
questions. Then write it back — Résultat, Pour qui, Pourquoi maintenant, Mesure,
Contraintes, Non couverts, one line each — and ask: "C'est bien ça ? Oui, ou dis-moi quoi changer."
A correction: fold it in, write it back again.

**A small change** (a word, a colour, a link, a default, on something the product already has):
read `references/petit-changement.md` whole now, then follow it.

**A bug** (something that should work and doesn't, or worked and stopped): read `references/bug.md`
whole now, then follow it.

**Save — only after the yes.**
1. A slug: lowercase words and hyphens, 24 characters at most. The number: the highest `NNNN` under
   `{docs}/features/` on the main branch and on every `feature/*` branch, plus one, on four digits.
2. The base: the repo's main branch (`origin/HEAD`, else `main`, else `master`), fetched first when
   there is a remote.
3. The branch and its worktree: add `.worktrees/` to `.git/info/exclude` if it is not there, then
   `git worktree add --no-track -b feature/<slug> .worktrees/feature.<slug> <base>`. Copy the
   untracked `.env*` files from the repo's top into the worktree (never commit them).
4. Write `.worktrees/feature.<slug>/{docs}/features/NNNN-<slug>/brief.md` with these headings
   exactly; a heading with nothing under it says `aucun`; **Mesure** and **Existant** are never `aucun`: ask or look them up:

   ```
   # <Titre>
   ## Résultat
   ## Pour qui
   ## Problème
   ## Pourquoi maintenant
   ## Mesure
   ## Contraintes
   ## Existant
   ## Non couverts
   ## Ouvert
   ```

5. Commit it on the feature branch: `brief — <Titre>`.
6. A split: one branch, folder and `brief.md` per feature, numbered in build order.
7. Go on to step 2 right away, on the first in build order, and say so in one line with how many
   decisions are left (« Reste 4 décisions, je commence. »). They stop you: `/cadrer-x-choisir <slug>`
   picks it up at step 2.

## Step 2 — the decisions

**Load, before any question.** The feature's `brief.md`, and `decisions.md` or `a-trancher.md` if
they exist. What is already settled — read it, never ask it: `{docs}/architecture.md` (its stack,
Modules, data), `{docs}/constitution.md`, `{docs}/adr/`.

Map the **design tree**: each decision and the ones that hang off it. The **frontier** is every
decision whose prerequisites are settled. Start from the idea's **Ouvert** list and the assumption
it rests on. Each answer reshapes the tree: recompute the frontier before the next question.

**The short path, as soon as you can tell**, for a small change: no new screen and no new way
through one (a change a person sees on a screen that exists is fine: a word, a colour, a link, a
button that misbehaves), no personal data, no new service or stack choice, no rule of the
constitution touched, and you can foresee one story and three tasks at most. A bug usually is one.
Say it in one line (« Petit changement : je prends la voie courte. ») and add `- voie : courte`
under **Étapes**. The decisions are then only the idea's **Ouvert** points: ask those, nothing more,
and save. Any doubt: the full path. The person's ask wins, before the tasks: the full path, or the
short path at any size: `- voie : courte — demandée`. **Bigger than it looked** (a later step
finds more than the above): `demandée` stays; else remove the line, commit `decisions.md` alone, and
with `écrans : oui` delete an uncommitted `taches.md`: the tasks follow the design. Each time, one
line says what the path skips (the design, the second look), or why it is now full.

**Stages, as soon as you can tell.** A browser page changes → `écrans : oui` (a terminal's output:
`non`). Say it in the first turn: with the spec comes a sketch of the screens and the ways
between them, and after its yes the finished design, its look and its words, which they approve
before the tasks are cut.

Format, without the tool:

```
**Q1** — <question> ? <why it matters, one line>
A) … · B) … · C) …
➡️ Conseil : A — <why>. « Oui » le prend ; ou une lettre, ou tes mots.
```

- **Ask until you can predict their next answers**, as in step 1, ranked scope > privacy > what the
  person sees > technical. What has a default nobody would argue with, write down as a decision
  marked *supposé* instead of asking.
- What you don't get to, or they leave for later, goes to `a-trancher.md` with your recommended
  answer: they settle it when the spec is written.
- Before closing, check the frontier holds each of these, where it applies, settled or cut on
  purpose: who uses it and whether each needs their own way in; where what it holds comes from, where
  it is kept, what happens if it is lost; the first time, an empty list, a wrong entry, a mistake
  undone; phone, computer or both; who else sees what; what it costs them to run; what must stay
  private. With screens, for the designer: the look (fonts, colours, a site they like, what
  « premium » means to them) and their real content (name, address, photos, and where those are).
- Small is a valid answer: if the feature shrinks to nothing worth building, say so.

**A new outside service** (email, text messages, payments, login, hosting, a database, an AI model,
storage, analytics, a scheduler) that the settled stack does not cover:
1. Say in two lines what is already chosen and what is ruled out: not asked again.
2. Look up what the settled services already offer for the need: an account they pay for often
   covers a second one.
3. Ask first: a service they want or already pay for. Then, unless the stack rules already say, one
   they refuse. What they name is used; say so plainly when it breaks a rule (a secret in the
   browser, personal data sent where nothing allows it, a line of the constitution).
4. For what is left: one proposal, with why, the monthly cost at their use, whether a card is
   needed, what happens at the free tier's limit, and what else was considered. They confirm.

**Close.** Tell one real day with the finished feature, step by step, in their words — who opens it,
what they do, what they see, what goes wrong — then what gets built, the stages, the services and
what they cost, the data kept and for how long, and what waits in `a-trancher.md`. Ask what is wrong
in it; each correction is folded in and the day told again, until a clear yes.

**Save — only after the yes**, in the feature's worktree: `decisions.md` beside `brief.md`, these
headings exactly, `aucun` under an empty one:

```
# <Titre> — décisions
## Décisions
- D1 <décision> — pourquoi : <their reason, or « supposé »>
## Étapes
- écrans : oui|non
- code : oui|non
- données : oui|non
- voie : courte|courte — demandée (only on the short path)
- bug : oui (only for a bug)
## Précisions
- Q : <question> → R : <réponse>
## Stack
- <besoin> : <choix> — pourquoi : … — coût : …/mois — aussi envisagé : … — demandé|proposé
## Impact archi
## Données et risques
## À faire
- [ ] <what the person sets up by hand, where> — avant le développement|avant la livraison
```

- **Étapes** — `code : non` is a copy or docs change; `données : oui` stores or changes stored data.
- **Impact archi** — usually `aucun`. Not when the feature adds a module, a table or a kind of stored
  data, an outside service or a running part (a job, a worker), or changes the stack. A setting saved
  per account is stored data: say what. `{docs}/architecture.md` itself is not edited here:
  `/cadrer-x-rendre` folds this in when the feature ships.
- **Données et risques** — read `cadrer-x-securite`. Each piece of personal data:
  what, where it is kept, the GDPR basis, how long, who sees it. Each secret by name and where it
  lives, never its value. The abuse cases: no login, someone else's data, bad input, too much input.
- **À faire** — every account, key or paid plan the person must create; each new outside service
  brings its own.

Questions left open: `a-trancher.md` beside them, one block each, numbered after the file's last Q:

```
## Q1 · spec · <the question, as they would ask it>
- Options : <a> | <b> | <c>
- Effets : <what each means for them>
- Conseil : <a> — <why>
- Réponse :
```

Commit on the feature branch: `décisions — <Titre>`. Then the spec, here: say in one line that you
go on with it, and go back to *Which step*. They stop you: `/cadrer-x-choisir <slug>` picks it up.

## Workers

The pages and the tasks are made by workers, subagents you start, so they never load here: you keep
the person. You start each one yourself, one after the other: no worker starts another.
`<skills folder>`: the folder holding this skill's folder, absolute path.

- **Start one** as the tool's general subagent (`general-purpose` in Claude Code, codex's default
  worker; never a registered or custom agent type, never the Skill tool), with a fresh context and
  one message: « You are cadrer-x-<role>. Read `<skills folder>/<its file>` whole and follow it, for
  <its stage> of the feature `<NNNN-slug>`, in `<the feature's worktree>`. Launched by choisir. » It
  runs in the background while you go on with the person; its last message is its report, which
  names every path it wrote, a helper's too (`{docs}/regles-ecriture.md`): you commit exactly those
  paths, never `git add -A`.
- **A correction** in this session goes to the same worker, resumed (Claude Code: a message to it;
  codex: input to it), in the person's words. With no worker open (a new session, or one closed), a
  fresh one reads the files already there and changes only what its message asks.
- Codex holds three subagents open at once, these and the ones that look facts up: close each worker
  once its stage is settled.
- **No subagents** (the tool has none, or they are off): follow its file yourself, then do your part
  below as if it had reported.

**The designer**: `cadrer-x-designer`, `cadrer-x-choisir/references/maquette.md`, for a feature with
screens (*Which step*), a changed screen as much as a new one. Its server is yours: a designer that
replaces it in this session gets its address and pid in its message, and you stop it (`kill <pid>`)
when you close the designer for good.

1. **The wireframe** (stage `wireframe`): started once the spec's draft is written. Show its report
   with the spec (the address, each screen, its states, where each leads): they judge the flow and the
   stories together, and the spec's yes waits for it. A flow change a story quotes changes the spec
   too; a spec change that moves a screen goes to the designer.
2. **The design** (stage `haute fidélité`), once the spec is `validée`: the same designer resumed,
   else a fresh one. Show the address, each screen and its states in one line, then its questions,
   one per message. With the claude-design tools in your session and no https `Lien :` in
   `passation.md`, offer once a Claude Design project of the same files, to see them on another
   device. On a yes, and later only when they ask, read `references/claude-design.md` whole and
   follow it yourself. Each correction goes to the designer, until a clear yes that names what it
   covers: « Ces mots et ce look : c'est bon ? »
3. **On the yes**, the designer (stage `passation`, with what `claude-design.md` gave for
   `passation.md`) writes `passation.md`. Commit the paths its reports named: `maquette — <Titre>`.
   Close the designer and its server, say in one line that you go on with the tasks, and go back to
   *Which step*. They stop you: `/cadrer-x-choisir <slug>` picks it up.

**The tasks**: the decoupeur (`cadrer-x-decoupeur`, `cadrer-x-choisir/references/decoupe.md`), then
the verificateur (`cadrer-x-verificateur`, `cadrer-x-verifier/SKILL.md`). No yes on the tasks: a
task list is technical.

1. **The decoupeur** writes `taches.md`. Its questions go to the person, one per message; each answer
   goes back to it, resumed. A report that they outgrow the short path: *bigger than it looked*; the
   line removed, back to *Which step*, else commit the paths its report named:
   `tâches — <Titre>`.
2. **The verificateur**, with nothing of yours in its message, unless `voie : courte`, or
   `cadrer-x-verifier` is not beside this skill's folder; wait for its report. What the files settle
   goes back to the decoupeur, resumed. What needs a product choice is a question for the person,
   with the finding's proposal as your recommendation; the spec is yours: their answer goes in
   `a-trancher.md` and in the scenario of `spec.md` (lint `spec` run again), then to the decoupeur.
   Commit what changed: `tâches — <Titre>`; `spec — <Titre> : corrections de la vérification` for
   the spec. No subagents: say in one line that `/cadrer-x-verifier`, in a fresh session, can check
   the spec and the tasks first.
3. **The stop.** Close the workers, and the designer's server if one runs. One message: what gets
   built (each story in one line, the number of tasks), what the second look changed, then
   `/cadrer-x-realiser <slug>`, better in a new session (`/clear`, then the command). Then stop: the
   build is theirs to start.

## Red flags

| Thought | Instead |
|---|---|
| "I'll ask the three basics at once to save time." | Step 1: one question, the next depends on it. Step 2: a numbered batch only of decisions that hang on nothing open. |
| "No guess, so I don't lead them." | A guess and a confidence, or a recommendation. |
| "Success: happier clients." | A number and a date they can check. |
| "I'll write the folder on the main branch." | The feature branch, in its worktree, after the yes. |
| "Both files saved; they'll type the next command." | Go on with the spec here, unless they stop you. |
| "No time: I'll code it here." | Never. The spec, in this reply: the short path is the fast way. |
| "I know what that reference says." | Read it whole now: it changes, and a summary drops it. |
