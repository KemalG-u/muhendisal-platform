# 5.2 Karar Ağacı — RAG mı, İnce Ayar mı?

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~30 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 5.1 okundu (prompt ↔ RAG ↔ ince ayar üçgeni + 3 ince ayar biçimi + maliyetler).</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> **10 kriterli karar ağacı** elinde; yeni proje geldiğinde 5 dakikada "prompt / RAG / ince ayar / hibrit" kararını **gerekçeli** verebiliyorsun. 5 somut senaryo (müşteri destek, hukuki doküman, tıbbi tanı, finansal analiz, yaratıcı yazım) üzerinde pratik uyguladın. Mülakattaki "İnce ayar mı, RAG mi?" sorusuna (10.2) derinleşmiş cevap. **Bölüm 5'in karar-odaklı sayfası.**</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **Concept drift (kavram kayması)** = verinin zamanla değişmesi; bu ayın müşteri sorusu geçen yılın sorusundan farklı. **Latency budget (gecikme bütçesi)** = uygulamanın cevap süresi bütçesi; chatbot 2-3 sn, batch ajan 30 sn tolere eder. **Cold start (soğuk başlangıç)** = ilk kullanıcı için modelin yüklenme/açılma süresi. **Staleness (bayatlık)** = modelin güncel olmaması; RAG'de parça (chunk) güncel kalır, ince ayar modeli eğitildiği günden sonra "donuk" olur. **Hibrit (hybrid)** = RAG + ince ayar birlikte; genellikle ince ayar ton/stil için, RAG bilgi için.

## Neden bu sayfa?

5.1'de kavramları gördün. Bu sayfa o kavramları **karara** dönüştürür. Müşterin geldi: *"Bana hukuki doküman analizi sistemi kur."* Nereden başlarsın?

AI Engineer'ı yeni başlayandan ayıran nokta: **doğru soru sorma refleksi.** Bu sayfa 10 kriterli soru listesi verir — her biri kararı daraltır. 10 dakika sonra müşterine: *"Sizinki için RAG + prompt mühendisliği yeter; ince ayara **şu noktada** ihtiyaç olursa geri dönelim"* diyebiliyorsun.

