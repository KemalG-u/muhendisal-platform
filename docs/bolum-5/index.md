# Bölüm 5 — RAG vs Fine-tuning

<div class="ma-meta" markdown>
**Persona:** Bölüm 4'te RAG çalıştırdın. "Bu yetmez, modeli kendime göre eğitsem mi?" diye sorduğun nokta. Ya da tam tersi: "RAG çok iş, ince ayar (fine-tuning) daha temiz olmaz mı?" · **Süre:** ~2.5-3 saat (4 sayfa; 5.4'te Colab eğitimi ek 30 dk) · **Önkoşul:** Bölüm 4 bitti, çalışan bir RAG sistemin var · **Çıktı:** Bir proje geldiğinde RAG / ince ayar / hibrit arasında **gerekçeli karar** verebilecek eşik, ve Hugging Face üzerinde mini LoRA denemesi
</div>

## Neden bu bölüm?

İnce ayar (fine-tuning) piyasada caziptir — "kendi modelimi eğittim" cümlesi ağır basar. Pratikte ise **çoğu projede ince ayar yerine RAG + iyi sistem promptu yeterli oluyor**. Anthropic, OpenAI ve HuggingFace dokümanları aynı sırayı tavsiye eder: önce prompt → sonra RAG → en son ince ayar. Bu bölüm o sıranın gerekçesini ve istisnalarını gösterir.

Niye 4 sayfa? Çünkü ince ayar bir kez yanlış yola saparsan $200-500 maliyet, 1-2 hafta iş, sonunda RAG'le aynı sonuç çıkar. Karar baştan doğru olsun diye önemli.

Üçüncüsü: 2024'ten itibaren tam ince ayar yerini büyük ölçüde **LoRA / QLoRA** tekniklerine bıraktı — modelin tüm ağırlıklarını eğitmek yerine küçük bir adaptör katmanı eğitiyorsun. 2026'da ucuz tüketici GPU'larında (RTX 4090 / 5090) bile 8B modelleri ince ayar etmek mümkün. Bu bölüm o ekonomiyi de açar.

## Bölüm 5 kısaca

