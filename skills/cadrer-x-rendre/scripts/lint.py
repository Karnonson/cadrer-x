#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's livraison.md or pr.md, as the person and the next release read them.

    python3 lint.py livraison <feature>/livraison.md
    python3 lint.py pr <feature>/pr.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0. It checks
the headings and labels by name, the version against the CHANGELOG, each story against spec.md and
each picture's path against the repo, never whether the words are right: that is the person's.
"""
import re
import subprocess
import sys
from pathlib import Path

LIV_H2 = ["Version", "Livré", "En ligne", "Mise en ligne", "Vérifié", "En cas de problème", "À faire"]
PR_H2 = ["Résumé", "Preuves", "Risque de fusion"]
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def read(p):
    return p.read_text(encoding="utf-8") if p.is_file() else None


def leftovers(lines, where, out):
    for i, l in enumerate(lines):
        if "<!--" in l:
            out.append(f"{where}:{i + 1}: a template comment is left")
        elif re.search(r"<[^<>`\s][^<>`]*>", re.sub(r"`[^`]*`", "", l)):
            out.append(f"{where}:{i + 1}: a `<…>` placeholder is left")
        elif "NNNN-<slug>" in l or "NNNN-x" in l:
            out.append(f"{where}:{i + 1}: a template path is left")


def sections(lines, names, where, title_word, out, repeat=False):
    """The title, then these `##` headings in order (repeat: several releases, each a full run of them).
    Returns the first run's {name: [(line_no, text), …]}."""
    first = next((l for l in lines if l.startswith("#")), "")
    if not re.match(rf"^# \S.* — {title_word}$" if title_word else r"^# \S", first):
        out.append(f"{where}:1: the first heading is the title `# <Titre>{' — ' + title_word if title_word else ' <x.y.z>'}`")
    h2 = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    got = [t for _, t in h2]
    first_run = got[:len(names)]
    if first_run != names:
        for n in names:
            if n not in got:
                out.append(f"{where}: `## {n}` is missing")
        if all(n in got for n in names):
            out.append(f"{where}: the headings go {', '.join(names)}, in this order")
    for i, t in h2:
        if t not in names:
            out.append(f"{where}:{i + 1}: `## {t}` is not a heading of this file")
    if not repeat and len(got) > len(names) and got[:len(names)] == names:
        out.append(f"{where}: each heading appears once")
    body = {}
    for k, (i, t) in enumerate(h2[:len(names)]):
        end = h2[k + 1][0] if k + 1 < len(h2) else len(lines)
        rows = [(r + 1, lines[r]) for r in range(i + 1, end) if lines[r].strip() and "<!--" not in lines[r]]
        body[t] = rows
        if not rows:
            out.append(f"{where}:{i + 1}: `## {t}` is empty")
    return body


def repo_top(folder):
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=folder, capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 else None


def changelog_versions(folder):
    top = repo_top(folder)
    for d in ([top] if top else []) + [folder.parent.parent.parent]:
        c = read(d / "CHANGELOG.md") if d else None
        if c is not None:
            return set(re.findall(r"^## \[?(\d+\.\d+\.\d+)\]?", c, re.M))
    return None


def lint_livraison(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()
    leftovers(lines, where, out)
    body = sections(lines, LIV_H2, where, "livraison", out, repeat=True)

    v = body.get("Version") or []
    if v and not VERSION.match(v[0][1].strip()):
        out.append(f"{where}:{v[0][0]}: the first line under `## Version` is the version alone (`0.2.0`)")
    elif v:
        known = changelog_versions(folder)
        if known is not None and v[0][1].strip() not in known:
            out.append(f"{where}:{v[0][0]}: CHANGELOG.md has no `## [{v[0][1].strip()}]` entry")

    spec = read(folder / "spec.md")
    stories = set(re.findall(r"^### (US\d+) — ", spec, re.M)) if spec else None
    named = set()
    for n, l in body.get("Livré") or []:
        named |= set(re.findall(r"\bUS\d+\b", l))
    if stories is not None:
        for us in sorted(stories - named, key=lambda s: int(s[2:])):
            out.append(f"{where}: `## Livré` does not name {us}")
        for us in sorted(named - stories):
            out.append(f"{where}: {us} under `## Livré` is no story of spec.md")

    online = body.get("En ligne") or []
    if online:
        t = online[0][1].strip()
        if t == "pas encore":
            pass
        elif t.startswith("aucun — "):
            pass
        elif not re.search(r"https?://\S+", " ".join(l for _, l in online)):
            out.append(f"{where}:{online[0][0]}: `## En ligne` is `pas encore`, `aucun — <pourquoi>`, or the address (https://…), the date, the commit")
        else:
            for name in ("Mise en ligne", "Vérifié", "En cas de problème"):
                rows = body.get(name) or []
                if rows and rows[0][1].strip() == "pas encore":
                    out.append(f"{where}:{rows[0][0]}: online, so `## {name}` says what was done, not `pas encore`")

    for n, l in body.get("À faire") or []:
        if l.startswith("- ") and l.strip() != "- aucun" and not l.startswith(("- [ ] ", "- [x] ")) and "à la main" not in l \
                and "/cadrer-x-" not in l:
            out.append(f"{where}:{n}: an À faire line is the person's (*à la main*) or names the skill that turns it into work")
    return out


def lint_pr(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()
    leftovers(lines, where, out)
    body = sections(lines, PR_H2, where, None, out)

    res = body.get("Résumé") or []
    if len(res) > 8:
        out.append(f"{where}:{res[0][0]}: `## Résumé` is three to five lines")
    pre = body.get("Preuves") or []
    if pre and not any("Vérifs" in l for _, l in pre):
        out.append(f"{where}:{pre[0][0]}: `## Preuves` names the checks run (`- Vérifs : …`)")
    top = repo_top(folder)
    for n, l in pre:
        for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", l):
            if img.startswith(("/", "http", "./", "../")):
                out.append(f"{where}:{n}: `{img}`: a picture's path starts at the repo's top")
            elif top and not (top / img).is_file():
                out.append(f"{where}:{n}: `{img}` is not in the repo")
    risk = body.get("Risque de fusion") or []
    texts = [l for _, l in risk]
    if not any(re.match(r"^\*\*Porte\*\* : (aller-retour|aller simple)$", l.strip()) for l in texts):
        out.append(f"{where}: `## Risque de fusion` has `**Porte** : aller-retour` or `**Porte** : aller simple`")
    if not any(re.match(r"^\*\*Portée\*\* : \S", l.strip()) for l in texts):
        out.append(f"{where}: `## Risque de fusion` has `**Portée** : <qui le remarquerait, et quoi>`")
    return out


def main(argv):
    if len(argv) != 3 or argv[1] not in ("livraison", "pr"):
        print("\n".join(l.strip() for l in __doc__.strip().splitlines()[2:4]), file=sys.stderr)
        return 2
    path = Path(argv[2])
    if not path.is_file():
        print(f"{path}: no such file", file=sys.stderr)
        return 1
    out = (lint_livraison if argv[1] == "livraison" else lint_pr)(path)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
