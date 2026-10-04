#!/usr/bin/env bash
# Install the cadrer-x skills for Claude Code and codex.
#
#   ./install.sh [DIR]          into the project DIR (default: the current folder): DIR/.claude/skills
#                               and DIR/.agents/skills, to commit with the project
#   ./install.sh --global       for every project of this user: ~/.claude/skills and ~/.agents/skills
#
# Options: --engine claude|codex (default: both) · --link (symlinks to this checkout instead of
# copies, to try changes to the skills live) · --remove (take the cadrer-x skills out again).

set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"
scope=project dir=. engines="claude codex" link=0 remove=0

while [ $# -gt 0 ]; do
  case "$1" in
    --global) scope=global ;;
    --engine) shift; case "${1:-}" in claude|codex) engines="$1" ;; *) echo "--engine is claude or codex" >&2; exit 2 ;; esac ;;
    --link) link=1 ;;
    --remove) remove=1 ;;
    -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option $1 (see --help)" >&2; exit 2 ;;
    *) dir="$1" ;;
  esac
  shift
done

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
  for skill in "$src"/cadrer-x-*/; do
    name="$(basename "$skill")"
    [ -f "$skill/SKILL.md" ] || continue          # a folder that holds only templates so far
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

if [ "$scope" = project ] && [ "$remove" = 0 ]; then
  echo
  echo "Installed for this project only. Commit .claude/skills and .agents/skills so everyone on it gets"
  echo "the same version. For every project of yours instead: ./install.sh --global"
fi
