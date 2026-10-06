# cadrer-x textes — the rules, then the writing, then the check

Loaded by `affiner` (the prototype's words, `contenu.md`), `realiser` (a text the screens lack),
`examiner` (the words on screen) and `rendre` (the CHANGELOG, `pr.md`). A product's French is part of
the product: its register, its words, its punctuation. The rules are the project's, then these, not
your taste.

## 1. Find the rules

Read, each whole, before writing a word:

1. **The project's**: `{docs}/regles-ecriture.md` (the product's register, its words, its tone), and what it points
   to (a brand voice). These win where they differ from the rest.
2. **The product's words**: `{docs}/glossaire.md`: the same word for the same thing, every time.
3. **The French the product already shows** (its pages, a feature's `contenu.md`), for the register and
   the words it uses.
4. **These defaults**, below.

No `{docs}/regles-ecriture.md`: these defaults, the register the product already uses (*tu* or *vous*, never both),
and say once that the project has no rules of its own.

## 2. Write

- French written as French, never translated from English.
- One register in every text of the product.
- Short sentences: 20 words at most between two periods.
- The product's words (« membre », never « utilisateur », when the glossary says so).
- Clear, not clever: what happened, then what to do next. An error never blames the person and has no
  exclamation mark. No marketing jargon.
- Written by a person, not a machine: subject, verb, complement. No colon to set up a punchline
  (« Le résultat : … »): `Libellé : valeur` only on a line of data (« Total : 57 points »). No slogan, no
  list of three for rhythm. The product does things (« Agendo compte »), never an « on ».
- Only what is true: no feature, number, price, date or promise that the spec or the product does not back.
- Punctuation: a space before `:` `;` `!` `?` and inside « » (non-breaking where the medium allows),
  « » never straight quotes, a decimal comma (`10,5 %`), a space between thousands (`10 000 €`).
- No anglicisms: « avoir du sens », never « faire sens »; « s'inscrire », never « appliquer pour ».
- A text that varies: each form written (« 1 note contient », « 3 notes contiennent »), what varies named
  (`{mot}`).
- On a screen: a button says what it does (« Chercher », never « OK »); a field's label says what to type;
  a message fits the screen at 390 px.

## 3. Check

1. `python3 <this file's folder>/scripts/frlint.py <file>…` on every `.md` or `.txt` you wrote or changed
   (a feature's `contenu.md` holds a page's words, so it is the one linted for screens). Fix each line it
   prints and rerun until it prints nothing. It checks what a machine can: the spacing before `: ; ! ?`
   and inside « », straight quotes around French, decimal commas, thousands, a mixed *tu* / *vous*,
   sentences over 20 words, known anglicisms.
2. Then what it can't, line by line against the rules: the register, the product's words, the tone,
   nothing promised that isn't true.
3. A rule broken on purpose (a brand name kept in English, a legal text): say it, with why.

## 4. Keep what the person corrects

A correction of the words (a tone, a turn of phrase, a word they dislike) is a rule the next text will
break again unless it is written down. Fix the text, then propose the rule in one line, worded as they
said it; on their yes, add it to `{docs}/regles-ecriture.md` (created when absent: `# Règles d'écriture`, one
`- <règle>` per line), committed with the step's own files. `examiner` and any read-only step only propose it, in the report. The next feature starts from it.

## 5. Who writes what

`affiner` writes the screens' words, in the pages and in `contenu.md`, and the person approves them with
the prototype. A builder takes them word for word. A text they lack (a server error, a limit) is not the
builder's to invent: one question to the person, with the proposed text written by these rules and linted too (write it to a scratch `.md`, run `frlint.py` on it) before you put it to the person.

## Red flags

| Thought | Instead |
|---|---|
| "I know French typography; the check is a formality." | Run it. |
| "« Vous » sounds more polite on this screen." | The product's register, everywhere. |
| "People will understand « utilisateur »." | The product's word. |
| "An exclamation mark makes the error friendlier." | Say what to do next instead. |
| "It's in the code, the check can't read it." | The words live in `contenu.md` too: check that. |
| "Fixed what they said; on to the next text." | Propose the rule for `{docs}/regles-ecriture.md`. |
