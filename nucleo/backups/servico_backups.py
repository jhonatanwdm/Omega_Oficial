from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nucleo.comum.config import caminhos_projeto
from nucleo.comum.logging import get_logger
from nucleo.memoria.servico_memoria import ServicoMemoria

log = get_logger("backups")


class ServicoBackups:
    def __init__(self, memoria: ServicoMemoria) -> None:
        self.memoria = memoria
        self.raiz = caminhos_projeto() / "dados" / "backups"
        self.raiz.mkdir(parents=True, exist_ok=True)
        self.indice = self.raiz / "indice.json"
        if not self.indice.exists():
            self.indice.write_text("[]", encoding="utf-8")

    def _ler_indice(self) -> list[dict[str, Any]]:
        return json.loads(self.indice.read_text(encoding="utf-8") or "[]")

    def _salvar_indice(self, itens: list[dict[str, Any]]) -> None:
        self.indice.write_text(json.dumps(itens, ensure_ascii=False, indent=2), encoding="utf-8")

    async def criar(self, rotulo: str = "manual", ouro: bool = False) -> dict[str, Any]:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        pasta = self.raiz / f"{ts}_{rotulo}"
        pasta.mkdir(parents=True, exist_ok=True)
        await self.memoria.exportar_snapshot(pasta)
        cfg = caminhos_projeto() / "configs"
        shutil.copytree(cfg, pasta / "configs", dirs_exist_ok=True)
        meta = {
            "id": pasta.name,
            "rotulo": rotulo,
            "ouro": ouro,
            "criado_em_utc": datetime.now(timezone.utc).isoformat(),
            "caminho": str(pasta),
            "estavel": True,
        }
        itens = self._ler_indice()
        itens.append(meta)
        # retenção: últimos 10 estáveis + ouros
        estaveis = [i for i in itens if i.get("estavel") and not i.get("ouro")]
        ouros = [i for i in itens if i.get("ouro")]
        outros = [i for i in itens if not i.get("estavel")]
        estaveis = estaveis[-10:]
        self._salvar_indice(ouros + estaveis + outros)
        log.info("backup_criado", id=meta["id"])
        return meta

    def listar(self) -> list[dict[str, Any]]:
        return self._ler_indice()

    async def restaurar(self, backup_id: str) -> dict[str, Any]:
        itens = self._ler_indice()
        alvo = next((i for i in itens if i["id"] == backup_id), None)
        if not alvo:
            return {"ok": False, "erro": "Backup não encontrado"}
        pasta = Path(alvo["caminho"])
        cfg_src = pasta / "configs"
        if cfg_src.exists():
            shutil.copytree(cfg_src, caminhos_projeto() / "configs", dirs_exist_ok=True)
        mem = pasta / "memoria.json"
        restore_copy = caminhos_projeto() / "dados" / "conhecimento" / f"restore_{backup_id}.json"
        if mem.exists():
            shutil.copy2(mem, restore_copy)
        return {"ok": True, "backup_id": backup_id, "memoria_copiada_para": str(restore_copy)}
