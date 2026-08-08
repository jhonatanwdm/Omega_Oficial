# Omega

Agente de IA pessoal híbrido (local + cloud autorizada), interface Flutter (Android, Web, Desktop) e núcleo Python.

## Início rápido

```powershell
# 1) Ambiente Python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2) Infra (opcional — Docker)
docker compose up -d

# 3) Hub Omega
python -m nucleo.api.principal

# 4) Cliente Flutter (requer Flutter SDK)
cd apps/omega_cliente
flutter pub get
flutter run -d windows
```

Sem Docker, o hub sobe com SQLite + memória vetorial embutida + LLM mock/Ollama.

## Estrutura

- `nucleo/` — cérebro FastAPI
- `sub_agentes/` — agentes especializados
- `apps/omega_cliente/` — Flutter
- `configs/` — políticas, permissões, diretrizes, padrões
- `docs/` — documentação PT-BR

## Executável Windows (Hub)

Um único arquivo na raiz:

```text
Omega.exe
```

Duplo clique para iniciar. Hub em `http://127.0.0.1:8741` (token `omega-dev-local`).

Para regenerar:

```powershell
.\scripts\build_exe.ps1
```

## Versão

`0.1.0` — Fundação + módulos das fases 0–6 + executável Windows.
