# Install the cadrer-x skills for Claude Code and codex, on Windows (PowerShell 5.1 or 7).
#
# One command, from the folder to install into:
#   irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex
# With options (the same as install.sh's: [DIR] --global --engine claude|codex --link --remove
# --yes --help):
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1))) --engine codex
#
# It checks for Git for Windows (its bash runs install.sh) and a Python 3 that really runs (not the
# Microsoft Store stub), offers to install what is missing with winget (--yes: without asking),
# then downloads install.sh and runs it with Git's bash from the current folder: install.sh does
# the rest (~/cadrer-x, the skills, .claude/settings.json). The folder of the real Python found
# goes first in PATH, so bash finds it as python.
#
# Under `irm | iex` this runs in the person's own session: never `exit` (it would close their
# window), only `return`, and nothing but these functions at the top level. The source stays ASCII
# so Windows PowerShell 5.1 reads it the same from a BOM-less file: accented letters are written
# {e} (e acute), {eg} (e grave), {ec} (e circumflex), {a} (a grave), {u} (u grave), {c} (c
# cedilla), and Write-CxSay puts them back.

function Write-CxSay {
  param([string]$Text, [string]$Color)
  $letters = @(@('{eg}', 0xE8), @('{ec}', 0xEA), @('{e}', 0xE9), @('{a}', 0xE0), @('{u}', 0xF9),
    @('{c}', 0xE7))
  foreach ($pair in $letters) { $Text = $Text.Replace($pair[0], [string][char]$pair[1]) }
  if ($Color) { Write-Host $Text -ForegroundColor $Color } else { Write-Host $Text }
}

function Test-CxWindows { return ($env:OS -eq 'Windows_NT') }

function Test-CxUnderWindowsDir {
  param([string]$Path)
  $root = $env:SystemRoot
  if (-not $root) { return $false }
  return $Path.StartsWith($root.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase) -or
    $Path.Equals($root, [StringComparison]::OrdinalIgnoreCase)
}

# Git's own bash.exe, never C:\Windows\System32\bash.exe (that one is WSL, another filesystem).
function Find-CxBash {
  $roots = @()
  foreach ($git in @(Get-Command git -CommandType Application -All -ErrorAction SilentlyContinue)) {
    # ...\Git\cmd\git.exe, ...\Git\bin\git.exe or ...\Git\mingw64\bin\git.exe
    $dir = Split-Path -Parent $git.Source
    for ($i = 0; $i -lt 3 -and $dir; $i++) { $roots += $dir; $dir = Split-Path -Parent $dir }
  }
  foreach ($key in @('HKLM:\SOFTWARE\GitForWindows', 'HKCU:\SOFTWARE\GitForWindows',
      'HKLM:\SOFTWARE\WOW6432Node\GitForWindows')) {
    try { $item = Get-ItemProperty -Path $key -Name InstallPath -ErrorAction Stop } catch { continue }
    if ($item.InstallPath) { $roots += $item.InstallPath }
  }
  if ($env:ProgramFiles) { $roots += Join-Path $env:ProgramFiles 'Git' }
  if ($env:LOCALAPPDATA) { $roots += Join-Path $env:LOCALAPPDATA 'Programs\Git' }
  foreach ($root in $roots) {
    $bash = Join-Path $root 'bin\bash.exe'
    if ((Test-Path -LiteralPath $bash -PathType Leaf) -and -not (Test-CxUnderWindowsDir $bash)) {
      return $bash
    }
  }
  return $null
}

# The path of a Python 3 that runs. python.exe and python3.exe in WindowsApps can be Store stubs
# that only print an error: each candidate is run, not just found.
function Find-CxPython {
  $ErrorActionPreference = 'Continue'
  $probe = 'import sys; print(sys.version_info[0]); print(sys.executable)'
  $tries = @()
  foreach ($cmd in @(Get-Command py -CommandType Application -All -ErrorAction SilentlyContinue)) {
    $tries += , @($cmd.Source, '-3')
  }
  foreach ($name in @('python', 'python3')) {
    foreach ($cmd in @(Get-Command $name -CommandType Application -All -ErrorAction SilentlyContinue)) {
      $tries += , @($cmd.Source)
    }
  }
  $globs = @()
  if ($env:LOCALAPPDATA) { $globs += Join-Path $env:LOCALAPPDATA 'Programs\Python\Python3*\python.exe' }
  if ($env:ProgramFiles) { $globs += Join-Path $env:ProgramFiles 'Python3*\python.exe' }
  foreach ($glob in $globs) {
    $found = @(Get-ChildItem -Path $glob -ErrorAction SilentlyContinue | Sort-Object Name -Descending)
    foreach ($file in $found) {
      $tries += , @($file.FullName)
    }
  }
  foreach ($try in $tries) {
    $exe = $try[0]
    $rest = @($try | Select-Object -Skip 1)
    # An empty stdin: a launcher that asks something (install a Python?) gets no and stops.
    try { $out = @('' | & $exe @rest -c $probe 2>$null) } catch { continue }
    if ($LASTEXITCODE -eq 0 -and $out.Count -ge 2 -and "$($out[0])".Trim() -eq '3') {
      return "$($out[1])".Trim()
    }
  }
  return $null
}

