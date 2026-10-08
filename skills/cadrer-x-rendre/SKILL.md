---
name: cadrer-x-rendre
description: "Livrer une fonctionnalité dont chaque récit a sa relecture validée dans `audit.md`. La doc du projet, l'ADR, la version, le CHANGELOG, `livraison.md` et `pr.md`, enregistrés sans rien demander ; un seul oui pour l'envoyer et la fusionner ; puis la mise en ligne : le plan montré avant de rien créer, payer ou envoyer, le trajet refait sur la vraie adresse. Ne corrige jamais le code."
disable-model-invocation: true
argument-hint: "[numéro ou nom de la fonctionnalité]"
---

# cadrer-x rendre — the paperwork, the merge, then online

You turn the reviewed feature into what a developer finds a year later (the project's docs, an ADR,
the CHANGELOG) and what the person reads at their one yes (`livraison.md`, `pr.md`); on it you push
and merge, then put it online with them. You alone push, only on their yes (*Never*). A code change
goes back to `/cadrer-x-realiser`, one the person asks first written as a task (its *The end*).

Talk, and write the files' text, in the person's language, every message included (each note between
tool calls too); in French, *tu* or *vous* as they write, *vous* when you can't tell, never both.
File names, headings, labels and commit messages stay exactly as written here and in the templates.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/aide.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

**Retour.** In the main session (never as a subagent), before the message that ends this run (the
stop, the next command given, or the person stopping): open `../cadrer-x-retour/SKILL.md`, beside
this skill's folder, → *When*, and follow it. Not there: go on without it.

## Which step

Read first: `cadrer-x.yml` (`docs:`, `commands`, `envs`), `git worktree list`, `git branch --list
'feature/*' 'tache/*'`, `git remote -v`, the main branch's name.

- **The feature.** The argument's number or slug (a near miss with one close feature: that one, said in
  one line). None: the feature of the worktree you are in, else the
  one feature branch not merged into the main branch whose stories all have a `validé` section in
  `audit.md`; several: ask which, one question.
- **Where you work.** Step 1 in the feature's worktree (`.worktrees/feature.<slug>`, or the checkout on
  `feature/<slug>`, else `git worktree add` it, `.worktrees/` in `.git/info/exclude` first); the merge
  and online in the main checkout (`<top>`, the repo's top), clean, on the main branch.
- `feature/<slug>` not merged into the main branch, and no `{feature}/livraison.md` committed for it:
  **step 1**. Committed, not merged, in this order: the feature branch has commits after it (a task
  added since): step 1 again, its files updated. Pushed as it is, its pull request open (`gh pr view
  feature/<slug>`, else `git ls-remote --heads origin feature/<slug>`): with `gh`, its checks passed
  and nothing queued, the yes for its merge alone (*The yes*); else say what it waits on, and wait.
  Else: **the yes**.
- Merged (with a remote, into `origin/<main>` after `git fetch`): *After the merge*.

## Step 1 — the package

### Ready, or say what is missing

Check each, and stop at the first that fails, naming the step that fixes it:

- `spec.md` and `taches.md` exist → else `/cadrer-x-choisir <slug>`.
- Every task of `taches.md` is `[x]` on the feature branch, and no `tache/<slug>-*` branch is left
  unmerged → else `/cadrer-x-realiser <slug>`.
- Every story `US<n>` of `taches.md` has a section in `{feature}/audit.md` whose **Verdict** is
  `validé` → else `/cadrer-x-realiser <slug>`. A chat message saying it passed is not a verdict.
- Every question of `a-trancher.md` has a **Réponse** → else ask it now, one question, your
  recommendation first, and write the answer; one that changes what gets built stops here.
- The feature's worktree is clean, and the whole check command of `cadrer-x.yml` passes, run now, fresh:
  its output is `pr.md`'s evidence. A failure: stop, show it, name `/cadrer-x-realiser`.
- The scan before a release passes, run now (read `cadrer-x-securite` → *Before a release*): its lines
  are `pr.md`'s evidence too. A secret: that helper's stop. A flaw in a package: the task that helper
  writes in `taches.md`, then stop and name `/cadrer-x-realiser <slug>`.

### Read, in this order

1. `{feature}/spec.md` (the stories, **Pas encore**: their words are the CHANGELOG's and the PR's),
   `decisions.md` (**Impact archi**, **Données et risques**, **Stack**, **À faire**), `taches.md` (what was
   built, each task's `Risques :`), `a-trancher.md`, `audit.md`, the list of `{feature}/captures/`.
2. The project's docs you will update: `{docs}/architecture.md`, `{docs}/adr/` (their numbering and
   headings), `{docs}/security/`, and `{docs}/constitution.md`, read only: a rule that says what is
   checked at release (personal data listed before it is kept) is yours to meet. Read `cadrer-x-securite`,
   and `cadrer-x-textes` before the CHANGELOG and `pr.md`.
3. `CHANGELOG.md`, the version file (the first of `package.json`, `pyproject.toml`, `Cargo.toml`,
   `VERSION` at the top), the commits of the feature (`git log --oneline <main>..feature/<slug>`).
4. The code each sentence you write is about. Write only what the branch shows: a protection with no
   code or test behind it is not written as done: an **À faire** line for `/cadrer-x-realiser <slug>`.

### The project's docs

- **An ADR** when **Impact archi** is not `aucun`: `{docs}/adr/NNNN-<slug>.md`, the next number. The
  existing ADRs' headings, else `templates/adr.md` (`Contexte`, `Décision`, `Options`, `Pourquoi`). At
  least two real options, from `decisions.md` and the code, never invented ones; « tu l'as choisi » where
  the person chose. An old ADR is never edited: a changed decision is a new ADR that names the one it
  replaces. A change to the constitution is an ADR too, and only one the person asked for.
- **`{docs}/architecture.md`**: only the sections the feature changes, each linking the ADR: **Modules**
  (the new module, what it owns, its paths), **Pièces**, **Données** (what is kept, who sees it, the
  copies), **Secrets** (by name), **Coût**, **Lancer**. The file stays the product's shape, never a log.
- **`{docs}/glossaire.md`**: each word the spec settled, with its meaning, and the word it replaces.
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
  with its id, then `- Plus tard : <what waits>`: **Pas encore**, a question left open, each `Détail :`
  left in `audit.md`), **En ligne** (`pas encore`, or `aucun — <pourquoi>` when the product never goes
  online), **Mise en ligne**, **Vérifié** and **En cas de problème** (going online fills them; `pas
  encore` meanwhile), **À faire**: only what needs the person's own hands (*à la main*) or a
  `/cadrer-x-…` command for a gap; never what is done or what an agent can do here. Each open `avant la
  livraison` item of `decisions.md` and `architecture.md`: checked now, ticked there if done.
