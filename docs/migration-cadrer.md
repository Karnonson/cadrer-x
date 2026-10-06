# Passer de cadrer à cadrer-x

cadrer-x reprend la méthode de cadrer, avec trois changements de fond :

- **Un dossier par fonctionnalité dans `docs/`**, plus `builds/` : `docs/features/0001-<nom>/`, et une seule
  `docs/architecture.md` pour tout le projet, au lieu d'une par build.
- **Une construction menée depuis une session** : `/cadrer-x-realiser <nom>` confie chaque tâche à un agent
  qui la construit dans son propre worktree, deux à la fois quand c'est possible, et la fusionne dans la
  fonctionnalité quand ses vérifs passent.
- **Une relecture par récit**, plus une par tranche : quand toutes les tâches d'un récit sont faites,
  `realiser` le fait relire par un agent neuf qui ne l'a pas construit, et fait corriger ce qu'il trouve.

## Les étapes

| cadrer | cadrer-x | Ce qui change |
|---|---|---|
| — | `/cadrer-x-init` | Nouveau, une fois par projet : la vision, puis `cadrer-x.yml`, `docs/architecture.md`, `docs/constitution.md`, `AGENTS.md`. |
| `cadrer-choisir` | `/cadrer-x-choisir`, étape 1 | L'idée, comme avant : `idee.md`. |
| `cadrer-affiner` | `/cadrer-x-choisir`, étape 2 | Les décisions : `decisions.md`. Où ça tourne et ce que ça coûte vont dans `docs/architecture.md`, celle du projet. |
| `cadrer-detailler` | `/cadrer-x-choisir`, la spec | La spec, au format de spec-kit : récits `US1`, scénarios Étant donné / quand / alors, exigences `EF1`, **Statut** brouillon puis validée sur ton oui. |
| — | `/cadrer-x-choisir`, la maquette | Nouveau, s'il y a des écrans : une maquette cliquable (`maquette/`), ses textes (`contenu.md`) et `passation.md`. |
| `cadrer-repartir` | `/cadrer-x-choisir`, les tâches | `tranches.md` devient `taches.md` : des tâches `T01`, rangées par récit, chacune avec ses cases, ses fichiers, ses risques et ce qu'elle attend ; puis un second regard (`verifier`) avant ton oui. |
| — | `/cadrer-x-verifier` | Facultatif : un second regard sur la spec seule, avant de découper. |
| `cadrer-executer` | `/cadrer-x-realiser <nom>` | Toute la construction : chaque tâche test d'abord, dans `.worktrees/tache.<nom>-t01`, fusionnée quand ses vérifs passent. `T01` pour une seule tâche. |
| `cadrer-reviser` | `/cadrer-x-realiser <nom> US1` | Un récit entier, plus une tranche, lancé par `realiser` ; `audits/<NN>.md` devient une section de `audit.md`. |
| — | `/cadrer-x-ranger` | Nouveau : le code existant rangé en modules, sans rien changer au produit. |
| `cadrer-livrer` | `/cadrer-x-rendre` | La doc du projet, l'ADR, la version, le CHANGELOG, `livraison.md` et `pr.md` d'abord ; puis la fusion, puis la mise en ligne, chacune sur son oui. |

## Les fichiers

| cadrer | cadrer-x |
|---|---|
| `builds/01-<nom>/` | `docs/features/0001-<nom>/` |
| `builds/01-<nom>/architecture.md` | `docs/architecture.md`, une pour le projet |
| **Comptes et secrets** · **À faire à la main** · **Pour lancer** | **Secrets** · **À faire** · **Lancer** |
| `tranches.md`, `## 01 — <titre>` | `taches.md`, `- [ ] T01 [US1] <titre>` |
| **Bloqué par :** | `Après :` |
| **Fait quand :** | les cases sous la tâche, une par scénario de la spec |
| **Fichiers :** | `Fichiers :` (la tâche ne touche qu'eux) |
| — | `Risques :`, `Exigences :`, `Écrans :`, `Taille :` |
| **Non placé** | **Pas encore**, dans la spec |
| `audits/01.md`, `audits/code.md` | `audit.md`, une section par récit |
| Verdict *fusionner* · *corriger d'abord* · *retour à la tranche* | **Verdict** : `validé` · `à corriger` (et une question à la personne si la spec était fausse) |
| `a-trancher.md` | `a-trancher.md`, chaque question `## Q1 · spec · …` avec Options, Effets, Conseil, Réponse |
| `livraison.md` : En ligne · Mise en ligne · Vérifié en ligne · Si ça casse · Reste à faire | `livraison.md` : Version · Livré · En ligne · Mise en ligne · Vérifié · En cas de problème · À faire |
| — | `pr.md`, `CHANGELOG.md`, `docs/adr/` |
| `captures/` | `captures/` |

## Les branches

| cadrer | cadrer-x |
|---|---|
| La branche où tu es | `feature/<nom>`, dans `.worktrees/feature.<nom>` |
| `parallele` : `tranche-01` dans `../<nom>-01` | `tache/<nom>-t01` dans `.worktrees/tache.<nom>-t01`, une session par tâche |
| `git merge --no-ff` après l'audit | `git merge --ff-only` dans la fonctionnalité, dès que les vérifs passent ; la fonctionnalité rejoint la branche principale avec `/cadrer-x-rendre`, sur ton oui |

## Migrer un projet

1. **Installer cadrer-x** dans le projet : depuis le dossier du projet, `~/cadrer-x/install.sh` (voir l'installation
   dans le [README](../README.md#installer)). Retirer les compétences
   cadrer de `.claude/skills` et `.agents/skills` (ou de `~/.claude/skills`), pour ne pas avoir deux méthodes
   à la fois.
2. **Lancer `/cadrer-x-init`.** L'étape 1 écrit la vision (dis-lui que `idee.md` du premier build la
   contient en partie). L'étape 2 range les docs : chaque `builds/<NN>-<nom>/` part dans
   `docs/features/<NNNN>-<nom>/` avec ses fichiers tels quels, et l'`architecture.md` du dernier build
   devient `docs/architecture.md`. Tout se passe sur la branche `chore/cadrer-x-init`, fusionnée sur ton oui.
3. **Un build déjà livré** : rien d'autre à faire. Ses anciens fichiers restent comme historique.
4. **Un build en cours** :
   - spec écrite, pas encore découpée : `/cadrer-x-choisir <nom>` réécrit la spec au nouveau format et
     te la fait valider, puis découpe les tâches.
   - déjà en tranches, en partie construit : termine la tranche en cours avec cadrer si elle est presque
     finie. Sinon, `/cadrer-x-choisir <nom>` (la spec au nouveau format, puis les tâches) : il lit le code
     des tranches cochées, écrit ce qu'elles prouvent déjà comme des tâches cochées `[x]`, et découpe
     seulement le reste.
   - une branche par build : renomme-la `feature/<nom>` (`git branch -m <ancienne> feature/<nom>`).
5. **Les audits passés** (`audits/`) ne se convertissent pas : la première relecture cadrer-x de chaque
   récit écrit `audit.md`.

À la main, si tu préfères ranger toi-même avant `/cadrer-x-init` :

```sh
mkdir -p docs/features
git mv builds/01-inscription docs/features/0001-inscription
git mv docs/features/0001-inscription/architecture.md docs/architecture.md   # le dernier build seulement
git commit -m "docs: ranger les builds de cadrer dans docs/features"
```
