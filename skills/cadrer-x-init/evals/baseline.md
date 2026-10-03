# Baseline — cadrer-x-init, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-init --engine claude
--baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, a repo holding only a French README (the book club app of a media library,
nothing built yet).

Prompt: « Une appli où les 30 membres du club votent chaque mois pour le prochain livre, et où on voit
l'historique des livres lus. »

Output: 31 s, nothing written.

## What went wrong — what the skill must prevent

1. **Five questions at once**: the login method, how books are put forward, how the vote works, what the
   history shows, the hosting. Later answers depend on earlier ones.
2. **Proposals with no confidence**: "je propose…" on each, never how sure, never what it rests on.
3. **No look at what exists.** A vote among 30 people each month is what Framadate, a form or a shared
   spreadsheet already do; building or using was never asked.
4. **Heading for the build**: "je commence par un document de cadrage dans le dépôt", before who it is for,
   the problem or success were settled.

What held without the skill: French throughout.
