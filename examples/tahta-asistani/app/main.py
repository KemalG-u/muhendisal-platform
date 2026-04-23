"""Tahta Asistani - FastAPI multimodal app.

Akis:
  POST /analiz  (multipart: foto.jpg) -> {"ozet", "quiz", "kavramlar"}
  GET  /health
  GET  /
"""
from __future__ import annotations

import base64
import json
import logging
import uuid
from contextlib import asynccontextmanager

import anthropic
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from PIL import Image
from pydantic import BaseModel
from pythonjsonlogger.json import JsonFormatter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

# Logging — structured JSON (Bolum 8.4 pattern)
_handler = logging.StreamHandler()
_handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[_handler])
log = logging.getLogger("tahta-asistani")

MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_MEDIA = {"image/jpeg", "image/png", "image/webp"}


class Kavram(BaseModel):
    ad: str
    aciklama: str


class QuizSorusu(BaseModel):
    soru: str
    secenekler: list[str]
    dogru_index: int
    aciklama: str


class AnalizSonuc(BaseModel):
    istek_id: str
    ozet: str
    kavramlar: list[Kavram]
    quiz: list[QuizSorusu]


# Claude client — Bolum 8.5 pattern (timeout + retry + fallback)
_client = anthropic.Anthropic(timeout=30.0)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
    retry=retry_if_exception_type(
        (
            anthropic.APIConnectionError,
            anthropic.APITimeoutError,
            anthropic.RateLimitError,
            anthropic.InternalServerError,
        )
    ),
    reraise=True,
)
def claude_analiz(image_data: str, media_type: str) -> dict:
    """Claude vision ile tahta foto analiz -> ozet+kavram+quiz JSON."""
    system_prompt = (
        "Sen Turkce bir ders asistanisin. Ogrenciye tahta/not defteri "
        "fotografi verilir; sen kisa ozet, anahtar kavramlar ve 3 quiz "
        "sorusu uretisin. Dil samimi ama ogretmen tonunda, 12-17 yas grubu."
    )

    user_prompt = (
        "Bu tahta/not fotografini analiz et. JSON olarak don:\n\n"
        '{\n'
        '  "ozet": "3-5 cumle Turkce ozet",\n'
        '  "kavramlar": [{"ad": "...", "aciklama": "1 cumle"}],\n'
        '  "quiz": [\n'
        '    {"soru": "...", "secenekler": ["A", "B", "C", "D"],\n'
        '     "dogru_index": 0, "aciklama": "neden dogru"}\n'
        "  ]\n"
        "}\n\n"
        "Kurallar:\n"
        "- 3 kavram (anahtar), 3 quiz sorusu\n"
        "- Quiz sorulari gorseldeki konuyu test etsin\n"
        "- dogru_index 0-3 arasi\n"
        "- Sadece JSON don, baska metin yok"
    )

    response = _client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": user_prompt},
                ],
            }
        ],
    )
    raw = response.content[0].text.strip()
    # JSON fence varsa ayikla
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _resize_if_huge(data: bytes, media: str) -> tuple[bytes, str]:
    """5MB'dan buyukse veya 2048px+ downscale."""
    if len(data) < MAX_IMAGE_BYTES and media in ALLOWED_MEDIA:
        img = Image.open(__import__("io").BytesIO(data))
        if max(img.size) <= 2048:
            return data, media
    # Downscale
    img = Image.open(__import__("io").BytesIO(data))
    img.thumbnail((2048, 2048))
    buf = __import__("io").BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=85)
    return buf.getvalue(), "image/jpeg"


# Rate limit (Bolum 8.3 pattern)
_limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("tahta-asistani starting")
    yield
    log.info("tahta-asistani stopping")


app = FastAPI(title="Tahta Asistani", lifespan=lifespan)
app.state.limiter = _limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": "claude-sonnet-4-5"}


@app.get("/")
def root() -> dict:
    return {
        "servis": "Tahta Asistani",
        "aciklama": "Tahta fotografi -> ders ozeti + quiz",
        "endpoints": ["/analiz (POST)", "/health"],
    }


@app.post("/analiz", response_model=AnalizSonuc)
@_limiter.limit("10/minute")
async def analiz(
    request: Request,
    foto: UploadFile = File(...),  # noqa: B008
) -> AnalizSonuc:
    istek_id = uuid.uuid4().hex[:10]

    # Validasyon
    if foto.content_type not in ALLOWED_MEDIA:
        raise HTTPException(400, f"Format desteklenmez: {foto.content_type}")

    data = await foto.read()
    if len(data) > MAX_IMAGE_BYTES * 2:
        raise HTTPException(413, "Dosya 10MB'dan buyuk")

    data, media_type = _resize_if_huge(data, foto.content_type or "image/jpeg")
    b64 = base64.b64encode(data).decode()

    log.info("analiz_basladi", extra={"istek_id": istek_id, "size": len(data)})

    try:
        sonuc = claude_analiz(b64, media_type)
    except anthropic.APIError as e:
        log.error("claude_hata", extra={"istek_id": istek_id, "hata": str(e)})
        raise HTTPException(502, f"Claude API hatasi: {e}") from e
    except json.JSONDecodeError as e:
        log.error("json_parse_hata", extra={"istek_id": istek_id, "hata": str(e)})
        raise HTTPException(500, "Model JSON format disi cevap verdi") from e

    log.info("analiz_tamam", extra={"istek_id": istek_id})

    return AnalizSonuc(
        istek_id=istek_id,
        ozet=sonuc["ozet"],
        kavramlar=[Kavram(**k) for k in sonuc["kavramlar"]],
        quiz=[QuizSorusu(**q) for q in sonuc["quiz"]],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
