# cadrer-x design system — find it, read it, never edit it

Loaded by `affiner` (the prototype), `realiser` (a task with screens) and `examiner` (the screens'
review). The design system is the one source of a product's look: its
tokens (every colour, font, size and space) and its parts (a button, a field, a card). A screen that
invents a colour or a part drifts from the rest of the product, and nobody sees it until it ships.

## 1. Find it

The first that answers:

1. `cadrer-x.yml` → `design_system:`, a path relative to the repo's top in the **main checkout**, never
   to your worktree: `top=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)"); ls
   "$top/<path>"`.
2. `{docs}/design-system/`.
3. None: section 5.

## 2. Read it, before anything

- Its stylesheet's tokens (`:root` custom properties): colours, fonts, sizes, spaces, radii, shadows, the
  smallest tap size.
- Its parts: the classes or components, with their variants and states.
- Its rules (the readme): contrast, the focus ring, what never to do. Its gallery page shows each part.
- In code, the project's own copy of it: the tokens file and the shared components that
  `{docs}/architecture.md` → **Modules** names. Their names may differ from the design system's. Map
  each token you need by value and role (the design system's `--color-accent-soft: #fbeee6` is the
  app's `--wash: #fbeee6`), and write the mapping once (a `Choix :` line), so the next task reuses it.

## 3. Use only it

- **Every colour, font, size, space, radius and shadow is a token** (`var(--wash)`), never a raw value
  (`#fbeee6`, `rgb(…)`, `14px` for a text size a token holds), also when the prototype or a screenshot
  shows the raw value. A design-system token name the app does not define renders nothing in the app.
- **Every part comes from it.** In a prototype: its classes. In code: the project's components
  (`<Field>`, `<Button>`, `<Card>`, `<Alert>`), never the prototype's classes and never a copy of its
  stylesheet in the app.
- **A value no token holds**: the nearest token, said once.
- **A part it lacks**: built from tokens in the feature's own files (a prototype page's `<style>`; in code,
  the task's module), never in the design system or the shared components. `affiner` lists it in
  `passation.md` → **Nouveautés**; a builder names it in the commit.

## 4. Never edit it

Not its stylesheet, readme or gallery; in code, not the shared tokens file or the shared components;
not "just one token", not when a task's `Fichiers :` names it. A change it needs (a missing colour, a token
that fails contrast, a part every feature will want) is a question to the person, with your
recommendation, in `{feature}/a-trancher.md`. A prototype's copy of the stylesheet is the design system
too: copied byte for byte, never edited.

## 5. No design system yet

- **`affiner`'s prototype**: the app's own tokens file and components when it has screens already;
  none: `../cadrer-x-affiner/templates/maquette/styles.css`, a plain neutral one, and say once that the look is
  the prototype's, not a brand. No step makes a design system on its own.
- **The person asks for one, in any step**: that step makes `{docs}/design-system/` from what the product already has, never
  from taste. `styles.css`: the tokens under `:root` with the values the
  product uses today (its tokens file, its global stylesheet, the colours its components repeat), one
  class per part it already has. `readme.md`: the tokens, a table of parts (part, classes, component in
  the code), the rules. A product with no styles at all: tokens only, the fewest that make a readable
  page, and ask the person for their brand (colours, a font), one question.
- **A builder**: use the project's existing tokens and components; never make a design system.

## Red flags

| Thought | Instead |
|---|---|
| "The prototype says `var(--color-accent-soft)`; I'll paste it." | Map it to the app's token that holds that value. |
| "Used once, a hex is fine." | A token, or the nearest one, said once. |
| "The design system lacks a badge; I'll add it." | Build it in the feature; list it under Nouveautés. |
| "I'll copy the prototype's styles.css into the app." | The app has its own tokens and components. |
| "No design system: I'll pick nice colours." | From what the product already uses, or ask. |
