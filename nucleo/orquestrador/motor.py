from __future__ import annotations

from typing import Any

from nucleo.comum.logging import get_logger
from sub_agentes.agenda.agente import AgenteAgenda
from sub_agentes.atualizacao.agente import AgenteAtualizacao
from sub_agentes.base import ContextoAgente
from sub_agentes.codigo.agente import AgenteCodigo
from sub_agentes.conhecimento.agente import AgenteConhecimento
from sub_agentes.pesquisa.agente import AgentePesquisa
from sub_agentes.seguranca.agente import AgenteSeguranca
from sub_agentes.sistema.agente import AgenteSistema
from sub_agentes.treino.agente import AgenteTreino
from sub_agentes.voz_turno.agente import AgenteVozTurno

log = get_logger("orquestrador")


class OrquestradorOmega:
    def __init__(self, deps: dict[str, Any]) -> None:
        self.deps = deps
        self.seguranca = AgenteSeguranca()
        self.agentes = [
            AgenteAtualizacao(),
            AgenteTreino(),
            AgenteAgenda(),
            AgenteConhecimento(),
            AgenteSistema(),
            AgentePesquisa(),
            AgenteCodigo(),
            AgenteVozTurno(),
        ]

    async def processar(
        self,
        texto: str,
        conversa_id: str | None = None,
        plataforma: str = "hub",
        confirmado: bool = False,
        metadados: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        memoria = self.deps["memoria"]
        llm = self.deps["llm"]
        aperf = self.deps["aperfeicoamento"]
        voz = self.deps["voz"]

        if not conversa_id:
            conv = await memoria.criar_conversa()
            conversa_id = conv.id

        await memoria.adicionar_mensagem(conversa_id, "usuario", texto, metadados)

        ctx = ContextoAgente(
            texto=texto,
            conversa_id=conversa_id,
            plataforma=plataforma,
            confirmado=confirmado,
            metadados=metadados or {},
        )

        # Segurança sempre primeiro para ação conversacional base
        ctx.metadados.setdefault("acao", "conversar_texto")
        seg = await self.seguranca.executar(ctx, self.deps)
        if not seg.ok and ctx.metadados.get("acao") != "conversar_texto":
            return {
                "conversa_id": conversa_id,
                "resposta": seg.saida,
                "bloqueado": True,
                "agentes": [seg.__dict__],
                "animacao": voz.estado_animacao("alerta"),
            }

        usados = [seg]
        resposta_partes: list[str] = []
        dados_extra: dict[str, Any] = {}

        for agente in self.agentes:
            if agente.pode_tratar(ctx):
                # revalida segurança se agente de efeito colateral
                if agente.nome in {"sistema", "treino", "atualizacao", "agenda"}:
                    ctx.metadados["acao"] = {
                        "sistema": "ler_arquivo_allowlist",
                        "treino": "treinar_lora",
                        "atualizacao": "aplicar_update",
                        "agenda": "agenda_escrever",
                    }.get(agente.nome, "conversar_texto")
                    seg2 = await self.seguranca.executar(ctx, self.deps)
                    usados.append(seg2)
                    if not seg2.ok and agente.nome != "agenda":
                        # agenda pode só listar; deixa o agente decidir
                        if "liste" not in texto.lower() and "mostrar" not in texto.lower():
                            resposta_partes.append(seg2.saida)
                            dados_extra["exige_confirmacao"] = seg2.dados.get("exige_confirmacao")
                            continue
                res = await agente.executar(ctx, self.deps)
                usados.append(res)
                if res.saida:
                    resposta_partes.append(res.saida)
                dados_extra.update(res.dados)
                # voz_turno só ecoa se marcado
                if agente.nome != "voz_turno" and agente.nome in {
                    "atualizacao",
                    "treino",
                    "agenda",
                    "conhecimento",
                    "sistema",
                    "pesquisa",
                    "codigo",
                }:
                    # se já houve resposta especializada forte, ainda pode complementar com LLM curto
                    pass

        if not resposta_partes or all(a.agente in {"seguranca", "voz_turno"} for a in usados if hasattr(a, "agente")):
            # RAG curto + LLM
            hits = await memoria.buscar_conhecimento(texto, limite=3)
            contexto_rag = "\n".join(h["texto"] for h in hits)
            sistema = aperf.prompt_sistema()
            if contexto_rag:
                sistema += f"\n\nConhecimento relevante:\n{contexto_rag}"
            llm_resp = await llm.gerar(texto, sistema=sistema)
            resposta_partes.append(llm_resp.texto)
            dados_extra["llm"] = {"provedor": llm_resp.provedor, "modelo": llm_resp.modelo}

        resposta = "\n\n".join(dict.fromkeys(resposta_partes))  # dedup preservando ordem
        await memoria.adicionar_mensagem(conversa_id, "omega", resposta, {"agentes": [u.agente for u in usados]})

        anim = voz.estado_animacao("falando" if resposta else "idle")
        tts = None
        if (metadados or {}).get("modo") == "voz":
            tts_res = voz.sintetizar(resposta)
            tts = tts_res.__dict__

        log.info("turno_ok", conversa_id=conversa_id, agentes=[u.agente for u in usados])
        return {
            "conversa_id": conversa_id,
            "resposta": resposta,
            "agentes": [
                {"agente": u.agente, "ok": u.ok, "saida": u.saida, "dados": u.dados} for u in usados
            ],
            "animacao": anim,
            "tts": tts,
            "extras": dados_extra,
        }
