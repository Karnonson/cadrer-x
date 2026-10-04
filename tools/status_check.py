"""Check that STATUS.md stays small enough to read before every session.

    python3 tools/status_check.py [STATUS.md]

Prints one line per problem and exits 1, or prints nothing. The rules are in AGENTS.md.
"""

import re
import sys

MAX_LINES = 40
SECTIONS = ["Goal", "Where things are", "Trial projects", "Next"]


def check(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    out = []
    if len(lines) > MAX_LINES:
        out.append(f"{path}: {len(lines)} lines, {MAX_LINES} at most: cut what is done or lives elsewhere")
    if not any(re.match(r"^\*\*Updated\*\*: \d{4}-\d{2}-\d{2}$", l) for l in lines):
        out.append(f"{path}: no `**Updated**: YYYY-MM-DD` line")
    got = [l[3:].strip() for l in lines if l.startswith("## ")]
    if got != SECTIONS:
        out.append(f"{path}: the sections are {', '.join(SECTIONS)}, in that order; found {', '.join(got) or 'none'}")
    return out


if __name__ == "__main__":
    problems = check(sys.argv[1] if len(sys.argv) > 1 else "STATUS.md")
    print("\n".join(problems), end="\n" if problems else "")
    sys.exit(1 if problems else 0)
