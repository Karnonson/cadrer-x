#!/usr/bin/env bash
# Install the cadrer-x skills for Claude Code and codex.
#
# One command, from the folder to install into: it fetches cadrer-x into ~/cadrer-x (or updates it),
# then installs from there.
#   macOS, Linux, Git Bash: curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash
#   Windows PowerShell:     irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex
# Options go after `bash -s --`: `... | bash -s -- --engine codex`. CADRER_X_HOME moves ~/cadrer-x.
#
# From a clone:
#   ./install.sh [DIR]          into the project DIR (default: the current folder): DIR/.claude/skills
#                               and DIR/.agents/skills, to commit with the project
#   ./install.sh --global       for every project of this user: ~/.claude/skills and ~/.agents/skills
#
# Options: --engine claude|codex (default: the ones this computer has, else both) · --link (symlinks
# to this checkout instead of copies, to try changes to the skills live) · --remove (take the cadrer-x
# skills out again) · --yes (install a missing tool without asking first).
# The skills need git, Python 3 as python3, and tar. When one is missing, it says which and the
# command that installs it, and runs it only on a yes. On Windows it may add ~/bin/python3, which
# runs the Python installed from python.org under that name.
# For a project, Claude Code's .claude/settings.json also gets the git commands the steps run
# (worktrees, merges, commits) allowed, and git push asked every time; --remove takes them out.

set -euo pipefail

# Read first: what to check and whether to ask depend on them. The full parse comes later.
assume_yes=0 remove=0 help=0
for arg in "$@"; do
  case "$arg" in --yes) assume_yes=1 ;; --remove) remove=1 ;; -h|--help) help=1 ;; esac
done

here="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" && pwd)"
# Piped, stdin is the rest of this script: nothing may read it.
piped=0; [ -z "${BASH_SOURCE[0]:-}" ] && piped=1
# A Windows path (C:\...\install.sh) gives here=".": only a real clone counts.
fetch=0; { [ "$piped" = 1 ] || [ ! -f "$here/install.sh" ] || [ ! -d "$here/skills/cadrer-x-init" ]; } && fetch=1

case "$(uname -s)" in
  Darwin) os=mac ;;
  MINGW*|MSYS*|CYGWIN*) os=windows ;;
  *) os=linux ;;
esac

# --- Tools: git, python3 (the skills run `python3 <skill>/scripts/lint.py`), tar (the copies).

works() {
  command -v "$1" >/dev/null 2>&1 || return 1
  # A Mac without the Command Line Tools has /usr/bin/git and /usr/bin/python3 that only open the
  # dialog installing them: never run one there.
  case "$os:$1" in
    mac:git|mac:python3)
      [ "$(command -v "$1")" = "/usr/bin/$1" ] && ! xcode-select -p >/dev/null 2>&1 && return 1 ;;
  esac
  case "$1" in
    git) git --version >/dev/null 2>&1 ;;
    # Also turns down Windows' own python3, which only points to the Microsoft Store.
    python3) python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1 ;;
    *) return 0 ;;
  esac
}

# python.org's Python on Windows answers to py and python, not python3: a ~/bin/python3 runs it,
# ~/bin being first on Git Bash's PATH. Also finds one just installed, this shell's PATH being stale.
win_python3() {
  local probe='import sys; assert sys.version_info >= (3, 8); print(sys.executable)'
  local exe="" cand la="" pf="" shim="$HOME/bin/python3"
  command -v cygpath >/dev/null 2>&1 || return 1
  [ -n "${LOCALAPPDATA:-}" ] && la="$(cygpath -u "$LOCALAPPDATA")"
  [ -n "${PROGRAMFILES:-}" ] && pf="$(cygpath -u "$PROGRAMFILES")"
  exe="$(py -3 -c "$probe" 2>/dev/null || python -c "$probe" 2>/dev/null || true)"
  if [ -z "$exe" ]; then
    for cand in "$la"/Programs/Python/Python3*/python.exe "$pf"/Python3*/python.exe; do
      [ -f "$cand" ] && exe="$("$cand" -c "$probe" 2>/dev/null)" && break
    done
  fi
  exe="$(printf '%s' "$exe" | tr -d '\r')"
  [ -n "$exe" ] || return 1
  # Never replace a python3 of the person's own.
  if [ -e "$shim" ] && ! grep -q cadrer-x "$shim" 2>/dev/null; then return 1; fi
  mkdir -p "$HOME/bin"
  printf '#!/bin/sh\n# Written by cadrer-x: Python on Windows has no python3.\nexec "%s" "$@"\n' \
    "$(cygpath -u "$exe")" >"$shim"
  chmod +x "$shim"
  case ":$PATH:" in *":$HOME/bin:"*) ;; *) PATH="$HOME/bin:$PATH"; export PATH ;; esac
  hash -r
  echo "J'ai créé $shim : il lance ton Python sous le nom python3, celui qu'utilisent les skills."
}

