# İçerik Özet Agent'ı — Referans Proje

> MühendisAl **Bölüm 6** (AI Agents ve MCP) kapanış referans projesi.
> **Ücretsiz, MIT lisanslı, çalışır durumda.** 4–6 haftalık bir AI Engineer öğrencisi klonlayıp kendi varyantını 1–2 saatte deploy eder.

Türkçe AI haberlerini günlük tarayıp özetleyen **multi-agent içerik pipeline**. Bölüm 6'da işlenen agent + tool + multi-agent + SDK kararlarının **tek bir çalışan projede** buluşması.

## Ne yapar

1. **Radar** — belirlediğin RSS kaynaklarını tarar, son 24 saat AI haberlerini toplar
2. **Yazar** — her başlık için 2–3 cümlelik **Türkçe özet** üretir (Claude Sonnet 4.5)
3. **Evaluator** — her özeti **3 kritere göre** 0–10 puanlar (evaluator-optimizer pattern, Bölüm 6.5)
4. **Publisher** — eşik üstü özetleri markdown rapor dosyasına yazar (`reports/YYYY-MM-DD.md`) + opsiyonel email
5. **SQLite** — tüm taslak + puan + yayın durumu `db/taslaklar.db`'ye kaydedilir (ileride feedback loop için hazır)

## Neden bu mimari

| Bölüm 6 kararı | Bu projede karşılığı |
|---|---|
| **6.1** Agent vs workflow | Kreatif + paralel + kalite-kritik → agent + multi-skill doğru |
| **6.2** Tool calling | Evaluator'da structured output (`tool_choice="tool"`, garanti JSON) |
| **6.5** Orchestrator-workers | `pipeline.py` → asyncio.gather ile yazar + evaluator paralel |
| **6.5** Evaluator-optimizer | `evaluator.py` → eşik altı filtrelenir |
| **6.5** Heterojen model | Yazar Sonnet (kalite) + Evaluator Haiku (ucuz, yeterli) — maliyet ~%70 düşer |
| **6.7** Ham `anthropic` SDK | Framework yok, her token elinde — chat/content için doğru seçim |
| **Maliyet şeffaflığı** | Her agent `response.usage` loglar; publisher rapor footer'ına yazar |
| **Rate limit koruması** | `asyncio.Semaphore(MAX_CONCURRENCY)` — paralelliği sınırlar |

## Kurulum (5 dakika)

```bash
git clone <bu-repo>
cd icerik-ozet-agent

# uv yoksa: https://docs.astral.sh/uv/#installation
uv sync --extra dev         # bağımlılıklar + dev tools (pytest, ruff)

cp .env.example .env
# .env içine ANTHROPIC_API_KEY gir (zorunlu)
# FIRECRAWL_API_KEY, SMTP_* opsiyonel
```

## Çalıştırma

```bash
# Tek seferlik tarama + özet + yayın
uv run python pipeline.py

# Yayınlamadan sadece konsolda göster
uv run python pipeline.py --dry-run

# Kalite eşiğini yükselt
uv run python pipeline.py --esik 7.5

# Son raporu konsola dök
uv run python pipeline.py --show-last

# Testleri koştur (gerçek API çağrısı yok, mock)
uv run pytest

# Lint
uv run ruff check
```

Örnek çıktı:

```
14:32:07 [pipeline] [radar] Son 24 saat taranıyor...
14:32:09 [pipeline] [radar] 12 başlık bulundu
14:32:09 [pipeline] [yazar] 12 özet paralel üretiliyor...
14:32:18 [pipeline] [yazar] tamam — 3847 output token, $0.0577
14:32:18 [pipeline] [evaluator] 12 özet puanlanıyor...
14:32:24 [pipeline] [evaluator] tamam — ortalama 7.3/10, $0.0089
14:32:24 [publisher] 9 özet rapora yazıldı: reports/2026-04-22.md
14:32:24 [pipeline] [db] 12 kayıt taslaklar tablosuna eklendi
14:32:24 [pipeline] [maliyet] toplam: $0.0666
```

