---
name: cadrer-x-modules
description: "Aide cadrer-x, chargée par les autres étapes : les frontières entre les modules du code, telles que `docs/architecture.md` → Modules les trace. À charger quand un changement importe d'un dossier à un autre, touche deux modules, ou qu'une page, un composant ou une tâche va chercher des données ailleurs ; et pour découper, construire ou relire dans un projet qui a cette carte."
user-invocable: false
---

# cadrer-x modules — the map decides

Loaded by `decouper` (where each task's files go), `realiser` (each new import) and `examiner` (each
crossing). `{docs}/architecture.md` → **Modules** is the map: each module, what it owns, its paths. The map
decides, not the folder names. With no map, the rules below still hold on the code's own layout.

## The rules

1. **The framework's folders win.** Never move or rename what the framework expects (Next.js `src/app/`,
   Django's apps, Rails' `app/`). Pages, routes and handlers stay thin: they call a module's entry and
   render.
2. **Each layer talks only to the next**: what is shown → the rules → what is kept → the database. A page
   or a component never imports the database client and never runs a query.
3. **A module uses another only through that module's entry** (its `api.py`, its `server/index.ts`, or the
   entry the map names), never its tables, its internals, or a file behind its entry. Types come from the
   entry too.
4. **What you need is not exported by the entry?** Add a small export to that entry, calling that module's
   own code. That is the path that keeps the border, even when it touches a file the task does not list:
   in `realiser`, ask the person first, then name the file in the commit message.

Before each new import: find both files on the map. Same module, next layer: fine. Another module: its
entry.

## When a plan points across a border

A task's `Fichiers :` line naming one file, « a one-line import », a habit in the code: none makes a
crossing right. The map outranks the plan.

- **Cutting tasks** (`decouper`): one module per task where you can; a task that needs two names the
  entry it goes through, and that entry's file is on its `Fichiers :` line.
- **Building** (`realiser`): take the path that keeps the map, and write it as a `Choix :` line: what the
  plan said, what you did, the file outside `Fichiers :` you touched (after the person's yes). Stop only
  when the one way through would move a framework folder or merge two modules.
- **Reviewing** (`examiner`): each crossing is a finding on the Règles axis, quoting the import or the
  query and the **Modules** line it breaks. A module the map lacks, with no **Impact archi** line in
  `decisions.md`, is a finding too. Updating the map is `rendre`'s, at release.

## Red flags

| Thought | Instead |
|---|---|
| "It's a one-line query on their table." | The short path is the crossing: the entry. |
| "`Fichiers :` lists only my module." | Touching the entry is the smaller harm: ask, then name it. |
| "A server component may query directly." | It still calls its module's entry. |
| "It's only a type import." | Types come from the entry too. |
| "I'll add the new module to architecture.md." | `rendre` does, at release. |
