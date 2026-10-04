# Baseline — cadrer-x-decouper, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-decouper --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, Carnet (Next.js, Turso, Better Auth, vitest), checked out on
`feature/recherche-notes`, whose folder holds a validated `spec.md` (two stories, five exigences), its
`passation.md` (SC1 Recherche, SC2 Note), `contenu.md` and `maquette/`. `decisions.md` relies on a rate
limit "already in place" that the code does not have.

Prompt: « recherche-notes : on découpe. »

Output: 296 s. Seven tranches, thin and end to end, on the module map, each with a risk line; it caught
the missing rate limit and the token names that differ between the prototype and the app. Then:

## What went wrong — what the skill must prevent

1. **Committed without a yes** (`324f4fa`), then asked whether the order suits them.
2. **Its own names**: `tranches.md`, ids `S01`, a `Points de relecture` section: `realiser`,
   `examiner` and `rendre` would find none of them. It tried fleet's English lint, failed it, and
   checked the coverage by hand.
3. **Four questions at once**, and a tranche (« un lien vers la recherche ») built before the person
   said yes to it.
4. **No `[P]`, no waves**: only "S01 and S04 can start together" in prose; the person running parallel
   sessions has to work out the rest from the `Après` column.
5. **Scenarios split by hand-made judgement**: the US2 tranches cut « introuvable » into a tranche of its
   own (S05), apart from the page that shows it.

What held without the skill: French and a consistent « tu », tracer bullets, files on the Modules map,
threats with protections, no layer-only task.

## With the skill (first run)

`taches.md` passed the lint, nothing committed, the tasks in a table with `[P]`, five waves, five À
surveiller lines, one question (the missing rate limit) with a recommendation. One judge line failed:
two Fondations tasks repair the fixture's tooling (no `tsconfig.json`, no vitest config, no
`shared-db` module), which the judge read as out of scope. The fixture was missing them for real: it
now has them, and the judge line allows tooling the project's checks need.
