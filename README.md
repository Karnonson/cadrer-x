# cadrer-x

Des compétences pour Claude Code et codex. Elles mènent un projet de l'idée à la mise en ligne, une
étape à la fois : `init`, puis **C**hoisir, **A**ffiner, **D**écouper (`choisir`), **R**éaliser,
**E**xaminer (`realiser`), **R**endre (`rendre`). Tu décides aux moments qui comptent.

Chaque étape écrit un fichier que la suivante lit. Une commande enchaîne ses étapes dans la même
session, sauf si tu l'arrêtes ; d'une commande à l'autre, c'est toi qui lances la suite
([Les étapes](#les-étapes)). Rien ne part sans ton oui : ni la spec, ni la fusion dans la branche
principale, ni la mise en ligne. Les étapes te parlent dans ta langue ; les noms de fichiers et les
titres restent fixes, en français, pour que chaque étape retrouve le travail de la précédente.

## Installer

### Avec Claude Code : le plugin

Le plus simple, sur macOS, Linux et Windows. Dans Claude Code, tape :

```
/plugin install cadrer-x --marketplace Karnonson/cadrer-x
```

Avec une version plus ancienne de Claude Code : `/plugin marketplace add Karnonson/cadrer-x`, puis
`/plugin install cadrer-x@cadrer-x`. Redémarre ensuite Claude Code.

Les étapes servent alors dans tous tes projets : `/cadrer-x-init`, `/cadrer-x-choisir`… (ou leur nom
complet, `/cadrer-x:cadrer-x-init`). Au début de chaque session, le plugin vérifie que ton ordinateur
a git et Python 3 ; s'il en manque, Claude te dit quoi et comment l'installer, et n'installe rien sans
ton oui. `cadrer-x-init` autorise dans le projet les commandes git que les étapes lancent ; `git push`
te sera toujours demandé.

Par défaut, le plugin sert à toi seul, dans tous tes projets. Pour que tout le monde sur un projet
l'ait aussi, lance depuis le dossier du projet, dans un terminal :

```sh
claude plugin marketplace add Karnonson/cadrer-x --scope project
claude plugin install cadrer-x@cadrer-x --scope project
```

Les deux s'écrivent dans `.claude/settings.json`, à committer : à l'ouverture du projet, Claude Code
propose le plugin à chacun.

Pour mettre à jour : `/plugin marketplace update cadrer-x`, ou active la mise à jour automatique dans
`/plugin`, onglet des marketplaces. Tant que le dépôt est privé, il faut y avoir accès et que git soit
connecté à GitHub (`gh auth login`, puis `gh auth setup-git`).

Le plugin ou les lignes ci-dessous, pas les deux dans le même projet : les étapes apparaîtraient deux
fois.

### Avec codex, ou pour mettre les compétences dans le projet

Il te faut d'abord Claude Code ou codex. Ensuite, depuis le dossier de ton projet, une seule ligne.

macOS, Linux (et Git Bash sous Windows) :

```sh
curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash
```

Windows (PowerShell) :

```powershell
irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex
```

Elle vérifie que ton ordinateur a git et Python 3 (et Git for Windows sous Windows). S'il en manque,
elle te dit quoi et comment elle va l'installer, et n'installe rien sans ton oui (`o`). Puis elle
récupère cadrer-x dans `~/cadrer-x` (sous Windows, `%USERPROFILE%\cadrer-x`) et installe les
compétences pour Claude Code, codex ou les deux, selon ce que ton ordinateur a. Relancer la même ligne
met à jour.

Les compétences vont dans `.claude/skills` (Claude Code) et `.agents/skills` (codex) du projet : à
committer, pour que tout le monde sur le projet ait la même version. `.claude/settings.json` autorise
aussi les commandes git que les étapes lancent (worktrees, fusions, commits), pour que le
développement ne te demande pas ton accord à chaque fusion ; `git push` te le demande toujours.
`cadrer-x-init` y ajoute les commandes du projet (installer, vérifier, lancer).

Les options sont les mêmes sur les deux systèmes : un `<dossier>` pour installer ailleurs que dans le
dossier courant, `--global` pour tous tes projets à la fois, `--engine claude` ou `--engine codex` pour
un seul des deux, `--link` pour suivre ta copie de cadrer-x en direct, `--remove` pour les retirer,
`--yes` pour répondre oui d'avance. Elles se mettent à la fin :

```sh
curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash -s -- --engine codex
~/cadrer-x/install.sh --global        # une fois cadrer-x récupéré
```

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1))) --engine codex
```

Pour essayer sans toucher un vrai projet, installe-les dans un dossier d'essai, en lien :
`~/cadrer-x/install.sh --link ~/essais`. Lance tes sessions depuis ce dossier ; une modification des
compétences dans `~/cadrer-x` s'y voit tout de suite. Sous Windows, `--link` fait une simple copie :
relance la ligne pour voir une modification.

Les compétences ne servent que dans le dossier où tu les installes : une session lancée dans un
sous-dossier ne les voit pas. Pour un projet rangé dans ton dossier d'essai, installe-les dans le
projet lui-même : `~/cadrer-x/install.sh --link ~/essais/mon-projet`. Sinon, installe-les pour tous
tes projets avec `--global`.

## Les étapes

```
/cadrer-x-init                 une fois par projet : la vision, puis l'organisation
/cadrer-x-ranger               si le code existe déjà : le ranger en modules, sans rien changer au produit
/cadrer-x-choisir              l'idée d'une fonctionnalité, ses décisions, la spec (tu la valides),
                               la maquette s'il y a des écrans (un croquis avec la spec, puis le
                               look et les mots, que tu valides), puis les tâches, vérifiées par un
                               second regard ; /cadrer-x-choisir <nom> reprend là où elle en est
