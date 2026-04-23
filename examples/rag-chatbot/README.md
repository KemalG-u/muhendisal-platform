# RAG Chatbot — PDF'inle sohbet et

MühendisAl platformunun **9.4 imza sayfası** için referans proje.
PDF yükle → soru sor → Claude Sonnet 4.5 kaynak chunk göstererek cevaplasın.

## Stack

- **FastAPI 0.136** — async backend, StreamingResponse ile token-token cevap
- **Qdrant 1.17** — self-hosted vector DB, Rust hızı
- **Voyage AI `voyage-3`** — Anthropic'in resmi embedding tavsiyesi
- **Claude Sonnet 4.5** — streaming, kaynak-gösterimli cevap
- **HTMX + Tailwind CDN** — build-yok frontend
- **Docker Compose** — app + qdrant iki servis
- **GitHub Actions** — test + build + GHCR + SSH deploy (9.3 pattern)

## Proje yapısı

```
rag-chatbot/
├── app/
│   ├── main.py              FastAPI endpoint'leri (/upload, /ask, /health)
│   ├── rag.py               Chunk + embed + search mantığı
│   ├── claude.py            Anthropic streaming + kaynak-gösterme
│   ├── templates/           index.html + _answer.html (HTMX)
│   └── static/style.css
├── tests/
│   ├── test_rag.py          Chunk + PDF parse
│   ├── test_claude.py       Prompt builder + mock streaming
│   └── test_api.py          Endpoint tests (TestClient)
├── Dockerfile               Multi-stage, non-root
├── compose.yml              2 servis, Qdrant hiç expose edilmez
├── pyproject.toml           Pin'li bağımlılıklar + ruff + pytest config
└── .github/workflows/deploy.yml
```

## Yerelde çalıştır

```bash
cp .env.example .env
# ANTHROPIC_API_KEY + VOYAGE_API_KEY doldur
docker compose up -d
open http://localhost:8000
```

## Test + lint

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

## Maliyet

- VPS Hetzner CX22 ~4 €/ay
- Domain ~1 €/ay
- Anthropic ~$1–3/ay (kişisel kullanım ~50 soru/gün)
- Voyage AI ~$0.4/ay (50 PDF + 1500 sorgu)
- **Toplam: ~$6–8/ay**

## CTO notları

1. **`input_type` asimetrisi** — `"document"` yüklemede, `"query"` aramada. Karıştırma, retrieval %20-30 düşer.
2. **AsyncAnthropic + streaming** — algılanan hız 6× artar.
3. **Qdrant hiç expose edilmez** — sadece Docker network'ünden erişim. App localhost bind + Caddy HTTPS önünde.
4. **Contextual Retrieval uygulanmadı** — tek-PDF kişisel kullanımda 3× maliyet; [4.8 HBV desenine](https://wiki.oluk.org/platform/bolum-4/08-hbv/) uygun dürüst sapma.
5. **`pyproject.toml` pin'leri** — `==` kritik kütüphaneler, `>=` esnek olanlar. Dependabot açık.

## Lisans

MIT

## Platform bağlantıları

- [9.4 — RAG Chatbot (imza sayfası)](https://wiki.oluk.org/platform/bolum-9/04-proje-1/)
- [9.1 Docker](https://wiki.oluk.org/platform/bolum-9/01-docker/) · [9.2 Cloud](https://wiki.oluk.org/platform/bolum-9/02-cloud/) · [9.3 CI/CD](https://wiki.oluk.org/platform/bolum-9/03-cicd/)
- [Bölüm 4 — RAG](https://wiki.oluk.org/platform/bolum-4/)
