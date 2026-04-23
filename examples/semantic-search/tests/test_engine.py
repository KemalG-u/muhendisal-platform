"""Engine birim testleri — mock'suz, Qdrant client lokal Docker'a ihtiyac duymaz."""
from __future__ import annotations

from app.engine import COLLECTION, EMBED_DIM, EMBED_MODEL, Haber


def test_constants() -> None:
    assert COLLECTION == "haberler"
    assert EMBED_DIM == 1024
    assert EMBED_MODEL == "voyage-3"


def test_haber_id_deterministic() -> None:
    """Ayni baslik + kategori -> ayni ID. Idempotent upsert icin kritik."""
    h1 = Haber(baslik="Test baslik", kategori="tek")
    h2 = Haber(baslik="Test baslik", kategori="tek")
    assert h1.id == h2.id


def test_haber_id_kategori_farki() -> None:
    """Ayni baslik farkli kategori -> farkli ID."""
    h1 = Haber(baslik="Test baslik", kategori="tek")
    h2 = Haber(baslik="Test baslik", kategori="spor")
    assert h1.id != h2.id


def test_haber_id_int_range() -> None:
    """ID Qdrant'in kabul ettigi int64 aralik icinde."""
    h = Haber(baslik="X" * 200, kategori="y" * 30)
    assert 0 <= h.id < 2**63


def test_haber_kaynak_opsiyonel() -> None:
    h1 = Haber(baslik="a", kategori="b")
    h2 = Haber(baslik="a", kategori="b", kaynak="https://x.com")
    # kaynak ID'yi etkilemez
    assert h1.id == h2.id
    assert h1.kaynak is None
    assert h2.kaynak == "https://x.com"
