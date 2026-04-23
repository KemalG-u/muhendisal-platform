"""Semantic search engine: Voyage AI embed + Qdrant retrieval.

Asimetri: yazarken input_type='document', sorgularken input_type='query'.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import TYPE_CHECKING

from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchAny,
    MatchValue,
    PointStruct,
    VectorParams,
)

if TYPE_CHECKING:
    import voyageai
    from qdrant_client import QdrantClient

COLLECTION = "haberler"
EMBED_MODEL = "voyage-3"
EMBED_DIM = 1024


@dataclass
class Haber:
    """Bir haber baslik + kategori + (opsiyonel) kaynak URL."""

    baslik: str
    kategori: str
    kaynak: str | None = None

    @property
    def id(self) -> int:
        """SHA-256 tabanli deterministik integer ID. Qdrant int ister."""
        h = hashlib.sha256(
            f"{self.kategori}|{self.baslik}".encode()
        ).hexdigest()[:15]
        return int(h, 16) % (2**63 - 1)


def ensure_collection(client: QdrantClient, name: str = COLLECTION) -> None:
    """Koleksiyon yoksa olustur (idempotent)."""
    existing = [c.name for c in client.get_collections().collections]
    if name not in existing:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def upsert_haberler(
    client: QdrantClient,
    vo: voyageai.Client,
    haberler: list[Haber],
) -> int:
    """Haberleri embed et ve Qdrant'a yaz. input_type='document' kritik."""
    if not haberler:
        return 0

    metinler = [h.baslik for h in haberler]
    result = vo.embed(metinler, model=EMBED_MODEL, input_type="document")
    vektorler = result.embeddings

    points = [
        PointStruct(
            id=h.id,
            vector=vec,
            payload={"baslik": h.baslik, "kategori": h.kategori, "kaynak": h.kaynak},
        )
        for h, vec in zip(haberler, vektorler, strict=True)
    ]
    client.upsert(collection_name=COLLECTION, points=points, wait=True)
    return len(points)


def search(
    client: QdrantClient,
    vo: voyageai.Client,
    sorgu: str,
    top_k: int = 5,
    kategoriler: list[str] | None = None,
) -> list[dict]:
    """Sorguyu embed et (input_type='query') ve Qdrant'ta ara.

    kategoriler verilirse payload filter uygula.
    """
    q_result = vo.embed([sorgu], model=EMBED_MODEL, input_type="query")
    q_vector = q_result.embeddings[0]

    query_filter = None
    if kategoriler:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="kategori",
                    match=(
                        MatchValue(value=kategoriler[0])
                        if len(kategoriler) == 1
                        else MatchAny(any=kategoriler)
                    ),
                )
            ]
        )

    hits = client.search(
        collection_name=COLLECTION,
        query_vector=q_vector,
        limit=top_k,
        query_filter=query_filter,
    )

    return [
        {
            "baslik": h.payload["baslik"],
            "kategori": h.payload["kategori"],
            "kaynak": h.payload.get("kaynak"),
            "skor": round(h.score, 4),
        }
        for h in hits
    ]


def collection_stats(client: QdrantClient) -> dict:
    """Koleksiyon istatistikleri."""
    info = client.get_collection(COLLECTION)
    return {
        "nokta_sayisi": info.points_count,
        "boyut": EMBED_DIM,
        "metric": "cosine",
    }
