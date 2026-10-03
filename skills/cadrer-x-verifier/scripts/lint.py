#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's verification.md.

    python3 lint.py verification <feature>/verification.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0: the title,
the head lines, the two headings, each finding's prefix and the step it names, and that the verdict
follows from the findings.
"""
import re
import sys
from pathlib import Path

HEAD = [("Date", r"\d{4}-\d{2}-\d{2}", "AAAA-MM-JJ"), ("Portée", r"spec|spec et tâches", "`spec` or `spec et tâches`"),
        ("Verdict", r"à reprendre|prête", "`à reprendre` or `prête`")]
FINDING = re.compile(r"^- (À reprendre|Remarque) : \S.*→ /cadrer-x-(affiner|decouper)\s*$")


def lint(path):
    where, out = str(path), []
    lines = path.read_text(encoding="utf-8").splitlines()
    first = next((l for l in lines if l.startswith("#")), "")
    if not re.match(r"^# \S.* — vérification$", first):
        out.append(f"{where}:1: the first line is the title `# <Titre> — vérification`")
    for i, l in enumerate(lines):
        if "<!--" in l:
            out.append(f"{where}:{i + 1}: a template comment is left")
        elif re.search(r"<[^<>`\s][^<>`]*>", re.sub(r"`[^`]*`", "", l)):
            out.append(f"{where}:{i + 1}: a `<…>` placeholder is left")
    vals = {}
    for label, rx, say in HEAD:
        m = next(((i, l) for i, l in enumerate(lines) if l.startswith(f"**{label}** : ")), None)
        if not m:
            out.append(f"{where}: `**{label}** :` is missing")
        elif not re.fullmatch(rx, m[1].split(" : ", 1)[1].strip()):
            out.append(f"{where}:{m[0] + 1}: `**{label}** :` is {say}")
        else:
            vals[label] = (m[0], m[1].split(" : ", 1)[1].strip())
    h2 = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    if [t for _, t in h2] != ["Constats", "Vérifié"]:
        out.append(f"{where}: the headings are `## Constats` then `## Vérifié`, and only these")
    blocking = 0
    spans = {t: (i, h2[k + 1][0] if k + 1 < len(h2) else len(lines)) for k, (i, t) in enumerate(h2)}
    if "Constats" in spans:
        a, b = spans["Constats"]
        rows = [(r, lines[r]) for r in range(a + 1, b) if lines[r].strip() and not lines[r].startswith((" ", "\t"))]
        if not rows:
            out.append(f"{where}:{a + 1}: `## Constats` is empty: clean is `- aucun`")
        for r, l in rows:
            if l.strip() == "- aucun":
                continue
            m = FINDING.match(l)
            if not m:
                out.append(f"{where}:{r + 1}: a finding is `- À reprendre : …` or `- Remarque : …`, ending `→ /cadrer-x-affiner` or `→ /cadrer-x-decouper`")
            elif m.group(1) == "À reprendre":
                blocking += 1
    if "Vérifié" in spans:
        a, b = spans["Vérifié"]
        if not any(lines[r].startswith("- ") for r in range(a + 1, b)):
            out.append(f"{where}:{a + 1}: `## Vérifié` lists what was checked and held")
    if "Verdict" in vals:
        i, v = vals["Verdict"]
        if blocking and v == "prête":
            out.append(f"{where}:{i + 1}: `prête` with {blocking} À reprendre left: `à reprendre`")
        if not blocking and v == "à reprendre":
            out.append(f"{where}:{i + 1}: `à reprendre` with no À reprendre finding: `prête`")
    return out


def main(argv):
    if len(argv) != 3 or argv[1] != "verification":
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
