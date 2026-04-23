"""FastAPI endpoint testleri — TestClient + state mock.

Lifespan VOYAGE_API_KEY ister, bu yuzden `with TestClient(app)` YOK.
State manuel set edilir (9.4 rag-chatbot'tan miras pattern).
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client_with_mock_state():
    from app.main import app

    app.state.qdrant = MagicMock()
    app.state.voyage = MagicMock()
    yield TestClient(app)


def test_health(client_with_mock_state: TestClient) -> None:
    r = client_with_mock_state.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_istatistik_calls_collection_stats(
    client_with_mock_state: TestClient, monkeypatch
) -> None:
    from app import main

    monkeypatch.setattr(
        main,
        "collection_stats",
        lambda c: {"nokta_sayisi": 42, "boyut": 1024, "metric": "cosine"},
    )
    r = client_with_mock_state.get("/istatistik")
    assert r.status_code == 200
    assert r.json()["nokta_sayisi"] == 42


def test_ekle_validation(client_with_mock_state: TestClient) -> None:
    """Baslik cok kisa -> 422."""
    r = client_with_mock_state.post(
        "/ekle", json={"baslik": "a", "kategori": "tek"}
    )
    assert r.status_code == 422


def test_ekle_basarili(client_with_mock_state: TestClient, monkeypatch) -> None:
    from app import main

    monkeypatch.setattr(main, "upsert_haberler", lambda c, v, hs: len(hs))
    r = client_with_mock_state.post(
        "/ekle",
        json={"baslik": "Test haberi basligi", "kategori": "tek"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["eklenen"] == 1
    assert isinstance(body["id"], int)


def test_toplu_ekle_limit(client_with_mock_state: TestClient) -> None:
    """501+ haber -> 413."""
    big = [{"baslik": "x" * 20, "kategori": "y"} for _ in range(501)]
    r = client_with_mock_state.post("/toplu-ekle", json=big)
    assert r.status_code == 413


def test_ara_basarili(client_with_mock_state: TestClient, monkeypatch) -> None:
    from app import main

    monkeypatch.setattr(
        main,
        "search",
        lambda c, v, sorgu, top_k, kategoriler: [
            {"baslik": "x", "kategori": "tek", "kaynak": None, "skor": 0.9}
        ],
    )
    r = client_with_mock_state.post(
        "/ara",
        json={"sorgu": "AI gelismeleri", "top_k": 3},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["sorgu"] == "AI gelismeleri"
    assert len(body["sonuclar"]) == 1


def test_ara_validation(client_with_mock_state: TestClient) -> None:
    """top_k 0 -> 422."""
    r = client_with_mock_state.post(
        "/ara", json={"sorgu": "test", "top_k": 0}
    )
    assert r.status_code == 422
