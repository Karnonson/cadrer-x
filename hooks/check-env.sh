#!/bin/sh
# SessionStart hook of the cadrer-x plugin: the steps need git and Python 3 (as python3). Silent when
# both work; otherwise prints what is missing for Claude's context, so the agent offers the install
# and runs it only on the person's yes, the way install.sh does. Windows runs it with Git Bash; with
# no Git Bash there is no git either, and the steps' first git command says so.

os="$(uname -s 2>/dev/null || echo unknown)"

# A Mac without the Command Line Tools has /usr/bin/git and /usr/bin/python3 stubs that open a
# dialog when run: don't run them.
clt=1
case "$os" in Darwin) xcode-select -p >/dev/null 2>&1 || clt=0 ;; esac
works() {
  [ "$clt" = 0 ] && case "$(command -v "$1")" in /usr/bin/*) return 1 ;; esac
  "$@" >/dev/null 2>&1
}

missing="" py_alt=""
works git --version || missing="git"
if ! works python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))'; then
  for cand in "py -3" python; do
    # shellcheck disable=SC2086 # "py -3" is two words on purpose
    if works $cand -c 'import sys; sys.exit(sys.version_info < (3, 8))'; then py_alt="$cand"; break; fi
  done
  [ -z "$py_alt" ] && missing="${missing:+$missing and }Python 3"
fi

if [ -n "$py_alt" ]; then
  echo "cadrer-x: on this computer Python 3 runs as \`$py_alt\`, not \`python3\`: wherever a cadrer-x skill says \`python3\`, run \`$py_alt\` instead."
fi
[ -z "$missing" ] && exit 0

case "$os" in
  Darwin)
    if command -v brew >/dev/null 2>&1; then how="brew install git python"
    else how="xcode-select --install (Apple's Command Line Tools: git and python3; it opens a dialog)"; fi ;;
  Linux)
    how="the system's package manager, e.g. sudo apt-get install -y git python3 (dnf, pacman: python, zypper, apk alike)" ;;
  MINGW*|MSYS*|CYGWIN*)
    how="winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements" ;;
  *) how="the system's usual installer" ;;
esac
echo "cadrer-x: this computer is missing $missing, which the cadrer-x steps need. Before a cadrer-x step runs, tell the person in their language what is missing and why, show the exact command that installs it ($how), and run it only after their yes; then check it works. If they say no, the step cannot go on: say so plainly."
