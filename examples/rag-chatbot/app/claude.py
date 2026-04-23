"""Claude Sonnet 4.5 ile streaming cevap + kaynak-gösterme."""
from __future__ import annotations

import os
from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """Sen bir RAG asistanısın. Kullanıcının sorusuna SADECE verilen
kaynak parçalarına dayanarak cevap ver. Kaynak dışı bilgi kullanma.

Kurallar:
1. Cevabını kaynaklara dayandır; her iddiada ilgili kaynak numarasını köşeli
   parantezde belirt, örnek: [1], [2].
2. Kaynaklar soruya yeterli cevap vermiyorsa açıkça söyle: "Verilen kaynaklarda
   bu sorunun cevabı yok."
3. Kısa, net ol. Türkçe cevap ver.
4. Halüsinasyon yok — emin değilsen söyleme.
"""


def build_user_prompt(question: str, sources: list[dict]) -> str:
    """Kaynakları numaralandır, sonuna soruyu ekle."""
    lines = ["Kaynaklar:\n"]
    for i, src in enumerate(sources, start=1):
        lines.append(
            f"[{i}] ({src['doc_name']}, s.{src['page']}, skor={src['score']})"
        )
        lines.append(src["text"])
        lines.append("---")
    lines.append(f"\nSoru: {question}")
    return "\n".join(lines)


async def stream_answer(
    question: str,
    sources: list[dict],
    client: AsyncAnthropic | None = None,
) -> AsyncIterator[str]:
    """Claude'dan streaming cevap. Client injection test için."""
    if client is None:
        client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    user_content = build_user_prompt(question, sources)

    async with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        async for text in stream.text_stream:
            yield text
