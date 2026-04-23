"""Claude prompt builder + stream_answer testleri (mock Anthropic client)."""
from __future__ import annotations

from collections.abc import AsyncIterator
from unittest.mock import MagicMock

import pytest

from app.claude import MAX_TOKENS, MODEL, SYSTEM_PROMPT, build_user_prompt, stream_answer


def test_system_prompt_is_turkish() -> None:
    """SYSTEM_PROMPT Türkçe ve kaynak-gösterme kuralı içermeli."""
    assert "Türkçe" in SYSTEM_PROMPT
    assert "[1]" in SYSTEM_PROMPT
    assert "Halüsinasyon" in SYSTEM_PROMPT


def test_model_and_max_tokens() -> None:
    """Sabit değerler dışarıya açık."""
    assert MODEL.startswith("claude-sonnet-4-5")
    assert MAX_TOKENS == 1024


def test_build_user_prompt_format() -> None:
    """Kaynaklar numaralı + soru sonda."""
    sources = [
        {"doc_name": "a.pdf", "page": 1, "text": "alfa", "score": 0.9},
        {"doc_name": "b.pdf", "page": 2, "text": "beta", "score": 0.8},
    ]
    out = build_user_prompt("test soru?", sources)
    assert "[1]" in out
    assert "[2]" in out
    assert "a.pdf" in out
    assert "alfa" in out
    assert "Soru: test soru?" in out
    # Soru en sonda olmalı
    assert out.rstrip().endswith("test soru?")


def test_build_user_prompt_empty_sources() -> None:
    """Kaynak listesi boşsa da çalışmalı (retrieval erken dönmüş olur)."""
    out = build_user_prompt("soru", [])
    assert "Soru: soru" in out


class _MockStream:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens

    async def __aenter__(self) -> _MockStream:
        return self

    async def __aexit__(self, *a) -> None:
        return None

    @property
    def text_stream(self) -> AsyncIterator[str]:
        async def gen():
            for t in self.tokens:
                yield t
        return gen()


@pytest.mark.asyncio
async def test_stream_answer_with_mock_client() -> None:
    """stream_answer mock client ile token-token verir."""
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    mock_client.messages.stream = MagicMock(
        return_value=_MockStream(["Merhaba", " dünya", "."])
    )

    sources = [{"doc_name": "x.pdf", "page": 1, "text": "içerik", "score": 0.5}]
    collected: list[str] = []
    async for tok in stream_answer("soru?", sources, client=mock_client):
        collected.append(tok)

    assert "".join(collected) == "Merhaba dünya."
    # stream() çağrısı doğru model + max_tokens ile yapıldı mı?
    call_kwargs = mock_client.messages.stream.call_args.kwargs
    assert call_kwargs["model"] == MODEL
    assert call_kwargs["max_tokens"] == MAX_TOKENS
    assert call_kwargs["system"] == SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_stream_answer_passes_sources_in_prompt() -> None:
    """Kaynaklar user message'a eklenmiş olmalı."""
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    mock_client.messages.stream = MagicMock(return_value=_MockStream([""]))

    sources = [{"doc_name": "uniq-doc.pdf", "page": 42, "text": "benzersiz", "score": 1.0}]
    async for _ in stream_answer("test", sources, client=mock_client):
        pass

    call_kwargs = mock_client.messages.stream.call_args.kwargs
    user_msg = call_kwargs["messages"][0]["content"]
    assert "uniq-doc.pdf" in user_msg
    assert "benzersiz" in user_msg
    assert "s.42" in user_msg
