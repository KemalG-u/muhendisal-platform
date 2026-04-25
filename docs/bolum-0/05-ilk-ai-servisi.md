# 0.5 İlk AI Servisi

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~35 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 0.3 bitmiş (Ollama `qwen2.5:3b` indirilmiş, çalışıyor) + 0.4 bitmiş (FastAPI `uvicorn` ile açılıyor); iki ayrı terminal açabilmelisin</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Kendi makinende **uçtan uca çalışan bir AI servisi** var — `curl -X POST http://localhost:8000/chat -d '{"mesaj":"..."}'` atınca Ollama cevap verir, FastAPI döndürür. **Bölüm 0'ın bitiş çizgisi.**</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    Bu sayfadaki **kalın** teknik terimler (endpoint, streaming, localhost gibi) ilk geçişte hemen yanında veya altında Türkçe açıklanır.

## Neden bu sayfa?

Önceki dört sayfa **parça parça aktör tanıttı:** Linux (0.1), Python (0.2), Ollama (0.3), FastAPI (0.4). Tek tek çalıştılar ama **birbirleriyle konuşmadılar.** Bu sayfa onları birleştirir. Sonuçta elinde **"çağırılabilir bir AI"** var — tarayıcıdan, mobilden, başka servisten, herkesten.

İkincisi: Bu sayfa **"somut çıktı"** anı. Bölüm 0'a başladığında "AI Engineer olacağım" dedin. Önceki sayfalarda kavramları öğrendin; bu sayfa bittiğinde **çalışan bir AI servisi** elinde var. Gerçek. Fotoğraflayabilirsin, paylaşabilirsin, portföyüne koyabilirsin. Bölüm 1'e başlarken **boş elle** değil **somut bir kanıtla** giriyorsun.

Üçüncüsü: Bu iskelet **Bölüm 2 itibarıyla Claude'a geçecek.** Ollama yerine Claude API'ye `httpx.post(...)` yapacaksın, o kadar. Bugün öğrendiğin HTTP → Python → LLM → JSON → HTTP **tam olarak gerçek AI servisinin iskeletidir.** Bundan sonraki 10 bölümde bu iskeletin üstüne katmanlar kurulacak (sistem prompt, RAG, agent, multimodal, güvenlik).

## Uçtan uca AI servisi kısaca — üç paragraf, matematiksiz

**İki süreç, iki port, bir köprü.** Ollama `:11434`'te çalışıyor (0.3). FastAPI `:8000` portunda çalışıyor (0.4). İki süreci **senin Python kodun** birleştiriyor: FastAPI'nin `/chat` adresi, `httpx` (Python'un asenkron HTTP kütüphanesi) ile Ollama'nın `http://localhost:11434/api/generate` adresine bir POST isteği atıyor, cevabı alıp kendi cevabı olarak döndürüyor. Üç parçalı zincir.

**async/await burada kritik.** Kullanıcı soruyu attığında LLM 2-30 saniye sürebilir (Claude'da daha hızlı, Ollama'da yavaş). Bu sürede FastAPI başka isteklere de cevap vermelidir — `async def` + `await` = **bloklamayan** servis. Aynı anda 10 kullanıcıya cevap verebilen bir servis, isteği tek tek işleyen servise göre yaklaşık 10 kat verimlidir.

**Hata yönetimi canlı serviste kodun yarısıdır.** Ollama kapalıysa? Model yüklenmediyse? Kullanıcı bomboş mesaj attıysa? Zaman aşımı (timeout) çıktıysa? Her bir durum için anlamlı hata + uygun HTTP durum kodu. Bu sayfada **5 farklı hata yolu** ele alıyoruz — Bölüm 8'de detay, buradaki giriş. Hata yönetimi yazılırken sıkıcı, çökünce hayat kurtarıcı.

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
  class USR kul
  class FA fw
  class OLLAMA srv
  class UVI,CODE,HC,RESP logic
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
import time

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
    basladi = time.time()

    ollama_istek = {
        "model": soru.model,
        "prompt": soru.mesaj,
        "stream": False,  # akış değil — tek parça cevap
    }

    try:
        # 120 sn — ilk çağrıda model RAM'e yükleniyor (cold start) olabilir
        async with httpx.AsyncClient(timeout=120.0) as client:
            r = await client.post(OLLAMA_URL, json=ollama_istek)
            r.raise_for_status()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama'ya bağlanılamadı. Çalışıyor mu? 'ollama serve' komutunu denedin mi?",
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Ollama 120 saniye içinde cevap vermedi. Mesaj çok uzun ya da donanım yavaş olabilir.",
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama hatası: {e.response.status_code} {e.response.text[:200]}",
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"HTTP istek hatası: {e}")

    try:
        ollama_cevap = r.json()
        cevap_metni = ollama_cevap["response"]
    except (KeyError, ValueError) as e:
        raise HTTPException(
            status_code=502, detail=f"Ollama JSON çözümleme hatası: {e}"
        )

    gecen = round(time.time() - basladi, 2)

    return Cevap(mesaj=cevap_metni, model=soru.model, kullanilan_saniye=gecen)