- **pr.md**, a body a person who doesn't code can scan: **Résumé** (what changes, for whom, three to
  five lines in the spec's words), **Preuves** (the checks run now, trimmed, with their result; each
  story's review tour and verdict; each capture as `![SC1 à 390](docs/features/NNNN-x/captures/SC1-390.png)`,
  a path from the repo's top), **Risque de fusion** (`**Porte** : aller-retour` when merging and going
  back are cheap, code only or an added table; `aller simple` when something cannot be taken back,
  data deleted or rewritten, a message sent, money; then `**Portée** :` who would notice, and what).

Run `python3 <this skill's folder>/scripts/lint.py livraison {feature}/livraison.md` and `… pr
{feature}/pr.md`; fix and rerun until both print nothing.

### The yes

Both lints clean: commit on the feature branch, unasked, the docs, the version file, `CHANGELOG.md`,
`livraison.md` and `pr.md`: `livraison — <Titre> <version>`. Then one message, the summary inside the
question: the version, each doc changed in one line, the ADR's title, the **Livré** lines (a `Détail :`
left waits under **Plus tard**: realiser asked, not you), **Porte** and **Portée**, **À faire**; then,
plainly: may you send it, open the pull request, merge it into the main branch (no remote: merge it)?
A hedge or a change asked for keeps it open; a package change: made, linted, committed, asked again.

On the yes:

- **A remote**: push `feature/<slug>`; with `gh`, open the pull request from `pr.md` (`gh pr create
  --base <main> --head feature/<slug> --title "<Titre> <version>" --body-file {feature}/pr.md`; one
  already open takes the push, never a second; its base not `<main>`: say so, and no merge). Then
  `gh pr checks feature/<slug>`: one failed or pending: say which, plainly, and stop, never
  bypassed. All passed, or none: `gh pr merge feature/<slug> --merge`, then `git fetch` and `git
  merge-base --is-ancestor feature/<slug> origin/<main>`; not there (queued): say so, and wait. No
  `gh`, or the host refuses the merge: say what you saw and give the address; the merge is theirs.
- **No remote**: `git -C <top> merge --no-ff feature/<slug> -m "<Titre> <version>"`, then the whole
  check command there once more. Red: say it, and go no further.

In `origin/<main>`, or merged here and green: *After the merge*.

### After the merge

With a remote, `git -C <top> pull --ff-only` first. Remove the feature's worktree and branch, if
still there (`git -C <top> worktree remove`, `branch -d`); never the folder this session runs in:
then say they stay until a run from elsewhere. Then, by `livraison.md`'s **En ligne**:

- `aucun — …`, or an address with nothing merged since: nothing left; say so. The next feature is
  theirs to start: `/cadrer-x-choisir`.
- `pas encore`, or an address with a later feature merged since: **online**, here (its plan has its
  own yes): read `references/en-ligne.md` whole now, then follow it; after a summary of this
  conversation, read it again.

## Never

Change code, tests or a verdict of `audit.md`; push, merge, deploy or spend without the yes that covers
it; write a secret's value anywhere; put local test data online.

## Red flags

| Thought | Instead |
|---|---|
| "US2's review is still à corriger, but it's minor." | Every story `validé`, or `/cadrer-x-realiser US2`. |
| "The review passed, so the tests surely still pass." | Run the checks now; that output is the evidence. |
| "The review looked at security; no need to scan." | The scan runs now: secrets in the history, flawed packages. |
| "A new table is no big change: no ADR." | **Impact archi** not `aucun` is an ADR. |
| "The audit says the race is guarded." | Open the code; not found goes under **À faire**. |
| "I know what that reference says." | Read it whole now: it changes, and a summary drops it. |
