from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TextIO

import structlog


def _caminho_log() -> Path:
    return Path("dados") / "omega.log"


class _Tee:
    def __init__(self, *streams: TextIO) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)
            try:
                stream.flush()
            except Exception:
                pass
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            try:
                stream.flush()
            except Exception:
                pass


def configurar_logs() -> None:
    caminho = _caminho_log()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    arquivo = open(caminho, "a", encoding="utf-8", buffering=1)
    frozen = bool(getattr(sys, "frozen", False))

    if frozen:
        sys.stdout = arquivo
        sys.stderr = arquivo
        destino: TextIO | _Tee = arquivo
    else:
        destino = _Tee(sys.stdout, arquivo) if sys.stdout is not None else arquivo

    logging.basicConfig(format="%(message)s", stream=destino, level=logging.INFO, force=True)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=destino),
        cache_logger_on_first_use=True,
    )


def get_logger(nome: str = "omega"):
    return structlog.get_logger(nome)
