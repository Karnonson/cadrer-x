# examiner — judging a story's screens

Read when `passation.md` gives the story a screen, or on the short path when a box names a page. Findings go on the `### Spec` and `### Règles` axes of `audit.md`, with the prefixes of `SKILL.md`.

The browser tool already held (another session): say so in
one line, judge from the code (below), write `Écrans : pas cliqués — navigateur occupé`. Never write
your own browser driver. You may start the app, only here: `commands.dev` of `cadrer-x.yml` and a
browser tool, from the feature's worktree on a free port (no other session's), wait until it answers,
stop it when done. Never install, never edit a file or environment variable to get in, never create an
account in an outside service. Behind a sign-in: a way in the project documents (a test member in its
README), else the screen goes under `### Non jugé`.

For each screen, at 390 then 1280 wide:

1. Reach each state its `États :` line names the way a person would (type, send, open, come back). A
   state you cannot cause from the page: `### Non jugé`, with why.
2. Do each scenario of the story on the screen: it works, or it is a Spec finding.
3. Texts against `contenu.md` word for word; each field's label; Tab order; no sideways scroll at 390
   (`document.documentElement.scrollWidth <= innerWidth`); no console error.
4. One screenshot per screen and width of its main state, `{feature}/captures/SC<n>-<largeur>.png`
   (`-<état>` added for a state worth showing apart).

Findings: a state the app lacks is partiel (`Bloquant :`); a text not `contenu.md`'s word for word, a
raw colour or size where a token holds it, a part neither the design system's nor a **Nouveauté** of
`passation.md`, a field with no label, a focus that jumps, a tap target under the design system's size,
sideways scroll at 390: `À corriger :`; spacing changing nothing a person can do: `Détail :`. From the
code, always, and all there is when screens could not be clicked: each `contenu.md` text in the code
(`grep -rn`), each state its code path, the project's own components used.

**The short path** (`voie : courte`, no `passation.md`): the page the box names, at 390 then 1280. Do
the box's scenario there, check the rest of the page did not move and the console has no error, and
save one screenshot per width, `{feature}/captures/page-<largeur>.png`. No `Écrans :` line in
`audit.md`: what you saw goes in a `- Info :` line of `### Spec`, with the two captures' paths, a gap
in a finding as above. The page not opened (the browser held, no tool, no `commands.dev`): that
`Info :` line says so and why, never left out, and you judge from the code.
