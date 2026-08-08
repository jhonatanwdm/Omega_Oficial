$ErrorActionPreference = "Stop"
$raiz = Split-Path $PSScriptRoot -Parent
Set-Location $raiz

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
  python -m venv .venv
}

$py = ".\.venv\Scripts\python.exe"
$pip = ".\.venv\Scripts\pip.exe"

& $pip install -q -r requirements.txt
& $pip install -q pyinstaller

if (Test-Path .\build) { Remove-Item -Recurse -Force .\build }
if (Test-Path .\dist\Omega.exe) { Remove-Item -Force .\dist\Omega.exe }
if (Test-Path .\dist\Omega) { Remove-Item -Recurse -Force .\dist\Omega }
if (Test-Path .\Omega.exe) { Remove-Item -Force .\Omega.exe }

& $py -m PyInstaller --noconfirm --clean omega_hub.spec

Copy-Item -Force .\dist\Omega.exe .\Omega.exe

Write-Host ""
Write-Host "Pronto - um unico executavel:"
Write-Host ("  " + (Join-Path $raiz "Omega.exe"))
