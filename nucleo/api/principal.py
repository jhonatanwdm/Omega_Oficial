from __future__ import annotations

import base64
import os
import threading
import webbrowser
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from nucleo import __version__
from nucleo.aperfeicoamento.servico_aperfeicoamento import ServicoAperfeicoamento
from nucleo.api.esquemas import (
    AperfApplyPedido,
    AperfPropostaPedido,
    ChatPedido,
    CloudPedido,
    ConhecimentoPedido,
    FerramentaPedido,
    SyncPedido,
    TempoPedido,
    TreinoExemploPedido,
    UpdatePedido,
)
from nucleo.atualizacoes.servico_atualizacoes import ServicoAtualizacoes
from nucleo.backups.servico_backups import ServicoBackups
from nucleo.comum.auth import Autorizacao, exigir_dev
from nucleo.comum.config import get_configs, get_settings, recurso_interno
from nucleo.comum.logging import configurar_logs, get_logger
from nucleo.ferramentas.registro import RegistroFerramentas
from nucleo.llm.roteador_llm import RoteadorLLM
from nucleo.memoria.cache_redis import CacheOmega
from nucleo.memoria.servico_memoria import ServicoMemoria
from nucleo.orquestrador.motor import OrquestradorOmega
from nucleo.politicas.motor_politicas import MotorPoliticas
from nucleo.tempo.servico_tempo import ServicoTempo
from nucleo.treino.servico_treino import ServicoTreino
from nucleo.voz.pipeline_voz import PipelineVoz

configurar_logs()
log = get_logger("api")


class AppState:
    memoria: ServicoMemoria
    cache: CacheOmega
    politicas: MotorPoliticas
    llm: RoteadorLLM
    voz: PipelineVoz
    ferramentas: RegistroFerramentas
    backups: ServicoBackups
    atualizacoes: ServicoAtualizacoes
    treino: ServicoTreino
    aperfeicoamento: ServicoAperfeicoamento
    tempo: ServicoTempo
    orquestrador: OrquestradorOmega


state = AppState()


def _pasta_estatico() -> Path:
    return recurso_interno("nucleo", "api", "estatico")


def _abrir_ui_no_navegador(porta: int) -> None:
    url = f"http://127.0.0.1:{porta}/"

    def _abrir() -> None:
        try:
            webbrowser.open(url)
            log.info("ui_aberta_no_navegador", url=url)
        except Exception as e:
            log.info("ui_navegador_indisponivel", detalhe=str(e))

    threading.Timer(1.2, _abrir).start()


@asynccontextmanager
async def lifespan(_: FastAPI):
    state.memoria = ServicoMemoria()
    await state.memoria.inicializar()
    state.cache = CacheOmega()
    state.politicas = MotorPoliticas()
    state.llm = RoteadorLLM(state.politicas)
    state.voz = PipelineVoz()
    state.ferramentas = RegistroFerramentas(state.politicas)
    state.backups = ServicoBackups(state.memoria)
    state.atualizacoes = ServicoAtualizacoes(state.backups)
    state.treino = ServicoTreino()
    state.aperfeicoamento = ServicoAperfeicoamento(state.backups)
    state.tempo = ServicoTempo()
    state.orquestrador = OrquestradorOmega(
        {
            "memoria": state.memoria,
            "politicas": state.politicas,
            "llm": state.llm,
            "voz": state.voz,
            "ferramentas": state.ferramentas,
            "backups": state.backups,
            "atualizacoes": state.atualizacoes,
            "treino": state.treino,
            "aperfeicoamento": state.aperfeicoamento,
            "tempo": state.tempo,
        }
    )
    log.info("hub_omega_pronto", versao=__version__)
    settings = get_settings()
    em_teste = bool(os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("OMEGA_TESTE"))
    if settings.omega_abrir_ui and not em_teste:
        _abrir_ui_no_navegador(settings.omega_porta)
    yield


app = FastAPI(title="Omega Hub", version=__version__, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_estatico = _pasta_estatico()
if _estatico.is_dir():
    app.mount("/ui", StaticFiles(directory=str(_estatico)), name="ui")


@app.get("/")
async def ui_raiz() -> FileResponse:
    index = _pasta_estatico() / "index.html"
    if not index.is_file():
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="UI estática não encontrada")
    return FileResponse(index)



@app.get("/saude")
async def saude() -> dict[str, Any]:
    sync = state.tempo.sincronizado()
    return {
        "ok": True,
        "nome": "Omega",
        "versao": __version__,
        "versao_hub": state.atualizacoes.estado().get("versao"),
        "tempo": sync,
        "cloud_llm": state.politicas.cloud_ativa(),
    }