/cadrer-x-realiser <nom>       tout le développement : chaque tâche test d'abord, chaque récit relu
/cadrer-x-rendre <nom>         la doc et la version, puis un seul oui pour envoyer et fusionner,
                               puis la mise en ligne, sur son propre oui
/cadrer-x-retour [mots]        quand tu veux : un court retour aux auteurs de cadrer-x
```

À la fin de chaque étape, si tu l'as accepté une fois (`retours: oui` dans `cadrer-x.yml`), un court
rapport part en ticket GitHub sur le dépôt cadrer-x, sous ton compte : l'étape, jusqu'où elle est
allée, ce qui a coincé, jamais rien de ton produit. Il t'est montré en entier à chaque fois. Pour
arrêter, dis-le, ou mets `retours: non`.

En pratique, trois sessions par fonctionnalité : `choisir` (de l'idée aux tâches), `realiser`, puis
`rendre` ; les deux premières finissent en te donnant la commande suivante. Tu peux toujours arrêter
une étape et lancer la commande plus tard. Une étape reprend là où ses fichiers s'arrêtent :
relance-la, elle sait où elle en est.

`/cadrer-x-realiser <nom>` mène tout le développement depuis une seule session : il confie chaque tâche
à un agent qui la développe dans son worktree (deux à la fois quand elles ne se touchent pas), la
fusionne dans la branche de la fonctionnalité quand les vérifs passent, fait relire chaque récit par un
agent neuf qui ne l'a pas développé (c'est lui qui clique les écrans, la maquette validée à côté ;
celui qui développe n'ouvre jamais le navigateur), et renvoie ce que la relecture trouve à un agent
qui le corrige. Il ne s'arrête que pour tes questions et, une fois tout relu, pour une dernière :
les détails que la relecture a laissés, on les corrige maintenant ou on livre ? Ceux qui attendent,
`rendre` les note dans `livraison.md`. À la main, si tu préfères :
`/cadrer-x-realiser T01` (une tâche), `/cadrer-x-realiser <nom> US1` (une relecture, dans une autre
session).

Un petit changement (un mot, une couleur, un bouton qui se comporte mal) ou un bug passe aussi par
`/cadrer-x-choisir` : décris-le en une phrase (« le bouton Envoyer ne fait rien »). L'entretien se
réduit à ce qui manque, l'agent essaie le bug lui-même, et la voie courte saute la maquette et les
validations en trop. La relecture par un agent neuf, elle, reste.

Facultatif : `/cadrer-x-verifier <nom>`, dans une session neuve, un regard à froid avant le code :
sur la spec seule, ou sur la spec et les tâches. Utile surtout quand `choisir` n'a pas pu lancer son
second regard (sans sous-agents) : il te le propose alors.

Six aides, de simples fichiers `aide.md`, sont lues par une étape au moment où elle en a besoin :
`cadrer-x-tdd`, `cadrer-x-securite`, `cadrer-x-debug`, `cadrer-x-modules`, `cadrer-x-design-system`,
`cadrer-x-textes`.

## Où vont les fichiers

```
cadrer-x.yml                       les commandes : installer, vérifier, lancer
docs/vision.md  docs/architecture.md  docs/glossaire.md  docs/constitution.md  docs/adr/
docs/features/0001-<nom>/
  brief.md  decisions.md  spec.md  a-trancher.md  taches.md
  maquette/  passation.md  contenu.md
  verification.md  audit.md  livraison.md  pr.md  captures/
