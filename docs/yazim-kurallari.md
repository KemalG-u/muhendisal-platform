# MühendisAl — Yazım Kuralları (64 Sayfa İçin Tek Kitap)

**Tarih:** 22 Nisan 2026 · **Durum:** CANLI · **Sürüm:** v3.2
**Kapsam:** `muhendisal_kapsam_v2` (Brain)
**Pilot referans:** `docs/bolum-2/01-llm-temelleri.md`

---

## Bu Dosyanın Amacı

64 sayfa yazılırken **hiç kimse yabancı kalmayacak.** Bu belge o yabancılığı öldüren kuralları toplar. Yeni sayfa yazmaya başlamadan önce buraya tekrar bakılır. Kural unutulursa pilot sayfa (referans) açılır, karşılaştırılır.

Bu belge bir kontrat: Bölüm 0'dan Bölüm 10'a kadar her sayfa bu kurallara uyacak. Kural istisnası **sadece** belirlenmiş özel bölüm tiplerinde (aşağıda "Özel Sayfa Tipleri" başlığı) geçerlidir.

---

## Temel Soru — Her Başlık + Her Paragraf İçin

Yeni bir başlık veya paragraf yazmadan önce kendine sor:

> **"Bu konuyu hiç bilmeyen biri bu satırı okudu. Anladı mı? Anlamadıysa neden? Bunu hem yazıyla hem görsel olarak nasıl anlatırım?"**

Cevap "anlamadı"ysa → yeniden yaz veya görsel/diyagram ekle veya referans kutu koy.
Cevap "anladı ama eksik bağlam var"sa → bağlamı ekle.
Cevap "anladı ve tam"sa → devam.

---

## Kural 1 — Her Sayfada Ekosistem Diyagramı (Mermaid)

**Yer:** "Teori" bölümünün hemen ardından, "Uygulama"dan önce. Sayfada tam bir tane (bazı özel sayfalarda iki; aşağıda).

**Ne anlatır:**
- 👤 Kullanıcı (ben) nerede?
- Etrafındaki aktörler kim?
- Ne yaptığımda ne tetikleniyor?
- Çıktı nereye gidiyor?
- Hangi yollar alternatif, hangileri zincir?

**Renk sözleşmesi (sabit, 64 sayfada aynı):**

| Renk | Rol | Örnek düğümler |
|---|---|---|
| 🟣 Mor `fill:#ddd6fe,stroke:#7c3aed` | Kullanıcının kendisi | "Sen", "Takım üyesi" |
| 🔵 Mavi `fill:#dbeafe,stroke:#2563eb` | Giriş kapıları, kullanıcının dokunduğu arayüzler | Console, Python script, CLI, browser, Excel, iframe |
| 🟠 Turuncu `fill:#fed7aa,stroke:#ea580c` | Uzak servisler, asıl iş yapanlar | api.anthropic.com, Claude modeli, vector DB, embedding servisi |
| 🟡 Sarı `fill:#fef3c7,stroke:#ca8a04` | Yan aktörler, arka planda izleyenler | fatura sayacı, rate limit, log, metrik, API key saklayıcısı |

**Label kuralı:** Mermaid node label'da çok satır için `\n` kullan (HTML `<br/>` escape olur, bozar).

```
S["👤 Sen\n(bilgisayarın başında)"]       ← DOĞRU
S["👤 Sen<br/>(bilgisayarın başında)"]    ← YANLIŞ (br escape olur)
```

**Düğüm sayısı:** 8'i geçerse `subgraph` ile grupla. Okunmazsa tek diyagramda inat etme, iki ayrı diyagram yap.

**Aktör tablosu zorunlu:** Diyagramın altına gelir. Her düğüm için: adı, nerede bulunduğu, ne iş yaptığı. Diyagramda renk körlüğü olana + ekran okuyucuya erişilebilirlik sağlar.

