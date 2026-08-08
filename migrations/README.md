# Migrações Omega (Alembic)

Baseline leve. O hub ainda cria tabelas via SQLModel no startup (`ServicoMemoria.inicializar`).
Esta pasta prepara o caminho para migrações versionadas quando o schema estabilizar.

## Uso (quando Alembic estiver no ambiente)

```bash
# a partir da raiz do projeto, com venv ativo
alembic revision --autogenerate -m "baseline"
alembic upgrade head
```

`alembic.ini` e `migrations/env.py` apontam para `OMEGA_DATABASE_URL` ou SQLite em `dados/omega.db`.
