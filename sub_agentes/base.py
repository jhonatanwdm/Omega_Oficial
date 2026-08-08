from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextoAgente:
    texto: str
    conversa_id: str | None = None
    plataforma: str = "hub"
    confirmado: bool = False
    metadados: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResultadoAgente:
    agente: str
    ok: bool
    saida: str
    dados: dict[str, Any] = field(default_factory=dict)


class SubAgente(ABC):
    nome: str = "base"

    @abstractmethod
    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        ...

    @abstractmethod
    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        ...
