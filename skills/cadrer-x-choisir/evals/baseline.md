# Baseline — cadrer-x-choisir, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-choisir --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, a two-page Next.js studio site with a French README (pnpm scripts for lint,
typecheck and test, a contact form sending through Brevo), no `proa.yml`, no `docs/`.

Prompt: « Les clients devraient pouvoir réserver un appel découverte depuis le site, payer un acompte de
50 € en réservant, recevoir un rappel la veille, et je veux un rapport mensuel du nombre d'appels devenus
des projets. »

Output: 43 s, nothing written. It read the repo, named the four capabilities, and recommended Cal.com or
Calendly with Stripe over building it. Then it ended on five numbered questions at once.

## What went wrong — what the skill must prevent

1. **Five questions in one message**: how a call becomes a project, what happens to the 50 €, email or
   text, the host, the report's format. The person has to answer a form, and later questions depend on
   earlier answers.
2. **No guess, no confidence** on any of them: the person invents every answer from scratch.
3. **Straight to the how.** Hosting, report format and channel are decisions for step 2; the idea
   itself (who, the problem, why now, a measure) was never asked.
4. **No word on the project setup**: no project file, no vision, and no offer of `/cadrer-x-init`.
5. **"Je comparerai… avant de coder l'intégration"**: it was heading for code, with no file that
   records what was decided.

What held without the skill: French throughout, no question about what the repo shows, the bundle of
capabilities spotted, an existing product put forward.
