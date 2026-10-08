"""Check that STATUS.md stays small enough to read before every session.

    python3 tools/status_check.py [STATUS.md]

Prints one line per problem and exits 1, or prints nothing. The rules are in AGENTS.md.
STATUS.md is local and gitignored: with none (a fresh clone), it says so and exits 0.
"""

import datetime
import os
import re
import sys

MAX_LINES = 40
SECTIONS = ["Goal", "Where things are", "Trial projects", "Next"]


def check(path):
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except UnicodeDecodeError:
        return [f"{path}: not UTF-8"]
    except OSError as e:
        return [f"{path}: cannot be read: {e.strerror or e}"]
    out = []
    if len(lines) > MAX_LINES:
        out.append(f"{path}: {len(lines)} lines, {MAX_LINES} at most: cut what is done or lives elsewhere")
    dates = [m.group(1) for l in lines if (m := re.match(r"^\s*\*\*Updated\*\*:\s*(.*?)\s*$", l))]
    if not dates:
        out.append(f"{path}: no `**Updated**: YYYY-MM-DD` line")
    elif len(dates) > 1:
        out.append(f"{path}: {len(dates)} `**Updated**` lines: keep exactly one")
    for d in dates:
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", d):
            out.append(f"{path}: `{d}` is not a date (YYYY-MM-DD)")
            continue
        try:
            day = datetime.date.fromisoformat(d)
        except ValueError:
            out.append(f"{path}: `{d}` is not on the calendar")
            continue
        if day > datetime.date.today():
            out.append(f"{path}: `{d}` is later than today")
    got = [l[3:].strip() for l in lines if l.startswith("## ")]
    if got != SECTIONS:
        out.append(f"{path}: the sections are {', '.join(SECTIONS)}, in that order; found {', '.join(got) or 'none'}")
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "STATUS.md"
    if not os.path.exists(path):
        print(f"{path}: none here; it is local and gitignored, so a fresh clone has none")
        sys.exit(0)
    problems = check(path)
    print("\n".join(problems), end="\n" if problems else "")
    sys.exit(1 if problems else 0)
