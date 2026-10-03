#!/usr/bin/env python3
"""Do the task's tests catch a broken signup? A small mutation test, run by the eval's checks.

    python3 mutants.py <task worktree>

Each mutant changes one spot of src/clubhouse/signup/api.py (a comparison flipped, a refusal turned into
a silent return) and runs tests/test_signup.py on it. A mutant the tests
still pass "survives". Prints each survivor; exits 0 when at least 4 mutants ran and at least 80% died.
"""
import re
import subprocess
import sys
from pathlib import Path

FLIPS = {">=": ">", ">": ">=", "<=": "<", "<": "<=", "==": "!=", "!=": "=="}
COMPARE = re.compile(r"(?<![<>=!-])(>=|<=|==|!=|>|<)(?![<>=])")


def mutants(lines):
    for n, line in enumerate(lines):
        code = line.split("#", 1)[0]
        if code.lstrip().startswith(("def ", "import ", "from ", "class ", "@")) or '"""' in code:
            continue
        for m in COMPARE.finditer(code):
            if code.count('"', 0, m.start()) % 2 or code.count("'", 0, m.start()) % 2:
                continue   # inside a string
            yield n, line[:m.start()] + FLIPS[m.group()] + line[m.end():], f"{m.group()} → {FLIPS[m.group()]}"
        stripped = code.strip()
        indent = line[:len(line) - len(line.lstrip())]
        if stripped.startswith("raise "):
            yield n, indent + "return None\n", "refusal turned into a silent return"


def main(worktree):
    root = Path(worktree)
    api = root / "src/clubhouse/signup/api.py"
    original = api.read_text()
    for stale in api.parent.glob("__pycache__/api.*.pyc"):   # two mutants of one size in one second share a stale pyc
        stale.unlink()
    lines = original.splitlines(keepends=True)
    ran, survivors = 0, []
    try:
        for n, new, what in mutants(lines):
            api.write_text("".join(lines[:n] + [new] + lines[n + 1:]))
            try:
                r = subprocess.run([sys.executable, "-B", "-m", "unittest", "tests.test_signup", "-q"], cwd=root,
                                   env={"PYTHONPATH": "src", "PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"}, capture_output=True, timeout=60)
                died = r.returncode != 0
            except subprocess.TimeoutExpired:
                died = True
            ran += 1
            if not died:
                survivors.append(f"line {n + 1}: {what}: {lines[n].strip()}")
    finally:
        api.write_text(original)
    killed = ran - len(survivors)
    print(f"{killed}/{ran} mutants caught")
    for s in survivors:
        print("survived:", s)
    return 0 if ran >= 4 and killed >= 0.8 * ran else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
