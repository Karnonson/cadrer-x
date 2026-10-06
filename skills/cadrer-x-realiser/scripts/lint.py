#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's audit.md, as realiser and rendre read it.

    python3 lint.py audit <feature>/audit.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0. It checks
the headings, labels and prefixes the later skills find by name, and that each verdict follows from its
findings, never whether a finding is right: that is the review's, and the person's.
"""
import re
import sys
from pathlib import Path

STORY_H2 = re.compile(r"^## (US\d+) \S")
H3 = ["Spec", "Règles", "Correctifs", "Non jugé"]
AXES = {"Spec", "Règles", "Correctifs"}
PREFIX = re.compile(r"^- (Bloquant|À corriger|Détail|Info|Corrigé) : \S")
BLOCKING = {"Bloquant", "À corriger"}
GAP = re.compile(r"\b(manquant|partiel|contraire|non demandé)\b")
HEAD = [("Tour", re.compile(r"^\d+$")), ("Date", re.compile(r"^\d{4}-\d{2}-\d{2}$")),
        ("Verdict", re.compile(r"^(à corriger|validé)$"))]
VERIFS = re.compile(r"^Vérifs : (lancées|pas lancées) — \S")
ECRANS = re.compile(r"^Écrans : (cliqués SC\d+|pas cliqués — \S)")


def read(p):
    return p.read_text(encoding="utf-8") if p.is_file() else None


def screens_of(passation):
    """{US<n>: [SC<m>, …]} from passation.md's `Récits :` lines."""
    out, cur = {}, None
    for l in (passation or "").splitlines():
        if m := re.match(r"^### (SC\d+) ", l):
            cur = m.group(1)
        elif cur and (m := re.match(r"^\s*-?\s*Récits : (.*)$", l)):
            for us in re.findall(r"US\d+", m.group(1)):
                out.setdefault(us, []).append(cur)
    return out


def lint(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()
    spec = read(folder / "spec.md")
    stories = set(re.findall(r"^### (US\d+) — ", spec, re.M)) if spec else None
    if spec is None:
        out.append(f"{where}: no spec.md next to it: the stories are checked against it")
    screens = screens_of(read(folder / "passation.md"))

    first = next((l for l in lines if l.startswith("#")), "")
    if not re.match(r"^# \S.* — audit$", first):
        out.append(f"{where}:1: the first heading is the title `# <Titre> — audit`")

    for i, l in enumerate(lines):
        if "<!--" in l:
            out.append(f"{where}:{i + 1}: a template comment is left")
        elif re.search(r"<[^<>`\s][^<>`]*>", re.sub(r"`[^`]*`", "", l)):
            out.append(f"{where}:{i + 1}: a `<…>` placeholder is left")

    # Story sections.
    starts = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]
    if not starts:
        out.append(f"{where}: no story section `## US<n> <titre>`")
    seen = set()
    for k, (i, l) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        m = STORY_H2.match(l)
        if not m:
            out.append(f"{where}:{i + 1}: `{l}` is not a story section (`## US1 <titre>`)")
            continue
        us = m.group(1)
        if us in seen:
            out.append(f"{where}:{i + 1}: {us} has two sections: a new tour replaces the old one")
        seen.add(us)
        if stories is not None and us not in stories:
            out.append(f"{where}:{i + 1}: {us} is no story of spec.md")
        out += section(lines, i, end, us, where, screens.get(us))
    return out


