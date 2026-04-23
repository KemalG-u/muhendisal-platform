"""Upsert/search davranisi — Qdrant ve Voyage MagicMock ile."""
from __future__ import annotations

from unittest.mock import MagicMock

from app.engine import Haber, search, upsert_haberler


def _mock_clients(mock_embeddings: list[list[float]] | None = None):
    """Qdrant ve Voyage client'larini mockla."""
    qdrant = MagicMock()
    voyage = MagicMock()
    # voyage.embed(...).embeddings -> list[list[float]]
    if mock_embeddings is None:
        mock_embeddings = [[0.1] * 1024]
    voyage.embed.return_value = MagicMock(embeddings=mock_embeddings)
    return qdrant, voyage


def test_upsert_empty_list_returns_zero() -> None:
    qdrant, voyage = _mock_clients()
    assert upsert_haberler(qdrant, voyage, []) == 0
    voyage.embed.assert_not_called()
    qdrant.upsert.assert_not_called()


def test_upsert_calls_voyage_with_document_mode() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.1] * 1024])
    haberler = [Haber(baslik="Test", kategori="tek")]
    n = upsert_haberler(qdrant, voyage, haberler)
    assert n == 1

    # input_type='document' asimetrisi kritik
    kwargs = voyage.embed.call_args.kwargs
    assert kwargs["input_type"] == "document"
    assert kwargs["model"] == "voyage-3"


def test_upsert_passes_payload_to_qdrant() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.1] * 1024])
    haberler = [Haber(baslik="Selam dunya", kategori="tek", kaynak="https://x.com")]
    upsert_haberler(qdrant, voyage, haberler)

    points = qdrant.upsert.call_args.kwargs["points"]
    assert len(points) == 1
    assert points[0].payload["baslik"] == "Selam dunya"
    assert points[0].payload["kategori"] == "tek"
    assert points[0].payload["kaynak"] == "https://x.com"


def test_search_uses_query_mode() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.2] * 1024])
    # Qdrant.search -> liste of hits
    fake_hit = MagicMock()
    fake_hit.score = 0.87
    fake_hit.payload = {
        "baslik": "Bulundu",
        "kategori": "tek",
        "kaynak": None,
    }
    qdrant.search.return_value = [fake_hit]

    sonuc = search(qdrant, voyage, sorgu="test soru?")
    assert len(sonuc) == 1
    assert sonuc[0]["baslik"] == "Bulundu"
    assert sonuc[0]["skor"] == 0.87

    # input_type='query' asimetrisi
    assert voyage.embed.call_args.kwargs["input_type"] == "query"


def test_search_with_single_kategori_filter() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.2] * 1024])
    qdrant.search.return_value = []
    search(qdrant, voyage, sorgu="x", kategoriler=["tek"])

    # query_filter gecerli olmali
    filter_arg = qdrant.search.call_args.kwargs["query_filter"]
    assert filter_arg is not None


def test_search_without_filter_passes_none() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.2] * 1024])
    qdrant.search.return_value = []
    search(qdrant, voyage, sorgu="x")

    filter_arg = qdrant.search.call_args.kwargs["query_filter"]
    assert filter_arg is None


def test_search_respects_top_k() -> None:
    qdrant, voyage = _mock_clients(mock_embeddings=[[0.2] * 1024])
    qdrant.search.return_value = []
    search(qdrant, voyage, sorgu="x", top_k=10)

    assert qdrant.search.call_args.kwargs["limit"] == 10
