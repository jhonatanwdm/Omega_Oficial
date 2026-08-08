from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteAgenda(SubAgente):
    nome = "agenda"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["agenda", "lembrete", "compromisso", "marque", "reunião", "reuniao"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        memoria = deps["memoria"]
        politicas = deps["politicas"]
        t = ctx.texto
        if re.search(r"\b(liste|mostrar|ver)\b.*\bagenda\b|\bagenda\b.*\b(hoje|semana)\b", t, re.I):
            eventos = await memoria.listar_agenda()
            if not eventos:
                return ResultadoAgente(self.nome, True, "Agenda vazia.", {})
            linhas = [f"- {e.titulo} @ {e.inicia_em_utc.isoformat()}" for e in eventos[:20]]
            return ResultadoAgente(self.nome, True, "Agenda:\n" + "\n".join(linhas), {"n": len(eventos)})

        dec = politicas.avaliar("agenda_escrever", ctx.plataforma, ctx.confirmado)
        if not dec.permitido:
            return ResultadoAgente(
                self.nome,
                False,
                dec.motivo,
                {"exige_confirmacao": dec.exige_confirmacao},
            )
        titulo = re.sub(r"(?i).*?(?:marque|lembrete|compromisso)\s*", "", t).strip() or t
        inicio = datetime.now(timezone.utc) + timedelta(hours=1)
        ev = await memoria.criar_evento_agenda(titulo=titulo[:120], inicia_em_utc=inicio, descricao=t)
        return ResultadoAgente(self.nome, True, f"Evento criado: {ev.titulo} em {ev.inicia_em_utc.isoformat()}", {"id": ev.id})
