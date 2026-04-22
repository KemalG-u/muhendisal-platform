# 0.5 İlk AI Servisi

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 0.3 bitmiş (Ollama `qwen2.5:3b` indirilmiş, çalışıyor) + 0.4 bitmiş (FastAPI `uvicorn` ile açılıyor); iki ayrı terminal açabilmelisin</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Kendi makinende **uçtan uca çalışan bir AI servisi** var — `curl -X POST http://localhost:8000/chat -d '{"mesaj":"..."}'` atınca Ollama cevap verir, FastAPI döndürür. **Bölüm 0'ın bitiş çizgisi.**</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    Bu sayfadaki **italik-altı çizili** ifadelerin (endpoint, streaming, localhost gibi) üstüne mouse'unu getir — kısa tanım çıkar. Mobilde dokun.

## Neden bu sayfa?

Önceki dört sayfa **parça parça aktör tanıttı:** Linux (0.1), Python (0.2), Ollama (0.3), FastAPI (0.4). Tek tek çalıştılar ama **birbirleriyle konuşmadılar.** Bu sayfa onları birleştirir. Sonuçta elinde **"çağırılabilir bir AI"** var — tarayıcıdan, mobilden, başka servisten, herkesten.

İkincisi: Bu sayfa **"deliller konuşsun"** anı. Bölüm 0'a başladığında "AI Engineer olacağım" dedin. Bu sayfa bittiğinde **çalışan bir AI servisi** elinde var. Gerçek. Fotoğraflayabilirsin, paylaşabilirsin, portföyüne koyabilirsin. Bölüm 1'e başlarken **boş eller** değil **bir deliller** ile giriyorsun.

Üçüncüsü: Bu iskelet **Bölüm 2 itibarıyla Claude'a geçecek.** Ollama yerine Claude API'ye `httpx.post(...)` yapacaksın, o kadar. Bugün öğrendiğin HTTP → Python → LLM → JSON → HTTP **tam olarak gerçek AI servisinin iskeletidir.** Bundan sonraki 10 bölümde bu iskeletin üstüne katmanlar kurulacak (sistem prompt, RAG, agent, multimodal, güvenlik).

## Uçtan uca AI servisi kısaca — üç paragraf, matematiksiz

**İki süreç, iki port, bir köprü.** Ollama `:11434`'te çalışıyor (0.3). FastAPI `:8000`'de çalışıyor (0.4). Bu iki süreci **senin Python kodun** birleştiriyor — FastAPI `/chat` endpoint'i `httpx` ile Ollama'nın `http://localhost:11434/api/generate`'ına POST atıyor, cevabı alıp kendi cevap olarak döndürüyor. Üç parçalı zincir.

**async/await burada kritik.** Kullanıcı soruyu attığında LLM 2-30 saniye sürebilir (Claude'da daha hızlı, Ollama'da yavaş). Bu sürede FastAPI başka isteklere de cevap vermelidir — `async def` + `await` = **bloklamayan** servis. Eş zamanlı 10 kullanıcıya cevap verebilen servis, tek iş yaptıktan sonra dönebilen servise göre 10 kat verimli.

**Hata yönetimi production'ın yarısı.** Ollama kapalıysa? Model yüklenmediyse? Kullanıcı bomboş mesaj attıysa? Timeout aşıldıysa? Her bir durum için anlamlı hata + uygun HTTP status code. Bu sayfada **5 farklı hata yolu** ele alıyoruz — Bölüm 8'de detay, buradaki giriş.

## Bu sayfanın ekosistemi — kim kime ne veriyor

<div class="ma-ekosistem" markdown>
<div class="ma-ekosistem-header">🗺️ Ekosistem — curl'den Ollama'ya ve geri</div>

