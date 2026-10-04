---
name: cadrer-x-ranger
description: "Ranger le code qui existe dans la disposition de cadrer-x (celle du framework, sinon un module par partie du produit), sans rien changer à ce que fait le produit. À lancer quand `docs/architecture.md` → À faire le demande, ou quand le code a grandi en désordre. Prouve d'abord ce que le produit fait aujourd'hui (tests, captures), puis déplace un module à la fois, les vérifs vertes après chacun, sur sa propre branche ; fait relire le tout ; fusion sur un oui. Ne construit aucune fonctionnalité."
disable-model-invocation: true
argument-hint: "[une partie du code, ou rien pour tout]"
---

# cadrer-x ranger — the code into modules, nothing changing

You move existing code to where `../cadrer-x-modules/references/structure.md` puts it, and change
nothing the product does. A move that also fixes a bug or adds a feature hides one inside the other:
this skill does neither. First you prove what the product does today; then you move one module at a
time, the checks green after each; then someone who did not move it looks for what changed. All of it
on its own branch, merged on the person's yes.

Talk, and write, in the person's language, every message included; in French, *tu* or *vous* as they
write, *vous* when you can't tell, never both. File names, headings, labels and commit messages stay as
written here.

**Helpers.** Where this file says *read `cadrer-x-<name>`*, open `../cadrer-x-<name>/SKILL.md`, beside
this skill's folder, at that moment; read it whole and follow it. Not there: go on without it.

## Where you are

Read first: `cadrer-x.yml` (`docs:`, `commands`), `{docs}/architecture.md` (**Modules**, **À
faire**), `{docs}/glossaire.md`, `git worktree list`, `git branch --list 'chore/ranger' 'feature/*'`.

- **The branch.** `.worktrees/` in `.git/info/exclude`, then `git worktree add -b chore/ranger
  .worktrees/chore.ranger <main branch>`, or reuse both. Copy the untracked `.env*` files from the repo's top (never commit them) and run `commands.install` there once, or the checks fail for the wrong reason. Everything below runs there.
- **A plan already there** (`{docs}/rangement.md` on `chore/ranger`): pick up at its first unticked
  module, and say so in one line.
- **Features in progress** (`feature/*` not merged into the main branch): each will have to take this
  in (`git merge <main>` in its worktree), and the conflicts land there. Say which, and recommend
  laying out the code once none is in progress; their call, one question.
- No checks in `cadrer-x.yml` and nothing that runs the code: the safety net below starts with one.

## 1. The target, stated

Read `../cadrer-x-modules/references/structure.md` and `cadrer-x-modules`, then the code. Where code
goes, that file answers: never ask the person, never call the project too simple for it. The
modules are areas of the product, named with words of `{docs}/glossaire.md` (never `utils`, `helpers`, `services`).
The argument names a part of the code: only that part.

Write `{docs}/rangement.md`:

```
# Rangement — <Produit>

**Cible** : <the layout in one line: the framework's way, or the tree of structure.md>
**Base** : <main branch> @ <commit>

## Avant
- Vérifs : <the command> — <its summary line>
- Écrans : <the pages and states captured, or aucun>

## Modules
- [ ] <module> — <ce qu'il possède> — depuis : <the files or functions it takes, from where>
- [ ] shared — <what several modules use and that holds no rule>

## Remarques
- <a bug or an oddity seen on the way: kept as it is, for a feature to fix>
```

Order the modules so each one moved depends only on modules already moved, or on code still in place.

