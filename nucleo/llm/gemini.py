"""Conector Gemini (cloud), gated pelas mesmas políticas dos demais LLMs cloud."""

from __future__ import annotations

from typing import Any

import httpx

from nucleo.comum.config import get_configs, get_settings
from nucleo.comum.logging import get_logger

log = get_logger("llm.gemini")


async def gerar_gemini(prompt: str, sistema: str | None = None) -> dict[str, Any] | None:
    """Chamada HTTP ao Generative Language API. Retorna None se indisponível."""
    settings = get_settings()
    chave = settings.gemini_api_key
    if not chave:
        log.info("gemini_sem_chave")
        return None

    provedores = get_configs()["provedores"]
    modelo = provedores.get("llm_cloud", {}).get("gemini", {}).get("modelo_padrao", "gemini-2.0-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    partes = []
    if sistema:
        partes.append({"text": f"[sistema]\n{sistema}"})
    partes.append({"text": prompt})
    payload = {"contents": [{"role": "user", "parts": partes}]}

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, params={"key": chave}, json=payload)
            if r.status_code != 200:
                log.info("gemini_http", status=r.status_code)
                return None
            data = r.json()
            candidatos = data.get("candidates") or []
            texto = ""
            if candidatos:
                parts = candidatos[0].get("content", {}).get("parts") or []
                texto = "".join(p.get("text", "") for p in parts).strip()
            if not texto:
                return None
            return {"texto": texto, "provedor": "gemini", "modelo": modelo}
    except Exception as e:
        log.info("gemini_falhou", detalhe=str(e))
        return None
