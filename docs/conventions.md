# cadrer-x conventions

Draft, 2026-10-03. The fixed names every cadrer-x skill writes and reads. A skill finds another skill's
section by its exact heading, so these names never change once released, and they are never translated per
person. Later, fleet parses the same names.

## Rules

- **Language.** A skill's name and `description`: French. Its body (instructions to the model): English.
  What it says and the prose it writes: the person's language. File names, headings and labels below:
  French, as written here, for everyone.
- **Short.** A heading is one or two words. A label ends with ` :` (`Fichiers :`).
- **Ids stay ids.** `US1` (story), `SC1` (screen), `T01` (task), `Q1` (question), `[P]` (a task that can be built at the same time as the one before it)
  are ids, not words: they are not translated.
- **Accents are part of the name.** `À surveiller`, not `A surveiller`.
- Marked **?**: a proposal still to confirm.

## Layout

```
proa.yml                          project file: code, install, checks
docs/architecture.md              stack, runtime, Modules
docs/constitution.md
docs/adr/NNNN-<slug>.md
docs/features/NNNN-<slug>/
  idee.md  decisions.md  spec.md  a-trancher.md  taches.md
  maquette/  passation.md  textes.md
  audit.md  livraison.md  pr.md  captures/
.worktrees/<branch>/
```

| Proa today | cadrer (old) | cadrer-x |
|---|---|---|
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
| Build or use | Faire ou prendre |

### decisions.md

| Proa | cadrer-x |
|---|---|
| Decisions | Décisions |
| Stages | Étapes |
| Clarifications | Précisions |
| Stack choices | Stack |
| Architecture impact | Impact archi |
| Data and risks | Données et risques |

### spec.md

| Proa | cadrer-x |
|---|---|
| User stories | Récits |
| `### US1 <title>` | `### US1 <titre>` |
| As a … I want … so that | En tant que … je veux … afin de |
| Success criteria | Critères |
| Not yet | Pas encore |
| Requirements checklist | Vérifs |

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

| Proa | cadrer-x |
|---|---|
| `## Review focus` | `## À surveiller` |
| `## Coverage` | `## Couverts` |
| `Files:` | `Fichiers :` |
| `After:` | `Après :` (the tasks it builds on; with `[P]` on its line when it needs none of the tasks still open before it) |
| `Screens:` | `Écrans :` |
| `Risks:` | `Risques :` |
| `MUSTs to own:` | `Exigences :` |
| — (cadrer) `Fait quand :` | `Fait quand :` |
| — (cadrer) `Audit :` | `Audit :` |

### passation.md (design handoff)

| Proa | cadrer-x |
|---|---|
| Prototype | Maquette |
| Screens | Écrans |
| `### SC1 <name>` | `### SC1 <nom>` |
| New parts | Nouveautés |
| Accessibility | Accessibilité |
| Open | Ouvert |
| `Title:` / `Link:` / `States:` / `Stories:` | `Titre :` / `Lien :` / `États :` / `Récits :` |
| `Widths:` | `Largeurs :` |

### audit.md (feature review)

| Proa | cadrer-x |
|---|---|
| `## Spec` | `## Spec` |
| `## Standards` | `## Règles` |
| `## Declined to judge` | `## Non jugé` |
| `### Fix round's diff` | `### Correctifs` |
| `CHECKS:` / `SCREENS:` | `Vérifs :` / `Écrans :` |
| Critical / Must / Nit / FYI / Fixed | Bloquant / À corriger / Détail / Info / Corrigé |

### livraison.md (release + going online)

| Proa release.md | cadrer livraison.md | cadrer-x |
|---|---|---|
| Version | — | Version |
| Where | En ligne | En ligne |
| What shipped | — | Livré |
| — | Mise en ligne | Mise en ligne |
| Evidence | Vérifié en ligne | Vérifié |
| How to roll back | Si ça casse | En cas de problème |
| Merge danger | — | Risque de fusion |
| Summary | — | Résumé |
| — | Reste à faire | À faire |

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

### ADR and CHANGELOG

| Proa | cadrer-x |
|---|---|
| Context / Decision / Options considered / Why | Contexte / Décision / Options / Pourquoi |
| Added / Changed / Fixed / Security | Ajouté / Modifié / Corrigé / Sécurité (Keep a Changelog's French version) |

## Skills

Proposal: 21 Proa skills become 7 skills and 5 helpers. `init` comes first, once per project; the
next six spell CADRER, in order. A skill holding two steps checks which one's file is missing and runs
that one. A helper is loaded by the skills that need it, never run on its own.

| | Skill | Its steps (Proa skills merged) | Writes |
|---|---|---|---|
| — | `cadrer-x-init` | 1. vision (proa-vision) · 2. layout (proa-adopt, proa-stack at project level) | `docs/vision.md` · `proa.yml`, `docs/architecture.md`, `AGENTS.md` |
| **C** | `cadrer-x-choisir` | 1. idea (proa-idea) · 2. decisions (proa-decide, proa-stack for a feature's new service) | `idee.md` · `decisions.md` |
| **A** | `cadrer-x-affiner` | 1. spec (proa-spec) · 2. prototype, when there are screens (prototype, design-handoff) | `spec.md`, `a-trancher.md` · `maquette/`, `textes.md`, `passation.md` |
| **D** | `cadrer-x-decouper` | tasks (proa-slice, threat-list) | `taches.md` |
| **R** | `cadrer-x-realiser` | one task per run, in `taches.md` order (proa-build) | code, the task's branch in `.worktrees/` |
| **E** | `cadrer-x-examiner` | the whole feature, once its last task is built (proa-review, design-review) | `audit.md` |
| **R** | `cadrer-x-rendre` | release and going online (proa-release, cadrer-livrer) | `livraison.md`, `pr.md`, CHANGELOG, ADR |

| Helper | Merges | Loaded by |
|---|---|---|
| `cadrer-x-securite` | secure-defaults, abuse-tests, data-inventory | choisir, affiner, realiser, examiner, rendre |
| `cadrer-x-debug` | proa-debug | realiser, examiner, any failing test |
| `cadrer-x-design-system` | design-system | init, affiner, realiser |
| `cadrer-x-modules` | module-borders | decouper, realiser, examiner |
| `cadrer-x-textes` | french-copy | affiner, realiser, rendre |

Kept apart, on purpose: affiner and decouper (the spec is the person's gate on *what*, before any *how*);
realiser and examiner (the one who built a task does not judge it).

## Later, for fleet

Fleet's parsers read the English names today (`claude/scripts/fleetlib/slices.py`, `handoff.py`, `lint.py`,
`review.py`, `gate.py`) and slice ids as `S01`. When fleet wraps cadrer-x, they switch to the names above
and to `T01`. Sailor reports
(`STATUS:`, `SUMMARY:`, …) are fleet's own and stay out of cadrer-x.
