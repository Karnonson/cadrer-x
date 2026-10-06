---
name: cadrer-x-affiner
description: "Affiner ce qu'on construit. À lancer quand une fonctionnalité a son `decisions.md` mais pas encore sa spec, ou sa spec validée mais pas encore sa maquette alors qu'elle a des écrans. Deux étapes : la spec (`spec.md` : les récits, les scénarios, les exigences, que la personne valide), puis la maquette cliquable quand il y a des écrans (`maquette/`, `contenu.md`, `passation.md`). Ne découpe pas en tâches, ne code pas."
disable-model-invocation: true
argument-hint: "<numéro ou nom de la fonctionnalité>"
---

# cadrer-x affiner — the spec, then the prototype

You turn the feature's idea and decisions into what the person approves before any *how*: the spec
(what each person does and sees), then, when the feature has screens, a prototype they click. Two
steps, each ending in files on the feature's branch: `spec.md` (with `a-trancher.md` for what is
left to decide), then `maquette/`, `contenu.md` and `passation.md`. No tasks, no code: `/cadrer-x-decouper`
cuts the tasks from your files, and the builders build from them without you.

Talk, and write the files' text, in the person's language, every message included (the short notes between steps too); in French, *tu* or *vous* as they write,
*vous* when you can't tell, and never both. File names, headings, labels and ids stay exactly as
written here and in the templates, in every language: the later skills find them by these names.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/aide.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Which step

Read first: `cadrer-x.yml` (`docs:`, default `docs`), `git worktree list`, `git branch --list 'feature/*'`.

- **The feature.** The argument's number or slug; a near miss (`devis` for `defis`, `001-defis`) with
  one close feature: that one, said in one line. No argument: the feature of the worktree you are in,
  else the one feature with `decisions.md` and no validated spec; several: ask which, one question.
- **Where you work.** Its worktree `.worktrees/feature.<slug>` when it exists; else the current
  checkout when it is on `feature/<slug>`; else the branch exists: `git worktree add
  .worktrees/feature.<slug> feature/<slug>` (add `.worktrees/` to `.git/info/exclude` first if it is
  missing, and copy the untracked `.env*` files in). Every file below is written there, in
  `{docs}/features/NNNN-<slug>/` (`{feature}` from here on), and committed on that branch.
- No `decisions.md`: say `/cadrer-x-choisir <slug>` settles the decisions first, and stop.
- No `spec.md`, or one whose **Statut** is `brouillon`: **step 1** (a draft is picked up where it is).
- A validated spec, `écrans : oui` in `decisions.md` → **Étapes**, no `voie : courte`, and no
  `passation.md`: **step 2**.
- A validated spec, and `écrans : non` or `voie : courte`: nothing to do here; say the next step,
  `/cadrer-x-decouper <slug>`.
- Everything there: a revision. A `{feature}/verification.md` committed after the last commit of `spec.md` (`git log -1 --format=%ct -- <file>`): its findings for
  `/cadrer-x-affiner` are what changes, never asked again. Else ask what changes; ask only that. Then
  redo the part it touches the way its step says. A spec change that moves a screen changes the prototype too; once `taches.md`
  exists, say `/cadrer-x-decouper <slug>` must cut the tasks again.

## Every turn, both steps

- **One question per message**, the one that changes the most, with your recommendation a plain
  "oui" accepts. One question has one thing to answer: never two asks joined by "and" or "or".
  Questions that hang on nothing still open may go out together, numbered, each with its
  recommendation: they answer in one message.
- With the AskUserQuestion tool: one question per call, your recommendation as the first option, the
  context in your message just before it. No tool, or it fails: write the question in your reply,
  and your turn ends there. Never say a question was asked elsewhere or will come separately.
- **Settled stays settled.** `decisions.md` → **Décisions** and **Précisions**, and every answered
  question of `a-trancher.md`, are read, never asked again.
- **Facts are looked up, never asked**: what the repo, the product or the web can answer. What you
  hand to a subagent, you don't also look up yourself.
- **Plain words.** No file names, formats or code in a question.
- **A clear yes closes a step**: "oui", "ok", "ça va", "c'est bon", "mieux", or a condition already
  met. Say in one line what you save, then save. A hedge ("bof", "je sais pas") or a change asked for
  keeps it open: ask what they would change.

## Step 1 — the spec

**Short path** (`voie : courte` under **Étapes** of `decisions.md`): one story, its scenarios, the
**Cas limites** that are real, **Exigences** and **Critères** in one or two lines each, no question
unless the three-part bar below is met, and no `Vérifs` ceremony beyond the lint. Show it in one
message and ask for the yes as below. A change a person sees: its scenario names the page and what
they see there, in their words. A bug (`bug : oui`): the first scenario is the report's steps, with
what should happen. If writing it shows more than one story, a new screen or a new way through one,
or personal data: say the change is bigger than it looked, remove the `voie : courte` line from `decisions.md`
(commit it), and carry on with the full path.

