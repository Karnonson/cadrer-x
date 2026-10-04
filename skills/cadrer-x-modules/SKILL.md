---
name: cadrer-x-modules
description: "Aide cadrer-x, chargée par les autres étapes : les frontières entre les modules du code, telles que `docs/architecture.md` → Modules les trace. À charger quand un changement importe d'un dossier à un autre, touche deux modules, ou qu'une page, un composant ou une tâche va chercher des données ailleurs ; et pour découper, construire ou relire dans un projet qui a cette carte."
user-invocable: false
---

# cadrer-x modules — the map decides

Loaded by `decouper` (where each task's files go), `realiser` (each new import), `ranger` (each move) and `examiner` (each
crossing). `{docs}/architecture.md` → **Modules** is the map: each module, what it owns, its paths. The map
decides, not the folder names. With no map, the rules below still hold on the code's own layout.

`references/structure.md`, beside this file, is the layout: the framework's own way when it has one,
used as it is; only where it leaves the layout open, `src/modules/<module>/api.<ext>` with `ui/`,
`server/`, `data/` behind it, `src/shared/`, `tests/modules/<module>/`. Open it when you place a new
module, a new file in one, or its tests.

## The rules

1. **The framework's way wins.** Its folders, its unit of code, where its tests go (Rails' `app/`,
   Django's apps, NestJS modules): use them as they are, never move, rename or wrap them. Pages, routes
   and handlers stay thin: they call a module's entry and render. Only what the framework leaves open
   goes in `src/modules/`, as `references/structure.md` says.
2. **Each layer talks only to the next**: what is shown → the rules → what is kept → the database. A page
   or a component never imports the database client and never runs a query.
3. **A module uses another only through that module's entry** (its `api.<ext>`, or the entry the map
   names), never its tables, its internals, or a file behind its entry. Types come from the entry too.
   Where the tree applies, `src/shared/` holds no rule of the product and never imports a module; only
   a `data/` folder imports its database client.
4. **What you need is not exported by the entry?** Add a small export to that entry, calling that module's
   own code. That is the path that keeps the border, even when it touches a file the task does not list:
   in `realiser` the builder does not touch it alone: it returns `Statut : question` (`Conseil :` the export to add), and the file is named in the commit once the person has said yes.

Before each new import: find both files on the map. Same module, next layer: fine. Another module: its
entry.

## When a plan points across a border

A task's `Fichiers :` line naming one file, « a one-line import », a habit in the code: none makes a
crossing right. The map outranks the plan.

- **Cutting tasks** (`decouper`): one module per task where you can; a task that needs two names the
  entry it goes through, and that entry's file is on its `Fichiers :` line. A new module's files and its
  tests go where `references/structure.md` puts them.
- **Building** (`realiser`): take the path that keeps the map, and write it as a `Choix :` line: what the
  plan said, what you did, the file outside `Fichiers :` you touched (once the person's yes came back through `realiser`). Stop only
  when the one way through would move a framework folder or merge two modules.
- **Reviewing** (`examiner`): each crossing is a finding on the Règles axis, quoting the import or the
  query and the **Modules** line it breaks. A module the map lacks, with no **Impact archi** line in
  `decisions.md`, is a finding too, and so is a new module or file placed against `references/structure.md`
  (a `utils` module, a rule in `shared/`, tests outside their module's folder). In a feature, updating the map is
  `rendre`'s, at release.

## Red flags

| Thought | Instead |
|---|---|
| "It's a one-line query on their table." | The short path is the crossing: the entry. |
| "`Fichiers :` lists only my module." | Touching the entry is the smaller harm: ask, then name it. |
| "A server component may query directly." | It still calls its module's entry. |
| "It's only a type import." | Types come from the entry too. |
| "I'll add the new module to architecture.md." | In a feature, `rendre` does, at release. Only `init` and `ranger` write the map earlier. |
| "A `utils` module for these helpers." | A rule of the product goes in its module; the rest in `shared/`. |
| "Django has apps, but I'll add `src/modules/` for consistency." | The framework's way wins: the app is the module. |
| "The framework has its `src/`, mine goes beside or inside it." | One code root: `modules/` and `shared/` go in the framework's `src/`. |
| "This old folder isn't laid out right, I'll move it." | Moving code is a feature of its own, on the person's yes. |