def section(lines, start, end, us, where, story_screens):
    out = []
    body = list(range(start + 1, end))
    h3 = [(j, lines[j][4:].strip()) for j in body if lines[j].startswith("### ")]
    first_h3 = h3[0][0] if h3 else end

    # The head: Tour, Date, Verdict, in order.
    head = [(j, lines[j]) for j in range(start + 1, first_h3) if lines[j].strip()]
    vals = {}
    for k, (label, rx) in enumerate(HEAD):
        if k >= len(head) or not head[k][1].startswith(f"**{label}** : "):
            out.append(f"{where}:{start + 1}: {us}: line {k + 1} under the heading is `**{label}** : …`")
            continue
        j, l = head[k]
        v = l.split(" : ", 1)[1].strip()
        if not rx.match(v):
            out.append(f"{where}:{j + 1}: {us}: `**{label}** :` is {'a number' if label == 'Tour' else 'AAAA-MM-JJ' if label == 'Date' else '`à corriger` or `validé`'}")
        vals[label] = (j, v)
    for j, l in head[len(HEAD):]:
        out.append(f"{where}:{j + 1}: {us}: only Tour, Date and Verdict come before `### Spec`")
    tour = int(vals["Tour"][1]) if "Tour" in vals and vals["Tour"][1].isdigit() else 1

    # The ### headings, in order.
    names = [t for _, t in h3]
    for j, t in h3:
        if t not in H3:
            out.append(f"{where}:{j + 1}: {us}: `### {t}` is not a heading of audit.md")
    for need in ("Spec", "Règles", "Non jugé"):
        if need not in names:
            out.append(f"{where}:{start + 1}: {us}: `### {need}` is missing")
    if "Correctifs" in names and tour < 2:
        out.append(f"{where}:{start + 1}: {us}: `### Correctifs` belongs to tour 2 and later")
    known = [t for t in names if t in H3]
    if known != [t for t in H3 if t in known]:
        out.append(f"{where}:{start + 1}: {us}: the headings go Spec, Règles, Correctifs (tour 2+), Non jugé")

    # Each axis: prefixed bullets, or `- aucun`.
    blocking = 0
    for k, (j, t) in enumerate(h3):
        stop = h3[k + 1][0] if k + 1 < len(h3) else end
        rows = [(r, lines[r]) for r in range(j + 1, stop) if lines[r].strip()]
        if t in AXES:
            tops = [(r, l) for r, l in rows if not l.startswith((" ", "\t"))]
            if not tops:
                out.append(f"{where}:{j + 1}: {us}: `### {t}` is empty: a clean axis is `- aucun`")
            for r, l in tops:
                if l.strip() == "- aucun":
                    if len(tops) > 1:
                        out.append(f"{where}:{r + 1}: {us}: `- aucun` stands alone under `### {t}`")
                    continue
                m = PREFIX.match(l)
                if not m:
                    out.append(f"{where}:{r + 1}: {us}: a finding starts `- Bloquant :`, `- À corriger :`, "
                               f"`- Détail :`, `- Info :` or `- Corrigé :` (a group is a deeper bullet, never prose)")
                    continue
                p = m.group(1)
                if p in BLOCKING:
                    blocking += 1
                    if t == "Spec" and not GAP.search(l):
                        out.append(f"{where}:{r + 1}: {us}: a Spec finding names its gap: manquant, partiel, contraire or non demandé")
                if p == "Corrigé" and tour < 2:
                    out.append(f"{where}:{r + 1}: {us}: `Corrigé :` belongs to tour 2 and later")
        elif t == "Non jugé":
            if not rows or not VERIFS.match(rows[0][1]):
                out.append(f"{where}:{j + 1}: {us}: `### Non jugé` opens with `Vérifs : lancées — …` or `Vérifs : pas lancées — …`")
            if story_screens:
                if len(rows) < 2 or not ECRANS.match(rows[1][1]):
                    out.append(f"{where}:{j + 1}: {us}: its screens ({', '.join(story_screens)}) need the `Écrans :` line after `Vérifs :`")
                else:
                    clicked = set(re.findall(r"SC\d+", rows[1][1].split("pas cliqués")[0]))
                    named = set(re.findall(r"SC\d+", rows[1][1]))
                    for sc in story_screens:
                        if sc not in named:
                            out.append(f"{where}:{rows[1][0] + 1}: {us}: `Écrans :` says nothing of {sc}")
                    for sc in clicked - set(story_screens):
                        out.append(f"{where}:{rows[1][0] + 1}: {us}: {sc} is not one of this story's screens")

    if "Verdict" in vals:
        j, v = vals["Verdict"]
        if blocking and v == "validé":
            out.append(f"{where}:{j + 1}: {us}: `validé` with {blocking} Bloquant / À corriger finding(s) left: `à corriger`")
        if not blocking and v == "à corriger":
            out.append(f"{where}:{j + 1}: {us}: `à corriger` with no Bloquant or À corriger finding: `validé`")
    return out


def main(argv):
    if len(argv) != 3 or argv[1] != "audit":
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    path = Path(argv[2])
    if not path.is_file():
        print(f"{path}: no such file", file=sys.stderr)
        return 1
    out = lint(path)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
