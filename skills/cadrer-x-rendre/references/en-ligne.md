# Going online — the plan on a yes, then the real address checked

Followed by `rendre` from its *After the merge*: **En ligne** `pas encore`, or a later feature merged
into a product already online.

Read `{docs}/architecture.md` (**Pièces**, **Secrets**, **Données**, **Coût**, **Trajet**, **À faire**),
`cadrer-x.yml` → `envs` (each environment: `url`, `deploy`, `rollback`), the feature's `livraison.md`,
and `decisions.md` → **À faire**. The main checkout is clean, on the main branch, at the merge
(*After the merge* pulled it); note the commit you put online.

**What the person prepares by hand.** Each open `avant la livraison` item that rendre's *`livraison.md`
and `pr.md`* gives the person (one an agent can do here is a row of the plan), in one message, in order:
what, where, why it is needed, what it costs. One that spends money gets its own yes, with the amount,
before they do it. **A secret's value never passes through this conversation**: give them the page
where they paste it, or a command to run in a terminal of their own, into the place **Secrets** names;
run a command here only when neither it nor its output holds a secret. When they say done, check each
one you can without showing a value (the account lets you in, the address answers, a secret exists by
name, a value is no longer its local stand-in, compared never printed) and tick it in its file; one
nothing here can check is ticked on their word, `confirmé par la personne`. One that fails: say what you
saw, and go no further until it passes or they drop it; if they drop an item that a part of the
product depends on, say what the people using it lose, and ask whether to go on without that part.

**The plan, before anything leaves this computer.** One table, in order: the action · what it creates,
changes, sends or deletes out there · what it costs now and per month · how to undo it. Real data starts
empty or from what the person gives, never from local test data; a change to kept data is a row that
says how to get it back. The cost alert **Coût** names is a row, and so are the copies **Données**
relies on. The last row is the check online. Wait for the yes; a changed row is shown again; a row that
spends money gets its own yes, with the amount. A no, or not now: say what is ready, write nothing.

**Run it.** The rows in order, from the commit you noted, one line per result. Never a secret's value in
code, a commit, a tracked file, or a command whose output is shown. A row that fails: stop, say what you
saw, undo the rows already run only if they say so, and write `livraison.md` with what is out there now
(each row run, what it created, spent or sent; the failed row under **À faire**), committed as
`livraison — arrêtée : <row>`: the next run skips what is still out there. The commands that worked go
into `cadrer-x.yml` → `envs` (`url`, `deploy`, `rollback`), so the next release runs them again.

**Check online.** On the real address, follow **Trajet** as the person would, then each scenario of the
feature that shows from outside, with a browser tool when you have one, and the person's own address or
account for anything sent, never someone else's. What you can't see from here (a message in their inbox):
ask them to look, and write what they said. A screenshot of each screen reached,
`{feature}/captures/livraison-<état>.png`. Remove what the check created, as the plan said. Wrong online
and right locally: say it plainly, and offer to go back to what was online before (the plan's undo) or
leave it up: their choice.

**Write and commit.** `livraison.md`: **En ligne** (the address, the date, the commit, the version),
**Mise en ligne** (the commands in order to do it again, secrets by name), **Vérifié** (each step of the
Trajet and each scenario checked: seen, or what was seen instead, with its capture), **En cas de
problème** (how to go back to the previous version, how to get the data back as **Données** says, where
to look when it stops), **À faire** (by rendre's *`livraison.md` and `pr.md`*; each thing found wrong
online, a `/cadrer-x-choisir` line). Lint it as that section says. Commit `livraison.md`,
`architecture.md`, `cadrer-x.yml` and the captures on the main branch: `livraison — <adresse>`; push it
only when a plan row said so.

End with: the address, what was checked and what was seen, what is wrong online if anything, and the
first thing to do now.

## Red flags

| Thought | Instead |
|---|---|
| "Paste the API key here and I'll set it." | Never through the conversation: the page, or their own terminal. |
| "I'll seed production with the test members." | Real data starts empty or from what they give. |
| "A one-line fix and the check online passes." | No code here: **À faire**, then `/cadrer-x-realiser`. |
