# The prototype — every screen, clicked before any code

Followed by `choisir` when its *Which step* finds the prototype open: a validated spec, with
screens. `templates/` and `scripts/` below are choisir's, beside `references/`.

A clickable mock-up of every screen the spec implies, made of plain pages, to judge before any code.
The builders build from it later, without you: `passation.md` tells them what each screen is.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open
`<skills folder>/cadrer-x-<name>/aide.md` (the folder that holds `cadrer-x-choisir/`) at that moment;
read it whole and follow it. Not there: go on without it.

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
there: `claude-design.md`, which choisir named. Each change is made in the pages and `contenu.md`,
checked again, and they are asked again, until a clear yes. A change that alters a word or a number
a scenario of `spec.md` quotes changes the spec too, in the same commit, its lint run again. A value
you made up for the page (points, a limit, a delay) that no file settles is a question before the save. A
correction to the words: read `cadrer-x-textes` (it offers to keep the rule).

**Save — only after the yes.** `kill <pid>`. Write `{feature}/passation.md` from
`templates/passation.md`: one screen per page, `SC1`, `SC2`… with no gap (a screen keeps its id
across revisions; a new one takes the next number), each line on one line, since a task's builder
quotes its screen's section word for word. Check it against its **Contrôle** list, reading the pages
themselves; what fails changes the pages or the file. Run `python3 <this skill's folder>/scripts/lint.py
passation {feature}/passation.md` until it prints nothing. Commit `maquette/`, `contenu.md`,
`passation.md` by their paths, never `git add -A`: `maquette — <Titre>`. The prototype is done: say
in one line that you go on with the tasks, and go back to choisir's *Which step*. They stop you:
`/cadrer-x-choisir <slug>` picks it up.

## Red flags

| Thought | Instead |
|---|---|
| "One page shows the main state; the rest is in passation.md." | Every state clickable: a section and an address. |
| "The design system lacks this colour; I'll add it to styles.css." | The copy is never edited: a token, or a Nouveauté. |
| "I'll open the page with `file://`." | Serve the folder on 127.0.0.1, then stop it. |
| "The prototype changed the button's word; the spec can stay." | The spec quotes it: change it too. |
| "The prototype is saved; they'll type the next command." | Go on with the tasks here, unless they stop you. |
