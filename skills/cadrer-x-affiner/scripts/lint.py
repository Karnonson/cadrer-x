#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's spec.md or passation.md, as the later skills read them.

    python3 lint.py spec <feature>/spec.md
    python3 lint.py passation <feature>/passation.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0. It checks
the headings, labels and ids the later skills find by name, never whether the content is right: that
is the Vérifs' and the Contrôle's job, and the person's.
"""
import re
import sys
from pathlib import Path

SPEC_H2 = ["Récits", "Exigences", "Critères", "Supposé", "Pas encore", "Vérifs"]
SPEC_H3 = {"Récits": {"Cas limites"}, "Exigences": {"Données clés"}}
STORY = re.compile(r"^### (US(\d+)) — \S.* \(Priorité : P\d+\)$")
MARKER = re.compile(r"\[À PRÉCISER : [^\]]*?→ (Q\d+)\]")
# What a person never reads in a spec: the how. Whole words, any case.
TECH = ["api", "endpoint", "csv", "json", "sql", "sqlite", "http", "https", "url", "backend", "frontend",
        "schéma", "schema", "utc", "token", "webhook", "cron", "base de données", "requête", "serveur"]
PASS_H2 = ["Maquette", "Écrans", "Nouveautés", "Accessibilité", "Ouvert", "Contrôle"]
SCREEN = re.compile(r"^### (SC(\d+)) \S")
SCREEN_LINES = ["Récits", "Fichier", "Parties", "États", "Largeurs", "Textes"]


def headings(lines):
    return [(i + 1, len(m.group(1)), m.group(2).strip())
            for i, l in enumerate(lines) if (m := re.match(r"^(#{1,6}) (.+)$", l))]


def outline(lines, where, title_word, h2_names, out):
    """The title, then exactly these `##` headings, in this order. Returns {name: (start, end)} line spans."""
    hs = headings(lines)
    if not hs or hs[0][1] != 1 or not hs[0][2].endswith(f" — {title_word}"):
        out.append(f"{where}:1: the first line is the title `# <Titre> — {title_word}`")
    got = [(n, t) for n, lvl, t in hs if lvl == 2]
    names = [t for _, t in got]
    for name in h2_names:
        if name not in names:
            out.append(f"{where}: `## {name}` is missing")
    for n, t in got:
        if t not in h2_names:
            out.append(f"{where}:{n}: `## {t}` is not a heading of this file ({', '.join(h2_names)})")
    present = [t for t in names if t in h2_names]
    if present != [t for t in h2_names if t in present]:
        out.append(f"{where}: the `##` headings are out of order: {', '.join(h2_names)}")
    spans = {}
    for k, (n, t) in enumerate(got):
        end = got[k + 1][0] - 1 if k + 1 < len(got) else len(lines)
        spans.setdefault(t, (n, end))
    return spans


def body(lines, span):
    return [(i + 1, lines[i]) for i in range(span[0], span[1])] if span else []


def leftovers(lines, where, out):
    in_code = False
    for i, l in enumerate(lines, 1):
        if l.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        if "<!--" in l:
            out.append(f"{where}:{i}: a template comment is left: remove it")
        elif re.search(r"<[a-zà-ÿ][^<>`]*>", re.sub(r"`[^`]*`", "", l)):
            out.append(f"{where}:{i}: a template placeholder `<…>` is left")


def ids_in_order(found, prefix, where, out):
    for k, (n, num) in enumerate(found, 1):
        if num != k:
            out.append(f"{where}:{n}: {prefix}{num} should be {prefix}{k}: ids go 1, 2, 3… with no gap")
            break


def questions(path):
    """{Q id: has a Conseil} from the a-trancher.md next to the spec."""
    if not path.exists():
        return None
    qs, cur = {}, None
    for l in path.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"^## (Q\d+) · ", l):
            cur = m.group(1)
            qs[cur] = False
        elif cur and re.match(r"^- Conseil : \S", l):
            qs[cur] = True
    return qs


def lint_spec(path):
    where, out = str(path), []
    lines = path.read_text(encoding="utf-8").splitlines()
    spans = outline(lines, where, "spec", SPEC_H2, out)
    leftovers(lines, where, out)

    status = next((m.group(1) for l in lines if (m := re.match(r"^\*\*Statut\*\* : (\S+)", l))), None)
    if status not in ("brouillon", "validée"):
        out.append(f"{where}: the line `**Statut** : brouillon` (or `validée` once the person said yes) is missing")

    # Stories, under Récits.
    stories, cur = [], None
    for n, l in body(lines, spans.get("Récits")):
        if l.startswith("### "):
            m = STORY.match(l)
            if m:
                cur = {"id": m.group(1), "num": int(m.group(2)), "line": n, "labels": set(), "scen": 0}
                stories.append(cur)
            elif l[4:].strip() in SPEC_H3["Récits"]:
                cur = None
            else:
                out.append(f"{where}:{n}: `{l}` — a story is `### US1 — <titre> (Priorité : P1)`")
                cur = None
        elif cur:
            for label in ("Pourquoi cette priorité", "Test seul", "Scénarios"):
                if l.startswith(f"**{label}** :"):
                    cur["labels"].add(label)
            if re.match(r"^\d+\. ", l):
                cur["scen"] += 1
    if not stories and "Récits" in spans:
        out.append(f"{where}:{spans['Récits'][0]}: no story under `## Récits`")
    ids_in_order([(s["line"], s["num"]) for s in stories], "US", where, out)
    for s in stories:
        for label in ("Pourquoi cette priorité", "Test seul", "Scénarios"):
            if label not in s["labels"]:
                out.append(f"{where}:{s['line']}: {s['id']} has no `**{label}** :` line")
        if not s["scen"]:
            out.append(f"{where}:{s['line']}: {s['id']} has no numbered scenario under **Scénarios**")

    # Third-level headings elsewhere.
    for name, span in spans.items():
        if name == "Récits":
            continue
        for n, l in body(lines, span):
            if l.startswith("### ") and l[4:].strip() not in SPEC_H3.get(name, set()):
                out.append(f"{where}:{n}: `{l}` is not a heading of `## {name}`")

    # Requirements and criteria.
    for name, prefix in (("Exigences", "EF"), ("Critères", "CS")):
        found = [(n, int(m.group(1))) for n, l in body(lines, spans.get(name))
                 if (m := re.match(rf"^- \*\*{prefix}(\d+)\*\* : \S", l))]
        if name in spans and not found:
            out.append(f"{where}:{spans[name][0]}: no `- **{prefix}1** : …` under `## {name}`")
        ids_in_order(found, prefix, where, out)

    # Questions.
    marks = [(i, m.group(1)) for i, l in enumerate(lines, 1) for m in MARKER.finditer(l)]
    if len({q for _, q in marks}) > 3:
        out.append(f"{where}: {len({q for _, q in marks})} questions are marked `[À PRÉCISER …]`: three at most")
    qs = questions(path.parent / "a-trancher.md")
    for n, q in marks:
        if status == "validée":
            out.append(f"{where}:{n}: {q} is still marked `[À PRÉCISER …]` in a validated spec")
        elif qs is None or q not in qs:
            out.append(f"{where}:{n}: {q} is not in a-trancher.md: add `## {q} · spec · <la question>`")
        elif not qs[q]:
            out.append(f"{where}:{n}: {q} in a-trancher.md has no `- Conseil : …` line")
    for i, l in enumerate(lines, 1):
        if "À PRÉCISER" in l and not MARKER.search(l):
            out.append(f"{where}:{i}: a marker is `[À PRÉCISER : <le point> → Q<n>]`")

    # The checklist.
    checks = [(n, l) for n, l in body(lines, spans.get("Vérifs")) if re.match(r"^- \[[ xX]\] ", l)]
    if "Vérifs" in spans and not checks:
        out.append(f"{where}:{spans['Vérifs'][0]}: no `- [x] <question> ? (US…)` under `## Vérifs`")
    if status == "validée":
        for n, l in checks:
            if l.startswith("- [ ]"):
                out.append(f"{where}:{n}: an unticked Vérif in a validated spec: the spec changes until it passes")

    # The how, out of sight.
    tech = re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, TECH)) + r")(?![\w-])", re.IGNORECASE)
    for i, l in enumerate(lines, 1):
        if l.startswith(("**Branche**", "**Source**")):
            continue
        for m in tech.finditer(re.sub(r"`[^`]*`", "", l)):
            out.append(f"{where}:{i}: a technical word, « {m.group(0)} »: say what the person does and sees")
    return out


def lint_passation(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()
    spans = outline(lines, where, "passation", PASS_H2, out)
    leftovers(lines, where, out)

    link = next(((n, l) for n, l in body(lines, spans.get("Maquette")) if l.startswith("- Lien :")), None)
    if not link:
        out.append(f"{where}: `## Maquette` has no `- Lien :` line")
    elif not re.match(r"^- Lien : (https://\S+|aucun — \S.*)$", link[1]):
        out.append(f"{where}:{link[0]}: `- Lien :` is an https:// address, or `aucun — <pourquoi>`")

    spec = folder / "spec.md"
    story_ids = set(re.findall(r"^### (US\d+) — ", spec.read_text(encoding="utf-8"), re.M)) if spec.exists() else None
    if story_ids is None:
        out.append(f"{where}: no spec.md next to it: each screen's Récits are checked against it")
    textes = folder / "textes.md"
    textes_ids = set(re.findall(r"^## (SC\d+)\b", textes.read_text(encoding="utf-8"), re.M)) if textes.exists() else None
    if textes_ids is None:
        out.append(f"{where}: no textes.md next to it")

    screens, cur = [], None
    for n, l in body(lines, spans.get("Écrans")):
        if l.startswith("### "):
            m = SCREEN.match(l)
            if not m:
                out.append(f"{where}:{n}: `{l}` — a screen is `### SC1 <nom>`")
                cur = None
                continue
            cur = {"id": m.group(1), "num": int(m.group(2)), "line": n, "lines": []}
            screens.append(cur)
        elif cur and (m := re.match(r"^- ([^:]+?) : (.*)$", l)):
            cur["lines"].append((n, m.group(1), m.group(2)))
        elif cur and l.strip() and not l.startswith("- "):
            out.append(f"{where}:{n}: under {cur['id']}, each line is `- <Libellé> : …` on one line")
    if "Écrans" in spans and not screens:
        out.append(f"{where}:{spans['Écrans'][0]}: no screen under `## Écrans`")
    ids_in_order([(s["line"], s["num"]) for s in screens], "SC", where, out)

    for s in screens:
        labels = [lab for _, lab, _ in s["lines"]]
        if labels != SCREEN_LINES:
            out.append(f"{where}:{s['line']}: {s['id']}'s lines are {', '.join(SCREEN_LINES)}, in that order (found: {', '.join(labels) or 'none'})")
        val = {lab: (n, v) for n, lab, v in s["lines"]}
        if "Récits" in val and story_ids is not None:
            n, v = val["Récits"]
            got = re.findall(r"US\d+", v)
            if not got:
                out.append(f"{where}:{n}: {s['id']} names no story (`Récits : US1, US2`)")
            for us in got:
                if us not in story_ids:
                    out.append(f"{where}:{n}: {us} is not a story of spec.md")
        states_file = None
        if "Fichier" in val:
            n, v = val["Fichier"]
            f = folder / v.strip().strip("`")
            if not v.strip().strip("`").startswith("maquette/") or not f.is_file():
                out.append(f"{where}:{n}: `{v}` is not a file under maquette/ next to passation.md")
            else:
                states_file = set(re.findall(r'data-state="([^"]+)"', f.read_text(encoding="utf-8")))
        if "États" in val:
            n, v = val["États"]
            anchors = set(re.findall(r"\(#([^)\s]+)\)", v))
            if not anchors:
                out.append(f"{where}:{n}: each state is `<état> (#<ancre>) — <ce qu'on voit>`")
            elif states_file is not None:
                for a in sorted(anchors - states_file):
                    out.append(f"{where}:{n}: #{a} is no `data-state` of {val['Fichier'][1]}")
                for a in sorted(states_file - anchors):
                    out.append(f"{where}:{n}: the page's state `{a}` is not listed")
        if textes_ids is not None and s["id"] not in textes_ids:
            out.append(f"{where}:{s['line']}: textes.md has no `## {s['id']} …` section")

    for n, l in body(lines, spans.get("Contrôle")):
        if l.startswith("- [ ]"):
            out.append(f"{where}:{n}: an unticked Contrôle line: the prototype or this file changes until it passes")
    return out


def main(argv):
    if len(argv) != 3 or argv[1] not in ("spec", "passation"):
        print(__doc__.strip().splitlines()[2].strip() + "\n" + __doc__.strip().splitlines()[3].strip(), file=sys.stderr)
        return 2
    path = Path(argv[2])
    if not path.is_file():
        print(f"{path}: no such file", file=sys.stderr)
        return 1
    out = (lint_spec if argv[1] == "spec" else lint_passation)(path)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
