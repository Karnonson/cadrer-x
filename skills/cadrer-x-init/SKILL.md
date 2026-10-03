---
name: cadrer-x-init
description: "Préparer le projet. À lancer une fois par projet, avant sa première fonctionnalité, ou quand sa vision ou son organisation est à refaire. Deux étapes : la vision (pour qui, le problème, le succès, faire ou louer un outil qui existe), puis l'organisation (`cadrer-x.yml`, `docs/architecture.md`, `docs/constitution.md`, `AGENTS.md`, et les docs déjà là rangés à leur place). Ne construit aucune fonctionnalité."
disable-model-invocation: true
argument-hint: "[le produit en une phrase]"
---

# cadrer-x init — the vision, then the layout

You set the project up with the person, once, before its first feature. Two steps, each ending in
files on one branch: the vision (`{docs}/vision.md`), then the layout (`cadrer-x.yml`,
`{docs}/architecture.md`, `{docs}/constitution.md`, `AGENTS.md`, and the docs already there moved to
their place). No feature, no code: the first task of the first feature sets up whatever code needs.

Talk, and write the files' text, in the person's language; in French, *tu* or *vous* as they write,
*vous* when you can't tell, and never both. File names, headings and labels stay exactly as written
here, in every language: the later skills find them by these names.

## Which step

Read first: the README, the manifest (package.json, pyproject.toml, Makefile…), `cadrer-x.yml` (`docs:`,
default `docs`), `{docs}/`, `git log --oneline | head`, `git branch --list 'chore/cadrer-x-init'`.

- No `{docs}/vision.md`, on the main branch or on `chore/cadrer-x-init`: **step 1**.
- A vision and no `cadrer-x.yml`, `{docs}/architecture.md`, `{docs}/constitution.md` or `AGENTS.md`:
  **step 2**, for what is missing.
- Everything there: a revision. Ask which file changes and what changed; ask only that. A change to
  `{docs}/constitution.md` is never made here: it goes through an ADR (see step 2).
- Not a git repository: say it will become one, and on their yes `git init` and commit the files as
  they are (or an empty README when there are none) as `init`.

**The branch.** Both steps write on `chore/cadrer-x-init`, in its worktree, so the main checkout stays
as it is: add `.worktrees/` to `.git/info/exclude` if it is not there, then
`git worktree add -b chore/cadrer-x-init .worktrees/chore.cadrer-x-init <main branch>` (or reuse it
when it exists). Commit each step there. The main branch is never written to without the person's yes.

## Every turn, both steps

- **One question per message**, the one that unblocks the most, with your answer: a guess and how sure
  you are, or a recommendation a plain "oui" accepts. One question has one thing to answer: never two
  asks joined by "and" or "or".
- With the AskUserQuestion tool: one question per call, your answer as the first option, the context
  in your message just before it. No tool, or it fails: write the question in your reply, and your
  turn ends there. Never say a question was asked elsewhere or will come separately.
- When a background check reports after your question, the message it triggers ends with the open
  question repeated whole, never a pointer to it.
- **Facts are looked up, never asked**: what the repo holds, what exists, what it costs today. Read
  them, or hand them to a subagent and ask something else meanwhile; what you handed off, you don't
  also look up yourself. They decide; they never research.
- **Plain words.** No file names, formats or code in a question. Never a question only a developer
  could answer.
- **Only an explicit yes closes a step** ("oui", "c'est ça"). "Ça me va", "comme tu veux" are not one:
  ask what they would change.

## Step 1 — the vision

**First turn.** Start the research on what already exists — it takes longest — in a subagent in the
background: the product in one sentence, who it is for, the problem as you understand it; for each
kind of alternative (existing products, open-source tools, no-code such as forms, Airtable or Notion,
a plain spreadsheet or a paper routine) what it does for this problem, its monthly cost at this size,
what it lacks, with links. No way to run it in the background: do it yourself after their first
answer. Then one message: one line saying you are checking what already exists and that using one of
those instead of building is a good ending, then Q1.

Format, without the tool, in their language:

```
**Q1 · Pour qui** — <the question in plain words, two or three choices when they help>
➡️ Mon idée : <what you expect, and what it rests on> — confiance ~50 % (il manque : <what>)
```

**The four sections of `vision.md`:**

- **Pour qui** — the specific people: who, how many, what they use today.
- **Problème** — what it costs them today, with the last real case.
- **Succès** — a number a non-developer can check, and a date. Theirs, not yours: ask for it; a figure
  you invent is a guess to put to them.
- **Faire ou louer** — the alternatives (what each does, costs, lacks) and the verdict.

**Faire ou louer.** When the research is back, show it as a short table (option · fait · coûte ·
manque), then one question: build, or use one of these? Recommend honestly: if a 10 €-a-month product
or a spreadsheet covers most of it, recommend it. "Louer X" ends here: `vision.md` records that
verdict, nothing gets built, step 2 does not follow — say it is a win (no code to keep alive). A build
verdict names what every option lacks that matters to them.

**Save — only after the yes.** Write back four lines (Pour qui · Problème · Succès · Faire ou louer)
and ask: "C'est bien ça ?" On the explicit yes, write `{docs}/vision.md` in the branch's worktree:

```
# <Produit> — vision
## Pour qui
## Problème
## Succès
## Faire ou louer
```

