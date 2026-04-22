# 0.4 FastAPI İskeleti

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 0.2 bitmiş — `venv` aktif, `pip install` çalışıyor; terminal + tarayıcı aynı anda açık</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Kendi makinende çalışan bir **FastAPI** servisi kurarsın; `GET /` + `POST /echo` endpoint'leri yanıt verir; tarayıcıda `http://localhost:8000/docs` sayfasına girip **otomatik dokümantasyonu** görürsün; `curl` ile HTTP POST atıp JSON cevap alırsın.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    Bu sayfadaki **italik-altı çizili** ifadelerin (endpoint, route, JSON, ASGI gibi) üstüne mouse'unu getir — kısa tanım çıkar. Mobilde dokun.

## Neden bu sayfa?

Bir AI servisi yazdın diyelim. `python chatbot.py` çalışıyor, soru soruyorsun, cevap veriyor. Güzel. Ama **sadece senin terminalinde.** Tarayıcıdan kullanmak isteyen? Mobil uygulamadan çağırmak isteyen? Başka servis entegrasyonu? Hepsine **HTTP arayüzü** lazım. FastAPI bunu 15 satırla açar.

İkincisi: Bölüm 9'da servisi canlıya vereceksin. Canlı servis = **HTTP üstünden konuşulan bir şey.** Docker image'ına koyacaksın, nginx'in arkasına atacaksın, bir domain'e bağlayacaksın — hepsi HTTP varsayar. Bugün öğrendiğin 15 satır, 9. Bölüm'de 3 kıta arasında çalışacak.

