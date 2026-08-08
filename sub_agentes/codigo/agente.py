from __future__ import annotations

from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteCodigo(SubAgente):
    nome = "codigo"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["código", "codigo", "refatore", "implemente", "bug", "teste unitário", "pytest"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        llm = deps["llm"]
        sistema = (
            deps["aperfeicoamento"].prompt_sistema()
            + " Ajude no desenvolvimento do monorepo Omega com respostas práticas em pt-BR."
        )
        resp = await llm.gerar(ctx.texto, sistema=sistema)
        return ResultadoAgente(self.nome, True, resp.texto, {"provedor": resp.provedor, "modelo": resp.modelo})