Commit it: `vision — <Produit>`. Then ask whether to do the layout now. Yes: step 2, right away. Not
now: say `/cadrer-x-init` picks it up at step 2.

## Step 2 — the layout

Four parts, in this order, each shown to the person before it is written. What the repo answers, you
don't ask.

### 1. Where things go

- **An existing repo with docs**: make a plan from `references/carte.md`, one line per path — `déplacer
  <path> → <place>`, `créer <path>`, `garder <path>` with why. Open each doc you would move (its
  heading, its first lines): the name guesses, the content decides (a `HISTORY.md` that tells the
  product's story is not a changelog). Code, assets and config never move: the framework's layout wins,
  and `architecture.md` → **Modules** maps the code wherever it is. What a file cannot settle is one
  question, with your guess. Show the plan in three or four lines (how many docs move, what is created,
  what stays and why), ask for the yes, then on the branch: `git mv` each line, fix every markdown link
  to a moved file (`git grep` the old path), and commit `docs: ranger les docs à leur place`.
- **No code yet**: nothing moves. The stack is settled in part 3.

### 2. `cadrer-x.yml`

The commands the repo defines, never invented: the manifest's scripts and the lockfile's manager
(`pnpm-lock.yaml` → `pnpm install --frozen-lockfile`), pyproject.toml, the Makefile.

```yaml
name: <repo name>
docs: docs
commands:
  install: <command>
  checks: [<command>, <command>]
  dev:
    run: <the command that starts the app>
    url: http://localhost:<port>
```

`root:` only when the app lives in a subfolder; `dev:` only when the app has screens. Tell them the
checks run after every task, so a check that fails today fails every task: run each once now, and
drop or fix a failing one with them. No code yet: `checks: []` and no `dev:`, and say the first
feature's foundation task fills them.

### 3. `{docs}/architecture.md`

From `templates/architecture.md`. **An existing repo**: fill each section from what the repo shows
(the manifest, the folders, the env files by name), and leave what you cannot tell as `(à compléter)`;
**Modules** names each code folder, what it owns, its paths. **No code yet**: settle the stack with
them first, one question per message:
1. What is already chosen or ruled out (their accounts, a host they pay for, a tool they refuse): ask
   first, and what they name is used — say so plainly when it breaks a safety rule.
2. Then two or three named setups, each with its trade-offs in plain words, your pick first: what
   each part does and where it runs; whether it must work with their computer off; whether a card is
   needed and the monthly cost at their use, looked up today; what happens at a free tier's limit;
   what they will set up by hand.
3. Follow one action of the product through the chosen parts in plain words ("tu cliques sur Envoyer
   → <part> le reçoit → <part> le garde → tu vois…") and ask what surprises them.
Each part, secret and chore lands in its section; the setups not chosen go under **Écarté**.
**Mots**, in both cases: the product's own terms, from the README, the screens and their answers
(« Inscription : jamais réservation »), so every spec and screen uses the same word.

### 4. `{docs}/constitution.md`, `AGENTS.md`

**The constitution** holds the rules every change keeps: what, if broken, puts a bug, a leak or a
liability in the product. From `templates/constitution.md`: its default rules, plus what the repo
implies (its tests, its modules), minus what does not apply (no personal data: no M3, no M4). An
existing file of rules (`principles.md`, `conventions.md`): its rules first, in this shape. Show the
rules as one table with who checks each and when, and ask which to change. Each change is one
question. The rules take effect on their yes; from then on, a rule changes only through an ADR they
approve (`{docs}/adr/`), written by `/cadrer-x-rendre` when the feature that needs the change ships.

**`AGENTS.md`** is for the agents, loaded every session: from `templates/AGENTS.md`, short — where the
docs are, the commands, a pointer to the constitution, never its rules copied in. An existing
`AGENTS.md`: add only its missing lines. No `CLAUDE.md`: create it with the one line `@AGENTS.md`, so
Claude reads the same file as codex; an existing `CLAUDE.md` gets that line if it lacks it.

**Save.** Show the files' changed lines in one message and ask for the yes. Then write them in the
branch's worktree and commit `init — organisation du projet`.

## End

Say what is on `chore/cadrer-x-init` (one line per file), then ask whether to merge it into the main
branch now. On their yes: from the main checkout, `git merge --ff-only chore/cadrer-x-init` (a merge
commit if it cannot fast-forward, on a second yes), then `git worktree remove .worktrees/chore.cadrer-x-init`
and `git branch -d chore/cadrer-x-init`. Never push. Then the next step and nothing more:
`/cadrer-x-choisir <idée>`.

## Red flags

| Thought | Instead |
|---|---|
| "The idea is clear enough to draft the vision." | Ask: who, the problem, success are theirs. |
| "Alternatives would only discourage them." | Faire ou louer comes first; using one is a win. |
| "Succès : moins de gaspillage." | Their number and their date. |
| "HISTORY.md, so CHANGELOG.md." | Open it: the name guesses, the content decides. |
| "src/lib/ should be a module, I'll move it." | Code stays; Modules maps it where it is. |
| "I'll add `pnpm test` to the checks, every project has it." | Only commands the repo defines, run once now. |
| "Prices are roughly…" | Look them up today. |
| "I'll paste the constitution into AGENTS.md." | A pointer: one file holds the rules. |
| "This rule is in the way, I'll drop it." | Rules change through an ADR they approve. |
| "Done, I'll merge into main." | Ask; merge on their yes, never push. |
