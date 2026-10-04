# The code layout

The framework's way first, whole. Where it leaves the layout open, the same shape in every cadrer-x
project: the product cut into modules, each with one entry. Read by `init` (**Modules**), `ranger`
(moving old code there), `decouper` (where each task's files go), `realiser` (where a new file goes)
and `examiner`. This file answers where code goes: never ask the person, and never call a project too
simple for it; projects grow.

## The framework's way wins

When the framework has its own way to lay out code, in its docs or its generator, cadrer-x uses it as it
is and adds nothing over it: its folders, its unit of code, where its tests and migrations go, its
names. Rails' `app/models`, `app/controllers` and `test/`; Django's apps with their `models.py`,
`views.py` and `tests.py`; Laravel's `app/`; NestJS and Angular modules with their `*.spec.ts` beside
the code; Mastra's `src/mastra/agents`, `tools`, `workflows`. Then:

- **A module is the framework's own unit** (a Django app, a NestJS module, an Angular feature folder),
  or, with none, an area of the product inside the framework's folders.
- **Its entry is what the framework makes public** (a NestJS module's exports, a Django app's views or
  services the project already calls). **Modules** names it, and the borders hold through it.
- Never a `src/modules/` beside a framework that already says where code goes, never a second `src/`,
  never a framework file moved or renamed.

## What the framework leaves open

Only what the framework says nothing about (Next.js outside `src/app/`, Express, Fastify, Hono, Flask,
FastAPI, a plain Vite app, a static site with no framework, a library) takes this tree:

```
src/                          the framework's own src/ when it has one (no src/src/)
  <the framework's folders>   app/, pages/, routes/… thin: they call a module's api
  modules/
    <module>/                 one area of the product, named with a word from Mots
      api.<ext>               its entry: the only file pages, other modules and tests import
      ui/                     its screens' parts (none when it has no screen)
      server/                 its rules and actions
      data/                   its queries: the only folder that reaches the database
  shared/                     what several modules use and that holds no rule of the product
    ui/                       the design system's parts in code
    db.<ext>                  the database client
    <helper>.<ext>            dates, amounts, ids…
tests/
  modules/<module>/           a module's tests, through its api.<ext>
db/migrations/
  0001_init.sql               one file per schema change, never edited once shipped
```

- **A module is an area of the product** (inscriptions, factures, membres), never a layer or a tool
  (`utils`, `services`, `hooks`). A feature that needs a new one says so on its **Impact archi** line;
  `rendre` adds it to **Modules** when the feature ships.
- **`api.<ext>` is the door.** It exports the functions and types others may use, and calls the
  module's own `server/`. No other module, page or test imports another module's `ui/`, `server/` or
  `data/`.
- **Each layer talks only to the next**: `ui/` → `server/` → `data/` → the database. A page or `ui/`
  never imports `data/` or `shared/db.<ext>`.
- **`shared/` never imports a module**, and only a `data/` folder imports `shared/db.<ext>`. A function
  that names a word of the product (an inscription, a place left) holds a rule: it belongs to a module.
- **Tests mirror the modules**: `tests/modules/<module>/` tests through `api.<ext>`. A task that renames
  or moves a module moves its tests folder in the same commit.
- **Migrations** go in `db/migrations/`, numbered, unless the ORM keeps its own folder (Prisma, Drizzle):
  its folder wins.
- **A layer only when the module has it.** A module with no server has no `server/`; one that keeps
  nothing has no `data/`.
- **The language's rules win too.** Python: imports go through the package, so the tree sits inside it
  (`src/<package>/modules/<module>/api.py`, `src/<package>/shared/`). Go: tests beside the code
  (`*_test.go`).

## A static site, no framework

Plain HTML, CSS and JavaScript, with or without a small build script:

```
src/
  index.html                  the pages: markup only, one <script type="module" src="main.js">
  main.js                     wires the modules to the page, nothing else
  styles.css                  the design system's tokens, then the page's own
  modules/<module>/api.js     loaded with import; ui/ for the parts it draws
  shared/                     helpers several modules use
public/                       copied as they are: favicon, images, fonts
tests/modules/<module>/       through api.js, with the runner the project has (node --test by default)
dist/                         what the build makes from src/ and public/: never edited by hand
```

No build step, the host serving the repo as it is: `index.html` stays where the host serves it, and
the code still goes in `src/`. One big page with inline scripts is not a layout: its code goes into
modules, through `/cadrer-x-ranger`.

## An existing project

`init` maps the code where it is, and never moves it. Code laid out neither the framework's way nor
this way: `init` writes the target layout under **Modules** and a line under **À faire**, and offers
`/cadrer-x-ranger`, which moves it one module at a time, nothing in the product changing. Until it is
done, **Modules** says where things are, and the map is what each step checks; a feature's new code
already goes where the layout puts it.
