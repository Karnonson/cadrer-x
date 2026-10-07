# Going online — the plan on a yes, then the real address checked

From `rendre`'s *After the merge*: **En ligne** `pas encore`, or a later feature merged into a product
online.

Read `{docs}/architecture.md` (**Pièces**, **Secrets**, **Données**, **Coût**, **Trajet**, **À faire**),
`cadrer-x.yml` → `envs` (per environment: `url`, `deploy`, `rollback`), the feature's `livraison.md`,
and `decisions.md` → **À faire**. Then the host the deploy uses, read with the tools at hand, never
asked: the remote, the token's scopes (`gh auth status`), the repo and who sees it (`gh repo view`),
whether the site is on (`gh api repos/<owner>/<repo>/pages`); the plan's rows use it. No repo out there
yet: one question, who may see the code and what each choice costs; never what their account allows.
The main checkout is clean, on main, at the merge (*After the merge* pulled it); note the commit you
put online.

**What the person prepares by hand.** Each open `avant la livraison` item that rendre's *`livraison.md`
and `pr.md`* gives the person (one an agent can do here is a plan row), and a login or scope the plan
needs and the token lacks, with its command (`gh auth refresh -s workflow` for a workflow file), in one
message, in order: what, where, why, what it costs. One that spends money gets its own yes, with the
amount, before they do it. **A secret's value never passes through this conversation**: give them the
page to paste it, or a command for a terminal of their own, into the place **Secrets** names; run a
command here only when neither it nor its output holds a secret. When they say done, check each one you
can without showing a value (the account lets you in, the address answers, a secret exists by name, a
value left its local stand-in, compared never printed) and tick it in its file; one nothing here can
check is ticked on their word, `confirmé par la personne`. One that fails: say what you saw; go no
further until it passes or they drop it. Dropping one a part of the product needs: say what its users
lose, ask whether to go on without it.

**The plan, before anything leaves this computer.** One table, in a message, in order: the action ·
what it creates, changes, sends or deletes out there · what it costs now and per month · how to undo
it. Real data starts empty or from what the person gives, never local test data; a change to
kept data is a row that says how to get it back. The cost alert **Coût** names and the copies
**Données** relies on are rows. Whether the host serves a private repo's site, the row that turns it on
settles by trying, and says so. The last row is the check online. Then the question, naming this plan;
a changed row is shown again; a row that spends money gets its own yes, with the amount. A no, or not
now: say what is ready, write nothing.

**Run it.** The rows in order, from the commit you noted, one line per result. Never a secret's value in
code, a commit, a tracked file, or a command whose output is shown. A row that fails: stop, say what you
saw, undo the rows run only if they say so, and write `livraison.md` with what is out there now (each
row run, what it created, spent or sent; the failed row under **À faire**), committed as
`livraison — arrêtée : <row>`: the next run skips what is still out there. The commands that worked go
in `cadrer-x.yml` → `envs` (`url`, `deploy`, `rollback`) for the next release.

**Check online.** On the real address, follow **Trajet** as the person would, then each scenario of the
feature that shows from outside, with a browser tool if you have one, and the person's own address or
account for anything sent, never someone else's. What you can't see (their inbox): ask them to look,
write what they said. A screenshot of each screen reached, `{feature}/captures/livraison-<état>.png`.
Remove what the check created, as planned. Wrong online, right locally: say it plainly; back to
what was online before (the plan's undo) or left up is their choice.

**Write and commit.** `livraison.md`: **En ligne** (the address, the date, the commit, the version),
**Mise en ligne** (the commands in order to do it again, secrets by name), **Vérifié** (each step of the
Trajet and each scenario checked: seen, or what was seen instead, with its capture), **En cas de
problème** (back to the previous version, the data back as **Données** says, where to look when it
stops), **À faire** (by rendre's *`livraison.md` and `pr.md`*; each thing found wrong online, a
`/cadrer-x-choisir` line). Lint it as that section says. Commit `livraison.md`, `architecture.md`,
`cadrer-x.yml` and the captures on main: `livraison — <adresse>`; push it only when a plan row said
so.

End with: the address, what was checked and seen, what is wrong online if anything, and the first thing
to do now.

## Red flags

| Thought | Instead |
|---|---|
| "Paste the API key here and I'll set it." | Never through the conversation: the page, or their own terminal. |
| "A one-line fix and the check online passes." | No code here: **À faire**, then `/cadrer-x-realiser`. |
| "I'll ask whether they have a paid plan." | What the host can tell, read it; what it won't, try and read the answer. |
