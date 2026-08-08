from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from nucleo.backups.servico_backups import ServicoBackups
from nucleo.comum.config import caminhos_projeto
from nucleo.comum.logging import get_logger

log = get_logger("aperfeicoamento")


class ServicoAperfeicoamento:
    """Autoaperfeiçoamento sandboxed: propõe, avalia, só aplica com backup + aprovação."""

    def __init__(self, backups: ServicoBackups) -> None:
        self.backups = backups
        self.dir = caminhos_projeto() / "dados" / "aperfeicoamento"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.prompts = self.dir / "prompts_sandbox.json"
        if not self.prompts.exists():
            self.prompts.write_text(
                json.dumps(
                    {
                        "sistema_ativo": "Você é o Omega, assistente pessoal em português brasileiro.",
                        "propostas": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

    def _load(self) -> dict[str, Any]:
        return json.loads(self.prompts.read_text(encoding="utf-8"))

    def _save(self, data: dict[str, Any]) -> None:
        self.prompts.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def propor_ajuste_prompt(self, motivo: str, novo_sistema: str) -> dict[str, Any]:
        data = self._load()
        prop = {
            "id": f"prop_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            "motivo": motivo,
            "novo_sistema": novo_sistema,
            "status": "proposta",
            "em_utc": datetime.now(timezone.utc).isoformat(),
        }
        data["propostas"].append(prop)
        self._save(data)
        return prop

    async def aplicar_proposta(self, proposta_id: str, confirmado: bool = False) -> dict[str, Any]:
        if not confirmado:
            return {"ok": False, "erro": "Aprovação humana obrigatória", "exige_confirmacao": True}
        data = self._load()
        prop = next((p for p in data["propostas"] if p["id"] == proposta_id), None)
        if not prop:
            return {"ok": False, "erro": "Proposta não encontrada"}
        backup = await self.backups.criar(rotulo=f"pre_aperf_{proposta_id}", ouro=False)
        data["sistema_ativo"] = prop["novo_sistema"]
        prop["status"] = "aplicada"
        prop["backup_id"] = backup["id"]
        self._save(data)
        log.info("aperfeicoamento_aplicado", id=proposta_id)
        return {"ok": True, "proposta": prop, "backup": backup}

    def prompt_sistema(self) -> str:
        return self._load().get("sistema_ativo", "Você é o Omega.")