**Show it, in plain words**: what each module will hold, what stays where it is (the framework's
folders, the host's files), and that nothing a person sees changes. One clear yes ("oui", "ok", "ça
va", "c'est bon"); a change asked for is folded in. Commit the plan: `rangement — plan`.

## 2. The safety net, before any move

1. Run the whole check command; read the exit code. A failure now: name it, note it under **Avant**;
   it is not yours.
2. **What no test proves yet.** For each module of the plan, the behaviours its code has today, through
   what will be its entry: a test that pins what it does now, even where it looks wrong (a wrong value
   is a **Remarque**, never fixed here). Read `cadrer-x-tdd`. Green on the code as it is. In the runner
   the project has; none: the smallest one the stack ships with (`node --test`, `python3 -m unittest`),
   and the check command learns it.
3. **The screens.** With pages and a browser tool: serve the app (`commands.dev`, else the folder on
   127.0.0.1), reach each page and each state a person can, at 390 and 1280 wide, and save a capture
   of each in `{docs}/rangement/avant/<page>-<état>-<largeur>.png`; note any console error.
4. Commit: `rangement — avant`.

## 3. One module at a time

For each module of the plan, in order:

1. **Make it**: its folder, its entry (`api.<ext>`, or what the framework makes public) exporting what
   the rest of the code uses of it.
2. **Move the code behind it.** A whole file: `git mv`, so its history follows. Part of a file: cut
   and paste, word for word; the old place calls the new entry until its callers have moved.
3. **Move the callers** to the entry, in batches, the checks green after each batch.
4. **Take the old away**: the old file or the forwarding left, once nothing calls it.
5. **The tests move with it**: to `tests/modules/<module>/` (or where the framework puts them), each
   through the entry. A test changes its import, never what it asserts.

Never changed by a move: what a person sees, a URL, a stored key (a `localStorage` key, a cookie, a
table, a column), a file the host serves by its name, an outside call. A move that would need one is a
question. The build script and the check command change only to find the files where they now are.

Then the whole check command; red: fix the move (read `cadrer-x-debug`), never the test. Tick the
module in `{docs}/rangement.md` and commit: `rangement — <module>`. Go on with the next module in the same session unless the person stops you; the ticks in `rangement.md` let `/cadrer-x-ranger` resume anywhere.

## 4. Nothing changed: the proof

1. The whole check command, fresh: green, and every test of `rangement — avant` still there, its
   assertion unchanged (`git diff` the commit of `avant` against now, on the tests).
2. The screens again, the same pages, states and widths, in `{docs}/rangement/apres/`; compare each pair
   with your own eyes. A visible difference is a move to fix.
3. **A second look.** When you can start a subagent: one with a fresh context, and this prompt, nothing
   of yours: « In `<the worktree>`, read `{docs}/rangement.md`, then `git diff <base>...chore/ranger`.
   It only moves code. Find each place where what the product does changed: a branch dropped in a move,
   a default or an order changed, an export lost, a handler no longer wired, a stored key, a URL or a
   served file renamed. Each with file:line and the old line. Change nothing; your last message is the
   list, or `aucun`. » Each real finding is fixed, with a test that would have caught it. No way to start a subagent: say so, and give the person this prompt to run in a fresh session before merging; do not merge on your own reading.
4. `{docs}/architecture.md` → **Modules**: the new map, each module with what it owns and its paths;
   its **À faire** line ticked. Commit: `rangement — fait`.

## 5. Merge — on the yes

One message: the modules now there, one line each; the tests before and after (how many, all green);
the screens compared; what the second look found and what was fixed; the **Remarques**. Then ask
whether to merge into the main branch. On their yes: from the main checkout, `git merge --ff-only
chore/ranger` (if it cannot fast-forward, ask once more before a merge commit), then `git worktree remove
.worktrees/chore.ranger` and `git branch -d chore/ranger`. Never push. Each feature in progress: say it
takes this in with `git merge <main>` in its worktree. Then the next step: `/cadrer-x-choisir <idée>`.

## Red flags

| Thought | Instead |
|---|---|
| "While I'm moving it, I'll fix this bug." | A **Remarque**; a feature fixes it. |
| "This test asserts something odd; I'll correct it." | It pins today's behaviour: only its import changes. |
| "All modules at once, then the checks." | One module, green, committed; then the next. |
| "No tests; the move is mechanical, it's fine." | The safety net first: tests and captures of today. |
| "A nicer key name for localStorage." | Stored and addressed names never change in a move. |
| "Their project is small; a `utils` folder will do." | Areas of the product, named from the glossary. |
| "The diff looks clean to me." | A second look by someone who did not move it. |
| "Moved: I'll merge into main." | Ask; merge on their yes, never push. |
