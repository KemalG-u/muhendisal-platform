# 5.1 Fine-tuning Nedir — Tam FT, LoRA, QLoRA

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~35 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> Bölüm 2 (prompt engineering) + Bölüm 4 (RAG) bitti. Çalışan bir RAG sistemin var.</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Fine-tuning'in 3 biçimini (tam FT, LoRA, QLoRA) biliyorsun; **prompt engineering ↔ RAG ↔ fine-tuning** üçgeninde her köşenin ne zaman seçildiğini anlıyorsun; maliyet + süre + donanım gerçekçi tahminleri elinde. Sayfadaki tek iddia: "Çoğu proje fine-tune **gerektirmez**" — bu iddianın arkasındaki gerekçeyi görebiliyorsun.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **Fine-tuning** = önceden eğitilmiş modelin ağırlıklarını kendi verinle güncelleme. **Full FT** (tam fine-tune) = tüm ağırlıklar değişir; pahalı. **LoRA** (Low-Rank Adaptation) = sadece küçük adapter katmanlar eğitilir; orijinal model donuk. **QLoRA** = LoRA + 4-bit quantization; tüketici GPU'da bile çalışır. **PEFT** (Parameter-Efficient Fine-Tuning) = LoRA/QLoRA/Prefix tuning gibi tekniklerin şemsiye adı. **Instruction tuning** = "Kullanıcı sorar, model cevap verir" formatına model öğretmek. **RLHF** = insan geri bildirimiyle hizalama.

## Neden bu bölüm?

Bölüm 4'te RAG kurdun. Projede bir sınır gördün: *"Bu model Türkçe'de bazı kültürel nüansları tam yakalamıyor"* veya *"Bizim şirket dilinde 'müşteri' yerine 'ürün sahibi' diyoruz, model direnmiyor bu dili kullanmaya"*. Çözüm olarak **"modeli kendi verimle eğitsem?"** sorusu aklına geldi.

Bu bölümün ana tezi: **fine-tune romantik olandır, RAG pratik olandır.** Fine-tune "kendi modelimi eğittim" hikâyesi güçlü — mülakatta ya da LinkedIn'de ağır basıyor. Ama **gerçekte %90 projede gereksiz**; maliyet + zaman + bakım üçlüsü RAG'e göre 10-100×. Bu bölümün 4 sayfası sen bu karar noktasında doğru tarafa düşesin diye yazıldı.

İkincisi: Fine-tune "eski" değil — 2024-2025'te **LoRA + QLoRA** teknikleriyle **tüketici GPU**'da (RTX 4090 veya Colab T4) bile büyük modeller eğitilebiliyor. Maliyet eşiği düştü. Ama düşen eşik **"her projeye uyar"** demek değil. Bölüm 5.2 karar matrisi bu sınırı çizer.

Üçüncüsü: Bu bölüm **platform'un kavramsal son bölümü** (teknik temel anlamında). Sonraki bölümler (7 Multimodal, 9.6 imza, 10 kariyer) uygulama-odaklı. 5.4 HF pratik sayfasında küçük bir LoRA deneyimi yapacaksın — deneyim için, production için değil.

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

### 1. Tam fine-tune (full fine-tuning)

Modelin **tüm ağırlıkları** güncellenir. Claude Sonnet ~100B+ parametre (spekülasyon; Anthropic resmen açıklamaz). Tam FT için:

- **Donanım:** 8+ H100 GPU kümesi (tek başına $200K veya bulut $$$$/saat)
- **Veri:** 10K+ kaliteli örnek (az ise overfitting)
- **Süre:** Saatler-günler
- **Maliyet:** Model + donanım ≈ $10K-$1M'luk proje
- **Kim yapar:** Anthropic, OpenAI, Google, Meta, büyük enterprise

**Çoğu geliştiricinin asla dokunmayacağı yöntem.** Sadece model geliştirenler.

### 2. LoRA — Low-Rank Adaptation (2021)

Temel fikir: Model ağırlıklarını **dondur**, **küçük adapter katmanlar** ekle, sadece onları eğit.

**Matematik sezgisi (formül yok):**

Bir matrisi (ağırlık matrisi) iki **küçük matrisin çarpımı** olarak yaklaş — "rank" denen bir boyutta. Orijinal 1000×1000 matrisin yerine 1000×8 + 8×1000 = iki matris tut. **Parametre sayısı 1/62'ye düşer** (örnek rakam).

Pratikte:

- **Donanım:** Tek A100 veya RTX 4090 (24GB VRAM)
- **Veri:** 500-5000 örnek yeter
- **Süre:** 1-4 saat
- **Maliyet:** $5-50/deney (Colab A100)
- **Dosya:** Adapter ağırlıkları ~10-50 MB (orijinal model ~30-70 GB)

**Büyük fayda:** Farklı görevler için ayrı adapter tut, aynı base modeli paylaş. 10 farklı tonunuz varsa 10 adapter + 1 base, toplam 70 GB + 500 MB = 70.5 GB.

### 3. QLoRA — Quantized LoRA (2023)

LoRA + **4-bit quantization**. Model ağırlıkları 4-bit'e sıkıştırılır (normal 16/32-bit yerine) — **hafıza 4×-8× azalır**, kalite kaybı çok az.

Pratikte:

