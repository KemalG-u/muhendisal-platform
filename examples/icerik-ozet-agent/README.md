# İçerik Özet Agent'ı — Referans Proje

Türkçe AI haberlerini günlük tarayıp özetleyen **multi-agent içerik pipeline'ı**. MühendisAl Bölüm 6'da işlenen agent + tool + multi-agent + SDK kararlarının **tek bir çalışan projede** buluşması. 4–6 haftalık bir AI Engineer adayı bunu okuyup kendi varyantını deploy edebilmeli.

## Ne yapar

1. **Radar agent** — belirlediğin haber kaynaklarını (RSS / HTML) tarar, son 24 saatin başlıklarını toplar.
2. **Yazar agent** — her başlık için 2–3 cümlelik **Türkçe özet** üretir (Claude Sonnet 4.5).
3. **Evaluator agent** — her özeti **kalite kriterlerine** göre 0–10 puanlar (evaluator-optimizer pattern, Bölüm 6.5).
4. **Publisher** — eşik üstü özetleri bir **markdown rapor** dosyasına yazar (`reports/YYYY-MM-DD.md`) + opsiyonel email.
5. **Tüm taslak + puan + yayın durumu** SQLite'a kaydedilir — ilerde feedback loop eklenebilir.

## Neden bu mimari

Bölüm 6.1 kontrol listesinde bu görev **kreatif + paralel + kalite-kritik** — workflow yetmez, tek agent yorulur. 6.5'teki **orchestrator-workers + evaluator-optimizer** hibrit deseni uygun. SDK seçimi 6.7 karar matrisine göre **ham `anthropic` SDK** — chat/content ağırlıklı, her token görünür olsun, framework overhead'i istemiyoruz.

## Kurulum (5 dakika)

```bash
git clone <bu-repo>
cd icerik-ozet-agent

# uv yoksa: https://docs.astral.sh/uv/#installation
uv sync                 # pyproject.toml'daki bağımlılıklar

cp .env.example .env
# .env içine ANTHROPIC_API_KEY gir (zorunlu)
# FIRECRAWL_API_KEY opsiyonel — yoksa demo RSS feed kullanılır
```

## Çalıştırma

```bash
# Tek seferlik tarama + özet + yayın
uv run python pipeline.py

# Sadece son raporu konsola dök
uv run python pipeline.py --show-last

# Pytest — agent'ları ayrı ayrı dene
uv run pytest
```

Çıktı:

```
[radar] 12 başlık bulundu (son 24 saat)
[yazar] 12 özet üretildi — toplam 3.847 output token
[evaluator] 12 özet puanlandı — ortalama 7.3/10
[publisher] 9 özet rapora yazıldı (eşik: 6.5)
[db] 12 kayıt kaydedildi — rapor: reports/2026-04-22.md
[maliyet] toplam: $0.0412 (Claude Sonnet 4.5)
```

## Klasör yapısı

```
icerik-ozet-agent/
├── README.md
├── .env.example
├── pyproject.toml
├── pipeline.py              # orchestrator — giriş noktası
├── agents/
│   ├── __init__.py
│   ├── radar.py             # haber toplayıcı (RSS + opsiyonel Firecrawl)
│   ├── yazar.py             # özet üretici (Claude)
│   ├── evaluator.py         # kalite puanlayıcı (ikinci Claude geçişi)
│   └── publisher.py         # markdown + email yayıncı
├── db/
│   └── schema.sql           # taslaklar + puanlar + yayın durumu
├── reports/                 # günlük rapor çıktıları (git-ignored)
└── tests/
    ├── __init__.py
    └── test_pipeline.py     # her agent için birim test
```

## Öğrenme hedefleri (Bölüm 6 uygulaması)

| Bölüm 6 konsepti | Bu projedeki uygulaması |
|---|---|
| 6.1 Agent vs workflow | Kreatif + paralel + kalite-kritik → agent doğru |
| 6.2 Tool calling | `radar.py` içinde `@tool`'suz raw HTTP — tool gereksiz bu görevde |
| 6.5 Orchestrator-workers | `pipeline.py` → `asyncio.gather` ile yazar+evaluator paralel |
| 6.5 Evaluator-optimizer | `evaluator.py` → puan < eşik ise publisher filtreler |
| 6.7 SDK seçimi | Ham `anthropic` — framework yok, her token elinde |
| Maliyet görünürlüğü | Her agent `response.usage` loglar — `pipeline.py` toplar |
| HITL (opsiyonel) | Publisher'da `--dry-run` bayrağı — insan gözü seçer |

## Geliştirme önerileri (öğrencinin genişletme rotası)

1. **Feedback loop** — publisher yayın sonrası okuyucu tepkisi toplasın (email reply, web form). Puanlama istatistikleriyle `yazar.py` system prompt'u otomatik güncellensin.
2. **Multi-provider** — `anthropic:claude-sonnet-4-5` yanına `openai:gpt-5-mini` alternatif ekle; aynı görev iki LLM'de, çıktı karşılaştır. Bu noktada **LangChain `create_agent`** anlamlı (Bölüm 6.7).
3. **MCP server paketle** — `radar` ve `publisher` tool'larını 6.4'teki FastMCP ile bağımsız MCP server yap; Claude Desktop'tan manuel çağrı da mümkün olsun.
4. **Headless deploy** — `claude-agent-sdk` + GitHub Actions cron ile CI üstünde günlük otomasyon (Bölüm 6.6 karar matrisi).
5. **Observability** — OpenTelemetry + Helicone/LangFuse integration.

## Lisans

MIT. İstediğin gibi fork'la, kendi ihtiyacına uyarla.