**Read, in this order:** `{feature}/idee.md` (Résultat, Pour qui, Mesure, Non couverts, **Ouvert**),
`{feature}/decisions.md` (Décisions, Étapes, **Précisions**, **Données et risques**),
`{feature}/a-trancher.md` if it exists, `{docs}/constitution.md` (no story may contradict a rule),
`{docs}/glossaire.md` and the README for the product's own words: use them, never a synonym. The
product's name: `{docs}/vision.md` and the glossary first, before the README or the pages; where they
disagree, one question. `{docs}/architecture.md` only tells you what exists; none of it goes into the
spec.

**What goes in, and what stays out.**
- **What and why, never how.** No stack, module, table, file format, request or code word ("API",
  "CSV", "base de données", "authentifié", "UTC"). Say what a person does and sees: "un fichier que
  mon tableur ouvre", "on me dit que l'atelier est complet". A decision worded technically in
  `decisions.md` becomes what the person sees.
- **Only what was asked.** Every story traces to the idea's Résultat or Problème, or to a decision or
  a précision. Something tempting nobody asked for (a history page, a clean-up job) goes under **Pas
  encore** with why. A data rule (how long it is kept, who may see it) is a scenario or an exigence
  of the story it touches, never a story of its own.
- **Every decision lands.** Each D<n> and each précision shows up in a story, an exigence, or Pas encore.
- **Personal data.** Where a story collects, keeps, shows or sends it, read `cadrer-x-securite`. Who may see, change or download each piece is a scenario of that story; each
  piece that **Données et risques** lacks, or lists without a basis or a duration, is a question.
- **The constitution is not yours to read loosely.** A story that needs a rule bent, or a reading of
  a rule's words the repo does not settle ("leurs ateliers" when nothing says who runs a workshop),
  is a question, never a line of Supposé. Rules change only through an ADR.
