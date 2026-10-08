# cadrer-x

cadrer-x est un ensemble de compétences pour Claude Code et codex. Elles mènent un projet de l'idée
à la mise en ligne, une étape à la fois : `init`, puis **C**hoisir, **A**ffiner, **D**écouper
(`choisir`), **R**éaliser, **E**xaminer (`realiser`), **R**endre (`rendre`). Tu décides aux moments
qui comptent.

Chaque étape écrit un fichier que la suivante lit. Une commande enchaîne ses étapes dans la même
session, sauf si tu l'arrêtes. D'une commande à l'autre, c'est toi qui lances la suite (voir [Les
étapes](#les-étapes)). Rien ne part sans ton oui : ni la spec (le document qui décrit la
fonctionnalité), ni la fusion dans la branche principale, ni la mise en ligne. Les étapes te parlent
dans ta langue. Les noms de fichiers et les titres, eux, restent fixes et en français : chaque étape
retrouve ainsi le travail de la précédente.

## Installer

### Avec Claude Code : le plugin

C'est la méthode la plus simple, sur macOS, Linux et Windows. Dans Claude Code, tape :

```
/plugin install cadrer-x --marketplace Karnonson/cadrer-x
```

Avec une version plus ancienne de Claude Code, tape `/plugin marketplace add Karnonson/cadrer-x`,
puis `/plugin install cadrer-x@cadrer-x`. Redémarre ensuite Claude Code.

Les étapes sont alors disponibles dans tous tes projets : `/cadrer-x-init`, `/cadrer-x-choisir`…
(ou leur nom complet, `/cadrer-x:cadrer-x-init`). Quand tu ouvres une session, le plugin vérifie
que Git et Python 3 sont installés sur ton ordinateur. S'il manque l'un des deux, Claude te dit
lequel et comment l'installer, et il n'installe rien sans ton oui. `cadrer-x-init` autorise dans le
projet les commandes Git que les étapes lancent, et la commande `gh` qui envoie les retours. Pour
`git push`, ton accord te sera toujours demandé.

Par défaut, le plugin ne sert qu'à toi, dans tous tes projets. Pour que toutes les personnes du
projet l'aient aussi, lance ces commandes dans un terminal, depuis le dossier du projet :

```sh
claude plugin marketplace add Karnonson/cadrer-x --scope project
claude plugin install cadrer-x@cadrer-x --scope project
```

Ces deux commandes inscrivent le plugin dans `.claude/settings.json`, un fichier à inclure dans le
dépôt. À l'ouverture du projet, Claude Code propose alors le plugin à chaque personne.

Pour mettre à jour le plugin, tape `/plugin marketplace update cadrer-x`. Tu peux aussi activer la
mise à jour automatique dans `/plugin`, onglet des marketplaces.

Dans un même projet, choisis le plugin ou l'installation de la section suivante, pas les deux :
sinon, les étapes apparaîtraient deux fois.

### Avec codex, ou pour mettre les compétences dans le projet

Il te faut d'abord Claude Code ou codex. Ensuite, il suffit de lancer une seule ligne dans un
terminal, depuis le dossier de ton projet.

macOS, Linux (et Git Bash sous Windows) :

```sh
curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash
```

Windows (PowerShell) :

```powershell
irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex
```

Cette ligne vérifie que Git et Python 3 sont installés sur ton ordinateur (et Git for Windows sous
Windows). S'il en manque un, elle te dit lequel et comment elle va l'installer, et elle n'installe
rien sans ton oui (`o`). Elle récupère ensuite cadrer-x dans `~/cadrer-x` (sous Windows,
`%USERPROFILE%\cadrer-x`). Puis elle installe les compétences pour Claude Code, codex ou les deux,
selon les outils présents sur ton ordinateur. Pour mettre à jour, relance la même ligne.

Les compétences vont dans les dossiers `.claude/skills` (Claude Code) et `.agents/skills` (codex)
du projet. Inclus-les dans le dépôt : toutes les personnes du projet auront ainsi la même version.
`.claude/settings.json` autorise aussi les commandes Git que les étapes lancent (fusions, commits),
et la commande `gh` qui envoie les retours. Pendant le développement, Claude ne te demande donc pas
ton accord à chaque fusion, mais il te le demande toujours avant `git push`. `cadrer-x-init` y
ajoute les commandes du projet (installer, vérifier, lancer).

Les options sont les mêmes sur les deux systèmes. Avec un `<dossier>`, l'installation se fait
ailleurs que dans le dossier où tu te trouves. `--global` installe pour tous tes projets à la fois.
`--engine claude` ou `--engine codex` installe pour un seul des deux. `--link` crée des liens vers
ta copie de cadrer-x : tes modifications s'y voient tout de suite. `--remove` retire les
compétences. `--yes` répond oui d'avance. Les options se placent à la fin de
la ligne :

```sh
curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash -s -- --engine codex
~/cadrer-x/install.sh --global        # une fois cadrer-x récupéré
```

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1))) --engine codex
```

Pour essayer sans toucher à un vrai projet, installe les compétences sous forme de liens dans un
dossier d'essai : `~/cadrer-x/install.sh --link ~/essais`. Lance tes sessions depuis ce dossier.
Toute modification des compétences dans `~/cadrer-x` s'y voit tout de suite. Sous Windows,
`--link` fait une simple copie : relance la ligne pour voir une modification.

Les compétences ne fonctionnent que dans le dossier où tu les installes : une session lancée dans
un sous-dossier ne les voit pas. Pour un projet rangé dans ton dossier d'essai, installe-les dans
le projet lui-même : `~/cadrer-x/install.sh --link ~/essais/mon-projet`. Sinon, installe-les pour
tous tes projets avec `--global`.

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

Les étapes peuvent aussi envoyer un court rapport aux auteurs de cadrer-x. Si tu l'acceptes (une
seule fois suffit), chaque étape en envoie un quand elle se termine, ou te donne le lien pour
l'envoyer. C'est un ticket public sur GitHub, sous ton compte, dans le dépôt cadrer-x : tout le
monde peut le lire. Il indique l'outil utilisé, l'étape, où elle s'est arrêtée, ce qui a posé
problème, le nombre de questions et les endroits où tu as corrigé l'agent. Il ne dit rien de ton
produit ni de ton code. Tu le vois en entier chaque fois. Pour arrêter, dis-le ou écris
`retours: non` dans `cadrer-x.yml`.

En pratique, une fonctionnalité demande trois sessions : `choisir` (de l'idée aux tâches),
`realiser`, puis `rendre`. Les deux premières se terminent en te donnant la commande suivante. Tu
peux toujours arrêter une étape et lancer la commande plus tard. Une étape reprend là où ses
fichiers s'arrêtent : relance-la, elle sait où elle en est.

`/cadrer-x-realiser <nom>` mène tout le développement depuis une seule session. Elle confie chaque
tâche à un agent (une autre instance de l'IA, qui travaille pour elle), qui la développe dans son
worktree, sa propre copie de travail. Jusqu'à deux agents travaillent en même temps, quand leurs
tâches ne se touchent pas. Quand les vérifications réussissent, elle fusionne la tâche dans la
branche de la fonctionnalité. Dès qu'un récit (une chose que l'utilisateur du produit veut faire)
est terminé, elle le fait relire par un agent neuf, qui ne l'a pas développé. C'est cet agent qui
essaie les écrans, la maquette validée sous les yeux : celui qui développe n'ouvre jamais le
navigateur. Ce que la relecture trouve est renvoyé à un agent qui le corrige. `/cadrer-x-realiser`
ne s'arrête que pour te poser ses questions et, une fois tout relu, une dernière : les détails que
la relecture a laissés, on les corrige maintenant ou on livre? `rendre` note dans `livraison.md`
les détails laissés pour plus tard. Si tu préfères
avancer à la main, lance `/cadrer-x-realiser T01` (une tâche) ou `/cadrer-x-realiser <nom> US1`
(une relecture, dans une autre session).

Un petit changement (un mot, une couleur, un bouton qui se comporte mal) ou un bogue passe aussi
par `/cadrer-x-choisir` : décris-le en une phrase (« le bouton Envoyer ne fait rien »). Les
questions se limitent à ce qui manque, et l'agent essaie de reproduire le bogue lui-même. Ce
parcours court saute la maquette et les validations inutiles pour un si petit changement. La
relecture par un agent neuf, elle, reste.

`/cadrer-x-verifier <nom>` est une étape facultative. Lancée dans une session neuve, elle pose un
regard à froid avant le code, sur la spec seule ou sur la spec et les tâches. Elle sert surtout
quand `choisir` n'a pas pu faire relire son travail par un autre agent (certains outils ne le
permettent pas). `choisir` te la propose alors.

Les étapes lisent aussi six aides, de simples fichiers `aide.md`, au moment où elles en ont
besoin : `cadrer-x-tdd`, `cadrer-x-securite`, `cadrer-x-debug`, `cadrer-x-modules`,
`cadrer-x-design-system`, `cadrer-x-textes`.

## Où vont les fichiers

```
cadrer-x.yml                       les commandes (installer, vérifier, lancer) et retours:
docs/vision.md  docs/architecture.md  docs/glossaire.md  docs/constitution.md  docs/adr/
docs/features/0001-<nom>/
  brief.md  decisions.md  spec.md  a-trancher.md  taches.md
  maquette/  passation.md  contenu.md
  verification.md  audit.md  livraison.md  pr.md  captures/