# 0 yes, 1 no, 2 no way to ask (no terminal: CI, a pipe without /dev/tty).
ask() {
  local answer=""
  [ "$assume_yes" = 1 ] && return 0
  printf '%s ' "$1"
  if [ -t 0 ]; then
    read -r answer || { echo; return 2; }
  elif ( : </dev/tty ) 2>/dev/null; then
    read -r answer </dev/tty || { echo; return 2; }
  elif [ "$piped" = 0 ]; then
    # Run as a file with no terminal, e.g. by install.ps1 through Git Bash: stdin is the console.
    read -r answer || { echo; return 2; }
  else
    echo; return 2
  fi
  case "$answer" in [oOyY]*) return 0 ;; *) return 1 ;; esac
}

# Installs the missing ones among its arguments, on the person's yes; exits when it cannot.
need_tools() {
  local tool missing="" pkgs="" plan="" manual="" note="" sudo="" pm="" still="" rc=0 i=0
  for tool in "$@"; do works "$tool" || missing="$missing $tool"; done
  if [ "$os" = windows ] && [[ " $missing " == *" python3 "* ]] && win_python3; then
    missing="${missing/ python3/}"
  fi
  [ -n "$missing" ] || return 0

  case "$os" in
    mac)
      if command -v brew >/dev/null 2>&1; then
        for tool in $missing; do
          case "$tool" in python3) pkgs="$pkgs python" ;; *) pkgs="$pkgs $tool" ;; esac
        done
        plan="brew install$pkgs"
      else
        plan="xcode-select --install"
        note="Une fenêtre va s'ouvrir : clique sur « Installer », puis attends la fin (une dizaine de minutes)."
      fi ;;
    windows)
      case "$missing" in
        *git*|*tar*)
          manual="installe Git for Windows (https://git-scm.com/download/win), puis relance cette commande." ;;
        *)
          if command -v winget >/dev/null 2>&1; then
            plan="winget install -e --id Python.Python.3.13 --accept-package-agreements --accept-source-agreements"
          else
            manual="installe Python 3 depuis https://www.python.org/downloads/, puis relance cette commande."
          fi ;;
      esac ;;
    linux)
      for pm in apt-get dnf yum pacman zypper apk ""; do
        [ -n "$pm" ] && command -v "$pm" >/dev/null 2>&1 && break
      done
      for tool in $missing; do
        case "$tool:$pm" in python3:pacman) pkgs="$pkgs python" ;; *) pkgs="$pkgs $tool" ;; esac
      done
      if [ "$(id -u)" != 0 ] && command -v sudo >/dev/null 2>&1; then
        sudo="sudo "
        note="sudo va sans doute te demander ton mot de passe (rien ne s'affiche pendant que tu le tapes)."
      fi
      case "$pm" in
        apt-get) plan="${sudo}apt-get update && ${sudo}env DEBIAN_FRONTEND=noninteractive apt-get install -y$pkgs" ;;
        dnf|yum) plan="$sudo$pm install -y$pkgs" ;;
        pacman) plan="${sudo}pacman -Sy --needed --noconfirm$pkgs" ;;
        zypper) plan="${sudo}zypper --non-interactive install$pkgs" ;;
        apk) plan="${sudo}apk add$pkgs" ;;
        *) manual="installe$pkgs avec le gestionnaire de paquets de ton système, puis relance cette commande." ;;
      esac
      if [ -n "$plan" ] && [ "$(id -u)" != 0 ] && [ -z "$sudo" ]; then
        manual="lance en administrateur (root) : $plan"; plan=""
      fi ;;
  esac

  echo "Il manque à cadrer-x :$missing."
  if [ -z "$plan" ]; then
    echo "Pour l'installer, $manual" >&2; exit 1
  fi
  echo "Pour l'installer, je vais lancer :"
  echo "  $plan"
  if [ -n "$note" ]; then echo "$note"; fi
  ask "Installer maintenant ? [o/N]" || rc=$?
  if [ "$rc" = 1 ]; then
    echo "D'accord, je n'installe rien. Lance cette commande toi-même, puis relance l'installation de cadrer-x." >&2
    exit 1
  elif [ "$rc" = 2 ]; then
    echo "Je ne peux pas te poser la question ici : lance cette commande toi-même, puis relance l'installation (ou relance-la avec --yes)." >&2
    exit 1
  fi

  # Piped, stdin is this script: an installer reading it would eat the rest. sudo asks on the terminal.
  eval "$plan" </dev/null || true
  if [ "$plan" = "xcode-select --install" ]; then
    echo "J'attends la fin de l'installation des outils du Mac…"
    until xcode-select -p >/dev/null 2>&1 && /usr/bin/git --version >/dev/null 2>&1; do
      i=$((i + 1)); [ "$i" -gt 180 ] && break; sleep 10
    done
  fi
  hash -r
  if [ "$os" = windows ] && ! works python3; then win_python3 || true; fi

  for tool in $missing; do works "$tool" || still="$still $tool"; done
  if [ -n "$still" ]; then
    echo "Toujours introuvable :$still. Si l'installation a échoué, lance la commande ci-dessus toi-même ; sinon, ouvre un nouveau terminal. Puis relance cette commande." >&2
    exit 1
  fi
  echo "C'est installé :$missing."
}

if [ "$help" = 0 ] && [ "$remove" = 0 ]; then
  need_tools git python3 tar
