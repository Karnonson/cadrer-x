# Baseline — cadrer-x-verifier, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-verifier --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, the pottery club on `feature/inscription-ateliers`, a validated spec and its
`taches.md`, nothing built. Both lints pass. Planted, beyond what they can see: US3 « elle s'affiche
rapidement » (no measure), copied into a T03 box; T02's box says 48 hours where the scenario says 24;
T02's `Risques :` is « aucun » while `decisions.md` names cancelling another member's sign-up as an
abuse; US2 says « réservation », which **Mots** forbids; and EF4 (« seuls les animateurs ») against M3
(« leurs ateliers »), already in the fixture.

Prompt: « inscription-ateliers, un second regard avant de coder ? »

Output: 84 s. A thorough read: all five planted faults found, plus real extras (re-signing up after a
cancellation hits the UNIQUE constraint, no task deletes after 12 months). Then:

## What went wrong — what the skill must prevent

1. **No file**: the findings lived in the chat; affiner and decouper would have nothing to fold in.
2. **No owner per finding**: thirteen points under « À régler », « Erreurs », « Pièges techniques »,
   none naming the step that fixes it.
3. **Out of its lane**: the « Pièges techniques » section designs T01's transaction and T02's datetime
   handling, the builder's work; and it held the existing failing workshops test against the plan.
4. **Offered to fix it itself**: « Je peux corriger les docs et le tri maintenant si tu veux. »

What held: nothing edited, nothing committed.

## With the skill (first run)

Every check and judge line passed: `verification.md` committed alone (`vérification — …`), « Portée :
spec et tâches », verdict « à reprendre », five `À reprendre :` each ending on its step
(`→ /cadrer-x-affiner` or `→ /cadrer-x-decouper`), eleven remarks, `## Vérifié` listing what held; the
reply named the next step and changed nothing else.
