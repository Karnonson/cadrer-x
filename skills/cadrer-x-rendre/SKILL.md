---
name: cadrer-x-rendre
description: "Livrer une fonctionnalité. À lancer quand chaque récit de `taches.md` a sa relecture validée dans `audit.md`. Deux étapes : le dossier (la doc du projet mise à jour, l'ADR, la version, le CHANGELOG, `livraison.md`, `pr.md`, puis la fusion dans la branche principale sur un oui), et la mise en ligne (ce qui reste à préparer à la main, le plan montré avant de rien créer, payer ou envoyer, puis le trajet refait sur la vraie adresse). Ne corrige jamais le code."
disable-model-invocation: true
argument-hint: "[numéro ou nom de la fonctionnalité]"
---

# cadrer-x rendre — the paperwork, the merge, then online

The stories are built and each passed its review. You turn the feature into what a developer finds a
year later (the project's docs, an ADR, the CHANGELOG) and what the person judges before it leaves
(`livraison.md`, `pr.md`); then, with them, you merge it and put it online. You are the one skill that
pushes, and only on their yes: nothing that cannot be taken back happens without it. You never change
code or tests: what needs a code change goes back to `/cadrer-x-realiser`.

Talk, and write the files' text, in the person's language, every message included (the short notes
between steps too); in French, *tu* or *vous* as they write, *vous* when you can't tell, never both.
File names, headings, labels and commit messages stay exactly as written here and in the templates.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which step

Read first: `cadrer-x.yml` (`docs:`, `commands`, `envs`), `git worktree list`, `git branch --list
'feature/*' 'tache/*'`, `git remote -v`, the main branch's name.

- **The feature.** The argument's number or slug (a near miss with one close feature: that one, said in
  one line). None: the feature of the worktree you are in, else the
  one feature branch not merged into the main branch whose stories all have a `validé` section in
  `audit.md`; several: ask which, one question.
- **Where you work.** Step 1 in the feature's worktree (`.worktrees/feature.<slug>`, or the checkout on
  `feature/<slug>`, else `git worktree add` it, `.worktrees/` in `.git/info/exclude` first); step 2 on
  the main branch.
- `feature/<slug>` not merged into the main branch, and no `{feature}/livraison.md` committed for it:
  **step 1**. Committed, not merged: step 1's last part, **the merge**.
- Merged, and `livraison.md`'s **En ligne** says `pas encore`: **step 2**. It says `aucun — …` (a library,
  a tool run on one computer): nothing left; say so.
- Online already, and a later feature merged: step 2 again, for what changed.

## Step 1 — the package

### Ready, or say what is missing

Check each, and stop at the first that fails, naming the step that fixes it:

- Every task of `taches.md` is `[x]` on the feature branch, and no `tache/<slug>-*` branch is left
  unmerged → else `/cadrer-x-realiser <slug>`.
- Every story `US<n>` of `taches.md` has a section in `{feature}/audit.md` whose **Verdict** is
  `validé` → else `/cadrer-x-realiser <slug>` (it reviews what has no section, and fixes what is `à
  corriger`). A chat message saying it passed is not a verdict.
- Every question of `a-trancher.md` has a **Réponse** → else ask it now, one question, your
  recommendation first, and write the answer; one that changes what gets built stops here.
- The feature's worktree is clean, and the whole check command of `cadrer-x.yml` passes, run now, fresh:
  its output is `pr.md`'s evidence. A failure: stop, show it, name `/cadrer-x-realiser`.

### Read, in this order

1. `{feature}/spec.md` (the stories, **Pas encore**: their words are the CHANGELOG's and the PR's),
   `decisions.md` (**Impact archi**, **Données et risques**, **Stack**, **À faire**), `taches.md` (what was
   built, each task's `Risques :`), `a-trancher.md`, `audit.md`, the list of `{feature}/captures/`.
2. The project's docs you will update: `{docs}/architecture.md`, `{docs}/adr/` (their numbering and
   headings), `{docs}/security/`, and `{docs}/constitution.md`, read only: a rule that says what is
   checked at release (personal data listed before it is kept) is yours to meet. Read `cadrer-x-securite`.
3. `CHANGELOG.md`, the version file (the first of `package.json`, `pyproject.toml`, `Cargo.toml`,
   `VERSION` at the top), the commits of the feature (`git log --oneline <main>..feature/<slug>`).
4. The code each sentence you write is about. Write only what the branch shows: a protection with no
   code or test behind it is not written as done; it goes under **À faire** and you tell the person.

### The project's docs

