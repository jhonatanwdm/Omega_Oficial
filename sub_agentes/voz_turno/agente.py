from __future__ import annotations

from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgenteVozTurno(SubAgente):
    nome = "voz_turno"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        return bool(ctx.metadados.get("audio_bytes") or ctx.metadados.get("modo") == "voz")

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        voz = deps["voz"]
        audio = ctx.metadados.get("audio_bytes")
        texto = ctx.texto
        if audio:
            stt = voz.transcrever(audio)
            texto = stt.texto or texto
        tts = voz.sintetizar(texto if ctx.metadados.get("somente_eco") else ctx.metadados.get("resposta", texto))
        anim = voz.estado_animacao("falando")
        return ResultadoAgente(
            self.nome,
            True,
            texto,
            {"tts": tts.__dict__, "animacao": anim, "transcricao": texto},
        )
