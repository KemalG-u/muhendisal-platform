# Tahta Asistani

**Multimodal AI asistanı** — öğretmen tahta fotoğrafı çeker, uygulama Claude vision ile analiz eder: **ders özeti + 3 anahtar kavram + 3 quiz sorusu**. MühendisAl platform Bölüm 9.6 İMZA projesi.

## Ne işe yarar

Öğretmen dersin sonunda tahtayı fotoğraflar → bu uygulama **30 saniyede**:
- 3-5 cümle ders özeti (Türkçe)
- 3 anahtar kavram (ad + tanım)
- 3 çoktan seçmeli quiz sorusu (açıklamalı)

Öğrenci dersin tekrarı + kontrol sınavı hazır. Öğretmen akşam kendi notlarını doldurmaz.

## Stack

- **FastAPI** + **uvicorn** — web servisi
- **Claude Sonnet 4.5 vision** — görsel analiz (Bölüm 7.1)
- **Pillow** — image validasyon + downscale
- **Pydantic** — input/output şema
- **slowapi** — rate limit (10 req/min)
- **Tenacity** — Claude API retry + jitter (Bölüm 8.5)
- **structured JSON log** — observability (Bölüm 8.4)

## Kurulum

```bash
git clone <repo>
cd examples/tahta-asistani
python -m venv venv && . venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# .env dosyasında ANTHROPIC_API_KEY koy
```

## Çalıştırma

```bash
uvicorn app.main:app --reload
# veya Docker
docker compose up --build
```

`http://localhost:8000` — servis açık.

## Kullanım

```bash
# health
curl http://localhost:8000/health

# analiz — tahta fotoğrafı
curl -X POST http://localhost:8000/analiz \
  -F "foto=@tahta.jpg"
```

**Örnek cevap:**

```json
{
  "istek_id": "a3b7c2d1ef",
  "ozet": "Bu derste fotosentez konusu işlendi...",
  "kavramlar": [
    {"ad": "Fotosentez", "aciklama": "Bitkilerin ışık enerjisini..."},
    {"ad": "Klorofil", "aciklama": "Işığı yakalayan yeşil pigment."},
    {"ad": "Glikoz", "aciklama": "Fotosentez sonucu üretilen şeker."}
  ],
  "quiz": [
    {
      "soru": "Fotosentez nerede gerçekleşir?",
      "secenekler": ["Ribozom", "Kloroplast", "Mitokondri", "Golgi"],
      "dogru_index": 1,
      "aciklama": "Kloroplastlar klorofil içerir."
    }
  ]
}
```

## Test

```bash
pytest -v
# 15 test geçiyor
```

## Endpoint'ler

- `GET /` — servis bilgisi
- `GET /health` — sağlık kontrolü
- `POST /analiz` — tahta fotoğrafı analiz (multipart, `foto` field)

## Kısıtlar

- **Format:** JPEG / PNG / WEBP
- **Boyut:** Max 10 MB (5 MB üstü otomatik downscale 2048px)
- **Rate limit:** 10 istek/dakika (IP başı)
- **Claude maliyet:** ~$0.02 per analiz (1500 token input + 500 output)

## Maliyet (öğretmen kullanımı)

- 1 öğretmen × 5 ders/gün × 20 iş günü = **100 analiz/ay**
- Aylık: 100 × $0.02 = **$2/ay**

10 öğretmenlik bir okul için: **$20/ay** — çok ekonomik.

## Production Checklist (Bölüm 8.6 uyumlu)

15 maddeli checklist:

- [x] G1 Prompt: tool-like JSON şeması + sistem prompt kilidi
- [x] G2 PII: tahta fotoğrafında öğrenci yüzü varsa maskele (TODO: prod)
- [x] G3 Secret: `.env` + `.gitignore` + GH Secrets
- [x] M1 Hard cap: Anthropic Console manuel
- [x] M2 Rate limit: slowapi 10/min
- [x] M3 Budget alert: manuel
- [x] O1 Structured log: python-json-logger JsonFormatter
- [x] O2 Metric: `/health` endpoint + log tail
- [x] H1 Retry: tenacity 3 attempt + jitter
- [x] H2 Circuit: tenacity retry yeterli (pybreaker opsiyonel)
- [x] H3 Fallback: Claude hata → 502 + net mesaj
- [x] D1 Docker: multi-stage + non-root user
- [x] D2 CI/CD: `pytest -v` + ruff hazır
- [x] D3 Health: `/health` + Docker HEALTHCHECK

**14/15 ✅** — G2 PII maskeleme production'da eklenir (TODO comment).

## Platform bağlantısı

Bu referans proje **MühendisAl Bölüm 9.6 İMZA** sayfasının kodu.  
Platform: [wiki.oluk.org/platform/bolum-9/06-proje-3/](https://wiki.oluk.org/platform/bolum-9/06-proje-3/)

Kullanılan bölümler:
- Bölüm 7.1 — Claude vision (base64 + prompt engineering)
- Bölüm 8.3 — Rate limit (slowapi)
- Bölüm 8.4 — Structured JSON log
- Bölüm 8.5 — Retry + timeout (tenacity)
- Bölüm 8.6 — Production checklist
- Bölüm 9.1 — Docker multi-stage
- Bölüm 9.2 — Compose yapılandırması

## Lisans

Apache 2.0
