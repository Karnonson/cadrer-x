# cadrer-x

Des compétences pour Claude Code et codex qui mènent un projet de l'idée à la mise en ligne, une étape à
la fois, avec toi aux moments qui comptent : `init`, puis **C**hoisir, **A**ffiner, **D**écouper,
**R**éaliser, **E**xaminer, **R**endre.

Chaque étape écrit un fichier que la suivante lit, et rien ne part sans ton oui : pas de commit de spec,
pas de fusion, pas de mise en ligne. Les étapes te parlent dans ta langue ; les noms de fichiers et les
titres restent fixes, en français, pour que chaque étape retrouve le travail de la précédente.

## Installer

Dans le dossier de ton projet (par défaut : seulement ce projet) :

```sh
/chemin/vers/cadrer-x/install.sh
```

Les compétences vont dans `.claude/skills` (Claude Code) et `.agents/skills` (codex) du projet : à committer,
pour que tout le monde sur le projet ait la même version.

Pour tous tes projets à la fois : `install.sh --global`. Options : `--engine claude` ou `--engine codex` pour
un seul des deux, `--link` pour suivre ce dépôt en direct, `--remove` pour les retirer.

## Les étapes

```
/cadrer-x-init                 une fois par projet : la vision, puis l'organisation
/cadrer-x-choisir              l'idée d'une fonctionnalité, puis ses décisions
/cadrer-x-affiner <nom>        la spec (tu la valides), puis la maquette s'il y a des écrans
/cadrer-x-decouper <nom>       les tâches, rangées par récit, avec ce qui peut se faire en même temps
/cadrer-x-realiser T01         une tâche par session, test d'abord, dans son worktree
/cadrer-x-examiner US1         la relecture d'un récit, dans une autre session
/cadrer-x-rendre <nom>         la doc, la version, la fusion, puis la mise en ligne
```

Facultatif : `/cadrer-x-verifier <nom>`, un second regard sur la spec et les tâches avant d'écrire le code.

Chaque étape te dit la suivante en finissant. Une étape en deux temps (choisir, affiner, rendre) reprend
là où le fichier manque : relance-la, elle sait où elle en est.

Cinq aides se chargent seules quand une étape en a besoin : `cadrer-x-securite`, `cadrer-x-debug`,
`cadrer-x-modules`, `cadrer-x-design-system`, `cadrer-x-textes`.

## Où vont les fichiers

```
cadrer-x.yml                       les commandes : installer, vérifier, lancer
docs/vision.md  docs/architecture.md  docs/constitution.md  docs/adr/
docs/features/0001-<nom>/
  idee.md  decisions.md  spec.md  a-trancher.md  taches.md
  maquette/  passation.md  textes.md
  verification.md  audit.md  livraison.md  pr.md  captures/
.worktrees/                        un dossier par branche en cours (feature.<nom>, tache.<nom>-t01)
```

Une fonctionnalité vit sur `feature/<nom>` ; chaque tâche sur `tache/<nom>-t01`, qui rejoint la
fonctionnalité sur ton oui. Seule `rendre` pousse, et seulement sur ton oui.

Les noms, titres et libellés exacts sont dans [`docs/conventions.md`](docs/conventions.md).

## Tu viens de cadrer ?

[`docs/migration-cadrer.md`](docs/migration-cadrer.md) : ce qui change, et comment passer un projet de
`builds/<NN>-<nom>/` à `docs/features/`.

## Les tests des compétences

Chaque compétence a ses cas dans `skills/<nom>/evals/` : un projet d'exemple, la demande, et ce qu'une
bonne réponse doit faire. `baseline.md` y note ce que le modèle faisait sans la compétence.
