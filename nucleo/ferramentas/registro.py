from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Awaitable

from nucleo.comum.logging import get_logger
from nucleo.politicas.motor_politicas import MotorPoliticas

log = get_logger("ferramentas")


@dataclass
class Ferramenta:
    id: str
    risco: str
    plataformas: list[str]
    exige_confirmacao: bool
    executar: Callable[..., Awaitable[dict[str, Any]]]


class RegistroFerramentas:
    def __init__(self, politicas: MotorPoliticas) -> None:
        self.politicas = politicas
        self._tools: dict[str, Ferramenta] = {}
        self._registrar_padrao()

    def _registrar_padrao(self) -> None:
        self._tools["ler_arquivo_allowlist"] = Ferramenta(
            id="ler_arquivo_allowlist",
            risco="medio",
            plataformas=["desktop", "hub"],
            exige_confirmacao=False,
            executar=self._ler_arquivo,
        )
        self._tools["escrever_arquivo_allowlist"] = Ferramenta(
            id="escrever_arquivo_allowlist",
            risco="alto",
            plataformas=["desktop", "hub"],
            exige_confirmacao=True,
            executar=self._escrever_arquivo,
        )
        self._tools["shell_allowlist"] = Ferramenta(
            id="shell_allowlist",
            risco="critico",
            plataformas=["hub"],
            exige_confirmacao=True,
            executar=self._shell,
        )
        self._tools["notificacao_android"] = Ferramenta(
            id="notificacao_android",
            risco="baixo",
            plataformas=["android"],
            exige_confirmacao=False,
            executar=self._notif_android,
        )

    def listar(self) -> list[dict[str, Any]]:
        return [
            {
                "id": t.id,
                "risco": t.risco,
                "plataformas": t.plataformas,
                "exige_confirmacao": t.exige_confirmacao,
            }
            for t in self._tools.values()
        ]

    async def executar(
        self,
        ferramenta_id: str,
        plataforma: str = "hub",
        confirmado: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        tool = self._tools.get(ferramenta_id)
        if not tool:
            return {"ok": False, "erro": "Ferramenta inexistente"}
        if plataforma not in tool.plataformas:
            return {"ok": False, "erro": f"Indisponível em {plataforma}"}
        dec = self.politicas.avaliar(ferramenta_id, plataforma=plataforma, confirmado=confirmado)
        if not dec.permitido:
            return {"ok": False, "erro": dec.motivo, "exige_confirmacao": dec.exige_confirmacao}
        return await tool.executar(**kwargs)

    async def _ler_arquivo(self, caminho: str, **_: Any) -> dict[str, Any]:
        if not self.politicas.caminho_permitido(caminho):
            return {"ok": False, "erro": "Caminho fora da allowlist"}
        p = Path(caminho)
        if not p.is_file():
            return {"ok": False, "erro": "Arquivo não encontrado"}
        texto = p.read_text(encoding="utf-8", errors="replace")
        return {"ok": True, "conteudo": texto[:50000], "bytes": p.stat().st_size}

    async def _escrever_arquivo(self, caminho: str, conteudo: str, **_: Any) -> dict[str, Any]:
        if not self.politicas.caminho_permitido(caminho):
            return {"ok": False, "erro": "Caminho fora da allowlist"}
        p = Path(caminho)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(conteudo, encoding="utf-8")
        return {"ok": True, "caminho": str(p)}

    async def _shell(self, comando: str, **_: Any) -> dict[str, Any]:
        import asyncio

        if not self.politicas.shell_permitido(comando):
            return {"ok": False, "erro": "Comando fora da allowlist"}
        proc = await asyncio.create_subprocess_shell(
            comando,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path(__file__).resolve().parents[2]),
        )
        out, err = await proc.communicate()
        return {
            "ok": proc.returncode == 0,
            "codigo": proc.returncode,
            "stdout": out.decode("utf-8", errors="replace")[-8000:],
            "stderr": err.decode("utf-8", errors="replace")[-4000:],
        }

    async def _notif_android(self, titulo: str, corpo: str, **_: Any) -> dict[str, Any]:
        # Bridge: o cliente Flutter consome este evento via sync/push local
        return {
            "ok": True,
            "evento": "notificacao_android",
            "titulo": titulo,
            "corpo": corpo,
            "nota": "Cliente Android deve apresentar a notificação localmente",
        }
