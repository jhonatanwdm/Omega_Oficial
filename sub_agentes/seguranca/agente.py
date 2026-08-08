from __future__ import annotations

from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteSeguranca(SubAgente):
    nome = "seguranca"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        return True  # sempre consultável

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        politicas = deps["politicas"]
        acao = ctx.metadados.get("acao", "conversar_texto")
        dec = politicas.avaliar(acao, plataforma=ctx.plataforma, confirmado=ctx.confirmado)
        await deps["memoria"].registrar_auditoria(acao, dec.permitido, dec.motivo)
        return ResultadoAgente(
            agente=self.nome,
            ok=dec.permitido,
            saida=dec.motivo,
            dados={
                "permitido": dec.permitido,
                "risco": dec.risco,
                "exige_confirmacao": dec.exige_confirmacao,
            },
        )