```mermaid
flowchart LR
  USR["👤 Kullanıcı\n(curl / browser)"]
  UVI["⚡ uvicorn\n:8000"]
  FA["🚀 FastAPI\n/chat"]
  CODE["🐍 chat()\nfonksiyonu"]
  HC["📡 httpx.AsyncClient"]
  OLLAMA["🦙 Ollama\n:11434\nqwen2.5:3b"]
  RESP["📦 JSON cevap"]

  USR -->|POST /chat\n{'mesaj':'...'}| UVI
  UVI --> FA --> CODE --> HC
  HC -->|POST /api/generate| OLLAMA
  OLLAMA -->|LLM cevabı| HC
  HC --> CODE --> RESP
  RESP --> USR

  classDef kul fill:#ddd6fe,stroke:#7c3aed,color:#111
  classDef srv fill:#fed7aa,stroke:#ea580c,color:#111
  classDef fw fill:#dbeafe,stroke:#2563eb,color:#111
  classDef logic fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef llm fill:#fce7f3,stroke:#be185d,color:#111
  classDef hed fill:#dcfce7,stroke:#16a34a,color:#111
  class USR kul
  class UVI srv
  class FA fw
  class CODE,HC logic
  class OLLAMA llm
  class RESP hed
```

<table class="ma-aktorler" markdown>

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 👤 **Kullanıcı** | Terminal / tarayıcı / uygulama | HTTP POST atar, cevap alır |
| ⚡ **uvicorn :8000** | Senin makinen | FastAPI app'ini ASGI olarak sunar |
| 🚀 **FastAPI /chat** | `main.py` | Route + Pydantic doğrulama + fonksiyon çağrısı |
| 🐍 **chat() fonksiyonu** | Senin iş mantığın | İstek hazırla → Ollama'ya sor → cevabı parse et → kullanıcıya yolla |
| 📡 **httpx.AsyncClient** | Python paketi | async HTTP istemcisi (asenkron requests) |
| 🦙 **Ollama :11434** | Aynı makine | Yerel LLM (`qwen2.5:3b`) çağrıyı işler, cevap üretir |
| 📦 **JSON cevap** | `return {...}` | FastAPI kullanıcıya döndürür |

</table>
</div>

## Uygulama — uçtan uca servis

### Adım 1 — Gerekli paketleri kur (venv aktif)

```bash
pip install fastapi uvicorn httpx pydantic
pip freeze > requirements.txt
```

### Adım 2 — `main.py` yaz

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

app = FastAPI(title="İlk AI Servisim", version="0.5.0")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"  # 0.3'te indirdiğin model


class Soru(BaseModel):
    mesaj: str = Field(..., min_length=1, max_length=2000)
    model: str = MODEL  # kullanıcı farklı model isteyebilir


class Cevap(BaseModel):
    mesaj: str
    model: str
    kullanilan_saniye: float


@app.get("/")
def saglik():
    return {"durum": "ayakta", "servis": "ilk-ai-servisim", "v": "0.5.0"}


@app.post("/chat", response_model=Cevap)
async def chat(soru: Soru):
    """Kullanıcı mesajını Ollama'ya sorar, cevabı döndürür."""
    import time
    basladi = time.time()

    ollama_istek = {
        "model": soru.model,
        "prompt": soru.mesaj,
        "stream": False,  # streaming değil — tek parça cevap
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(OLLAMA_URL, json=ollama_istek)
            r.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama'ya baglanilamadi. Calisiyor mu? 'ollama serve'",
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Ollama 60 saniye icinde cevap vermedi. Mesaj cok uzun olabilir.",
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama hatasi: {e.response.status_code} {e.response.text[:200]}",
        )

    ollama_cevap = r.json()
    gecen = round(time.time() - basladi, 2)

    return Cevap(
        mesaj=ollama_cevap["response"],
        model=soru.model,
        kullanilan_saniye=gecen,
    )
```

### Adım 3 — İki terminal açık: Ollama + FastAPI

**Terminal 1 — Ollama:**

```bash
ollama serve
# Eğer "address already in use" hatası alırsan zaten çalışıyor demek
```

**Terminal 2 — FastAPI:**

```bash
# venv aktif olmalı
uvicorn main:app --reload
```

### Adım 4 — Test (3. terminal)

```bash
# Sağlık kontrolü
curl http://localhost:8000/

# İlk AI çağrısı
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mesaj":"Türkiyenin başkenti neresidir? Tek cümle."}'
```

Beklenen çıktı (yaklaşık, model'e göre değişir):

```json
{
  "mesaj": "Türkiye'nin başkenti Ankara'dır.",
  "model": "qwen2.5:3b",
  "kullanilan_saniye": 2.34
}
```

**Hatayı test et:**

```bash
# Boş mesaj → Pydantic validasyon hatası (422)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mesaj":""}'

