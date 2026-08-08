from __future__ import annotations

from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteTreino(SubAgente):
    nome = "treino"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["treine", "lora", "dataset", "aprenda este exemplo"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        treino = deps["treino"]
        t = ctx.texto
        if "aprenda este exemplo" in t.lower() and "|" in t:
            _, resto = t.split("aprenda este exemplo", 1)
            entrada, saida = [x.strip() for x in resto.split("|", 1)]
            item = treino.coletar_exemplo(entrada, saida)
            return ResultadoAgente(self.nome, True, "Exemplo adicionado ao dataset.", item)
        if "treine" in t.lower() or "lora" in t.lower():
            r = await treino.treinar_lora_sandbox(confirmado=ctx.confirmado)
            return ResultadoAgente(self.nome, r.get("ok", False), str(r), r)
        return ResultadoAgente(self.nome, True, f"Dataset com {len(treino.listar_dataset())} exemplos.", {})
