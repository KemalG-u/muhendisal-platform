"""Radar agent — Türkçe AI haber kaynaklarından son 24 saat başlıklarını toplar.

RSS feed öncelikli (ücretsiz). FIRECRAWL_API_KEY tanımlıysa opsiyonel olarak
HTML sayfalarını da derin tarar.

Referans: MühendisAl Bölüm 6 — https://wiki.oluk.org/platform/bolum-6/
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import feedparser
import httpx

# Türkçe teknoloji / AI RSS kaynakları — kullanıcı kendi listesini genişletebilir.
# NOT: Bu kaynaklar örnek amaçlı; üretimde kendi alan listeni oluştur.
DEFAULT_FEEDS: list[str] = [
    "https://webrazzi.com/feed/",
    "https://shiftdelete.net/feed",
    "https://www.donanimhaber.com/rss/tum/",
]

# Konu filtresi — başlık bu anahtar kelimelerden en az birini içermeli
KEYWORDS: tuple[str, ...] = (
    "yapay zeka", "ai ", " ai", "llm", "claude", "gpt", "agent",
    "model", "chatbot", "openai", "anthropic", "gemini", "hugging",
)


@dataclass
class Haber:
    """Tek bir haber başlığı + meta veri."""

    baslik: str
    link: str
    kaynak: str
    yayin_tarihi: datetime
    ozet_ham: str = ""   # RSS'ten gelen ham özet (varsa)


async def topla(
    feeds: list[str] | None = None,
    son_saat: int = 24,
    max_adet: int = 20,
) -> list[Haber]:
    """Son N saatteki AI haberlerini toplar.

    Args:
        feeds: RSS URL listesi. None ise DEFAULT_FEEDS kullanılır.
        son_saat: Ne kadar geriye bakılsın (saat).
        max_adet: Dönecek maksimum haber sayısı.

    Returns:
        Yayın tarihine göre azalan sıralı `Haber` listesi.
    """
    feeds = feeds or DEFAULT_FEEDS
    esik = datetime.now(timezone.utc) - timedelta(hours=son_saat)
    haberler: list[Haber] = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        for url in feeds:
            try:
                r = await client.get(url, follow_redirects=True)
                r.raise_for_status()
            except httpx.HTTPError as e:
                print(f"[radar] {url} okunamadı: {e}")
                continue

            parsed = feedparser.parse(r.content)
            kaynak = parsed.feed.get("title", url)

            for entry in parsed.entries:
                # Yayın tarihini çek (struct_time → datetime)
                tarih_raw = entry.get("published_parsed") or entry.get("updated_parsed")
                if not tarih_raw:
                    continue
                tarih = datetime(*tarih_raw[:6], tzinfo=timezone.utc)
                if tarih < esik:
                    continue

                baslik = entry.get("title", "").strip()
                if not baslik:
                    continue

                # Anahtar kelime filtresi — AI/teknoloji odaklı tut
                if not any(k in baslik.lower() for k in KEYWORDS):
                    continue

                haberler.append(Haber(
                    baslik=baslik,
                    link=entry.get("link", ""),
                    kaynak=kaynak,
                    yayin_tarihi=tarih,
                    ozet_ham=entry.get("summary", "")[:500],
                ))

    # En yeni önce, max_adet ile kes
    haberler.sort(key=lambda h: h.yayin_tarihi, reverse=True)
    return haberler[:max_adet]


async def firecrawl_derinlemesine(url: str) -> str:
    """Opsiyonel — Firecrawl ile bir sayfanın tam metnini çeker.

    FIRECRAWL_API_KEY yoksa boş string döner. Kullanım: öne çıkan bir
    başlığın tam metnini özetlemeden önce çek.
    """
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        return ""

    async with httpx.AsyncClient(timeout=20.0) as c:
        r = await c.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers={"Authorization": f"Bearer {key}"},
            json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
        )
        if r.status_code != 200:
            return ""
        return r.json().get("data", {}).get("markdown", "")[:4000]
