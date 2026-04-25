# Bölüm 4 — RAG (Retrieval Augmented Generation)

<div class="ma-meta" markdown>
**Persona:** Bölüm 3 bitmiş, Qdrant ayakta, semantic search çalışıyor. Şimdi "PDF'ten soru cevaplayan asistan" kurmak istiyor · **Süre:** ~6 saat (7 sayfa, hepsinde kod) · **Önkoşul:** Bölüm 2 + 3, Qdrant kurulu, Claude API anahtarı aktif · **Çıktı:** Kendi dokümanlarından soru cevaplayan çalışan bir RAG servisi — web arayüzüyle veya API endpoint'iyle
</div>

## Neden bu bölüm?

RAG **2025-2026'nın en popüler AI mimarisi.** ChatGPT'nin "Custom GPTs", Claude'un "Projects", her kurumsal chatbot — hepsinin altında RAG var. Çünkü fine-tune pahalı, zor, yavaş; RAG ucuz, hızlı, güncel dokümanla çalışır.

Ama RAG "basit" görünür, production'da kırılır. **"Niye cevap saçmalıyor?"** sorusunun cevabı 9/10 kez chunking veya retrieval'da. Bu bölüm o 9 kırılma noktasını teker teker açar — yüzeye "basit RAG" kurmaktan daha derin bir şeydir.

Üçüncüsü: **Platformun 3 proje tipinden ikisi RAG üstüne kurulabilir** — "PDF özetleyici" (iş), "ders notu asistanı" (kişisel). Bu bölümü bitirince kendi projenin omurgasını atmış oluyorsun.

## Bölüm 4 kısaca

**4.1 — RAG Nedir, Niye Lazım.** Fine-tune vs context stuffing vs RAG karşılaştırması. RAG'ın 3 adımı: Embed → Retrieve → Generate. Naif RAG vs production RAG.

