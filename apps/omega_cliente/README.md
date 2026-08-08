# Omega Cliente (Flutter)

Cliente único para Android, Web e Windows Desktop.

## Requisitos

- Flutter SDK 3.5+ (`C:\flutter\bin` no PATH)
- Hub Omega em `http://127.0.0.1:8741`
- **Windows**: Visual Studio Build Tools (Desktop C++)
- **Android**: Android SDK / Android Studio
- **Web**: Chrome
- Para plugins nativos de voz (`record` / `just_audio`): ative **Developer Mode** no Windows (symlinks)

## Setup

```powershell
$env:Path = "C:\flutter\bin;" + $env:Path
cd apps\omega_cliente
flutter pub get
dart run build_runner build
```

## Executar

```powershell
flutter run -d windows
flutter run -d chrome
# Android (quando SDK estiver configurado):
flutter run -d android
```

## Build Windows

```powershell
flutter build windows
```

Token padrão: `omega-dev-local` (header `X-Omega-Token`).

## Persistência

Drift + SQLite em `%APPDATA%\Omega\cliente\omega_local.sqlite` (sem plugin `path_provider`).

## Voz

Hooks em `lib/servicos/omega_voz.dart` (stub sem plugins nativos). Voz completa: UI web do hub com Web Speech.

## Nota Android

O projeto `android/` está gerado. Sem Android SDK, `flutter build apk` não roda — instale o SDK e use `flutter config --android-sdk <caminho>`.