- **An ADR** when **Impact archi** is not `aucun`: `{docs}/adr/NNNN-<slug>.md`, the next number. The
  existing ADRs' headings, else `templates/adr.md` (`Contexte`, `Décision`, `Options`, `Pourquoi`). At
  least two real options, from `decisions.md` and the code, never invented ones; « tu l'as choisi » where
  the person chose. An old ADR is never edited: a changed decision is a new ADR that names the one it
  replaces. A change to the constitution is an ADR too, and only one the person asked for.
- **`{docs}/architecture.md`**: only the sections the feature changes, each linking the ADR: **Modules**
  (the new module, what it owns, its paths), **Pièces**, **Données** (what is kept, who sees it, the
  copies), **Secrets** (by name), **Coût**, **Lancer**, **Mots** (a word the spec settled). The file stays
  the product's shape, never a log.
- **Personal data**: each piece the feature keeps or sends gets its line in the data list under
  `{docs}/security/` (`data-inventory.md`, or the file the constitution names): what, where it is kept, its
  GDPR basis, how long and then what, who sees it, from **Données et risques**.
- **Threats**: each task's `Risques :` line, with its protection and the test that proves it, in
  `{docs}/security/threat-model.md` (or the project's own file). Secrets by name only, never a value.
- **`{docs}/runbook.md`**, when it exists and the feature changes how the product is run: a table the
  copies must cover, a duration to enforce, a step to go back. Nothing changed: leave it.

Every file keeps its own format: headings, columns, numbering, language. A file the project lacks is
made only when the feature gives it something to hold.

### The version and the CHANGELOG

- The next version by what shipped: a new capability a minor bump, fixes only a patch, a change that
  breaks callers or kept data a major. Update the version file in its own syntax; none: the CHANGELOG
  carries the version alone, and no version file is made.
- `CHANGELOG.md` in its own format, else Keep a Changelog in French (`## [x.y.z] - AAAA-MM-JJ`,
  `### Ajouté`, `### Modifié`, `### Corrigé`, `### Sécurité`): one line per story, in the spec's words, for
  the people who use it.

### `livraison.md` and `pr.md`

From `templates/livraison.md` and `templates/pr.md`, in the feature's folder. A later release of the
same feature puts its section on top, under its version.

- **livraison.md**: **Version** (the new version alone on its first line), **Livré** (one line per story
  with its id, then what waits: **Pas encore**, a question left open), **En ligne** (`pas encore`, or
  `aucun — <pourquoi>` when the product never goes online), **Mise en ligne**, **Vérifié** and **En cas
  de problème** (step 2 fills them; `pas encore` meanwhile), **À faire** (each `avant la livraison` item
  of `decisions.md` and `architecture.md` still open, marked *à la main*).
- **pr.md**, a body a person who doesn't code can scan: **Résumé** (what changes, for whom, three to
  five lines in the spec's words), **Preuves** (the checks run now, trimmed, with their result; each
  story's review tour and verdict; each capture as `![SC1 à 390](docs/features/NNNN-x/captures/SC1-390.png)`,
  a path from the repo's top), **Risque de fusion** (`**Porte** : aller-retour` when merging and going
  back are cheap, code only or an added table; `aller simple` when something cannot be taken back,
  data deleted or rewritten, a message sent, money; then `**Portée** :` who would notice, and what).

Run `python3 <this skill's folder>/scripts/lint.py livraison {feature}/livraison.md` and `… pr
{feature}/pr.md`; fix and rerun until both print nothing.

### Show it, then save

In your message: the version, each doc changed (one line each: what it now says), the ADR's title, the
**Livré** lines, the **Porte**, what is under **À faire**. Ask what they would change, and fold each change
in, until a clear yes ("oui", "ok", "ça va", "c'est bon"; a hedge or a change asked for keeps it open). On the yes: commit on the feature
branch, the docs, the version file, `CHANGELOG.md`, `livraison.md` and `pr.md`: `livraison — <Titre> <version>`.

### The merge — its own yes

Say how it will go, and ask:

- **A remote** (`git remote -v`): push `feature/<slug>`, then open the pull request from `pr.md` (`gh pr
  create --base <main> --head feature/<slug> --title "<Titre> <version>" --body-file {feature}/pr.md`
  when `gh` is there; else give them the address git printed). Who merges it is the person's, on the
  host. Once merged (`git fetch`, then `git branch -r --merged origin/<main>`), step 2.
- **No remote**: in the main checkout, clean and on the main branch, `git merge --no-ff feature/<slug>
  -m "<Titre> <version>"`, then the whole check command once more on the result. Red: say it, and go
  no further.

