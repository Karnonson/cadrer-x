# cadrer-x conventions

2026-10-03. The fixed names every cadrer-x skill writes and reads. A skill finds another skill's
section by its exact heading, so these names never change once released, and they are never translated per
person. Later, fleet parses the same names.

## Rules

- **Language.** A skill's name and `description`: French. Its body (instructions to the model): English.
  What it says and the prose it writes: the person's language. File names, headings and labels below:
  French, as written here, for everyone.
- **Short.** A heading is one or two words. A label ends with ` :` (`Fichiers :`).
- **Ids stay ids.** `US1` (story), `SC1` (screen), `T01` (task), `Q1` (question), `EF1` (requirement), `CS1` (success criterion), `D1` (decision), `M4` (a rule of the constitution), `[P]` (a task that can be built at the same time as the one before it)
  are ids, not words: they are not translated.
- **Accents are part of the name.** `À surveiller`, not `A surveiller`.

## Layout

```
cadrer-x.yml                      project file: code, install, checks
docs/architecture.md              stack, runtime, Modules
docs/constitution.md
docs/adr/NNNN-<slug>.md
docs/features/NNNN-<slug>/
  idee.md  decisions.md  spec.md  a-trancher.md  taches.md
  maquette/  passation.md  textes.md
  verification.md  audit.md  livraison.md  pr.md  captures/
.worktrees/<branch with / as .>/
```

Branches and worktrees:

| What | Branch | Worktree | Merged into |
|---|---|---|---|
| project setup | `chore/cadrer-x-init` | `.worktrees/chore.cadrer-x-init` | the main branch, on the person's yes |
| a feature | `feature/<slug>` | `.worktrees/feature.<slug>` | the main branch, by `rendre` |
| a task | `tache/<slug>-t01` | `.worktrees/tache.<slug>-t01` | `feature/<slug>`, fast-forward, on the person's yes |
| a story's fixes | `tache/<slug>-us1-correctifs` | `.worktrees/tache.<slug>-us1-correctifs` | `feature/<slug>`, on the person's yes |

`.worktrees/` is in `.git/info/exclude`; untracked `.env*` files are copied into each worktree. A task's
branch first merges in what the feature gained meanwhile and runs the checks again, so the feature only
ever fast-forwards. A task commits as `T01 — <titre>`, with `Choix :` lines for what its builder decided
alone, and ticks its own `[x]` in `taches.md` in that commit. No skill pushes but `rendre`, and only on the person's yes.

| Proa today | cadrer (old) | cadrer-x |
|---|---|---|
| `proa.yml` | — | `cadrer-x.yml` |
| `docs/features/NNNN-<slug>/` | `builds/<NN>-<slug>/` | `docs/features/NNNN-<slug>/` |
| `idea.md` | `idee.md` | `idee.md` |
| `decisions.md` | `decisions.md` | `decisions.md` |
| `spec.md` | `spec.md` | `spec.md` |
| `open-questions.md` | `a-trancher.md` | `a-trancher.md` |
| `slices.md` | `tranches.md` | `taches.md` |
| `prototype/` | — | `maquette/` |
| `handoff.md` | — | `passation.md` |
| `copy.md` | — | `textes.md` |
| `review.md` | `audits/code.md` | `audit.md` |
| `release.md` | `livraison.md` | `livraison.md` |
| `pr.md` | — | `pr.md` |
| — (in `docs/architecture.md`) | `builds/…/architecture.md` | `docs/architecture.md` (one per project) |

## Headings by file

### idee.md

| Proa | cadrer-x |
|---|---|
| Problem | Problème |
| User | Pour qui |
| Why now | Pourquoi maintenant |
| Success measure | Mesure |
| Outcome | Résultat |
| Constraints | Contraintes |
| Existing options | Existant |
| Out of scope | Non couverts |
| Open | Ouvert |

### vision (`docs/vision.md`)

| Proa | cadrer-x |
|---|---|
| Who | Pour qui |
| Problem | Problème |
| Success | Succès |
| Build or use | Faire ou louer |

