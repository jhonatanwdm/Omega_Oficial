from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatPedido(BaseModel):
    texto: str
    conversa_id: str | None = None
    plataforma: str = "hub"
    confirmado: bool = False
    modo: str = "texto"  # texto | voz


class CloudPedido(BaseModel):
    minutos: int = Field(default=30, ge=1, le=60)
    confirmado: bool = False


class FerramentaPedido(BaseModel):
    ferramenta_id: str
    plataforma: str = "hub"
    confirmado: bool = False
    args: dict[str, Any] = Field(default_factory=dict)


class ConhecimentoPedido(BaseModel):
    titulo: str
    conteudo: str
    tags: str = ""
    critico: bool = False


class TreinoExemploPedido(BaseModel):
    entrada: str
    saida: str
    tags: str = ""


class UpdatePedido(BaseModel):
    versao: str
    notas: str = "Update Omega"
    confirmado: bool = False


class AperfPropostaPedido(BaseModel):
    motivo: str
    novo_sistema: str


class AperfApplyPedido(BaseModel):
    proposta_id: str
    confirmado: bool = False


class SyncPedido(BaseModel):
    entidade: str
    desde_versao: int = 0


class TempoPedido(BaseModel):
    relogio_cliente_utc: str | None = None
