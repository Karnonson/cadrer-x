# cadrer-x direction — a look made for this product, not for any product

Adapted from Anthropic's frontend-design skill (Apache-2.0, `LICENSE-frontend-design.txt` beside
this file), modified for cadrer-x.

Read by `choisir`'s designer at the `haute fidélité` only: how to make the look you propose, and
the parts you add (Nouveautés), distinct and well made. Make deliberate choices for this product,
and take an aesthetic risk when the brief justifies it.

**What wins.** The person's own words in `{feature}/decisions.md` (a colour, a font, a site they
like, a look they asked for, even one of the defaults below) are followed exactly. A design system,
or the look the app's screens already have, wins over everything here: then this file shapes only
the Nouveautés, inside its tokens. Where they leave a choice free, don't spend it on a default.

## The subject first

The look comes from what the product is about: its trade, its materials, its words, the people it
serves. A booking page for a climbing gym and a tool for accountants look nothing alike. Before
designing, name in one line the subject, who it is for and the screen's main job, from `brief.md`
and `decisions.md`; never ask the person (a doubt goes under your report's Questions). Use their
real content throughout.

The top of the main screen shows the most characteristic thing in their world, in the form that
fits it: a headline, a photo, a live example, a moment of interaction. A big number with a small
label and a gradient is the default; use it only when it truly is the best.

## Type

Typography carries the page's personality.
- Faces chosen for this product, never the families you would reach for on any project. One family
  or two; two clearly different.
- A type scale with deliberate weights, widths and spacing, after *The Elements of Typographic
  Style*. A headline's type is part of the design, not a neutral carrier.
- Lines under 80 characters; serif body text gets a little more line height than sans.
- An open-licence face (as on Google Fonts) is the normal way, downloaded once so the folder stays
  self-contained: each weight's `.woff2` into `maquette/fonts/`, from
  `https://cdn.jsdelivr.net/fontsource/fonts/<id>@latest/latin-<weight>-normal.woff2` (`<id>`: the
  family in lowercase, hyphens for spaces; `latin` holds French; `-italic` for italics), and its
  licence beside it, from its folder in `github.com/google/fonts` (`ofl/<name>/OFL.txt`,
  `apache/<name>/LICENSE.txt` or `ufl/<name>/UFL.txt`, the name without hyphens). Each font file
  must be real (`file` says Web Open Font Format (Version 2)), its licence must have answered with
  its text; else another open face, or the closest system face, said in your report.

## Structure

Visual structure is information: a border, a number, a label or a divider says something about the
content, or it goes. Hierarchy comes from size, weight, space and position before boxes. Space
groups what belongs together and separates what does not, on one spacing scale. An image is theirs
(`decisions.md`) or none: with no photo, the layout holds with type, colour or a pattern made in
CSS; a placeholder looks like one and is in your Questions.

## The defaults that give a generated page away

Generated pages cluster around these. Each is right for some brief, but none is a choice when it
appears whatever the subject:
1. A warm cream background (near `#F4F1EA`), a high-contrast serif display, a terracotta or clay
   accent (near `#D97757`).
2. A near-black background with one acid-green or vermilion accent.
3. A broadsheet: hairline rules, no radius, dense newspaper columns.
4. The SaaS-card kit: content cut into identical rounded cards, one radius on everything, the same
   soft grey shadow under each, gradient washes as decoration.
5. Template chrome: a tracked-out all-caps label above every heading; details joined by middle dots
   (A · B · C); labels as « MOT — fragment »; a near-black like `#111` standing in for black; a
   monospace face for small data; a `→` after link and button text.
6. One word of a headline set apart (italic, bold, another colour); all caps for labels; a label
   above content that needs none.
7. Numbered markers (01 / 02 / 03) on content that is not a sequence (steps, a timeline).
8. Motion everywhere: each section fading and sliding up, a hover effect on every card. One
   orchestrated moment (the page's arrival, one reveal) lands better. Motion that answers an action
   (opening, confirming) and shows what changed is welcome; `prefers-reduced-motion` turns it off.

## Three pistes, when the look is yours

At the first design only (no `passation.md` yet), with no design system, no screens in the app yet
and no pick recorded (no `/* Piste choisie :` comment at the top of `maquette/styles.css`), the
`haute fidélité` starts here, unless the person's words in `decisions.md` already settle the look
whole. Make the main screen in three clearly different looks, each its own page,
`maquette/piste-1.html` to `piste-3.html`, its look whole in its `<style>` (its tokens declared
there: the one place a raw value lives), its plan (below), reviewed, in a comment at the top.
Three variations of one idea are one piste. Your report lists them under `Pistes :`, each with its
address and one plain line on what it feels like, never a hex value or a font name. Then stop:
nothing else is built before their pick. Started again on the pages with no word from the person:
report them again as they are. A correction (none fits, or what they want instead) revises the
pistes, and you wait for a pick again.

Their pick (one piste, or parts of several): first write its plan, resolved, with their pick in
their words, as the comment at the top of `maquette/styles.css`, starting `/* Piste choisie :`, and
its tokens there: that is the record of the pick. Then delete the piste pages (any left once that
comment exists too), and build the whole `haute fidélité` from it, as from any recorded pick. A
piste page is never in your report's `Fichiers :`.

## Plan, review, build, critique

1. **Plan** the look in a few lines: the palette as 4 to 6 named hex values; the typefaces and their
   roles; the layout idea in one sentence (an ASCII sketch helps compare), with its alignment; the
   one memorable thing.
2. **Review the plan against the brief** before any code. A part you would produce for any similar
   page (run a similar brief in your head: same answer?) is a default: revise it, and keep one line
   on what changed and why.
3. **Build** from the revised plan. Keep selectors from cancelling each other: a section's padding
   against a button's margin is the usual one.
4. **Critique** before the report, on your screenshots at both widths: each page against the
   defaults above and against its plan (the picked piste's, or each piste's own). Fix what reads as
   a default or strays from the plan, look again, and say under `Retouches :` what you changed.

## Restraint

Spend your boldness in one place: one memorable thing, everything around it quiet and disciplined.
Cut decoration the brief does not need; before the report, remove one accessory. Beyond the page
checks you already run: the focus ring stays visible in your colours, text contrast is at least
4.5:1, the palette holds together.
