from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class Conversa(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    titulo: str = "Conversa Omega"
    criado_em_utc: datetime = Field(default_factory=_agora)
    atualizado_em_utc: datetime = Field(default_factory=_agora)
    fuso_origem: str = "America/Sao_Paulo"
    versao_sync: int = 1


class Mensagem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversa_id: str = Field(index=True)
    papel: str  # usuario | omega | sistema
    conteudo: str
    criado_em_utc: datetime = Field(default_factory=_agora)
    atualizado_em_utc: datetime = Field(default_factory=_agora)
    fuso_origem: str = "America/Sao_Paulo"
    versao_sync: int = 1
    metadados_json: str = "{}"


class ItemConhecimento(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    titulo: str
    conteudo: str
    tags: str = ""
    critico: bool = False
    criado_em_utc: datetime = Field(default_factory=_agora)
    atualizado_em_utc: datetime = Field(default_factory=_agora)
    fuso_origem: str = "America/Sao_Paulo"
    versao_sync: int = 1
    vetor_id: Optional[str] = None


class EventoAgenda(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    titulo: str
    descricao: str = ""
    inicia_em_utc: datetime
    termina_em_utc: Optional[datetime] = None
    criado_em_utc: datetime = Field(default_factory=_agora)
    atualizado_em_utc: datetime = Field(default_factory=_agora)
    versao_sync: int = 1


class Auditoria(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    acao: str
    permitido: bool
    detalhe: str = ""
    criado_em_utc: datetime = Field(default_factory=_agora)


class CursorSync(SQLModel, table=True):
    entidade: str = Field(primary_key=True)
    cursor: int = 0
    atualizado_em_utc: datetime = Field(default_factory=_agora)
