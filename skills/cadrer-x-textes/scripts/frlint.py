#!/usr/bin/env python3
"""Check the French rules a machine can check, in .md and .txt files.

    python3 frlint.py <file or folder>…

Prints one line per finding (`path:line: rule — the line`) and exits 1, or prints nothing and exits 0.
Rules: a space before `: ; ! ?` and inside « », no straight quotes around French, a decimal comma, a
space between thousands, no sentence over 20 words, no mixed tu/vous, known anglicisms. Code spans,
fenced code, links and front matter are skipped. Ported from fleet's `frlint`; labels
are French here (`- Titre : …`), so every colon takes its space.
"""
import re
import sys
from pathlib import Path

FRENCH_WORD = re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*", re.UNICODE)
TU_FORM = re.compile(r"\b(?:tu|te|toi|ton|ta|tes)\b", re.I)
VOUS_FORM = re.compile(r"(?<!rendez-)\b(?:vous|votre|vos)\b", re.I)   # `rendez-vous` is a noun
URL = re.compile(r"https?://\S+|www\.\S+|\b(?:mailto|tel):\S+", re.I)
CODE_SPAN = re.compile(r"`[^`]*`")
FRENCH_SPACE = "   "
DECIMAL_POINT = re.compile(r"(?<![\d.])\d+\.\d+(?![\d.])")          # `26.09.2026` and `2.1.3` have more points
HEADING_NUM = re.compile(r"^\s*#+\s*\d+(?:\.\d+)*\.?(?=\s)")        # `## 2.1 Le plan`: numbering
THOUSANDS_COMMA = re.compile(r"(?<![\d,])\d{1,3}(?:,\d{3})+(?![\d,])")
ANGLICISMS = re.compile(r"\b(?:faire|fais|fait|faisons|faites|font)\s+sens\b|\bscale\b|\bappliquer\s+pour\b", re.I)
# A version, not a decimal: after a capitalised name (Python 3.11) or glued to letters (v2.1).
VERSION_BEFORE = re.compile(r"(?:\b[A-Z][\w.+-]*\s+|[A-Za-z][-_]?)$")


def lint_file(path):
    findings, tu_lines, vous_lines = [], [], []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return [f"{path}:1: not UTF-8 text"]
    front_end = 0
    if lines and lines[0].strip() == "---":
        front_end = next((n for n, l in enumerate(lines[1:], 2) if l.strip() == "---"), 1)
    fence = False
    for number, original in enumerate(lines, 1):
        if number <= front_end:
            continue
        line = original.strip()
        if line.startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or line.startswith("<!--"):
            continue
        clean = URL.sub(" ", CODE_SPAN.sub(" ", original))
        excerpt = line[:160]

        def finding(rule):
            findings.append(f"{path}:{number}: {rule} — {excerpt}")

        if not line.startswith("#") and "|" not in clean:
            for sentence in re.split(r"[.!?]+", clean):
                if len(FRENCH_WORD.findall(sentence)) > 20:
                    finding("sentence over 20 words")
        for m in re.finditer(r"[:;!?]", clean):
            pos = m.start()
            if m.group() == ":" and 0 < pos < len(clean) - 1 and clean[pos - 1].isdigit() and clean[pos + 1].isdigit():
                continue
            if m.group() in "!?" and pos and clean[pos - 1] in "!?":
                continue
            if pos and clean[pos - 1] not in FRENCH_SPACE:
                finding("French punctuation spacing")
        for m in re.finditer("[«»]", clean):
            pos = m.start()
            if (m.group() == "«" and (pos + 1 == len(clean) or clean[pos + 1] not in FRENCH_SPACE)) or \
               (m.group() == "»" and (pos == 0 or clean[pos - 1] not in FRENCH_SPACE)):
                finding("French guillemet spacing")
        if re.search(r'"[^"\n]*[^\W\d_][^"\n]*"', clean):
            finding("straight double quotes around French text")
        numbers = HEADING_NUM.sub("", clean) if line.startswith("#") else clean
        if any(not VERSION_BEFORE.search(numbers[:m.start()]) for m in DECIMAL_POINT.finditer(numbers)):
            finding("decimal comma")
        if THOUSANDS_COMMA.search(clean):
            finding("thousands separator: a space")
        for m in ANGLICISMS.finditer(clean):
            finding(f"anglicism — {m.group().lower()}")
        if TU_FORM.search(clean):
            tu_lines.append((number, excerpt))
        if VOUS_FORM.search(clean):
            vous_lines.append((number, excerpt))
    if tu_lines and vous_lines:
        number, excerpt = vous_lines[0]
        findings.append(f"{path}:{number}: mixed tu/vous register — {excerpt}")
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    out = []
    for a in argv[1:]:
        p = Path(a)
        if not p.exists():
            print(f"{p}: no such file", file=sys.stderr)
            return 2
        files = sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in (".md", ".txt")) if p.is_dir() else [p]
        for f in files:
            out += lint_file(f)
    for line in out:
        print(line)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