function Test-CxWinget {
  $ErrorActionPreference = 'Continue'
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { return $false }
  try { $null = & winget --version 2>$null } catch { return $false }
  return ($LASTEXITCODE -eq 0)
}

# For this user only (no administrator needed): both packages have a per-user installer. Not
# captured, so winget shows its progress; the caller reads $LASTEXITCODE.
function Invoke-CxWinget {
  param([string]$Id)
  $ErrorActionPreference = 'Continue'
  & winget install -e --id $Id --source winget --scope user --accept-package-agreements `
    --accept-source-agreements
}

# What winget just installed is in the registry's PATH, not yet in this window's.
function Sync-CxPath {
  $parts = @()
  foreach ($scope in @('Machine', 'User')) {
    $value = [Environment]::GetEnvironmentVariable('Path', $scope)
    if ($value) { $parts += $value.Split(';') }
  }
  if ($env:Path) { $parts += $env:Path.Split(';') }
  $seen = @{}
  $keep = @()
  foreach ($part in $parts) {
    $part = $part.Trim()
    if ($part -and -not $seen.ContainsKey($part)) { $seen[$part] = $true; $keep += $part }
  }
  $env:Path = $keep -join ';'
}

# install.sh for bash: UTF-8 without a BOM, LF line endings.
function Write-CxInstallSh {
  param([string]$Text, [string]$Path)
  $Text = $Text.Replace("`r", '')
  [IO.File]::WriteAllText($Path, $Text, (New-Object Text.UTF8Encoding $false))
}

function Get-CxInstallSh {
  param([string]$Path)
  # Windows PowerShell 5.1 on an older .NET may not offer TLS 1.2 by itself; GitHub requires it.
  try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor
      [Net.SecurityProtocolType]::Tls12
  } catch { Write-Verbose "TLS 1.2: $($_.Exception.Message)" }
  $url = 'https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh'
  # The bytes, read as UTF-8: .Content would depend on the charset the server sends.
  $bytes = (Invoke-WebRequest -Uri $url -UseBasicParsing).RawContentStream.ToArray()
  $text = [Text.Encoding]::UTF8.GetString($bytes).TrimStart([char]0xFEFF)
  Write-CxInstallSh -Text $text -Path $Path
}

# Not captured, so bash talks with the person directly; the caller reads $LASTEXITCODE.
function Invoke-CxBash {
  param([string]$Bash, [string[]]$Arguments)
  & $Bash @Arguments
}

function Show-CxHelp {
  Write-CxSay @'
Installe les skills cadrer-x dans le dossier de ton projet, pour Claude Code et codex.
Ouvre PowerShell dans ce dossier (ou va dedans avec cd), puis :

  irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1 | iex

Avec des options :

  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.ps1))) --engine codex

Options :
  DOSSIER          installer dans ce dossier au lieu du dossier actuel
  --global         installer pour tous tes projets
  --engine claude  seulement pour Claude Code (--engine codex : seulement pour codex)
  --link           suivre %USERPROFILE%\cadrer-x ; sous Windows, une simple copie : relance la ligne
  --remove         retirer les skills cadrer-x
  --yes            installer ce qui manque sans poser la question
  --help           afficher cette aide

Il faut Git pour Windows et Python 3 : s'ils manquent, je te propose de les installer.
'@
}

