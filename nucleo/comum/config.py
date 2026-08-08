from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _raiz_empacotada() -> Path | None:
    """Diretório do .exe quando rodando via PyInstaller."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return None


def caminhos_projeto() -> Path:
    empacotado = _raiz_empacotada()
    if empacotado is not None:
        return empacotado
    return Path(__file__).resolve().parents[2]


def recurso_interno(*partes: str) -> Path:
    """Arquivos embutidos no bundle (_MEIPASS) ou no projeto fonte."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS, *partes)  # type: ignore[attr-defined]
    return caminhos_projeto().joinpath(*partes)


def carregar_yaml(nome: str) -> dict[str, Any]:
    caminho = caminhos_projeto() / "configs" / nome
    with caminho.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class ConfigOmega(BaseSettings):
    omega_token_dev: str = "omega-dev-local"
    omega_database_url: str = ""
    omega_redis_url: str = "redis://127.0.0.1:6379/0"
    omega_qdrant_url: str = "http://127.0.0.1:6333"
    omega_host: str = "0.0.0.0"
    omega_porta: int = 8741
    cloud_llm_habilitada: bool = False
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_modelo: str = "qwen2.5:7b"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class EstadoRuntime(BaseModel):
    cloud_llm_habilitada: bool = False
    cloud_escopo_ate_utc: str | None = None
    versao: str = "0.1.0"
    flags: dict[str, Any] = Field(default_factory=dict)


@lru_cache
def get_settings() -> ConfigOmega:
    return ConfigOmega()


@lru_cache
def get_configs() -> dict[str, dict[str, Any]]:
    return {
        "permissoes": carregar_yaml("permissoes.yaml"),
        "politicas": carregar_yaml("politicas.yaml"),
        "diretrizes": carregar_yaml("diretrizes.yaml"),
        "padroes": carregar_yaml("padroes.yaml"),
        "provedores": carregar_yaml("provedores.yaml"),
    }
