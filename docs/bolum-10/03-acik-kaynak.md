# 10.3 Açık Kaynak Katkı — İlk PR Stratejisi

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> GitHub hesap + 2-3 kendi projen (9.4 + 9.5). Git + PR süreciyle temel tanışıklık.</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> 3 ay içinde **5-10 açık kaynak PR** birikimin var. Her biri Anthropic Cookbook, Qdrant, LangChain veya benzer AI projelere. Junior + lateral mover için **en güçlü referans inşası** — CV'de "5 açık kaynak katkı" + GitHub profile "Contributed to" badge. LinkedIn DM'de "Anthropic Cookbook'a katkıda bulunuyorum" cümlesi ile mülakat daveti %30-50 artar.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **PR** (Pull Request) = kodunu proje sahiplerine inceleme için göndermek; kabul edilirse `main` branch'e merge olur. **Issue** = proje sahibinin açtığı sorun/feature request; sen yakala → PR at → çöz. **Good first issue** = yeni katkı verenler için işaretli kolay issue'lar. **Upstream** = orijinal proje; senin fork'un "downstream". **Squash merge** = PR'ın N commit'ini 1 commit'e birleştirip merge etme.

## Neden bu sayfa?

İş aramada CV'nin üzerinde 3 şeyi var: (1) eğitim, (2) iş tecrübesi, (3) projeler. Junior için ilk ikisi zayıf olabilir; **üçüncüsü güçlü** olmalı. Projelerin 2 boyutu:

- **Senin projelerin** (9.4 + 9.5) — sıfırdan kurduğun, kendi kararların
- **Başkasının projelerine katkı** — koordinasyon + code review + kodlama disiplin kanıtı

**İkinci boyut junior için altın.** Şirket "bu aday başkalarıyla çalışabilir mi, review alabilir mi, disiplin içinde kod yazıyor mu?" sorusunun cevabını **senin kodundan değil** PR tarihçenden görür. 5-10 merged PR = "evet, yapabiliyor" kanıtı.

İkincisi: Açık kaynak PR **topluluk sermayesi**. Anthropic Cookbook'a PR atarsan → Anthropic developer relations ekibi adını görür → 6 ay sonra "bu adaya bakalım" fırsatı. LangChain'e katkı → LangChain ekosistem şirketlerinde tanınırlık. Qdrant'a katkı → CV'de Qdrant spesifik uzmanlık kanıtı.

Üçüncüsü: **Açık kaynak öğrenme hızlandırıcısı.** Başkalarının code review'i gelir, senin hatalarını görürler, kod stilini şekillendirirler. 1 kaliteli review 10 saat solo kodlamadan değerli.

## İlk PR — beginner-friendly etiketler

GitHub'ta `good first issue`, `help wanted`, `beginner-friendly`, `easy` etiketleri vardır. Yeni katkı verenler için özel işaretlenmiş issue'lar.

### Arama yolu

**GitHub global search:**

```
https://github.com/issues?q=is:issue+is:open+label:%22good+first+issue%22+language:Python
```

Python + açık issue + good-first-issue etiketli liste.

**Belirli org'da:**

```
https://github.com/search?q=org:anthropics+label:%22good+first+issue%22+is:open
https://github.com/search?q=org:qdrant+label:%22good+first+issue%22+is:open
https://github.com/search?q=org:langchain-ai+label:%22good+first+issue%22+is:open
```

