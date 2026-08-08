from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nucleo import __version__
from nucleo.backups.servico_backups import ServicoBackups
from nucleo.comum.config import caminhos_projeto
from nucleo.comum.logging import get_logger

log = get_logger("atualizacoes")


class ServicoAtualizacoes:
    def __init__(self, backups: ServicoBackups) -> None:
        self.backups = backups
        self.arquivo = caminhos_projeto() / "dados" / "versao.json"
        if not self.arquivo.exists():
            self._salvar(
                {
                    "versao": __version__,
                    "changelog": [{"versao": __version__, "notas": "Fundação Omega", "em": datetime.now(timezone.utc).isoformat()}],
                }
            )

    def _salvar(self, data: dict[str, Any]) -> None:
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        self.arquivo.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def estado(self) -> dict[str, Any]:
        return json.loads(self.arquivo.read_text(encoding="utf-8"))

    async def aplicar(self, nova_versao: str, notas: str, confirmado: bool = False) -> dict[str, Any]:
        if not confirmado:
            return {"ok": False, "erro": "Confirmação obrigatória", "exige_confirmacao": True}
        backup = await self.backups.criar(rotulo=f"pre_update_{nova_versao}", ouro=False)
        data = self.estado()
        data["versao"] = nova_versao
        data["changelog"].insert(
            0,
            {
                "versao": nova_versao,
                "notas": notas,
                "em": datetime.now(timezone.utc).isoformat(),
                "backup_id": backup["id"],
            },
        )
        self._salvar(data)
        log.info("update_aplicado", versao=nova_versao, backup=backup["id"])
        return {"ok": True, "versao": nova_versao, "backup": backup}
