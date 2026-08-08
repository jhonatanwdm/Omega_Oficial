from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from nucleo.comum.config import caminhos_projeto, get_configs, get_settings
from nucleo.comum.logging import get_logger
from nucleo.memoria.modelos import (
    Auditoria,
    Conversa,
    CursorSync,
    EventoAgenda,
    ItemConhecimento,
    Mensagem,
    SQLModel,
)
from nucleo.memoria.vetor import ArmazemVetorialLocal

log = get_logger("memoria")


class ServicoMemoria:
    def __init__(self) -> None:
        settings = get_settings()
        provedores = get_configs()["provedores"]["banco"]
        url = settings.omega_database_url or provedores["sqlite_fallback"]
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        self.url = url
        self.engine = create_async_engine(url, echo=False)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        self.vetor = ArmazemVetorialLocal()
        self.dir_conhecimento = caminhos_projeto() / "dados" / "conhecimento"
        self.dir_conhecimento.mkdir(parents=True, exist_ok=True)

    async def inicializar(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        log.info("memoria_inicializada", url=self.url.split("://")[0])

    async def criar_conversa(self, titulo: str = "Conversa Omega") -> Conversa:
        conv = Conversa(titulo=titulo)
        async with self.session_factory() as session:
            session.add(conv)
            await session.commit()
            await session.refresh(conv)
        return conv

    async def adicionar_mensagem(
        self,
        conversa_id: str,
        papel: str,
        conteudo: str,
        metadados: dict[str, Any] | None = None,
    ) -> Mensagem:
        msg = Mensagem(
            conversa_id=conversa_id,
            papel=papel,
            conteudo=conteudo,
            metadados_json=json.dumps(metadados or {}, ensure_ascii=False),
        )
        async with self.session_factory() as session:
            session.add(msg)
            conv = await session.get(Conversa, conversa_id)
            if conv:
                conv.atualizado_em_utc = datetime.now(timezone.utc)
                conv.versao_sync += 1
            await session.commit()
            await session.refresh(msg)
        return msg

    async def listar_mensagens(self, conversa_id: str, limite: int = 50) -> list[Mensagem]:
        async with self.session_factory() as session:
            res = await session.exec(
                select(Mensagem)
                .where(Mensagem.conversa_id == conversa_id)
                .order_by(Mensagem.criado_em_utc)
                .limit(limite)
            )
            return list(res.all())

    async def gravar_conhecimento(
        self,
        titulo: str,
        conteudo: str,
        tags: str = "",
        critico: bool = False,
    ) -> ItemConhecimento:
        item = ItemConhecimento(titulo=titulo, conteudo=conteudo, tags=tags, critico=critico)
        vetor_id = self.vetor.upsert(item.id, f"{titulo}\n{conteudo}", {"titulo": titulo, "tags": tags})
        item.vetor_id = vetor_id
        async with self.session_factory() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
        arquivo = self.dir_conhecimento / f"{item.id}.json"
        arquivo.write_text(
            json.dumps(
                {
                    "id": item.id,
                    "titulo": titulo,
                    "conteudo": conteudo,
                    "tags": tags,
                    "critico": critico,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return item

    async def buscar_conhecimento(self, consulta: str, limite: int = 5) -> list[dict[str, Any]]:
        return self.vetor.buscar(consulta, limite=limite)

    async def registrar_auditoria(self, acao: str, permitido: bool, detalhe: str = "") -> None:
        ev = Auditoria(acao=acao, permitido=permitido, detalhe=detalhe)
        async with self.session_factory() as session:
            session.add(ev)
            await session.commit()

    async def criar_evento_agenda(
        self, titulo: str, inicia_em_utc: datetime, descricao: str = "", termina_em_utc: datetime | None = None
    ) -> EventoAgenda:
        ev = EventoAgenda(
            titulo=titulo,
            descricao=descricao,
            inicia_em_utc=inicia_em_utc,
            termina_em_utc=termina_em_utc,
        )
        async with self.session_factory() as session:
            session.add(ev)
            await session.commit()
            await session.refresh(ev)
        return ev

    async def listar_agenda(self) -> list[EventoAgenda]:
        async with self.session_factory() as session:
            res = await session.exec(select(EventoAgenda).order_by(EventoAgenda.inicia_em_utc))
            return list(res.all())

    async def sync_pull(self, entidade: str, desde_versao: int = 0) -> dict[str, Any]:
        async with self.session_factory() as session:
            if entidade == "mensagens":
                res = await session.exec(
                    select(Mensagem).where(Mensagem.versao_sync > desde_versao).limit(200)
                )
                itens = [m.model_dump(mode="json") for m in res.all()]
            elif entidade == "conhecimento":
                res = await session.exec(
                    select(ItemConhecimento).where(ItemConhecimento.versao_sync > desde_versao).limit(200)
                )
                itens = [m.model_dump(mode="json") for m in res.all()]
            elif entidade == "agenda":
                res = await session.exec(
                    select(EventoAgenda).where(EventoAgenda.versao_sync > desde_versao).limit(200)
                )
                itens = [m.model_dump(mode="json") for m in res.all()]
            else:
                itens = []
            cursor = max([i.get("versao_sync", 0) for i in itens], default=desde_versao)
            row = await session.get(CursorSync, entidade)
            if not row:
                row = CursorSync(entidade=entidade, cursor=cursor)
                session.add(row)
            else:
                row.cursor = max(row.cursor, cursor)
                row.atualizado_em_utc = datetime.now(timezone.utc)
            await session.commit()
        return {"entidade": entidade, "cursor": cursor, "itens": itens}

    async def exportar_snapshot(self, destino: Path) -> Path:
        destino.mkdir(parents=True, exist_ok=True)
        async with self.session_factory() as session:
            dados = {
                "conversas": [c.model_dump(mode="json") for c in (await session.exec(select(Conversa))).all()],
                "mensagens": [m.model_dump(mode="json") for m in (await session.exec(select(Mensagem))).all()],
                "conhecimento": [
                    k.model_dump(mode="json") for k in (await session.exec(select(ItemConhecimento))).all()
                ],
                "agenda": [a.model_dump(mode="json") for a in (await session.exec(select(EventoAgenda))).all()],
            }
        caminho = destino / "memoria.json"
        caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return caminho
