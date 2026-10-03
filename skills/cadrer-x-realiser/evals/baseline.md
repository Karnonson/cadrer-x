# Baseline — cadrer-x-realiser, without the skill

Engine: Claude (opus, effort high), 2026-10-03. One run, `fleet skills eval cadrer-x-realiser --engine
claude --baseline` with `FLEET_SKILLS_SRC` pointing at this repo's `skills/`.

Fixture: `evals/fixture/`, the pottery club (Python, standard library, unittest), checked out on
`feature/inscription-ateliers`, whose folder holds a validated `spec.md` and a `taches.md` of three tasks.
T01 builds signing up, up to the seats. A test of the workshops module already fails before any change
(`list_workshops` sorts by id, not by date): an honest build names it and leaves it.

Prompt: « T01 inscription-ateliers » (the behaviour case now adds « , on y va. »: a bare id gives no language to answer in)

Output: 138 s. Working code with a real race test (it removed the lock to see the test catch it), the
pre-existing failure named and left. Then:

## What went wrong — what the skill must prevent

1. **No task worktree, no task branch**: it built in the feature's own checkout. A `[P]` task started in
   another session meanwhile would write into the same files.
2. **Outside its files**: it created `docs/security/data-inventory.md` and edited `docs/architecture.md`,
   which are `rendre`'s, while another task may be touching them.
3. **No red first**: the tests were written alongside the code; no run showed one failing on its
   assertion before the code existed.
4. **No box-to-test map**: « 8 tests cover the scenarios and the risks », with no test named per box
   or per risk.
5. **Its working messages in English**, and it ended on « je peux commiter sur
   feature/inscription-ateliers quand vous voulez »: straight onto the feature, no merge step, nothing
   committed.

What held without the skill: the race guarded in one transaction, the module borders kept, the failing
test named as not its own, nothing pushed.

## With the skill (first run)

Every judge line passed: a red run on assertions before the code, a table of each box and risk with its
test, the four misuses tested, the pre-existing failure named, `Choix :` lines in the commit, the merge
asked, not done. One check failed: the run's first whole-suite check, in the main checkout before the
worktree existed, left `__pycache__/` there, because the fixture had no `.gitignore`. A real Python
project has one; the fixture now does.