- **Donanım:** RTX 3090 (24GB), Colab T4 ücretsiz (16GB, 7B model fine-tune)
- **Veri:** LoRA ile aynı (500-5000 örnek)
- **Süre:** LoRA'dan 2× yavaş ama tek GPU'da çalışır
- **Maliyet:** **$0-10** ücretsiz Colab'de 7B model eğitimi
- **Kalite:** Tam FT ile karşılaştırılabilir (bazı benchmark'larda %90-95)

**5.4 sayfasında QLoRA ile Colab T4 üstünde 1.5B modeli eğiteceksin** — 50 örnek, 20 dakika.

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
- **Embedding:** Voyage-3 pay-as-you-go, 1M token ~$0.12
- **LLM:** Claude Sonnet $3/M input, $15/M output
- **Aylık 6000 sorgu:** ~$5-10

**RAG FT'den 100×-1000× ucuz + hafta yerine saatte canlı + güncellemesi kolay.**

## Araçlar — açık kaynak

<table class="ma-aktorler" markdown>

| Araç | Ne için | Not |
|---|---|---|
| **Hugging Face Transformers** | Standart eğitim + inference | transformers==5.6.1, ekosistem kalbi |
| **PEFT** (HF) | LoRA/QLoRA config | peft==0.19.1, resmi Hugging Face |
| **TRL** (HF) | SFT, DPO, RLHF trainer'ları | Adım adım tutorial + notebook |
| **Unsloth** | Hızlı LoRA/QLoRA, 2-5× optimize | Niş ama hızlı |
| **Axolotl** | YAML config + production pipeline | Daha karmaşık projeler |
| **bitsandbytes** | Quantization (4-bit, 8-bit) | QLoRA temel |
| **Accelerate** (HF) | Multi-GPU training soyutlama | Ölçek büyüdükçe |

</table>

**5.4 sayfasında:** Colab + Hugging Face Transformers + PEFT + TRL + bitsandbytes birleşimi — tek notebook.

## Managed platformlar

Kendin kod yazmadan:

<table class="ma-aktorler" markdown>

| Platform | Destek | Fiyat |
|---|---|---|
| **OpenAI Fine-tuning** | GPT-4o, GPT-4o-mini, o-series | ~$25/1M training tokens + usage 8× |
| **Google Vertex AI** | Gemini, PaLM | Değişken, Google Cloud fiyatı |
| **AWS Bedrock** | Claude (sınırlı), Llama, Titan | Provisioned throughput gerekli |
| **Azure OpenAI** | GPT-4o fine-tuning | Azure enterprise fiyatı |
| **Anthropic** | **Henüz genel kullanıma açık değil** (2026 Nisan) | - |

</table>

**Uyarı — Anthropic FT 2026 itibarıyla:** Claude fine-tuning'i Anthropic tarafından **selective access** ile enterprise müşterilere sunuluyor. Claude 3 Haiku için AWS Bedrock'ta sınırlı FT var. Claude 4 Sonnet için public FT **yok** — Constitutional AI + Model Spec ile davranış tanımlıdır; müşteri FT ile bu tanımı bozmasın. Bu tasarım tercih, eksik değil.

**Pratik:** Claude kullanıyorsan **prompt engineering + RAG + tool calling** üçlüsüyle çoğu problemi çöz. Fine-tuning için başka modele (Llama, Qwen, Gemma açık kaynak) geç.

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

## CTO tuzakları — 8 yaygın FT hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | İlk projede FT dene | $500 maliyet, RAG'le aynı sonuç | Prompt → RAG → FT sırası |
| 2 | 50 örnekle FT | Overfitting | Minimum 200-500 örnek |
| 3 | Kalitesiz veri ile çok örnek | Gürültü model | 200 temiz > 5000 kirli |
| 4 | Tam FT "havalı" diye dene | $10K donanım | LoRA/QLoRA yeter |
| 5 | FT sonrası evaluation yok | "Daha iyi mi?" bilinmez | Hold-out test set + benchmark |
| 6 | Production'da FT modeli direkt | Bakım cehennemi | A/B test + gradual rollout |
| 7 | Claude'u FT etmek için agresif ara | Official path yok (public) | Prompt + RAG + tool = eşdeğer |
| 8 | "Her domain için ayrı FT" | 50 adapter, hangi müşteri hangisinde? | Tek genel FT + RAG ile niche |

## Anthropic ekosistemi — neden Claude FT zor?

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude FT filozofisi</strong></summary>

Anthropic'in Claude modelleri için **public fine-tuning'i** 2026 itibarıyla sınırlıdır. Bu eksik değil **tasarım tercihi**:

### 1. Constitutional AI tutarlılığı

Claude'un [Model Spec](https://platform.claude.com/docs/en/docs/model-spec)'i tanımlı davranış listesi içerir (zararlı isteği reddetme, dürüstlük, kullanıcı güvenliği). FT bu tanımı bozabilir. Müşteri "benim için FT edin" derse, Anthropic şöyle sorar: "Hangi Model Spec maddesi sana çelişki yaratıyor? Belki yanlış yoldasın."

### 2. Alternatifler yeterli

**System prompt + few-shot + tool calling + prompt caching** dörtlüsü, 100K-1M token bağlam alanı ve structured output disiplini ile **çoğu FT senaryosunu karşılar**. Claude 200K context + prompt caching %90 indirim = büyük örnek seti prompt'a sığar.

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

FT kesinlikle gerekliyse:

- **Llama 3.1/3.2/3.3** (Meta) — 8B, 70B, 405B; açık ağırlık
- **Qwen 3** (Alibaba) — Çince + İngilizce + Türkçe güçlü
- **Gemma 3** (Google) — 2B, 9B, 27B
- **Mistral 8x7B** veya **Mixtral** — MoE (mixture of experts)
- **DeepSeek V3.5** — kod + reasoning güçlü

Bu modelleri self-host + fine-tune. Claude'la **hybrid**: hassas/karmaşık sorgu → Claude API; niche/FT-gerektiren → kendi model.

**Sonuç:** Claude'u FT edememek eksik değil; sistemi doğru tasarlama teşviki.

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
