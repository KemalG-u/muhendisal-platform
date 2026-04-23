"""FastAPI app: /upload, /ask, /health."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

import voyageai
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from qdrant_client import QdrantClient

from app.claude import stream_answer
from app.rag import ensure_collection, pdf_to_chunks, search, upsert_chunks

BASE = Path(__file__).parent
templates = Jinja2Templates(directory=BASE / "templates")

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: Qdrant + Voyage client + collection. Shutdown: clean (auto)."""
    app.state.qdrant = QdrantClient(
        url=os.environ.get("QDRANT_URL", "http://qdrant:6333")
    )
    app.state.voyage = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    ensure_collection(app.state.qdrant)
    yield


def create_app() -> FastAPI:
    """Factory — test için mock'lanabilir lifespan."""
    app = FastAPI(title="RAG Chatbot", lifespan=lifespan)
    app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
    return app


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "git_sha": os.environ.get("GIT_SHA", "dev")}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict[str, int | str]:
    """PDF yükle, chunk'la, Qdrant'a gönder."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Sadece PDF")
    if file.size and file.size > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Max 20 MB")

    content = await file.read()
    chunks = pdf_to_chunks(content, doc_name=file.filename)
    n = upsert_chunks(app.state.qdrant, app.state.voyage, chunks)
    return {"doc": file.filename, "chunks": n}


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)) -> StreamingResponse:
    """Soru -> retrieval -> Claude streaming cevap + kaynak listesi."""
    sources = search(app.state.qdrant, app.state.voyage, question, top_k=5)
    if not sources:
        return HTMLResponse('<div class="answer">Önce PDF yükle.</div>')

    async def generate():
        yield '<div class="answer"><div class="stream">'
        async for token in stream_answer(question, sources):
            yield token
        yield "</div>"
        yield templates.get_template("_answer.html").render(sources=sources)
        yield "</div>"

    return StreamingResponse(generate(), media_type="text/html")