Üçüncüsü: FastAPI **Python ekosisteminin altın standardı** oldu (2020'den beri). Type hints ile otomatik validation, Swagger UI otomatik, async default, **hız**: Django + Flask'tan belirgin üstün. Anthropic'in kendi [claude-cookbook](https://github.com/anthropics/anthropic-cookbook)'unda "deployment" örneklerinin çoğu FastAPI ile. Bu refleks = iş pazarında da değer.

## FastAPI kısaca — üç paragraf, matematiksiz

**FastAPI = Python'da HTTP API kurmanın modern yolu.** `@app.get("/")` decorator'ı ile bir fonksiyonu URL'e bağlıyorsun. Fonksiyon ne döndürürse, FastAPI onu **otomatik JSON'a çeviriyor.** Sen `return {"mesaj": "merhaba"}` yazıyorsun, tarayıcı `{"mesaj":"merhaba"}` alıyor.

**`POST` için Pydantic modelleri var.** `class Soru(BaseModel): mesaj: str` yazıyorsun — FastAPI bu şemayı anlıyor, gelen JSON'u doğruluyor (eksik alan = otomatik hata), sonra fonksiyonuna temiz bir `Soru` nesnesi veriyor. 20 satırlık validasyon kodu yazmadın.

**`uvicorn` sunucu, FastAPI ise framework.** `uvicorn main:app --reload` komutu uygulamayı başlatır, `--reload` sen kodu değiştirdikçe otomatik yeniler. Port default `8000`. Tarayıcıdan `http://localhost:8000/docs` → **Swagger UI** otomatik açılır, her endpoint'i tarayıcıdan test edebilirsin. Postman gerekmez.

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

  classDef cli fill:#ddd6fe,stroke:#7c3aed,color:#111
  classDef srv fill:#fed7aa,stroke:#ea580c,color:#111
  classDef fw fill:#dbeafe,stroke:#2563eb,color:#111
  classDef logic fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef hed fill:#dcfce7,stroke:#16a34a,color:#111
  class BROWSER cli
  class UVI srv
  class FA,ROUTE fw
  class FN,PYD logic
  class JSON hed
```

<table class="ma-aktorler" markdown>

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 🌐 **Tarayıcı / curl** | Senin makinen | HTTP isteği atar (GET, POST), cevabı alır |
| ⚡ **uvicorn** | Aynı makine, port 8000 | **ASGI sunucu** — HTTP protokolünü konuşur, FastAPI'ye bağlar |
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
pip install fastapi uvicorn
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
{"aldim":"Merhaba FastAPI","senden":"Kemal","karakter_sayisi":17}
```

**Burada olan nedir (diyagram referansı):** curl → uvicorn (:8000) → FastAPI app → `/echo` route → Pydantic `Soru` doğrulaması → `mesaji_yansit` fonksiyonu → JSON cevap → curl'e döndü. Diyagramın tüm akışı 15 satır kodda çalıştı.

### Yol B — Hata yönetimi + async + path parameter

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx  # pip install httpx

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
    async with httpx.AsyncClient() as client:
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

**Önemli:** `--host 0.0.0.0` = "dış dünyadan erişilebilir" demek. Local geliştirmede `127.0.0.1` (default) kal. VPS'te servis açarken nginx reverse proxy kullan (Bölüm 9).

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu konuyu nasıl anlatıyor — öz</div>

Anthropic FastAPI'yi **resmi olarak önermez** — Python web framework'u seçimi sana kalmış. Ama Anthropic'in kendi örneklerinde ve cookbook'ta FastAPI **en sık gördüğün framework.**

**1. Cookbook örnekleri FastAPI tabanlı.** [anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) repo'sundaki deploy ve tool use notebook'larının çoğu FastAPI + uvicorn ile. "Claude'u production'a nasıl koyarım" sorusuna Anthropic'in örtük cevabı bu.

**2. Claude SDK async-friendly.** Anthropic Python SDK `AsyncAnthropic` sınıfı ile gelir. FastAPI `async def` endpoint'leriyle mükemmel uyumlu — aynı event loop, aynı dosya. Blocking `time.sleep` değil, `await client.messages.create(...)` = doğru desen.

**3. Pydantic + Claude structured output.** Claude'un tool use cevapları JSON Schema'ya uygun gelir; FastAPI'nin Pydantic modelleri aynı ekosistem (JSON Schema standardı). Claude'dan gelen structured data'yı direkt Pydantic model'e döküp doğrulamak yaygın desen. Bölüm 6'da detay.

??? info "Teknik detay — isteyene (parameter adları, mekanikler, edge case'ler)"

    **ASGI vs WSGI.** `uvicorn` ASGI (Async Server Gateway Interface) — FastAPI için. Flask/Django eski WSGI üstünde, bu yüzden async native değiller. Farkı bilmek FastAPI'nin neden hızlı olduğunu anlatır.

    **Dependency injection.** FastAPI'nin `Depends()` sistemi — auth, DB bağlantısı, Claude client gibi bağımlılıkları fonksiyon imzasında deklare ediyorsun. Test edilebilirlik çok yüksek. Bölüm 9'da detay.

    **Background tasks.** `BackgroundTasks` — HTTP cevabı döndükten sonra arka planda iş yaptırma (log yazma, webhook gönderme). Kullanıcı beklemiyor, iş arka planda.

    **Middleware.** CORS (tarayıcı uyumluluğu), auth, rate limit — middleware olarak eklenir. `app.add_middleware(CORSMiddleware, ...)`.

    **OpenAPI schema.** FastAPI otomatik OpenAPI 3.0 schema üretir — `http://localhost:8000/openapi.json`. Bu standart sayesinde Claude'a "şu OpenAPI'ye uygun isteği yaz" demek mümkün. Agent'larda güçlü desen.

    **Production uvicorn.** Dev'de `--reload`, prod'da `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app` (worker sayısı = CPU × 2 + 1 genelde). Tek process yetmez.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [FastAPI resmi dokümanı](https://fastapi.tiangolo.com/) (EN, Türkçe çevirisi var). Başlangıç için birebir rehber. Pekiştirme: [Anthropic Cookbook — tool_use notebook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use) — FastAPI ile Claude tool use üretim deseni.
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

- **A → B:** Python fonksiyonunu "dış dünya" doğrudan çağıramaz; araya bir **HTTP arayüzü** gerek.
- **B → C:** FastAPI decorator'ı (`@app.post(...)`) = fonksiyonu HTTP URL'e bağlayan **tek satır.**
- **C → D:** Pydantic model → gelen JSON'un doğru şekilde geldiğini garanti ediyor; 20 satır validation kodu yazmıyorsun.
- **D → E:** uvicorn **ASGI sunucusu** = async fonksiyonları doğru çalıştıran event loop — LLM çağrısı I/O-ağır olduğu için kritik.
- **E → F:** `/docs` Swagger UI = ücretsiz, otomatik, paylaşılabilir API dokümantasyonu. Frontend ekip, test ekip aynı sayfadan konuşuyor.

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