**4.2 — Chunking Stratejileri.** Sabit karakter (en kolay, en kötü), cümle bazlı, paragraf bazlı, semantik chunking (embedding ile bölme), **contextual chunking** (Anthropic önerir — chunk'a özet başlık ekler, arama kalitesini %30 artırır).

**4.3 — Retrieval ve Re-ranking.** Vektör araması + BM25 (kelime araması) hibrit. Top-K çekip LLM'e ver mi, yoksa önce re-rank (Cohere Rerank veya Claude ile ikinci eleme) et mi. Somut örneklerle iki yaklaşımın farkı.

**4.4 — Context Engineering.** LLM'e gelen final prompt'u nasıl kuruyorsun — sistem prompt + chunks + kullanıcı sorusu dizilimi. XML tag'leri ile yapılandırma. "Bağlamı iyi, cevap iyi" prensibi.

**4.5 — RAG Değerlendirme.** Prompt'un nasıl doğru çalıştığını ölçeceksin? **RAGAS** framework'u, **faithfulness/answer relevancy/context precision** metrikleri. 20 örnek soru-cevap üzerinde kendi RAG'inin skorunu ölçüyorsun.

**4.6 — LangChain ile RAG.** Sıfırdan vs LangChain. "Framework kullanmadan bile %80 kod aynı" gerçeği. LangChain'in artı-eksisi. Kısa pratik örneği.

**4.7 (nav'da kapalı):** Production ipuçları — caching, logging, cost control, kullanıcı için fallback.

## Bu bölümün yol haritası

```mermaid
flowchart LR
  S["👤 Sen\n(B3 bitti)"]
  P41["📄 4.1\nRAG\ntemel"]
  P42["📄 4.2\nChunking"]
  P43["📄 4.3\nRetrieval\n+ rerank"]
  P44["📄 4.4\nContext\neng"]
  P45["📄 4.5\nEval\nRAGAS"]
  P46["📄 4.6\nLangChain"]
  P47["🏁 4.7\nProduction"]
  OUT{{"✅ Çalışan\nRAG servisi\n+ skor tablosu"}}
  ANT[("📖 Anthropic\nContextual\nRetrieval"])

  S --> P41 --> P42 --> P43 --> P44 --> P45 --> P46 --> P47 --> OUT
  P42 -.köprü.-> ANT
  P44 -.köprü.-> ANT

  classDef user fill:#ddd6fe,stroke:#7c3aed,color:#111
  classDef page fill:#dbeafe,stroke:#2563eb,color:#111
  classDef goal fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef ext fill:#fed7aa,stroke:#ea580c,color:#111
  class S user
  class P41,P42,P43,P44,P45,P46,P47 page
  class OUT goal
  class ANT ext
```

### Aktör tablosu

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 👤 **Sen** | Qdrant + Claude API + Python ortamı | PDF yükle, chunk, embed, ara, cevap üret |
| 📄 **4.1 RAG nedir** | Platform | Kavram + neden + 3 adım |
| 📄 **4.2 Chunking** | Platform + Python | 4 strateji karşılaştırma + contextual chunking |
| 📄 **4.3 Retrieval** | Platform + Qdrant | Vector only vs hibrit vs re-rank |
| 📄 **4.4 Context eng** | Platform + Python | Prompt şablon yapılandırma |
| 📄 **4.5 Eval** | Python + RAGAS | 20 soru-cevap seti, skor üret |
| 📄 **4.6 LangChain** | Python | "Framework mi sıfırdan mı" karşılaştırma |
| 🏁 **4.7 Production** | Servis olarak | Final entegrasyon + deploy hazırlığı |
| 📖 **Anthropic Contextual Retrieval** | Cookbook | Chunk öncesi bağlam zenginleştirme tekniği |
| ✅ **Çıktı** | Repo'nda `4-rag-servisi/` | Çalışan RAG — Bölüm 9'da deploy'a gidecek |

## Bu bölüm bittiğinde elinde ne olacak

- **Çalışan RAG servisi:** PDF (veya metin klasörü) yükle, soru sor, cevap ve kaynak al
- **4 chunking stratejisi deneyimlemiş:** Karakter / cümle / paragraf / contextual — hangisi ne zaman, notların var
- **Hibrit retrieval + rerank:** Sadece vektör arama ile yetinmeyen, üretim kalitesinde arama kurmuşsun
- **RAGAS skor tablosu:** Kendi RAG'inin faithfulness + relevancy skorları yazılı — iyileştirmeyi ölçülebilir kılıyorsun
- **LangChain ile-olmadan karşılaştırması:** Framework bağımlılığı gerekli mi kendi kararın var
- **Anthropic Contextual Retrieval tekniği:** Chunk kalitesini %30+ artıran yöntem elinde

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu bölümde ne der — öz</div>

RAG konusunda Anthropic'in **en güçlü teknik makalelerinden biri** burada devreye girer:

**1. Contextual Retrieval (anthropic.com/news/contextual-retrieval, Sept 2024).** Anthropic "RAG'in en büyük kırılma noktası chunk'ın bağlamdan kopması" diye açıkladı — ve çözüm önerdi: her chunk'a Claude ile özet başlık üretip embedding'ini bu başlıkla beraber al. Sonuç: arama hatalarında **%49 azalma.** 4.2'de bu tekniği uyguluyoruz.

**2. Anthropic Cookbook — contextual-embeddings notebook.** Yukarıdaki makalenin pratik Jupyter versiyonu. Bölüm 3.5'te giriş yaptık, 4.2'de derinleşiyoruz. Kendi Colab'inde çalıştırabilirsin.

**3. Prompt Caching ([platform.claude.com/docs/en/build-with-claude/prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).** RAG'de uzun sistem prompt'ları tekrar tekrar gönderilir — caching ile cache okuma maliyeti yaklaşık %90 düşer (cache hit base × 0.1). 4.4 "Context Engineering"de bu tekniği entegre ediyoruz. 2.7-2.8'de görmüştük, burada uygulaması.

**4. Claude'u cevap üretici olarak kullanmanın avantajı.** RAG'ın "Generate" adımında model seçimi kritik. Claude Sonnet 4.x uzun bağlama (200K token) iyi dayanır, "I don't know" demeyi biliyor (halüsinasyon az). 4.3-4.4'te bu davranışları test ediyoruz.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [Anthropic News — Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (İngilizce, blog yazısı, ~15 dk okuma). 4.2'den önce aç — tekniği makaleden anlayıp, sayfada pratiğe dönüştüreceğiz.
</div>
</div>

---

<div class="ma-sonraki" markdown>
**Bir sonraki adım →** [4.1 RAG Nedir, Niye Lazım](01-rag-nedir.md) (45 dk, kavram + niye RAG fine-tune'dan iyi)

← [Bölüm 3 — Embeddings](../bolum-3/index.md) &nbsp;|&nbsp; [Ana Sayfa](../index.md)
</div>
