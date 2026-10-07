# Judging a story's screens

Read when `passation.md` gives the story a screen, on the short path when a box names a page, or for
a terminal app (`commands.dev` with no `url`). Findings go on the `### Spec` and `### Règles` axes of
`audit.md`, with the prefixes of `examen.md`.

**The sizes**, given here only: a page at 390 then 1280 wide; a terminal at 80 columns × 24 rows.

**The real entry.** Start the app as a person does, only here: `commands.dev` of `cadrer-x.yml`
(plain pages without it: `python3 -m http.server <port> --bind 127.0.0.1` in their folder), from the
feature's worktree on a free port (no other session's); wait until it answers; stop it when done.
Open its first page and go by its links and buttons to each screen, until it is ready (its data in,
nothing loading), never a file or a part opened alone. The browser tool already held (another
session): say so in one line, judge from the code (below), write `Écrans : pas cliqués — navigateur
occupé`. Never write your own browser driver. Never install, never edit a file or environment
variable to get in, never create an account in an outside service. Behind a sign-in: a way in the
project documents (a test member in its README), else the screen goes under `### Non jugé`.

For each screen, at each size:

1. Reach each state its `États :` line names the way a person would (type, send, open, come back). A
   state you cannot cause from the page: `### Non jugé`, with why.
2. Do each scenario of the story on the screen: it works, or it is a Spec finding.
3. Texts against `contenu.md` word for word; each field's label; Tab order; no sideways scroll at the
   narrow size (`document.documentElement.scrollWidth <= innerWidth`); no console error.
4. One screenshot per screen and width of its main state, `{feature}/captures/SC<n>-<largeur>.png`
   (`-<état>` added for a state worth showing apart).

Findings: a state the app lacks is partiel (`Bloquant :`); a text not `contenu.md`'s word for word, a
field with no label, a focus that jumps, a tap target under the design system's size, sideways scroll:
`À corriger :`; a raw colour or size where a token holds it, a part neither the design system's nor
a **Nouveauté** of `passation.md`, spacing: `Détail :`. From the code, always, and all there is when
screens could not be clicked: each `contenu.md` text in the code (`grep -rn`), each state its code
path, the project's own components used.

**A terminal app**: `dev.run` (else the README's command) in a terminal of the size above, with a
temporary home and data folders (never the person's own files). One that waits for keys: left open
until its ready screen is drawn (a run that quits first proves nothing), then each scenario with the
keys a person presses. A command that prints and exits: for each scenario, its output at that width,
its exit status and what it wrote in the temporary folders are the evidence. A crash, a line cut or
overlapping, a key that does nothing: a finding as above. What it drew or printed: an `Info :` line
of `### Spec`, as on the short path.

**The short path** (`voie : courte`, no `passation.md`): the page the box names, at both sizes. Do
the box's scenario there, check the rest of the page did not move and the console has no error, and
save one screenshot per width, `{feature}/captures/page-<largeur>.png`. No `Écrans :` line in
`audit.md`: what you saw goes in a `- Info :` line of `### Spec`, with the two captures' paths, a gap
in a finding as above. The page not opened (the browser held, no tool, no `commands.dev`): that
`Info :` line says so and why, never left out, and you judge from the code.