elif [ "$fetch" = 1 ]; then
  need_tools git
fi

# Run from a pipe, or from outside a clone: fetch or update the clone, then run its install.sh.
if [ "$fetch" = 1 ]; then
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
      echo "$home existe déjà et n'est pas une copie de cadrer-x : déplace-le, ou choisis un autre dossier avec CADRER_X_HOME." >&2
      exit 1
    fi
    git -C "$home" pull --ff-only --quiet || echo "Impossible de mettre à jour $home : j'installe la version qu'il contient." >&2
  else
    # Git for Windows turns LF into CRLF on checkout by default, and bash cannot run a CRLF script.
    git clone -c core.autocrlf=false --quiet https://github.com/Karnonson/cadrer-x.git "$home" ||
      { echo "Impossible de télécharger cadrer-x : vérifie ta connexion à internet, puis relance cette commande." >&2; exit 1; }
  fi
  if [ "$piped" = 1 ]; then exec bash "$home/install.sh" "$@" </dev/null; fi
  exec bash "$home/install.sh" "$@"
fi

self="$here/install.sh"
src="$here/skills"
# Skills cadrer-x no longer has, taken out of the destination by every install and --remove: when a
# skill becomes a reference, append its folder's name.
retired="cadrer-x-examiner cadrer-x-affiner cadrer-x-decouper"
scope=project dir=. engines="" link=0

while [ $# -gt 0 ]; do
  case "$1" in
    --global) scope=global ;;
    --engine) shift; case "${1:-}" in claude|codex) engines="$1" ;; *) echo "--engine attend claude ou codex" >&2; exit 2 ;; esac ;;
    --link) link=1 ;;
    --remove|--yes) ;;
    -h|--help) sed -n '2,22p' "$self" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "Option inconnue : $1 (voir --help)" >&2; exit 2 ;;
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
  [ -d "$dir" ] || { echo "Pas de dossier $dir" >&2; exit 1; }
  base="$(cd "$dir" && pwd)"
  [ "$base" = "$(cd "$src/.." && pwd)" ] && { echo "C'est le dossier de cadrer-x lui-même : donne le dossier de ton projet, ou utilise --global." >&2; exit 1; }
fi

for engine in $engines; do
  case "$engine" in claude) dest="$base/.claude/skills" ;; codex) dest="$base/.agents/skills" ;; esac
  mkdir -p "$dest"
  [ "$(cd "$dest" && pwd -P)" = "$(cd "$src" && pwd -P)" ] && { echo "$dest est le dossier des skills de cadrer-x lui-même : rien à faire." >&2; continue; }
  for name in $retired; do
    [ -e "$dest/$name" ] || [ -L "$dest/$name" ] || continue
    rm -rf "${dest:?}/${name:?}" && printf '%-10s%s\n' retiré "$dest/$name"
  done
  for skill in "$src"/cadrer-x-*/; do
    name="$(basename "$skill")"
    # A skill has SKILL.md, a helper aide.md; a folder with neither holds only templates so far.
    [ -f "$skill/SKILL.md" ] || [ -f "$skill/aide.md" ] || continue
    target="$dest/$name"
    rm -rf "${target:?}"
    [ "$remove" = 1 ] && { printf '%-10s%s\n' retiré "$target"; continue; }
    if [ "$link" = 1 ]; then
      ln -s "${skill%/}" "$target"
    else
      mkdir -p "$target"
      (cd "$skill" && tar --exclude=__pycache__ --exclude="*.pyc" -cf - .) | (cd "$target" && tar -xf -)
    fi
    printf '%-10s%s\n' "$([ "$link" = 1 ] && echo lié || echo copié)" "$target"
  done
done

# The git commands every step runs, so a build is not a prompt per merge. Pushing stays asked.
if [ "$scope" = project ] && [[ " $engines " == *" claude "* ]]; then
  py=""
  for cand in python3 python; do
    "$cand" -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1 && { py="$cand"; break; }
  done
  if [ -z "$py" ]; then
    echo "Python 3 introuvable : .claude/settings.json reste tel quel (Claude Code demandera chaque commande git)." >&2
  else
    "$py" - "$base/.claude/settings.json" "$remove" "$src/cadrer-x-init/references/permissions.json" <<'PY'
import json, sys, pathlib
path, remove = pathlib.Path(sys.argv[1]), sys.argv[2] == "1"
# The list lives with cadrer-x-init, which merges the same file when the plugin installed cadrer-x.
rules = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
allow, ask = rules["allow"], rules["ask"]
data = json.loads(path.read_text(encoding="utf-8")) if path.exists() and path.read_text(encoding="utf-8").strip() else {}
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
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{'nettoyé' if remove else 'autorisé':<9}les commandes git dans {path}")
PY
  fi
fi

if [ "$scope" = project ] && [ "$remove" = 0 ]; then
  echo
  echo "Installé pour ce projet seulement. Ajoute .claude/skills, .agents/skills et .claude/settings.json"
  echo "au dépôt git du projet (commit) pour que tout le monde y ait la même version."
  echo "Pour tous tes projets à la place : bash $self --global"
fi
