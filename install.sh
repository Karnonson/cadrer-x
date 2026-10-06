#!/usr/bin/env bash
# Install the cadrer-x skills for Claude Code and codex.
#
# One command, from the folder to install into: it fetches cadrer-x into ~/cadrer-x (or updates it),
# then installs from there. While the repo is private, with gh signed in:
#   gh api repos/Karnonson/cadrer-x/contents/install.sh -H "Accept: application/vnd.github.raw" | bash
# Once it is public:
#   curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash
# Options go after `bash -s --`: `... | bash -s -- --engine codex`. CADRER_X_HOME moves ~/cadrer-x.
#
# From a clone:
#   ./install.sh [DIR]          into the project DIR (default: the current folder): DIR/.claude/skills
#                               and DIR/.agents/skills, to commit with the project
#   ./install.sh --global       for every project of this user: ~/.claude/skills and ~/.agents/skills
#
# Options: --engine claude|codex (default: the ones this computer has, else both) · --link (symlinks
# to this checkout instead of copies, to try changes to the skills live) · --remove (take the cadrer-x
# skills out again).
# For a project, Claude Code's .claude/settings.json also gets the git commands the steps run
# (worktrees, merges, commits) allowed, and git push asked every time; --remove takes them out.

set -euo pipefail

# Run from a pipe, or from outside a clone: fetch or update the clone, then run its install.sh.
here="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" && pwd)"
if [ -z "${BASH_SOURCE[0]:-}" ] || [ ! -d "$here/skills" ]; then
  home="${CADRER_X_HOME:-$HOME/cadrer-x}"
  if [ -e "$home" ]; then
    # Only the top of a clone of this repository: never pull or run another checkout's script.
    origin="$(git -C "$home" remote get-url origin 2>/dev/null || true)"
    top="$(git -C "$home" rev-parse --show-toplevel 2>/dev/null || true)"
    case "$origin" in
      https://github.com/Karnonson/cadrer-x | https://github.com/Karnonson/cadrer-x.git | \
      git@github.com:Karnonson/cadrer-x | git@github.com:Karnonson/cadrer-x.git | \
      ssh://git@github.com/Karnonson/cadrer-x | ssh://git@github.com/Karnonson/cadrer-x.git) ok=1 ;;
      *) ok=0 ;;
    esac
    if [ "$ok" = 0 ] || [ "$top" != "$(cd "$home" && pwd -P)" ]; then
      echo "$home exists and is not a cadrer-x clone: move it, or set CADRER_X_HOME" >&2; exit 1
    fi
    git -C "$home" pull --ff-only --quiet || echo "could not update $home: installing the version it has" >&2
  elif command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
    gh repo clone Karnonson/cadrer-x "$home" -- --quiet
  else
    git clone --quiet https://github.com/Karnonson/cadrer-x.git "$home"
  fi
  exec bash "$home/install.sh" "$@"
fi

self="$here/install.sh"
src="$here/skills"
scope=project dir=. engines="" link=0 remove=0

while [ $# -gt 0 ]; do
  case "$1" in
    --global) scope=global ;;
    --engine) shift; case "${1:-}" in claude|codex) engines="$1" ;; *) echo "--engine is claude or codex" >&2; exit 2 ;; esac ;;
    --link) link=1 ;;
    --remove) remove=1 ;;
    -h|--help) sed -n '2,20p' "$self" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option $1 (see --help)" >&2; exit 2 ;;
    *) dir="$1" ;;
  esac
  shift
done

# No --engine: the engines this computer has, else both (and both to remove).
if [ -z "$engines" ]; then
  if [ "$remove" = 0 ]; then
    command -v claude >/dev/null && engines="claude"
    command -v codex >/dev/null && engines="$engines codex"
  fi
  engines="${engines:-claude codex}"
fi

if [ "$scope" = global ]; then
  base="$HOME"
else
  [ -d "$dir" ] || { echo "no folder $dir" >&2; exit 1; }
  base="$(cd "$dir" && pwd)"
  [ "$base" = "$(cd "$src/.." && pwd)" ] && { echo "that is the cadrer-x checkout itself: name your project's folder, or use --global" >&2; exit 1; }
fi

for engine in $engines; do
  case "$engine" in claude) dest="$base/.claude/skills" ;; codex) dest="$base/.agents/skills" ;; esac
  mkdir -p "$dest"
  [ "$(cd "$dest" && pwd -P)" = "$(cd "$src" && pwd -P)" ] && { echo "$dest is this checkout's skills folder: nothing to do" >&2; continue; }
  for skill in "$src"/cadrer-x-*/; do
    name="$(basename "$skill")"
    # A skill has SKILL.md, a helper aide.md; a folder with neither holds only templates so far.
    [ -f "$skill/SKILL.md" ] || [ -f "$skill/aide.md" ] || continue
    target="$dest/$name"
    rm -rf "$target"
    [ "$remove" = 1 ] && { echo "removed  $target"; continue; }
    if [ "$link" = 1 ]; then
      ln -s "${skill%/}" "$target"
    else
      mkdir -p "$target"
      (cd "$skill" && tar --exclude=__pycache__ --exclude="*.pyc" -cf - .) | (cd "$target" && tar -xf -)
    fi
    echo "$([ "$link" = 1 ] && echo linked || echo copied)   $target"
  done
done

# The git commands every step runs, so a build is not a prompt per merge. Pushing stays asked.
if [ "$scope" = project ] && [[ " $engines " == *" claude "* ]]; then
  python3 - "$base/.claude/settings.json" "$remove" <<'PY'
import json, sys, pathlib
path, remove = pathlib.Path(sys.argv[1]), sys.argv[2] == "1"
allow = [f"Bash(git {c} *)" for c in ("status", "log", "diff", "show", "branch", "worktree", "merge",
         "merge-base", "add", "commit", "mv", "rm", "grep", "rev-parse", "rev-list", "ls-files", "stash")]
allow += [f"Bash(git {c})" for c in ("status", "log", "diff", "branch", "stash")]
ask = ["Bash(git push *)", "Bash(git push)"]
data = json.loads(path.read_text()) if path.exists() and path.read_text().strip() else {}
perms = data.setdefault("permissions", {})
for key, rules in (("allow", allow), ("ask", ask)):
    have = perms.get(key, [])
    perms[key] = [r for r in have if r not in rules] if remove else have + [r for r in rules if r not in have]
    if not perms[key]:
        del perms[key]
if not perms:
    del data["permissions"]
if data or path.exists():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{'cleaned' if remove else 'allowed'}  git commands in {path}")
PY
fi

if [ "$scope" = project ] && [ "$remove" = 0 ]; then
  echo
  echo "Installed for this project only. Commit .claude/skills, .agents/skills and .claude/settings.json"
  echo "so everyone on it gets the same version. For every project of yours instead: $self --global"
fi
