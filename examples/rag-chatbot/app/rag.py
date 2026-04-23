"""RAG pipeline: PDF'i parçala, embed et, Qdrant'a yaz, sorguda ara."""
from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pypdf import PdfReader
from qdrant_client.models import Distance, PointStruct, VectorParams

if TYPE_CHECKING:
    import voyageai
    from qdrant_client import QdrantClient

COLLECTION = "documents"
EMBED_MODEL = "voyage-3"
EMBED_DIM = 1024
CHUNK_TOKENS = 800
CHUNK_OVERLAP = 100


@dataclass
class Chunk:
    id: str
    text: str
    doc_name: str
    page: int


def _pdf_to_text_pages(pdf_bytes: bytes) -> list[tuple[int, str]]:
    """PDF'i sayfa-sayfa metin olarak çıkar. Boş sayfaları atla."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages: list[tuple[int, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append((i, text))
    return pages


def _chunk_text(
    text: str,
    chunk_size: int = CHUNK_TOKENS,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Kelime tabanlı basit chunker. Production için semantic chunker değerlendir."""
    words = text.split()
    if not words:
        return []
    approx_tpw = 1.3
    size = max(1, int(chunk_size / approx_tpw))
    step = max(1, size - int(overlap / approx_tpw))
    chunks = [" ".join(words[i : i + size]) for i in range(0, len(words), step)]
    return [c for c in chunks if c.strip()]


def pdf_to_chunks(pdf_bytes: bytes, doc_name: str) -> list[Chunk]:
    """PDF bytes -> Chunk listesi. ID: doc_name + sayfa + metin-önek hash."""
    chunks: list[Chunk] = []
    for page_num, page_text in _pdf_to_text_pages(pdf_bytes):
        for chunk_text in _chunk_text(page_text):
            cid = hashlib.sha256(
                f"{doc_name}|{page_num}|{chunk_text[:50]}".encode()
            ).hexdigest()[:16]
            chunks.append(
                Chunk(id=cid, text=chunk_text, doc_name=doc_name, page=page_num)
            )
    return chunks


def ensure_collection(client: QdrantClient) -> None:
    """Collection yoksa oluştur."""
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def upsert_chunks(
    client: QdrantClient,
    vo: voyageai.Client,
    chunks: list[Chunk],
) -> int:
    """Voyage AI ile embed -> Qdrant upsert. input_type='document' asimetrisi kritik."""
    if not chunks:
        return 0
    texts = [c.text for c in chunks]
    result = vo.embed(texts, model=EMBED_MODEL, input_type="document")
    vectors = result.embeddings

    points = [
        PointStruct(
            id=int(c.id, 16) % (2**63 - 1),
            vector=vec,
            payload={"text": c.text, "doc_name": c.doc_name, "page": c.page},
        )
        for c, vec in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=COLLECTION, points=points, wait=True)
    return len(points)


def search(
    client: QdrantClient,
    vo: voyageai.Client,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Soruyu embed et (input_type='query'), top_k chunk getir."""
    result = vo.embed([query], model=EMBED_MODEL, input_type="query")
    query_vector = result.embeddings[0]
    hits = client.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=top_k,
    )
    return [
        {
            "text": h.payload["text"],
            "doc_name": h.payload["doc_name"],
            "page": h.payload["page"],
            "score": round(h.score, 4),
        }
        for h in hits
    ]
