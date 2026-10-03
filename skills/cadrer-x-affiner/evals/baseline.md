# Baseline — cadrer-x-affiner, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-affiner --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, the pottery club (Python, standard library), checked out on
`feature/inscription-ateliers`, whose folder holds the feature's `idee.md` and `decisions.md` in
cadrer-x's French layout (`écrans : oui`). The idea leaves open whether a member may sign up a spouse
with no account.

Prompt: « inscription-ateliers : on passe à la spec. »

Output: 269 s. A spec of five stories, plain in its wording, with the spouse question parked and a
recommendation. It caught two real gaps the fixture holds: the product has no way to sign in yet, and
the constitution's « leurs ateliers » (M3) does not say who runs a workshop. Then:

## What went wrong — what the skill must prevent

1. **Committed without a yes.** The spec went straight onto the feature branch (`fbe2cee`): the person
   never approved what gets built.
2. **Four questions at once**, plus a fifth about the tooling, in one message: the person answers a
   form, and Q2 depends on Q1.
3. **Its own file names**: `questions-ouvertes.md` and `arbitrages.md` instead of `a-trancher.md`, and
   headings no later skill finds by name. It tried fleet's English lint, failed it, and asked the person
   to pick between English headings and a new lint: a question only a developer could answer.
4. **No status**: nothing tells a reader the spec is a draft still to approve.
5. **Stories summed up in three or four sentences each**, and one story (« Être reconnu sans mot de
   passe ») is a how, not something a member asked for.

What held without the skill: French and a consistent « vous », plain scenarios, nothing invented, the
spouse question parked with a recommendation, the decisions all landing.