function Invoke-CxInstall {
  $ErrorActionPreference = 'Stop'
  $gitLink = 'https://git-scm.com/download/win'
  $pythonLink = 'https://www.python.org/downloads/windows/'
  $tmp = $null
  try {
    # The options: only --help is handled here; install.sh checks the rest, a few are checked
    # first so that a typo stops before anything gets installed.
    $yes = $false
    $isGlobal = $false
    $dir = $null
    $pass = @()
    for ($i = 0; $i -lt $args.Count; $i++) {
      $arg = [string]$args[$i]
      if ($arg -eq '-h' -or $arg -eq '--help') { Show-CxHelp; return }
      if ($arg -eq '--yes') { $yes = $true }
      elseif ($arg -eq '--global') { $isGlobal = $true }
      elseif ($arg -eq '--engine') {
        $next = $null
        if ($i + 1 -lt $args.Count) { $next = [string]$args[$i + 1] }
        if ($next -ne 'claude' -and $next -ne 'codex') {
          Write-CxSay "Apr{eg}s --engine, mets claude ou codex." Yellow
          return
        }
        $pass += $arg
        $arg = $next
        $i++
      }
      elseif ($arg -eq '--link' -or $arg -eq '--remove') { }
      elseif ($arg.StartsWith('-')) {
        Write-CxSay "Je ne connais pas l'option $arg. La liste : --help" Yellow
        return
      }
      else {
        # A folder: bash reads C:/x/y better than C:\x\y.
        $dir = $arg
        $arg = $arg.Replace('\', '/')
      }
      $pass += $arg
    }

    if (-not (Test-CxWindows)) {
      Write-CxSay "Ce script est pour Windows. Sur macOS ou Linux :" Yellow
      Write-CxSay "  curl -fsSL https://raw.githubusercontent.com/Karnonson/cadrer-x/main/install.sh | bash"
      return
    }
    if ($PWD.Provider.Name -ne 'FileSystem') {
      Write-CxSay "PowerShell n'est pas dans un dossier de fichiers ($PWD)." Yellow
      Write-CxSay "Va dans le dossier de ton projet avec cd, puis relance la commande."
      return
    }
    if (-not $isGlobal -and -not $dir -and (Test-CxUnderWindowsDir $PWD.ProviderPath)) {
      Write-CxSay "PowerShell est dans le dossier de Windows ($($PWD.ProviderPath)), pas dans ton projet." Yellow
      Write-CxSay "Va dans le dossier de ton projet, par exemple : cd `$HOME\Documents\mon-projet"
      Write-CxSay "puis relance la commande."
      return
    }

    # What is missing.
    $bash = Find-CxBash
    $python = Find-CxPython
    $missing = @()
    if (-not $bash) { $missing += , @('Git pour Windows', 'Git.Git', $gitLink) }
    if (-not $python) { $missing += , @('Python 3', 'Python.Python.3.13', $pythonLink) }
    if ($missing.Count -gt 0) {
      $hasWinget = Test-CxWinget
      Write-CxSay "Il manque sur cet ordinateur, pour installer cadrer-x :"
      foreach ($m in $missing) {
        if ($hasWinget) { Write-CxSay "  - $($m[0]) : winget install -e --id $($m[1])" }
        else { Write-CxSay "  - $($m[0]) : $($m[2])" }
      }
      if (-not $hasWinget) {
        Write-CxSay "winget, l'outil qui les installerait, n'est pas sur cet ordinateur." Yellow
        Write-CxSay "T{e}l{e}charge-les depuis ces liens et installe-les,"
        Write-CxSay "puis ferme PowerShell, rouvre-le et relance la commande."
        return
      }
      if (-not $yes) {
        $answer = ''
        try { $answer = Read-Host 'Installer maintenant ? [o/N]' } catch { $answer = '' }
        if (@('o', 'oui', 'y', 'yes') -notcontains "$answer".Trim().ToLower()) {
          Write-CxSay "D'accord, rien n'a {e}t{e} install{e}. Relance la commande quand tu veux."
          return
        }
      }
      Write-CxSay "Installation en cours. Si Windows te demande une autorisation, accepte."
      foreach ($m in $missing) {
        Invoke-CxWinget $m[1]
        # 0: installed. The other two: already there (the check after the PATH refresh decides).
        if (@(0, -1978335189, -1978335135) -notcontains $LASTEXITCODE) {
          Write-CxSay "L'installation de $($m[0]) n'a pas march{e}. Installe-le depuis $($m[2])" Yellow
          Write-CxSay "puis ferme PowerShell, rouvre-le et relance la commande."
          return
        }
      }
      Sync-CxPath
      $bash = Find-CxBash
      $python = Find-CxPython
      if (-not $bash -or -not $python) {
        Write-CxSay "C'est install{e}, mais cette fen{ec}tre PowerShell ne le voit pas encore." Yellow
        Write-CxSay "Ferme PowerShell, rouvre-le dans le dossier de ton projet et relance la commande."
        return
      }
    }

    # bash finds python through PATH.
    $pythonDir = Split-Path -Parent $python
    if (@("$env:Path".Split(';')) -notcontains $pythonDir) { $env:Path = $pythonDir + ';' + $env:Path }

    $name = 'cadrer-x-install-' + [guid]::NewGuid().ToString('N') + '.sh'
    $tmp = Join-Path ([IO.Path]::GetTempPath()) $name
    try { Get-CxInstallSh -Path $tmp } catch {
      Write-CxSay "Je n'arrive pas {a} t{e}l{e}charger le programme d'installation." Yellow
      Write-CxSay "V{e}rifie ta connexion {a} internet, puis relance la commande."
      return
    }

    # PowerShell starts bash in the current folder ($PWD); install.sh installs there.
    Invoke-CxBash -Bash $bash -Arguments (@($tmp.Replace('\', '/')) + $pass)
    if ($LASTEXITCODE -ne 0) {
      Write-CxSay "L'installation s'est arr{ec}t{e}e avant la fin (code $LASTEXITCODE)." Yellow
      Write-CxSay "Le message juste au-dessus dit pourquoi."
    }
  } catch {
    Write-CxSay "L'installation s'est arr{ec}t{e}e sur une erreur : $($_.Exception.Message)" Yellow
  } finally {
    if ($tmp -and (Test-Path -LiteralPath $tmp)) {
      Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
  }
}

Invoke-CxInstall @args
