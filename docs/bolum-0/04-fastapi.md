# 0.4 FastAPI İskeleti

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~25 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 0.2 bitmiş — `venv` aktif, `pip install` çalışıyor; terminal + tarayıcı aynı anda açık</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Kendi makinende çalışan bir **FastAPI** servisi kurarsın; `GET /` + `POST /echo` endpoint'leri yanıt verir; tarayıcıda `http://localhost:8000/docs` sayfasına girip **otomatik dokümantasyonu** görürsün; `curl` ile HTTP POST atıp JSON cevap alırsın.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    Bu sayfadaki **kalın** teknik terimler (endpoint, route, JSON, ASGI gibi) ilk geçişte hemen yanında veya altında Türkçe açıklanır.

## Neden bu sayfa?

Bir AI servisi yazdın diyelim. `python chatbot.py` çalışıyor, soru soruyorsun, cevap veriyor. Güzel. Ama **sadece senin terminalinde.** Tarayıcıdan kullanmak isteyen? Mobil uygulamadan çağırmak isteyen? Başka servis entegrasyonu? Hepsine **HTTP arayüzü** lazım. FastAPI bunu 15 satırla açar.

İkincisi: Bölüm 9'da servisi canlıya vereceksin. Canlı servis = **HTTP üstünden konuşulan bir şey.** Docker image'ına koyacaksın, nginx'in arkasına atacaksın, bir domain'e bağlayacaksın — hepsi HTTP varsayar. Bugün öğrendiğin 15 satır, 9. Bölüm'de 3 kıta arasında çalışacak.

Üçüncüsü: FastAPI **Python ekosisteminin altın standardı** oldu (2020'den beri). Tip ipuçlarıyla (type hints) otomatik doğrulama, Swagger UI (API'nın etkileşimli dokümantasyon sayfası) otomatik, asenkron çağrı varsayılan, **hız**: Django + Flask'tan belirgin üstün. Anthropic'in kendi [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) deposundaki "deployment" örneklerinin çoğu FastAPI ile yazılmış. Bu beceri iş ilanlarında da sık aranır.

## FastAPI kısaca — üç paragraf, matematiksiz

**FastAPI = Python'da HTTP API kurmanın modern yolu.** `@app.get("/")` **dekoratörü** (bir fonksiyonun üstüne yerleştirip ona ek özellik veren Python işareti) ile bir fonksiyonu URL'e bağlıyorsun. Fonksiyon ne döndürürse, FastAPI onu **otomatik JSON'a çeviriyor.** Sen `return {"mesaj": "merhaba"}` yazıyorsun, tarayıcı `{"mesaj":"merhaba"}` alıyor.

**`POST` için Pydantic modelleri var.** `class Soru(BaseModel): mesaj: str` yazıyorsun — FastAPI bu şemayı anlıyor, gelen JSON'u doğruluyor (eksik alan = otomatik hata), sonra fonksiyonuna temiz bir `Soru` nesnesi veriyor. Sen kendin yazsaydın 20 satır **doğrulama (validasyon)** kodu çıkardı; FastAPI bunu otomatik yapıyor.

