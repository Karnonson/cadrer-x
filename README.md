# cadrer-x

Des compétences pour Claude Code et codex qui mènent un projet de l'idée à la mise en ligne, une étape à
la fois : `init`, puis **C**hoisir, **A**ffiner, **D**écouper, **R**éaliser, **E**xaminer, **R**endre.

Les sept étapes sont prêtes ; l'étape facultative `verifier` et les aides arrivent.

## Installer

Dans le dossier de ton projet (par défaut : seulement ce projet) :

```sh
/chemin/vers/cadrer-x/install.sh
```

Les compétences vont dans `.claude/skills` (Claude Code) et `.agents/skills` (codex) du projet : à
committer, pour que tout le monde sur le projet ait la même version.

Pour tous tes projets à la fois :

```sh
/chemin/vers/cadrer-x/install.sh --global
```

Options : `--engine claude` ou `--engine codex` pour un seul des deux, `--remove` pour les retirer.

## Commencer

```
/cadrer-x-init        la vision du produit, puis l'organisation du projet
/cadrer-x-choisir     l'idée d'une fonctionnalité, puis ses décisions
```

Les noms, titres et fichiers que les étapes partagent sont dans `docs/conventions.md`.