### decisions.md

| Proa | cadrer-x |
|---|---|
| Decisions | Décisions |
| Stages | Étapes |
| Clarifications | Précisions |
| Stack choices | Stack |
| Architecture impact | Impact archi |
| Data and risks | Données et risques |
| — | À faire (what the person sets up by hand, each marked avant la construction or avant la livraison) |

### spec.md

The template is `skills/cadrer-x-affiner/templates/spec.md`, adapted from spec-kit's (MIT).


| Proa | cadrer-x |
|---|---|
| User stories | Récits |
| `### US1 <title>` | `### US1 — <titre> (Priorité : P1)` |
| As a … I want … so that | En tant que … je veux … afin de |
| — (spec-kit) Why this priority / Independent Test / Acceptance Scenarios | Pourquoi cette priorité / Test seul / Scénarios |
| — (spec-kit) Given / When / Then | Étant donné / quand / alors |
| — (spec-kit) Edge Cases | `### Cas limites` |
| — (spec-kit) Functional Requirements, `FR-001` | `## Exigences`, `EF1` |
| — (spec-kit) Key Entities | `### Données clés` |
| — (spec-kit) `[NEEDS CLARIFICATION: …]` | `[À PRÉCISER : … → Q<n>]`, its question in `a-trancher.md` |
| Success criteria, `SC-001` (spec-kit) | `## Critères`, `CS1` (not `SC`: that is a screen) |
| — (spec-kit) Assumptions | `## Supposé` |
| Not yet | Pas encore |
| Requirements checklist | Vérifs (written by affiner itself; cadrer-x-verifier is the second, independent look) |
| — | `**Statut** : brouillon` while the person reads it, `validée` on their yes |

`skills/cadrer-x-affiner/scripts/lint.py spec|passation <path>` checks the form of both files.

### a-trancher.md (and Rulings / Noticed wherever they appear)

| Proa | cadrer-x |
|---|---|
| `## Q1 · spec · <question>` | `## Q1 · spec · <question>` (stage words stay: `spec`, `plan`, `build`) |
| options | Options |
| implications | Effets |
| recommended | Conseil |
| answer | Réponse |
| `## Rulings` | `## Arbitrages` |
| `## Noticed` | `## Remarqué` |
| `## Convergence` | `## Convergence` |

### taches.md

The template is `skills/cadrer-x-decouper/templates/taches.md`, adapted from spec-kit's tasks template
(MIT): tasks grouped by story, each story ending on a checkpoint where `examiner` reviews it.

