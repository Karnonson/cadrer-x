# The design — every screen, clicked before any code

Followed by the designer `choisir` starts (its message says *Launched by choisir* and names the
stage), or by choisir itself with no subagents. `templates/` and `scripts/` below are choisir's,
beside `references/`. Three stages: the `wireframe`, while the spec is written; the `haute
fidélité`, once the spec is approved; the `passation`, once the person approved the design. The
builders build from it later, without you: `passation.md` tells them what each screen is.

**Launched by choisir.** You never ask the person and never commit: they are not here. What you
would ask goes in your report, and your last message is that report (the end of this file). Resumed
with a correction, or started on pages already there: read `maquette/` and `contenu.md` again first
(the person's own edits may be in), and change only what is asked. Not launched: you are choisir;
ask the person directly, and go on with its *Workers* where the report would be.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open
`<skills folder>/cadrer-x-<name>/aide.md` (the folder that holds `cadrer-x-choisir/`) at that moment;
read it whole and follow it. Not there: go on without it.

**Read:** `{feature}/idee.md`, `{feature}/spec.md` (each story a person sees is a screen, or a state
of one; its scenarios are what the screen must let them do and see), `{feature}/decisions.md` (the
look and the real content they gave), `{docs}/constitution.md`. From the `haute fidélité` on: **the
look**, read `cadrer-x-design-system`; **the words**, read `cadrer-x-textes`; in French, at least:
the product's *tu* or *vous*, its own words, a space before `: ; ! ?` and inside `« »`.

## The pages, in `{feature}/maquette/`

- **The wireframe** is the flow, to judge with the spec: every screen the draft implies, its states
  and the moves between them, the template's neutral `styles.css`, the spec's words. No `contenu.md`
  yet. The spec is being written meanwhile: never edit it; a flow that differs is in your report.
- **The `haute fidélité`** replaces it: the final look and the real words, as the person will see
  them. Its first version is the feature's, whole: every tone and motion the decisions and the spec
  name (animations, a playful tone, emoji) is in it already; a page that plays it safe costs a round.

Both:
- **Self-contained.** `maquette/styles.css`: the template's for the wireframe; then the design
  system's, copied byte for byte (`cp`, never edited), or with none the look you propose. No script
  or stylesheet from another site, no build step: the folder alone opens every page. A font the look
  needs is copied into `maquette/fonts/` (a `.woff2` its licence lets you copy) and declared in the
  page's `<style>`.
- **One plain `.html` page per screen**, from `templates/maquette/page.html`: `lang` the person's
  language, `href="styles.css"`, `src="maquette.js"` (`templates/maquette/maquette.js`, copied as is).
- **Only the stylesheet's tokens and parts.** A part it lacks is built from its tokens in the page's
  `<style>`, and listed in `passation.md` → **Nouveautés**. No raw colour or size.
- **Every state reachable.** Each state the stories imply (before anything, the ordinary result,
  nothing found, an error, too long, done) is a `<section data-state="<name>">`, shown by its address
  (`recherche.html#erreur`) and by clicking; the page's own controls move between states (sending the
  form shows the result) with `data-goto="<state>"`. The bar `<nav class="maquette-etats">` links
  every state; it and `maquette.js` are the prototype's own, never product code. Pages link to each
  other as the real screens will.
- **Their own content** where `decisions.md` gives it (their name, address, photos, copied into
  `maquette/`); else invented, plausible data, never a real person's, and no more of a person's own
  data than the screen needs (a first name, not an email address). A screen that collects personal
  data says what for, and asks for consent, never pre-ticked, when **Données et risques** gives
  consent as the basis.
- **Every text a person reads**, from the `haute fidélité` on, is also in `{feature}/contenu.md`
  (from `templates/contenu.md`), word for word, by screen and state; a number that varies has each
  form.

**Check it in a browser, at 390 and 1280 wide.** Serve the folder on this machine only. A server
your message or your last round names is reused. Else first stop any left serving this folder by an
earlier session (`pgrep -af 'http.server.*{feature}/maquette'`, then `kill` each), and start
one in the background; choisir stops it later:

```
port=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])') && (python3 -m http.server "$port" --bind 127.0.0.1 --directory {feature}/maquette >/dev/null 2>&1 & echo "port $port pid $!")
```

With a browser tool, for each page and state (`http://127.0.0.1:<port>/<page>.html#<state>`), at
390×844 and 1280×800: each text is `contenu.md`'s (once there is one), each field has a label, Tab
walks a sensible order; `document.documentElement.scrollWidth <= innerWidth`; no console error; each
link and control goes where its story says. Look at each screenshot as the person will see it: the
whole page at that width, not only what you changed. None goes in the repo. Fix what fails, and
check again. No browser tool: say so, and never call the pages checked.

**A correction.** A layout fix changes only the block asked about. A change that alters a word or a
number a scenario of `spec.md` quotes changes the spec too, from the `haute fidélité` on, its lint
run again (`python3 <this skill's folder>/scripts/lint.py spec {feature}/spec.md`). A value you made
up for the page (points, a limit, a delay) that no file settles is a question. A correction to the
words: read `cadrer-x-textes` (it offers to keep the rule).

## The passation

Once the person approved the design: write `{feature}/passation.md` from `templates/passation.md`:
one screen per page, `SC1`, `SC2`… with no gap (a screen keeps its id across revisions; a new one
takes the next number), each line on one line, since a task's builder quotes its screen's section
word for word. Check it against its **Contrôle** list, reading the pages themselves; what fails
changes the pages or the file. Run `python3 <this skill's folder>/scripts/lint.py passation
{feature}/passation.md` until it prints nothing.

## The report

Your last message, in the person's language, these labels as written; a section with nothing says
`aucun`:

```
Étape : wireframe | haute fidélité | passation
Adresse : http://127.0.0.1:<port>/<page>.html, pid <pid> (or: arrêtée)
Écrans :
- <page> — <its states> — <where each control leads>
Changé : <what changed since your last report, spec.md included; or: tout>
Fichiers : <every path you wrote, a helper's too ({docs}/regles-ecriture.md)>
Vérifié : <each page and state at 390 and 1280; or what was not checked, and why>
Questions :
- <the question, in plain words, never a file or code> — Conseil : <your recommendation, why>
```

## Red flags

| Thought | Instead |
|---|---|
| "One page shows the main state; the rest is in passation.md." | Every state clickable: a section and an address. |
| "The design system lacks this colour; I'll add it to styles.css." | The copy is never edited: a token, or a Nouveauté. |
| "I'll open the page with `file://`." | Serve the folder on 127.0.0.1. |
| "The design changed the button's word; the spec can stay." | The spec quotes it: change it too. |
