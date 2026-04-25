# 10.3 Açık Kaynak Katkı — İlk PR Stratejisi

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~25 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> GitHub hesap + 2-3 kendi projen (9.4 + 9.5). Git + PR süreciyle temel tanışıklık.</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> 3 ay içinde **5-10 açık kaynak PR** birikimin var. Her biri Anthropic Cookbook, Qdrant, LangChain veya benzer AI projelere. Junior + lateral mover için **en güçlü referans inşası** — CV'de "5 açık kaynak katkı" + GitHub profile "Contributed to" badge. LinkedIn DM'de "Anthropic Cookbook'a katkıda bulunuyorum" cümlesi ile mülakat daveti %30-50 artar.</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **PR** (Pull Request — çekme isteği) = kodunu proje yöneticilerine inceleme için göndermek; kabul edilirse `main` dalına birleştirilir. **Issue** (mesele) = proje sahibinin açtığı sorun veya özellik isteği; sen yakala → PR at → çöz. **Good first issue** (iyi ilk mesele) = yeni katkı verenler için işaretli kolay meseleler. **Upstream** (yukarı akış) = orijinal proje; senin çatalın "downstream" (aşağı akış). **Squash merge** (sıkıştırılarak birleştirme) = PR'ın N commit'ini tek commit'e indirgeyip birleştirme. **CLA** (Contributor License Agreement — Katkı Verici Lisans Sözleşmesi) = bazı projelerin (Google, Meta) katkı vermeden önce imzalattığı sözleşme; lisans haklarını netleştirir. **Maintainer** (yönetici) = projeyi sürdüren kişi; PR'ları kabul/reddeden. **Triage** (öncelendirme) = açılan issue/PR'ları etiketleme + önceliklendirme; birçok projede topluluk üyeleri yardımcı olur.

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

[github.com/anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) — Anthropic'in resmi Jupyter not defteri koleksiyonu. Claude kullanım örnekleri. **Tarihsel not:** Repo eskiden `anthropic-cookbook` adındaydı; 2024'te `claude-cookbooks` adıyla yeniden adlandırıldı. Eski URL hâlâ yönlendiriyor olsa da yeni adı kullan.

### Neden Anthropic Cookbook ideal?

1. **Aktif sürdürme** — Anthropic Developer Relations + Applied AI ekipleri düzenli günceller.
2. **Yüksek görünürlük** — 15K+ yıldız, binlerce çatal (fork); Anthropic'in ana eğitim kaynaklarından.
3. **Senin yığının (stack)** — Claude, MCP, ajan örnekleri; senin derinliğin.
4. **Kariyer sinyali** — Anthropic ekibi PR'ını okur. İşe alımcı "bu aday Anthropic ekosistemine katkıda" der.
5. **CLA yok** — Anthropic 2024'ten beri kendi açık kaynak repolarında CLA istemiyor; bireysel katkı süreci hızlı.

**Yan repolar (aynı org):**

