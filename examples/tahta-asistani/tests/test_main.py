"""Tests — Claude vision mock + FastAPI endpoints."""
from __future__ import annotations

import io
import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image


@pytest.fixture
def test_image_bytes() -> bytes:
    """Kucuk test JPG uret (100x100 siyah)."""
    img = Image.new("RGB", (100, 100), color="black")
    buf = io.BytesIO()
    img.save(buf, "JPEG")
    return buf.getvalue()


@pytest.fixture
def fake_claude_response() -> dict:
    return {
        "ozet": "Bu derste fotosentez konusu islendi. Isik + CO2 + su kullanilarak glikoz ve oksijen uretilir.",
        "kavramlar": [
            {"ad": "Fotosentez", "aciklama": "Bitkilerin isik enerjisini kimyasal enerjiye cevirme sureci."},
            {"ad": "Klorofil", "aciklama": "Isigi yakalayan yesil pigment."},
            {"ad": "Glikoz", "aciklama": "Fotosentez sonucu uretilen seker."},
        ],
        "quiz": [
            {
                "soru": "Fotosentez nerede gerceklesir?",
                "secenekler": ["Ribozom", "Kloroplast", "Mitokondri", "Golgi"],
                "dogru_index": 1,
                "aciklama": "Kloroplastlar klorofil icerir ve fotosentez merkezidir.",
            },
            {
                "soru": "Fotosentez icin hangisi GEREKLI DEGIL?",
                "secenekler": ["Isik", "Karbondioksit", "Oksijen", "Su"],
                "dogru_index": 2,
                "aciklama": "Oksijen urun, girdi degil.",
            },
            {
                "soru": "Glikoz nedir?",
                "secenekler": ["Yag", "Protein", "Seker", "Vitamin"],
                "dogru_index": 2,
                "aciklama": "Glikoz basit bir sekerdir.",
            },
        ],
    }


@pytest.fixture
def client(fake_claude_response):
    """TestClient with mocked Claude."""
    with patch("app.main._client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=json.dumps(fake_claude_response))]
        mock_client.messages.create.return_value = mock_msg

        from app.main import app
        yield TestClient(app)


def test_root_endpoint(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert "Tahta Asistani" in data["servis"]


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analiz_success(client, test_image_bytes):
    r = client.post(
        "/analiz",
        files={"foto": ("tahta.jpg", test_image_bytes, "image/jpeg")},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "istek_id" in data
    assert len(data["ozet"]) > 20
    assert len(data["kavramlar"]) == 3
    assert len(data["quiz"]) == 3


def test_analiz_yapilandirma(client, test_image_bytes):
    r = client.post(
        "/analiz",
        files={"foto": ("tahta.jpg", test_image_bytes, "image/jpeg")},
    )
    data = r.json()
    # Kavram yapisi
    kav = data["kavramlar"][0]
    assert "ad" in kav and "aciklama" in kav
    # Quiz yapisi
    q = data["quiz"][0]
    assert "soru" in q
    assert len(q["secenekler"]) == 4
    assert 0 <= q["dogru_index"] <= 3


def test_analiz_gecersiz_format(client):
    """TXT dosya atma - reddedilmeli."""
    r = client.post(
        "/analiz",
        files={"foto": ("metin.txt", b"bu bir yazidir", "text/plain")},
    )
    assert r.status_code == 400
    assert "Format desteklenmez" in r.json()["detail"]


def test_analiz_png_kabul(client, test_image_bytes):
    """PNG de kabul edilmeli."""
    img = Image.new("RGB", (100, 100), color="white")
    buf = io.BytesIO()
    img.save(buf, "PNG")

    r = client.post(
        "/analiz",
        files={"foto": ("tahta.png", buf.getvalue(), "image/png")},
    )
    assert r.status_code == 200


def test_analiz_cok_buyuk(client):
    """11 MB dosya - reddedilmeli."""
    big_data = b"\xff" * (11 * 1024 * 1024)
    r = client.post(
        "/analiz",
        files={"foto": ("buyuk.jpg", big_data, "image/jpeg")},
    )
    assert r.status_code == 413


def test_quiz_dogru_index_gecerli(client, test_image_bytes):
    r = client.post(
        "/analiz",
        files={"foto": ("tahta.jpg", test_image_bytes, "image/jpeg")},
    )
    data = r.json()
    for q in data["quiz"]:
        # Dogru index 0-3 arasinda + secenekler listesinde
        assert 0 <= q["dogru_index"] < len(q["secenekler"])


def test_analiz_claude_json_parse_hatasi(test_image_bytes):
    """Claude hatali JSON donerse 500."""
    with patch("app.main._client") as mock_client:
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="bozuk {json not parseable")]
        mock_client.messages.create.return_value = mock_msg

        from app.main import app
        c = TestClient(app)
        r = c.post(
            "/analiz",
            files={"foto": ("t.jpg", test_image_bytes, "image/jpeg")},
        )
        assert r.status_code == 500


def test_model_schema(fake_claude_response):
    """Pydantic model ile sonuc parse edilebilmeli."""
    from app.main import AnalizSonuc, Kavram, QuizSorusu

    sonuc = AnalizSonuc(
        istek_id="test123",
        ozet=fake_claude_response["ozet"],
        kavramlar=[Kavram(**k) for k in fake_claude_response["kavramlar"]],
        quiz=[QuizSorusu(**q) for q in fake_claude_response["quiz"]],
    )
    assert sonuc.istek_id == "test123"
    assert len(sonuc.kavramlar) == 3


def test_allowed_media_set():
    """JPEG + PNG + WEBP kabul."""
    from app.main import ALLOWED_MEDIA
    assert "image/jpeg" in ALLOWED_MEDIA
    assert "image/png" in ALLOWED_MEDIA
    assert "image/webp" in ALLOWED_MEDIA


def test_max_bytes_constant():
    from app.main import MAX_IMAGE_BYTES
    assert MAX_IMAGE_BYTES == 5 * 1024 * 1024


def test_resize_kucuk_degismez(test_image_bytes):
    """100x100 JPG tetiklemez downscale."""
    from app.main import _resize_if_huge
    data, media = _resize_if_huge(test_image_bytes, "image/jpeg")
    assert data == test_image_bytes
    assert media == "image/jpeg"


def test_resize_buyuk_downscale():
    """3000x3000 dogal downscale."""
    from app.main import _resize_if_huge
    img = Image.new("RGB", (3000, 3000), "red")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=95)
    orig = buf.getvalue()

    new_data, new_media = _resize_if_huge(orig, "image/jpeg")
    new_img = Image.open(io.BytesIO(new_data))
    assert max(new_img.size) <= 2048
    assert new_media == "image/jpeg"
