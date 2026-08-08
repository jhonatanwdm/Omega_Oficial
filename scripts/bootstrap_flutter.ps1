$ErrorActionPreference = "Stop"
Set-Location (Join-Path (Split-Path $PSScriptRoot -Parent) "apps\omega_cliente")
if (-not (Get-Command flutter -ErrorAction SilentlyContinue)) {
  Write-Host "Instale o Flutter SDK e rode este script novamente."
  exit 1
}
flutter create --project-name omega_cliente --org br.omega .
flutter pub get
Write-Host "Cliente pronto. Use: flutter run -d windows"
