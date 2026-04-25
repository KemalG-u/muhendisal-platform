# 10.1 LinkedIn + İleri Kariyer Stratejisi

> **TL;DR:** LinkedIn 2026 algoritmasına uygun haftalık paylaşım takvimi + 25 ATS anahtar kelime + DM ile iş bulma refleksi kurarsın · Sayfa sonunda kariyer profilin (junior/mid/lateral/freelance) net.

<div class="ma-meta" markdown>
<div class="ma-meta-row"><span class="ma-icon">👤</span> <strong>Kim için:</strong> 🟢 başlangıç · 🔵 iş · 🟣 kişisel — kariyer açılış sayfası.</div>
<div class="ma-meta-row"><span class="ma-icon">⏱️</span> <strong>Süre:</strong> ~30 dakika</div>
<div class="ma-meta-row"><span class="ma-icon">📋</span> <strong>Önkoşul:</strong> 9.7 Portföy Paketleme okundu (profil foto + headline + About temelleri kuruldu). 9.4 + 9.5 canlıda. GitHub + LinkedIn hesapları mevcut.</div>
<div class="ma-meta-row"><span class="ma-icon">🎯</span> <strong>Çıktı:</strong> **İçerik stratejin var** — haftalık paylaşım takvimin, 3 ay sonraki hedefin (500-1000 bağlantı, 5-10 yorum/paylaşım), DM ile iş bulma refleksin. LinkedIn ATS anahtar kelimeleri derinleştirilmiş. Kariyer konumun net: junior / mid / lateral mover / freelance. **Platform kapanış bölümünün açılış sayfası** — 10.5'e kadar her sayfa iş aramana doğrudan destek.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **Engagement** (etkileşim) = LinkedIn/X'te paylaşımına gelen beğeni/yorum/yeniden paylaşım sayısı. **Reach** (erişim) = paylaşımını gören kullanıcı sayısı (takipçi + algoritmanın yaydığı kişiler). **Lateral mover** (yatay geçiş yapan) = farklı meslekten AI mühendisine geçiş yapan kişi (arka uç geliştirici, avukat, öğretmen vb.). **DM** (direct message — doğrudan mesaj) = profil/paylaşım dışı özel iletişim. **Creator mode** (üretici modu) = LinkedIn'in yazar/içerik üretici moduna geçiş; takipçi sayısı görünür olur. **InMail** = LinkedIn Premium aboneliğiyle tanımadığın kişiye mesaj. **ATS** (Applicant Tracking System — başvuru takip sistemi) = işe alımcının CV/profil tarayan otomatik sistemi; anahtar kelimelerle eşleşme arar. **Dwell time** (kalış süresi) = bir kullanıcının paylaşımını okurken sayfada geçirdiği saniye sayısı; LinkedIn 2026 algoritmasının ana sıralama sinyali. **CTA** (Call to Action — eylem çağrısı) = paylaşımın sonundaki net istek ("DM atın", "linke tıklayın").

## Platform yolculuğun — 10 bölümdü, 1 kaldı

Geride bıraktığın 9 bölüm:

```
✅ Bölüm 0  → Kurulum (Python, Docker, venv, FastAPI)
✅ Bölüm 1  → AI Engineer kim, ne yapar, nasıl yetişir
✅ Bölüm 2  → Claude API + prompt engineering
✅ Bölüm 3  → Embedding + vector DB + Qdrant
✅ Bölüm 4  → RAG (Retrieval-Augmented Generation)
◻️ Bölüm 5  → RAG vs Fine-tuning (ileri konu)
✅ Bölüm 6  → Agent + MCP + tool calling
◻️ Bölüm 7  → Multimodal (görsel + ses, ileri konu)
✅ Bölüm 8  → Güvenlik + Production (3/7 tamam)
✅ Bölüm 9  → Deploy + 2 canlı portföy + README paketleme
👉 Bölüm 10 → **KARIYER — buradayız.**
```

Elindeki **somut varlıklar**:

