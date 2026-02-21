$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")

Set-Location $repoRoot

if (Get-Command py -ErrorAction SilentlyContinue) {
  py scripts/run_local.py
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  python scripts/run_local.py
} else {
  throw "Python was not found in PATH. Install Python 3.10+ and retry."
}
