from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from nucleo.comum.config import get_configs, get_settings
from nucleo.comum.logging import get_logger
from nucleo.politicas.motor_politicas import MotorPoliticas

log = get_logger("llm")


@dataclass
class RespostaLLM:
    texto: str
    provedor: str
    modelo: str
    usado_cloud: bool = False


class RoteadorLLM:
    def __init__(self, politicas: MotorPoliticas) -> None:
        self.politicas = politicas
        self.provedores = get_configs()["provedores"]
        self.settings = get_settings()

    async def gerar(
        self,
        prompt: str,
        sistema: str | None = None,
        forcar_cloud: bool = False,
        confirmado_cloud: bool = False,
    ) -> RespostaLLM:
        if forcar_cloud:
            dec = self.politicas.avaliar("usar_llm_cloud", confirmado=confirmado_cloud)
            if not dec.permitido:
                return RespostaLLM(
                    texto=f"[Política] Cloud bloqueada: {dec.motivo}. Usando local.",
                    provedor="politica",
                    modelo="bloqueio",
                )
            cloud = await self._cloud(prompt, sistema)
            if cloud:
                return cloud

        local = await self._ollama(prompt, sistema)
        if local:
            return local

        return self._mock(prompt, sistema)

    async def _ollama(self, prompt: str, sistema: str | None) -> RespostaLLM | None:
        base = self.settings.ollama_base_url
        modelo = self.settings.ollama_modelo
        mensagens = []
        if sistema:
            mensagens.append({"role": "system", "content": sistema})
        mensagens.append({"role": "user", "content": prompt})
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                r = await client.post(
                    f"{base}/api/chat",
                    json={"model": modelo, "messages": mensagens, "stream": False},
                )
                if r.status_code != 200:
                    return None
                data = r.json()
                texto = data.get("message", {}).get("content") or data.get("response", "")
                return RespostaLLM(texto=texto.strip(), provedor="ollama", modelo=modelo)
        except Exception as e:
            log.info("ollama_indisponivel", erro=str(e))
            return None

    async def _cloud(self, prompt: str, sistema: str | None) -> RespostaLLM | None:
        if self.settings.openai_api_key:
            try:
                from openai import AsyncOpenAI

                client = AsyncOpenAI(api_key=self.settings.openai_api_key)
                modelo = self.provedores["llm_cloud"]["openai"]["modelo_padrao"]
                msgs: list[dict[str, Any]] = []
                if sistema:
                    msgs.append({"role": "system", "content": sistema})
                msgs.append({"role": "user", "content": prompt})
                resp = await client.chat.completions.create(model=modelo, messages=msgs)
                return RespostaLLM(
                    texto=resp.choices[0].message.content or "",
                    provedor="openai",
                    modelo=modelo,
                    usado_cloud=True,
                )
            except Exception as e:
                log.info("openai_falhou", erro=str(e))

        if self.settings.anthropic_api_key:
            try:
                from anthropic import AsyncAnthropic

                client = AsyncAnthropic(api_key=self.settings.anthropic_api_key)
                modelo = self.provedores["llm_cloud"]["anthropic"]["modelo_padrao"]
                resp = await client.messages.create(
                    model=modelo,
                    max_tokens=1024,
                    system=sistema or "Você é o Omega, assistente em pt-BR.",
                    messages=[{"role": "user", "content": prompt}],
                )
                texto = "".join(getattr(b, "text", "") for b in resp.content)
                return RespostaLLM(texto=texto, provedor="anthropic", modelo=modelo, usado_cloud=True)
            except Exception as e:
                log.info("anthropic_falhou", erro=str(e))
        return None

    def _mock(self, prompt: str, sistema: str | None) -> RespostaLLM:
        base = (
            "Sou o Omega (modo local sem Ollama). "
            "Recebi sua mensagem e estou operando com o núcleo híbrido em fallback. "
            f"Resumo do pedido: {prompt[:280]}"
        )
        return RespostaLLM(texto=base, provedor="mock", modelo="omega-fallback")