@app.get("/configs")
async def configs(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return get_configs()


@app.post("/chat")
async def chat(pedido: ChatPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.orquestrador.processar(
        texto=pedido.texto,
        conversa_id=pedido.conversa_id,
        plataforma=pedido.plataforma,
        confirmado=pedido.confirmado,
        metadados={"modo": pedido.modo},
    )


@app.get("/conversas/{conversa_id}/mensagens")
async def mensagens(conversa_id: str, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    msgs = await state.memoria.listar_mensagens(conversa_id)
    return {"itens": [m.model_dump(mode="json") for m in msgs]}


@app.post("/voz/stt")
async def voz_stt(arquivo: UploadFile = File(...), _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    data = await arquivo.read()
    r = state.voz.transcrever(data)
    return r.__dict__


@app.post("/voz/tts")
async def voz_tts(pedido: ChatPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    r = state.voz.sintetizar(pedido.texto)
    return r.__dict__


@app.websocket("/ws/voz")
async def ws_voz(ws: WebSocket) -> None:
    await ws.accept()
    token = ws.headers.get("x-omega-token") or ws.query_params.get("token")
    from nucleo.comum.auth import verificar_token_dev

    if not verificar_token_dev(token).valido:
        await ws.send_json({"ok": False, "erro": "não autorizado"})
        await ws.close()
        return
    try:
        while True:
            msg = await ws.receive_json()
            fase = msg.get("fase", "ouvindo")
            await ws.send_json({"animacao": state.voz.estado_animacao(fase)})
            if msg.get("audio_b64"):
                audio = base64.b64decode(msg["audio_b64"])
                stt = state.voz.transcrever(audio)
                resultado = await state.orquestrador.processar(
                    texto=stt.texto or msg.get("texto", ""),
                    conversa_id=msg.get("conversa_id"),
                    plataforma=msg.get("plataforma", "desktop"),
                    confirmado=bool(msg.get("confirmado")),
                    metadados={"modo": "voz"},
                )
                await ws.send_json({"ok": True, "stt": stt.__dict__, **resultado})
            elif msg.get("texto"):
                resultado = await state.orquestrador.processar(
                    texto=msg["texto"],
                    conversa_id=msg.get("conversa_id"),
                    plataforma=msg.get("plataforma", "desktop"),
                    confirmado=bool(msg.get("confirmado")),
                    metadados={"modo": "voz"},
                )
                await ws.send_json({"ok": True, **resultado})
    except WebSocketDisconnect:
        log.info("ws_voz_desconectado")


@app.post("/cloud/habilitar")
async def cloud_on(pedido: CloudPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    dec = state.politicas.habilitar_cloud(pedido.minutos, pedido.confirmado)
    return dec.__dict__


@app.post("/cloud/desabilitar")
async def cloud_off(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return state.politicas.desabilitar_cloud().__dict__


@app.get("/ferramentas")
async def listar_ferramentas(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return {"itens": state.ferramentas.listar()}


@app.post("/ferramentas/executar")
async def exec_ferramenta(pedido: FerramentaPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.ferramentas.executar(
        pedido.ferramenta_id,
        plataforma=pedido.plataforma,
        confirmado=pedido.confirmado,
        **pedido.args,
    )


@app.post("/conhecimento")
async def gravar_conhecimento(pedido: ConhecimentoPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    item = await state.memoria.gravar_conhecimento(
        pedido.titulo, pedido.conteudo, pedido.tags, pedido.critico
    )
    return item.model_dump(mode="json")


@app.get("/conhecimento/buscar")
async def buscar_conhecimento(q: str, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return {"itens": await state.memoria.buscar_conhecimento(q)}


@app.post("/treino/exemplo")
async def treino_exemplo(pedido: TreinoExemploPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return state.treino.coletar_exemplo(pedido.entrada, pedido.saida, pedido.tags)


@app.post("/treino/lora")
async def treino_lora(confirmado: bool = False, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.treino.treinar_lora_sandbox(confirmado=confirmado)


@app.get("/treino/propostas")
async def treino_propostas(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return {"itens": state.treino.listar_propostas()}


@app.post("/aperfeicoamento/propor")
async def aperf_propor(pedido: AperfPropostaPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return state.aperfeicoamento.propor_ajuste_prompt(pedido.motivo, pedido.novo_sistema)


@app.post("/aperfeicoamento/aplicar")
async def aperf_aplicar(pedido: AperfApplyPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.aperfeicoamento.aplicar_proposta(pedido.proposta_id, pedido.confirmado)


@app.post("/backups")
async def criar_backup(rotulo: str = "manual", ouro: bool = False, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.backups.criar(rotulo=rotulo, ouro=ouro)


@app.get("/backups")
async def listar_backups(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return {"itens": state.backups.listar()}


@app.post("/backups/{backup_id}/restaurar")
async def restaurar_backup(backup_id: str, confirmado: bool = False, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    if not confirmado:
        return {"ok": False, "erro": "Confirmação obrigatória", "exige_confirmacao": True}
    return await state.backups.restaurar(backup_id)


@app.get("/updates")
async def updates_estado(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return state.atualizacoes.estado()


@app.post("/updates")
async def updates_aplicar(pedido: UpdatePedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.atualizacoes.aplicar(pedido.versao, pedido.notas, pedido.confirmado)


@app.post("/sync/pull")
async def sync_pull(pedido: SyncPedido, _: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return await state.memoria.sync_pull(pedido.entidade, pedido.desde_versao)


@app.get("/tempo")
async def tempo_agora() -> dict[str, Any]:
    return state.tempo.sincronizado()


@app.post("/tempo/validar")
async def tempo_validar(pedido: TempoPedido) -> dict[str, Any]:
    cliente = None
    if pedido.relogio_cliente_utc:
        cliente = datetime.fromisoformat(pedido.relogio_cliente_utc.replace("Z", "+00:00"))
    inst = state.tempo.agora(cliente)
    return {
        "utc": inst.iso_utc,
        "local": inst.iso_local,
        "fuso": inst.fuso,
        "drift_segundos": inst.drift_segundos,
        "aviso_drift": inst.aviso_drift,
    }


@app.get("/permissoes")
async def permissoes(_: Autorizacao = Depends(exigir_dev)) -> dict[str, Any]:
    return get_configs()["permissoes"]


def main() -> None:
    import uvicorn

    settings = get_settings()
    # Passar o objeto app (necessário para PyInstaller; string import falha no .exe)
    uvicorn.run(
        app,
        host=settings.omega_host,
        port=settings.omega_porta,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
