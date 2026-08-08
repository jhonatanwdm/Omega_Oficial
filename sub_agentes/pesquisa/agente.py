from __future__ import annotations

from pathlib import Path
from typing import Any

from sub_agentes.base import ContextoAgente, ResultadoAgente, SubAgente


class AgentePesquisa(SubAgente):
    nome = "pesquisa"

    def pode_tratar(self, ctx: ContextoAgente) -> bool:
        t = ctx.texto.lower()
        return any(k in t for k in ["pesquise", "procure", "busque no projeto", "onde está"])

    async def executar(self, ctx: ContextoAgente, deps: dict[str, Any]) -> ResultadoAgente:
        # Pesquisa local no monorepo (web só quando política permitir — fase segura)
        raiz = Path(__file__).resolve().parents[2]
        termo = ctx.texto
        for prefix in ["pesquise", "procure", "busque no projeto", "onde está"]:
            if termo.lower().startswith(prefix):
                termo = termo[len(prefix) :].strip(" :")
                break
        termo = termo.strip() or ctx.texto
        hits = []
        for path in raiz.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".yaml", ".md", ".dart", ".json"}:
                if "venv" in path.parts or ".git" in path.parts:
                    continue
                try:
                    txt = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                if termo.lower() in txt.lower() or termo.lower() in str(path).lower():
                    hits.append(str(path.relative_to(raiz)))
                if len(hits) >= 15:
                    break
        if not hits:
            return ResultadoAgente(self.nome, True, f"Nada encontrado para '{termo}'.", {})
        return ResultadoAgente(self.nome, True, "Encontrado:\n- " + "\n- ".join(hits), {"hits": hits})
