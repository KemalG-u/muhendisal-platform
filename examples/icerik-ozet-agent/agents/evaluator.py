"""Evaluator agent — Her özeti kalite kriterlerine göre 0-10 puanlar.

Evaluator-optimizer pattern (Bölüm 6.5). Ayrı (genelde daha ucuz) bir model
ile ikinci pass — üretici tek başına objektif olamaz.

Structured output: Claude'un tool_choice="tool" mekanizması ile JSON şema
garanti (Bölüm 6.2). Puanlar + açıklama zorunlu.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field

import anthropic

from .yazar import Ozet

log = logging.getLogger(__name__)

# Aynı anda Anthropic API'ye açılan maks bağlantı — rate limit güvenliği
_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", "5"))


# Structured output — Claude bu tool'u çağırmak ZORUNDA, bize istenen JSON gelir
PUANLAMA_TOOL = {
    "name": "ozeti_puanla",
    "description": "Verilen özeti 3 kritere göre 0-10 arası puanla ve kısa açıklama yaz.",
    "input_schema": {
        "type": "object",
        "properties": {
            "teknik_dogruluk": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10,
                "description": "Teknik terim kullanımı doğru mu? Terim uydurmuş mu?",
            },
            "turkce_kalitesi": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10,
                "description": "Dil doğal mı? Çeviri tadı var mı? Gramer hatası?",
            },
            "ozet_netligi": {
                "type": "integer",
                "minimum": 0,
                "maximum": 10,
                "description": "Haberin ana noktası net mi? Gereksiz kelimesi var mı?",
            },
            "aciklama": {
                "type": "string",
                "description": "Puanlamanın kısa gerekçesi, 1-2 cümle.",
            },
        },
        "required": ["teknik_dogruluk", "turkce_kalitesi", "ozet_netligi", "aciklama"],
    },
}

SYSTEM_PROMPT = """Sen Türkçe AI haberleri özetlerini denetleyen bir editörsün.

Sana verilecek başlık + özet çiftini 3 kritere göre puanla:
1. Teknik doğruluk (terim kullanımı, olgusal hatalar)
2. Türkçe kalitesi (doğallık, gramer, akıcılık)
3. Özet netliği (ana nokta, gereksiz kelime)

Her kriteri 0-10 arası ver. 7 ve üstü "iyi", 5-6 "orta", altı "zayıf".
SADECE `ozeti_puanla` tool'unu çağır — metin cevap verme.
"""


@dataclass
class Puan:
    """Puanlama çıktısı + yayın durumu.

    `yayinlandi` alanı publisher tarafından eşik kontrolü sonrasında
    True yapılır. Pipeline DB kaydı buna bakar — id() hilesi yok.
    """

    ozet: Ozet
    teknik_dogruluk: int
    turkce_kalitesi: int
    ozet_netligi: int
    aciklama: str
    input_tokens: int
    output_tokens: int
    model: str
    yayinlandi: bool = field(default=False)

    @property
    def ortalama(self) -> float:
        return (self.teknik_dogruluk + self.turkce_kalitesi + self.ozet_netligi) / 3.0

    @property
    def maliyet_usd(self) -> float:
        # Fiyatlar 2026 Nisan itibarıyla docs.claude.com/pricing'den:
        #   Sonnet 4.5: $3 / 1M input, $15 / 1M output
        #   Haiku 4.5:  $1 / 1M input,  $5 / 1M output
        if "haiku" in self.model.lower():
            return (self.input_tokens * 1.0 + self.output_tokens * 5.0) / 1_000_000
        return (self.input_tokens * 3.0 + self.output_tokens * 15.0) / 1_000_000


async def puanla_tek(
    client: anthropic.AsyncAnthropic,
    ozet: Ozet,
    model: str | None = None,
    semaphore: asyncio.Semaphore | None = None,
) -> Puan:
    """Tek bir özeti puanlar. Semaphore varsa concurrency limiti uygular."""
    model = model or os.environ.get("EVALUATOR_MODEL", "claude-haiku-4-5")

    async def _call():
        return await client.messages.create(
            model=model,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            tools=[PUANLAMA_TOOL],
            tool_choice={"type": "tool", "name": "ozeti_puanla"},
            messages=[{
                "role": "user",
                "content": (
                    f"BAŞLIK: {ozet.haber.baslik}\n\n"
                    f"ÖZET: {ozet.metin}"
                ),
            }],
        )

    if semaphore is not None:
        async with semaphore:
            resp = await _call()
    else:
        resp = await _call()

    # tool_use bloğunu bul
    tool_block = next(
        (b for b in resp.content if b.type == "tool_use"), None
    )
    if tool_block is None:
        # Güvenli düşüş — tool çağrısı başarısız, nötr puan (eşik geçmez)
        log.warning("[evaluator] tool_use yok: %s", ozet.haber.baslik[:60])
        return Puan(
            ozet=ozet,
            teknik_dogruluk=5, turkce_kalitesi=5, ozet_netligi=5,
            aciklama="Puanlama başarısız, varsayılan nötr puan.",
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            model=model,
        )

    args = tool_block.input
    return Puan(
        ozet=ozet,
        teknik_dogruluk=args["teknik_dogruluk"],
        turkce_kalitesi=args["turkce_kalitesi"],
        ozet_netligi=args["ozet_netligi"],
        aciklama=args["aciklama"],
        input_tokens=resp.usage.input_tokens,
        output_tokens=resp.usage.output_tokens,
        model=model,
    )


async def puanla_toplu(ozetler: list[Ozet], model: str | None = None) -> list[Puan]:
    """Paralel puanlama — orchestrator-workers + semaphore concurrency limit.

    Tek AsyncAnthropic client; asyncio.Semaphore ile aynı anda en fazla
    `_CONCURRENCY` çağrı açık tutulur (rate limit + connection pool koruması).
    """
    client = anthropic.AsyncAnthropic()
    sem = asyncio.Semaphore(_CONCURRENCY)
    tasks = [puanla_tek(client, o, model, semaphore=sem) for o in ozetler]
    return await asyncio.gather(*tasks)