```

### Adım 3 — İki terminal açık: Ollama + FastAPI

**Terminal 1 — Ollama:**

```bash
ollama serve
# "address already in use" (port zaten kullanımda) hatası alırsan
# Ollama zaten arka planda çalışıyor demektir; ayrıca çalıştırmana gerek yok.
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

**Burada olan nedir (diyagram referansı):** curl → uvicorn:8000 → FastAPI `/chat` → Pydantic `Soru` doğrulaması → `chat()` fonksiyonu → httpx → Ollama:11434 → LLM cevabı → httpx → `Cevap` modeli → JSON → curl. **Tam zincir, ~70 satır kod.**

??? warning "Tipik servis hataları — şu durum olduğunda şu yanıt"

    | HTTP yanıt | Sebep | Çözüm |
    |---|---|---|
    | `503` | Ollama kapalı | Terminal 1'de `ollama serve` çalıştır |
    | `504` | Model çok büyük / RAM yetmiyor / cold start | Daha küçük model dene: `MODEL = "qwen2.5:1.5b"` |
    | `422` | Body boş veya `mesaj` eksik | JSON gönderirken `mesaj` alanı dolu olmalı (en az 1 karakter) |
    | `404` (curl) | Yanlış uç | URL `localhost:8000/chat` olmalı (kök slash + endpoint) |
    | İlk çağrı 30+ saniye | Model RAM'e yükleniyor (cold start) | Normaldir; sonraki çağrılar 1-5 sn olur |

### Bonus — `/docs` Swagger UI'da test et

Tarayıcı → `http://localhost:8000/docs` → `POST /chat` → "Try it out" → JSON'u düzenle → "Execute". Cevap altta çıkar, gerçek API gibi tarayıcıdan test ediyorsun.

### Ollama vs Claude — ne zaman hangisi

