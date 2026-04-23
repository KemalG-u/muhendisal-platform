"""FastAPI semantic search servisi.

Endpoint'ler:
    GET  /health         saglik + collection boyutu
    POST /ekle           tek haber ekle
    POST /toplu-ekle     bir listede N haber
    POST /ara            sorgu + opsiyonel kategori filter
    GET  /istatistik     collection stats
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

import voyageai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

from app.engine import (
    Haber,
    collection_stats,
    ensure_collection,
    search,
    upsert_haberler,
)


class HaberInput(BaseModel):
    baslik: str = Field(..., min_length=3, max_length=500)
    kategori: str = Field(..., min_length=1, max_length=50)
    kaynak: str | None = None


class AramaInput(BaseModel):
    sorgu: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(5, ge=1, le=50)
    kategoriler: list[str] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: Qdrant + Voyage client + koleksiyon."""
    app.state.qdrant = QdrantClient(
        url=os.environ.get("QDRANT_URL", "http://qdrant:6333")
    )
    app.state.voyage = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    ensure_collection(app.state.qdrant)
    yield


def create_app() -> FastAPI:
    return FastAPI(title="Semantic Search", lifespan=lifespan)


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "git_sha": os.environ.get("GIT_SHA", "dev")}


@app.get("/istatistik")
def istatistik() -> dict:
    return collection_stats(app.state.qdrant)


@app.post("/ekle")
def ekle(inp: HaberInput) -> dict:
    h = Haber(baslik=inp.baslik, kategori=inp.kategori, kaynak=inp.kaynak)
    n = upsert_haberler(app.state.qdrant, app.state.voyage, [h])
    return {"eklenen": n, "id": h.id}


@app.post("/toplu-ekle")
def toplu_ekle(haberler: list[HaberInput]) -> dict:
    if len(haberler) > 500:
        raise HTTPException(413, "Tek istekte max 500 haber")
    objs = [Haber(baslik=h.baslik, kategori=h.kategori, kaynak=h.kaynak) for h in haberler]
    n = upsert_haberler(app.state.qdrant, app.state.voyage, objs)
    return {"eklenen": n}


@app.post("/ara")
def ara(inp: AramaInput) -> dict:
    sonuclar = search(
        app.state.qdrant,
        app.state.voyage,
        sorgu=inp.sorgu,
        top_k=inp.top_k,
        kategoriler=inp.kategoriler,
    )
    return {"sorgu": inp.sorgu, "sonuclar": sonuclar}
