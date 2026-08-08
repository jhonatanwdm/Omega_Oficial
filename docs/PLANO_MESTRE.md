# Plano Mestre Omega v1 (implementado)

Ver também o plano Cursor anexado. Este documento espelha o estado do repositório.

## Decisões

- Cérebro híbrido Python (Ollama local + cloud gated)
- UI Flutter (Android / Web / Windows)
- Persistência: PostgreSQL ou SQLite fallback + Qdrant ou vetor local
- Governança em `configs/*.yaml`

## Fases

0. Fundação — feita
1. Cérebro conversacional — feita
2. Voz + UI viva — feita (pipeline + animações de estado)
3. Ferramentas autorizadas — feita
4. Sub-agentes — feitos
5. Treino / autoaperfeiçoamento — feito (sandbox)
6. Sync / backups / updates / tempo — feitos
