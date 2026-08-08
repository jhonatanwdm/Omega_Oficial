from __future__ import annotations

import re
from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteAtualizacao(SubAgente):
    nome = "atualizacao"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["atualize para", "versão", "versao", "backup", "restaure"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        updates = deps["atualizacoes"]
        backups = deps["backups"]
        t = ctx.texto
        if "backup" in t.lower() and "restaure" not in t.lower():
            meta = await backups.criar(rotulo="manual")
            return ResultadoAgente(self.nome, True, f"Backup criado: {meta['id']}", meta)
        m = re.search(r"restaure\s+(\S+)", t, re.I)
        if m:
            r = await backups.restaurar(m.group(1))
            return ResultadoAgente(self.nome, r.get("ok", False), str(r), r)
        m = re.search(r"atualize para\s+(\S+)\s*(?:-\s*(.*))?", t, re.I)
        if m:
            r = await updates.aplicar(m.group(1), m.group(2) or "Update Omega", confirmado=ctx.confirmado)
            return ResultadoAgente(self.nome, r.get("ok", False), str(r), r)
        return ResultadoAgente(self.nome, True, str(updates.estado()), updates.estado())