**`uvicorn` sunucu, FastAPI ise çerçeve (framework).** `uvicorn main:app --reload` komutu uygulamayı başlatır, `--reload` sen kodu değiştirdikçe otomatik yeniler. Varsayılan port `8000`. Tarayıcıdan `http://localhost:8000/docs` → **Swagger UI** (API'nın etkileşimli dokümantasyon sayfası) otomatik açılır, her uç noktayı (endpoint) tarayıcıdan test edebilirsin. Postman gerekmez.


## Flask / Django / FastAPI — hangisi ne zaman

| Kıstas | Flask | Django | FastAPI |
|---|---|---|---|
| **Öğrenme eğrisi** | Düşük | Yüksek | Orta |
| **Async desteği** | Eklenti ile | Django 4.1+ kısmi | Native (`async def`) |
| **Otomatik dokümantasyon** | Yok | Yok | Swagger + ReDoc |
| **Pydantic validasyon** | Yok | Form-based | Built-in |
| **AI servisi için** | Basit script | Admin paneli şartsa | **Tercih** |

> **Sonuç:** Bu platformda FastAPI kullanacağız. Anthropic cookbook örneklerinin büyük çoğunluğu FastAPI + uvicorn üzerinde; `async def` ve Pydantic, Claude SDK ile doğal uyum içinde çalışıyor.

## Bu sayfanın ekosistemi — kim kime ne veriyor

<div class="ma-ekosistem" markdown>
<div class="ma-ekosistem-header">🗺️ Ekosistem — HTTP isteğinden fonksiyon cevabına</div>

```mermaid
flowchart LR
  BROWSER["🌐 Tarayıcı\nveya curl"]
  UVI["⚡ uvicorn\nASGI sunucu\n:8000"]
  FA["🚀 FastAPI app"]
  ROUTE["🛣️ /echo\nroute"]
  FN["🐍 Python fonksiyon\nmesaji_yansit()"]
  PYD["📋 Pydantic\nSoru modeli"]
  JSON["📦 JSON\ncevap"]

  BROWSER -->|POST /echo\n{'mesaj':'selam'}| UVI
  UVI --> FA
  FA --> ROUTE
  ROUTE --> PYD
  PYD -->|validated| FN
  FN --> JSON
  JSON --> BROWSER

  classDef fw fill:#dbeafe,stroke:#2563eb,color:#111
  classDef logic fill:#fef3c7,stroke:#ca8a04,color:#111
  class BROWSER,FA,ROUTE fw
  class UVI,FN,PYD,JSON logic
```

<table class="ma-aktorler" markdown>

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 🌐 **Tarayıcı / curl** | Senin makinen | HTTP isteği atar (GET, POST), cevabı alır |
| ⚡ **uvicorn** | Aynı makine, port 8000 | **ASGI sunucu** (asenkron Python web sunucusu) — HTTP isteklerini alır, FastAPI'ye bağlar |
| 🚀 **FastAPI app** | `main.py` dosyası | Route kayıtlarını tutar, gelen isteği doğru fonksiyona yönlendirir |
| 🛣️ **Route** | `@app.post("/echo")` decorator | URL + HTTP metot eşleşmesi |
| 📋 **Pydantic Soru** | `class Soru(BaseModel)` | Gelen JSON'u doğrular — eksik alan varsa otomatik 422 hata |
| 🐍 **Python fonksiyon** | İş mantığın | Asıl işi yapan yerin; LLM çağrısı, DB sorgusu, vs. |
| 📦 **JSON cevap** | `return {...}` | FastAPI otomatik JSON'a serialize eder |

</table>
</div>

## Uygulama — iki yol

### Yol A — İlk FastAPI iskeletin (15 satır)

```bash
# venv aktif olmalı, 0.2'den hatırla
# Nisan 2026: fastapi 0.136.1 + uvicorn 0.34+
pip install "fastapi[standard]"
```

`main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ilk Servisim", version="0.1")


class Soru(BaseModel):
    mesaj: str
    kullanici: str = "misafir"  # default değer, opsiyonel


@app.get("/")
def kok():
    return {"durum": "ayakta", "mesaj": "FastAPI calisiyor"}


@app.post("/echo")
def mesaji_yansit(soru: Soru):
    return {
        "aldim": soru.mesaj,
        "senden": soru.kullanici,
        "karakter_sayisi": len(soru.mesaj),
    }
```

Çalıştır:

```bash
uvicorn main:app --reload
```

Beklenen çıktı (terminal):

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

Test 1 — tarayıcıdan GET:

```
http://localhost:8000/
→ {"durum":"ayakta","mesaj":"FastAPI calisiyor"}
```

Test 2 — **Swagger UI otomatik dokümantasyon**:

```
http://localhost:8000/docs
```

Burada 2 endpoint görürsün (`GET /` ve `POST /echo`). `POST /echo`'yu aç → "Try it out" → JSON gir → "Execute". Tarayıcıdan test ettin, Postman gerekmedi.

Test 3 — **curl ile POST** (yeni terminal aç, venv aktive et):

```bash
curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"mesaj":"Merhaba FastAPI", "kullanici":"Kemal"}'
```

Beklenen çıktı:

```json
{"aldim":"Merhaba FastAPI","senden":"Kemal","karakter_sayisi":15}
```

**Burada olan nedir (diyagram referansı):** curl → uvicorn (:8000) → FastAPI app → `/echo` route → Pydantic `Soru` doğrulaması → `mesaji_yansit` fonksiyonu → JSON cevap → curl'e döndü. Diyagramın tüm akışı 15 satır kodda çalıştı.

### Yol B — Hata yönetimi + async + path parameter

İlk olarak `httpx` paketini kur:

```bash
pip install httpx
```

Sonra `main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Biraz Daha Pro", version="0.2")


class Soru(BaseModel):
    mesaj: str


@app.post("/echo/{dil}")
async def echo_dilli(dil: str, soru: Soru):
    """
    Dil parametresi URL'den geliyor (path parameter).
    async fonksiyon — LLM çağrısı gibi I/O işler için gerekli.
    """
    izin_verilen = {"tr", "en", "de"}
    if dil not in izin_verilen:
        raise HTTPException(
            status_code=400,
            detail=f"Dil '{dil}' desteklenmiyor. Seçenekler: {izin_verilen}",
        )

    # Örnek async iş — gerçek projede burada Claude/Ollama çağrısı olur
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(f"https://httpbin.org/anything?dil={dil}")
        http_durum = r.status_code

    return {
        "dil": dil,
        "mesaj": soru.mesaj,
        "test_durumu": http_durum,
    }
```

Test:

```bash
# Başarılı
curl -X POST http://localhost:8000/echo/tr \
  -H "Content-Type: application/json" \
  -d '{"mesaj":"merhaba"}'

# Hata — desteklenmeyen dil
curl -X POST http://localhost:8000/echo/fr \
  -H "Content-Type: application/json" \
  -d '{"mesaj":"merhaba"}'
```

Beklenen:

```json
// İlk çağrı
{"dil":"tr","mesaj":"merhaba","test_durumu":200}

// İkinci çağrı
{"detail":"Dil 'fr' desteklenmiyor. Seçenekler: {'tr', 'en', 'de'}"}
// HTTP 400 status code ile
```

**Burada olan nedir (diyagram referansı):** Path parameter (`{dil}`) URL'den geliyor, Pydantic `Soru` body'den geliyor. `async` + `httpx` = Claude/Ollama gibi I/O-ağır çağrılar için **doğru desen.** Bu 0.5'in temeli.

### Servisi durdur / tekrar başlat

```bash
# Durdur: terminalde Ctrl+C
# Başlat: uvicorn main:app --reload
# Farklı port: uvicorn main:app --reload --port 8080
# Başka makineden erişim (dikkatli!): uvicorn main:app --host 0.0.0.0
```

**Önemli:** `--host 0.0.0.0` = "dış dünyadan erişilebilir" demek. **Yerel** geliştirmede `127.0.0.1` (varsayılan) kal. VPS'te servis açarken nginx ters vekil sunucu (reverse proxy) kullan (Bölüm 9).

??? warning "Tipik FastAPI hataları — şu mesaj çıkarsa şu çözüm"

    | Hata | Sebep | Çözüm |
    |---|---|---|
    | `[Errno 48] Address already in use` | 8000 portu meşgul | Farklı port: `uvicorn main:app --port 8001`; ya da `lsof -i:8000` ile süreç bul, `kill <pid>` |
    | Tarayıcıda `/docs` 404 | Uygulama ayağa kalkmadı veya yanlış URL | Terminal log'una bak: "Application startup complete" görmelisin; URL `localhost:8000/docs` olmalı |
    | `422 Unprocessable Entity` | Body şeması eksik/yanlış | Pydantic hata mesajındaki `loc` alanına bak — eksik veya yanlış alan adını gösterir |
    | `--reload` reload etmiyor | Uygulama dışı dosyada değişiklik var | `--reload-dir` ile dizin ekle veya manuel restart |
    | `ImportError: cannot import name 'FastAPI'` | Paket kurulmamış / yanlış venv | `pip list | grep fastapi` kontrol et; venv aktif değilse aktive et |

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu konuyu nasıl anlatıyor — öz</div>

Anthropic FastAPI'yi **resmi olarak önermez** — Python web framework'u seçimi sana kalmış. Ama Anthropic'in kendi örneklerinde ve cookbook'ta FastAPI **en sık gördüğün framework.**

**1. Cookbook örnekleri FastAPI tabanlı.** [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) repo'sundaki deploy ve tool use notebook'larının çoğu FastAPI + uvicorn ile. "Claude'u production'a nasıl koyarım" sorusuna Anthropic'in örtük cevabı bu.

**2. Claude SDK async-friendly.** Anthropic Python SDK `AsyncAnthropic` sınıfı ile gelir. FastAPI `async def` endpoint'leriyle mükemmel uyumlu — aynı event loop, aynı dosya. Blocking `time.sleep` değil, `await client.messages.create(...)` = doğru desen.

**3. Pydantic + Claude structured output.** Claude'un tool use cevapları JSON Schema'ya uygun gelir; FastAPI'nin Pydantic modelleri aynı ekosistem (JSON Schema standardı). Claude'dan gelen structured data'yı direkt Pydantic model'e döküp doğrulamak yaygın desen. Bölüm 6'da detay.

??? info "Teknik detay — isteyene (parameter adları, mekanikler, edge case'ler)"

    **ASGI ile WSGI farkı.** `uvicorn` ASGI (Asenkron Sunucu Ağ Geçidi Arayüzü) tabanlı — FastAPI için ideal. Flask/Django eski WSGI üstünde çalışır; bu yüzden asenkron çağrıyı doğal olarak yapamazlar. Farkı bilmek FastAPI'nin neden hızlı olduğunu anlatır.

    **Bağımlılık enjeksiyonu (dependency injection).** FastAPI'nin `Depends()` sistemi — kimlik doğrulama (auth), veritabanı bağlantısı, Claude istemcisi gibi bağımlılıkları fonksiyon imzasında bildiriyorsun. Test edilebilirlik çok yüksek. Bölüm 9'da detay.

    **Arka plan görevleri (background tasks).** `BackgroundTasks` — HTTP cevabı döndükten sonra arka planda iş yaptırma (log yazma, webhook gönderme). Kullanıcı beklemiyor, iş arka planda.

    **Ara katman (middleware).** Tarayıcı uyumluluğu (CORS), kimlik doğrulama, istek sınırı (rate limit) — bunlar isteğin önüne eklenen filtre katmanlarıdır. `app.add_middleware(CORSMiddleware, ...)`.

    **OpenAPI şeması.** FastAPI otomatik OpenAPI 3.0 şeması üretir — `http://localhost:8000/openapi.json`. Bu standart sayesinde Claude'a "şu OpenAPI'ye uygun isteği yaz" demek mümkün. Ajanlarda güçlü bir desen.

    **Üretim için uvicorn.** Geliştirmede `--reload`, **canlıda** `uvicorn main:app --workers 4` (modern uvicorn 0.30+ doğrudan çoklu süreç destekler — eski `gunicorn -w 4 -k uvicorn.workers.UvicornWorker` deseni artık gereksiz). Worker sayısı genelde CPU çekirdek sayısının 2 katı civarı. Tek süreç yetmez.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [FastAPI resmi dokümanı](https://fastapi.tiangolo.com/) (EN, Türkçe çevirisi var). Başlangıç için birebir rehber. Pekiştirme: [claude-cookbooks/tool_use/customer_service_agent.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/tool_use/customer_service_agent.ipynb) — Claude tool use üretim deseni; FastAPI'ye taşımak için doğal örnek.
</div>
</div>

<div class="ma-cikti-kaniti" markdown>
### 📦 Bu sayfayı bitirdiğini nasıl kanıtlarsın

#### 1. 📝 Refleksiyon yazısı — 5 dakika

> "FastAPI kurdum. `GET /` cevabı: [şu]. `POST /echo` ile [şunu] gönderdim, [şunu] aldım. `/docs` sayfası [şöyle] göründü. Async + hata yönetimi denemem: [başarılı / takıldığım yer şu]. Bu iskeleti 0.5'te Ollama'ya bağlayacağım."

Kaydet: `muhendisal-notlarim/bolum-0/04-fastapi/refleksiyon.txt`

#### 2. 📸 Ekran görüntüsü — 3 dakika

**Neyin görüntüsü:** Tarayıcıda `http://localhost:8000/docs` sayfası — Swagger UI açık, 2 endpoint görünür.

| OS | Kısayol | Kayıt |
|---|---|---|
| Windows | `Win + Shift + S` | Paint → PNG |
| Mac | `Cmd + Shift + 4` | Masaüstü |
| Linux | `Shift + PrtScr` | Resimler |

Kaydet: `muhendisal-notlarim/bolum-0/04-fastapi/swagger.png`

#### 3. 💻 Kendi servisin + GitHub — 10 dakika

`main.py`'ye **kendi bir endpoint'in** ekle (örn: `POST /selamla` → isim alsın, kişiye özel selam dönsün). `requirements.txt` güncelle (`pip freeze > requirements.txt`). GitHub repo'ya commit + push. README'ye kurulum + örnek curl ekle.

Repo linkini kaydet: `muhendisal-notlarim/bolum-0/04-fastapi/repo-link.txt`

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**Python fonksiyonu dışarıdan çağrılamaz.** Terminal script = sadece sen çalıştırıyorsun. Bu yüzden **araya HTTP arayüzü (FastAPI) gerek.**</li>
<li>**FastAPI decorator = URL bağlama.** `@app.post(...)` = fonksiyonu HTTP endpoint'e bağlayan tek satır. Bu yüzden **routing kodu yazmıyorsun.**</li>
<li>**Pydantic = otomatik validasyon.** Gelen JSON şemasını tanımlıyorsun. Bu yüzden **20 satır doğrulama kodu yazmıyorsun.**</li>
<li>**uvicorn ASGI = bloklanmayan event loop.** LLM çağrısı I/O-ağır, async yapı şart. Bu yüzden **eş zamanlı birden fazla kullanıcıya cevap verebiliyorsun.**</li>
<li>**`/docs` = ücretsiz dokümantasyon.** FastAPI OpenAPI schema otomatik üretiyor. Bu yüzden **Postman yerine tarayıcıdan test ediyorsun.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** "Python'da LLM çağırdım" ile "Python'da HTTP servisi açıp LLM çağırdım" arasında 10x kariyer farkı var. İkincisi production, birincisi script. Bu sayfa o atlamayı verdi. 0.5'te Ollama (0.3) ve FastAPI (0.4) birleşecek = uçtan uca AI servisi.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[0.5 İlk AI Servisi →](05-ilk-ai-servisi.md)** — Ollama (0.3) + FastAPI (0.4) = `POST /chat` endpoint'i. curl → FastAPI → Ollama → cevap → kullanıcı. Bölüm 0'ın kapanışı, gerçek bitiş çizgisi.

← [0.3 Ollama ile Yerel LLM](03-ollama.md) &nbsp;|&nbsp; [Bölüm 0 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** FastAPI Türkçe tutorial'ı birebir takip et: [fastapi.tiangolo.com/tr](https://fastapi.tiangolo.com/tr/). 30 dakika + örnekler = bu sayfanın 3 katı derinlik. Sonraki bölümlerde sana geri dönüşü büyük.
</div>