- **2 canlı AI sistemi** (9.4 RAG Chatbot + 9.5 Agent Otomasyon)
- **3 referans proje** (rag-chatbot + semantic-search + icerik-ozet-agent, her biri pytest + ruff temiz)
- **GitHub profili** (pinned 2-3 proje, README'ler, demo GIF)
- **LinkedIn temeli** (profil foto, Headline, About, Skills)
- **CV AI Engineer formatı** (projeler üstte, ATS keyword yoğun)
- **Başvuru mesajı şablonu** (TR + EN, 3-cümle)

Bu varlıklarla **AI Engineer pozisyonuna başvurabilir durumdasın.** Ama sadece başvurmak yetmez — pazar seni **bulmalı**. Bu sayfa görünürlüğünü **pasif**ten **aktif**e çeviriyor.

## Kariyer pozisyonunu net gör — 4 profil

Öğrencilerin çoğu "ne iş ararım" sorusuna net cevap vermeden başvuruya başlar. Sonuç: dağınık başvuru, düşük dönüş. **Önce kendi konumunu seç:**

<table class="ma-aktorler" markdown>

| Profil | Durum | Hedef pozisyon | Strateji |
|---|---|---|---|
| 🟢 **Junior** | 0-2 yıl yazılım tecrübesi | "Junior AI Engineer", "AI Developer" | Portföy ağır, junior pozisyon, stajyer kabul |
| 🔵 **Mid** | 2-5 yıl backend / fullstack | "Mid AI Engineer", "Applied AI Engineer" | Lateral + AI skill, orta maaş beklenti |
| 🟣 **Lateral mover** | 5+ yıl farklı alanda (avukat, öğretmen, PM) | "Domain-specialist AI Engineer" | Alan uzmanlığı + AI = niche güç |
| 🟠 **Freelance / solo** | Kimsenin için değil kendin için | Bağımsız proje, ürün, danışmanlık | Topluluk + içerik + SaaS |

</table>

**Kendi konumunu karar ver** — 3 dk düşün, dosyana yaz: *"Ben [X] profilim, hedef pozisyonum [Y], strateji [Z]."*

Bu kararı vermeden LinkedIn optimize edilmez. Aynı profil her pozisyona cevap veremiyor — junior için "öğrenmeye açık", lateral mover için "alan tecrübemle AI" farklı hikâye.

## LinkedIn 2026 — algoritma ve anahtar kelime

### Algoritma ne seviyor (2026 güncel)

LinkedIn 2025 sonu / 2026 başı algoritması 4 sinyali ana sıralamaya alır:

1. **Dwell time (kalış süresi)** — paylaşımına bakan kişi ne kadar süre okuyor? Uzun metinler (200-500 kelime) "More" (devamı) düğmesine tıklatınca dwell time'ı artırır → kısa metinlerden belirgin önde.
2. **Erken etkileşim ivmesi** — ilk 60-90 dakikada 10+ kaliteli yorum → algoritma 1. derece bağlantılarının ötesine yayar.
3. **Yorum kalitesi (kelime sayısı)** — 5 kelimelik "Harika!" yerine 25-50 kelimelik teknik yorumlar premium sinyal sayılır.
4. **Format hiyerarşisi** — `video > belge taşıyıcı (carousel/PDF) > resim > sade metin`. Kısa video (60-90 sn) ham reach'i 3-5x artırır; carousel ortalama dwell time'ı 1.6x'a çıkarır.

**Eski tavsiyelerin geçersizleştiği noktalar:**

- ❌ "İlk yorumda link bırak" — 2024'ten bu yana etkisi azaldı, link doğrudan paylaşımda olabilir.
- ❌ "Hashtag yığını (#10+)" — 3-5 odaklı hashtag yeterli; fazlası spam sinyali.
- ❌ "Pod/yorum çetesi" — LinkedIn 2025'te tespit eden modeller devreye soktu, hesap kısıtlanır.

**Pratik zaman çizelgesi (Türkiye saati):**

- **Pazartesi-Çarşamba 08:30-10:00** → TR teknik kitle aktif.
- **Salı-Perşembe 17:00-18:30** → Avrupa kapanış + ABD açılış kesişimi (uluslararası reach hedefliyorsan).
- Paylaşımdan sonra ilk 30-60 dk çevrimiçi kal, gelen yorumlara **2-3 cümlelik teknik cevaplar** ver.
- 2-3 yakın bağlantıdan "ilk 30 dk içinde gerçek yorum bırak" iyiliği iste — yorum **gerçek + uzun** olmalı, "tebrikler" değil.

### ATS anahtar kelime derinleşmesi

9.7'de 10 yetkinlik seçtik. LinkedIn ATS + işe alımcı taraması için **profilin her yerine** yerleştirilecek 25 anahtar kelime listesi (2026 işe alım ilanı analizinden):

<table class="ma-aktorler" markdown>

| Kategori | Anahtar kelimeler (her biri farklı yerde görünmeli) |
|---|---|
| **Çekirdek AI** | AI Engineer · LLM · RAG · Claude · Anthropic · Prompt Engineering · Agent Systems · MCP (Model Context Protocol) · Tool Calling · Function Calling |
| **Yığın (Stack)** | Python · FastAPI · Qdrant · Vector Database · Embeddings · Docker · PostgreSQL · pgvector · LangChain · LangGraph |
| **Üretim (Production)** | Deployment · CI/CD · Monitoring · Observability · Cost Optimization · LangFuse · Helicone |
| **Güvenlik & Etik** | AI Safety · Constitutional AI · Prompt Injection · Jailbreak Defense · Bias Audit · KVKK · GDPR · EU AI Act |
| **Çoklu kip (Multimodal)** | Vision-Language Models · Computer Use · Voice Agent · PDF Extraction |
| **Yumuşak yetkinlikler** | Technical Writing · Turkish-English Bilingual · Open Source Contribution · Self-directed Learning |

</table>

!!! info "2026 işveren ilan analizi — yeni eklenenler"
    LinkedIn iş ilanlarında 2025'in sonuna kadar nadiren geçen ama 2026 başında **standart aranan** anahtar kelimeler: `MCP`, `Constitutional AI`, `Agent Systems`, `Computer Use`, `EU AI Act`, `Tool Calling`, `LangGraph`. Bu yedi kelimeyi profilinden eksik tutarsan AI Engineer ilanlarının yaklaşık üçte biri ATS taramasında elenir.

**Nereye konur (LinkedIn alan adlarıyla):**

- **Headline (başlık):** En güçlü 3 anahtar kelime (AI Engineer + Claude + RAG). 220 karakter sınır, ilk 70 karakter mobilde görünür.
- **About (Hakkımda) — yukarıdan aşağı:** 10-15 anahtar kelime doğal akışta. İlk 3 satır "See more" düğmesinden önce — en önemli mesaj burada.
- **Experience (Deneyim) — her pozisyon:** Her açıklamada 3-5 anahtar kelime + somut sayı (kullanıcı sayısı, gecikme, maliyet).
- **Skills (Yetkinlikler):** 10-15 açık yetkinlik (eski 10 + 5 yeni). LinkedIn 2025'te yetkinlik onayı ağırlığını azalttı; sertifika eşleşmesi öne çıktı.
- **Featured (Öne çıkanlar):** 2-3 proje, her biri anahtar kelime yoğun açıklama + ekran görüntüsü.
- **Recommendations (Öneriler) — iste:** Eski iş arkadaşından "Python + Claude ile ... kurdu" şeklinde tavsiye. 2026'da işverenlerin %40'ı tavsiyeleri AI taraması için ek sinyal sayıyor.
- **Licenses & Certifications (Sertifikalar):** Anthropic Academy sertifikalarını sırayla ekle — her birinin "Issuing organization" alanına `Anthropic` yaz, ATS bunu işveren adı eşleşmesi olarak da yakalar.

**Anahtar kelime şişirme uyarısı:** Aynı kelimeyi 20 kez yazmak ters etki yapar. 25 anahtar kelime = her biri 2-4 kez, doğal bağlamda. İşe alımcı "okuyunca doğal" hissedecek; ATS "eşleşme oranı yüksek" sinyali alacak. LinkedIn 2025'te gizli metin (beyaz üzerine beyaz keyword) tespit eden modeli devreye soktu — bu yöntem artık hesap askıya alma riski.

## Haftalık içerik takvimi — 6 hafta plan

9.7'de 6-post serisi taslağı koydum. Bu sayfada **genişlemiş versiyonu:**

### Hafta 1 — "Ben kimim + ne yaptım" (origin story)

**Post tipi:** Uzun metin (300-400 kelime)
**Başlık:** "2 aydır AI Engineer olmak için ne yaptığımı paylaşıyorum"
**İçerik:**
- Nereden geldiğin (junior/mid/lateral)
- 2 canlı proje (link + demo GIF, 2-3 sn)
- 2 ay içinde öğrendiğin 3 somut şey
- "Geri bildirim + iş ilanı varsa DM atın" kapanış

**Hedef:** 50-100 etkileşim, 20 yeni bağlantı isteği.

### Hafta 2 — Teknik derinleşme (authority signal)

**Post tipi:** Teknik deep-dive
**Başlık:** "Embedding'de `document` / `query` asimetrisi — %20 retrieval kalite farkı"
**İçerik:**
- Somut kod örneği (3.1 sayfasından ilham al)
- "Çoğu geliştirici atlıyor" spin
- Bu bilgi olmadan ne olur gösterimi
- Kendi projende nasıl çözdüğün

**Hedef:** 30-50 etkileşim, teknik topluluk dikkati.

### Hafta 3 — Maliyet/pragmatizm (mid/senior çekici)

**Başlık:** "Heterojen model tercihiyle agent maliyeti %38 düştü — 4 karar"
**İçerik:** 9.5 projesindeki Sonnet/Haiku ayrımı. Sayı + kod + gerçekçi fatura.

### Hafta 4 — Araç/Kütüphane karşılaştırması (SEO mıknatısı)

**Başlık:** "Qdrant 1.18 vs Pinecone 2026 — kendi sunucumda 1M vektör senaryosu"
**İçerik:** 3.3 sayfasının özetlenmiş hali. `query_points()` API göçü + barındırma maliyeti karşılaştırması + karar matrisi. Karşılaştırma paylaşımları SEO için en güçlüsü — Google "Qdrant vs Pinecone 2026" araması seni getirir, sonraki haftalarda Türkiye dışından da bağlantı isteği gelir.

### Hafta 5 — Dürüst post-mortem (samimiyet sinyali)

**Başlık:** "RAG chatbot kurarken 3 büyük hatam"
**İçerik:**
- Hata 1: document/query karıştırdım → %20 kalite kaybı
- Hata 2: Qdrant portunu dışa açtım → güvenlik hatası
- Hata 3: Claude hard cap koymadım → $47 beklenmedik fatura

Bu post **çok güçlü** — recruiter "bu aday hataları öğrenmiş" sinyali alır.

### Hafta 6 — Açık iş isteği (call to action)

**Başlık:** "2 canlı AI proje + [X] ay tecrübe — AI Engineer pozisyonuna açığım"
**İçerik:**
- Özet: ne yaptın, nerede çalıştın (varsa), ne arıyorsun
- Projeler link
- Sınır: uzaktan/hibrit/ofis tercihin, Türkiye mi AB mi
- Net CTA: "Uygun pozisyon varsa DM atın"

**İpucu:** Hafta 6 post'u LinkedIn'de **feature** olarak üste sabitle (kendi profilinde "Featured" bölümü).

## DM ile iş bulma — 2025-2026 trendi

Klasik yol: LinkedIn'de ilana başvur → 2000-5000 başvuru arasında kaybol (AI Engineer ilanları 2025'ten itibaren ortalama 3000+ başvuru alıyor; ChatGPT ile başvuru üretimi yapanlar bu sayıyı şişirdi). **Alternatif yol** (2025-2026'da daha etkili):

1. Hedef 10-20 şirket belirle — ilgilendiğin AI odaklı Türkiye/uzaktan şirketler.
    - **Türkiye AI yığını örnekleri:** Hepsiburada (öneri sistemi), Trendyol Tech (arama), Getir Veri (ETA tahmini), Peak Games (oyun içi AI), Insider (CDP + AI), Commencis, OBSS, Oredata (kurumsal AI danışmanlığı), Vivense (RAG arama), Picus Security (AI savunma).
    - **Uzaktan TR-EU köprüsü örnekleri:** Helbiz, Yousign, Pipedrive, Intercom, Pleo (Türkiye'den uzaktan AI Engineer alımı yapan AB merkezli şirketler).
2. Her şirketten **işe alım yöneticisi** (hiring manager) veya CTO bul. LinkedIn arama: `"AI" + "[Şirket]" + "founder"` veya `"CTO"` veya `"Head of AI"` veya `"Engineering Manager"`.
3. **3 cümlelik mesaj at** (9.7'deki şablon):
    - Şirkete özel 1 cümle (ürününü kullanıyorum, son blog yazısı/teknoloji seçimi hakkında somut yorum).
    - Portföy bağlantısı + 1 cümle ne yaptığın.
    - Net eylem çağrısı (20 dakikalık tanışma görüşmesi).

**Örnek:**

```
Merhaba [İsim],

[Şirket]'in son yayımladığı [X feature/blog post] ilgimi çekti — özellikle 
[SOMUT NOT]. Kendim 2026 başından beri Türkçe AI sistemleri kuruyorum 
(github.com/KULLANICI/rag-chatbot — 45+ gün canlıda). [Şirket]'te AI 
ekibinize katkıda bulunabilir miyim diye 20 dk görüşmek isterim. Önümüzdeki 
hafta Salı-Perşembe müsaitim.

Teşekkürler,
[İsim]
```

**Tipik dönüş oranı (2026 LinkedIn topluluk verileri):**

- İlan tabanlı başvuru: %1-3 ilk görüşme daveti (AI ilan başvuru sayısı 3000+ olduğundan oran 2024'e göre düştü).
- DM tabanlı başvuru: %12-20 ilk görüşme daveti (yüksek kalite hedef + özenli mesaj).
- DM + öncesinde paylaşım yorumu (ısıtma): %20-30 ilk görüşme daveti (en iyi yöntem).

**Uyarı:** DM ile iş başvurusu zaman alır — **her mesajı ayrı araştır ve yaz**. Aynı mesajı 50 kişiye kopyala-yapıştır = LinkedIn spam işaretlemesi, hesap kısıtlaması. LinkedIn 2025'te bağlantı isteklerinde haftalık üst sınırı 100'e indirdi (önceden 200+); kalitesiz mesaj akışı bağlantı isteğini de kısıtlar.

**Günlük yük:** 3-5 yüksek kalite DM. 1-1.5 saat sürer (her şirket için 10-15 dk araştırma + mesaj). Haftada 20-25 DM → ayda 80-100 DM → 15-25 ilk görüşme daveti gerçekçi beklenti.

**Takip mesajı kuralı:** İlk DM cevapsızsa **5-7 gün sonra tek bir takip mesajı** at. 2'den fazla takip = ısrar, ters etki. Takip mesajı ek değer sunsun: "Bu arada [konu]'da yeni bir paylaşım yaptım, ilgilenirseniz" gibi yumuşak.

## Creator Mode + bülten + kişisel marka

LinkedIn Creator Mode'u (Üretici Modu) aktif et:

1. Profil sayfana gir → Resources (Kaynaklar) → "Creator Mode: Off" üzerine tıkla, **On** yap.
2. İlk 5 konu seç: `AI Engineering`, `Claude`, `LLMs`, `RAG`, `Python`.
3. Takipçiler görünür olur (Connections — Bağlantılar değil, Followers — Takipçiler sayısı). Bir işe alımcı için "bu kişinin sesi var" sinyali.

**Bülten (Newsletter) özelliği — 2025'te tüm Creator Mode hesaplarına açıldı:**

- Aylık veya iki haftada bir teknik bülten yayımlayabilirsin (ör. "Türkçe AI Mühendisi Notları").
- Yeni bültene abone olan kullanıcılara LinkedIn otomatik bildirim gönderir → ilk paylaşımdan farklı bir reach kanalı.
- 2026'da bülten sahipliği işe alımcıların gözünde "uzman içerik üretici" eşdeğeri sayılıyor.

**3 ay sonra hedef:** 300-500 takipçi + haftada 1 paylaşım + ayda 1 bülten. 6 ay sonra 1000-2000 takipçi gerçekçi.

### Personal brand vs kimlik

"Personal brand" kelimesi korkutabilir — "ben satışçı değilim, mühendisim." Gerçek: personal brand = **görünür olmak**, satmak değil. Bir mühendis kimliğinin görünür olması = iş fırsatı farkı.

**3 eksen personal brand:**

1. **Teknik derinlik** — RAG + agent + Claude alanında öne çıkan bilgi.
2. **Pragmatizm** — maliyet, production, gerçekçi kod (teori değil).
3. **Dil** — Türkçe'de yayın yap; Türkçe AI engineering yazarı az, niş güç.

Bu üçü sürekli tekrarlar → insanlar seni "Türkçe üretim AI yazarı" olarak tanır. Eş niteli (Ahmet Abi, Ayşe Abla stili) İngilizce-yoğun AI yazarları var; sen **Türkçe-ağırlıklı** git → rekabeti az.

## İleri görüşme teknikleri (10.2'ye köprü)

Post paylaş + DM at = görüşme davetleri gelir. Sonraki adım **görüşme**. 10.2 Mülakat Soruları sayfası 30 sık soru cevaplarıyla dolu olacak. Şimdilik temel refleks:

- **Teknik soru:** Her cevapta **somut kod/proje örneği** ver. Soyut teori reddet.
- **Davranışsal soru:** STAR formatı (Situation-Task-Action-Result). Öğrencinin hatası: "Action"ı atlayıp "Result"a geçmek.
- **Maaş sorusu:** 1.2'deki maaş bantlarını kaydet (TL + USD). Recruiter "beklenti nedir" sorunca **sayı ver**, "görüşürüz" deme.
- **Soru yerine soru:** "Şirket'te AI pipeline'ı nasıl deploy ediyorsunuz?" — mülakatçıya görev yükle, ilgini göster.

## GitHub profil momentum — contributions sürdürülebilirliği

GitHub profil sayfandaki yeşil kareler "aktifim" sinyali. **Son 3 ay** kritik — recruiter bakınca dolu görmeli.

**Sürdürme stratejisi (günde 15 dk):**

- Kendi projelerinde küçük düzeltmeler (README, test ekleme, bug fix)
- Açık kaynağa katkı (Anthropic Cookbook, Qdrant örnekler) — 10.3 sayfası detayda
- Platform öğrendiklerini kendi notes repo'suna commit (muhendisal-notlarim/)

**Amaç:** Her gün **en az 1 commit**. Kısa olsun, mühim değil. 3 ay sonra takvimin yeşil.

## Anthropic ekosistemi — kariyer fırsatı

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Anthropic'te çalışma + Ambassador programı</strong></summary>

### Anthropic Careers (doğrudan başvuru)

[Anthropic Careers](https://www.anthropic.com/careers) — 2026'da aktif işe alım yapan ofisler: San Francisco, New York, Londra, Dublin, Tokyo, Zürih. Türkiye ofisi **yok** (2026 başı itibarıyla).

- **Applied AI Engineer:** Claude'u kurumsal müşteri ürünlerine entegre etme. 1.2'de "AI Engineer" olarak tanımlanan rol.
- **Member of Technical Staff (MTS):** Platform + API + model altyapısı geliştirme.
- **Solutions Engineer:** Kurumsal müşterilere ön satış + entegrasyon desteği.
- **Forward Deployed Engineer (FDE):** 2025'te eklenen rol — müşteri sahasında hızlı prototipleme.

Türkiye'den uzaktan — pozisyona bağlı. Çoğu pozisyon "US/UK time zone overlap" istiyor; Türkiye saati üst üste binmesi makul (TR-LDN 3 saat, TR-NY 7 saat fark).

**Profil gereksinimi (gerçekçi):**

- 3+ yıl üretim Python/arka uç deneyimi
- LLM entegrasyon deneyimi (tercihen Claude API ile)
- Güçlü portföy (senin 2 projen **başlangıç için yeterli değil**, 4-5 canlı proje + açık kaynak katkıları birikimi gerek)
- İngilizce akıcı (yazı + görüşme); Anthropic mülakat süreci 5-7 aşama, çoğu İngilizce kod canlı yazımı.

Senin için **1-2 yıllık bir hedef.** Şimdi başvurma — önce birikim + 1-2 yıl şirket deneyimi. Sonra Anthropic'e geçiş güçlü.

### Anthropic topluluk programları

Anthropic 2025-2026'da topluluk tarafına yatırım yapıyor:

- **Anthropic Builder Program** (2025'te başladı): aktif geliştiricilere artırılmış API kredisi + erken özellik erişimi. Başvuru sayfası: [anthropic.com/builders](https://www.anthropic.com/builders) (URL 2026'da değişebilir, ana sayfadan "builders" araması yap).
- **Anthropic Community Discord** — kayıt: [anthropic.com/discord](https://www.anthropic.com/discord) yönlendirmesi. Burada düzenli AMA + canlı kod oturumu yapılır.
- **MCP topluluk çalışmaları** — Aralık 2025'te MCP Linux Foundation'a (AAIF — AI Alliance Foundation) bağışlandığından beri MCP topluluk yönetişimi açık; sunucu/istemci katkıları için iyi bir başlangıç.

Resmi başvurular Anthropic blog ve X hesabında duyurulur. Resmi URL'ler 2026 boyunca değişebilir — ana sayfadan ara.

### LinkedIn'de Anthropic takibi

- [Anthropic LinkedIn](https://www.linkedin.com/company/anthropicresearch/) follow et
- **Yorum yap** — Anthropic post'larına teknik yorum → recruiter'lar görür
- #AIEngineering #Claude #ResponsibleAI hashtag'lerinde aktif ol

**Stratejik değer:** Anthropic LinkedIn postlarına 6 ay boyunca kaliteli yorum yazan profillerin bir kısmı sonradan Anthropic recruiter tarafından DM'ye çağrıldı (kamu örnekler var). "Yorum = başvuru eksili" kısmı.

</details>

## CTO tuzakları — 12 LinkedIn hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Profil durağan, 6 aydır paylaşım yok | "Atlatılmış" sinyali | Haftada 1 paylaşım asgari |
| 2 | Anahtar kelime şişirme | Robot metin, ATS reddi | 25 anahtar kelime doğal bağlamda |
| 3 | Aynı DM 50 kişiye | Spam işaretlemesi, hesap kısıtlaması | Her DM özel, günde 3-5 |
| 4 | "Açık kaynak" Featured'da proje yok | İnandırıcılık zayıf | 2-3 proje sabitle + açıklama |
| 5 | Creator Mode kapalı, bülten yok | Takipçi sayısı görünmez, otorite yok | Aç, 5 konu seç, bülten başlat |
| 6 | Headline "Software Dev @ X" | AI araması dışı | "AI Engineer \| Claude + RAG \| Şehir" |
| 7 | Paylaşım sonrası etkileşim yok | Algoritma boğar | İlk 60 dk kendin yorum + bağlantılara haber |
| 8 | About 500+ kelime | Okunmaz, ilk 3 satır kritik | 150-300 kelime, 3-4 paragraf |
| 9 | Sadece Türkçe | Küresel fırsat kaçar | TR ağırlık + EN kısa özet (Headline + About sonu) |
| 10 | Anthropic + OpenAI + Google AI takibi yok | Haber kaçar, yorum fırsatı yok | Üçünü de takip + haftalık 2-3 yorum |
| 11 | Sertifika alanı boş | Eğitim sinyali zayıf | Anthropic Academy 2-3 sertifika + ekle |
| 12 | LinkedIn iş ilanı uyarısı (alert) kurulmamış | Yeni ilanları geç görürsün | "AI Engineer Türkiye + Remote" iki uyarı kur, günlük e-posta |

## Çıktı kanıtları — 3 kanıt

<div class="ma-cikti-kaniti" markdown>
<div class="ma-cikti-kaniti-header">📏 Çıktı — 3 kanıt</div>

**1. Kariyer pozisyonu yazılı:**

`muhendisal-notlarim/bolum-10/01-linkedin/pozisyon.md` →
- Profilim: Junior / Mid / Lateral / Freelance
- Hedef pozisyon: _______________
- Strateji: _______________

**2. 20 keyword yerleştirildi:**

LinkedIn profili tarandı, 20 keyword 2-4 kez her yerde (Headline + About + Experience + Skills + Featured). "Keyword density" Word/notes dokümandan sayıldı.

**3. Creator Mode + 1. post yayında:**

Creator Mode on, Hafta 1 post (origin story) yayınlandı. İlk 24 saatte etkileşim sayısı ne? Screenshot kanıt.

</div>

## Görev — 3 saat kariyer hazırlığı

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — içerik stratejin canlıya geçsin</div>

### Saat 1 — Konum kararı + LinkedIn güncelleme

1. 4 profilden hangisisin? Yazılı karar.
2. Headline revize: "AI Engineer \| Python + Claude + RAG \| Şehir" (220 karakter, ilk 70 mobil için kritik).
3. About 150-300 kelime, 25 anahtar kelimenin ilk 12-15'ini doğal yerleştir; ilk 3 satırda en güçlü mesajı ver ("See more" düğmesi öncesi).
4. Skills: 10'dan 15'e çıkar. Yeni ekleler: Prompt Injection · AI Safety · Constitutional AI · MCP · Türkçe Teknik Yazım · Cost Optimization · LangGraph.
5. Creator Mode aç, 5 konu seç. Bülten oluşturma penceresi açılırsa "Türkçe AI Mühendisi Notları" gibi bir bülten başlat.

### Saat 2 — 1. post yaz

1. Hafta 1 post şablonuna göre 300-400 kelime "origin story" yaz.
2. Demo GIF (9.7'den) post'a ekle.
3. 2 canlı proje linki + "DM açık" CTA.
4. Pazartesi 08:00-10:00 yayınla.
5. İlk 30 dk çevrimiçi kal, yorumlara cevap ver.

### Saat 3 — DM hedefleri + Anthropic ekosistem takibi

1. 10 hedef şirket belirle — Türkiye + uzaktan AI odaklı (yukarıdaki örneklere bak).
2. Her şirketten 1 işe alım yöneticisi / CTO profil kaydet.
3. Anthropic + OpenAI + Google DeepMind + Mistral + Hugging Face LinkedIn takip.
4. LinkedIn iş ilanı uyarısı (Job Alert) kur: "AI Engineer Türkiye" + "AI Engineer Remote Europe" iki ayrı uyarı, günlük e-posta.
5. 6 haftalık paylaşım takvimini `muhendisal-notlarim/bolum-10/icerik-plani.md`'ye kaydet.
6. İlk DM'yi yaz, Çarşamba 10:00 gönder. Eğer 5 gün cevap yoksa tek bir takip mesajı planla.

**Başarı kriteri:** 3 saat sonunda içerik stratejin yazılı, 1 post yayında, 1 DM gönderilmiş.

Kanıt: pozisyon kararı + LinkedIn ekran görüntüsü + post + DM gönderim onayı.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**A → B:** 9 bölüm sonunda 2 canlı proje + paketleme var; 'pasif varlık'tan 'aktif görünürlük'e geçiş zamanı. Bu yüzden **teknik birikim görünür olmalı.**</li>
<li>**B → C:** Kariyer pozisyonu (junior / mid / lateral / freelance) kararı her sonraki adımın öngörüsü. Bu yüzden **konum kararı stratejiyi şekillendirir.**</li>
<li>**C → D:** LinkedIn 2026 algoritması: dwell time, erken engagement, yorum kalitesi — uzun teknik post'lar kazanıyor. Bu yüzden **kaliteli içerik algoritmayı geçer.**</li>
<li>**D → E:** 20 keyword Headline + About + Experience + Skills + Featured yerleşimi; ATS + recruiter taraması ikisi birden. Bu yüzden **keyword yerleşimi stratejik.**</li>
<li>**E → F:** 6 haftalık içerik takvimi: origin story → teknik deep-dive → maliyet → karşılaştırma → post-mortem → açık iş isteği. Bu yüzden **takvim tutarlılığı sağlar.**</li>
<li>**F → G:** DM tabanlı iş arama 2025-2026 trendi; 10-20 hedef + 3-cümle mesaj + günde 3-5 kontingent. Bu yüzden **DM ilan beklemekten önde.**</li>
<li>**G → H:** Creator Mode + personal brand üçlü eksende (teknik derinlik + pragmatizm + dil); 3-6 ay 300-2000 follower realistik. Bu yüzden **kısa vadede çabuk sonuç bekleme.**</li>
<li>**H → I:** Anthropic ekosistemi takip — LinkedIn yorum → 6 ay birikim → recruiter dikkati. Bu yüzden **ekosistem içinde görünürlük değer katar.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Kariyer stratejin yazılı. Haftalık takvim hazır. İlk post yayında. DM refleksin var. Sonraki sayfalar (10.2 Mülakat, 10.3 Açık Kaynak, 10.4 İleri Konular, 10.5 Topluluk) bu stratejiyi **derinleştirir + sürdürür**.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[10.2 Mülakat Soruları →](02-mulakat.md)** — 30 sık soru + model cevap + STAR formatı + maaş müzakeresi.

← [Bölüm 10 girişi](index.md) &nbsp;|&nbsp; [9.7 Portföy Paketleme](../bolum-9/07-github.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [LinkedIn Creator Education](https://www.linkedin.com/help/linkedin) + [Justin Welsh Solopreneur newsletter](https://www.justinwelsh.me/) (LinkedIn personal brand otoritesi) + [Lenny Rachitsky newsletter](https://www.lennysnewsletter.com/) (tech career stratejisi). Üçü farklı bakış: LinkedIn resmi + kişisel brand + product-career. Hafta sonu 1 saat taraması, içerik stratejin keskinleşir.
</div>