# Ollama'yı durdur (Terminal 1'de Ctrl+C), tekrar çağır → 503
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mesaj":"merhaba"}'
```

**Burada olan nedir (diyagram referansı):** curl → uvicorn:8000 → FastAPI `/chat` → Pydantic `Soru` validasyonu → `chat()` fonksiyonu → httpx → Ollama:11434 → LLM cevabı → httpx → `Cevap` modeli → JSON → curl. **Tam zincir, 45 satır kod.**

### Bonus — `/docs` Swagger UI'da test et

Tarayıcı → `http://localhost:8000/docs` → `POST /chat` → "Try it out" → JSON'u düzenle → "Execute". Cevap altta çıkar, gerçek API gibi tarayıcıdan test ediyorsun.

### Claude'a geçiş öngörüsü (Bölüm 2'de)

Bölüm 2'de `chat()` fonksiyonu değişecek, geri kalan her şey aynı kalacak:

```python
# Şu anki (Ollama)
async with httpx.AsyncClient(timeout=60.0) as client:
    r = await client.post(OLLAMA_URL, json=ollama_istek)

# Bölüm 2 itibarıyla (Claude)
import anthropic
client = anthropic.AsyncAnthropic()
cevap = await client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": soru.mesaj}],
)
```

**Yani bugün öğrendiğin iskelet, Bölüm 9'da production'a verdiğin servisin tam olarak iskeleti.** 10 bölüm boyunca katmanlar ekleniyor, omurga aynı.

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu konuyu nasıl anlatıyor — öz</div>

Anthropic Bölüm 0 seviyesinde bir şey demez — AI servis kurmanın Python / FastAPI / Docker tarafı Anthropic'in domain'i değil. Ama Claude'u devreye soktuğunda Anthropic'in tavsiyeleri çok net.

**1. `AsyncAnthropic` client default kullan.** Web servisinde (FastAPI, Flask, Django) **bloklamayan istemci** şart. Sync `Anthropic()` client'ı tek kullanıcılı script için. Gerçek servis = `AsyncAnthropic()`.

**2. API key env değişkeninden.** `ANTHROPIC_API_KEY` env değişkeni → SDK otomatik okur. Kodda hard-code etme. `.env` dosyası + `python-dotenv` = lokal geliştirme. Prod'da cloud secrets manager.

**3. Retry + backoff built-in.** Anthropic SDK, 429 rate limit + 5xx geçici hatalarda otomatik retry yapar (exponential backoff). Sen `try/except` ile ek tabaka yazarsın — 0.5 versiyonda gösterdiğimiz httpx deseni Claude için de aynı. Bölüm 8'de detay.

