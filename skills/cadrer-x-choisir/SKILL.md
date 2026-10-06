---
name: cadrer-x-choisir
description: "Choisir quoi construire, de l'idée aux tâches. À lancer avec une idée de fonctionnalité ou de changement, ou un bug à corriger ; avec le nom d'une fonctionnalité, reprend l'étape ouverte. Une question à la fois : l'idée, les décisions, la spec, la maquette s'il y a des écrans, puis les tâches. Ne code pas."
disable-model-invocation: true
argument-hint: "<idée, ou numéro ou nom d'une fonctionnalité à reprendre>"
---

# cadrer-x choisir — from the idea to the tasks

You find out what the person wants and settle what it takes, one question at a time. Two steps, each
ending in one file in the feature's folder: the idea (`idee.md`), then the decisions (`decisions.md`).
Then the stages your references hold: the spec, the prototype when there are screens, the tasks. No
code: the builders build from your files, and whatever you leave unsettled they will guess.

Talk, and write the files' text, in the person's language, every message included (the short notes between steps too); in French, *tu* or *vous* as they write,
*vous* when you can't tell, and never both. File names, headings and labels stay
exactly as written here, in every language: the later skills find them by these names.

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
  close feature: that one, said in one line) with no `idee.md`, or it is an idea in words: **step 1**.
- **Where you work**, for a feature that has its `idee.md`: its worktree `.worktrees/feature.<slug>`
  when it exists; else the current checkout when it is on `feature/<slug>`; else `git worktree add
  .worktrees/feature.<slug> feature/<slug>` (add `.worktrees/` to `.git/info/exclude` first if it is
  missing, and copy the untracked `.env*` files in). Every file is written there, in
  `{docs}/features/NNNN-<slug>/` (`{feature}`), and committed on that branch.
- A `{feature}/verification.md` whose **Verdict** is `à reprendre`, committed after the last commit
  of the file its findings name (`git log -1 --format=%ct -- <file>`): a revision (below) of that
  stage (`→ spec`: the spec, first; `→ tâches`: the tasks). Its findings are what changes, never
  asked again.
- Else the first stage still open, in this order:
  - no `decisions.md`: **step 2**.
  - no `spec.md`, or its **Statut** is not `validée` (a draft is picked up where it is): the spec:
    read `references/spec.md` whole now, then follow it.
  - `écrans : oui` in `decisions.md` → **Étapes**, no `voie : courte`, and no `passation.md`: the
    prototype: read `references/maquette.md` whole now, then follow it. With the claude-design tools
    in your session, its Claude Design offer: `references/claude-design.md`.
  - no `taches.md`: the tasks: read `references/decoupe.md` whole now, then follow it.
- Every stage's file there: a revision. Ask which file changes and what changed; ask only that.
- **A revision** runs the stage that changes, then each later stage whose file exists, in order, each
  by its step or reference as above, without asking again: the prototype only when the change moves
  a screen, the tasks once `taches.md` exists. A stage that ends by going back to *Which step* goes
  on to the next of these; after the last, stop with its usual next step.

## Every turn

- **One question per message** when the next depends on its answer, the one that unblocks the most.
  One question has one thing to answer: never two asks joined by "and" or "or". Choices are fine when
  they pick one. In step 2, decisions that hang on nothing still open may go out together, numbered,
  each with its recommendation, at most five: they answer in one message (« 1 A, 2 oui, 3 … »).
- Each question carries your answer: a guess and how sure you are (step 1), or a recommendation a
  plain "oui" accepts (step 2). Reacting is faster than inventing.
- With the AskUserQuestion tool: one question per call, your answer as the first option, the context
  in your message just before it. No tool, or it fails: write the question in your reply, and your
  turn ends there. Never say a question was asked elsewhere or will come separately.
- When a background check reports after your question, the message it triggers ends with the open
  question repeated whole, never a pointer to it.
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
   `idee.md`, the manifest (package.json, pyproject.toml, Makefile). What they answer, you don't ask.
   What a memory or another project says about the person is a guess to put to them, never a line of
   `idee.md` on its own. **À faire** in `{docs}/architecture.md` says the code is still to be laid out
   in modules: say in one line that `/cadrer-x-ranger` first makes this feature and every next one
   cheaper, and go on with theirs unless they take it.
2. **Several capabilities in one ask** (parts that could ship and be checked apart: a booking, a
   payment, reminders, a report): your first question is the split. A short table — feature · what it
   does · what it needs first — a build order (what the others need, then the most useful), and your
   guess which to talk through first. Each becomes its own feature; what they share (who, why now) is
   asked once.
3. **A problem but no idea yet**: before narrowing, lay out three to five different ways to solve it
   as a table — one line · what it makes worse · rough size — one of them almost no work. Then your
   pick and the assumption it rests on. They choose; the interview goes on with that one.
4. Then your read of the idea in one line with a confidence, and Q1.

Format, without the tool, in their language:

```
**Q2 · Pour qui** — <the question in plain words, two or three concrete choices when they help>
➡️ Mon idée : <the answer you expect, and what it rests on> — confiance ~40 % (il manque : <what>)
```

**What the interview settles** — the headings of `idee.md`:

