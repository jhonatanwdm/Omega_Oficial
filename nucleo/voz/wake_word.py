"""Stub de wake word local (ex.: 'Omega').

Integração futura: Porcupine / openWakeWord. Por enquanto, detecção textual
simples sobre transcript STT para manter o fluxo de voz plugável.
"""

from __future__ import annotations

from dataclasses import dataclass

from nucleo.comum.logging import get_logger

log = get_logger("voz.wake")

WAKE_PADRAO = ("omega", "ei omega", "olá omega", "ola omega")


@dataclass
class ResultadoWake:
    detectado: bool
    termo: str | None = None
    residual: str = ""


class DetectorWakeWord:
    def __init__(self, termos: tuple[str, ...] = WAKE_PADRAO) -> None:
        self.termos = tuple(t.lower() for t in termos)
        log.info("wake_word_stub_ativo", termos=list(self.termos))

    def avaliar(self, texto: str) -> ResultadoWake:
        bruto = (texto or "").strip()
        if not bruto:
            return ResultadoWake(detectado=False)
        baixo = bruto.lower()
        for termo in self.termos:
            if baixo.startswith(termo):
                residual = bruto[len(termo) :].lstrip(" ,.-:;")
                return ResultadoWake(detectado=True, termo=termo, residual=residual)
            if termo in baixo:
                idx = baixo.index(termo)
                residual = (bruto[:idx] + bruto[idx + len(termo) :]).strip(" ,.-:;")
                return ResultadoWake(detectado=True, termo=termo, residual=residual)
        return ResultadoWake(detectado=False, residual=bruto)
