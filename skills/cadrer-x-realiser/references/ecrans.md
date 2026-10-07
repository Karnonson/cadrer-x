# Judging a story's screens

Read when realiser names it (its *Reviews* says when). Findings go on the `### Spec` and
`### Règles` axes of `audit.md`, with the prefixes of `examen.md`.

**The sizes**, given here only: a page at 390 then 1280 wide; a terminal at 80 columns × 24 rows.

**The real entry.** Start the app as a person does, only here: `commands.dev` of `cadrer-x.yml`
(plain pages without it: `python3 -m http.server <port> --bind 127.0.0.1` in their folder), from the
feature's worktree on a free port (no other session's); wait until it answers; kill its pid when done.
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
3. Beside it, the maquette page the person approved: `{feature}/` served as plain pages (the command
   above, its own port, killed after), `maquette/<page>.html#<état>` at the same width; its state bar
   is not product.
4. Texts against `contenu.md` word for word; each field's label; Tab order; no sideways scroll at the
   narrow size (`document.documentElement.scrollWidth <= innerWidth`); no console error.
5. One screenshot per screen and width of its main state, `{feature}/captures/SC<n>-<largeur>.png`
   (`-<état>` added for a state worth showing apart).

Findings: a state the app lacks is partiel (`Bloquant :`); what a person would see missing or
different from the maquette, against its Nouveautés and `États :` (a background, a block's size
or place, a text's font or size, a motion, a state), is partiel too: `À corriger :`, like a text not
`contenu.md`'s, a field with no label, a focus that jumps, a tap target under the design system's
size, sideways scroll; a token's name or a raw value in its place, the CSS form, spacing: `Détail :`.
From the code, always, and all there is when screens could not be clicked: each `contenu.md` text in
the code (`grep -rn`), each state its code path, the project's own components used.

**A story run in a terminal**: the command its scenarios run (else `dev.run`, else the README's) in
a terminal of the size above, with a temporary home and data folders (never the person's own).
One that waits for keys: left open until its ready screen is drawn, then each scenario with the keys
a person presses. A command that prints and exits: for each scenario, its output at that width, exit
status and what it wrote in the temporary folders are the evidence. A crash, a line cut or
overlapping, a key that does nothing: a finding as above. What it drew or printed: an `Info :` line
of `### Spec`, as on the short path.

**The short path** (`voie : courte`, no `passation.md`): the page the box names, at both sizes. Do
the box's scenario there, check the rest of the page did not move, no console error, and save one
screenshot per width, `{feature}/captures/page-<largeur>.png`. What you saw: a `- Info :` line of
`### Spec` (no `Écrans :` line) with the two captures' paths; a gap is a finding as above. The page
not opened (browser held, no tool, no `commands.dev`): that `Info :` line says so and why; judge from
the code.
