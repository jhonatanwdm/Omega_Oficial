from __future__ import annotations

import re
from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteSistema(SubAgente):
    nome = "sistema"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["abra o arquivo", "leia o arquivo", "execute", "shell", "notifique android"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        tools = deps["ferramentas"]
        t = ctx.texto
        m = re.search(r"leia o arquivo\s+(.+)", t, re.I)
        if m:
            r = await tools.executar(
                "ler_arquivo_allowlist",
                plataforma=ctx.plataforma,
                confirmado=ctx.confirmado,
                caminho=m.group(1).strip().strip('"'),
            )
            return ResultadoAgente(self.nome, r.get("ok", False), r.get("conteudo") or r.get("erro", ""), r)

        m = re.search(r"execute\s+(.+)", t, re.I)
        if m:
            r = await tools.executar(
                "shell_allowlist",
                plataforma="hub",
                confirmado=ctx.confirmado,
                comando=m.group(1).strip(),
            )
            out = r.get("stdout") or r.get("erro") or ""
            return ResultadoAgente(self.nome, r.get("ok", False), out, r)

        if "notifique android" in t.lower():
            r = await tools.executar(
                "notificacao_android",
                plataforma="android",
                confirmado=True,
                titulo="Omega",
                corpo=t,
            )
            return ResultadoAgente(self.nome, True, "Notificação encaminhada ao cliente Android.", r)

        return ResultadoAgente(self.nome, False, "Não entendi a ação de sistema.", {})
