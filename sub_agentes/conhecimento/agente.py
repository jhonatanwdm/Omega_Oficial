from __future__ import annotations

import re
from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteConhecimento(SubAgente):
    nome = "conhecimento"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["lembre", "memorize", "salve que", "o que você sabe", "busque conhecimento", "rag"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        memoria = deps["memoria"]
        t = ctx.texto
        m = re.search(r"(?:lembre|memorize|salve que)\s+(.+)", t, flags=re.I)
        if m:
            conteudo = m.group(1).strip()
            item = await memoria.gravar_conhecimento(titulo=conteudo[:80], conteudo=conteudo)
            return ResultadoAgente(
                self.nome,
                True,
                f"Conhecimento salvo (id={item.id}).",
                {"id": item.id},
            )
        hits = await memoria.buscar_conhecimento(t, limite=5)
        if not hits:
            return ResultadoAgente(self.nome, True, "Nenhum conhecimento relevante encontrado.", {"hits": []})
        linhas = [f"- ({h['score']:.2f}) {h['texto'][:200]}" for h in hits]
        return ResultadoAgente(self.nome, True, "Conhecimento relacionado:\n" + "\n".join(linhas), {"hits": hits})