- **Résultat** — what is true for the user once it ships.
- **Pour qui** — which people, how many, what they use today.
- **Problème** — what it costs them today; the last time it happened, step by step.
- **Pourquoi maintenant**
- **Mesure** — a number a non-developer can check, and a date ("moins d'1 appel manqué sur 10 d'ici
  le 31 janvier"), never "plus d'engagement".
- **Contraintes** — money, time, what must not change.
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
4. Write `.worktrees/feature.<slug>/{docs}/features/NNNN-<slug>/idee.md` with these headings
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

5. Commit it on the feature branch: `idee — <Titre>`.
6. A split: one branch, folder and `idee.md` per feature, numbered in build order.
7. Go on to step 2 right away, on the first in build order, and say so in one line with how many
   decisions are left (« Reste 4 décisions, je commence. »). They stop you: `/cadrer-x-choisir <slug>`
   picks it up at step 2.

## Step 2 — the decisions

**Load, before any question.** The feature's `idee.md`, and `decisions.md` or `a-trancher.md` if
they exist. What is already settled — read it, never ask it: `{docs}/architecture.md` (its stack,
Modules, data), `{docs}/constitution.md`, `{docs}/adr/`.

Map the **design tree**: each decision and the ones that hang off it. The **frontier** is every
decision whose prerequisites are settled. Start from the idea's **Ouvert** list and the assumption
it rests on. Each answer reshapes the tree: recompute the frontier before the next question.

**The short path, as soon as you can tell.** A small change does not need the whole ceremony: no new
screen and no new way through one (a change a person sees on a screen that exists is fine: a word, a
colour, a link, a button that misbehaves), no personal data, no new service or stack choice, no rule
of the constitution touched, and you can foresee one story and three tasks at most. A bug usually is
one. Say it in one line (« Petit changement : je prends la voie courte. ») and add `- voie : courte`
under **Étapes**. The decisions are then only the idea's **Ouvert** points: ask those, nothing more,
and save. Any doubt, or the person asks for the full path: the full path. The spec, the tasks and
`realiser` read that line and lighten their steps.

**Stages, as soon as you can tell.** Anything a person sees changes → `écrans : oui`. Say it in the
first turn: after the spec comes a clickable prototype they judge before the tasks are cut. On the
short path, no prototype: the review checks the change on the real page.

Format, without the tool, in their language:

```
**Q1** — <question> ? <why it matters, one line>
A) … · B) … · C) …
➡️ Conseil : A — <why>. « Oui » le prend ; ou une lettre, ou tes mots.
```

- **At most 5 clarification questions.** Rank them scope > privacy > what the person sees >
  technical. What has a default nobody would argue with, write down as a decision marked *supposé*
  instead of asking. The stack questions and the closing story do not count.
- What you don't get to, or they leave for later, goes to `a-trancher.md` with your recommended
  answer: they settle it when the spec is written.
- Before closing, check the frontier holds each of these, where it applies, settled or cut on
  purpose: who uses it and whether each needs their own way in; where what it holds comes from, where
  it is kept, what happens if it is lost; the first time, an empty list, a wrong entry, a mistake
  undone; phone, computer or both; who else sees what; what it costs them to run; what must stay
  private.
- Small is a valid answer: if the feature shrinks to nothing worth building, say so.

**A new outside service** (email, text messages, payments, login, hosting, a database, an AI model,
storage, analytics, a scheduler) that the settled stack does not cover:
1. Say in two lines what is already chosen and what is ruled out: not asked again.
2. Look up what the settled services already offer for the need: an account they pay for often
   covers a second one. Today's docs and prices, never memory.
3. Ask first: a service they want or already pay for. Then, unless the stack rules already say, one
   they refuse. What they name is used; say so plainly when it breaks a rule (a secret in the
   browser, personal data sent where nothing allows it, a line of the constitution).
4. For what is left: one proposal, with why, the monthly cost at their use, whether a card is
   needed, what happens at the free tier's limit, and what else was considered. They confirm.

**Close.** Tell one real day with the finished feature, step by step, in their words — who opens it,
what they do, what they see, what goes wrong — then what gets built, the stages, the services and
what they cost, the data kept and for how long, and what waits in `a-trancher.md`. Ask what is wrong
in it; each correction is folded in and the day told again, until a clear yes.

**Save — only after the yes**, in the feature's worktree: `decisions.md` beside `idee.md`, these
headings exactly, `aucun` under an empty one:

```
# <Titre> — décisions
## Décisions
- D1 <décision> — pourquoi : <their reason, or « supposé »>
## Étapes
- écrans : oui|non
- code : oui|non
- données : oui|non
- voie : courte (only on the short path; else no line)
- bug : oui (only for a bug; else no line)
## Précisions
- Q : <question> → R : <réponse>
## Stack
- <besoin> : <choix> — pourquoi : … — coût : …/mois — aussi envisagé : … — demandé|proposé
## Impact archi
## Données et risques
## À faire
- [ ] <what the person sets up by hand, where> — avant la construction|avant la livraison
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

## Red flags

| Thought | Instead |
|---|---|
| "I'll ask the three basics at once to save time." | Step 1: one question, the next depends on it. Step 2: a numbered batch only of decisions that hang on nothing open. |
| "No guess, so I don't lead them." | A guess and a confidence, or a recommendation. |
| "It's one idea, one feature." | Could its parts ship apart? Then it is several. |
| "Success: happier clients." | A number and a date they can check. |
| "I'll write the folder on the main branch." | The feature branch, in its worktree, after the yes. |
| "Both files saved; they'll type the next command." | Go on with the spec here, unless they stop you. |
| "I know what that reference says." | Read it whole now: it changes, and a summary drops it. |
