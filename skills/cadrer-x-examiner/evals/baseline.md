# Baseline — cadrer-x-examiner, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-examiner --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, the pottery club on `feature/inscription-ateliers`, with T01 (US1) built and
ticked. Planted in it: `taken > seats` lets one member more than the seats in (EF1), and the full-workshop
test starts from an already overbooked workshop, so it cannot see it; the count and the insert are not
in one transaction, and the race test signs up one after the other; `_member_exists` reads the members
table directly (M6); `my_sign_ups`, which no scenario asks for. A workshops test already fails, not US1's.

The harness commits a fixture as one commit, so `main` and the feature branch are the same commit: the
skill reviews the story's tasks' `Fichiers :`, and the history check (a test loosened in a later commit)
is not exercised here.

Prompt: « US1 inscription-ateliers, tu peux relire ? »

Output: 92 s. A sharp review: it found the off-by-one and why the test hides it, the missing transaction
(reproduced with two connections), M6, `my_sign_ups`, and a real extra: signing up again after a
cancellation hits the UNIQUE constraint. Then:

## What went wrong — what the skill must prevent

1. **No audit.md**: the review lived only in the chat; realiser's fix round and rendre would have nothing
   to read.
2. **Held the wrong things against the story**: the workshops test failing (not US1's) as « Bloquant »,
   and `docs/security/data-inventory.md` missing as a broken M4, which is rendre's, at ship time.
3. **The wrong next step**: « à reprendre dans une session `/cadrer-x-realiser T01` », a task already
   ticked; there is no fix round on a story without an audit to read.
4. **Offered to fix it itself**: « veux-tu que j'enchaîne sur les corrections ? » — the reviewer would then
   build what it judged.
5. No severity scheme the next skill can read (« Bloquant / À corriger avant US2 / Mineur », in headings).

What held without the skill: the code left untouched, nothing committed or pushed, French throughout.

## With the skill (first run)

Every check and judge line passed: `audit.md` with the story's section, Spec and Règles axes, each
finding prefixed and typed, `Vérifs : lancées`; the off-by-one proven with `>` and `>=` against the test;
the workshops failure under Non jugé as not US1's; `my_sign_ups` as a question to the person; committed
as `audit US1 — à corriger`; next step `/cadrer-x-realiser US1`, in a new session.
