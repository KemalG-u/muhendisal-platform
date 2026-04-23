# Semantic Search — Türkçe Haber Başlığı Arama

MühendisAl platformunun **3.5 imza sayfası** için referans proje.
FastAPI + Qdrant + Voyage AI üçlüsüyle semantic search servisi.

## Stack

- **FastAPI 0.136** (async backend)
- **Qdrant 1.17** (vector DB, self-host)
- **Voyage AI voyage-3** (embedding, Anthropic resmi tavsiyesi)
- **Pydantic 2.10** (validation)
- **Docker Compose** (2 servis, Qdrant hiç expose edilmez)

## Proje yapısı (12 dosya)

```
semantic-search/
├── app/
│   ├── __init__.py
│   ├── engine.py          Haber + upsert + search (3.4 pattern)
│   └── main.py            FastAPI: /ekle, /toplu-ekle, /ara, /health
├── tests/
│   ├── __init__.py
│   ├── test_engine.py     Haber ID + sabitler (5 test)
│   ├── test_upsert_search.py  Mock Qdrant/Voyage (7 test)
│   └── test_api.py        FastAPI TestClient (7 test)
├── Dockerfile             Multi-stage, non-root
├── compose.yml            app + qdrant, env_file required:false
├── pyproject.toml         Pin'li: voyageai + qdrant-client + fastapi
├── .env.example
├── .gitignore
└── .github/workflows/ci.yml  Python 3.12/3.13 matrix
```

## Endpoint'ler

```
GET  /health              sağlık + git SHA
GET  /istatistik          nokta sayısı + boyut
POST /ekle                tek haber (baslik + kategori + kaynak?)
POST /toplu-ekle          liste[Haber] max 500
POST /ara                 sorgu + top_k + kategoriler?
```

## Yerelde çalıştır

```bash
cp .env.example .env
# VOYAGE_API_KEY doldur
docker compose up -d

# Test
curl http://localhost:8000/health

# Bir haber ekle
curl -X POST http://localhost:8000/ekle \
  -H "Content-Type: application/json" \
  -d '{"baslik": "Anthropic Claude 5 tanıtıldı", "kategori": "tek"}'

# Ara
curl -X POST http://localhost:8000/ara \
  -H "Content-Type: application/json" \
  -d '{"sorgu": "AI modelleri gelişmeler", "top_k": 5}'

# Kategori filter ile ara
curl -X POST http://localhost:8000/ara \
  -H "Content-Type: application/json" \
  -d '{"sorgu": "yeni model", "top_k": 3, "kategoriler": ["tek"]}'
```

## Test + lint

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

## 9.4 RAG Chatbot ile fark

| Boyut | 9.4 RAG Chatbot | 3.5 Semantic Search |
|---|---|---|
| Ana amaç | LLM cevap üretimi | Sadece retrieval (kaynak liste) |
| LLM çağrısı | Claude Sonnet 4.5 | **Yok** |
| Input | PDF + soru | Metin (başlık) + sorgu |
| Output | Streaming cevap + kaynaklar | Skorlu liste |
| Maliyet | Claude $1-3/ay + Voyage $0.4 | Sadece Voyage $0.4/ay |
| Öğretme değeri | Tam RAG pipeline | Sadece vector DB akışı |

Semantic search = RAG'in ilk yarısı. Bu proje **retrieval'a odak**; Claude eklenince RAG (Bölüm 4) olur.

## CTO notları

1. **`input_type` asimetrisi** — `upsert_haberler` → `document`, `search` → `query`. 3.1 kuralı.
2. **Deterministik ID** — `Haber.id` SHA-256 tabanlı; aynı başlık + kategori = aynı ID. Idempotent upsert (3.4 pattern).
3. **Qdrant hiç expose edilmez** — `compose.yml` app'i `127.0.0.1:8000` bind, Qdrant sadece Docker network.
4. **`env_file: required: false`** — .env yokken de `docker compose config` geçer.
5. **Lifespan atlatma pattern** — `tests/test_api.py`'de `with TestClient` YOK; state manuel set.

## Lisans

MIT
