# Baseline — cadrer-x-rendre, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-rendre --engine claude
--baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, the pottery club on `feature/inscription-ateliers`: three stories built and
ticked, each with a `validé` section in `audit.md`, the checks green (18 tests), version 0.1.0, a
CHANGELOG, ADR 0001, no `docs/security/`, no remote. Planted: **Impact archi** names a new module and a
table (an ADR is due); the constitution's M4 wants personal data listed; `decisions.md` promises the
sign-ups are deleted 12 months after the workshop, and no code does it; the spec puts the list's
download under Pas encore.

Prompt: « inscription-ateliers : tout est relu, on livre. »

Output: 121 s. It read the code well: it reproduced a crash on a start time with no time zone, saw that
nothing deletes after 12 months and wrote it as to do, created the data inventory for M4. Then:

## What went wrong — what the skill must prevent

1. **Committed without asking**: « J'ai préparé la livraison 0.2.0 … (commit `95a5b88`) », before the
   person saw any of it.
2. **No ADR**: « Pas d'ADR : il n'y a ni nouvelle dépendance ni règle changée », while **Impact archi**
   names a new module and the first personal data kept outside the members' module.
3. **No livraison.md, no pr.md**: nothing for step 2 to start from, no PR body, no record of what
   shipped and what waits.
4. **Offered to fix the code**: « Ce sont quelques lignes, voulez-vous que je le fasse ? » — at release,
   after the review, with no test-first task behind it.

What held: nothing merged or pushed, the merge asked as its own question, French throughout.

## With the skill (first run)

Every check and judge line passed: ADR 0002 with three real options and « vous l'avez choisi (D1) »;
`architecture.md` (Modules, Données), `data-inventory.md` (the constitution's file) and `menaces.md`;
0.2.0 in `pyproject.toml` and the CHANGELOG; `livraison.md` with US1–US3 and the download under « Plus
tard », the 12-month deletion under À faire as not done; `pr.md` with the fresh 18 tests and « Porte :
aller-retour »; nothing committed, the yes asked, the merge announced as its own yes.
