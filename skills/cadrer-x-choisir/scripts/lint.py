#!/usr/bin/env python3
"""Check the form of a cadrer-x feature's spec.md, passation.md or taches.md, as the later skills read them.

    python3 lint.py spec <feature>/spec.md
    python3 lint.py passation <feature>/passation.md
    python3 lint.py taches <feature>/taches.md

Prints one line per problem (`path:line: what`) and exits 1, or prints nothing and exits 0.

spec, passation: it checks the headings, labels and ids the later skills find by name, never whether
the content is right: that is the Vérifs' and the Contrôle's job, and the person's.

taches: as realiser and rendre read it. It reads the spec.md, passation.md and the project's
constitution next to it for the ids, and checks the form and the plan's links (stories, exigences,
screens, shared files, `Après :`, `[P]`), never whether the tasks are well cut: that is the person's,
and the review's.
"""
import re
import subprocess
import sys
from pathlib import Path

SPEC_H2 = ["Récits", "Exigences", "Critères", "Supposé", "Pas encore", "Vérifs"]
SPEC_H3 = {"Récits": {"Cas limites"}, "Exigences": {"Données clés"}}
STORY = re.compile(r"^### (US(\d+)) — \S.* \(Priorité : (P\d+|bonus)\)$")
MARKER = re.compile(r"\[À PRÉCISER : [^\]]*?→ (Q\d+)\]")
# What a person never reads in a spec: the how. Whole words, any case.
TECH = ["api", "endpoint", "csv", "json", "sql", "sqlite", "http", "https", "url", "backend", "frontend",
        "schéma", "schema", "utc", "token", "webhook", "cron", "base de données", "requête", "serveur"]
PASS_H2 = ["Maquette", "Écrans", "Nouveautés", "Accessibilité", "Ouvert", "Contrôle"]
SCREEN = re.compile(r"^### (SC(\d+)) \S")
SCREEN_LINES = ["Récits", "Fichier", "Parties", "États", "Largeurs", "Contenu"]

FIXED_H2 = ["Fondations", "Ordre", "À surveiller", "Couverts"]
STORY_H2 = re.compile(r"^US(\d+) — \S.* \(Priorité : (P\d+|bonus)\)( 🎯)?$")
TASK = re.compile(r"^- \[([ xX])\] (T(\d{2,})) (\[P\] )?(\[(US\d+)\] )?(\S.*)$")
LINES = ["Exigences", "Risques", "Écrans", "Fichiers", "Après", "Taille"]
NEVER = re.compile(r"(^|/)(spec\.md|taches\.md|passation\.md|contenu\.md|CHANGELOG\.md)$|(^|/)maquette/")
RENDRE = r"(architecture\.md|adr/|security/)"


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

    spec = folder / "spec.md"
    story_ids = set(re.findall(r"^### (US\d+) — ", spec.read_text(encoding="utf-8"), re.M)) if spec.exists() else None
    if story_ids is None:
        out.append(f"{where}: no spec.md next to it: each screen's Récits are checked against it")
    contenu = folder / "contenu.md"
    contenu_ids = set(re.findall(r"^## (SC\d+)\b", contenu.read_text(encoding="utf-8"), re.M)) if contenu.exists() else None
    if contenu_ids is None:
        out.append(f"{where}: no contenu.md next to it")

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
        if contenu_ids is not None and s["id"] not in contenu_ids:
            out.append(f"{where}:{s['line']}: contenu.md has no `## {s['id']} …` section")

    for n, l in body(lines, spans.get("Contrôle")):
        if l.startswith("- [ ]"):
            out.append(f"{where}:{n}: an unticked Contrôle line: the prototype or this file changes until it passes")
    return out


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


def rendre_docs(folder):
    """rendre's docs under {docs}/, the folder two levels up from features/NNNN-x/, as the repo names it."""
    docs = folder.resolve().parent.parent
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=folder, capture_output=True, text=True)
    try:
        rel = docs.relative_to(Path(r.stdout.strip()).resolve()).as_posix() if r.returncode == 0 else "docs"
    except ValueError:
        rel = "docs"
    return re.compile(r"^(\./)?" + ("" if rel == "." else re.escape(rel) + "/") + RENDRE)


def files_of(v):
    out = []
    for f in v.split(","):
        f = f.strip().strip("`")
        if f and f.lower() != "aucun" and f not in out:
            out.append(f)
    return out


def lint_taches(path):
    where, out = str(path), []
    folder = path.parent
    lines = path.read_text(encoding="utf-8").splitlines()
    rendre_files = rendre_docs(folder)

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
    # A bonus story is bonus in both files.
    spec_prio = dict(re.findall(r"^### (US\d+) — .* \(Priorité : (P\d+|bonus)\)$", spec or "", re.M))
    for n, t in h2:
        if (m := STORY_H2.match(t)) and f"US{m.group(1)}" in spec_prio:
            if (m.group(2) == "bonus") != (spec_prio[f"US{m.group(1)}"] == "bonus"):
                out.append(f"{where}:{n}: US{m.group(1)} is `{m.group(2)}` here but `{spec_prio[f'US{m.group(1)}']}` in spec.md")

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
    # Ids: T01 to Tn, each once; a task added after the build (realiser, rendre) takes Tn+1 last in its
    # story's section, so ids rise within a section, not across the file.
    nums = sorted(t["num"] for t in tasks)
    if nums != list(range(1, len(tasks) + 1)):
        out.append(f"{where}: ids go T01 to T{len(tasks):02d}, each once, no gap; found {', '.join(t['id'] for t in tasks)}")
    for a, b in zip(tasks, tasks[1:]):
        if a["sec"] == b["sec"] and b["num"] <= a["num"]:
            out.append(f"{where}:{b['line']}: {b['id']} comes after {a['id']} in its section: ids rise within a section")
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
                if NEVER.search(f) or rendre_files.search(f):
                    out.append(f"{where}:{n}: `{f}` is never a task's file (choisir's or rendre's)")
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

    # Nothing required stands on a bonus story's task.
    def bonus(t):
        m = STORY_H2.match(t["sec"] or "")
        return bool(m) and m.group(2) == "bonus"
    for t in tasks:
        for a in t["after"]:
            if not bonus(t) and bonus(by_id[a]):
                out.append(f"{where}:{t['line']}: {t['id']} is after {a}, a bonus story's task: what a required story stands on is never a bonus")

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
    lints = {"spec": lint_spec, "passation": lint_passation, "taches": lint_taches}
    if len(argv) != 3 or argv[1] not in lints:
        print("\n".join(l.strip() for l in __doc__.strip().splitlines()[2:5]), file=sys.stderr)
        return 2
    path = Path(argv[2])
    if not path.is_file():
        print(f"{path}: no such file", file=sys.stderr)
        return 1
    out = lints[argv[1]](path)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
