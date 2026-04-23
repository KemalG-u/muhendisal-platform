"""Yazar agent — Her haber başlığı için 2-3 cümlelik Türkçe özet üretir.

Claude Sonnet 4.5 default. Async — çoklu başlık paralel işlenir (asyncio.gather).
Maliyet + token metrikleri her çağrıda loglanır.

Referans: Bölüm 6.5 orchestrator-workers pattern.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass

import anthropic

from .radar import Haber

log = logging.getLogger(__name__)

_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", "5"))

SYSTEM_PROMPT = """Sen bir Türkçe AI haber özetçisin. Görevin:

- Verilen başlığı 2-3 cümlelik Türkçe özete çevir
- Teknik doğrulukta ödün verme, terim uydurma
- Türkçesi doğal olsun, çeviri tadı verme
- Başlığı tekrarlama; ek bilgi / bağlam / çıkarım ekle
- Emoji, slogan, abartı yok

Formatın: SADECE özet metin. Başlık, madde işareti, meta açıklama YOK.
"""


@dataclass
class Ozet:
    """Bir haberin özet çıktısı + maliyet meta verisi."""

    haber: Haber
    metin: str
    input_tokens: int
    output_tokens: int
    model: str

    @property
    def maliyet_usd(self) -> float:
        """Claude fiyatları 2026 Nisan itibarıyla docs.claude.com/pricing:
        Sonnet 4.5: $3 / 1M input, $15 / 1M output
        Haiku 4.5:  $1 / 1M input,  $5 / 1M output
        """
        if "haiku" in self.model.lower():
            return (self.input_tokens * 1.0 + self.output_tokens * 5.0) / 1_000_000
        return (self.input_tokens * 3.0 + self.output_tokens * 15.0) / 1_000_000


async def ozetle_tek(
    client: anthropic.AsyncAnthropic,
    haber: Haber,
    model: str | None = None,
    semaphore: asyncio.Semaphore | None = None,
) -> Ozet:
    """Tek bir haberi özetler."""
    model = model or os.environ.get("WRITER_MODEL", "claude-sonnet-4-5")

    user_msg = f"BAŞLIK: {haber.baslik}\n\nKAYNAK: {haber.kaynak}"
    if haber.ozet_ham:
        user_msg += f"\n\nRSS ÖZET HAM (referans):\n{haber.ozet_ham}"

    async def _call():
        return await client.messages.create(
            model=model,
            max_tokens=256,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )

    if semaphore is not None:
        async with semaphore:
            resp = await _call()
    else:
        resp = await _call()

    metin = "".join(
        block.text for block in resp.content if block.type == "text"
    ).strip()

    return Ozet(
        haber=haber,
        metin=metin,
        input_tokens=resp.usage.input_tokens,
        output_tokens=resp.usage.output_tokens,
        model=model,
    )


async def ozetle_toplu(
    haberler: list[Haber],
    model: str | None = None,
) -> list[Ozet]:
    """Birden fazla haberi paralel olarak özetler.

    Orchestrator-workers pattern (6.5). asyncio.gather ile toplam süre
    ≈ en yavaş çağrının süresi. Semaphore ile eşzamanlı çağrı sayısı
    `MAX_CONCURRENCY` (default 5) ile sınırlı — rate limit koruması.
    """
    client = anthropic.AsyncAnthropic()
    sem = asyncio.Semaphore(_CONCURRENCY)
    tasks = [ozetle_tek(client, h, model, semaphore=sem) for h in haberler]
    return await asyncio.gather(*tasks)
