# The spec — what the person approves before any how

Followed by `choisir` when its *Which step* finds the spec open. `templates/` and `scripts/` below are
choisir's, beside `references/`.

You turn the feature's idea and decisions into what the person approves before any *how*: the spec
(what each person does and sees). It ends in files on the feature's branch: `spec.md`, with
`a-trancher.md` for what is left to decide. No tasks, no code: the tasks are cut from your files, and
the builders build from them without you.

Talk, and write the files' text, in the person's language, every message included (the short notes between steps too); in French, *tu* or *vous* as they write,
*vous* when you can't tell, and never both. File names, headings, labels and ids stay exactly as
written here and in the templates, in every language: the later skills find them by these names.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open
`<skills folder>/cadrer-x-<name>/aide.md` (the folder that holds `cadrer-x-choisir/`) at that moment;
read it whole and follow it. Not there: go on without it.

## Every turn

- **One question per message**, the one that changes the most, with your recommendation a plain
  "oui" accepts. One question has one thing to answer: never two asks joined by "and" or "or".
  Questions that hang on nothing still open may go out together, numbered, each with its
  recommendation: they answer in one message.

## The spec

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
`spec — <Titre>`. The spec is done: say in one line that you go on with the next stage, and go back
to choisir's *Which step*. They stop you: `/cadrer-x-choisir <slug>` picks it up.

## Red flags

| Thought | Instead |
|---|---|
| "Le fichier CSV est généré à la demande." | What they see: « un fichier que mon tableur ouvre ». |
| "Keep data 12 months: US5." | A scenario or an exigence of the story it touches. |
| "« Leurs ateliers » surely means all of them." | A reading of a rule is a question, never Supposé. |
