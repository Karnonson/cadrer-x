# cadrer-x

Skills for Claude Code and codex that take someone who doesn't code from an idea to software online:
`init`, then Choisir, Affiner, Découper, Réaliser, Examiner, Rendre. Free, for a francophone audience.
This repository holds the skills only; marketing, the course and lead magnets live elsewhere.

## Where things are

- `skills/cadrer-x-<name>/`: one skill each. `SKILL.md`, and as needed `references/` (read when the
  skill says), `templates/` (the files it writes), `scripts/lint.py` (checks those files),
  `agents/openai.yaml` (codex).
- `docs/vision.md`: why cadrer-x exists and for whom. `docs/roadmap.md`: what comes before and after
  v1. `docs/conventions.md`: every file name, heading, label and id the skills write and read, and
  which skill does what. Read the conventions before changing a skill.
- `install.sh`: installs the skills into a project (`.claude/skills`, `.agents/skills`) or globally.
- `tools/token_estimate.py`: what the skills cost in tokens.

## Writing a skill

- A skill's `name` and `description`: French. Its body: English, instructions to the model. What it
  says to the person and the prose it writes: their language.
- File names, headings, labels and ids (`US1`, `T01`, `SC1`, …) are fixed, in French, accents
  included, as `docs/conventions.md` lists them: other skills and the lints find them by name. Change
  one only with the conventions, every skill that reads it, its template and its lint, in the same
  commit.
- A helper (`tdd`, `securite`, `debug`, `modules`, `design-system`, `textes`) has
  `user-invocable: false` and `allow_implicit_invocation: true` in its `agents/openai.yaml`; a skill
  loads it by reading `../cadrer-x-<name>/SKILL.md` at the moment it names.
- In a skill's instructions: the person using cadrer-x decides the product only, so the skill never
  asks them a technical question, and nothing that can't be taken back (a merge, a push, going online,
  a payment) happens without their yes. This is about cadrer-x's users, not about working on this
  repository: here, technical questions to the owner are fine.
- Short sentences, plain words, prose wrapped near 100 columns. A rule appears once; other files point
  to it.

## Checking a change

There is no test suite. Before a commit:

- `git diff --check`, and `bash -n install.sh` when it changed.
- A changed template or format: write a sample file and run the skill's lint on it, for instance
  `python3 skills/cadrer-x-decouper/scripts/lint.py taches <dir>/taches.md` (each lint's docstring
  gives its usage).
- A changed install: `./install.sh --link <scratch dir>` and look at what landed there.
- Size: `uv run tools/token_estimate.py skills`.

## Git

- Work on a branch; `main` is what the one-command install fetches from GitHub, so a change reaches
  people only once it is merged and pushed.
- Commit on the branch freely; merge into `main` only on the owner's go.
- Commit subjects: `<area>: <what changed>`, lowercase (`skills: …`, `install: …`, `docs: …`).