**Tool:** [goodfirstissues.com](https://goodfirstissues.com/) — filtreli arama UI.

### Issue seçim kriterleri

Her good-first-issue atlama ideal değil. 4 kriter:

1. **Senin alanında mı?** AI Engineer'sin → Python + LLM + vector DB + agent. React frontend issue'sunu çözme.
2. **Sahip aktif mi?** Issue son 30 gün içinde maintainer yorumu var mı? Ölü projelerde PR merge edilmez.
3. **Scope küçük mü?** Dokumentation fix, test ekleme, küçük bug → ilk PR için iyi. Complete rewrite → sonraya.
4. **Sahiplenilmiş mi?** Başkası zaten "I'll take this" demiş mi? Alma.

### İyi ilk PR örnekleri

- **Dokumentation typo fix** — README veya docstring'de hata; 5 dk iş.
- **Test eksiği** — bir fonksiyon için test yok, yazılır.
- **Error mesajı iyileştirme** — "Error" yerine kullanıcıya yardımcı mesaj.
- **Type hint ekleme** — Python dosyasında type hints eksik; mypy strict altına getirir.
- **Deprecated API güncelleme** — kütüphane yeni sürüm, docs/examples'da eski kullanım var.

**Kaçın:**

- **Önerilmemiş büyük refactor** — "Bu dosyayı yeniden yazdım" → reject.
- **Maintainer'ın görmediği yeni feature** — önce `issue` aç, tartış, sonra PR.
- **Birkaç farklı değişikliği tek PR'da** — "docs + bug fix + refactor" birlikte → review zor, reject.

## Anthropic Cookbook — hedef #1

[github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) — Anthropic'in resmi Jupyter notebook koleksiyonu. Claude kullanım örnekleri.

### Neden Anthropic Cookbook ideal?

1. **Aktif maintain** — Anthropic developer relations ekibi düzenli günceller.
2. **Yüksek görünürlük** — 15K+ star, binlerce fork.
3. **Senin stack'in** — Claude, MCP, agent örnekleri; senin derinliğin.
4. **Kariyer sinyal** — Anthropic ekibi PR'ını okur. Recruiter "bu aday Anthropic ekosistemine katkıda" der.

### Nasıl katkı verirsin

**Seçenek 1 — Mevcut notebook iyileştirme:**

1. `skills/` dizinindeki notebook'ları incele.
2. Hata, eski API, Türkçe çeviri fırsatı ara.
3. `git clone` → fork → branch → düzelt → PR.

**Örnek: Türkçe notebook ekleme:**

```
skills/
  classification/
    guide.ipynb           (İngilizce, mevcut)
    guide.tr.ipynb        (Türkçe, senin PR'ın)
```

Sistem prompt Türkçe çevir + Türkçe örnek veri + açıklamalar. **Pedagojik değer yüksek** — Türkçe AI Engineer topluluğuna hizmet.

**Seçenek 2 — Yeni pattern/tutorial ekleme:**

Bir use-case için notebook yok mu? Sen yaz:

- "Türkçe RAG chatbot — 9.4 referansla step-by-step"
- "MCP server — Telegram bot entegrasyonu"
- "Agent evaluator pattern — 9.5 icerik-ozet-agent adapte"

Önce issue aç → "Bu notebook'u eklemeyi düşünüyorum, kabul edilir mi?" — maintainer yeşil verir sonra PR.

**Seçenek 3 — Test ekleme:**

Notebook'lar test sistemi sınırlı. Bir notebook için smoke test yaz (anthropic API çağrısı mock + çıktı kontrol). PR olarak gönder.

## Qdrant — vector DB alanında derinleş

[github.com/qdrant/qdrant-client](https://github.com/qdrant/qdrant-client) — Qdrant Python SDK (3.5 + 9.4'te kullandın).

### Katkı fırsatları

1. **Dokümentasyon eksikleri** — docstring boş method'lar, usage example eksik.
2. **Type hint iyileştirme** — bazı methodlar `Any` kullanıyor, daha spesifik type eklenebilir.
3. **Example notebook** — "Turkish semantic search" notebook, Voyage + Qdrant + FastAPI. 3.5 projen adapte edilebilir.
4. **Bug fix** — `good first issue` etiketli küçük hatalar.

**Kanal:** [Qdrant Discord](https://qdrant.to/discord) — soru sorabilir, maintainer ile temas kurabilirsin; PR öncesi tartışma.

## LangChain — geniş ekosistem

[github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) — RAG + agent için en yaygın Python framework (Türkiye de dahil).

### Katkı farkındalık

LangChain **büyük**. PR çok, maintainer az → **PR kuyrukta 2-6 ay bekleyebilir**. Anthropic Cookbook'a göre yavaş süreç.

**Stratejiler:**

1. **Küçük PR** — dokumentation, type hint, basit bug. Hızlı merge.
2. **Integration module** — az kullanılan provider için integration eklemek (ör. yeni bir vector DB).
3. **Example notebook** — `docs/docs/integrations/` altında.

**Uyarı:** LangChain'in `langchain-core`, `langchain-community`, `langchain-openai`, vb. alt paketleri ayrılmış (monorepo). Doğru paket bul, yanlış yere PR atma.

## Commit hygiene — reviewer'ın hayatını kolaylaştır

PR kabul oranı **kod kalite** + **PR sunumu** ikisi birden. Sunum kötüyse iyi kod da reject.

### 1. Commit mesajı formatı

[Conventional Commits](https://www.conventionalcommits.org/) yaygın standart:

```
fix: Qdrant payload boyut sınırı 16KB'a çıkarıldı

Qdrant native 64KB'a kadar destekliyor ama client-side 16KB
sınırlandırılmıştı (legacy). Testler 64KB için başarılı, limit
kaldırıldı.

Fixes #1234
```

**Prefix'ler:**

- `feat:` yeni özellik
- `fix:` bug düzeltme
- `docs:` dokümantasyon
- `test:` test ekleme
- `refactor:` kod yapısı (davranış aynı)
- `perf:` performans
- `chore:` bakım (deps, build)

### 2. Commit küçük + odaklı

**Kötü:** `"Fixed stuff"` — 50 dosya değişmiş.
**İyi:** 3 ayrı commit:
- `fix: embedding dim mismatch in batch processing`
- `docs: add Turkish example in README`
- `test: cover batch processing error cases`

**`git add -p`** (patch mode) — dosyanın bir kısmını commit et, diğerini ayırarak. Atomic commit için zorunlu.

### 3. PR açıklama şablonu

```markdown
## Özet
Bu PR [X problemini] [Y yöntemle] çözüyor.

## Değişenler
- Fixed: Qdrant client 16KB payload sınırı kaldırıldı
- Added: 64KB için test case

## Motivasyon
Issue #1234'te rapor edilen problemi gideriyor. RAG chunk'ı 20KB olunca
batch insert başarısız oluyordu.

## Test
- `pytest tests/test_batch.py::test_large_payload` yeşil
- Local 50K chunk'lı dataset ile dene

## Checklist
- [x] Testler geçiyor
- [x] `ruff check .` temiz
- [x] Docstring güncellendi (varsa)
- [x] CHANGELOG'a eklendi (varsa)
- [ ] Breaking change VAR mı? (hayır)
```

**Reviewer 30 saniyede PR'ı anlar.** Merge hızı 3× artar.

## Code review alma — refleksin

İlk PR'ın geldi, maintainer comment bıraktı: *"Bu yaklaşım yerine X deseyi neden kullanmadın?"*

### Kötü cevaplar

- **Savunma:** "Çünkü X yöntemi daha iyi" → egolu, kabul edilmez.
- **Pasif:** PR kapat, yeniden yazma → maintainer yorumunu değerlendirmedin.
- **Gecikme:** 3 gün cevap yok → PR stale, maintainer unutur.

### İyi cevap formatı

1. **Teşekkür** — "Dikkat için teşekkürler" (samimi, abartma).
2. **Cevap** — "X yöntemini bilmiyordum, şöyle düşünmüştüm: [açıklama]".
3. **Soru/eylem** — "X pattern daha iyi görünüyor; PR'ı o şekilde güncelleyeyim mi?" veya "Bu case için X çalışmaz çünkü [neden]; ne önerirsin?".

**24 saat içinde cevap ver.** Stale PR ölür.

### Maintainer "no" dediyse

Bazen PR kabul edilmez — "Projenin vizyonuna uymuyor" gibi. Kötü değil, öğrenim:

- **Teşekkür et** — "Anladım, teşekkürler incelediğin için."
- **PR'ı kapat** — dürüstçe.
- **Alternatif** — aynı iyileştirmeyi kendi fork'unda yap, README'ye "custom improvements" olarak belgele. Senin işine yaramaya devam eder.

**Bir reject 10 başarılı PR'dan daha değerli ders** — neden kabul edilmediği maintainer'ın zihniyetini gösterir.

## First-time contributor tuzakları — 8 yaygın hata

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Kurulum okumadan PR | Testler geçmez, revize | README + CONTRIBUTING.md zorunlu |
| 2 | Fork'tan clone değil, direkt clone | Push reddeder | `fork` butonu → `git clone fork URL` |
| 3 | `main` branch'e commit | Proje convention ihlali | Yeni branch: `git checkout -b fix/X` |
| 4 | 1 PR'da 5 değişiklik | Review zor, reject | Her değişiklik ayrı PR |
| 5 | Test yazmadan bug fix | Regression engellenmez | Bug için önce test, sonra fix |
| 6 | Commit mesajı 1 kelime | Hikâye yok | Conventional Commits formatı |
| 7 | PR açıklama boş | Maintainer neyi değerlendirecek? | Şablon + motivasyon + test |
| 8 | Maintainer cevabı görmezden | PR stale, kapanır | 24-48 saat içinde yanıt |

## 3 ay plan — 5-10 PR hedefi

<table class="ma-aktorler" markdown>

| Ay | Hedef | Kaynak öneri |
|---|---|---|
| **1** | 1 PR — Anthropic Cookbook typo/docs fix | Kolay başlangıç |
| **1-2** | 2 PR — Qdrant/LangChain docs veya küçük bug | Issue araması + tartışma |
| **2** | 1 PR — yeni notebook (Türkçe RAG veya MCP örnek) | Önce issue aç |
| **3** | 1 PR — integration modülü veya test ekleme | Orta karmaşıklık |
| **3+** | 2-3 PR — serbest; senin ilgin | Rutin |

</table>

**Toplam 3 ay → 5-7 merged PR.** CV + LinkedIn'de somut hikâye.

## Referans inşası — GitHub profile impact

Merged PR'ların GitHub profil sayfanda **Contributions** bölümünde görünür:

- Contributor badge (Anthropic Cookbook → "Contributor" etiketi profil altında).
- Repo contributions list — açık ve sayılabilir.
- Pinned repo'ların yanında pinned Gists veya katkı verdiğin projeler.

**LinkedIn tarafında:** Featured bölümüne "Contributed to Anthropic Cookbook" başlığıyla PR URL'ini ekle. Post örnek (hafta 3 content takvimi - 10.1):

> "Anthropic Cookbook'a bu hafta 1. PR'ım merge edildi: [linkage]. Konu: Türkçe RAG tutorial notebook ekleme. 3 aylık AI Engineer yolculuğumun görünür parçası."

Bu tür post **mülakat DM davetleri** getirir.

## CTO tuzakları — 8 açık kaynak hatası

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Sadece "star" — hiç PR | Referans yok | Ayda 1 PR minimum |
| 2 | Büyük feature ilk PR | Reject, moral düşer | Docs/typo ilk başla |
| 3 | Projenin style guide okumama | PR revize edilir | CONTRIBUTING.md + ruff |
| 4 | PR açtıktan sonra dalma | Stale kapanır | Maintainer cevap bekle, yanıtla |
| 5 | Kendi kod stilini dayatma | Reject | Projenin formatına uy |
| 6 | "README'yi baştan yazdım" | Reddedilir, alay konusu | Küçük iyileştirme |
| 7 | Fork'u sync'lememiş | Conflict + eski base | `git fetch upstream && git rebase` |
| 8 | Reddedilen PR'a öfke | Topluluk dışında | "Teşekkür, öğrendim" + kapat |

## Anthropic ekosistemi — Claude ile PR yazma

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude Code + PR süreci</strong></summary>

**Claude Code** (terminal + IDE için Anthropic ürünü) açık kaynak PR sürecinde değerli:

1. **Repo keşfi** — `claude` komutu ile proje diziniini açıp "bu projede X nasıl yapılır?" sor. Claude `CONTRIBUTING.md` + önceki PR'ları okuyarak proje konvansiyonunu **öğretir**.
2. **Issue analizi** — Issue linki ver → Claude sorunun nedenini + çözüm yolunu çıkarır.
3. **Kod yazma** — Claude senin stack'inde kod yazar, test ekler.
4. **PR açıklama** — "Bu değişiklikleri bir PR açıklaması olarak yaz" → Claude şablona göre açıklar.
5. **Review cevapları** — Maintainer yorumunu ver → Claude nazik + teknik cevap önerir.

**Önemli not:** Claude'un yazdığı kodu **kendi anladığından emin ol** commit etmeden önce. Maintainer sorar: "Bu satır niye böyle yazıldı?" — sen cevaplayamazsan PR zayıflar.

### Anthropic'in açık kaynak politikası

Anthropic kendi projelerine (anthropic-cookbook, anthropic-sdk-python, mcp) CLA (Contributor License Agreement) istemez; MIT lisansı + normal PR süreci. Katkı süreci standartlaşmış.

[Anthropic open-source list](https://github.com/anthropics) — hepsi açık. Seç birini, 3 ay katkı.

### Community Awards

Anthropic Discord/Slack'te "Community Contributor" rozeti veriliyor (gayri resmi). 5+ merged PR = tanınma. Resmi program 2026'da netlikleşiyor.

</details>

## Çıktı kanıtları — 3 kanıt

<div class="ma-cikti-kaniti" markdown>
<div class="ma-cikti-kaniti-header">📏 Çıktı — 3 kanıt</div>

**1. İlk PR merged:**

Anthropic Cookbook veya Qdrant veya LangChain'de merged PR URL. GitHub'da "Contributor" badge profile altında.

**2. 3 ay plan dolduruldu:**

`muhendisal-notlarim/bolum-10/03-acik-kaynak/plan.md` — 3 ay hedefleri + her birine takvim + issue URL'ler.

**3. Commit hygiene refleksi:**

Son 3 kendi commit'in Conventional Commits formatında (`feat:`, `fix:`, `docs:`). `git log --oneline -10` görsel kanıt.

</div>

## Görev — 1 saat ilk PR

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — bu hafta ilk PR'ı at</div>

1. [Anthropic Cookbook issues](https://github.com/anthropics/anthropic-cookbook/issues) listesine git.
2. Açık issue'lara bak; **documentation** / **typo** / **example improvement** türü küçük bir tane seç.
3. (Yoksa) `skills/` dizininde bir notebook oku; Türkçe çeviri veya küçük iyileştirme (comment netlik, kullanımlar güncel) olasılığı var mı?
4. Fork + clone + branch + değişiklik + commit (Conventional format) + push + PR.
5. PR açıklama şablonuna uy.
6. 2-3 gün bekle, maintainer cevap ver.

**Başarı kriteri:** 1 hafta sonunda PR açılmış, merged veya aktif review'da.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

- **A → B:** Açık kaynak katkı CV'de 3. boyut (senin projelerin + işin + katkı); junior için altın.
- **B → C:** Beginner-friendly etiket aramayla başla; good-first-issue + help-wanted.
- **C → D:** Anthropic Cookbook ideal hedef — aktif, yüksek görünürlük, senin stack'in.
- **D → E:** Qdrant + LangChain eş değerli; farklı ekosistem derinleşmeleri.
- **E → F:** Commit hygiene + PR açıklama şablonu reviewer'ın hayatını kolaylaştırır, merge hızı 3×.
- **F → G:** Code review alma refleksi: teşekkür + cevap + eylem; 24 saat yanıt.
- **G → H:** 3 ay plan — ayda 1-3 PR, 5-10 toplam hedef.
- **H → I:** GitHub profile contributions + LinkedIn featured → recruiter görünürlük.

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Açık kaynak katkı disiplini elinde. İlk PR 1 hafta içinde atıldı, 3 ay sonra 5-10 merged PR CV'de. Sonraki (10.4): İleri konular ve trendler — sürekli öğrenme ritmi için 2026 sonrası landscape.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[10.4 İleri Konular ve Trendler →](04-ileri-konular.md)** — 2026 sonrası AI manzarası: agents at scale, on-device inference, AI safety research.

← [10.2 Mülakat Soruları](02-mulakat.md) &nbsp;|&nbsp; [Bölüm 10 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [First Contributions](https://github.com/firstcontributions/first-contributions) (adım adım tutorial) + [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/) + [GitHub Skills — First Day on GitHub](https://skills.github.com/). Üçü toplam 3 saat, PR süreci tamamen oturur.
</div>