İkincisi: Mülakat sorusu olarak doğrudan çıkar. 10.2 sayfasında "İnce ayar mı, RAG mi?" sorusu vardı; bu sayfa o cevabı derinleştirir. Senaryo soruları için (10.2'deki senaryo 29) somut cevap şablonu.

Üçüncüsü: Bu sayfa **imza niteliğinde** — Bölüm 5'in karar-odaklı sayfası. Index'te 🏁 işaretli. 5.4 pratik imzası (Colab'de LoRA), 5.2 kavramsal imzası (karar refleksi).

## 10 kriterli karar soruları

Yeni proje için sırayla sor:

### 1. Veri değişim sıklığı

**Soru:** Model görevinin **bilgisi** ne sıklıkta değişir?

| Sıklık | Kategori | Tercih |
|---|---|---|
| Saat / gün | Fiyat, stok, haber | **RAG** (ince ayar anlık güncellenemez) |
| Hafta | Müşteri kataloğu, doküman | **RAG** |
| Ay | Ürün kılavuzu | RAG veya hibrit |
| Yıl | Şirket stili, tıp kurallarının temeli | İnce ayar düşünülebilir |
| Hiç | Matematik sabitleri | Model zaten biliyor, hiçbiri gereksiz |

**Altın kural:** Veri ayda 1'den sık değişiyorsa **RAG**. İnce ayarda her güncellemede yeniden eğitim = sürdürülemez.

### 2. Kaynak alıntı gereksinimi

**Soru:** Kullanıcı cevabın **hangi belgeye** dayandığını görmeli mi?

- **Evet:** Hukuk, tıp, finans, akademi → **RAG** zorunlu. İnce ayarlı model "şu sayfadan" bilgi veremez (kaynak ile bilgi içselleştirilmiştir).
- **Hayır:** Günlük chatbot, stil değiştirme → ince ayar veya prompt.

Kaynak alıntı = RAG'in **yapısal avantajı**. Hiçbir ince ayar bu açığı kapatmaz.

### 3. Veri miktarı

**Soru:** Elinde kaç kaliteli örnek var?

| Örnek sayısı | Tercih |
|---|---|
| **0-50** | Prompt mühendisliği + few-shot (ince ayar yetersiz, ezberler) |
| **50-500** | Prompt + RAG |
| **500-2000** | RAG veya küçük LoRA |
| **2000-10.000** | LoRA/QLoRA anlamlı |
| **10.000+** | İnce ayarı ciddi düşün; sürekli ön-eğitim (continued pre-training) ihtimali |

### 4. Davranış mı bilgi mi?

**Soru:** Sorun ne?

| Sorun | Tercih |
|---|---|
| "Model **bilmiyor**" (yeni ürün, içine eklenmemiş bilgi) | **RAG** |
| "Model **yanlış söylüyor**" (stil, ton, format) | **İnce ayar** |
| "Model **yapmıyor**" (tool çağırmıyor, format dışında cevap veriyor) | Prompt mühendisliği + tool calling |

**Örnek ayrımı:**

- "Model 'müşteri' diyor, biz 'ürün sahibi' diyoruz" → **İnce ayar** (ton)
- "Model şirketin iade politikasını bilmiyor" → **RAG** (bilgi)
- "Model JSON dönüş formatına uymuyor" → **tool_choice** (prompt)

### 5. Latency bütçesi

**Soru:** Uygulaman ne kadar hızlı cevap vermeli?

- **<500 ms** (sesli ajan, gerçek zamanlı): **İnce ayar** (retrieval ek yükü yok) veya küçük model
- **500 ms - 3 sn** (chatbot, akış): **RAG** uygun (retrieval 100-300 ms)
- **>3 sn** (toplu iş, ajan): Her ikisi de olur

RAG retrieval bir ek adım (embedding hesapla + Qdrant sorgu + bağlam ekle). Toplam gecikme 300-500 ms artar. Kritik durumda ince ayar veya cache.

### 6. Maliyet bütçesi

**Soru:** Aylık AI bütçesi?

| Aylık bütçe | Tercih |
|---|---|
| **<$50** | Prompt + hafif RAG + Haiku 4.5 ($1/$5) |
| **$50-500** | RAG + Sonnet 4.6 ($3/$15) + prompt caching |
| **$500-5000** | RAG (Opus 4.7 — $5/$25) veya QLoRA self-host |
| **$5K+** | İnce ayar + self-host geniş kapsamlı düşün |

**İnce ayarın gizli maliyeti:** GPU çıkarımı (inference). Bulutta A100 80 GB ayda ~$300-500 (saatlik ~$1.5-2 × yarım gün); Anthropic API'siyle aynı yükü ~$100/ay tutar. İnce ayar %80+ kesintisiz kullanılırsa kendini karşılar; yoksa maliyet artar.

### 7. Domain spesifiklik

**Soru:** Sorun ne kadar niche?

- **Genel bilgi** (özet, çeviri, soru-cevap): Claude zaten üstün → prompt yeter
- **Orta niş** (hukuk, tıp, finans): **RAG** kaynaklarla zenginleştir
- **Derin niş** (molecular biology terimleri, maritime law TR): FT veya hybrid

Claude + Voyage **çoğu niş**'te İngilizce ve Türkçe'de iyi. FT'ye atlamadan önce RAG + zengin kaynak + few-shot dene.

### 8. Bakım kapasitesi

**Soru:** Modeli **canlı tutmak** için kaç kişi ayırırsın?

- **Solo (sen):** RAG çok daha kolay. Qdrant + embedding = 1 haftada kurulur, ayda 1 saat bakım.
- **2-3 kişi:** LoRA/QLoRA mümkün, aylık retrain döngüsü.
- **5+ kişi / ML team:** Tam FT + continuous training düşünülebilir.

**Solo için altın kural:** FT'ye girme. Sürdürülemez. 6 ay sonra model "çürür" (concept drift) ve yeniden eğitim için zaman yok.

### 9. Veri sahipliği + gizlilik

**Soru:** Veri nerede kalmalı?

- **Bulut tamam** (KVKK uyumu varsa): Claude + Qdrant Cloud → kolay.
- **Yerinde (on-prem) zorunlu** (sağlık, savunma): Kendi sunucunda Qdrant + kendi sunucunda model (Llama / Qwen / DeepSeek). İnce ayar muhtemelen gerekli — API kullanamazsın.
- **Hibrit:** Hassas veri yerinde (embedding yerinde), LLM bulutta (anonimleştirilmiş prompt).

Yerinde + API kullanmaya direnç yüksekse ince ayar + kendi sunucunda Llama/Qwen tek seçenek.

### 10. Geri alınabilirlik

**Soru:** Yanlış giderse ne kadar hızlı düzeltebilirsin?

- **Prompt** — 1 dakikada `git commit` ile geri al.
- **RAG** — parçaları (chunks) yeniden indeksle, 1 saatte geri al.
- **İnce ayar** — eski adaptörü yükle + yeni eğitim başlat; gün veya hafta sürer.

**Kritik:** İnce ayar "iade edilemez" değil ama "yavaş iade." Üretimdeki bir hata 3 gün kalıcı olursa müşteri kaybedebilirsin.

## Karar ağacı — görsel

<div class="ma-ekosistem" markdown>
<div class="ma-ekosistem-header">🗺️ 5-dakikalık karar ağacı</div>

```mermaid
flowchart TB
    START["🆕 Yeni AI projesi"]

    Q1{"Veri ayda 1'den\nsık değişiyor mu?"}
    Q2{"Kaynak alıntı\ngerekli mi?"}
    Q3{"Davranış mı\nbilgi mi?"}
    Q4{"Bakım için\n5+ kişi var mı?"}
    Q5{"Bütçe $5K+/ay mı?"}

    PROMPT["🎯 Prompt Engineering\nyeter"]
    RAG["📚 RAG"]
    RAG_PROMPT["📚 RAG + Prompt\ncaching"]
    FT_LORA["🔧 LoRA/QLoRA\ndene"]
    HYBRID["🔀 RAG + FT\n(ileri)"]

    START --> Q1
    Q1 -->|Evet| RAG
    Q1 -->|Hayır| Q2
    Q2 -->|Evet| RAG
    Q2 -->|Hayır| Q3
    Q3 -->|Bilgi| RAG_PROMPT
    Q3 -->|Davranış/Stil| Q4
    Q3 -->|Her ikisi| HYBRID
    Q4 -->|Hayır| PROMPT
    Q4 -->|Evet| Q5
    Q5 -->|Evet| FT_LORA
    Q5 -->|Hayır| PROMPT

    classDef q fill:#dbeafe,stroke:#2563eb,color:#111
    classDef result fill:#fef3c7,stroke:#ca8a04,color:#111
    classDef warning fill:#fef3c7,stroke:#ca8a04,color:#111
    classDef advanced fill:#fed7aa,stroke:#ea580c,color:#111
    class Q1,Q2,Q3,Q4,Q5 q
    class PROMPT,RAG,RAG_PROMPT result
    class FT_LORA warning
    class HYBRID advanced
```

**Ağacın mesajı:** 5 "evet/hayır" sorusu → karar. Çoğu yol **RAG veya prompt**'a çıkıyor — FT sadece çok spesifik koşulların birleşimi.

</div>

## 5 senaryo — pratik uygulama

### Senaryo 1 — Müşteri destek chatbot'u

**Durum:** E-ticaret şirket, günlük 500 müşteri soru. Sipariş takibi + iade + kargo + ürün bilgisi.

**Kriter uygulama:**
- Veri değişim: günlük (sipariş durumu değişir) → **RAG**
- Kaynak: "Sipariş #X şuradan aldık" gerek → **RAG**
- Davranış/bilgi: **bilgi** (ürün + sipariş) → **RAG**
- Bakım: solo dev → **RAG kolay**
- Gizlilik: bulut OK (KVKK form) → **RAG kolay**

**Karar: RAG + prompt engineering.** Sipariş veritabanı real-time; ürün katalogu Qdrant'ta; Claude Sonnet cevap. FT gerekmez.

### Senaryo 2 — Hukuki doküman analizi

**Durum:** Hukuk bürosu, avukat sözleşmeleri yüklüyor, risk analizi istiyor.

**Kriter uygulama:**
- Veri: sözleşme değişir, yasa değişir (nadiren) → **RAG**
- Kaynak alıntı: **kritik** — "Madde 3'te riskli" demek gerek → **RAG**
- Davranış: Avukat jargonu → **prompt + few-shot** yeter
- Gizlilik: müşteri sözleşmesi hassas → KVKK rıza + şifreleme ama API OK

**Karar: RAG + Claude Sonnet + kapsamlı system prompt.** Yasalar + sözleşmeler ayrı Qdrant collection. Reference + line number gönderme zorunlu.

### Senaryo 3 — Tıbbi tanı asistan (araştırma)

**Durum:** Radyoloji bölümü, X-ray + röntgen raporu yazım asistanı. Sadece **araştırma ortamı**, son karar radyolog.

**Kriter uygulama:**
- Veri: tıbbi literatür (yıllık güncellemeler) + hastane protokolleri
- Kaynak alıntı: zorunlu — tıp etiği
- Davranış: radyolog tonu + rapor biçimi
- Gizlilik: yerinde (on-prem) zorunlu (HIPAA / KVKK özel nitelikli veri)
- Bütçe: araştırma projesi, uygun

**Karar: Hibrit (RAG + LoRA ince ayar) kendi sunucunda.** Llama 3.1 70B veya Llama 4 Scout kendi sunucunda; radyolog raporu biçimi için LoRA (500 örnek); tıp literatürü Qdrant RAG; yerinde. İnce ayar ton için, RAG bilgi için. **Karmaşık proje; 3-6 aylık iş.**

### Senaryo 4 — Finansal analiz (kişisel proje)

**Durum:** Kendi kişisel gelir-gider takibi + bütçe önerisi. Sadece senin verin.

**Kriter uygulama:**
- Veri: kişisel, günlük değişir → **RAG** veya direkt prompt
- Kaynak alıntı: yok (kişisel, sen zaten görürsün)
- Davranış: samimi dil OK → prompt
- Bakım: yalnız sen → **minimal**
- Bütçe: düşük → Haiku

**Karar: Prompt engineering + Claude Haiku + günlük CSV.** Hayır, RAG bile gereksiz — CSV prompt'a direkt yapıştır. 200-satır Python script, tek dosya, ayda $2.

### Senaryo 5 — Yaratıcı yazım — "Ahmet Ümit tonunda polisiye roman üret"

**Durum:** Roman yazarı, Ahmet Ümit'in 10 romanını verdi, benzer ton istiyor.

**Kriter uygulama:**
- Veri: sabit (10 roman, değişmez) → ince ayar uygun
- Kaynak alıntı: **yok** (yaratıcı eser)
- Davranış: **ton + stil değişimi** → **ince ayarın kullanım alanı**
- Gizlilik: eser telifli; edebi taklit (pastiche) için eğitim hukuki gri bölge — ticari için TELİF SAHİBİNDEN İZİN şart
- Bütçe: hobi → düşük

**Karar: QLoRA + Llama 3.2 1B veya Qwen 3-1.7B (Türkçe iyi) + 200-300 örnek paragraf.** Colab T4/L4 ücretsiz katmanı, 3-4 saat eğitim, $0. **Telif uyarısı (ciddi):** Telifli eserle eğitilmiş model **ticari** kullanılırsa yazarın ya da yayınevinin dava açma hakkı vardır (2024-2025'te ABD'de bu yönde davalar açıldı). Sadece **kişisel deney + paylaşmama** koşuluyla yap.

**Alternatif (daha basit):** Claude Sonnet 4.6 + 20 Ahmet Ümit paragrafı few-shot + prompt caching. Kalite yetmezse LoRA.

## Hybrid yaklaşım — ileri kullanım

RAG + FT birlikte. Amaç: FT ton/stil/format, RAG bilgi.

### Mimari

```
[Kullanıcı sorusu]
     ↓
[RAG retrieval] ← Qdrant: bilgi kaynakları
     ↓
[Fine-tuned Llama] ← LoRA adapter: ton/stil/format
     ↓
[Cevap (müşteri tonunda + doğru bilgi)]
```

### Hybrid'in maliyeti

- **Compute:** GPU self-host (Llama + adapter) veya Anthropic + FT başka platform
- **Complexity:** 2 sistem bakımı (RAG index + LoRA adapter)
- **Bakım:** her ikisinin de kendi refresh döngüsü

### Hybrid ne zaman?

- Hukuk/tıp gibi **kaynak alıntı + sektör dili** ikisi birden gerekli
- Banka müşteri destek — stil şirket kimliği + veri gerçek zamanlı
- Çok-dilli + domain spesifik sistem (tıp İngilizce + Türkçe)

**Çoğu projede gerekmez.** Hybrid "gösterişli" ama bakım yükü çifte.

## CTO tuzakları — 8 karar hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Sadece trende göre karar | "İnce ayar popüler" diye seçmek → maliyet patlar | 10 kriteri sırayla uygula |
| 2 | İlk denemede hibrit | 2 sistem bakımı + karmaşık | Önce tekil, yetmezse hibrit |
| 3 | Prompt denemeden RAG'e geç | Gereksiz Qdrant kurulumu | Prompt + few-shot önce |
| 4 | RAG denemeden ince ayara geç | $500-$5K gereksiz | RAG 1 haftada sonuç verir; ince ayar 4 haftada |
| 5 | "Müşteri ince ayar istedi" = ince ayar | Müşterinin teknik bilgisi eksik | Gereksinim analizi yap + sen karar ver |
| 6 | Tek senaryo için 3 saatlik karar tartışması | Boşa zaman | 10 kriter + 5 dakika yeter |
| 7 | Karar sonrası sorgulama yok | 3 ay sonra yanlış anlaşılır | 1 aylık kontrol noktası koy |
| 8 | "Hibrit en iyisi" refleksi | Gereksiz karmaşıklık | Tekil yetiyorsa tekil |

## Anthropic ekosistemi — karar öncesi sorgular

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude + RAG + tool'a özel kalibre</strong></summary>

Claude kullanıyorsan karar ağacının **RAG** yolu %80+ olasılıkla sonuç. Sebepleri:

### 1. 1M bağlam + prompt caching

Claude Sonnet 4.6 ve Opus 4.7 = 1M token bağlam (Haiku 4.5 = 200K). Prompt caching (Kasım 2024'ten beri) ile sistem promptunun cache okuma maliyeti yaklaşık base × 0.1 (%90 düşüş). **Büyük few-shot örnek seti** (50-100 örnek, 10K+ token) sistem promptuna rahat sığar; her istekte cache'den okunur. Bu **"mini ince ayar"** gibi çalışır — model parametreleri değişmez ama bağlamda tutarlı örnekler kalır.

### 2. Tool calling — davranış kilidi

`tool_choice={"type":"tool","name":"X"}` ile Claude cevabı kesin JSON şemasına uyar. FT'nin "format değişikliği" ihtiyacının %80'ini karşılar. Bölüm 6.2 + 8.1 referans.

### 3. Extended thinking (2025+)

Claude'un reasoning modu karmaşık problemlerde adım adım düşünür; FT ile yapılmaya çalışılan "reasoning kapasitesi" artışının bir kısmını karşılar. Platform'da Bölüm 4.7/4.8 civarında değindi.

### 4. Constitutional AI tutarlılığı

Claude "kötü karar" vermeme refleksine sahip. FT bu refleksi bozabilir. Claude hybrid'te cloud tarafı + self-host Llama'yı FT için kullan — Claude Constitutional rolü (güvenli cevap filter), Llama domain rolü.

### 5. Pratik karar

"Claude + RAG + tool calling" %85 projeye uyar. Kalan %15'te:

- Ton/stil değişimi kritik → Llama/Qwen LoRA
- On-prem zorunlu → self-host Llama
- Kosulsuz latency <500ms → küçük self-host model

**Claude projen için karar ağacı eğik RAG tarafına.** 5.1'de Anthropic public FT yok dedim; bu eksik değil, sistem tasarımı teşvik.

### Model seçimi içinde karar

Proje ince ayar gerektiriyorsa:

| Senaryo | Öneri |
|---|---|
| Türkçe yaratıcı | Llama 3.2 1B/3B veya Llama 3.1 8B |
| Türkçe + kod | Qwen 3-1.7B / Qwen 3.5-7B |
| Çok dilli | Mistral Nemo 12B veya Mistral 7B |
| Küçük (mobil) | Gemma 3 2B / 9B / 27B |
| Akıl yürütme yoğun | DeepSeek V3.2 (671B / 37B aktif MoE) |
| Açık ağırlıklı yeni nesil | Llama 4 Scout (17B aktif / 109B toplam) |

Hepsi açık ağırlıklı + HuggingFace'te erişilebilir + LoRA/QLoRA uyumlu.

</details>

## Çıktı kanıtları — 3 kanıt

<div class="ma-cikti-kaniti" markdown>
<div class="ma-cikti-kaniti-header">📏 Çıktı — 3 kanıt</div>

**1. 10 kriter özeti:**

Tek sayfa (not defterinde veya `notlarim/bolum-5/02-karar/10-kriter.md`): her kriter + karar yönü. 5 dakika tekrar hatırlama için referans.

**2. Kendi 3 projesini karar ağacına koy:**

9.4 RAG Chatbot + 9.5 Agent + 5.4 FT Deneyi (bir sonraki sayfada yapacağın) için karar ağacı yürüt. Hangi dalda? Neden?

**3. Müşteri sorusu için karar:**

Bir arkadaş veya kendi düşündüğün bir proje — "AI sistemi istiyorum" dediğinde 5 dakika içinde karar ağacı uygula + sonucu yaz.

**Kanıt klasörü:** `muhendisal-notlarim/bolum-5/02-karar/`

</div>

## Görev — 45 dk üç karar yaz

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — karar ağacını 3 projede uygula</div>

1. **Proje A:** Kendin için — 9.4 RAG Chatbot + 5 soru (10 kriterden) — karar zaten RAG, ama **nedenini** yaz.
2. **Proje B:** Hayali senaryo — "Türkiye bir avukat grubu için yasa + içtihat arama sistemi" — karar ağacı uygula + gerekçe 3 paragraf.
3. **Proje C:** Senin niş ilgin — kendi seçtiğin bir domain (oyun, müzik, finans, eğitim...) — "X için AI asistan" + karar.
4. `muhendisal-notlarim/bolum-5/02-karar/kararlar.md` dosyasına commit.
5. Mülakatta "FT mi RAG mi?" sorusuna bu 3 karardan **1 tanesini** örnekle anlatırsın.

**Başarı kriteri:** 45 dakika sonunda 3 proje için gerekçeli karar yazılı. Karar ağacı refleksin sağlam.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**A → B:** AI Engineer'ı junior'dan ayıran: doğru soru sorma + karar refleksi. Bu yüzden **karar çerçevesi kod yazmaktan önce gelir.**</li>
<li>**B → C:** 10 kriter: değişim sıklığı + kaynak + veri + davranış/bilgi + latency + maliyet + niş + bakım + gizlilik + geri alınabilirlik. Bu yüzden **tek kriter yetmez.**</li>
<li>**C → D:** Karar ağacı 5 soruda sonuç; çoğu yol RAG veya prompt'a çıkar. Bu yüzden **FT nadir seçilen seçenek.**</li>
<li>**D → E:** 5 senaryo (müşteri destek, hukuk, tıp, kişisel finans, yaratıcı); her birinde karar ağacı uygulandı. Bu yüzden **soyut kural somut senaryoda pekişir.**</li>
<li>**E → F:** Hybrid (RAG + FT) ileri seviye; tekil yetiyorsa tekil; hukuk/tıp büyük projelerde anlamlı. Bu yüzden **karmaşıklık ancak zorunluysa eklenir.**</li>
<li>**F → G:** Claude kullanıyorsan karar ağacı %80+ RAG'e çıkar; FT gerekiyorsa Llama/Qwen self-host. Bu yüzden **provider seçimi karar ağacını etkiler.**</li>
<li>**G → H:** 8 CTO tuzak; en yaygını 'ilk denemede hybrid' ve 'müşteri FT dedi diye FT'. Bu yüzden **talepten değil, gereksinimden hareket et.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Karar refleksi kuruldu. Yeni proje için 5 dakika → karar. Sonraki (5.3): LoRA + QLoRA matematik sezgi — eğer FT'ye girersen ne yapıyorsun.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[5.3 LoRA ve QLoRA →](03-lora.md)** — matris ayrıştırma sezgisi + 4-bit quantization + hangi GPU için hangisi.

← [5.1 Fine-tuning Nedir](01-finetune-nedir.md) &nbsp;|&nbsp; [Bölüm 5 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [OpenAI fine-tuning docs](https://platform.openai.com/docs/guides/fine-tuning) + [Anthropic Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) + [HuggingFace Smol Course](https://huggingface.co/learn/cookbook). Üç farklı bakış: sağlayıcıya özel + çerçeve bağımsız + uygulamalı.
</div>
