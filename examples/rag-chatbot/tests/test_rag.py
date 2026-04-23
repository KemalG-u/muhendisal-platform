"""RAG pipeline birim testleri — deterministic, mock'suz."""
from __future__ import annotations

import io

from pypdf import PdfWriter

from app.rag import (
    CHUNK_OVERLAP,
    CHUNK_TOKENS,
    Chunk,
    _chunk_text,
    _pdf_to_text_pages,
    pdf_to_chunks,
)


def _make_pdf_bytes(pages_text: list[str]) -> bytes:
    """Test için minimal PDF oluştur. pypdf ile metin eklemek sınırlı;
    testte bos-PDF davranışı ve yapı bütünlüğü kontrolü yapıyoruz."""
    writer = PdfWriter()
    for _ in pages_text:
        writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_chunk_text_empty() -> None:
    assert _chunk_text("") == []
    assert _chunk_text("   ") == []


def test_chunk_text_short() -> None:
    """Küçük metin tek chunk olmalı."""
    out = _chunk_text("bir iki üç dört beş")
    assert len(out) == 1
    assert "bir" in out[0]


def test_chunk_text_overlap() -> None:
    """Büyük metin birden fazla chunk + overlap."""
    words = ["kelime"] * 2000
    text = " ".join(words)
    chunks = _chunk_text(text, chunk_size=200, overlap=20)
    assert len(chunks) > 1
    # Her chunk approx kelime/1.3 ≈ 150 kelime
    assert all(len(c.split()) <= 160 for c in chunks)


def test_chunk_text_respects_constants() -> None:
    """Default parametreler import edildiği haliyle çalışmalı."""
    assert CHUNK_TOKENS == 800
    assert CHUNK_OVERLAP == 100
    out = _chunk_text("a " * 500)
    assert len(out) >= 1


def test_pdf_blank_pages_skipped() -> None:
    """Boş sayfalar (metin yok) atlanmalı."""
    pdf_bytes = _make_pdf_bytes(["", "", ""])  # 3 boş sayfa
    pages = _pdf_to_text_pages(pdf_bytes)
    assert pages == []  # hiç metin yoksa boş liste


def test_pdf_to_chunks_empty_pdf() -> None:
    """Boş PDF → sıfır chunk."""
    pdf_bytes = _make_pdf_bytes(["", ""])
    chunks = pdf_to_chunks(pdf_bytes, doc_name="test.pdf")
    assert chunks == []


def test_chunk_dataclass() -> None:
    """Chunk dataclass yapısı."""
    c = Chunk(id="abc123", text="hello", doc_name="doc.pdf", page=1)
    assert c.id == "abc123"
    assert c.doc_name == "doc.pdf"
    assert c.page == 1


def test_chunk_id_deterministic() -> None:
    """Aynı girdi → aynı ID (hash stabilitesi)."""
    words = "Lorem ipsum dolor sit amet " * 100
    # pdf_to_chunks doğrudan test edemiyoruz (PDF oluşturmak zor),
    # ama chunk ID formülü _chunk_text sonucunda deterministic olmalı.
    chunks1 = _chunk_text(words)
    chunks2 = _chunk_text(words)
    assert chunks1 == chunks2
