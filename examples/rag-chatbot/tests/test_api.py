"""FastAPI endpoint testleri — TestClient + state mock.

Not: `with TestClient(app)` lifespan'i tetikler ve env var gerektirir.
Testte state'i doğrudan set ettiğimiz için `with`-siz kullanım lifespan'i atlatır."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client_with_mock_state():
    """Lifespan'i atlayıp state'i doğrudan mock'la."""
    from app.main import app

    app.state.qdrant = MagicMock()
    app.state.voyage = MagicMock()
    # `with` YOK — lifespan tetiklenmez, env var sorgusu yapılmaz.
    yield TestClient(app)


def test_health(client_with_mock_state: TestClient) -> None:
    r = client_with_mock_state.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "git_sha" in body


def test_index_renders(client_with_mock_state: TestClient) -> None:
    """Ana sayfa HTML render eder, HTMX + Tailwind CDN içerir."""
    r = client_with_mock_state.get("/")
    assert r.status_code == 200
    html = r.text
    assert "RAG Chatbot" in html
    assert "htmx" in html.lower()
    assert 'hx-post="/upload"' in html
    assert 'hx-post="/ask"' in html


def test_upload_rejects_non_pdf(client_with_mock_state: TestClient) -> None:
    """PDF olmayan dosya 400 döndürür."""
    r = client_with_mock_state.post(
        "/upload",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert r.status_code == 400
    assert "PDF" in r.json()["detail"]


def test_upload_empty_pdf_accepts(
    client_with_mock_state: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Geçerli PDF uzantısı + mock'lu voyage → 200, chunks sayısı dönmeli."""
    from app import main

    monkeypatch.setattr(main, "pdf_to_chunks", lambda b, doc_name: [])
    monkeypatch.setattr(main, "upsert_chunks", lambda c, v, chunks: len(chunks))

    pdf_bytes = b"%PDF-1.4\n%%EOF\n"
    r = client_with_mock_state.post(
        "/upload",
        files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["doc"] == "test.pdf"
    assert body["chunks"] == 0


def test_ask_without_sources(
    client_with_mock_state: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Qdrant boşsa 'Önce PDF yükle' mesajı."""
    from app import main

    monkeypatch.setattr(main, "search", lambda c, v, q, top_k: [])

    r = client_with_mock_state.post("/ask", data={"question": "test?"})
    assert r.status_code == 200
    assert "Önce PDF yükle" in r.text