**5.1 — İnce Ayar Nedir.** Tam ince ayar (tüm parametre, pahalı), LoRA (adaptör katman, küçük), QLoRA (4-bit küçültme + LoRA, tüketici GPU'da). İnce ayar ile prompt mühendisliği ve RAG arasındaki rol ayrımı.

**5.2 — Hangisini Seçmeli.** **Karar ağacı.** "Modelin davranışını mı değiştirmek istiyorsun (ton, stil, format) → ince ayar. Yeni bilgi mi eklemek → RAG. Çok spesifik alan (tıbbi, hukuki) + davranış değiştirme → hibrit." Somut 5 proje senaryosu üzerinde uygulama.

**5.3 — LoRA ve QLoRA.** LoRA matematiği sezgisel (matris ayrıştırma). QLoRA'nın 4-bit küçültme ile 24 GB GPU'da 70B model ince ayar edebildiği iddiası ve sınırları. Pratikte hangi GPU için hangisi (RTX 4090 / 5090 / A100 / H100).

**5.4 — Hugging Face ile Pratik.** Küçük bir model (Qwen 3-1.7B veya Llama 3.2 1B) üzerinde 50 örnekli LoRA ince ayarı. Colab ücretsiz katmanı (T4 / L4, kullanım kotası var) ya da yerelde 12 GB+ VRAM yeter. Kendi küçük "tonu değişmiş" model üretimi. Deneyim için; üretim için değil.

## Bu bölümün yol haritası

```mermaid
flowchart LR
  S["👤 Sen\n(Bölüm 4 bitti)"]
  P51["📄 5.1\nİnce ayar\nnedir"]
  P52["🏁 5.2\nHangisini\nseçmeli"]
  P53["📄 5.3\nLoRA\nQLoRA"]
  P54["📄 5.4\nHF pratik"]
  GPU[("🖥 Colab\nT4/L4 GPU\nücretsiz katman")]
  OUT(["✅ Karar eşiği\n+ 1 mini LoRA\ndenemesi"])

  S --> P51 --> P52 --> P53 --> P54 --> OUT
  P54 -.çalışır.-> GPU

  classDef user fill:#ddd6fe,stroke:#7c3aed,color:#111
  classDef page fill:#dbeafe,stroke:#2563eb,color:#111
  classDef pilot fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef infra fill:#fed7aa,stroke:#ea580c,color:#111
  classDef goal fill:#fef3c7,stroke:#ca8a04,color:#111
  class S user
  class P51,P53,P54 page
  class P52 pilot
  class GPU infra
  class OUT goal
```

### Aktör tablosu

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 👤 **Sen** | Platform + Google Colab | 5.1-5.3 oku, 5.4 Colab'de çalıştır |
| 📄 **5.1 İnce ayar nedir** | Platform | Tam ince ayar ile LoRA ve QLoRA tanımları |
| 🏁 **5.2 Karar ağacı** | Platform (en kritik) | 5 senaryo + karar tablosu |
| 📄 **5.3 LoRA/QLoRA** | Platform | Matematik sezgisi (yine formül yok) |
| 📄 **5.4 HF pratik** | Colab + T4/L4 GPU | Qwen 3-1.7B üstünde 50 örnek LoRA, ~20-30 dk eğitim |
| 🖥 **Google Colab** | Tarayıcı | Ücretsiz katman (2024 sonu kısıtlandı) — günlük kullanım kotası ve 12 saat oturum sınırı; sürekli kullanım için Colab Pro ($10/ay) öneriliyor |
| ✅ **Çıktı** | Reponda karar notu + Colab linki | "Ben bu projede şunu seçerim, çünkü..." yazılı |

## Bu bölüm bittiğinde elinde ne olacak

- **Karar ağacı:** RAG mı, ince ayar mı, hibrit mi — 10 saniyede kararı veren eşik
- **Maliyet farkındalığı:** Tam ince ayar (8B model) $200-500, LoRA $10-30, QLoRA $3-10 — 2026 cloud GPU fiyatlarına göre rakamlı karşılaştırma (5.3'te detay)
- **1 mini LoRA denemesi:** Qwen 3-1.7B'yi kendi tonunla eğitmiş olmanın deneyimi — "ince ayar efsanevi değilmiş, ama RAG'in yerini de tutmuyor" hissi
- **Hugging Face + Colab refleksi:** Sonraki ML denemeleri için hazır ortam

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu bölümde ne der — öz</div>

**Anthropic'in ince ayara bakışı belirgin şekilde temkinli.** Şöyle özetlenebilir:

**1. "Prompt mühendisliği + RAG önce."** Anthropic dokümanları ilk başlık olarak prompt + RAG önerir. İnce ayar "son çare" olarak konumlandırılır — *"Before considering fine-tuning, exhaust prompt engineering and RAG."* Bu bölümün ana hattı bu görüşü yansıtır: önce RAG dene, yetmezse LoRA.

**2. Claude için ince ayar kısıtlı.** Claude'un ağırlıkları halka açık değil; doğrudan ince ayara açık değil. AWS Bedrock üzerindeki "Custom Model Import" özelliği sadece açık ağırlıklı modeller (Llama, Mistral, DeepSeek) içindir; **Claude buna dahil değildir**. Yani "Claude'u ince ayar edeyim" mümkün değil — **Claude prompt ile şekillenir, RAG ile beslenir, ince ayar başka modellerde** (Qwen, Llama, Mistral) yapılır.

**3. Claude Code'un yaklaşımı.** Anthropic'in kendi kod asistanı Claude Code hiç ince ayar kullanmıyor — sistem promptu + tool use + MCP ile çözüyor. Bu bölümün "ince ayar çoğu projede gereksiz" tezi Anthropic'in kendi ürün disiplininin yansıması.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [platform.claude.com — Prompt Engineering Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (İngilizce, ~15 dk). Fine-tune konusundaki Anthropic duruşunu doc'ta açıkça okuyabilirsin — "before considering fine-tuning" paragrafı 5.2 karar ağacımızla uyumlu.
</div>
</div>

---

<div class="ma-sonraki" markdown>
**Bir sonraki adım →** [5.1 Fine-tuning Nedir](01-finetune-nedir.md) (30 dk, FT/LoRA/QLoRA tanımları)

← [Bölüm 4 — RAG](../bolum-4/index.md) &nbsp;|&nbsp; [Ana Sayfa](../index.md)
</div>
