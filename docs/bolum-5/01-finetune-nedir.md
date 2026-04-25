# 5.1 İnce Ayar (Fine-tuning) Nedir — Tam FT, LoRA, QLoRA

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~35 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> Bölüm 2 (prompt engineering) + Bölüm 4 (RAG) bitti. Çalışan bir RAG sistemin var.</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> İnce ayarın 3 biçimini (tam FT, LoRA, QLoRA) biliyorsun; **prompt mühendisliği ↔ RAG ↔ ince ayar** üçgeninde her köşenin ne zaman seçildiğini anlıyorsun; maliyet + süre + donanım gerçekçi tahminleri elinde. Sayfadaki tek iddia: "Çoğu proje ince ayar **gerektirmez**" — bu iddianın arkasındaki gerekçeyi görebiliyorsun.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **İnce ayar (fine-tuning)** = önceden eğitilmiş modelin ağırlıklarını kendi verinle güncelleme. **Tam ince ayar (full FT)** = tüm ağırlıklar değişir; pahalı. **LoRA** (Low-Rank Adaptation — düşük dereceli uyarlama) = sadece küçük adaptör katmanlar eğitilir; orijinal model donuk kalır. **QLoRA** = LoRA + 4-bit küçültme (quantization); tüketici GPU'da bile çalışır. **PEFT** (Parameter-Efficient Fine-Tuning — verimli parametreli ince ayar) = LoRA/QLoRA/Prefix tuning gibi tekniklerin şemsiye adı. **Instruction tuning (talimat ayarı)** = "Kullanıcı sorar, model cevap verir" formatına modeli öğretmek. **RLHF** (Reinforcement Learning from Human Feedback) = insan geri bildirimiyle hizalama.

## Neden bu bölüm?

Bölüm 4'te RAG kurdun. Projede bir sınır gördün: *"Bu model Türkçe'de bazı kültürel ayrıntıları tam yakalamıyor"* ya da *"Bizim şirket dilinde 'müşteri' yerine 'ürün sahibi' diyoruz, model bu dili benimseyemiyor"*. Çözüm olarak **"modeli kendi verimle eğitsem?"** sorusu aklına geldi.

Bu bölümün ana tezi: **ince ayar pahalı bir yol, RAG ucuz bir yoldur.** "Kendi modelimi eğittim" hikâyesi mülakatta ya da LinkedIn'de cazip görünür. Ama **çoğu projede maliyet + zaman + bakım üçlüsü RAG'e göre 10-100 katı çıkar.** Bu bölümün 4 sayfası, sen bu karar noktasında doğru tarafa düşesin diye yazıldı.

İkincisi: İnce ayar 2026'da daha ucuz — 2024-2025'te **LoRA + QLoRA** teknikleriyle **tüketici GPU**'da (RTX 4090, RTX 5090, Colab T4/L4) bile büyük modeller eğitilebiliyor. Maliyet eşiği düştü. Ama düşen eşik **"her projeye uyar"** demek değil. 5.2 karar matrisi bu sınırı çizer.

Üçüncüsü: Bu bölüm **platformun kavramsal son bölümü** (teknik temel anlamında). Sonraki bölümler (Bölüm 7 Multimodal, Bölüm 9.6 imza projesi, Bölüm 10 kariyer) uygulama-odaklı. 5.4 HF pratik sayfasında küçük bir LoRA deneyimi yapacaksın — deneyim için, üretim için değil.

## 3 köşeli üçgen — Prompt ↔ RAG ↔ Fine-tune

AI Engineer'ın "modele yeni şey öğretme" araç kutusu 3 parça:

<div class="ma-ekosistem" markdown>
<div class="ma-ekosistem-header">🗺️ 3 teknik, 3 farklı problem</div>