**Template (pilot'tan al):** `docs/bolum-2/01-llm-temelleri.md` → `## Bu sayfanın ekosistemi` bölümü.

---

## Kural 2 — Anthropic Bağlamlı Öz (Link Değil, İçerik)

**Yer:** Uygulama bölümünden sonra, Çıktı Kanıtı'ndan önce.

**YANLIŞ:** "Daha fazla bilgi için [Building with the Claude API](link)"
**DOĞRU:** Kaynağın **bu sayfaya dokunan 3-5 maddesini Türkçe özetle, sayfaya göm**, en altta tek kaynak satırı.

**Format (zorunlu, değişmez):**

```markdown
<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu konuyu nasıl anlatıyor — öz</div>

[1-2 cümle: Anthropic bu konuyu hangi kaynakta hangi çerçevede anlatıyor]

**1. [Madde başlığı].** [2-4 cümle özet — sayfamızdaki uygulamayla bağ kur]

**2. [Madde başlığı].** [2-4 cümle]

**3. [Madde başlığı].** [2-4 cümle]

[Opsiyonel 4-5]

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [kaynak adı](url) (tür, dil, süre). [1-2 cümle: bu kaynak sayfamızdan bağımsız ne kazandırır — kullanıcı "ne zaman tıklarım"ı bilsin]
</div>
</div>
```

**Sonuç:** Kullanıcı o kaynağa tıklamasa bile konuyu kavrıyor. Tıklarsa zaten hazır — yabancılık çekmiyor.

**Araştırma yükümlülüğü:** Bu özeti yazmadan önce Kemal kuralı 11 uygulanır — 3+ `web_search` + 2 `web_fetch`. Tahmin ile özetleme. Kaynak yoksa açıkça "bu konuda Anthropic resmi kaynağı henüz yok, alternatif: [X]" yaz.

---

## Kural 3 — Dış Linkler Yeni Sekmede

**Otomatik:** `docs/assets/js/ekosistem.js` hook'u bunu global olarak yapıyor. Manuel iş yok.

**Kontrol:**
- Kullanıcı sayfa yüklendiğinde tüm `http://` / `https://` ile başlayan dış-host link otomatik `target="_blank" rel="noopener noreferrer external"` alır + yanında `↗` simgesi görünür.
- İç linkler (`.md` dosya referansları, `/platform/...`) aynı sekmede açılır.
- Link test: tarayıcıda **HARD REFRESH (Ctrl+Shift+R / Cmd+Shift+R)** yapılmazsa eski cache görülür — kullanıcı ilk açtığında her sayfada hard refresh uyarısı gerekmez, sadece geliştirmede.

**Yazarken dikkat:** `console.anthropic.com` gibi yazıları **link haline getirmeyi unutma** — sadece metin bırakırsan kullanıcı manuel yazmak zorunda kalır. Yaz: `[console.anthropic.com](https://console.anthropic.com)`.

---

## Kural 4 — Neden-Sonuç Zinciri (Sayfa Kapanışı)

**Yer:** Çıktı Kanıtı'ndan sonra, Sonraki Adım'dan önce.

**Amaç:** Kullanıcı sayfayı bitirince "ne yaptım, neden yaptım, ne elde ettim" zincirini **bir daha** görsün. Öğrenme pekişir, bağlam dağılmaz.

**Format:**

```markdown
<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**[Olgu].** Bu yüzden **[sonraki adım gerekli oldu]**.</li>
<li>**[Olgu].** Bu yüzden **[...]**.</li>
<li>**[Olgu].** Bu yüzden **[...]**.</li>
<li>[4-7 halka arası]</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** [1-2 cümle — elinde somut olarak ne kaldı]
</div>
</div>
```

**Halka sayısı:** En az 4, en fazla 7. 3'ten az → konu yeterince derinleşmemiş. 8+ → sayfa çok uzun, bölmek lazım.

**Sonuç cümlesi:** Eylem odaklı ("elinde X var, bundan sonra Y yapabilirsin"). Felsefi değil.

---

## Kural 5 — Her Başlık + Paragraf İçin "Yabancı Testi"

Yazarken (veya bitirip gözden geçirirken) **her başlığın + her paragrafın yanına zihninde şu notu düş:**

| Test | Uygulama |
|---|---|
| **Yeni terim geldi mi?** | İlk geçişinde tek cümlelik Türkçe tanım parantez içinde veya kutu içinde ver. Örneğin: "token (kelimenin yaklaşık %75'ine denk gelen bir parça)". |
| **Görselleştirilebilir mi?** | Konu bir akış/ilişki/yapıyı anlatıyorsa Mermaid diyagramı veya tablo kaçınılmazdır. Tek tek madde anlatıyorsa + örnekse tablo kullan. |
| **Kendi örneğimi verebilir miyim?** | Ham dokümantasyon çevirisi değil. Her kavrama **bu platformda kullandığımız somut örnek** (Bölüm 2'de "selam Claude" prompt'u gibi). |
| **Niye? sorusu cevaplı mı?** | "X yap" diyorsan arkasında "çünkü Y" olmalı. Boş talimat yok. |
| **Kullanıcı nerede durdu?** | Her bölüm geçişinde "şimdi elinde X var, şimdi Y yapacağız" köprüsü kur. |

---

## Kural 6 — Sayfa İskeleti (Değişmez)

Her sayfa bu sırayla yazılır. Bölümler atlanamaz, yerleri değiştirilemez:

```
1. H1 başlık (sayfa adı)
2. <div class="ma-meta"> — persona + süre + önkoşul + çıktı
3. ## Neden bu sayfa? — 1-2 paragraf motivasyon + konum
4. ## [Konu] kısaca — 2-3 paragraf teori, matematiksiz, yanılsama uyarısı
5. ## Bu sayfanın ekosistemi — Mermaid + aktör tablosu   [KURAL 1]
6. ## Uygulama — kod/komut/artifact, her adımda "Burada olan nedir (diyagram ref)"
7. <div class="ma-anthropic-oz"> — Anthropic bağlamlı öz         [KURAL 2]
8. <div class="ma-cikti-kaniti"> — 3 teslim seçeneği + feedback
9. <div class="ma-neden-sonuc"> — zincir + sonuç                 [KURAL 4]
10. <div class="ma-sonraki"> — sonraki sayfa + pekiştirme
```

**Pilot referansı:** `docs/bolum-2/01-llm-temelleri.md` açık tutulmalı, yeni sayfa yazarken yan yana bakılmalı.

---

## Kural 7 — Özel Sayfa Tipleri (Kural İstisnaları)

Aşağıdaki sayfa tipleri iskeletin **bazı bölümlerini atlar** veya farklı uygular. Yeni sayfa yazarken önce "bu normal sayfa mı, özel mi" diye belirle.

### Tip A — `index.md` (Bölüm Girişi)

Her bölümün ilk sayfası. **11 tane var** (Bölüm 0-10 index.md).

**Farklılıklar:**
- "Uygulama" bölümü yok — index uygulama sayfası değil
- Ekosistem diyagramı yerine **bölüm yol haritası** Mermaid'i (bu bölümdeki 5-8 sayfanın birbirine bağlanan grafiği)
- Çıktı kanıtı yerine **bölüm sonu çıktısı** (bölüm bitince elinde ne olacak özet)
- Neden-sonuç isteğe bağlı
- Anthropic öz **zorunlu** — bölümün genel konusu için

### Tip B — Platform Giriş `index.md` (Ana Sayfa)

1 tane var — `docs/index.md`.

**Farklılıklar:**
- Persona SEÇİM ekranı (3 büyük düğme)
- "Neden bu platform" bölümü (kapsam v2 özeti)
- Toplam yol haritası Mermaid'i (11 bölüm zinciri)
- Dürüst scope + beklenti yönetimi (kapsam v2 başarı/başarısızlık kriteri)
- Çıktı kanıtı yok; onun yerine "bu platformu bitirdiğinde elinde ne olacak"

### Tip C — Proje Sayfaları (Bölüm 10)

Bölüm 10 (Proje Bitişi) — **tam bir mini-proje kılavuzu**.

**Farklılıklar:**
- Ekosistem diyagramı **daha büyük**, tüm proje mimarisini kapsar
- Çıktı kanıtı **tek seçenek** (canlı deploy URL)
- Neden-sonuç zinciri tüm kurs boyunca öğrenilenleri toplar

### Tip D — Referans/Sözlük Sayfaları (varsa)

Terim sözlüğü, komut referansı gibi statik referanslar. 64 sayfanın parçası değil ama gerekirse eklenecek.

**Farklılıklar:**
- Ekosistem yok
- Neden-sonuç yok
- Sadece tablo + açıklama + kaynak

---

## Kural 8 — Araştırma Protokolü

Bilmediğim bir konuda sayfa yazmadan önce (veya Anthropic öz bloğu için) **mutlaka araştırma yap**:

1. `web_search` — 3 farklı arama (Anthropic resmi, teknik doc, topluluk)
2. `web_fetch` — Bulduğun 2 birincil kaynağı tam oku
3. Pyodide/SDK/CLI konuları için: **`anthropics/courses` GitHub repo'suna bak** (notebook örnekleri genellikle en temiz kaynak)
4. Sentezi yap → sayfaya yaz → kaynakları anthropic-oz bloğuna koy

**SEO blog yasak** (Kemal kuralı 15). Forum sadece doğrulama için, tek başına kaynak değil.

---

## Kural 9 — Türkçe Dil Kuralı

- **İngilizce terim sadece teknik zorunluluk** (örn: `messages.create`, `max_tokens`, `transformer`). İlk geçişinde Türkçe parantez ver: "transformer (dönüştürücü mimari)".
- Cümleler doğal Türkçe: "yapman gerek" yerine "yaparsın", "olabilir" yerine "olur" (Kemal preference).
- "duruma göre değişir" yasak — taraf seç (Kemal preference).
- "Harika soru" / övgü yok (Kemal preference).
- "Bir uzmana danış" yasak — kurstaki bilgiyi ver veya "bu konuda resmi kaynak yetersiz" de.

---

## Kural 10 — Görsellik Bütünlüğü

Her sayfada en az **iki görsel öğe** olmalı:

1. **Ekosistem diyagramı** (Mermaid) — zorunlu
2. **Aktör tablosu** — zorunlu
3. Opsiyonel 3. görsel:
   - Neden-sonuç zinciri (zaten numaralı görsel)
   - Tablo (karşılaştırma için — örn: "Console vs Python vs Claude Code")
   - `mermaid` sequence diagram (zaman akışı gerektiğinde — örn: HTTPS request-response)
   - Code block + satır yorum (kod anlatırken)

**Kaçınılması gerekenler:**
- 5+ paragraf metin üst üste (görsel kır)
- Sadece emoji (emoji yardımcıdır, ana iş değil)
- Ekran görüntüsü (dark mode kırılır, git'te büyür) — zorunlu değilse Mermaid tercih

---

## Kural 11 — Önce Araştır, Sonra Yaz, Sonra Test Et, Sonra Commit

Her yeni sayfa için akış:

1. **Kapsam netleştir** — Rol 1 (hedefleyici): 1 cümle çıktı hedefi yaz
2. **Araştırma yap** — Kural 8 protokolü
3. **İskeleti oluştur** — Kural 6 sırası
4. **Bölümleri yaz** — Kural 5 yabancı testi her başlıkta
5. **Ekosistem diyagramını çiz** — Kural 1
6. **Anthropic özü gömlükle** — Kural 2
7. **Neden-sonuç zincirini yaz** — Kural 4
8. **Build test** — `./scripts/rebuild.sh`, warning sıfır olmalı
9. **Canlı test** — URL aç, **hard refresh**, görsel render doğrula
10. **Commit** — `content(bölüm-X): sayfa adı — 1 cümle özet`

---

## Kural 12 — Sayfa Başlangıç Testi (5 Somut Soru)

**Ne zaman:** Yeni sayfa yazmaya başlamadan önce. Boş dosyanın üstüne H1 yazmadan önce.

**Amaç:** Sayfa yarılandığında "acaba ben bunu kime ne için yazıyorum" sorusunun çıkmaması. Bu 5 soru **hepsi somut cevap almalı**. Biri bile "duruma göre" / "herkes için" / "genel olarak" ile cevaplanıyorsa sayfa henüz yazmaya hazır değil.

### Beş Soru

**S1 — Bu sayfayı kim bitirecek? (persona)**

| | Cevap |
|---|---|
| ✅ Doğru | "Python bilen, Anthropic API'yi hiç görmemiş geliştirici" |
| ❌ Yanlış | "Herkes" / "İlgili kişi" / "Geliştiriciler" |

Cevap yoksa → Bölüm index'ine dön, persona seçim diyagramına bak. Hâlâ muğlaksa → sayfayı yazma, önce Bölüm 0'a gönder.

**S2 — Sayfa bitince kullanıcının elinde hangi somut çıktı olacak?**

| | Cevap |
|---|---|
| ✅ Doğru | "Terminal'de `python hello_claude.py` çalıştırdı, Claude'dan ilk cevabı aldı, ekran görüntüsü aldı" |
| ❌ Yanlış | "LLM'leri anlar" / "Konsept kavrar" / "Farkında olur" |

Cevap kavramsalsa → çıktı kanıtı bölümü (`ma-cikti-kaniti`) yazılamaz. Sayfayı yazma.

**S3 — Gelen kullanıcı önceden ne biliyor olmalı? (önkoşul)**

| | Cevap |
|---|---|
| ✅ Doğru | "Bölüm 0 bitti, Python 3.10+ kurulu, terminal açabiliyor, `venv` ne olduğunu biliyor" |
| ❌ Yanlış | "Biraz Python" / "Temel bilgisayar bilgisi" |

Önkoşul muğlaksa → sayfayı ikiye böl veya önkoşul oluşturan bir sayfayı önce yaz.

**S4 — Ekosistem diyagramında hangi 4-8 aktör olacak? (Kural 1 hazırlığı)**

| | Cevap |
|---|---|
| ✅ Doğru | "Sen (mor), Python script (mavi), anthropic SDK (mavi), api.anthropic.com (turuncu), Claude modeli (turuncu), fatura sayacı (sarı), API key saklayıcı (sarı)" |
| ❌ Yanlış | "Kullanıcı ve sistem" / "İstemci-sunucu" |

Aktörler sayılamıyorsa → konu yeterince derinleşmemiş. Önce Kural 8 araştırması yap, sonra dön.

**S5 — Anthropic-öz bloğu hangi resmi kaynağa yaslanacak? (Kural 2 hazırlığı)**

| | Cevap |
|---|---|
| ✅ Doğru | "docs.claude.com/en/api/messages — 'Request body' ve 'System prompts' bölümleri + `anthropics/courses` repo `01_basic_api_usage.ipynb`" |
| ❌ Yanlış | "İnternette bakarız" / "Birkaç kaynak var" / (boş) |

Birincil kaynak yoksa → Kural 8'i uygula: 3+ `web_search` + 2 `web_fetch`. Yine yoksa Anthropic-öz bloğunu "resmi kaynak henüz yok, alternatif: [X]" kalıbıyla yaz.

### Karar Matrisi

| 5 sorunun durumu | Ne yap |
|---|---|
| 5'i de somut cevaplı | Yazmaya başla. Kural 11 akışına geç. |
| 1-2'si muğlak | Muğlakları netleştir (15 dk kapsam notu). Sonra başla. |
| 3+ muğlak | Sayfa henüz olgunlaşmamış. Brain'e `muhendisal_sayfa_<konu>_sorular.md` aç, notları topla, 1 gün sonra dön. |

### Sayfa Başında Yazılı Kanıt

Cevaplar dosyanın **en tepesindeki `ma-meta` bloğunda** zaten yer tutar (persona + süre + önkoşul + çıktı). S4 ve S5 ise yazarın zihninde/scratch notunda tutulur, sayfada görünmez — ama diyagram + öz bloğu yazılırken oradan beslenir.

**Kendini denetle:** Sayfa bittiğinde `ma-meta` bloğundaki persona + önkoşul + çıktı ile sayfanın gerçek içeriği aynı hikâyeyi anlatıyor mu? Uyuşmuyorsa S1-S3'ü yanlış cevaplamışsın — başa dön.

---

## Pilot Sayfa — Canlı Referans

**URL:** https://wiki.oluk.org/platform/bolum-2/01-llm-temelleri/
**Dosya:** `docs/bolum-2/01-llm-temelleri.md` (v3.2, 18.9 KB)
**Sayfa tipi:** Normal (Tip olmayan — standart)

Bu sayfa bu kurallar kitabının canlı uygulamasıdır. Yeni sayfa yazmaya başlarken:
1. Pilot dosyayı yan pencerede aç
2. Bu kural kitabını yan pencerede aç
3. Yeni sayfa iskeletini pilot'tan kopyala
4. İçerikleri kendi konuna göre yaz, **yapıyı değiştirme**
5. Her 3 bölümde bir kural kitabına dönüp "atladığım kural var mı" kontrolü yap

---

## Kural Dışı Durumlar — Karar Ağacı

**Bazı sayfalarda kuralları uygulamak mantıksız görünürse:**

| Durum | Karar |
|---|---|
| Konu tamamen teorik (örn: "LLM tarihi") | Yine de ekosistem diyagramı — aktörler: araştırmacı, üniversite, lab, makale. Kültürel bile olsa akış var. |
| Konu çok kısa (örn: "Python virtualenv kurulumu") | Ekosistem minimum tutulur (3 düğüm: sen, paket kaynağı, disk) ama atılamaz. |
| Kullanıcı gerçekten ilk sayfada | `docs/index.md` — Tip B kurallarına geç |
| Bölüm girişi | `bolum-X/index.md` — Tip A kurallarına geç |

**Son karar:** Bir kural atlanacaksa gerekçesi brain'de `muhendisal_kurallar_istisna` sayfasına yazılır. Aksi halde atlanmaz.

---

## Güncelleme Geçmişi

- **v3.2** (22 Nis 2026) — Kural 12 (5-soru başlangıç testi) eklendi, glossary + `hooks/pre_build.py` devreye alındı (45 terim auto-inject), pilot sayfa (`bolum-2/01-llm-temelleri.md`) v3.2 yeniden yazıldı.
- **v3.1** (21 Nis 2026) — Kemal pilot kontrol sonrası: `<br/>` → `\n` Mermaid fix, "yabancı testi" (Kural 5) eklendi, özel sayfa tipleri (Kural 7) netleştirildi.
- **v3.0** (21 Nis 2026) — Kemal "yabancılık öldür" yönergesi: 4 zorunlu blok (ekosistem + anthropic-oz + dış link + neden-sonuc).
- **v2.0** (21 Nis 2026) — Kapsam v2 onayı: persona etiketleri, çıktı kanıtı, Anthropic köprüsü.
- **v1.0** (20 Nis 2026) — İlk taslak (64 iskelet sayfa açıldı).
