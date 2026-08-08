from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nucleo.comum.config import get_configs, get_settings


@dataclass
class DecisaoPolitica:
    permitido: bool
    motivo: str
    risco: str = "baixo"
    exige_confirmacao: bool = False
    detalhes: dict[str, Any] = field(default_factory=dict)


class MotorPoliticas:
    def __init__(self) -> None:
        cfgs = get_configs()
        self.permissoes = cfgs["permissoes"]
        self.politicas = cfgs["politicas"]
        self._cloud_sessao_ativa = False
        self._confirmacoes: set[str] = set()

    def habilitar_cloud(self, minutos: int, confirmado: bool) -> DecisaoPolitica:
        if not confirmado:
            return DecisaoPolitica(False, "Confirmação humana obrigatória para cloud LLM", "alto", True)
        max_m = int(self.politicas["cloud_llm"]["escopo_maximo_minutos"])
        if minutos > max_m:
            return DecisaoPolitica(False, f"Escopo máximo é {max_m} minutos", "alto", True)
        self._cloud_sessao_ativa = True
        get_settings().cloud_llm_habilitada = True
        return DecisaoPolitica(True, "Cloud LLM habilitada temporariamente", "alto", False, {"minutos": minutos})

    def desabilitar_cloud(self) -> DecisaoPolitica:
        self._cloud_sessao_ativa = False
        get_settings().cloud_llm_habilitada = False
        return DecisaoPolitica(True, "Cloud LLM desabilitada", "baixo")

    def cloud_ativa(self) -> bool:
        return bool(get_settings().cloud_llm_habilitada or self._cloud_sessao_ativa)

    def registrar_confirmacao(self, acao_id: str) -> None:
        self._confirmacoes.add(acao_id)

    def avaliar(self, acao_id: str, plataforma: str = "hub", confirmado: bool = False) -> DecisaoPolitica:
        for proibido in self.permissoes.get("nao_pode", []):
            if proibido["id"] == acao_id:
                return DecisaoPolitica(False, proibido.get("motivo", "Proibido"), "critico")

        permitido_item = None
        for item in self.permissoes.get("pode", []):
            if item["id"] == acao_id:
                permitido_item = item
                break

        if not permitido_item:
            return DecisaoPolitica(False, f"Ação não listada: {acao_id}", "alto", True)

        if plataforma not in permitido_item.get("plataformas", []):
            return DecisaoPolitica(False, f"Ação {acao_id} indisponível em {plataforma}", "alto")

        risco = permitido_item.get("risco", "baixo")
        exige = bool(permitido_item.get("confirmacao_humana"))
        if permitido_item.get("exige_flag") == "cloud_llm_habilitada" and not self.cloud_ativa():
            return DecisaoPolitica(False, "Cloud LLM desligada — habilite com autorização", "alto", True)

        if exige and not (confirmado or acao_id in self._confirmacoes):
            return DecisaoPolitica(False, "Confirmação do desenvolvedor necessária", risco, True)

        return DecisaoPolitica(True, "Permitido", risco, False)

    def caminho_permitido(self, caminho: str) -> bool:
        allow = self.permissoes.get("allowlist_caminhos_windows", [])
        caminho_n = caminho.replace("/", "\\")
        return any(caminho_n.lower().startswith(a.lower()) for a in allow)

    def shell_permitido(self, comando: str) -> bool:
        return comando.strip() in set(self.permissoes.get("allowlist_shell", []))
