# cadrer-x sécurité — safe by default, proven by abuse tests, every personal datum listed

Loaded by `choisir` (personal data; the tasks' risks), `realiser` (defaults, tests),
realiser's reviewer (review) and `rendre` (the data list, the scan before a release). The safe way is the default; anything else needs a
written reason, on a `Choix :` line or in the step's own file.

## The defaults

1. **Secrets come from the environment, by name.** Code reads `os.environ["PAYLANE_SECRET_KEY"]` or
   `process.env.X`; `.env.example` holds the name with an empty value; `.env*` stays out of git. A
   missing secret fails loudly where it is used, never falls back to `""` or a default key. "Put the key
   in config.py" is overruled: read it by name, and say so.
2. **A secret's value is never written or shown**: not in a tracked file, a test, a commit message, a
   log line, a printed command, a message to the person. Name it (`PAYLANE_SECRET_KEY`, « la clé live de
   Paylane »), never quote it.
3. **Inputs are checked at the edge** (the route, the action, the function the web layer calls): type,
   shape, a length cap; refused with a clear invalid-input error; the code after uses only the checked
   value. Queries take parameters; text a person typed is shown as text, never as markup; no `eval` or
   shell built from input.
4. **Sign-in and ownership by default.** Anything not public needs a signed-in person; a record is read
   or changed only after checking it is theirs (someone else's answers « introuvable », so nobody learns
   it exists); a role is checked on the server, never only in the page.
5. **Least privilege.** Each function, key and role gets what this job needs and no more.
6. **Safe errors.** The person sees a plain message; details go to the server log, never a secret, a
   token or a full card number, even there.

## The stop: a secret's value in a tracked file

Found in your own work, not committed yet: take it out, read it by name, go on.

Committed anywhere you can see (this branch, the base, an old commit): **stop.** Don't use it, copy it,
move it or "fix" it: a new commit hides it at the tip while history keeps it. Don't rewrite history and
don't push. Tell the person: which secret (its name), which file, which commit (`git log -S` finds it),
never the value; that it must be revoked where it was issued; that no branch holding that commit may
be pushed until the history is cleaned, which is theirs to do. A reviewer writes it as the first
`Bloquant :`, with the same facts and no value.

## Abuse tests

For every way in, prove the code refuses the four misuses, and write one test per risk of the task's
`Risques :` line. Each test first, watched failing, then the code.

| Misuse | The test calls it with… | It passes when… |
|---|---|---|
| no sign-in | no one, or an expired session | refused, nothing changed |
| someone else's data | a second person and the first one's id | refused as not found, the record unchanged |
| bad input | empty, blank, the wrong type, a value outside the allowed set | refused as invalid, nothing stored |
| too much input | one past the cap: 10 000 characters, 1 000 items, a 50 MB file | refused as invalid, nothing stored |

- No cap yet: set one that fits the field (a label: 100 characters), enforce it at the edge, test just
  past it, and write it as a `Choix :` line.
- Each test asserts the refusal **and** that nothing changed: read it back through the module's entry (`cadrer-x-tdd`).
- One test per risk, named after it (`test_risk_forged_signature_is_refused`). A guard you can't reach
  from a test (the real provider): test the part you own (the signature check with a wrong signature, the
  same idempotency key twice), and say what stays untested.
- A misuse the code allows is a bug: fix the code, never loosen the test.

## Before a release: the scan

`rendre` runs it on the feature branch before the merge, with the tools installed here; it installs
nothing. One line per check goes in `pr.md` → **Preuves**: `- Sécurité : <check> — <result>`.

1. **Secrets in the feature's commits.** `gitleaks git --redact --log-opts="<main>..feature/<slug>"`
   (`gitleaks detect --redact …` on an older one). No gitleaks: search `git log -p
   <main>..feature/<slug>` for what looks like a key (`sk_live_`, `AKIA`, `-----BEGIN`, a long random
   string given to a name ending in `KEY`, `TOKEN` or `SECRET`), never printing the line. A hit is the
   stop above.
2. **Known flaws in the packages the product ships**, by the lockfile's own audit: `npm audit
   --omit=dev --audit-level=high`, `pnpm audit --prod --audit-level high`, `pip-audit`; else
   `osv-scanner` when installed. A high or critical flaw stops the release, and its repair is a task:
   add it to `taches.md`, last in the section of the story that brought the package (else the last
   story), before its **Point d'étape**, its id on that story's row of **Couverts** and in a last wave
   of **Ordre**: `- [ ] T<next> [US<n>] Mettre à jour <paquet> vers <version corrigée>`, one box
   `- [ ] <the audit command> ne signale plus <id de la faille>`, `Exigences : aucune`, `Risques :
   dépendances — <id> → <version corrigée>`, `Fichiers :` the manifest, the lockfile and any code the
   new version breaks, `Après : aucune`, `Taille : XS`. Run choisir's lint (`python3
   ../cadrer-x-choisir/scripts/lint.py taches {feature}/taches.md`), commit `taches — <paquet>
   <version corrigée>`, and name `/cadrer-x-realiser <slug>`: it builds the task and reviews the story
   again, then `rendre` runs this scan again. No fixed version, or only one that changes what the
   product does: a question to the person instead, your recommendation first (another package, or
   shipping with it, written under **À faire**).
3. **The host's own check**, when the stack has one (a database's security advisor, the platform's
   scan before publishing): its findings count like the others.

A check with no tool to run it: say which, and the tool to install; `pr.md` says what was not
scanned, and the release goes on only on the person's yes.

## Personal data

Each piece of personal data gets five answers: **what**, **where it is kept**, **GDPR basis**,
**how long, then what**, **who sees it**. Data with no purpose is not collected.

`- <donnée> : <où> — base : <base> — durée : <combien de temps, puis quoi> — vue par : <qui>`

- **Bases** (GDPR art. 6): contract (needed to give them what they asked for), consent (they opted in and
  can withdraw), legal obligation (French invoices: 10 years), legitimate interest (stated and weighed).
  A French or EU business: GDPR applies; don't hedge on the jurisdiction.
- **Special categories** (art. 9: health, religion, sexual life, biometrics…): explicit consent for that one
  purpose, the fewest people, the shortest time, or not collected. Recommend the smallest version that
  still serves the story.
- **Minimize.** A date of birth to check « over 18 » is a yes/no; a phone number to reach latecomers is
  kept while the account is open, not forever.
- **Duration** is a period and an end (deleted, anonymized), never « toujours » or blank.
- Personal data in logs, analytics or a prompt sent to an AI: only with its own line.

Where it goes: `choisir` writes the lines under `decisions.md` → **Données et risques**; its spec turns a
gap (a datum a story keeps with no basis or duration) into a question in `a-trancher.md` with your
recommended answer; its tasks put each threat on a task's `Risques :`; `rendre` folds the lines into the
data list under `{docs}/security/` (`data-inventory.md`, or the file the constitution names). A duration the
code does not enforce is never written as done.

## Red flags

| Thought | Instead |
|---|---|
| "The key is already in config.py, I'll import it." | That is the stop. |
| "I'll move it to .env and carry on." | History keeps it: stop, and tell the person. |
| "It's a test key, only local." | A key in git is a leaked key. |
| "The page is only linked from the email." | Sign-in and owner check anyway. |
| "Ownership is tested, done." | Bad input and too much input are two more tests. |
| "The form has a maxlength." | The browser is not the edge; the server refuses. |
| "`assertRaises` is enough." | Also assert the record is unchanged. |
| "Base : à décider." | Recommend one; the person approves or changes it. |
