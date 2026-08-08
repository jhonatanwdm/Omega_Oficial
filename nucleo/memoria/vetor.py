from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from typing import Any


def _tokenizar(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower(), flags=re.UNICODE)


def embedding_hash(texto: str, dim: int = 384) -> list[float]:
    """Fallback determinístico quando sentence-transformers/Qdrant não estão disponíveis."""
    vec = [0.0] * dim
    for tok in _tokenizar(texto):
        h = hashlib.sha256(tok.encode("utf-8")).digest()
        for i in range(0, min(len(h), 32)):
            idx = (h[i] + i * 13) % dim
            vec[idx] += (h[i] / 255.0) * 2 - 1
    norma = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norma for v in vec]


def cosseno(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


@dataclass
class DocumentoVetor:
    id: str
    texto: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vetor: list[float] = field(default_factory=list)


class ArmazemVetorialLocal:
    def __init__(self, dim: int = 384) -> None:
        self.dim = dim
        self._docs: dict[str, DocumentoVetor] = {}
        self._embedder = None
        try:
            from sentence_transformers import SentenceTransformer

            self._embedder = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )
            self.dim = int(self._embedder.get_sentence_embedding_dimension())
        except Exception:
            self._embedder = None

        self._qdrant = None
        self._colecao = "omega_conhecimento"
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams

            from nucleo.comum.config import get_settings

            client = QdrantClient(url=get_settings().omega_qdrant_url, timeout=2.0)
            # ping leve
            client.get_collections()
            nomes = {c.name for c in client.get_collections().collections}
            if self._colecao not in nomes:
                client.create_collection(
                    self._colecao,
                    vectors_config=VectorParams(size=self.dim, distance=Distance.COSINE),
                )
            self._qdrant = client
        except Exception:
            self._qdrant = None

    def embed(self, texto: str) -> list[float]:
        if self._embedder is not None:
            return self._embedder.encode(texto).tolist()
        return embedding_hash(texto, self.dim)

    def upsert(self, doc_id: str, texto: str, metadata: dict[str, Any] | None = None) -> str:
        vetor = self.embed(texto)
        meta = metadata or {}
        self._docs[doc_id] = DocumentoVetor(doc_id, texto, meta, vetor)
        if self._qdrant is not None:
            from qdrant_client.http.models import PointStruct

            self._qdrant.upsert(
                collection_name=self._colecao,
                points=[PointStruct(id=doc_id, vector=vetor, payload={"texto": texto, **meta})],
            )
        return doc_id

    def buscar(self, consulta: str, limite: int = 5) -> list[dict[str, Any]]:
        q = self.embed(consulta)
        if self._qdrant is not None:
            try:
                hits = self._qdrant.search(collection_name=self._colecao, query_vector=q, limit=limite)
                return [
                    {
                        "id": str(h.id),
                        "score": float(h.score),
                        "texto": h.payload.get("texto", ""),
                        "metadata": {k: v for k, v in h.payload.items() if k != "texto"},
                    }
                    for h in hits
                ]
            except Exception:
                pass

        ranked = []
        for doc in self._docs.values():
            ranked.append((cosseno(q, doc.vetor), doc))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [
            {"id": d.id, "score": float(s), "texto": d.texto, "metadata": d.metadata}
            for s, d in ranked[:limite]
        ]
