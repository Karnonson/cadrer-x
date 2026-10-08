# cadrer-x

cadrer-x est un ensemble de skills pour Claude Code et codex. Elles mènent un projet de l'idée
à la mise en ligne, une étape à la fois.

## Installer

### Avec Claude Code

Dans Claude Code, tape cette commande, puis redémarre Claude Code :

```
/plugin install cadrer-x --marketplace Karnonson/cadrer-x
```

Si ta version de Claude Code ne la connaît pas, tape `/plugin marketplace add Karnonson/cadrer-x`,
puis `/plugin install cadrer-x@cadrer-x`. Pour mettre à jour, ouvre `/plugin`, onglet des
marketplaces, choisis cadrer-x, puis la mise à jour, et tape `/reload-plugins`. Dans ce même onglet,
tu peux aussi activer la mise à jour automatique.

Pour que toute l'équipe d'un projet ait le plugin, lance ces deux commandes dans le dossier du
projet, puis ajoute `.claude/settings.json` au dépôt :

```sh
claude plugin marketplace add Karnonson/cadrer-x --scope project
claude plugin install cadrer-x@cadrer-x --scope project
```

### Avec codex, ou dans les fichiers du projet

Dans un terminal, depuis le dossier de ton projet :

```sh
curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex
```

La commande propose d'installer Git et Python 3 s'ils manquent. Elle place cadrer-x dans
`~/cadrer-x`, puis les skills dans `.claude/skills` et `.agents/skills` du projet. Relance-la
pour mettre à jour. Les options se mettent à la fin, par exemple `… | bash -s -- --global` :
`--global` installe pour tous tes projets, `--engine codex` pour codex seulement, `--remove` retire
cadrer-x. `~/cadrer-x/install.sh --help` donne les autres.

Choisis le plugin ou cette commande, pas les deux : chaque étape apparaîtrait deux fois.

## Les étapes

```
/cadrer-x-init               une fois par projet : la vision, puis l'organisation du code
/cadrer-x-choisir            une fonctionnalité : l'idée, la spec, la maquette, les tâches
/cadrer-x-realiser <nom>     le développement, tâche par tâche, et la relecture
/cadrer-x-rendre <nom>       la doc, la version, la fusion, puis la mise en ligne
/cadrer-x-ranger             si le code existe déjà : le ranger, sans rien changer au produit
/cadrer-x-verifier <nom>     facultatif : un second regard sur la spec et les tâches
/cadrer-x-retour [mots]      un court mot aux auteurs de cadrer-x
```

Une fonctionnalité prend trois sessions : `choisir`, `realiser`, puis `rendre`. Chaque étape finit
en te donnant la commande suivante. Tu peux t'arrêter quand tu veux : relancée, une étape reprend
où elle en était. Pour un petit changement ou un bogue, lance aussi `/cadrer-x-choisir` et
décris-le en une phrase.

Les étapes écrivent leurs fichiers dans `docs/`. Leurs noms, fixes et en français, sont dans
[`docs/conventions.md`](docs/conventions.md).

## Les retours

La première fois, une étape te demande si elle peut envoyer un court rapport à la fin de chaque
session. Si tu acceptes, ce rapport devient un ticket public sur GitHub, sous ton compte, dans le
dépôt cadrer-x. Il dit quel outil et quelle étape ont servi, où l'étape s'est arrêtée, ce qui a
coincé, combien de questions tu as eues et où tu as corrigé l'agent. Il ne dit rien de ton produit
ni de ton code, et tu le vois en entier chaque fois. Pour arrêter, dis-le à l'agent ou écris
`retours: non` dans `cadrer-x.yml`.

## Tu utilisais déjà cadrer?

[`docs/migration-cadrer.md`](docs/migration-cadrer.md) explique comment passer un projet à cadrer-x.

## Pourquoi les consignes sont en anglais

Les étapes te parlent dans ta langue. Les consignes que lit l'agent, elles, sont en anglais : en
français, elles coûteraient de 17 à 28 % de jetons (tokens) de plus, à chaque étape.
`tools/token_estimate.py` refait la mesure.

## Feuille de route

[`docs/roadmap.md`](docs/roadmap.md)

## Licence

MIT ([`LICENSE`](LICENSE)), sauf `skills/cadrer-x-design-system/direction.md`, adapté de la
skill frontend-design d'Anthropic, sous licence Apache-2.0
([`LICENSE-frontend-design.txt`](skills/cadrer-x-design-system/LICENSE-frontend-design.txt)).