```mermaid
flowchart TB
    PROBLEM[❓ "Model istediğim gibi davranmıyor"]

    subgraph PROMPT["1️⃣ Prompt Engineering"]
        P1[System prompt + few-shot]
        P2[Dakikalar, 0 maliyet]
        P3[Örnek az, etki sınırlı]
    end

    subgraph RAG["2️⃣ RAG"]
        R1[Vector DB + retrieval]
        R2[Saatler, düşük maliyet]
        R3[Bilgi ekler, davranış değişmez]
    end

    subgraph FT["3️⃣ Fine-tuning"]
        F1[Model ağırlıkları günceller]
        F2[Günler, yüksek maliyet]
        F3[Davranış değişir, bakım sürekli]
    end

    PROBLEM --> PROMPT
    PROBLEM --> RAG
    PROBLEM --> FT

    classDef prompt fill:#fef3c7,stroke:#ca8a04,color:#111
    classDef rag fill:#dbeafe,stroke:#2563eb,color:#111
    classDef ft fill:#fed7aa,stroke:#ea580c,color:#111
    class P1,P2,P3 prompt
    class R1,R2,R3 rag
    class F1,F2,F3 ft
```

**Üçü aynı probleme farklı cevap verir.** Doğru eşleşme:

| Sorun tipi | Çözüm |
|---|---|
| "Model cevap formatını bilmiyor" | Prompt engineering (few-shot örnek) |
| "Model benim şirket verimi bilmiyor" | RAG |
| "Model benim ürün jargon'umu bilmiyor (1000 kere öğretmek zor)" | Fine-tune |
| "Model Türkçe üretim yapıyor ama TDK standardı yerine argo kullanıyor" | Fine-tune (stil) |
| "Model sağlık kaynaklarını tıp doktoru tonunda söylesin" | Fine-tune (ton) + RAG (kaynak) = hybrid |

</div>

## Fine-tuning nedir — 3 biçim

### 1. Tam ince ayar (full fine-tuning)

