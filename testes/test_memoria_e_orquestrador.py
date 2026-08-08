import pytest

from nucleo.aperfeicoamento.servico_aperfeicoamento import ServicoAperfeicoamento
from nucleo.atualizacoes.servico_atualizacoes import ServicoAtualizacoes
from nucleo.backups.servico_backups import ServicoBackups
from nucleo.ferramentas.registro import RegistroFerramentas
from nucleo.llm.roteador_llm import RoteadorLLM
from nucleo.memoria.servico_memoria import ServicoMemoria
from nucleo.orquestrador.motor import OrquestradorOmega
from nucleo.politicas.motor_politicas import MotorPoliticas
from nucleo.tempo.servico_tempo import ServicoTempo
from nucleo.treino.servico_treino import ServicoTreino
from nucleo.voz.pipeline_voz import PipelineVoz


@pytest.fixture
async def deps(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # aponta dados relativos ao projeto real via módulos já importados
    memoria = ServicoMemoria()
    # força sqlite no tmp
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from sqlmodel.ext.asyncio.session import AsyncSession
    from nucleo.memoria.modelos import SQLModel

    url = f"sqlite+aiosqlite:///{tmp_path/'t.db'}"
    memoria.engine = create_async_engine(url)
    memoria.session_factory = async_sessionmaker(memoria.engine, class_=AsyncSession, expire_on_commit=False)
    await memoria.inicializar()
    politicas = MotorPoliticas()
    llm = RoteadorLLM(politicas)
    voz = PipelineVoz()
    ferramentas = RegistroFerramentas(politicas)
    backups = ServicoBackups(memoria)
    atualizacoes = ServicoAtualizacoes(backups)
    treino = ServicoTreino()
    aperf = ServicoAperfeicoamento(backups)
    tempo = ServicoTempo()
    orch = OrquestradorOmega(
        {
            "memoria": memoria,
            "politicas": politicas,
            "llm": llm,
            "voz": voz,
            "ferramentas": ferramentas,
            "backups": backups,
            "atualizacoes": atualizacoes,
            "treino": treino,
            "aperfeicoamento": aperf,
            "tempo": tempo,
        }
    )
    return {
        "memoria": memoria,
        "orch": orch,
        "backups": backups,
        "treino": treino,
        "aperf": aperf,
        "atualizacoes": atualizacoes,
        "voz": voz,
    }


@pytest.mark.asyncio
async def test_chat_e_memoria(deps):
    r = await deps["orch"].processar("Olá Omega, tudo bem?")
    assert r["resposta"]
    assert r["conversa_id"]
    msgs = await deps["memoria"].listar_mensagens(r["conversa_id"])
    assert len(msgs) >= 2


@pytest.mark.asyncio
async def test_conhecimento(deps):
    await deps["memoria"].gravar_conhecimento("Preferência", "Gosto de café sem açúcar")
    hits = await deps["memoria"].buscar_conhecimento("café")
    assert hits


@pytest.mark.asyncio
async def test_backup_e_update(deps):
    b = await deps["backups"].criar("teste")
    assert b["id"]
    up = await deps["atualizacoes"].aplicar("0.1.1", "patch", confirmado=True)
    assert up["ok"] is True


@pytest.mark.asyncio
async def test_treino_sandbox(deps):
    t = deps["treino"]
    t.coletar_exemplo("oi", "olá")
    t.coletar_exemplo("tudo bem", "tudo ótimo")
    t.coletar_exemplo("nome", "sou o Omega")
    r = await t.treinar_lora_sandbox(confirmado=True)
    assert r["ok"] is True


@pytest.mark.asyncio
async def test_tts_fallback(deps):
    r = deps["voz"].sintetizar("Olá")
    assert r.audio_b64
    assert r.mime == "audio/wav"