- [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) — resmi Python SDK (`pip install anthropic`).
- [anthropics/claude-code](https://github.com/anthropics/claude-code) — Claude Code CLI; istek/öneri için issue, doc PR.
- [anthropics/courses](https://github.com/anthropics/courses) — Anthropic Academy'nin açık kaynak ders materyalleri; yazım hatası ve Türkçe çeviri PR'ları için iyi başlangıç.

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

## Qdrant — vektör veritabanı alanında derinleş

[github.com/qdrant/qdrant-client](https://github.com/qdrant/qdrant-client) — Qdrant Python SDK (3.5 + 9.4'te kullandın). [github.com/qdrant/qdrant](https://github.com/qdrant/qdrant) — Rust tarafındaki ana motor; Rust biliyorsan ayrı bir alan.

### Katkı fırsatları

1. **Belge eksiklikleri** — docstring boş yöntemler, kullanım örneği eksik.
2. **Tür ipucu (type hint) iyileştirme** — bazı yöntemler `Any` kullanıyor, daha özelleşmiş tür eklenebilir.
3. **Örnek not defteri** — "Turkish semantic search" not defteri, Voyage 4 + Qdrant 1.18 + FastAPI. 3.5 projen uyarlanabilir.
4. **Hata düzeltmesi** — `good first issue` etiketli küçük hatalar.
5. **Göç (migration) belgesi** — Qdrant 1.18'le `client.search()` → `client.query_points()` API değişimi yaşandı; üst sürüme geçen kullanıcılara yardımcı belge eksik olabilir; göç notu bir PR olarak iyi katkı.

**İletişim kanalı:** [Qdrant Discord](https://qdrant.to/discord) — soru sorabilir, yöneticilerle temas kurabilirsin; PR öncesi tartışma. Türkiye saatine en yakın etkin saatler 14:00-19:00 (CEST).

## MCP referans sunucuları — Linux Foundation altında yeni standart

[github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — MCP referans sunucu koleksiyonu (filesystem, git, GitHub, Slack, Postgres, fetch, brave-search, vb.). **Aralık 2025'te repo yönetişimi Linux Foundation altındaki AI Alliance Foundation (AAIF) bünyesine geçti** — yönetişim Anthropic'ten bağımsız, OpenAI / Google / Microsoft maintainer havuzunda.

### Neden burası katkı verme alanı için iyi

1. **Anthropic + OpenAI + Google üç ekosistem ortak repo** — tek katkı, üç ekosistem görünürlüğü.
2. **Çapraz dil** — TypeScript + Python + Go + Rust referans sunucular; senin dilini seç.
3. **Yeni MCP istemcileri** — Claude Desktop, Cursor, Zed, Continue ekosistemleri sürekli yeni sunucu ihtiyacı duyuyor.
4. **Türkçe MCP sunucusu fırsatı** — Türkçe servislere (e-Devlet açık veri, Türkiye İstatistik Kurumu API) MCP sunucusu yazıp eklersen niş katkı.

[github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) — Python SDK; `mcp` paketi pip ile gelir. Belge ve örnek PR'ları için iyi.

## LangChain + LangGraph — geniş ekosistem

[github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) — RAG + ajan için en yaygın Python çatısı (Türkiye dahil). 2025'te **LangChain 1.x** dalı çıktı; eski 0.x API'sinden kırılma var (mesela `LLMChain` deprecated, doğrudan `RunnableSequence` ya da yeni `chat_models` arayüzü kullanılıyor). [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) — durumlu ajan grafları için ayrı kütüphane; LangChain 1.x'te ajan tarafının fiili önerilen yolu.

### Katkı için bilinmesi gerekenler

LangChain **büyük**. Çok PR, az yönetici → **PR kuyrukta 2-6 ay bekleyebilir**. Anthropic Cookbook'a göre yavaş bir süreç. 2025'te LangChain ekibi inceleme akışını "core team triage" → "subject area maintainer" düzenine ayırdı; doğru etiketli olduğunda hızlanıyor.

**Stratejiler:**

1. **Küçük PR** — belge, tür ipucu, basit hata. Hızlı birleştirme.
2. **Tümleştirme (integration) modülü** — az kullanılan sağlayıcı için tümleştirme eklemek (ör. yeni bir vektör veritabanı).
3. **Örnek not defteri** — `docs/docs/integrations/` altında veya `docs/docs/tutorials/` içinde Türkçe örnek.
4. **Migrasyon belgesi** — 0.x → 1.x göç süreci yaşayan kullanıcı çoktur; konuya özgü göç notu (ör. "Anthropic ile LangChain 0.3'ten 1.1'e geçiş") iyi PR.

**Uyarı:** LangChain'in `langchain-core`, `langchain-community`, `langchain-openai`, `langchain-anthropic`, `langchain-qdrant` vb. alt paketleri ayrılmış (monorepo). Doğru paketi bul, yanlış yere PR atma. `langchain-anthropic` için PR atarken Anthropic SDK uyumluluğu (mevcut sürüm `anthropic` Python SDK 0.45+) test edilmeli.

## Commit hygiene — reviewer'ın hayatını kolaylaştır

PR kabul oranı **kod kalite** + **PR sunumu** ikisi birden. Sunum kötüyse iyi kod da reject.

### 1. Commit mesajı biçimi

[Conventional Commits 1.0.0](https://www.conventionalcommits.org/tr/v1.0.0/) yaygın standart (Türkçe çevirisi de var):

```
fix(qdrant): payload boyut sınırı 16KB'tan 64KB'a yükseltildi

Qdrant motoru yerel olarak 64KB'a kadar destekliyor ama istemci
tarafında 16KB ile sınırlandırılmıştı (eski davranış). Testler
64KB için başarılı, sınır kaldırıldı.

Fixes #1234
```

**Önekler:**

- `feat:` yeni özellik
- `fix:` hata düzeltmesi
- `docs:` belge
- `test:` test ekleme
- `refactor:` kod yapısı (davranış aynı)
- `perf:` başarım
- `chore:` bakım (bağımlılıklar, build)
- `ci:` CI yapılandırması
- `build:` paketleme/derleme

**Kapsam (scope) parantez içinde:** `feat(rag):`, `fix(qdrant):` gibi modül adı eklenebilir; LangChain monorepo benzeri büyük projelerde zorunlu.

**Kırıcı değişiklik:** `feat!:` ya da gövdede `BREAKING CHANGE:` satırı; SemVer'in major sürüm artışını tetikler.

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

## 3 ay planı — 5-10 PR hedefi

<table class="ma-aktorler" markdown>

| Ay | Hedef | Kaynak öneri |
|---|---|---|
| **1** | 1 PR — Anthropic Cookbook yazım/belge düzeltmesi | Kolay başlangıç, repo: `anthropics/claude-cookbooks` |
| **1-2** | 2 PR — Qdrant 1.18 göç notu + LangChain 1.x belge | İssue araması + tartışma |
| **2** | 1 PR — yeni MCP sunucusu (Türkçe açık veri) | `modelcontextprotocol/servers` reposunda issue aç önce |
| **2** | 1 PR — yeni not defteri (Türkçe RAG veya değerlendirici örüntüsü) | Önce issue aç, kabul olursa yaz |
| **3** | 1 PR — tümleştirme modülü veya test ekleme (`langchain-anthropic` veya `langchain-qdrant`) | Orta karmaşıklık |
| **3+** | 2-3 PR — serbest; senin ilgin | Rutin |

</table>

**Toplam 3 ay → 6-8 birleştirilmiş PR.** CV + LinkedIn'de somut hikâye.

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

Anthropic kendi projelerine (claude-cookbooks, anthropic-sdk-python, claude-code, courses) CLA (Katkı Verici Lisans Sözleşmesi) **istemiyor**; MIT lisansı + normal PR süreci. Katkı süreci standartlaşmış. **Karşılaştırma:** OpenAI ve Google'ın bazı projeleri CLA imzası ister (DocuSign üzerinden); imzalamadığında PR otomatik olarak engellenir. MCP referans repo'su (Linux Foundation altında) DCO (Developer Certificate of Origin) modeli kullanıyor; commit'lerine `git commit -s` ile imza eklemen yeterli, ayrıca form doldurmana gerek yok.

[Anthropic open-source list](https://github.com/anthropics) — hepsi açık. Seç birini, 3 ay katkı ver.

### Topluluk ödülleri

Anthropic Discord'da "Community Contributor" / "Helpful" gibi gayri resmi rozetler dolaşır. 5+ birleştirilmiş PR = topluluk içi tanınma. Anthropic 2025'in son çeyreğinde "Anthropic Builder" programını ilan etti — etkin katkı verenlere artırılmış API kredisi + erken özellik erişimi. Başvuru duyuruları Anthropic blog ve X hesabında çıkar; resmi başvuru sayfası 2026 boyunca güncellenebilir.

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

1. [Anthropic Cookbook issues](https://github.com/anthropics/claude-cookbooks/issues) listesine git.
2. Açık issue'lara bak; **documentation** / **typo** / **example improvement** türü küçük bir tane seç.
3. (Yoksa) `skills/` dizininde bir notebook oku; Türkçe çeviri veya küçük iyileştirme (comment netlik, kullanımlar güncel) olasılığı var mı?
4. Fork + clone + branch + değişiklik + commit (Conventional format) + push + PR.
5. PR açıklama şablonuna uy.
6. 2-3 gün bekle, maintainer cevap ver.

**Başarı kriteri:** 1 hafta sonunda PR açılmış, merged veya aktif review'da.

</div>

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**A → B:** Açık kaynak katkı CV'de 3. boyut (senin projelerin + işin + katkı); junior için altın. Bu yüzden **katkı fark yaratan kanıt.**</li>
<li>**B → C:** Beginner-friendly etiket aramayla başla; good-first-issue + help-wanted. Bu yüzden **düşük eşik, yüksek değer.**</li>
<li>**C → D:** Anthropic Cookbook ideal hedef — aktif, yüksek görünürlük, senin stack'in. Bu yüzden **ekosistem içi katkı double değer taşır.**</li>
<li>**D → E:** Qdrant + LangChain eş değerli; farklı ekosistem derinleşmeleri. Bu yüzden **birden fazla repo iyi.**</li>
<li>**E → F:** Commit hygiene + PR açıklama şablonu reviewer'ın hayatını kolaylaştırır, merge hızı 3×. Bu yüzden **iletişim kalitesi kod kalitesi kadar önemli.**</li>
<li>**F → G:** Code review alma refleksi: teşekkür + cevap + eylem; 24 saat yanıt. Bu yüzden **hız ve naziklik kapı açar.**</li>
<li>**G → H:** 3 ay plan — ayda 1-3 PR, 5-10 toplam hedef. Bu yüzden **plan olmadan birikim olmaz.**</li>
<li>**H → I:** GitHub profile contributions + LinkedIn featured → recruiter görünürlük. Bu yüzden **katkı görünür yapılmalı.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** Açık kaynak katkı disiplini elinde. İlk PR 1 hafta içinde atıldı, 3 ay sonra 5-10 merged PR CV'de. Sonraki (10.4): İleri konular ve trendler — sürekli öğrenme ritmi için 2026 sonrası landscape.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[10.4 İleri Konular ve Trendler →](04-ileri-konular.md)** — 2026 sonrası AI manzarası: agents at scale, on-device inference, AI safety research.

← [10.2 Mülakat Soruları](02-mulakat.md) &nbsp;|&nbsp; [Bölüm 10 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [First Contributions](https://github.com/firstcontributions/first-contributions) (adım adım eğitim, 70+ dilde Türkçe dahil) + [Open Source Guides — Katkı](https://opensource.guide/tr/how-to-contribute/) (GitHub'ın kendi rehberi, Türkçe çevirisi var) + [GitHub Skills — Communicate using Markdown](https://skills.github.com/). Üçü toplam ~3 saat, PR süreci tamamen oturur. **2026 Türkiye topluluk kaynağı:** [Türkiye Açık Kaynak Platformu](https://acikkaynak.gov.tr) — kamu kurumlarının açık kaynak projeleri burada listelenir; yerel katkı için iyi başlangıç.
</div>
