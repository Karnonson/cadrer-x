#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's taches.md, as realiser, examiner and rendre read it.

    python3 lint.py taches <feature>/taches.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0. It reads
the spec.md, passation.md and the project's constitution next to it for the ids, and checks the form
and the plan's links (stories, exigences, screens, shared files, `Après :`, `[P]`), never whether the
tasks are well cut: that is the person's, and the review's.
"""
import re
import sys
from pathlib import Path

FIXED_H2 = ["Fondations", "Ordre", "À surveiller", "Couverts"]
STORY_H2 = re.compile(r"^US(\d+) — \S.* \(Priorité : P\d+\)( 🎯)?$")
TASK = re.compile(r"^- \[([ xX])\] (T(\d{2,})) (\[P\] )?(\[(US\d+)\] )?(\S.*)$")
LINES = ["Exigences", "Risques", "Écrans", "Fichiers", "Après", "Taille"]
NEVER = re.compile(r"(^|/)(spec\.md|taches\.md|passation\.md|textes\.md|CHANGELOG\.md)$|(^|/)maquette/|"
                   r"(^|/)docs/(architecture\.md|adr/|security/)")


def ids(text, pattern):
    return set(re.findall(pattern, text, re.M)) if text is not None else None


def read(p):
    return p.read_text(encoding="utf-8") if p.is_file() else None


def constitution(folder):
    """The constitution beside the feature: {docs}/constitution.md, two levels up from features/NNNN-x/."""
    for up in (folder.parent.parent, folder.parent.parent.parent):
        c = up / "constitution.md"
        if c.is_file():
            return c
    return None


def files_of(v):
    out = []
    for f in v.split(","):
        f = f.strip().strip("`")
        if f and f.lower() != "aucun" and f not in out:
            out.append(f)
    return out


def lint(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()

    spec = read(folder / "spec.md")
    stories = ids(spec, r"^### (US\d+) — ")
    reqs = ids(spec, r"^- \*\*(EF\d+)\*\* :")
    if spec is None:
        out.append(f"{where}: no spec.md next to it: the stories and exigences are checked against it")
    passation = read(folder / "passation.md")
    screens = ids(passation, r"^### (SC\d+) ")
    c = constitution(folder)
    rules = ids(read(c), r"^\| (M\d+) \|") if c else None

    # Outline.
    first = next((l for l in lines if l.startswith("#")), "")
    if not re.match(r"^# \S.* — tâches$", first):
        out.append(f"{where}:1: the first heading is the title `# <Titre> — tâches`")
    h2 = [(i + 1, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    names = [t for _, t in h2]
    for name in FIXED_H2:
        if name not in names:
            out.append(f"{where}: `## {name}` is missing")
    story_secs = []
    for n, t in h2:
        if m := STORY_H2.match(t):
            story_secs.append((n, f"US{m.group(1)}"))
        elif t not in FIXED_H2 + ["Format"]:
            out.append(f"{where}:{n}: `## {t}` is not a heading of taches.md (a story is `## US1 — <titre> (Priorité : P1)`)")
    order = [t if t in FIXED_H2 + ["Format"] else "US" for _, t in h2 if t in FIXED_H2 + ["Format"] or STORY_H2.match(t)]
    expect = [x for x in ["Format", "Fondations", "US", "Ordre", "À surveiller", "Couverts"] if x in order]
    if [x for i, x in enumerate(order) if i == 0 or order[i - 1] != x] != expect:
        out.append(f"{where}: the sections go Fondations, the stories, Ordre, À surveiller, Couverts")
    for n, us in story_secs:
        if stories is not None and us not in stories:
            out.append(f"{where}:{n}: {us} is not a story of spec.md")
    for us in sorted((stories or set()) - {u for _, u in story_secs}, key=lambda s: int(s[2:])):
        out.append(f"{where}: {us} of spec.md has no `## {us} — …` section")

    def section_at(n):
        cur = None
        for hn, t in h2:
            if hn <= n:
                cur = t
        return cur

    # Story sections end on a checkpoint.
    for k, (n, us) in enumerate(story_secs):
        end = next((hn for hn, _ in h2 if hn > n), len(lines) + 1)
        if not any(l.startswith("**Point d'étape**") for l in lines[n:end - 1]):
            out.append(f"{where}:{n}: {us}'s section has no `**Point d'étape** : …` line")

    # Tasks.
    tasks, cur = [], None
    for i, l in enumerate(lines, 1):
        sec = section_at(i)
        if l.startswith("- [") and re.match(r"^- \[[ xX]\] T", l):
            m = TASK.match(l)
            if not m:
                out.append(f"{where}:{i}: a task is `- [ ] T01 [P] [US1] <verbe> <titre>`")
                cur = None
                continue
            cur = {"id": m.group(2), "num": int(m.group(3)), "p": bool(m.group(4)), "us": m.group(6),
                   "line": i, "sec": sec, "boxes": 0, "lines": []}
            tasks.append(cur)
            if sec not in ("Fondations",) and not STORY_H2.match(sec or ""):
                out.append(f"{where}:{i}: {cur['id']} sits under `## {sec}`: tasks go under Fondations or a story")
        elif l.startswith("## "):
            cur = None
        elif cur and re.match(r"^\s+- \[[ xX]\] \S", l):
            cur["boxes"] += 1
        elif cur and (m := re.match(r"^\s+([^\W\d_]+) : (.*)$", l)):
            cur["lines"].append((i, m.group(1), m.group(2).strip()))

    if not tasks:
        out.append(f"{where}: no task")
    for k, t in enumerate(tasks, 1):
        if t["num"] != k:
            out.append(f"{where}:{t['line']}: {t['id']} should be T{k:02d}: ids go T01, T02… in file order, no gap")
            break
    by_id = {t["id"]: t for t in tasks}
    pos = {t["id"]: k for k, t in enumerate(tasks)}

    for t in tasks:
        n0, tid = t["line"], t["id"]
        sec = t["sec"] or ""
        if m := STORY_H2.match(sec):
            if t["us"] != f"US{m.group(1)}":
                out.append(f"{where}:{n0}: {tid} sits under US{m.group(1)}'s section but is tagged {t['us'] or 'no story'}")
        if t["us"] and stories is not None and t["us"] not in stories:
            out.append(f"{where}:{n0}: {tid} tags {t['us']}, which spec.md does not have")
        if not t["boxes"]:
            out.append(f"{where}:{n0}: {tid} has no `- [ ] <fait quand>` box")
        labels = [lab for _, lab, _ in t["lines"]]
        want = [x for x in LINES if x != "Écrans" or "Écrans" in labels]
        if labels != want:
            out.append(f"{where}:{n0}: {tid}'s lines are {', '.join(want)}, in that order (Écrans only with a screen); found: {', '.join(labels) or 'none'}")
        val = {lab: (n, v) for n, lab, v in t["lines"]}
        t["files"] = files_of(val["Fichiers"][1]) if "Fichiers" in val else []
        t["after"] = []
        if "Exigences" in val:
            n, v = val["Exigences"]
            got = re.findall(r"EF\d+", v)
            if not got and v != "aucune":
                out.append(f"{where}:{n}: `Exigences :` lists EF ids, or says `aucune`")
            for ef in got:
                if reqs is not None and ef not in reqs:
                    out.append(f"{where}:{n}: {ef} is not an exigence of spec.md")
            t["reqs"] = got
        if "Risques" in val:
            n, v = val["Risques"]
            if not (re.match(r"^aucun — \S", v) or all(re.match(r"^\S.* — .+ → \S", r.strip()) for r in v.split(";"))):
                out.append(f"{where}:{n}: `Risques :` is `<domaine> — <menace> → <protection>` (`;` between), or `aucun — <pourquoi>`")
        if "Écrans" in val:
            n, v = val["Écrans"]
            got = re.findall(r"SC\d+", v)
            if screens is None:
                out.append(f"{where}:{n}: `Écrans :` but no passation.md next to it")
            for sc in got:
                if screens is not None and sc not in screens:
                    out.append(f"{where}:{n}: {sc} is not a screen of passation.md")
            t["screens"] = got
        if "Fichiers" in val:
            n, v = val["Fichiers"]
            if not t["files"]:
                out.append(f"{where}:{n}: `Fichiers :` names the exact paths, tests included")
            for f in t["files"]:
                if NEVER.search(f):
                    out.append(f"{where}:{n}: `{f}` is never a task's file (affiner's, découper's or rendre's)")
        if "Après" in val:
            n, v = val["Après"]
            got = re.findall(r"T\d{2,}", v)
            if not got and v != "aucune":
                out.append(f"{where}:{n}: `Après :` names earlier tasks, or says `aucune`")
            for a in got:
                if a not in by_id or pos[a] >= pos[tid]:
                    out.append(f"{where}:{n}: {tid} is after {a}, which is not an earlier task")
            t["after"] = [a for a in got if a in by_id and pos[a] < pos[tid]]
        if "Taille" in val and val["Taille"][1] not in ("XS", "S", "M"):
            out.append(f"{where}:{val['Taille'][0]}: `Taille :` is XS, S or M; bigger is two tasks")

    def ancestors(tid, seen=None):
        seen = set() if seen is None else seen
        for a in by_id[tid]["after"]:
            if a not in seen:
                seen.add(a)
                ancestors(a, seen)
        return seen

    # [P]: not after the one before, no shared file with it.
    for k, t in enumerate(tasks):
        if t["p"] and k:
            prev = tasks[k - 1]
            if prev["id"] in ancestors(t["id"]):
                out.append(f"{where}:{t['line']}: {t['id']} is [P] but stands on {prev['id']}, the task before it")
            shared = set(t["files"]) & set(prev["files"])
            if shared:
                out.append(f"{where}:{t['line']}: {t['id']} is [P] but shares {', '.join(sorted(shared))} with {prev['id']}")

    # Shared files: one owner, the others after it.
    owner = {}
    for t in tasks:
        for f in t["files"]:
            if f not in owner:
                owner[f] = t["id"]
            elif owner[f] not in ancestors(t["id"]):
                out.append(f"{where}:{t['line']}: {t['id']} changes `{f}`, owned by {owner[f]}: it must be `Après :` {owner[f]}")

    # Screens all built.
    named = {sc for t in tasks for sc in t.get("screens", [])}
    for sc in sorted((screens or set()) - named):
        out.append(f"{where}: {sc} of passation.md is on no task's `Écrans :` line")

    # Couverts.
    try:
        ci = names.index("Couverts")
        start = h2[ci][0]
        end = h2[ci + 1][0] - 1 if ci + 1 < len(h2) else len(lines)
    except ValueError:
        start = end = None
    if start:
        rows = {}
        for i in range(start, end):
            l = lines[i]
            if m := re.match(r"^\| *((?:US|EF|M)\d+) *\| *(.*?) *\|$", l):
                rows[m.group(1)] = (i + 1, re.findall(r"T\d{2,}", m.group(2)))
        conflict = next((lines[i] for i in range(start, end) if lines[i].startswith("- Règles en conflit :")), None)
        if conflict is None:
            out.append(f"{where}:{start}: `## Couverts` ends on `- Règles en conflit : aucune` (or the rules, each with its task)")
        for key, (n, ts) in rows.items():
            if not ts:
                out.append(f"{where}:{n}: {key} names no task")
            for x in ts:
                if x not in by_id:
                    out.append(f"{where}:{n}: {x} is not a task")
            if key.startswith("M") and rules is not None and key not in rules:
                out.append(f"{where}:{n}: {key} is not a rule of the constitution")
        for key in sorted((stories or set()) | (reqs or set()), key=lambda s: (s[:2], int(re.sub(r'\D', '', s)))):
            if key not in rows:
                out.append(f"{where}:{start}: {key} of spec.md has no row under Couverts")
        covered = {x for _, ts in rows.values() for x in ts}
        for t in tasks:
            if t["id"] not in covered:
                out.append(f"{where}:{t['line']}: {t['id']} is in no row of Couverts")
        if conflict:
            for m_ in re.findall(r"M\d+", conflict):
                if m_ not in rows:
                    out.append(f"{where}: {m_} is in conflict but has no row naming the task that owns it")

    for i, l in enumerate(lines, 1):
        if "<!--" in l:
            out.append(f"{where}:{i}: a template comment is left: remove it")
        elif re.search(r"<[a-zà-ÿ][^<>`]*>", re.sub(r"`[^`]*`", "", l)) and section_at(i) != "Format":
            out.append(f"{where}:{i}: a template placeholder `<…>` is left")
    return out


def main(argv):
    if len(argv) != 3 or argv[1] != "taches":
        print("python3 lint.py taches <feature>/taches.md", file=sys.stderr)
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
