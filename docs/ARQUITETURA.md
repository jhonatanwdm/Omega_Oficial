# Arquitetura Omega

## Hub

`nucleo.api.principal` sobe FastAPI na porta `8741`.

Componentes:

- `orquestrador` — roteia intenções aos sub-agentes
- `politicas` — pode/não pode
- `memoria` — SQLModel + vetores
- `llm` — Ollama / cloud / mock
- `voz` — STT/TTS
- `ferramentas` — PC/Android allowlisted
- `treino` / `aperfeicoamento` / `backups` / `atualizacoes` / `tempo`

## Cliente

Flutter em `apps/omega_cliente` consome `/chat`, `/sync/pull`, `/tempo` e WebSocket `/ws/voz`.
