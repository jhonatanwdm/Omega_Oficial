from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nucleo.comum.config import caminhos_projeto
from nucleo.comum.logging import get_logger

log = get_logger("treino")


class ServicoTreino:
    """Pipeline dataset → LoRA (sandbox) → avaliação. Aplicação exige aprovação."""

    def __init__(self) -> None:
        self.raiz = caminhos_projeto() / "dados" / "datasets_treino"
        self.raiz.mkdir(parents=True, exist_ok=True)
        self.propostas = caminhos_projeto() / "dados" / "propostas_lora"
        self.propostas.mkdir(parents=True, exist_ok=True)

    def coletar_exemplo(self, entrada: str, saida_desejada: str, tags: str = "") -> dict[str, Any]:
        item = {
            "entrada": entrada,
            "saida": saida_desejada,
            "tags": tags,
            "em_utc": datetime.now(timezone.utc).isoformat(),
        }
        arq = self.raiz / "dataset.jsonl"
        with arq.open("a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        return item

    def listar_dataset(self, limite: int = 100) -> list[dict[str, Any]]:
        arq = self.raiz / "dataset.jsonl"
        if not arq.exists():
            return []
        linhas = arq.read_text(encoding="utf-8").splitlines()[-limite:]
        return [json.loads(l) for l in linhas if l.strip()]

    async def treinar_lora_sandbox(self, nome: str = "omega-lora", confirmado: bool = False) -> dict[str, Any]:
        if not confirmado:
            return {"ok": False, "erro": "Confirmação do desenvolvedor necessária", "exige_confirmacao": True}
        exemplos = self.listar_dataset()
        if len(exemplos) < 3:
            return {"ok": False, "erro": "Dataset insuficiente (mínimo 3 exemplos)"}

        # Sandbox: gera adapter stub avaliável sem GPU obrigatória
        proposta_id = f"{nome}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        pasta = self.propostas / proposta_id
        pasta.mkdir(parents=True, exist_ok=True)
        metricas = self._avaliar(exemplos)
        meta = {
            "id": proposta_id,
            "status": "sandbox_avaliado",
            "aprovado": metricas["score"] >= 0.5,
            "metricas": metricas,
            "exemplos": len(exemplos),
            "nota": "Adapter LoRA real (PEFT) pode ser plugado aqui com GPU NVIDIA",
        }
        (pasta / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        (pasta / "adapter_stub.json").write_text(
            json.dumps({"tipo": "lora_stub", "base": "qwen2.5", "rank": 8}, indent=2),
            encoding="utf-8",
        )
        log.info("treino_sandbox", id=proposta_id, score=metricas["score"])
        return {"ok": True, **meta}

    def _avaliar(self, exemplos: list[dict[str, Any]]) -> dict[str, Any]:
        # Heurística: cobertura média de tokens da saída nos pares
        scores = []
        for ex in exemplos:
            alvo = set(ex["saida"].lower().split())
            ent = set(ex["entrada"].lower().split())
            if not alvo:
                scores.append(0.0)
                continue
            scores.append(len(alvo & ent) / max(len(alvo), 1) + 0.4)
        score = sum(scores) / len(scores) if scores else 0.0
        return {"score": min(score, 1.0), "n": len(exemplos)}

    def listar_propostas(self) -> list[dict[str, Any]]:
        out = []
        for p in sorted(self.propostas.glob("*/meta.json")):
            out.append(json.loads(p.read_text(encoding="utf-8")))
        return out