.worktrees/                        un dossier par branche en cours (feature.<nom>, tache.<nom>-t01)
```

Le code suit d'abord le framework : s'il a sa façon de ranger le code (Rails, Django, NestJS…),
cadrer-x la suit telle quelle. Ce qu'il laisse libre prend la même forme dans chaque projet : un module
par partie du produit, chacun avec une seule porte d'entrée.

```
src/                               un seul, celui du framework quand il en a un (jamais src/src/)
  <dossiers du framework>          app/, pages/, routes/… : minces, ils appellent un module
  modules/<module>/api.<ext>       la seule porte du module ; derrière : ui/, server/, data/
  shared/                          ce que plusieurs modules partagent, sans règle du produit
tests/modules/<module>/            les tests d'un module, par sa porte
db/migrations/                     un fichier par changement du schéma
```

Un projet existant garde sa disposition jusqu'à ce que tu la changes : `cadrer-x-init` la décrit telle
qu'elle est, écrit celle visée, puis propose `/cadrer-x-ranger`, qui déplace le code un module à la
fois, après avoir prouvé par des tests et des captures ce que le produit fait aujourd'hui. Le détail :
[`skills/cadrer-x-modules/references/structure.md`](skills/cadrer-x-modules/references/structure.md).

Une fonctionnalité vit sur `feature/<nom>` ; chaque tâche sur `tache/<nom>-t01`, qui rejoint la
fonctionnalité dès que ses vérifs passent (c'est local, et ça se défait d'une commande). Seule `rendre`
fusionne dans la branche principale et pousse, et seulement sur ton oui.

Les noms, titres et libellés exacts sont dans [`docs/conventions.md`](docs/conventions.md).

## Feuille de route

Ce qui vient, avant et après la v2 : [`docs/roadmap.md`](docs/roadmap.md).

## Tu viens de cadrer ?

[`docs/migration-cadrer.md`](docs/migration-cadrer.md) : ce qui change, et comment passer un projet de
`builds/<NN>-<nom>/` à `docs/features/`.

## Pourquoi les compétences sont en anglais

Ce que tu lis est en français : les noms des commandes, leurs descriptions, les fichiers que les étapes
écrivent (`spec.md`, `taches.md`…), leurs titres et leurs libellés. Les étapes te parlent dans ta langue.

Le corps d'une compétence, lui, n'est lu que par l'agent : ce sont ses consignes, chargées à chaque
fois qu'une étape tourne. Le français coûte plus de tokens pour la même consigne, donc il est en anglais.

Mesuré avec `tools/token_estimate.py` le 2026-10-03, sur quatre compétences (`realiser`, `modules`,
`tdd`, `debug`) traduites en entier en français :

| | Anglais | Français |
| --- | --- | --- |
| Quatre compétences, tokenizer o200k | 4 987 | 5 855 (1,17×) |
| Médiane de sept tokenizers publics | | 1,26× (de 1,17× à 1,28×) |

Au 2026-10-07, les six compétences et les six aides font environ 29 500 tokens en anglais (o200k ;
55 500 avec les fichiers qu'elles lisent). En français, ce serait de 5 000 à 8 300 tokens de plus,
payés à chaque étape lancée : une fois par tâche pour l'agent qui la développe, une fois par récit
pour celui qui le relit. Le tokenizer de Claude n'est pas public : le ratio vient des tokenizers
publics, et `ANTHROPIC_API_KEY` ajoute le compte exact de Claude.

## Outils

`tools/token_estimate.py` compte ce que les compétences coûtent en tokens, et compare deux versions
(appariées par nom de dossier, ou `--map EN=FR`). Repris de cadrer.

```sh
uv run tools/token_estimate.py skills                       # les consignes seules
uv run tools/token_estimate.py skills --files               # avec references/ et templates/
uv run tools/token_estimate.py skills chemin/vers/fr/skills  # anglais contre français
```

`--detail o200k` détaille par compétence, `--only o200k` n'en charge qu'un, `--json` donne les chiffres.

## Licence

MIT, voir [`LICENSE`](LICENSE). Sauf `skills/cadrer-x-design-system/direction.md` : adapté de la
compétence frontend-design d'Anthropic, il reste sous licence Apache-2.0
([`LICENSE-frontend-design.txt`](skills/cadrer-x-design-system/LICENSE-frontend-design.txt)).
