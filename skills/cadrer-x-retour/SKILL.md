---
name: cadrer-x-retour
description: "Envoyer un retour sur cadrer-x : un court rapport sur la session (quelle étape, jusqu'où, ce qui a coincé), sans rien de ton produit, montré en entier et publié en ticket GitHub sur le dépôt cadrer-x. À lancer quand tu t'arrêtes en route ou que tu as quelque chose à dire ; les autres étapes l'envoient d'elles-mêmes à leur fin si tu l'as accepté une fois. Ne touche pas au projet, sauf `retours:` dans `cadrer-x.yml`."
disable-model-invocation: true
argument-hint: "[ce que tu veux dire à cadrer-x, en quelques mots]"
---

# cadrer-x retour — what this run taught cadrer-x

cadrer-x gets better from how its steps really run: where a question came back, a lint failed, the
person had to correct you. You turn this run into a short report and send it as a GitHub issue on
`Karnonson/cadrer-x`, on a consent the person gives once, kept in `cadrer-x.yml` → `retours:`.

Talk in the person's language; in French, *tu* or *vous* as they write. The report itself is in
French, whatever their language: the owner reads them all.

## When

- **From another skill** (its last message is coming): `retours: oui`: the report, then *Send it*.
  `retours: non`, or no `cadrer-x.yml` yet: nothing, not a word; back to that skill. No `retours:`:
  the consent question below, as that message's last line; on the answer, go on as it says.
- **Run by the person** (`/cadrer-x-retour`): that is their yes for this one report, whatever
  `retours:` says. In a fresh session this conversation holds nothing: their words are the report;
  none given, one question, what went wrong or what they would change.

**The consent, once.** One question, in plain words: at the end of each step, a short report goes to
the people who make cadrer-x, so they can improve it; what it holds (the step, how far it got, what
went wrong, how many questions); never anything of their product, their words or their code; shown
whole each time; posted as a ticket under their GitHub account, visible to anyone who sees the
cadrer-x repository. Yes or no, and they can change their mind any time by saying so. Write
`retours: oui` or `retours: non` at the end of `cadrer-x.yml` and commit it alone: `retours —
<oui|non>`. Never asked again once it is there.

## The report

From this conversation only. Under 1,500 characters. These lines, each with a value or left out:

```
**Outil** : <Claude Code | codex>, <model if you know it>
**Version** : <see below>
**Étape** : <the skill, e.g. choisir> — <the furthest section reached, as this skill names it>
**Fin** : <terminée | arrêtée par la personne | bloquée : <what, in general words>>
**Durée** : <about how long, if you can tell>
**Questions** : <how many to the person> ; <any asked twice: which step, why>
**Accrocs** : <each lint failure (which lint, which rule), tool error, failed subagent, step redone>
**Corrections** : <where the person corrected you or turned down a recommendation, in general words>
**Remarque** : <what they said about cadrer-x itself, rewritten without any detail of their product>
```

**Version**: the file `version` beside this one; else, this folder being a git checkout, `git -C
<this folder> describe --tags --always`; else `inconnue`.

**Never in it**, because it is public and under their name: the product's or the feature's name,
the person's words quoted, any file's content, code, a path beyond cadrer-x's own file names, a URL,
a person's or company's name, an account, an amount, a secret. In doubt, leave it out.

## Send it

Write it to a temporary file outside the repository; title `Retour : <skill> — <section reached>`.
Show the report whole in one message, then:

- `gh auth status` logged in: `gh issue create -R Karnonson/cadrer-x --title "<title>" --body-file
  <file>`. Always `-R`: without it the ticket lands in the person's own repository. Give its address;
  to take it back, they close it there.
- No `gh`, not logged in, or refused: the link `https://github.com/Karnonson/cadrer-x/issues/new`
  with `?title=` and `&body=`, both URL-encoded. One click from them sends it; say so.

Once per run, never again in it. Then back to the message the skill was about to send.
