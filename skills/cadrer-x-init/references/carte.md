# Where each doc goes

Places are under `{docs}/` (`docs/` unless `cadrer-x.yml` says otherwise), except the top-level files. A
doc is placed by what it holds; its name is only a first guess.

| What it holds | Its place | Usual old names |
|---|---|---|
| Who the product serves, the problem, success | `{docs}/vision.md` | vision, product, mission, product-vision |
| The stack, the parts, where they run, the modules | `{docs}/architecture.md` | architecture, arch, system-design |
| The rules every change keeps | `{docs}/constitution.md` | constitution, principles, conventions, guidelines, engineering-rules |
| One decision each, never edited, only superseded | `{docs}/adr/NNNN-<slug>.md` | adr/, adrs/, decisions/, decision-records/ |
| One folder per feature: idea, decisions, spec, tasks | `{docs}/features/NNNN-<slug>/` | specs/, rfcs/, prd/, proposals/, features/ |
| How to deploy, restart, restore | `{docs}/runbook.md` | runbook, operations, ops, deploy, deployment |
| Threats and their guards | `{docs}/security/threat-model.md` | threat-model, threats |
| Personal data: what, where, basis, retention | `{docs}/security/data-inventory.md` | data-inventory, privacy, gdpr, personal-data |
| What went wrong and what changed after | `{docs}/postmortems/` | postmortems/, incidents/ |
| Colours, type, spacing, components | `{docs}/design-system/` | design-system/, styleguide/ |
| What changed in each version | `CHANGELOG.md` (top) | changelog, history, changes, releases, release-notes |
| Instructions for the agents | `AGENTS.md` (top), `CLAUDE.md` → `@AGENTS.md` | AGENTS.md, CLAUDE.md, GEMINI.md |
| How to run the project, the checks | `cadrer-x.yml` (top) | — |
| The app's own env variables, no real values | `.env.example` (top) | .env.sample, .env.template, .env.dist |

Stay where they are, always:

- Code, assets, config, tests, migrations: the framework's layout wins.
- README, LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT and the other top-level files GitHub reads.
- A docs site's folder (MkDocs, Docusaurus, Sphinx, Jekyll): a move breaks its navigation and its URLs.
- A doc in another markup (`.rst`, `.adoc`): renaming it `.md` would break it. Converting it is a
  change of its own, the person's call, later.
- A `.env.sample` whose values look real (a live key, a production host): tell the person before
  anything else.