| Proa / spec-kit | cadrer-x |
|---|---|
| `- [ ] S01 [P] [US1] <verb> <title>` / `T001` | `- [ ] T01 [P] [US1] <verbe> <titre>` |
| a done-when box | `- [ ] <fait quand>` (one spec scenario) |
| `Files:` | `Fichiers :` |
| `After:` | `Après :` (the tasks it builds on, or `aucune`) |
| `Screens:` | `Écrans :` |
| `Risks:` | `Risques :` |
| `Size:` | `Taille :` |
| — | `Exigences :` (the spec's `EF<n>` the task makes true) |
| spec-kit Phase 1–2: Setup, Foundational | `## Fondations` |
| spec-kit Phase 3+: User Story N | `## US1 — <titre> (Priorité : P1)`, with `**But**`, `**Test seul**`, `**Point d'étape**` |
| spec-kit Implementation Strategy | `## Ordre`, ending on the waves: `- Vague 1 : T01`, `- Vague 2 : T02, T03` (each wave the tasks the earlier waves unblock) |
| `## Review focus` | `## À surveiller` |
| `## Coverage` | `## Couverts` (rows: `US<n>`, `EF<n>`, constitution rules `M<n>`) |
| `MUSTs to own:` | dropped: each constitution rule a task handles is its own `M<n>` row under `## Couverts` |
| `MUST conflicts:` | `Règles en conflit :` |

`[P]`: the task can be built at the same time as the one before it — its `Après :` does not name it and
they share no file. Dropped from spec-kit: separate test tasks (each task writes its test first) and the
Polish phase (docs are `rendre`'s; anything else belongs to a story).

`skills/cadrer-x-decouper/scripts/lint.py taches <path>` checks the form and the plan's links: ids, each task's
lines, its stories, exigences and screens against `spec.md` and `passation.md`, `[P]`, one owner per shared file,
the files a task never touches, and `Couverts`.

### passation.md (design handoff)

| Proa | cadrer-x |
|---|---|
| Prototype | Maquette (`- Lien :`, `- Style :`) |
| Screens | Écrans |
| `### SC1 <name>` | `### SC1 <nom>` |
| `Stories:` / `File:` / `Parts:` / `States:` / `Widths:` / `Copy:` | `Récits :` / `Fichier :` / `Parties :` / `États :` / `Largeurs :` / `Textes :` (one line each, in that order) |
| New parts | Nouveautés |
| Accessibility | Accessibilité |
| Open | Ouvert |
| the design-handoff checklist | `## Contrôle` (ticked before the save) |

Template: `skills/cadrer-x-affiner/templates/passation.md`. The pages: `maquette/<page>.html`, one per
screen, each state a `<section data-state="<état>">` reached at `<page>.html#<état>`; `maquette/styles.css`
(the design system's, copied unedited, or the template's neutral one); `maquette/maquette.js` (the
template's, unedited); the state bar `nav.maquette-etats`. Neither the bar nor the script is product code.

### textes.md

`# <Titre> — textes`, then `## SC1 <nom>`, `### <état>`, and `- <Clé> : <texte>` (Titre, Message,
Bouton…; `{mot}` for what varies). Proa kept it as `prototype/copy.md`; cadrer-x keeps it beside
`passation.md`. Template: `skills/cadrer-x-affiner/templates/textes.md`.

### audit.md (one review per user story)

One section per story, the latest on top: `## US1 <titre>`, then `**Tour** :`, `**Date** :`, `**Verdict** :`
(`à corriger` while any `Bloquant :` or `À corriger :` is left, else `validé`), and under it:

| Proa | cadrer-x |
|---|---|
| `## Spec` | `### Spec` |
| `## Standards` | `### Règles` |
| `## Declined to judge` | `### Non jugé` |
| `### Fix round's diff` | `### Correctifs` |
| `CHECKS:` / `SCREENS:` | `Vérifs :` / `Écrans :` |
| Critical / Must / Nit / FYI / Fixed | Bloquant / À corriger / Détail / Info / Corrigé |
| missing / partial / contradicts / unrequested | manquant / partiel / contraire / non demandé |

Each finding: `- <Préfixe> : <file:line> — <gap> : <what> ; <what a person meets> ; correction : <fix>`. A
clean axis is `- aucun`. A new tour of a story replaces its section. Committed on the feature branch as
`audit US1 — <verdict>`, with its screenshots in `captures/SC1-390.png`. Template:
`skills/cadrer-x-examiner/templates/audit.md`; `skills/cadrer-x-examiner/scripts/lint.py audit <path>` checks
the form and that each verdict follows from its findings.

### livraison.md (release + going online)

| Proa release.md | cadrer livraison.md | cadrer-x |
|---|---|---|
| Version | — | Version (the version alone on its first line) |
| What shipped | — | Livré (one line per story, then « Plus tard : … ») |
| Where | En ligne | En ligne (`pas encore`, `aucun — <pourquoi>`, or the address, date, commit) |
| — | Mise en ligne | Mise en ligne |
| Evidence | Vérifié en ligne | Vérifié |
| How to roll back | Si ça casse | En cas de problème |
| — | Reste à faire | À faire (each line *à la main*, or the skill that turns it into work) |

A later release of the feature puts its section on top. Template: `skills/cadrer-x-rendre/templates/livraison.md`.

### pr.md (the pull request's body)

| Proa pr.md | cadrer-x |
|---|---|
| Summary | Résumé |
| Evidence | Preuves (`- Vérifs : …`, each story's review tour, captures as `![…](<repo path>)`) |
| Merge danger | Risque de fusion |
| `**Door:** one-way \| two-way` | `**Porte** : aller simple` \| `aller-retour` |
| `**Blast radius:**` | `**Portée** :` |

`skills/cadrer-x-rendre/scripts/lint.py livraison|pr <path>` checks both. rendre commits them with the
docs as `livraison — <Titre> <version>` on the person's yes; the merge has its own yes (a push and a PR
from `pr.md` with a remote, `git merge --no-ff` without). Step 2 commits `livraison — <adresse>` on the main
branch, and writes the commands that worked into `cadrer-x.yml` → `envs` (`<env>: {url, deploy, rollback}`).

### docs/security/

The data list (`data-inventory.md`, or the file the constitution names) and the threats (`threat-model.md`), folded in
by `rendre` at release; no task touches them.

### verification.md (cadrer-x-verifier)

`# <Titre> — vérification`, then `**Date** :`, `**Portée** :` (`spec` | `spec et tâches`), `**Verdict** :`
(`à reprendre` | `prête`), `## Constats` (`- À reprendre : <file:line> — … ; → /cadrer-x-affiner`, or
`- Remarque : …`, each ending on the step that fixes it), `## Vérifié`. Committed alone as `vérification —
<Titre>`. Template and lint: `skills/cadrer-x-verifier/templates/verification.md`, `scripts/lint.py verification`.

### docs/architecture.md

| Proa / cadrer | cadrer-x |
|---|---|
| Modules | Modules |
| Pièces | Pièces |
| Comptes et secrets | Secrets |
| Données | Données |
| Coût | Coût |
| À faire à la main | À faire |
| En local | En local |
| Pour lancer | Lancer |
| Trajet | Trajet |
| Écarté (cadrer) | Écarté |
| Words (Proa) | Mots (the product's own terms; a spec uses them, never a synonym) |

Template: `skills/cadrer-x-init/templates/architecture.md`.

### docs/constitution.md

Written by `cadrer-x-init` (step 2) from `skills/cadrer-x-init/templates/constitution.md`, each rule
approved by the person; changed only through an ADR they approve, which `cadrer-x-rendre` writes.

| Heading / column | cadrer-x |
|---|---|
| title | `# <Produit> — constitution` |
| table | `# | Règle | Vérifiée par | Quand`, rows `M1`… |
| exceptions | `## Exceptions` |

### AGENTS.md, CLAUDE.md

`AGENTS.md` is for the agents: where the docs are, the commands, a pointer to the constitution, never
its rules. `CLAUDE.md` holds `@AGENTS.md`, so both engines read one file.

### ADR and CHANGELOG

| Proa | cadrer-x |
|---|---|
| Context / Decision / Options considered / Why | Contexte / Décision / Options / Pourquoi |

ADR template: `skills/cadrer-x-rendre/templates/adr.md` (with `**Date** :`, `**Fonctionnalité** :`, `**Remplace** :`).
| Added / Changed / Fixed / Security | Ajouté / Modifié / Corrigé / Sécurité (Keep a Changelog's French version) |

## Skills

21 Proa skills became 7 skills, 1 optional check and 6 helpers. `init` comes first, once per project; the
next six spell CADRER, in order. A skill holding two steps checks which one's file is missing and runs
that one. A helper is loaded by the skills that need it, never run on its own.

| | Skill | Its steps (Proa skills merged) | Writes |
|---|---|---|---|
| — | `cadrer-x-init` | 1. vision (proa-vision) · 2. layout (proa-adopt, proa-stack at project level, the constitution); both on branch `chore/cadrer-x-init`, merged on the person's yes | `docs/vision.md` · `cadrer-x.yml`, `docs/architecture.md`, `AGENTS.md` |
| **C** | `cadrer-x-choisir` | 1. idea (proa-idea) · 2. decisions (proa-decide, proa-stack for a feature's new service) | `idee.md` · `decisions.md` |
| **A** | `cadrer-x-affiner` | 1. spec (proa-spec) · 2. prototype, when there are screens (prototype, design-handoff) | `spec.md`, `a-trancher.md` · `maquette/`, `textes.md`, `passation.md` |
| **D** | `cadrer-x-decouper` | tasks (proa-slice, threat-list) | `taches.md` |
| **R** | `cadrer-x-realiser` | one task per session; `[P]` tasks run in parallel sessions, each in its own worktree branched from the feature (proa-build) | code, the task's branch in `.worktrees/`, merged back into `feature/<slug>` |
| **E** | `cadrer-x-examiner` | one user story, once all its `[US<n>]` tasks are built; a task with no story is reviewed with the first story that builds on it (proa-review, design-review) | `audit.md` |
| **R** | `cadrer-x-rendre` | release and going online, once every story's audit passes and the whole test suite is green (proa-release, cadrer-livrer) | `livraison.md`, `pr.md`, CHANGELOG, ADR |

Optional, outside the acronym, like spec-kit's `/analyze`:

| | Skill | What it does | Writes |
|---|---|---|---|
| — | `cadrer-x-verifier` | Read-only, in a fresh session, after affiner or after decouper: checks the stories themselves before any code. Each acceptance line can be checked without code; each decision of `decisions.md` lands in a story or under `Pas encore`; once `taches.md` exists, every story has its tasks under `Couverts` and every task points to a story or is `Après :` one; nothing in the spec contradicts `decisions.md` or `docs/constitution.md`. Fixes nothing: each finding names the skill that fixes it (affiner or decouper). | `verification.md` |

| Helper | Merges | Loaded by |
|---|---|---|
| `cadrer-x-securite` | secure-defaults, abuse-tests, data-inventory | choisir, affiner, decouper, realiser, examiner, rendre |
| `cadrer-x-tdd` | (new, after Matt Pocock's `tdd`) | realiser, examiner |
| `cadrer-x-debug` | proa-debug | realiser, examiner, any failing test |
| `cadrer-x-design-system` | design-system | init, affiner, realiser, examiner |
| `cadrer-x-modules` | module-borders | decouper, realiser, examiner |
| `cadrer-x-textes` | french-copy, with fleet's `frlint` ported as `scripts/frlint.py` | affiner, realiser, examiner, rendre |

A helper has `user-invocable: false` (Claude Code keeps it out of the `/` menu) and
`allow_implicit_invocation: true` in its `agents/openai.yaml` (codex may load it on its own). The
project's own copy rules live in `{docs}/textes.md`; `cadrer-x-textes` reads them before its defaults.

Kept apart, on purpose: affiner and decouper (the spec is the person's gate on *what*, before any *how*);
realiser and examiner. realiser proves its own task works: a failing test first, then the code, then the
checks run fresh. examiner asks what those tests cannot: whether the story is what the spec asked for, and
whether its tests would fail if the behaviour broke. The builder's tests carry the builder's reading of the
spec, so a misreading passes them.

## Install

`install.sh` copies each skill (without its `evals/`) into the project by default: `.claude/skills` and
`.agents/skills`, committed with the project so everyone on it has the same version. `--global` puts
them in `~/.claude/skills` and `~/.agents/skills` instead. `--link` symlinks to the checkout, to try
changes live; `--remove` takes them out.

## Later, for fleet

Fleet's parsers read the English names today (`claude/scripts/fleetlib/slices.py`, `handoff.py`, `lint.py`,
`review.py`, `gate.py`) and slice ids as `S01`. When fleet wraps cadrer-x, they switch to the names above
and to `T01`; and fleet reads the project file as `cadrer-x.yml` where it reads `proa.yml` today. Sailor reports
(`STATUS:`, `SUMMARY:`, …) are fleet's own and stay out of cadrer-x.
