from __future__ import annotations

import json
from typing import Any

from nucleo.comum.config import get_settings
from nucleo.comum.logging import get_logger

log = get_logger("redis")


class CacheOmega:
    """Redis com fallback em memória para filas/sessão/rate-limit."""

    def __init__(self) -> None:
        self._mem: dict[str, str] = {}
        self._redis = None
        try:
            import redis

            client = redis.Redis.from_url(get_settings().omega_redis_url, socket_connect_timeout=1)
            client.ping()
            self._redis = client
            log.info("redis_conectado")
        except Exception as e:
            log.info("redis_fallback_memoria", erro=str(e))

    def set_json(self, chave: str, valor: Any, ttl: int | None = 3600) -> None:
        raw = json.dumps(valor, ensure_ascii=False, default=str)
        if self._redis is not None:
            self._redis.set(chave, raw, ex=ttl)
        else:
            self._mem[chave] = raw

    def get_json(self, chave: str) -> Any | None:
        if self._redis is not None:
            raw = self._redis.get(chave)
            if raw is None:
                return None
            return json.loads(raw)
        raw = self._mem.get(chave)
        return json.loads(raw) if raw else None