## Test çıktısı

```
$ uv run pytest -v
=============== test session starts ================
collected 9 items

tests/test_pipeline.py::test_anahtar_kelime_listesi_ai_terimlerini_icerir PASSED
tests/test_pipeline.py::test_haber_dataclass_alanlari                    PASSED
tests/test_pipeline.py::test_ozetle_tek_mock                             PASSED
tests/test_pipeline.py::test_ozet_maliyet_hesabi                         PASSED
tests/test_pipeline.py::test_haiku_daha_ucuz                             PASSED
tests/test_pipeline.py::test_puanla_tek_mock                             PASSED
tests/test_pipeline.py::test_puanla_tool_use_yoksa_notr_puan             PASSED
tests/test_pipeline.py::test_rapor_yaz_esik_filtresi                     PASSED
tests/test_pipeline.py::test_rapor_yaz_bos_liste                         PASSED

============== 9 passed in 0.39s ==================
```

## Klasör yapısı

```
icerik-ozet-agent/
├── README.md                # bu dosya
├── .env.example             # env şablonu (kendi .env'ini oluştur)
├── .gitignore               # .env, db, reports git-ignore
├── pyproject.toml           # uv + bağımlılık + pytest + ruff config
├── pipeline.py              # orchestrator — giriş noktası
├── agents/
│   ├── __init__.py
│   ├── radar.py             # haber toplayıcı (RSS + opsiyonel Firecrawl)
│   ├── yazar.py             # özet üretici (Claude Sonnet)
│   ├── evaluator.py         # kalite puanlayıcı (Claude Haiku, structured output)
│   └── publisher.py         # markdown + email yayıncı
├── db/
│   └── schema.sql           # taslaklar + geri_bildirim (gelecek) tablo şeması
├── reports/                 # günlük rapor çıktıları (git-ignored)
└── tests/
    ├── __init__.py
    └── test_pipeline.py     # 9 birim test (mock, gerçek API yok)
```

## Maliyet hesabı

Günde 20 başlık, her biri ~500 input + ~150 output token:

- **Yazar** (Sonnet 4.5): 20 × (500 × $3 + 150 × $15) / 1M ≈ **$0.075/gün**
- **Evaluator** (Haiku 4.5): 20 × (200 × $1 + 70 × $5) / 1M ≈ **$0.011/gün**
- **Aylık toplam:** ~**$2.60** (6.5 kopya kahve)

Heterojen model kullanılmasa (ikisi de Sonnet): ~$4.20/ay — **%38 tasarruf.** Bölüm 6.5 maliyet optimizasyonunun somut karşılığı.

## Genişletme rotası (öğrencinin sonraki adımları)

| Genişletme | Bölüm 6 köprüsü | Tahmini iş |
|---|---|---|
| 1. **Feedback loop** — publisher'dan okuyucu tepkisi topla, `yazar.py` system prompt'unu otomatik güncelle | 6.5 evaluator-optimizer (kapalı döngü) | 1–2 gün |
| 2. **Multi-provider** — `create_agent` ile aynı görevi OpenAI/Gemini'de de çalıştır, karşılaştır | 6.7 LangChain `create_agent` | 3–4 saat |
| 3. **MCP server paketle** — `radar`'ı 6.4'teki FastMCP ile bağımsız MCP server yap | 6.4 MCP Server | 1 gün |
| 4. **Headless deploy** — GitHub Actions cron ile CI üstünde günlük otomasyon | 6.6 `claude-agent-sdk` | 2–3 saat |
| 5. **Observability** — OpenTelemetry + Helicone/LangFuse | 6.5 prod multi-agent | 1 gün |

## Lisans

MIT — istediğin gibi fork'la, kendi ihtiyacına uyarla, projelere entegre et.

---

**Sorular:** MühendisAl Bölüm 6 — [wiki.oluk.org/platform/bolum-6/](https://wiki.oluk.org/platform/bolum-6/)
