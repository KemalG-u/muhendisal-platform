"""Pipeline birim testleri.

Gerçek Claude API çağrısı YAPMAZ — mock kullanır. CI'da deterministic
çalışması için. Gerçek API ile entegrasyon testi için `test_live.py`
ayrı dosyada yazılabilir (bu repoda opsiyonel).

pyproject `asyncio_mode = "auto"` ayarlı — async test fonksiyonları
@pytest.mark.asyncio decoratoru GEREKSİZDİR, otomatik çalışır.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from agents.radar import Haber, KEYWORDS
from agents.yazar import Ozet, ozetle_tek
from agents.evaluator import Puan, puanla_tek
from agents.publisher import rapor_yaz


# ─── Fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def ornek_haber() -> Haber:
    return Haber(
        baslik="Anthropic Claude 4.5 için yeni tool use güncellemesi duyurdu",
        link="https://example.com/haber",
        kaynak="Örnek RSS",
        yayin_tarihi=datetime(2026, 4, 22, 10, 0, tzinfo=timezone.utc),
        ozet_ham="Claude artık paralel tool çağrılarını destekliyor...",
    )


@pytest.fixture
def ornek_ozet(ornek_haber) -> Ozet:
    return Ozet(
        haber=ornek_haber,
        metin="Anthropic, Claude 4.5 için paralel tool çağrısı özelliği duyurdu; "
              "agent'lar artık tek turda birden fazla tool'u aynı anda tetikleyebiliyor.",
        input_tokens=120,
        output_tokens=45,
        model="claude-sonnet-4-5",
    )


# ─── Radar testleri ──────────────────────────────────────────────────────

def test_anahtar_kelime_listesi_ai_terimlerini_icerir():
    """KEYWORDS listesi kritik AI terimlerini içermeli."""
    kritik = ["yapay zeka", "llm", "claude", "gpt", "model"]
    for k in kritik:
        assert k in KEYWORDS, f"'{k}' KEYWORDS içinde olmalı"


def test_haber_dataclass_alanlari(ornek_haber):
    """Haber dataclass beklenen alanlara sahip."""
    assert ornek_haber.baslik
    assert ornek_haber.link.startswith("https://")
    assert ornek_haber.yayin_tarihi.tzinfo is not None  # UTC aware


# ─── Yazar testleri ──────────────────────────────────────────────────────

async def test_ozetle_tek_mock(ornek_haber):
    """Yazar agent'ı mock API ile test."""
    client = MagicMock()
    fake_resp = MagicMock()
    fake_text = MagicMock(type="text", text="Mock özet metni.")
    fake_resp.content = [fake_text]
    fake_resp.usage = MagicMock(input_tokens=100, output_tokens=40)
    client.messages.create = AsyncMock(return_value=fake_resp)

    ozet = await ozetle_tek(client, ornek_haber)
    assert ozet.metin == "Mock özet metni."
    assert ozet.input_tokens == 100
    assert ozet.output_tokens == 40
    assert ozet.maliyet_usd > 0


def test_ozet_maliyet_hesabi():
    """Sonnet 4.5 fiyat hesabı doğru — $3/1M input, $15/1M output."""
    h = Haber("t", "https://x", "k", datetime.now(timezone.utc))
    o = Ozet(haber=h, metin="x", input_tokens=1_000_000, output_tokens=1_000_000,
             model="claude-sonnet-4-5")
    assert o.maliyet_usd == pytest.approx(18.0)  # $3 + $15


def test_haiku_daha_ucuz():
    """Haiku 4.5 Sonnet'ten ucuz olmalı."""
    h = Haber("t", "https://x", "k", datetime.now(timezone.utc))
    sonnet = Ozet(h, "x", 1000, 1000, "claude-sonnet-4-5").maliyet_usd
    haiku = Ozet(h, "x", 1000, 1000, "claude-haiku-4-5").maliyet_usd
    assert haiku < sonnet


# ─── Evaluator testleri ──────────────────────────────────────────────────

async def test_puanla_tek_mock(ornek_ozet):
    """Evaluator tool_use çıktısı doğru parse edilmeli."""
    client = MagicMock()
    tool_block = MagicMock(type="tool_use", input={
        "teknik_dogruluk": 8,
        "turkce_kalitesi": 7,
        "ozet_netligi": 9,
        "aciklama": "Teknik terimler doğru, dil akıcı.",
    })
    fake_resp = MagicMock()
    fake_resp.content = [tool_block]
    fake_resp.usage = MagicMock(input_tokens=200, output_tokens=60)
    client.messages.create = AsyncMock(return_value=fake_resp)

    puan = await puanla_tek(client, ornek_ozet)
    assert puan.teknik_dogruluk == 8
    assert puan.turkce_kalitesi == 7
    assert puan.ozet_netligi == 9
    assert puan.ortalama == pytest.approx(8.0)
    assert puan.yayinlandi is False  # publisher henüz çağrılmadı


async def test_puanla_tool_use_yoksa_notr_puan(ornek_ozet):
    """Tool çağrısı başarısızsa nötr (5/5/5) puan dönmeli — eşik geçmez."""
    client = MagicMock()
    fake_resp = MagicMock()
    fake_resp.content = []  # tool_use bloğu yok
    fake_resp.usage = MagicMock(input_tokens=200, output_tokens=0)
    client.messages.create = AsyncMock(return_value=fake_resp)

    puan = await puanla_tek(client, ornek_ozet)
    assert puan.ortalama == pytest.approx(5.0)
    assert "başarısız" in puan.aciklama.lower()


# ─── Publisher testleri ──────────────────────────────────────────────────

def test_rapor_yaz_esik_filtresi(ornek_ozet):
    """Eşik altı puanlar rapora girmemeli + yayınlanan Puan.yayinlandi=True."""
    yuksek = Puan(ornek_ozet, 9, 9, 9, "İyi", 100, 30, "claude-haiku-4-5")
    dusuk = Puan(ornek_ozet, 3, 4, 3, "Kötü", 100, 30, "claude-haiku-4-5")

    _, yayin = rapor_yaz([yuksek, dusuk], esik=6.5, dry_run=True)
    assert len(yayin) == 1
    assert yayin[0].ortalama == pytest.approx(9.0)
    # yayinlandi flag'i doğru set edilmiş mi
    assert yuksek.yayinlandi is True
    assert dusuk.yayinlandi is False


def test_rapor_yaz_bos_liste():
    """Hiç eşik üstü yoksa yayın boş olmalı."""
    _, yayin = rapor_yaz([], esik=6.5, dry_run=True)
    assert yayin == []
