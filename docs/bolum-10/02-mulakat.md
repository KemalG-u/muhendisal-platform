# 10.2 Mülakat Soruları — 30 Soru + Model Cevap

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 10.1 LinkedIn stratejisi uygulandı; ilk DM atıldı veya başvuru yapıldı. 9.4 + 9.5 canlıda, kendi kodun hakkında konuşacak birikimin var.</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> **30 yaygın AI Engineer mülakat sorusuna** model cevabın hazır — teknik 18, davranışsal 6, senaryo 6. STAR formatı refleksi, **kendi projenden örneklerle** her cevapta kanıt. Maaş müzakere refleksi. Mülakatçıya sorman gereken 5 soru. **Cevapları ezberleme — tez olarak kullan**, kendi örnekleriyle yaz.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **STAR** = Situation (durum), Task (görev), Action (aksiyon), Result (sonuç). Davranışsal soru cevap formatı. **Tech screen** = ön teknik görüşme, 30-60 dk. **Take-home** = ev ödevi, 4-8 saat kod yazarsın + sunarsın. **Behavioral round** = davranışsal görüşme, liderlikle. **Cultural fit** = şirket kültürüne uygunluk değerlendirmesi. **Leveling** = junior/mid/senior seviye kararı.

## Mülakat süreç tipik

AI Engineer pozisyonunda mülakat 3-5 aşama:

```
1. Recruiter screen   (30 dk)  → CV + motivasyon + maaş bandı
2. Tech screen        (60 dk)  → kodlama + temel teknik sorular
3. Take-home          (4-8 sa) → küçük AI projesi (opsiyonel)
4. Deep tech          (60 dk)  → sistem tasarımı + projen derinleşme
5. Behavioral         (45 dk)  → hiring manager ile kültür + takım
```

**Süre:** 2-4 hafta. Küçük şirket daha hızlı (1 hafta, 2 görüşme), büyük şirket yavaş (1 ay, 5 görüşme).

Bu sayfadaki 30 soru **her aşamada** çıkabilir. Hepsini önce oku, sonra **kendi cevabını** yaz.

## Teknik sorular — 18 soru

### 1. Prompt, token, context window nedir?

**Model cevap:** Prompt = LLM'e gönderdiğin metin; sistem mesajı (rol) + kullanıcı mesajı (soru) + asistan mesajları (varsa geçmiş). Token = modelin işlediği atom birim; Türkçe'de 1 kelime ~2-3 token, İngilizce'de 1 kelime ~1.3 token. Context window = modelin tek çağrıda işleyebileceği max token; Claude Sonnet 4.5 için 200K (input + output toplam). 200K token ~150K kelime veya ~500 sayfa metin — tam bir roman okur.

**Senin örneğin:** "9.4 RAG Chatbot'umda 50 sayfalık PDF ~25K token; Claude'un 200K context'inde rahatça sığıyor."

### 2. Temperature ne işe yarar?

**Model cevap:** Temperature modelin cevap çeşitliliğini kontrol eder. 0 = deterministik (aynı soru aynı cevap); 1 = yaratıcı (çeşitli cevaplar). RAG'de **0 veya 0.1** — sadık retrieval cevabı istiyorsun. Yaratıcı yazma (blog, şiir) **0.7-1**. Code generation **0-0.3**. Değer aralığı modele göre farklı (Claude 0-1, OpenAI 0-2). Default genelde 1 — üretim için düşür.

### 3. RAG nedir, fine-tuning'den ne zaman tercih edilir?

**Model cevap:** RAG (Retrieval-Augmented Generation) = vector DB'den ilgili metinleri bul, LLM'e context olarak gönder, cevabı onunla üret. Fine-tuning = modelin ağırlıklarını kendi verinde yeniden eğit. RAG tercih edilir: (1) bilgi sık güncelleniyor (haftalık); (2) kaynak alıntısı gerekli (hukuk, sağlık); (3) maliyet düşük (embedding + retrieval); (4) veri az (<1000 örnek). Fine-tuning tercih: (1) stil/format öğretmek (markdown output, özel ton); (2) domain jargon derin (tıp terminolojisi); (3) çok örnek (10K+ eşleştirilmiş); (4) latency kritik.