.worktrees/                        un dossier par branche en cours (feature.<nom>, tache.<nom>-t01)
```

Le code suit d'abord le framework, c'est-à-dire le cadre de développement du projet. Si le
framework (Rails, Django, NestJS…) a sa propre façon de ranger le code, cadrer-x la suit telle
quelle. Ce
qu'il laisse libre prend la même forme dans chaque projet : un module par partie du produit,
chacun avec une seule porte d'entrée.

```
src/                               un seul, celui du framework quand il en a un (jamais src/src/)
  <dossiers du framework>          app/, pages/, routes/… : minces, ils appellent un module
  modules/<module>/api.<ext>       la seule porte du module ; derrière : ui/, server/, data/
  shared/                          ce que plusieurs modules partagent, sans règle du produit
tests/modules/<module>/            les tests d'un module, par sa porte
db/migrations/                     un fichier par changement du schéma
```

Un projet existant garde son organisation jusqu'à ce que tu la changes. `cadrer-x-init` décrit
l'organisation actuelle, écrit l'organisation visée, puis propose `/cadrer-x-ranger`. Cette commande
prouve d'abord, par des tests et des captures, ce que le produit fait aujourd'hui. Elle déplace
ensuite le code un module à la fois. Pour le détail, voir
[`skills/cadrer-x-modules/references/structure.md`](skills/cadrer-x-modules/references/structure.md).

Une fonctionnalité vit sur la branche `feature/<nom>`, et chaque tâche sur `tache/<nom>-t01`. Une
tâche rejoint la fonctionnalité dès que ses vérifications réussissent : cette fusion reste sur ton
ordinateur et s'annule en une commande. Seule l'étape `rendre` fusionne dans la branche principale
et envoie le code vers le dépôt en ligne, et uniquement avec ton accord.

Les noms, titres et libellés exacts sont dans [`docs/conventions.md`](docs/conventions.md).

## Feuille de route

Ce qui est prévu avant et après la v2 se trouve dans [`docs/roadmap.md`](docs/roadmap.md).

## Tu utilisais déjà cadrer?

[`docs/migration-cadrer.md`](docs/migration-cadrer.md) explique ce qui change et comment passer un
projet de `builds/<NN>-<nom>/` à `docs/features/`.

## Pourquoi les compétences sont en anglais

Ce que tu lis est en français : les noms des commandes, leurs descriptions, les fichiers que les
étapes écrivent (`spec.md`, `taches.md`…), leurs titres et leurs libellés. Les étapes te parlent
dans ta langue.

Le corps d'une compétence, lui, n'est lu que par l'agent : ce sont ses consignes, chargées chaque
fois qu'une étape s'exécute. Pour la même consigne, le français coûte plus de tokens (les jetons,
ces morceaux de texte que lit le modèle). C'est pourquoi ce corps est en anglais.

La mesure a été faite avec `tools/token_estimate.py` le 3 octobre 2026, sur quatre compétences
(`realiser`, `modules`, `tdd`, `debug`) traduites en entier en français :

| | Anglais | Français |
| --- | --- | --- |
| Quatre compétences, tokenizer o200k | 4 987 | 5 855 (1,17×) |
| Médiane de sept tokenizers publics | | 1,26× (de 1,17× à 1,28×) |

Au 8 octobre 2026, les sept compétences et les six aides font environ 31 100 tokens en anglais, et
57 200 avec les fichiers qu'elles lisent (avec o200k, un tokenizer public, c'est-à-dire une façon de
découper le texte en tokens). En français, il en faudrait de 5 300 à 8 700 de plus, payés à chaque
étape lancée : une fois par tâche pour l'agent qui la développe, et une fois par récit pour celui
qui le relit. Celui de Claude n'est pas public : le ratio vient donc des tokenizers publics. Avec
`ANTHROPIC_API_KEY`, l'outil ajoute le nombre exact de tokens selon Claude.

## Outils

`tools/token_estimate.py` compte ce que les compétences coûtent en tokens et compare deux
versions, appariées par nom de dossier ou avec `--map EN=FR`. Cet outil est repris de cadrer.

```sh
uv run tools/token_estimate.py skills                       # les consignes seules
uv run tools/token_estimate.py skills --files               # avec references/ et templates/
uv run tools/token_estimate.py skills chemin/vers/fr/skills  # anglais contre français
```

`--detail o200k` donne le détail par compétence, `--only o200k` ne charge que ce tokenizer et
`--json` donne les chiffres.

## Licence

cadrer-x est sous licence MIT : voir [`LICENSE`](LICENSE). Seule exception :
`skills/cadrer-x-design-system/direction.md`, adapté de la compétence frontend-design d'Anthropic,
reste sous licence Apache-2.0
([`LICENSE-frontend-design.txt`](skills/cadrer-x-design-system/LICENSE-frontend-design.txt)).