Merged: remove the feature's worktree and its branch (`git worktree remove`, `git branch -d`). Then,
when **En ligne** says `pas encore`: step 2, here, said in one line (its plan has its own yes). Else
the next feature: `/cadrer-x-choisir`.

## Step 2 — online

Read `{docs}/architecture.md` (**Pièces**, **Secrets**, **Données**, **Coût**, **Trajet**, **À faire**),
`cadrer-x.yml` → `envs` (each environment: `url`, `deploy`, `rollback`), the feature's `livraison.md`, and
`decisions.md` → **À faire**. The main checkout is clean, on the main branch, at the merge (with a remote, `git pull --ff-only`
first); note the commit you put online.

**What the person prepares by hand.** Every open `avant la livraison` item, in one message, in order:
what, where, why it is needed, what it costs. One that spends money gets its own yes, with the amount,
before they do it. **A secret's value never passes through this conversation**: give them the page
where they paste it, or a command to run in a terminal of their own, into the place **Secrets** names;
run a command here only when neither it nor its output holds a secret. When they say done, check each
one you can without showing a value (the account lets you in, the address answers, a secret exists by
name, a value is no longer its local stand-in, compared never printed) and tick it in its file; one
nothing here can check is ticked on their word, `confirmé par la personne`. One that fails: say what you
saw, and go no further until it passes or they drop it; dropping one a piece needs drops that piece:
say what the people using it lose, and stop.

**The plan, before anything leaves this computer.** One table, in order: the action · what it creates,
changes, sends or deletes out there · what it costs now and per month · how to undo it. Real data starts
empty or from what the person gives, never from local test data; a change to kept data is a row that
says how to get it back. The cost alert **Coût** names is a row, and so are the copies **Données**
relies on. The last row is the check online. Wait for the yes; a changed row is shown again; a row that
spends money gets its own yes, with the amount. A no, or not now: say what is ready, write nothing.

**Run it.** The rows in order, from the commit you noted, one line per result. Never a secret's value in
code, a commit, a tracked file, or a command whose output is shown. A row that fails: stop, say what you
saw, undo the rows already run only if they say so, and write `livraison.md` with what is out there now
(each row run, what it created, spent or sent; the failed row under **À faire**), committed as
`livraison — arrêtée : <row>`: the next run skips what is still out there. The commands that worked go
into `cadrer-x.yml` → `envs` (`url`, `deploy`, `rollback`), so the next release runs them again.

**Check online.** On the real address, follow **Trajet** as the person would, then each scenario of the
feature that shows from outside, with a browser tool when you have one, and the person's own address or
account for anything sent, never someone else's. What you can't see from here (a message in their inbox):
ask them to look, and write what they said. A screenshot of each screen reached,
`{feature}/captures/livraison-<état>.png`. Remove what the check created, as the plan said. Wrong online
and right locally: say it plainly, and offer to go back to what was online before (the plan's undo) or
leave it up: their choice.

**Write and commit.** `livraison.md`: **En ligne** (the address, the date, the commit, the version),
**Mise en ligne** (the commands in order to do it again, secrets by name), **Vérifié** (each step of the
Trajet and each scenario checked: seen, or what was seen instead, with its capture), **En cas de
problème** (how to go back to the previous version, how to get the data back as **Données** says, where
to look when it stops), **À faire** (each item still open, *à la main*; each thing found wrong online,
one line `/cadrer-x-choisir` or `/cadrer-x-decouper` can turn into work). Lint it. Commit `livraison.md`,
`architecture.md`, `cadrer-x.yml` and the captures on the main branch: `livraison — <adresse>`; push it
only when a plan row said so.

End with: the address, what was checked and what was seen, what is wrong online if anything, and the
first thing to do now.

## Never

Change code, tests or a verdict of `audit.md`; push, merge, deploy or spend without the yes that covers
it; write a secret's value anywhere; put local test data online.

## Red flags

| Thought | Instead |
|---|---|
| "US2's review is still à corriger, but it's minor." | Every story `validé`, or `/cadrer-x-realiser US2`. |
| "The review passed, so the tests surely still pass." | Run the checks now; that output is the evidence. |
| "A new table is no big change: no ADR." | **Impact archi** not `aucun` is an ADR. |
| "The audit says the race is guarded." | Open the code; not found goes under **À faire**. |
| "They said yes to the package: I'll push too." | The merge has its own yes. |
| "Paste the API key here and I'll set it." | Never through the conversation: the page, or their own terminal. |
| "I'll seed production with the test members." | Real data starts empty or from what they give. |
| "A one-line fix and the check online passes." | No code here: **À faire**, then `/cadrer-x-realiser`. |