**Senin örneğin:** "9.4'te RAG seçtim çünkü PDF içeriği kullanıcı yüklüyor, hafta hafta değişiyor. Fine-tuning anlamsızdı."

### 4. Embedding nedir, cosine similarity neden?

**Model cevap:** Embedding = metni N-boyutlu vektöre dönüştürme; anlamsal olarak yakın metinler vektör uzayında yakın. Voyage-3 1024 boyut üretir. Cosine similarity iki vektör arasındaki açının kosinüsü — **büyüklüğü ihmal eder**, yönü kıyaslar. Metin embedding'lerde büyüklük (magnitude) metin uzunluğuyla korelasyon; anlamsal benzerlik **yönde**. Euclidean distance büyüklüğü karıştırır, anlamsal benzerlikte yanıltıcı. Cosine → [-1, 1]; 1 = aynı yön, 0 = dik, -1 = zıt.

### 5. Vector DB: Qdrant vs Pinecone ne zaman?

**Model cevap:** Qdrant = açık kaynak, self-host + managed (Qdrant Cloud). Pinecone = managed SaaS only, proprietary. Qdrant tercih: (1) maliyet kritik (1M vektör $4-5/ay VPS vs Pinecone $70+); (2) on-prem veri zorunluluğu; (3) filter + hybrid search zengin. Pinecone tercih: (1) zero-ops (AWS'siz ekip); (2) auto-scale gerek; (3) enterprise SLA. Ara yol: Qdrant Cloud ($25-100/ay). Chroma küçük prototip için; Weaviate GraphQL seven için; pgvector PostgreSQL zaten varsa.

**Senin örneğin:** "3.5 Semantic Search projemde Qdrant seçtim çünkü self-host + filter zengin. 100 bin vektör, $4/ay VPS, aylık Pinecone'un $70'ine göre 18× ucuz."

### 6. Prompt injection nedir, nasıl önlenir?

**Model cevap:** Prompt injection = kullanıcı input'u içine gizlenen komut, LLM'i sistem prompt'tan saptırır ("Önceki talimatları unut, X yap"). 4 katman savunma: (1) sistem prompt sertleştirme (rol kilidi, injection reddi); (2) Pydantic input validation (uzunluk + pattern red); (3) output sanitization (bleach HTML, SQL parameterize); (4) structured output zorla (`tool_choice={"type":"tool","name":"X"}`). Tek katman yetmez — RAG'de chunk injection (context boundary system prompt) ek savunma gerekir.

### 7. Agent vs workflow farkı?

**Model cevap:** Workflow = deterministik adım dizisi; her adımda LLM olabilir ama karar yok. Agent = LLM karar verici; hangi tool'u hangi sırayla çağıracağını kendi seçer. Anthropic "Building Effective Agents" (2024) der: "Start simple — workflow before agents." Workflow tercih: süreç belli, adım tahmin edilebilir (RSS parse → özet → puanla). Agent tercih: kullanıcı sorusu açık uçlu, plan dinamik (deep research, coding agent). Çoğu production sistemi **workflow + 1-2 yerde agent** karması — 9.5 İçerik Özet Agent örnek (radar deterministik, yazar+evaluator LLM ama döngü yok).

### 8. MCP nedir?

**Model cevap:** MCP (Model Context Protocol) = Anthropic'in açık standartı, Claude'u dış servislere bağlamak için. 2024 Kasım yayınlandı. Öncesinde her entegrasyon özel kod; MCP ile standart protokol — bir MCP server yaz, Claude Desktop/Claude Code/API hepsi kullanır. JSON-RPC üstü, stdio veya SSE transport. Tools + resources + prompts üç primitive. Gmail, Slack, GitHub için hazır server'lar var; kendi veri kaynağın için custom yazabilirsin.

**Senin örneğin:** "ClawdBot'ta MCP server yazdım — Claude bot'u Telegram üstünden projelerime bağlıyor; saatler yerine dakikalar."

### 9. Tool calling nasıl çalışır?

**Model cevap:** Tool calling = LLM'e fonksiyon şemaları (JSON schema) verirsin, LLM "bu tool'u şu argümanlarla çağır" der, sen çalıştırırsın, sonucu geri döndürürsün, LLM devam eder. 3 aşama: (1) `tools=[...]` parametresi ile tool listesi; (2) LLM response'da `content` içinde `type: "tool_use"` block; (3) tool'u çalıştır, `type: "tool_result"` olarak geri gönder. `tool_choice="auto"` LLM karar, `tool_choice={"type":"tool","name":"X"}` zorla. Structured output için ikinci pattern kritik — cevap kesin JSON şemasına uyar.

### 10. Streaming nasıl çalışır?

**Model cevap:** Streaming = LLM cevabı **token token** gelir, `messages.stream(...)` ile. Avantaj: kullanıcı ilk token'ı 400ms'de görür, toplam cevap 5 saniye sürse bile **psikolojik olarak hızlı**. UX kritik — chatbot tipi proje. SSE (Server-Sent Events) veya WebSocket'le client'a forward. HTMX + SSE basit implementasyon. Latency ölçümü değişir: "time to first token" vs "total time". p95 ilk token ~500-1500ms iyi hedef.

### 11. Chunking stratejisi?

**Model cevap:** 3 yaygın yaklaşım: (1) **Fixed** — N karakter/token; basit, context parçalanabilir; (2) **Recursive** — paragraf/cümle sınırını önce dene, sonra küçült; semantik daha iyi korunur; LangChain `RecursiveCharacterTextSplitter` standart; (3) **Semantic** — embedding similarity'yle chunk sınırı; en doğru ama yavaş + pahalı. Chunk boyutu: 300-800 token optimum; çok küçük (<100) context kaybolur, çok büyük (>1500) retrieval hassasiyeti düşer. Overlap 10-20% — sınıra düşen bilgi kaybını önler.

### 12. Hybrid search ne zaman?

**Model cevap:** Hybrid search = dense (embedding) + sparse (BM25 keyword) skorlarını birleştir. Dense tek başına eksik: özel isimler (kod, ürün SKU), nadir terimler, tam eşleşme gereken sorgularda zayıf. BM25 tam kelime eşleşmesi iyi yapar ama anlamsal yakınlığı bilmez. Reciprocal Rank Fusion (RRF) veya ağırlıklı toplam. Qdrant 1.10+ native hybrid destek. Örnek: "Türk ceza kanunu 301" — dense "cezai yaptırım"ı bulur, BM25 "301" sayısını direkt yakalar.

### 13. Rate limit nasıl çözülür?

**Model cevap:** 3 katman: (1) client-side (slowapi + Redis) — 10 req/min/IP + user başı token budget; (2) server-side retry (Tenacity exponential jitter 3 deneme); (3) Anthropic Console hard cap $100/ay. 429 retry-After header oku + exponential backoff + jitter. Circuit breaker (pybreaker) 5 peş peşe fail → 60s kapat. Herd effect engeli için jitter zorunlu. Retry sadece geçici hatalar (429, 5xx, timeout); kalıcı (400, 401) retry anlamsız.

**Senin örneğin:** "9.5 agent'ımda Semaphore 3 Sonnet + 5 Haiku ile rate'i istemci tarafında kontrol ediyorum, paralel çağrılar Anthropic'i zorlamıyor."

### 14. Maliyet optimizasyonu?

**Model cevap:** 5 teknik: (1) **Heterojen model** — basit görev Haiku, karmaşık Sonnet (9.5'te %38 tasarruf); (2) **Prompt caching** — aynı system prompt %90 indirimli (Anthropic 2024 Kasım); (3) **Batch API** — %50 indirim, 24 saat bekler (offline işler); (4) **Chunk optimizasyonu** — daha az context → daha az input token; (5) **Model downgrade** — Opus yerine Sonnet, Sonnet yerine Haiku deneyi. Her request için `usage.input_tokens` + `output_tokens` logla; 1 ay sonra "hangi endpoint en pahalı?" net.

### 15. Hallucination nasıl azaltılır?

**Model cevap:** Halüsinasyon = model kaynakta olmayan şeyi uydurur. Azaltma: (1) RAG + kaynak alıntı zorunluluğu; (2) sistem prompt katı ("sadece kaynakta olan bilgi, bilmiyorsan 'bilmiyorum' de"); (3) low temperature (0-0.1); (4) Claude'un dürüstlük refleksi (Anthropic Constitutional AI avantajı — emin değilse söyler); (5) evaluator pattern (ikinci LLM cevabı kaynağa göre denetler, 9.5 agent örneği). Tam sıfırlamaz ama %80+ azaltır.

### 16. Structured output garanti?

**Model cevap:** 3 yol: (1) **Tool calling + `tool_choice`** — Claude mutlaka tool'u çağırır, input schema'ya uyar. En güçlü yöntem. (2) **JSON mode** (bazı modellerde) — response JSON olarak gelir ama şema zorlanmaz, Pydantic validation gerek. (3) **Prompt tuning + regex parse** — "JSON olarak döndür" + regex ile yakalama; zayıf, hata riskli. Production'da tool calling standart. Anthropic 2024-12 "Building Effective Agents" evaluator-optimizer pattern'inde tool calling kullanır.

### 17. Observability?

**Model cevap:** 3 boyut: log (ne oldu, discrete events), metric (ne kadar oldu, time series), trace (nasıl oldu, request path). Structured JSON log + trace_id middleware (FastAPI contextvars). Kritik metrikler: error rate, p95 latency, token/saat, maliyet/saat. Küçük proje `jq` + cron email; orta-büyük Grafana + Loki. PII maskeleme zorunlu (presidio). 24/7 agent için heartbeat + Uptime Kuma + Sentry — sessiz başarısızlık engeli.

### 18. Production deploy?

**Model cevap:** Dockerfile multi-stage + non-root + healthcheck. compose.yml `127.0.0.1` bind (Caddy reverse proxy HTTPS). CI/CD GitHub Actions: test + ruff + build + SSH deploy (systemctl restart). Secret management 4 katman (.env + GH Secrets + systemd EnvironmentFile + vault). Rollback prosedürü yazılı (git revert veya önceki docker tag). Pre-launch 15 maddeli checklist (Bölüm 8.6) — GO/NO-GO objektif karar.

## Davranışsal sorular — 6 soru (STAR)

**STAR formülü:** Situation (bağlam 1-2 cümle) + Task (görev 1 cümle) + Action (ne yaptın 3-4 cümle) + Result (sonuç rakamla 1-2 cümle).

### 19. Son 3 ayda öğrendiğin en büyük şey?

**Model cevap (STAR):**
- **S:** "9.4 RAG chatbot'umu kurarken ilk embedding sonuçları %60 irrelevant çıkıyordu."
- **T:** "Retrieval kalitesini %85+ çıkarmak gerekliydi yoksa proje kullanışsız."
- **A:** "Voyage AI dokümantasyonunu okuyup `input_type='document'` vs `'query'` ayrımını gördüm — document ile index'lendi ama query de document olarak embedding alıyordu. Bu asimetriyi düzeltince retrieval kalitesi sıçradı."
- **R:** "Retrieval precision %60'tan %85'e çıktı, kullanıcı deneyimi çok iyileşti. Bu ders: model dokümantasyonunu **pratikte** sorun çıkana kadar üzerinden geçmek atlama."

### 20. Yanlış karar verdiğin ve düzelttiğin bir örnek?

**Model cevap (STAR):**
- **S:** "9.5 Agent Otomasyon'u başta tüm model çağrıları için Sonnet 4.5 seçtim."
- **T:** "Aylık fatura $4.20 geliyordu, optimize etmem gerekiyordu."
- **A:** "Anthropic'in Building Effective Agents makalesinde 'heterogeneous model' pattern'ini okuyunca evaluator'ı Haiku'ya düşürdüm — puanlama basit karar, Sonnet overkill. Yazar Sonnet'ta kaldı, kalite kritik."
- **R:** "Aylık maliyet $2.60'a indi, %38 tasarruf. 10× ölçekte $15 farkı yapacaktı. Ders: 'bir model her şey için' refleksi yanlış; her görev için doğru model."

### 21. Takım arkadaşıyla anlaşamadığın teknik konu + çözüm?

**Model cevap (STAR):**
- **S:** "Bir arkadaş chatbot'a 'temperature 0.8' önerdi, kullanıcıya daha 'hayat dolu' gelsin diye."
- **T:** "Ben RAG tabanlı sistemde 0'a yakın istiyordum; sadakat için kritik."
- **A:** "Tartışma uzadı; 'test yapalım' dedim. 20 soru iki ayarla çalıştırdık; temperature 0.8'de 4 hallucination tespit ettik, 0.1'de 0. Örneklerle ikna oldu."
- **R:** "Temperature 0.1 ile canlıya çıktık. Ders: Teknik anlaşmazlıkta **test et**, teori üzerinden tartışma uzar."

### 22. En zor debug ettiğin sorun?

**Model cevap (STAR):**
- **S:** "9.4 canlıda sorgular bazen 30 saniye sürüyordu, bazen 1 saniye. Pattern yoktu."
- **T:** "Sorunu bulmalıydım çünkü p95 latency hedefi 2 saniyeydi."
- **A:** "Log'a trace_id + her adımın latency'sini ekledim. 3 gün sonra pattern gördüm: uzun cevaplar hep Claude streaming dönüşü, ama FastAPI response buffering'i kapamamıştım. `StreamingResponse` yerine `JSONResponse` kullanıyordum."
- **R:** "Streaming düzeltince p95 1.2 saniyeye düştü. Ders: 'bazen yavaş' sorunlarda **structured log + trace_id** olmadan bulamazsın."

### 23. Kendini son 12 ayda nasıl yetiştirdin?

**Model cevap:** Üç eksende ritim kurdum. (1) **Haftalık 3 saat öğrenme** — Pazartesi Anthropic News, Çarşamba 1 paper, Cuma 1 araç deneyi. (2) **Canlı proje** — sadece tutorial yeterli değil, 9.4 + 9.5 + semantic-search üç referans proje build ettim. (3) **Topluluk** — turkiye.ai Discord + Anthropic Discord aktifim, haftada 3-5 soru + 3-5 cevap. Öğrenme yalnızlıkta ölür; **paylaşım + pratik** canlı tutar. Kaynak kalite > miktar: 1-2 kaliteli kaynağa derinleş.

### 24. Neden Claude / Anthropic?

**Model cevap:** 3 sebep. (1) **Constitutional AI + dürüstlük refleksi** — Claude hallucination yerine "bilmiyorum" diyor; production sistemlerde bu altın. (2) **Model Spec + RSP şeffaflığı** — Anthropic'in davranış tanımı + scaling policy açık; müşteri "Claude nasıl karar verir" sorusuna spec'e yönlendirebilirim. (3) **Türkçe kalite** — Voyage + Claude ikilisinde Türkçe retrieval + cevap testlerim üstün sonuçlar verdi. OpenAI/Gemini iyi ama Anthropic'in ekosistem olgunluğu + şeffaflığı benim için belirleyici.

## Senaryo sorular — 6 soru

### 25. "100 müşteriye RAG chatbot yapacaksın, nereden başlarsın?"

**Model cevap:** Önce **ölçek varsayımları**: 100 müşteri × günlük 10 soru × 30 gün = 30K sorgu/ay; context ~3K token ortalama. Maliyet tahmini: Sonnet 4.5 ile ~$180/ay, Haiku + caching'le ~$50. Adımlar: (1) **MVP** — tek müşteriyle başla, 9.4 pattern'de FastAPI + Qdrant + Claude; (2) **multi-tenancy** — Qdrant collection per müşteri, isolation katmanı; (3) **admin panel** — müşteri PDF yükler, kendi verileri; (4) **billing** — kullanıcı başı token sayaç + aylık fatura; (5) **rate limit + hard cap** müşteri başı; (6) **production checklist** (8.6 15 madde) uygulama. İlk canlı 4 hafta; 100 müşteri 2-3 ay.

### 26. "Agent sistemi $500/ay, %30 düşür"

**Model cevap:** 5 optimizasyon aday: (1) **Heterojen model** — hangi çağrılar Sonnet, Haiku'ya düşürelebilir? Evaluator/classifier → Haiku (5× ucuz). (2) **Prompt caching** — system prompt sabit ise %90 indirim. (3) **Batch API** — offline raporlar için %50 indirim. (4) **Chunk optimizasyon** — retrieval'ı tighten, context küçült. (5) **Cache layer** — popular sorular Redis'te; cache hit'te LLM çağırma. Öncelik: cache layer + heterojen model en yüksek ROI. Ölçüm: 1 hafta log + maliyet breakdown per endpoint; en pahalı 3'ünü optimize. Beklenti: %30 hedef gerçekçi, $500 → $350.

### 27. "User PII sızdırdı, şimdi ne?"

**Model cevap:** **İlk 1 saat — acil**: (1) Incident log başlat (zaman + impact tahmini). (2) Sızıntı boyutu — kaç kullanıcı, ne tür PII, nereye gitti (log/ekrana/DB/üçüncü taraf)? (3) Kaynak izole — sızıntı kanalını kapat (endpoint kapat, deploy rollback). **İlk 24 saat — legal + kullanıcı**: (4) KVKK Kurumuna bildirim — 72 saat içinde zorunlu, hassas veriyse daha hızlı; KVKK Madde 12. (5) Etkilenen kullanıcılara email — şeffaf açıklama. **İlk hafta — düzeltme**: (6) presidio + log_safe() katmanı ekle; (7) audit 3 ay geriye dönük (benzer sızıntı var mı?); (8) post-mortem yaz + çıkarım kalem. **Önlem (gelecek)**: 8.1 sayfası 4 katman PII savunma, DB'de de maskeli sakla.

### 28. "Agent production'da sessiz ölüyor, debug?"

**Model cevap:** Sessiz ölüm = sistem çalışıyor ama output üretmiyor. Adımlar: (1) **Sentry/error log** kontrol — unhandled exception var mı? (2) **Heartbeat** — agent son ne zaman başarılı çalıştı? `last_success.txt` veya Uptime Kuma dashboard. (3) **Dead Letter Queue** — başarısız işler orada mı? Hata mesajı ne? (4) **External service health** — Anthropic status page + Qdrant ping + Voyage. (5) **Resource limits** — VPS disk/RAM dolu mu? (6) **Trace log** — son başarılı + ilk başarısız run log'ları trace_id karşılaştır. Çoğu kez: circular import, Anthropic 429 hiç handle edilmemiş, SQLite lock (iki cron aynı anda). Önlem (gelecek): 8.4 heartbeat + DLQ + Sentry zorunlu, 8.5 retry + circuit breaker.

### 29. "Fine-tuning mi RAG mi — müşteri için karar?"

**Model cevap:** Müşterinin verisini ve gereksinimini sormam gerek. Karar ağacı: (1) **Veri sık değişiyor mu?** Evet → RAG (FT yeniden eğitim her güncellemeyle pahalı). (2) **Kaynak alıntı gerekli mi?** Evet → RAG (FT alıntı veremez). (3) **Yapılacak iş stil/format mı kavram mı?** Stil (ton, markdown) → FT iyi; bilgi → RAG. (4) **Veri miktar?** <1000 örnek → RAG zorunlu; 10K+ → FT düşünülebilir. (5) **Latency kritik mi?** Çok → FT (RAG retrieval ekstra 100-300ms). (6) **Maliyet bütçesi?** Düşük → RAG; yüksek → her ikisi (FT + RAG hybrid). **Çoğu iş RAG ile başlar**, FT sonradan eklenir. "RAG first, FT when needed."

### 30. "Claude Sonnet outage, servisin çalışmalı — fallback planı?"

**Model cevap:** 3 seviye hazırlık: (1) **Fallback zinciri** — Sonnet down → Haiku'ya düş; kalite düşer ama servis çalışır. `MODEL_ZINCIRI = ["sonnet-4-5", "haiku-4-5"]` kod. (2) **Cache fallback** — son bilinen iyi cevap Redis'te; popüler sorular için LLM çağırma bile; outage'da bu yeter. (3) **Static fallback** — "Sistem yoğun, 5 dk sonra" insan okuyabilir cevap. **Monitor**: Anthropic Status Page webhook → Slack/Telegram. Circuit breaker (pybreaker) 5 fail → 60s açık; outage'da Anthropic'e istek bile göndermiyoruz. **Post-outage**: cache rebuild + fallback Haiku cevaplarını gözden geçir, kalite düşük olanları yeniden işle. Provider lock-in endişesi varsa **multi-provider** (OpenAI adapter) eklenebilir ama genelde overkill.

## Maaş müzakeresi — 3 refleks

### 1. Beklenti sayı ver

Recruiter "beklenti nedir?" dediğinde "görüşürüz" **yanlış** — seni düşük banttadan alır. **Sayı ver** ama aralıkla:

- **Junior AI Engineer:** 60K-100K TL/ay brüt (Türkiye 2026)
- **Mid AI Engineer:** 100K-180K TL/ay brüt
- **Remote global (USD):** Junior $50K-80K/yıl, Mid $80K-140K/yıl

1.2 Bölümündeki bant hatırla. Şehir + remote vs ofis + şirket büyüklüğü farkı büyük.

### 2. Total compensation

Maaş tek değişken değil — toplam paket: (1) base; (2) bonus (yıllık %10-30); (3) equity / stock (startup); (4) sigorta / özel sağlık; (5) uzaktan çalışma; (6) ekipman + ofis.

Base düşük + total yüksek olabilir. Recruiter'a "toplam paket nedir?" sor.

### 3. "Bu bandın neresindesiniz?"

Recruiter "60K-100K arasında pozisyon" dedi. Sen "100K tarafına yakın olacak diye düşünüyorum çünkü **2 canlı portföy + 3 referans proje + pytest testli kod**" diyerek somut neden ver.

**Kötü:** "Neden ya, sizi başkaları gibi ayırmayız?" (fiyat kırılır).
**İyi:** "100K-120K bandına bakıyorum; portföyüm + [X pozisyon önceki tecrübem] gerekçesiyle."

## Mülakatçıya sor — 5 soru

Mülakat sonunda "sorun var mı?" dediklerinde **sadece "yok"** deme — ilginizsiz görünürsün. 5 güçlü soru:

1. **"AI pipeline'ı production'a nasıl deploy ediyorsunuz? CI/CD + Docker + VPS veya cloud?"** — teknik ilgi + senin stack refleksin gösterir.
2. **"Bu pozisyondaki ilk 3 ay için somut başarı kriterleri ne?"** — somut hedef ilgisi + sana plan verir.
3. **"Ekipte AI Engineer sayısı ve senior/mid/junior dağılımı nasıl?"** — takımı ölçersin; tek AI Engineer'sen yalnız boğulursun.
4. **"Son 6 ayda bu ekipte çözdüğünüz en zor teknik sorun neydi?"** — ekibin seviyesi ortaya çıkar.
5. **"Öğrenmeye/konferanslara/kursa bütçe var mı? Açık kaynağa katkı destekleniyor mu?"** — sürekli öğrenme kültürü kontrolü.

## CTO tuzakları — 8 yaygın mülakat hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Ezberlenmiş cevap | Robot izlenim | Kendi projenden örnek |
| 2 | "Bilmiyorum" yerine uydurma | Trust kaybı | "Bilmiyorum, ama şöyle düşünürüm" |
| 3 | Tek kelimeyle yanıt | Pasif görünüm | En az 2-3 cümle + örnek |
| 4 | Mülakatçıya soru sormama | İlgisiz | 3-5 güçlü soru hazır |
| 5 | Maaş "görüşürüz" | Düşük banttan başlar | Sayı ver, aralıkla |
| 6 | Projeni övmek, hata söylememek | Abartılı | Post-mortem formatı (3 iyi + 3 kötü) |
| 7 | Teknik tartışmada ego | Çatışma izlenimi | "İyi nokta, ben şöyle düşünüyorum çünkü..." |
| 8 | Take-home'da overkill | Zaman aşımı | Basit + iyi test edilmiş > karmaşık + buggy |

## Anthropic ekosistemi — mülakat spesifik

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude kullanan şirketlerde mülakat</strong></summary>

Claude kullanan şirketlerde (Anthropic customers) mülakatta büyük olasılıkla şu sorular:

1. **"Claude Sonnet, Haiku, Opus hangisi ne zaman?"** — her modelin pricing + kullanım alanı net (Bölüm 2.5 özet).
2. **"Prompt caching'i kullanıyor musunuz?"** — %90 indirim bilmek.
3. **"Anthropic'in Building Effective Agents makalesini okudunuz mu?"** — EVET + kısaca 3 pattern (workflow-first, augmented LLM, orchestrator-workers).
4. **"Constitutional AI ne?"** — Claude'un etik eğitim mimarisi; Bölüm 8.2'de gördün.
5. **"MCP server yazdınız mı?"** — Bölüm 6.2 + 6.5 referans; "evet, X entegrasyonu için" net cevap.

### Anthropic'in kendi mülakatı

Anthropic'e doğrudan başvurursan (Applied AI Engineer rol) 5 aşama: recruiter → tech screen → take-home (AI sistem tasarımı) → onsite 4 round → offer. Take-home zor — 4-8 saat, production-level kod. Deep tech aşamada **derin sistem tasarımı** — "Claude-based RAG chatbot tasarla, 10M kullanıcı, aşağıdaki constraint'lerle...". Güncel referans: Anthropic Careers blog post'ları + ex-Anthropic mühendislerin blog'ları (Simon Willison, Andrej Karpathy).

**Gerçekçi değerlendirme:** Anthropic direkt 2026 itibarıyla **senior+** bias — junior pozisyon az. 2-3 yıl production AI engineering sonra güçlü. Öncesi: Claude kullanan customer şirket (Notion, Zapier, Replit vb) → 2 yıl → Anthropic geçişi.

</details>

## Görev — 2 saat kendi cevabını yaz

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — 30 sorudan 10'una kendi cevap</div>

1. Bu sayfanın 30 sorusundan **en olasılıklı 10'unu** seç (teknik 6 + davranışsal 2 + senaryo 2).
2. Her birine **kendi projenden örnek** ile cevap yaz (4-6 cümle).
3. Davranışsal için **STAR formatı** uygula.
4. `muhendisal-notlarim/bolum-10/02-mulakat/kendi-cevaplarim.md` dosyasına commit.
5. 2-3 gün sonra tekrar oku — daha iyi örnek aklına gelir, revize et.
6. Mülakat öncesi gece **5 cevabı yüksek sesle** pratik et.

**Başarı kriteri:** 2 saat sonunda 10 sorunun kendi cevabı yazılı. Bir arkadaşa gönder, "3 cümleyle ne yaptığını anlıyor muyum?" testi yap.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

- **A → B:** Mülakat süreci tipik 3-5 aşama; teknik + davranışsal + senaryo karışık.
- **B → C:** 18 teknik soru — prompt/token/RAG/embedding/agent/MCP/tool calling/deploy ekseninde; her biri kısa paragraf + senin projenden örnek.
- **C → D:** 6 davranışsal soru STAR formatı; Situation + Task + Action + Result sıra + rakam.
- **D → E:** 6 senaryo soru — "X şirket durumu, ne yaparsın?"; sistem tasarımı + trade-off refleksi.
- **E → F:** Maaş müzakeresi sayı ver + total compensation + bandın üstü çek; "görüşürüz" yanlış.
- **F → G:** Mülakatçıya 5 soru hazır; pasif dinleme değil aktif sorgulama.
- **G → H:** 8 CTO tuzak; ezber yerine örnek, yalan yerine "bilmiyorum", tek kelime yerine paragraf.

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** 30 soruya model cevap hazır. Senin işin kendi projenden **somut örnek** ile kişiselleştirmek — ezber değil refleks. Sonraki (10.3): açık kaynak katkı; PR atarken referans inşası.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[10.3 Açık Kaynak Katkı →](03-acik-kaynak.md)** — İlk PR stratejisi + Anthropic Cookbook + Qdrant/LangChain + commit hygiene.

← [10.1 LinkedIn Strateji](01-linkedin.md) &nbsp;|&nbsp; [Bölüm 10 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [Interviewing.io AI/ML mock interviews](https://interviewing.io/) + [Educative System Design for ML](https://www.educative.io/) + [Pramp ücretsiz peer mock](https://www.pramp.com/). Bir arkadaşla haftada 1 mock görüşme — gerçeğe en iyi hazırlık.
</div>