??? info "Teknik detay — isteyene (parameter adları, mekanikler, edge case'ler)"

    **Streaming.** LLM cevabı 30 saniye sürebilir; kullanıcı beklemek istemez. Streaming = cevap üretilirken **token token** aktarmak. Ollama `"stream": True`, Claude `client.messages.stream(...)` ile. Frontend'de SSE (Server-Sent Events) veya WebSocket ile gösterilir. Bölüm 9'da detay.

    **CORS.** Tarayıcıdan direkt çağıracaksan (React/Vue frontend) CORS middleware eklemek zorunda. `from fastapi.middleware.cors import CORSMiddleware`. Production'da `allow_origins` kısıtlı tutulur — sadece sizin domain.

    **Auth.** Bu iskelet auth'suz. Production'da header'dan API key veya JWT ile koruma şart. `Depends(get_current_user)` deseni + FastAPI security utilities. Bölüm 8'de güvenlik katmanı.

    **Docker paketleme.** `requirements.txt` + `Dockerfile` + `docker-compose.yml` ile Ollama + FastAPI tek komutla kalkar. Bölüm 9.1'de detay.

    **Timeouts disiplini.** `httpx.AsyncClient(timeout=60.0)` — 60 saniye. Çok kısa = LLM cevap yetişemez, çok uzun = kullanıcı bekler. Claude için 120 saniye, Ollama için 60 saniye makul başlangıç.

    **Observability.** Her `/chat` çağrısını logla (input hash + model + latency + token count). Datadog / Prometheus / Grafana — Bölüm 8.4 detay.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [docs.claude.com — Client SDKs](https://docs.claude.com/en/api/client-sdks) (EN, ~10 dk). Python SDK + async kullanım örnekleri. Pekiştirme: [Anthropic Cookbook — basic usage](https://github.com/anthropics/anthropic-cookbook/tree/main/misc) — Claude'un en sade FastAPI örnekleri.
</div>
</div>

<div class="ma-cikti-kaniti" markdown>
### 📦 Bu sayfayı bitirdiğini nasıl kanıtlarsın

#### 1. 📝 Refleksiyon yazısı — 5 dakika

> "İlk AI servisimi kurdum. `curl -X POST .../chat` ile [şu] mesajı gönderdim, [şu cevabı] aldım, [X] saniye sürdü. Ollama'yı durdurup test ettim, [503 hatası] doğru şekilde döndü. Kendi makinemde çalışan bir AI servisi oldu — Bölüm 2'de Claude'a geçireceğim."

Kaydet: `muhendisal-notlarim/bolum-0/05-ilk-ai-servisi/refleksiyon.txt`

#### 2. 📸 Ekran görüntüsü — 3 dakika

**Neyin görüntüsü:** 3 terminal yan yana — Ollama log'u, uvicorn log'u, curl çıktısı (JSON cevabı).

| OS | Kısayol |
|---|---|
| Windows | `Win + Shift + S` |
| Mac | `Cmd + Shift + 4` |
| Linux | `Shift + PrtScr` |

Kaydet: `muhendisal-notlarim/bolum-0/05-ilk-ai-servisi/ucucuncan-uca.png`

#### 3. 💻 GitHub repo + README + demo gif — 10 dakika

`main.py` + `requirements.txt` + `README.md`'yi GitHub'a koy. README'ye **kurulum adımları** (venv, ollama, uvicorn) + **örnek curl** + **beklenen çıktı** yaz. Bonus: [terminalizer](https://github.com/faressoft/terminalizer) veya ekran kayıt ile 10 saniyelik gif çek, README'ye ekle.

Repo linkini kaydet: `muhendisal-notlarim/bolum-0/05-ilk-ai-servisi/repo-link.txt` — **bu link senin ilk portföy kanıtın.**

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

- **A → B:** HTTP servisi + LLM = "çağırılabilir AI" = production prototipi. Tek script'ten 10 kat üstün.
- **B → C:** `async def` + `httpx.AsyncClient` → uvicorn event loop'unu bloklamıyor → 10 kullanıcıya aynı anda cevap.
- **C → D:** Pydantic `Soru` + `Cevap` modelleri = hem validasyon hem otomatik dokümantasyon (`/docs`).
- **D → E:** 5 farklı hata yolu (ConnectError, Timeout, HTTPStatusError, validasyon 422, generic 500) = her hata **anlamlı cevap + doğru status code.**
- **E → F:** Bu iskelet Bölüm 2'de Claude'a, Bölüm 4'te RAG'e, Bölüm 6'da agent'a, Bölüm 9'da production'a evrilir. **Omurga değişmez.**

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Bölüm 0 bitti. Boş bir ekrandan başladın, şimdi curl → Python → LLM → JSON → curl zinciri çalışıyor. Bölüm 1'e başlarken artık "AI nasıl çağrılır" sorusunun cevabı **senin makinendeki portföy dosyan.** Sıradaki 10 bölüm bu iskeletin üstüne inşa.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[Bölüm 1 — Giriş ve Temeller →](../bolum-1/index.md)** — Haritayı genişletelim. "AI Engineer" tam olarak kimdir, "ML Engineer"dan farkı ne, 2026'nın AI ekosistemi nasıl görünüyor, sen hangi yolu seçmelisin.

← [0.4 FastAPI İskeleti](04-fastapi.md) &nbsp;|&nbsp; [Bölüm 0 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** `main.py`'a **bir system prompt özelliği** ekle — `Soru` modeline `sistem: str | None = None` ekle, Ollama isteğine `"system": soru.sistem` geç. Farklı sistem promptlarıyla aynı mesajın nasıl farklı cevaplandığını dene. Bu Bölüm 2.4'ün ön provası.
</div>