Modelin **tüm ağırlıkları** güncellenir. (Claude'un parametre sayısı resmi olarak açıklanmaz; sızıntı/spekülasyon değerleri kullanılmaz.) Tam ince ayar için:

- **Donanım:** 8+ H100 GPU kümesi (tek başına $200K satın alma; bulutta saatlik $40-60/H100)
- **Veri:** 10K+ kaliteli örnek (az ise modelin ezberlemesi — overfitting)
- **Süre:** Saatler-günler
- **Maliyet:** Compute + veri + tekrar eğitim ≈ $5K-1M arası proje
- **Kim yapar:** Anthropic, OpenAI, Google, Meta, büyük kurumsal ekipler

**Çoğu geliştiricinin asla dokunmayacağı yöntem.** Sadece model üreticileri.

### 2. LoRA — Düşük Dereceli Uyarlama (2021)

Temel fikir: Model ağırlıklarını **dondur**, **küçük adaptör katmanlar** ekle, sadece onları eğit.

**Matematik sezgisi (formül yok):**

Bir ağırlık matrisini iki **küçük matrisin çarpımı** olarak yaklaş — "rank" denen düşük bir boyutta. Orijinal 1000×1000 matrisin yerine 1000×8 + 8×1000 = iki küçük matris tutarsın. **Eğitilebilir parametre sayısı orijinalin %1-2'sine düşer** (rank 8 için).

Pratikte:

- **Donanım:** Tek A100 veya RTX 4090/5090 (24-32 GB VRAM)
- **Veri:** 500-5000 örnek yeter
- **Süre:** 1-4 saat
- **Maliyet:** Colab Pro A100 (~$1.20/saat) ya da RunPod A100 (~$1.50-2/saat) ile $5-30/deney (2026 fiyatları)
- **Dosya:** Adaptör ağırlıkları ~10-50 MB (orijinal model 16 GB Llama 3.1 8B / 140 GB Llama 3.1 70B)

**Büyük fayda:** Farklı görevler için ayrı adaptör tut, aynı temel modeli paylaş. 10 farklı tonun varsa 10 adaptör + 1 temel model = 16-140 GB + 500 MB.

### 3. QLoRA — Küçültülmüş LoRA (2023)

LoRA + **4-bit küçültme (quantization)**. Model ağırlıkları 4-bit'e sıkıştırılır (normal FP16/BF16 yerine) — **bellek 4 kat azalır**, kalite kaybı çok az (tipik %1-3 benchmark farkı).

Pratikte:

- **Donanım:** RTX 3090 / 4090 / 5090 (24-32 GB), Colab L4 ücretsiz katmanı (22 GB), Colab T4 ücretsiz katmanı (16 GB; sadece 7B veya altı küçültülmüş)
- **Veri:** LoRA ile aynı (500-5000 örnek)
- **Süre:** LoRA'dan ~2 kat yavaş ama tek GPU'da çalışır
- **Maliyet:** **$0-10** Colab ücretsiz katmanında 7B model eğitimi (ücretsiz katman 2024 sonu kısıtlandı; günlük kota var)
- **Kalite:** Tam FT ile karşılaştırılabilir (bazı benchmarklarda farkı %3-5 arası)

**5.4 sayfasında QLoRA ile Colab T4/L4 üstünde Qwen 3-1.7B veya Llama 3.2 1B modeli eğiteceksin** — 50 örnek, ~20-30 dakika.

## Instruction tuning vs continued pre-training

Fine-tune iki alt tür:

<table class="ma-aktorler" markdown>

| Tür | Ne yapar | Örnek |
|---|---|---|
| **Instruction tuning** | Model "komut → cevap" formatına geçer | "Özet yap: [metin]" → "Özet şu:" |
| **Continued pre-training** | Modele yeni dil/domain metin "okut" | Tıp literatürü yüz milyon token |

</table>

**%95 geliştirici sadece instruction tuning yapar.** Continued pre-training ciddi compute + veri ister.

## Veri hazırlama — formatlar

### Instruction format (en yaygın)

```json
{
  "instruction": "Aşağıdaki müşteri yorumunu pozitif/negatif olarak kategorize et.",
  "input": "Ürün kaliteli ama kargo çok yavaş geldi.",
  "output": "Karışık (pozitif: kalite, negatif: kargo hızı)"
}
```

### Chat format (modern)

```json
{
  "messages": [
    {"role": "system", "content": "Sen bir Türkçe müşteri destek asistanısın."},
    {"role": "user", "content": "Siparişim gelmedi."},
    {"role": "assistant", "content": "Üzgünüm, sipariş numaranızı paylaşır mısınız?"}
  ]
}
```

Claude + Llama 3 + Gemma son sürümler bu format. Hugging Face `datasets` kütüphanesi ikisini de okur.

### Kaç örnek gerek?

| Örnek sayısı | Sonuç |
|---|---|
| **<100** | Overfitting; ezberler, genelleyemez |
| **100-500** | Basit stil değişimi (ton, format) işe yarar |
| **500-2000** | Çoğu domain-specific FT için yeterli |
| **2000-10K** | Ciddi davranış değişikliği; production kalite |
| **10K+** | Continued pre-training seviyesi; mükemmel ama sınırlı getiri |

**"Fazla veri = daha iyi model" yanılgı.** 200 yüksek kalite > 5000 gürültülü. Veri temizliği + çeşitlilik miktardan önemli.

## Maliyet — gerçekçi tahmin

### QLoRA 7B model (Colab)

- **GPU:** Colab T4 ücretsiz veya Colab Pro A100 $10/ay
- **Veri hazırlama:** 20-40 saat insan iş gücü
- **Eğitim süresi:** 500 örnek × 3 epoch = 1-3 saat
- **Toplam:** $0-10 (Colab) + insan emeği
- **Kullanılabilirlik:** Deneme, ufak ticari iş

### LoRA 13B model (RunPod veya Lambda Labs)

- **GPU:** A100 80GB kiralık $1.5-2/saat
- **Veri hazırlama:** 40-80 saat
- **Eğitim:** 2-8 saat × $2 = $4-16
- **Toplam:** ~$50-100 + insan emeği
- **Kullanılabilirlik:** Orta ticari projeler

### Tam FT 70B model (enterprise)

- **GPU:** 8×H100 saatlik $40-60
- **Veri:** 10K+ örnek, haftalarca hazırlık
- **Eğitim:** 12-48 saat × $50 = $600-2400
- **Toplam:** $5K-50K (veri + compute + iteration)
- **Kullanılabilirlik:** Büyük enterprise

### Kıyas — RAG'in maliyeti

Aynı problem için RAG yaklaşımı:

- **Qdrant VPS:** 4 €/ay
- **Embedding:** Voyage-4 kullandıkça öde (pay-as-you-go), 1M token ~$0.06; ayda ilk 200M token ücretsiz
- **LLM:** Claude Sonnet 4.6 $3/M input, $15/M output (Opus 4.7: $5/$25)
- **Aylık 6000 sorgu:** ~$5-10

**RAG ince ayardan 100-1000 kat ucuz + hafta yerine saatte canlı + güncellemesi kolay.**

## Araçlar — açık kaynak

<table class="ma-aktorler" markdown>

| Araç | Ne için | Not |
|---|---|---|
| **Hugging Face Transformers** | Standart eğitim + çıkarım | `transformers` 4.x serisi (Nisan 2026 itibarıyla 4.46+); ekosistemin kalbi |
| **PEFT** (HF) | LoRA/QLoRA yapılandırma | `peft` 0.13+ (2026 Nisan); resmi Hugging Face |
| **TRL** (HF) | SFT, DPO, RLHF eğiticileri | Adım adım eğitim + notebook |
| **Unsloth** | Hızlı LoRA/QLoRA, 2-5 kat hızlanma | Niş ama Colab için ideal |
| **Axolotl** | YAML yapılandırma + üretim hattı | Daha karmaşık projeler |
| **bitsandbytes** | Küçültme (4-bit, 8-bit) | QLoRA'nın temel taşı |
| **Accelerate** (HF) | Çoklu-GPU eğitim soyutlama | Ölçek büyüdükçe |

</table>

**5.4 sayfasında:** Colab + Hugging Face Transformers + PEFT + TRL + bitsandbytes birleşimi — tek notebook.

## Managed platformlar

Kendin kod yazmadan:

<table class="ma-aktorler" markdown>

| Platform | Destek | Fiyat |
|---|---|---|
| **OpenAI Fine-tuning** | GPT-5, GPT-5-mini, GPT-5.2, o3 | Eğitim ~$25/M token + çağrı sırasında base fiyatın yaklaşık 8 katı (2026 Nisan) |
| **Google Vertex AI** | Gemini 2.5 ailesi | Değişken, Google Cloud fiyatı |
| **AWS Bedrock — Custom Model Import** | Llama, Mistral, DeepSeek (Claude **dahil değil**) | Saatlik ayrılmış (provisioned throughput) gerek |
| **Azure OpenAI** | GPT-5 ailesi ince ayarı | Azure kurumsal fiyatı |
| **Anthropic** | **Genel kullanıma açık değil** (2026 Nisan); seçili kurumsal müşterilere selective access | - |

</table>

**Uyarı — Anthropic ince ayarı 2026 itibarıyla:** Claude için ince ayar Anthropic tarafından sadece **seçili erişim (selective access)** ile büyük kurumsal müşterilere sunuluyor; herkese açık değil. AWS Bedrock'taki "Custom Model Import" özelliği Llama / Mistral / DeepSeek gibi açık ağırlıklı modeller içindir; **Claude buna dahil değildir**. Bu tasarım tercih, eksik değil — Constitutional AI + Model Spec ile Claude'un davranışı tanımlıdır; müşteri ince ayarla bu tanımı bozmasın.

**Pratik:** Claude kullanıyorsan **prompt mühendisliği + RAG + tool calling** üçlüsüyle çoğu problemi çöz. İnce ayar için başka modele (Llama 4, Qwen 3.5/3.6, Gemma 3 — açık kaynak) geç.

## RLHF ve alignment

İleri konu — platform'un bu kısmında **geçici olarak** duracağız. RLHF = Reinforcement Learning from Human Feedback. İnsan puanlamalarıyla modeli eğitme. Claude'un "zararlı isteği reddetme" refleksi büyük ölçüde bunun sonucu.

- **PPO** (Proximal Policy Optimization) — klasik RLHF algoritması
- **DPO** (Direct Preference Optimization, 2023) — PPO'dan kolay, aynı kalite
- **Constitutional AI** (Anthropic) — model **kendi kendini** anayasa metnine göre düzeltir; insan puanlayıcı bias'ı azalır

**Sen yapmayacaksın** büyük ihtimal. Ama bilmek önemli — mülakatta "RLHF ne?" sorusuna cevap: "İnsan geri bildirimiyle model hizalama; PPO/DPO iki algoritma; Anthropic CAI bir varyant."

## "FT gerektirmez" — %90 iddiasının arkası

Bu platform tekrar tekrar **FT'yi erteler**. Neden?

1. **Maliyet** — $500-$5000 vs RAG $5-50.
2. **Zaman** — hafta vs saat.
3. **Bakım** — modelin "çürümesi" (concept drift); 3 ayda yeni data ile yeniden eğit.
4. **Versioning** — v1.0, v1.1, v1.2 adapter'ları; hangi müşteri hangi versiyonu kullanıyor.
5. **Infrastructure** — GPU inference; CPU yetmez; saat başı maliyet.
6. **İade edilemez** — fark ettiğin bug modelin **içinde**; sistem prompt'ta bug fix kolay, FT modelde yeniden eğitim gerek.
7. **Claude spec** — Anthropic'in Model Spec + Constitutional AI disiplini; FT ile bu disiplini bozarsın.

**FT doğru seçim olduğunda bile,** prompt + RAG denenmiş + yetmediği kanıtlanmış olmalı. 5.2 karar ağacı bu sırayı uygular.

## CTO tuzakları — 8 yaygın ince ayar hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | İlk projede doğrudan ince ayara dalmak | $200-500 maliyet, RAG'le aynı sonuç | Prompt → RAG → ince ayar sırası |
| 2 | 50 örnekle ince ayar | Modelin ezberlemesi (overfitting) | Minimum 200-500 örnek |
| 3 | Kalitesiz veri ile çok örnek | Gürültülü model | 200 temiz > 5000 kirli |
| 4 | Tam ince ayar "kulağa hoş" diye dene | $5K-10K donanım | LoRA/QLoRA yeter |
| 5 | İnce ayar sonrası değerlendirme yok | "Daha iyi mi?" bilinmez | Ayrı test seti + benchmark |
| 6 | Üretime ince ayar modelini doğrudan koymak | Bakım cehennemi | A/B test + kademeli yayılım |
| 7 | Claude'u ince ayar etmek için yol aramak | Resmi yol yok (genel kullanım için) | Prompt + RAG + tool = eşdeğer |
| 8 | "Her alan için ayrı ince ayar" | 50 adaptör, hangi müşteri hangisinde? | Tek genel ince ayar + RAG ile niş |

??? warning "Tipik ince ayar hataları — şu durum şu çözüm"

    | Hata | Sebep | Çözüm |
    |---|---|---|
    | `CUDA out of memory` (eğitim sırasında) | VRAM yetmiyor | Batch size düşür (1-2), gradient accumulation kullan; QLoRA'ya geç |
    | Eğitim loss düşmüyor (sabit kalıyor) | Learning rate çok düşük veya veri çok az | LR'yi 10 kat artır; 200+ örnekli veriyle dene |
    | Eğitim loss düşüyor ama val loss artıyor | Modelin ezberlemesi (overfitting) | Epoch sayısını azalt; veri ekle; LoRA rank'i düşür |
    | İnce ayar sonrası model "saçmalıyor" | Yıkıcı unutma (catastrophic forgetting) | Tam ince ayar yerine LoRA; öğrenme oranını düşür |
    | `bitsandbytes` import hatası | CUDA / sürücü uyumsuz | `pip install bitsandbytes --upgrade`; CUDA 12.x sürücü kontrol et |

## Anthropic ekosistemi — neden Claude FT zor?

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude FT filozofisi</strong></summary>

Anthropic'in Claude modelleri için **public fine-tuning'i** 2026 itibarıyla sınırlıdır. Bu eksik değil **tasarım tercihi**:

### 1. Constitutional AI tutarlılığı

Claude'un [Model Spec](https://platform.claude.com/docs/en/about-claude/model-spec) tanımlı davranış listesi içerir (zararlı isteği reddetme, dürüstlük, kullanıcı güvenliği). FT bu tanımı bozabilir. Müşteri "benim için FT edin" derse, Anthropic şöyle sorar: "Hangi Model Spec maddesi sana çelişki yaratıyor? Belki yanlış yoldasın."

### 2. Alternatifler yeterli

**Sistem promptu + few-shot + tool calling + prompt caching** dörtlüsü, 200K-1M token bağlam alanı (Sonnet 4.6 / Opus 4.7 = 1M; Haiku 4.5 = 200K) ve yapılandırılmış çıktı (structured output) disiplini ile **çoğu ince ayar senaryosunu karşılar**. 1M bağlam + cache okuma yaklaşık base × 0.1 (yaklaşık %90 ucuz) = büyük örnek seti prompt'a sığar.

### 3. Model güvenlik sorumluluğu

Anthropic RSP (Responsible Scaling Policy) modeli davranış garantisi verir. FT sonrası bu garanti bozulabilir — müşteri bug'ı Anthropic'e değil müşterinin kendisine ait olur. Tarafsız hiyerarşi.

### 4. Claude için gerçekçi alternatifler

Claude FT gerekiyor mu diyorsun? Dene:

1. **Structured output + tool calling** — davranış şemasını sen kontrol et, model değil.
2. **System prompt "Model Spec override"** — `"Sen [müşteri] stilinde yaz: tonça [özellik], asla [yasaklı]."`
3. **Few-shot caching** — 20-50 örnek system'de, `cache_control` ile %90 indirim.
4. **RAG + instruction** — müşteri data'sı RAG'e, davranış kuralları prompt'a.

Bu dört teknik bir araya gelince **FT'nin %80-95'ini** karşılar.

### 5. Alternatif model yolları

İnce ayar kesinlikle gerekliyse:

- **Llama 3.1 / 3.2** (Meta) — 1B, 3B, 8B, 70B, 405B; açık ağırlık (yoğun mimari, ince ayar için en yaygın)
- **Llama 4** (Meta, 2026) — Scout (17B aktif / 109B toplam), Maverick (17B / 400B), Behemoth (288B / 2T); MoE mimarisi (uzman ekonomisi farklı)
- **Qwen 3.5 / Qwen 3.6** (Alibaba) — Çince + İngilizce + Türkçe güçlü; Qwen 3.5 açık ağırlık, 3.6-Plus kapalı
- **Gemma 3** (Google) — 2B, 9B, 27B
- **Mistral 7B / Mixtral 8x7B / Codestral 25.08** — yoğun + MoE karması
- **DeepSeek V3.2** — 671B parametre (37B aktif MoE), kod + akıl yürütme güçlü, açık ağırlık

Bu modelleri kendi sunucunda barındır + ince ayar et. Claude'la **hibrit**: hassas/karmaşık sorgu → Claude API; niş/ince-ayar gerektiren → kendi model.

**Sonuç:** Claude'u ince ayar edememek eksik değil; sistemi doğru tasarlama teşviki.

</details>

## Çıktı kanıtları — 3 kanıt

<div class="ma-cikti-kaniti" markdown>
<div class="ma-cikti-kaniti-header">📏 Çıktı — 3 kanıt</div>

**1. Üç tekniği karşılaştırma özetin:**

`muhendisal-notlarim/bolum-5/01-finetune-nedir/3-teknik-karsilastirma.md` — Prompt + RAG + FT tablosu. Her teknik için: ne zaman, ne kadar, hangi araç, hangi maliyet.

**2. Kendi projenden karar:**

9.4 RAG Chatbot veya 9.5 Agent için — "FT gerekli mi? Neden gerekli / gereksiz?" 1 paragraf analiz.

**3. Maliyet simülasyonu:**

Kendi düşünceli bir proje (imkanlı — müşteri destek FT) için QLoRA + 1000 örnek senaryosu maliyet çıkar. Veri hazırlama saati × $30/saat + GPU saati × $2. Toplam gerçekçi rakam.

</div>

## Görev — 30 dk karar refleksi

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — FT gereksizliğini kanıtla (kendi projende)</div>

1. 9.4 RAG Chatbot için 3 teknikten **hangisi** uygundu — prompt, RAG, FT?
2. FT gerekli olsaydı maliyet + süre + bakım yükü ne olurdu?
3. Aynı davranışı prompt + RAG ile çözdüğün için **neler kazandın**?
4. `muhendisal-notlarim/bolum-5/01-finetune-nedir/analiz.md` dosyasına yaz.

**Başarı kriteri:** 30 dakika sonra kendi projenden somut örnekle "FT %90 projede gereksiz" tezini **kendi sesinle** savunabiliyorsun. Mülakatta bu soru gelince hazırsın.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**A → B:** AI Engineer'ın model öğretme araç kutusu 3 parça: prompt + RAG + FT; her biri farklı problem için. Bu yüzden **araç seçimi önce.**</li>
<li>**B → C:** Fine-tune 3 biçim: tam FT (enterprise-only), LoRA (adapter, tek GPU), QLoRA (4-bit + tüketici GPU). Bu yüzden **kaynak kısıtı belirleyici.**</li>
<li>**C → D:** Instruction tuning %95 geliştiricinin yaptığı FT; chat format modern standart. Bu yüzden **büyük olasılıkla instruction FT yapacaksın.**</li>
<li>**D → E:** Veri 200-2000 örnek optimum; miktar yerine kalite + çeşitlilik. Bu yüzden **veri kalitesi hiperparametreden önemli.**</li>
<li>**E → F:** QLoRA $0-10 (Colab) vs tam FT $5K-50K — 1000× fark. Bu yüzden **çoğu proje QLoRA ile başlamalı.**</li>
<li>**F → G:** Araçlar: HF Transformers + PEFT + TRL + Unsloth + Axolotl ekosistemi. Bu yüzden **ekosistemi tanımak zaman kazandırır.**</li>
<li>**G → H:** Managed: OpenAI/Vertex/Bedrock var; Anthropic public FT sınırlı — Constitutional AI tutarlılığı için. Bu yüzden **Claude FT yerine RAG tercih et.**</li>
<li>**H → I:** 'FT gerektirmez' %90 iddiası 7 nedenle: maliyet, zaman, bakım, version, infra, geri alınamaz, Claude Model Spec. Bu yüzden **FT kararını ertelemek çoğu zaman doğru.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Fine-tuning kavramı netti — 3 biçim + maliyet + araç + "%90 gerektirmez" gerekçe. Sonraki (5.2): karar ağacı — 10 kriter + 5 senaryo üzerinde "hangisini seçerim?" refleksi.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[5.2 Karar Ağacı — Hangisini Seçmeli →](02-karar.md)** — 10 kriter + 5 somut senaryo + hybrid yaklaşım.

← [Bölüm 5 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md) &nbsp;|&nbsp; [Bölüm 4 — RAG](../bolum-4/index.md)

**Pekiştirme:** [Hugging Face PEFT docs](https://huggingface.co/docs/peft) + [LoRA paper (2021)](https://arxiv.org/abs/2106.09685) + [QLoRA paper (2023)](https://arxiv.org/abs/2305.14314). Üçünü 2-3 saatte tara; FT kavramı kemikleşir.
</div>
