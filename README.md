# Omega

Agente de IA pessoal híbrido (local + cloud autorizada), interface web no hub, cliente Flutter (Android, Web, Desktop) e núcleo Python.

## Início rápido

### Hub + UI web (recomendado)

```powershell
# Duplo clique ou:
.\Omega.exe
```

Abre o hub em `http://127.0.0.1:8741/` e o navegador automaticamente.
Token das APIs: `omega-dev-local` (header `X-Omega-Token`).

### Desenvolvimento Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m nucleo.api.principal
```

### Cliente Flutter

```powershell
$env:Path = "C:\flutter\bin;" + $env:Path
cd apps\omega_cliente
flutter pub get
dart run build_runner build
flutter run -d windows
# ou: flutter run -d chrome
```

Sem Docker, o hub sobe com SQLite + memória vetorial embutida + LLM mock/Ollama.

## Estrutura

- `nucleo/` — cérebro FastAPI + UI estática (`nucleo/api/estatico`)
- `sub_agentes/` — agentes especializados
- `apps/omega_cliente/` — Flutter (android/web/windows)
- `configs/` — políticas, permissões, diretrizes, padrões
- `migrations/` — baseline Alembic
- `docs/` — documentação PT-BR

## Executável Windows

Um único arquivo na raiz:

```text
Omega.exe
```

Inicia o hub **e** abre a UI. Regenerar:

```powershell
.\scripts\build_exe.ps1
```

## Versão

`1.0.1` - API Groq, UI redesenhada e lançamento windowed.
