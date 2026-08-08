"""Entrada do executável Omega Hub (PyInstaller)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def _garantir_estrutura() -> Path:
    if getattr(sys, "frozen", False):
        raiz = Path(sys.executable).resolve().parent
        meipass = Path(getattr(sys, "_MEIPASS", raiz))
    else:
        raiz = Path(__file__).resolve().parents[1]
        meipass = raiz

    for pasta in ("configs", "dados", "dados/conhecimento", "dados/datasets_treino", "dados/backups"):
        (raiz / pasta).mkdir(parents=True, exist_ok=True)

    origem_cfg = meipass / "configs"
    destino_cfg = raiz / "configs"
    if origem_cfg.exists():
        for arq in origem_cfg.glob("*.yaml"):
            alvo = destino_cfg / arq.name
            if not alvo.exists():
                shutil.copy2(arq, alvo)

    versao_origem = meipass / "dados" / "versao.json"
    versao_destino = raiz / "dados" / "versao.json"
    if versao_origem.exists() and not versao_destino.exists():
        shutil.copy2(versao_origem, versao_destino)

    return raiz


def main() -> None:
    raiz = _garantir_estrutura()
    import os

    os.chdir(raiz)
    # Garante imports do monorepo quando rodando fora do bundle
    if str(raiz) not in sys.path:
        sys.path.insert(0, str(raiz))

    print("=" * 50)
    print("  Omega Hub")
    print("  http://127.0.0.1:8741")
    print("  Token: omega-dev-local")
    print(f"  Dados: {raiz / 'dados'}")
    print("=" * 50)
    print("Pressione Ctrl+C para encerrar.\n")

    from nucleo.api.principal import main as iniciar_hub

    iniciar_hub()


if __name__ == "__main__":
    main()