- **What the product lacks.** A story that needs something the product does not have yet (a way to
  sign in, a person's role, a place to show it) says so: a question when it changes what a person
  sees or who sees what, else a line of Supposé naming the gap.

**Write the draft** from `templates/spec.md`, its headings, labels and ids exactly, comments
removed, **Statut** : `brouillon`:
- Stories `US1`, `US2`… with no gap, one per thing someone does or gets, the most useful first, each
  with its priority, **Test seul** and two to five **Scénarios** (Étant donné… quand… alors…): the
  ordinary case, then the awkward ones the decisions imply (full, empty, twice, too late, someone
  else's data).
- **Exigences** `EF1`…: each a "DOIT" a person could check, each tied to a story's scenario.
  **Données clés** only when `données : oui`.
- **Critères** `CS1`…: the idea's Mesure, checkable without code (counted, timed, seen).
- **Supposé**: every default you chose alone, one line each, so they can strike it.
- **Pas encore**: the idea's Non couverts, what you cut, each with why.

**A question, only where all three hold:** the answer changes the scope, someone's privacy, or what a
person sees; the readings differ in what they cost; no default nobody would argue with exists. At
most three, scope first, then privacy, then what people see. The open `spec` questions already in
`a-trancher.md` and the idea's **Ouvert** points are the usual ones; everything below the bar is a
line of **Supposé**. Write the draft around your recommended answer, mark the place
`[À PRÉCISER : <the point> → Q<n>]`, and add the question to `{feature}/a-trancher.md` (create it with
a `# <Titre> — à trancher` title; next free Q number):

```
## Q1 · spec · <the question, as they would ask it>
- Options : <a> | <b> | <c>
- Effets : <what each changes for them, in plain words>
- Conseil : <a> — <why>
- Réponse :
```

**First turn**, once the draft is written: say where it is (one line), its stories one line each
(id, who, what), then the first question, in this format without the tool:

```
**Q1** — <question> ? <why it matters, one line>
A) … · B) … · C) …
➡️ Conseil : A — <why>. « Oui » le prend ; ou une lettre, ou tes mots.
```

Each answer goes in `- Réponse :`, and the draft changes where its marker was; then the next
question. No question left: ask them to read the spec, and what they would change. Each change is
folded in, and they are asked again, until a clear yes.

**The Vérifs, before the yes.** Check the draft against each line of **Vérifs**, plus the feature's
own, and tick a line only once the spec passes it. A line that fails changes the spec until it
passes; a line is never deleted to pass.

**Save — only after the yes.** **Statut** : `validée`. Run `python3 <this skill's folder>/scripts/lint.py
spec {feature}/spec.md`, fix and rerun until it prints nothing. Commit `spec.md` and `a-trancher.md`:
`spec — <Titre>`. Then, `écrans : oui` and no `voie : courte`: step 2, right away, said in one line.
`écrans : non`, or `voie : courte`: the tasks, here: say in one line that you go on, open `../cadrer-x-decouper/SKILL.md`, read it whole and
follow it for this feature. They stop you: the command to type later.

## Step 2 — the prototype

A clickable mock-up of every screen the spec implies, made of plain pages, to judge before any code.
The builders build from it later, without you: `passation.md` tells them what each screen is.

**Read:** `{feature}/spec.md` (each story a person sees is a screen, or a state of one; its scenarios
are what the screen must let them do and see), `{feature}/decisions.md`, `{docs}/constitution.md`.
**The look**, the first that answers: `cadrer-x.yml` → `design_system:` (a path), `{docs}/design-system/`,
then the app's own tokens file and components when it has screens already. Read `cadrer-x-design-system`. None: `templates/maquette/styles.css`, a plain
neutral one, and say once that the look is the prototype's, not a brand. **The words:** read `cadrer-x-textes`; in French, at least: the product's *tu* or *vous*, its own
words, a space before `: ; ! ?` and inside `« »`.

**The pages, in `{feature}/maquette/`:**
- **Self-contained.** The design system's stylesheet copied byte for byte as `maquette/styles.css`
  (`cp`, never edited), `templates/maquette/maquette.js` copied as is. No script or stylesheet from
  another site, no build step: the folder alone opens every page. A font the look needs is copied into
  `maquette/fonts/` (a `.woff2` its licence lets you copy) and declared in the page's `<style>`.
- **The first version is the feature's, whole.** Every tone and motion the decisions and the spec name
  (animations, a playful tone, emoji) is in it already: a prototype that plays it safe costs a round.
- **One plain `.html` page per screen**, from `templates/maquette/page.html`: `lang` the person's
  language, `href="styles.css"`, `src="maquette.js"`.
- **Only the design system's tokens and parts.** A part it lacks is built from its tokens in the
  page's `<style>`, and listed in `passation.md` → **Nouveautés**. No raw colour or size.
- **Every state reachable.** Each state the stories imply (before anything, the ordinary result,
  nothing found, an error, too long, done) is a `<section data-state="<name>">`, shown by its address
  (`recherche.html#erreur`) and by clicking; the page's own controls move between states (sending the
  form shows the result) with `data-goto="<state>"`. The bar `<nav class="maquette-etats">` links
  every state; it and `maquette.js` are the prototype's own, never product code. Pages link to each
  other as the real screens will.
- **Invented, plausible data**, never a real person's, and no more of a person's own data than the
  screen needs (a first name, not an email address). A screen that collects personal data says what
  for, and asks for consent, never pre-ticked, when **Données et risques** gives consent as the basis.
- **Every text a person reads** is also in `{feature}/contenu.md` (from `templates/contenu.md`), word
  for word, by screen and state; a number that varies has each form.

**Check it in a browser, at 390 and 1280 wide.** Serve the folder on this machine only, in the
background, and keep the pid:

```
port=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])') && (python3 -m http.server "$port" --bind 127.0.0.1 --directory {feature}/maquette >/dev/null 2>&1 & echo "port $port pid $!")
```

With a browser tool, for each page and state (`http://127.0.0.1:<port>/<page>.html#<state>`), at
390×844 and 1280×800: each text is `contenu.md`'s, each field has a label, Tab walks a sensible order;
`document.documentElement.scrollWidth <= innerWidth`; no console error; each link and control goes
where its story says. Screenshots are only for you to look at: none goes in the repo. Fix what
fails, and check again. No browser tool: say so, and never call the pages checked.

**Show it.** Give them the address of the first page (the server keeps running), the screens and
their states one line each, and ask what they would change. With the claude-design tools in your
session, offer once to put the same files in a Claude Design project, to open on a phone and comment
there: `references/claude-design.md`. Each change is made in the pages and `contenu.md`, checked
again, and they are asked again, until a clear yes. A change that alters a word or a number a scenario
of `spec.md` quotes changes the spec too, in the same commit, its lint run again. A value you made up
for the page (points, a limit, a delay) that no file settles is a question before the save. A
correction to the words: read `cadrer-x-textes` (it offers to keep the rule).

**Save — only after the yes.** `kill <pid>`. Write `{feature}/passation.md` from
`templates/passation.md`: one screen per page, `SC1`, `SC2`… with no gap (a screen keeps its id
across revisions; a new one takes the next number), each line on one line, since a task's builder
quotes its screen's section word for word. Check it against its **Contrôle** list, reading the pages
themselves; what fails changes the pages or the file. Run `python3 <this skill's folder>/scripts/lint.py
passation {feature}/passation.md` until it prints nothing. Commit `maquette/`, `contenu.md`,
`passation.md` by their paths, never `git add -A`: `maquette — <Titre>`. Then the tasks, here: say
in one line that you go on, open `../cadrer-x-decouper/SKILL.md`, read it whole and follow it for this
feature. They stop you: `/cadrer-x-decouper <slug>` picks it up.

## Red flags

| Thought | Instead |
|---|---|
| "Le fichier CSV est généré à la demande." | What they see: « un fichier que mon tableur ouvre ». |
| "Keep data 12 months: US5." | A scenario or an exigence of the story it touches. |
| "« Leurs ateliers » surely means all of them." | A reading of a rule is a question, never Supposé. |
| "One page shows the main state; the rest is in passation.md." | Every state clickable: a section and an address. |
| "The design system lacks this colour; I'll add it to styles.css." | The copy is never edited: a token, or a Nouveauté. |
| "I'll open the page with `file://`." | Serve the folder on 127.0.0.1, then stop it. |
| "The prototype changed the button's word; the spec can stay." | The spec quotes it: change it too. |
| "The prototype is saved; they'll type the next command." | Go on with the tasks here, unless they stop you. |