| Kıstas | Ollama (lokal) | Claude API |
|---|---|---|
| **Maliyet** | Sıfır (donanım hariç) | Token başı ücret |
| **Hız** | Donanıma bağlı (GPU'suz yavaş) | Hızlı (Anthropic altyapısı) |
| **Türkçe kalite** | `qwen2.5` — iyi | Claude — çok iyi |
| **İnternet** | Offline çalışır | İnternet şart |
| **Gizlilik** | Veriler makinende | Anthropic sunucularına gider |
| **Ne zaman?** | Geliştirme, prototip, maliyet testi | Prod servis, kalite kritik |

### Claude'a geçiş öngörüsü (Bölüm 2'de)

Bölüm 2'ye geçtiğinde sadece `chat()` fonksiyonunun **içi** değişecek (Ollama yerine Claude çağrısı), geri kalan tüm iskelet (FastAPI, Pydantic, hata yönetimi) aynı kalacak. Yani bugün öğrendiğin yapı boşa gitmiyor:

```python
# Şu anki (Ollama)
async with httpx.AsyncClient(timeout=60.0) as client:
    r = await client.post(OLLAMA_URL, json=ollama_istek)

# Bölüm 2 itibarıyla (Claude)
import anthropic
client = anthropic.AsyncAnthropic()
cevap = await client.messages.create(
    model="claude-sonnet-4-6",
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

    **Akış (streaming).** LLM cevabı 30 saniye sürebilir; kullanıcı beklemek istemez. Akış = cevap üretilirken **token token** aktarmak. Ollama'da `"stream": True`, Claude'da `client.messages.stream(...)` ile. **Tarayıcı tarafında (frontend)** ise SSE (Server-Sent Events — sunucudan tarayıcıya canlı akış) veya WebSocket (çift yönlü canlı bağlantı) ile gösterilir. Bölüm 9'da detay.

    **CORS.** Tarayıcıdan direkt çağıracaksan (React/Vue frontend) CORS middleware eklemek zorunda. `from fastapi.middleware.cors import CORSMiddleware`. Production'da `allow_origins` kısıtlı tutulur — sadece sizin domain.

    **Auth.** Bu iskelet auth'suz. Production'da header'dan API key veya JWT ile koruma şart. `Depends(get_current_user)` deseni + FastAPI security utilities. Bölüm 8'de güvenlik katmanı.

    **Docker paketleme.** `requirements.txt` + `Dockerfile` + `docker-compose.yml` ile Ollama + FastAPI tek komutla kalkar. Bölüm 9.1'de detay.

    **Zaman aşımı (timeout) disiplini.** `httpx.AsyncClient(timeout=120.0)` — 120 saniye. Çok kısa olursa LLM cevabı yetiştiremez, çok uzun olursa kullanıcı sıkılıp bırakır. Claude için 120 saniye, Ollama için cold start dahil 120 saniye makul başlangıç. Sıcak (warm) çağrılarda 30 sn yeterlidir.

    **Observability.** Her `/chat` çağrısını logla (input hash + model + latency + token count). Datadog / Prometheus / Grafana — Bölüm 8.4 detay.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [platform.claude.com — Client SDKs](https://platform.claude.com/docs/en/api/client-sdks) (EN, ~10 dk). Python SDK + async kullanım örnekleri. Pekiştirme: [anthropics/courses — anthropic_api_fundamentals](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) — Anthropic'in resmi giriş kursu (ücretsiz Jupyter notebook serisi).
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

Kaydet: `muhendisal-notlarim/bolum-0/05-ilk-ai-servisi/uctan-uca.png`

#### 3. 💻 GitHub repo + README + demo gif — 10 dakika

`main.py` + `requirements.txt` + `README.md`'yi GitHub'a koy. README'ye **kurulum adımları** (venv, ollama, uvicorn) + **örnek curl** + **beklenen çıktı** yaz. Bonus: [terminalizer](https://github.com/faressoft/terminalizer) (terminal kaydedip GIF'e dönüştüren araç) veya ekran kaydı uygulaması ile 10 saniyelik kısa video/GIF hazırla, README'ye ekle.

Repo linkini kaydet: `muhendisal-notlarim/bolum-0/05-ilk-ai-servisi/repo-link.txt` — **bu link senin ilk portföy kanıtın.**

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**HTTP servisi + LLM = çağırılabilir AI.** Terminal script = sadece sen kullanabilirsin. Bu yüzden **FastAPI arayüzüyle production prototipi oldu.**</li>
<li>**`async def` + `httpx.AsyncClient` = bloklanmayan servis.** LLM 2–30 saniye sürer; diğer isteklerin beklemesi anlamsız. Bu yüzden **eş zamanlı birden fazla kullanıcıya cevap veriyorsun.**</li>
<li>**Pydantic `Soru` + `Cevap` = validasyon + dokümantasyon.** Şema tanımla, FastAPI geri kalanını halleder. Bu yüzden **`/docs` Swagger UI otomatik oluşuyor.**</li>
<li>**5 hata yolu = anlamlı hata mesajları.** ConnectError, Timeout, HTTPStatusError, 422, 500 — her biri farklı durum. Bu yüzden **kullanıcı "bir şeyler ters gitti" değil "Ollama kapalı" görüyor.**</li>
<li>**Omurga değişmez.** Bölüm 2'de Claude'a, 4'te RAG'e, 6'da agent'a, 9'da production'a evrilir. Bu yüzden **bugün öğrendiğin iskelet 10 bölüm boyunca taşınacak.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Bölüm 0 bitti. Boş bir ekrandan başladın, şimdi curl → Python → LLM → JSON → curl zinciri çalışıyor. Bölüm 1'e başlarken artık "AI nasıl çağrılır" sorusunun cevabı **senin makinendeki portföy dosyan.** Sıradaki 10 bölüm bu iskeletin üstüne inşa.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[Bölüm 1 — Giriş ve Temeller →](../bolum-1/index.md)** — Haritayı genişletelim. "AI Engineer" tam olarak kimdir, "ML Engineer"dan farkı ne, 2026'nın AI ekosistemi nasıl görünüyor, sen hangi yolu seçmelisin.

← [0.4 FastAPI İskeleti](04-fastapi.md) &nbsp;|&nbsp; [Bölüm 0 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** `main.py`'a bir **sistem promptu** (modele "sen kimsin, nasıl davran" diyen başlangıç talimatı) özelliği ekle — `Soru` modeline `sistem: str | None = None` ekle, Ollama isteğine `"system": soru.sistem` geç. Farklı sistem promptlarıyla aynı mesajın nasıl farklı cevaplandığını dene. Bu Bölüm 2.4'ün ön provası.
</div>
