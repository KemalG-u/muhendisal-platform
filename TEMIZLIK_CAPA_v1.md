# ÇAPA — MühendisAl Kapsamlı Temizlik & Profesyonelleştirme

**Tarih:** 25 Nisan 2026
**Hedef:** Kimlik krizini çöz, güvenlik açığını kapat, UX'i profesyonel hale getir, performansı iyileştir, SEO/paylaşım ekle.
**Kapsam:** 38 madde, 10 kategori. Tek seansta otonom yapılacak.
**Pilot referans:** Anthropic Docs (https://docs.claude.com), Stripe Docs (görsel disiplin).

## KURAL 0 — ONAY YASAK

- Hiçbir adımda Kemal'e sorma
- `bypassPermissions` zaten aktif (`.claude/settings.json`)
- Tıkanırsan: 1 retry → workaround → devam → sona rapor
- Subagent KULLANMA, tek operatör

## KURAL 1 — KANIT-ÖNCE-İDDİA

Her aşama sonu:
1. `./scripts/rebuild.sh` → 0 warning
2. Lokal test (curl) → beklenen sonuç
3. Commit
4. Sonra ileri

## AŞAMA 0 — Hazırlık (5 dk)

```bash
cd /root/muhendisal-platform
git status                    # temiz olmalı
git log --oneline -3          # son commit görünür
ls .claude/settings.json      # bypass açık
pm2 list | grep muhendisal-api  # online
```

İlk mesaj: "Aşama 0 tamam. 10 aşama × 38 madde başlıyorum."

---

## AŞAMA 1 — GÜVENLİK ACİL (15 dk) — A KATEGORI

### 1.1 — `nick="Kemal"` default kaldır

`backend/routes/auth.py:39`:

```python
# YANLIŞ:
user = models.User(token=payload.token, nick=payload.nick or "Kemal")

# DOĞRU:
user = models.User(token=payload.token, nick=payload.nick or "Misafir")
```

`models.py` ve `schemas.py` `nick` alanına min/max length 1-30 ekle (Pydantic validator).

### 1.2 — Rate limit sıkılaştır

`backend/routes/auth.py:26`:

```python
# YANLIŞ: @limiter.limit("5/minute")
# DOĞRU:
@limiter.limit("3/hour;10/day")
```

Diğer endpoint'ler (`/feedback`, `/quiz/attempt`, `/seen`, `/complete`) makul (3/dk - 30/dk arası), Kemal kullanırken sıkıştırmasın.

### 1.3 — Token format validation

`backend/schemas.py` `UserInit`:

```python
class UserInit(BaseModel):
    token: str = Field(..., min_length=8, max_length=64, pattern=r'^[a-zA-Z0-9-]+$')
    nick: Optional[str] = Field(None, max_length=30, pattern=r'^[\w\s.\-_]+$')
```

### 1.4 — Audit log

`backend/main.py` middleware ekle: tüm `POST /api/*` istekleri `data.db.api_log` tablosuna yaz (timestamp, ip, endpoint, status). Tablo yoksa oluştur.

### 1.5 — pm2 restart + test

```bash
pm2 restart muhendisal-api
sleep 2
# 4 hızlı istek (3 başarılı, 4. = 429)
for i in 1 2 3 4 5; do
  curl -s https://wiki.oluk.org/platform/api/auth/init \
    -X POST -H "Content-Type: application/json" \
    -d "{\"token\":\"sec-test-$(uuidgen)\"}" -w " HTTP=%{http_code}\n" | tail -1
done
# Beklenen: 1-3 başarı, 4-5 = 429
```

**Commit:** `fix(security): nick default + rate limit + validation + audit log`

---

## AŞAMA 2 — KİMLİK & VAAT TEMİZLİĞİ (20 dk) — A KATEGORI

### 2.1 — Ana sayfa yeniden yaz

`docs/index.md` baştan yaz. **Yeni vaat:**

- "75+ sayfada AI Engineer'ın günlük işini öğretir" (kesin sayı yok, "75+")
- "Sonunda canlı bir mini-proje + LinkedIn paylaşımına hazır portföy"
- "Bölüm 10 ayrıca kariyer ipuçları içerir (mülakat, LinkedIn, maaş bantları)"
- Süre vaadi: "**3-4 ay** akşam 30 dk/gün ritminde" (4-6 hafta yalanı düzelt)

### 2.2 — Fine-tune çelişki düzelt

Ana sayfa "Ne yapmaz" listesinden "fine-tune etmez" satırını **kaldır**. Yerine:

> "5. Bölüm fine-tune'a giriş seviyesinde bir QLoRA pratiği içerir; üretim seviyesi için Anthropic Academy'ye yönlendirir."

### 2.3 — Sayfa sayısını otomatik tut

`mkdocs.yml`'a hook ekle veya basit: build script'te `find docs -name '*.md' | wc -l` sonucu README'ye yaz. Manuel "64 sayfa" yerine.

### 2.4 — `/hakkimda` sayfası ekle

`docs/hakkimda.md`:
- Kemal kim (teknik kurucu, akşamları builder, tax office müdür yardımcısı **gizle** — sadece "Türkiye'de kamu sektöründe çalışan" de)
- Neden yazdı (Türkçe AI öğrenme açığı + kendi öğrenme yolu)
- Diğer projeler: HBV, KarıncaAI, ClawdBot
- İletişim: hatay61@gmail.com, X @KarincaAI

`mkdocs.yml` nav'a ekle: "Hakkımda" en sağda.

**Commit:** `docs(identity): ana sayfa vaat-teslimat tutarlilik + hakkimda sayfasi`

---

## AŞAMA 3 — UI GÖRSEL TEMİZLİK (30 dk) — C KATEGORI

### 3.1 — XP rozeti üst sağdan kaldır

`docs/assets/js/progress.js` içinde "ma-badge" oluşturan kısım — DOM'a sadece `/dashboard/` URL'sinde inject et:

```javascript
if (location.pathname.includes('/dashboard/')) {
  // mevcut badge kodu
}
```

### 3.2 — "Yazım Kuralları (CTO)" üst nav'dan kaldır

`mkdocs.yml` nav listesinden sil. Dosyayı `CONTRIBUTING.md`'ye taşı (repo root). Site nav temizlenir.

### 3.3 — Üst nav'ı daralt

`mkdocs.yml` nav:
- Ana Sayfa
- Bölümler (dropdown — Bölüm 0-10 hepsi alt menü)
- Dashboard
- Hakkımda

Mevcut "Bölüm 0", "Bölüm 1", ... "Bölüm 10" tek tek tab değil, **dropdown altında**.

### 3.4 — Renk paleti yumuşat

`mkdocs.yml`:
```yaml
palette:
  - media: "(prefers-color-scheme: light)"
    scheme: default
    primary: custom       # özel renk: #D97757 (Anthropic koyu turuncu yumuşak)
    accent: custom
```

`docs/assets/custom.css` üst:
```css
:root {
  --md-primary-fg-color: #D97757;
  --md-primary-fg-color--light: #E89272;
  --md-primary-fg-color--dark: #B85B3F;
  --md-accent-fg-color: #D97757;
}
```

### 3.5 — Persona kutusu yeniden tasarım

`.ma-meta` CSS'i 4 ayrı satıra böl, her birinde ikon:

```html
<div class="ma-meta">
  <div class="ma-meta-row"><span class="ma-icon">👤</span> <strong>Kim:</strong> ...</div>
  <div class="ma-meta-row"><span class="ma-icon">⏱️</span> <strong>Süre:</strong> ~30 dk</div>
  <div class="ma-meta-row"><span class="ma-icon">📋</span> <strong>Önkoşul:</strong> ...</div>
  <div class="ma-meta-row"><span class="ma-icon">🎯</span> <strong>Çıktı:</strong> ...</div>
</div>
```

CSS: 4 satır flex layout, satır arası 8px boşluk, ikon 20px.

**Otomatik dönüşüm scripti:** `scripts/persona-kutu-format.py` yaz, tüm `docs/bolum-*/*.md` üstündeki `ma-meta` bloklarını 4 satır formatına çevir. Mevcut tek satır içeriği `· Süre · Önkoşul · Çıktı` ayraçlarından böl.

**Commit:** `style(ui): xp badge sadece dashboard, nav daraltma, anthropic renk paleti, persona kutusu 4 satir`

---

## AŞAMA 4 — NAVİGASYON (15 dk) — D KATEGORI

### 4.1 — Sayfa altı "Sonraki / Önceki"

`mkdocs.yml`:
```yaml
theme:
  features:
    - navigation.footer    # ZATEN VAR — kontrol et
```

Eğer `navigation.footer` zaten varsa Material kendisi sayfa altı önceki/sonraki linkleri ekler. Test et: `wiki.oluk.org/platform/bolum-1/01-ai-engineer/` altında "Önceki: ... | Sonraki: ..." görünüyor mu?

### 4.2 — Sol sidebar bölümler arası

`mkdocs.yml`:
```yaml
features:
  - navigation.sections     # ZATEN VAR
  - navigation.indexes      # ZATEN VAR
  # Eklenecek:
  - navigation.expand       # bölümler genişlemiş başlasın
```

`navigation.expand` zaten var → sol sidebar tüm bölümleri göstermeli. Görmüyorsa CSS override var demektir.

### 4.3 — Breadcrumb iyileştir

Material default breadcrumb `Ana Sayfa > Bölüm 1 > 1.1 AI Engineer Nedir`. Şu an `Ana Sayfa > Bölüm 1 — Giriş ve Temeller` görünüyor (alt sayfa kayıp). Sayfa içindeki başlık eşleşmesi.

**Commit:** `nav(footer-breadcrumb): sayfa alti onceki-sonraki ve breadcrumb iyilestirme`

---

## AŞAMA 5 — PERFORMANS (20 dk) — E KATEGORI

### 5.1 — JS dosyalarını sayfa-spesifik yükle

`mkdocs.yml`'dan `extra_javascript:` listesini sil. Yerine **tek bir loader** ekle: `docs/assets/js/loader.js`:

```javascript
(function() {
  var path = location.pathname;
  function load(src) {
    var s = document.createElement('script');
    s.src = src;
    s.defer = true;
    document.body.appendChild(s);
  }
  // Her sayfa: api-client + progress (XP toplama için her sayfada)
  load('/platform/assets/js/api-client.js');
  load('/platform/assets/js/progress.js');
  // Sayfa-spesifik:
  if (path.includes('/dashboard/')) load('/platform/assets/js/dashboard.js');
  if (path.includes('/quiz') || document.querySelector('.ma-quiz')) load('/platform/assets/js/quiz.js');
  if (document.querySelector('.ma-code-editor')) load('/platform/assets/js/code-editor.js');
  if (path.endsWith('/ekosistem/') || path.includes('bolum-1/03')) load('/platform/assets/js/ekosistem.js');
  load('/platform/assets/js/app.js');
})();
```

`mkdocs.yml`:
```yaml
extra_javascript:
  - assets/js/loader.js
```

### 5.2 — Build & test

```bash
./scripts/rebuild.sh
# Yeni HTML kontrol:
grep -c "<script" site/bolum-1/01-ai-engineer/index.html
# Beklenen: 3-4 (loader + Material bundle + glightbox)
```

**Commit:** `perf(js): 9 dosyadan 2 dosyaya, sayfa-spesifik lazy load`

---

## AŞAMA 6 — SEO & PAYLAŞIM (25 dk) — F KATEGORI

### 6.1 — MkDocs Material plugin: `meta` + `social`

`mkdocs.yml`:
```yaml
plugins:
  - search
  - meta                    # her sayfa meta override
  - social:                 # otomatik og:image üretici
      cards: true
      cards_layout_options:
        background_color: "#D97757"
        color: "#FFFFFF"
        font_family: Inter
```

`pip install pillow cairosvg` (social plugin için).

### 6.2 — Default og: meta her sayfaya

`mkdocs.yml`:
```yaml
extra:
  social:
    - icon: fontawesome/brands/x-twitter
      link: https://x.com/KarincaAI
    - icon: fontawesome/brands/github
      link: https://github.com/KemalG-u/muhendisal-platform
```

`overrides/main.html` oluştur (mkdocs-material override):
```html
{% extends "base.html" %}
{% block extrahead %}
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ page.title }} — MühendisAl">
  <meta property="og:description" content="{{ page.meta.description if page.meta.description else config.site_description }}">
  <meta property="og:image" content="{{ page.canonical_url }}image.png">
  <meta property="og:url" content="{{ page.canonical_url }}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@KarincaAI">
{% endblock %}
```

`mkdocs.yml`:
```yaml
theme:
  custom_dir: overrides
```

### 6.3 — JSON-LD structured data

Aynı `overrides/main.html`'de:
```html
{% if page.meta and page.meta.type == 'article' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{{ page.title }}",
  "author": {"@type": "Person", "name": "Kemal", "url": "https://wiki.oluk.org/platform/hakkimda/"},
  "publisher": {"@type": "Organization", "name": "MühendisAl"}
}
</script>
{% endif %}
```

**Commit:** `seo(meta): og + twitter card + json-ld structured data + social plugin`

---

## AŞAMA 7 — XP/GAMIFICATION ELDEN GEÇIRME (10 dk) — I KATEGORI

### 7.1 — XP rozeti default kapalı

`progress.js` üst:
```javascript
var SHOW_BADGE = localStorage.getItem('ma_show_badge') === '1';
if (!SHOW_BADGE && !location.pathname.includes('/dashboard/')) return;
```

Dashboard'da bir toggle: "İlerleme rozetini her sayfada göster" — tıklayınca `localStorage.setItem('ma_show_badge','1')`.

### 7.2 — "Bu sayfayı tamamladım" butonu opsiyonel

Default kapalı, dashboard'da toggle ile aç.

**Commit:** `feat(xp): rozet ve tamamlandim butonu default kapali, dashboard toggle`

---

## AŞAMA 8 — İÇERİK SADELEŞTİRME (60 dk) — G KATEGORI

**ÖNEMLİ:** Bu aşama içerik silmek değil, **özetlemek + yeniden organize etmek**. Bu seansta SADECE 5 örnek sayfa yap (pilot), gerisi sonraki seans.

### 8.1 — Pilot sayfalar seç

- `bolum-0/index.md` — bölüm girişi formatı pilot
- `bolum-1/01-ai-engineer.md` — sayfa formatı pilot
- `bolum-2/01-llm-temelleri.md` — referans (zaten pilot)
- `bolum-9/04-proje-1.md` — proje sayfa formatı pilot
- `bolum-10/01-linkedin.md` — kariyer sayfa formatı pilot

### 8.2 — Sayfa baş 2-cümlelik TL;DR

Her sayfanın `# Başlık` satırından sonra:

```markdown
> **TL;DR:** [Tek cümle ne öğreniyorsun] · [Tek cümle elinde ne olacak]
```

Persona kutusu hemen onun altında.

### 8.3 — "Neden bu bölüm" 1 paragrafa indir

Mevcut 3 paragraf "Neden bu bölüm" → 4-6 cümlelik tek paragraf. **Korunacak:** ana mesaj. **Atılacak:** 2. ve 3. paragraf detayları (zaten alt başlıklarda var).

### 8.4 — Pilot sayfaları yeniden yaz

5 pilot sayfayı bu disiplinle yeniden yaz. Her birinde:
- TL;DR satırı
- 4-satır persona kutusu
- 1 paragraf "Neden bu sayfa"
- Geri kalan içerik aynen
- Footer "Sonraki sayfa →" linki

**Commit:** `content(pilot): 5 sayfada TL;DR + 4-satir persona + 1-paragraf giris`

---

## AŞAMA 9 — KİMLİK / HAKKIMDA + TOPLULUK (10 dk) — H, J KATEGORI

### 9.1 — `/hakkimda` sayfası (zaten 2.4'te yapıldı, kontrol)

### 9.2 — Footer'a sosyal bağlantı

`mkdocs.yml`:
```yaml
extra:
  social:
    - icon: fontawesome/brands/x-twitter
      link: https://x.com/KarincaAI
      name: KarıncaAI
    - icon: fontawesome/brands/github
      link: https://github.com/KemalG-u/muhendisal-platform
      name: GitHub repo
    - icon: fontawesome/brands/linkedin
      link: https://www.linkedin.com/in/kemal-...    # Kemal'in LinkedIn'i
      name: LinkedIn
```

### 9.3 — RSS feed

`mkdocs.yml`:
```yaml
plugins:
  - rss:
      match_path: bolum-.*
      date_from_meta:
        as_creation: date
```

`pip install mkdocs-rss-plugin`.

**Commit:** `feat(community): footer sosyal baglantilar + RSS feed + hakkimda`

---

## AŞAMA 10 — FINAL: BUILD + PUSH + RAPOR (15 dk)

### 10.1 — Tam build + smoke test

```bash
./scripts/rebuild.sh 2>&1 | tail -20    # 0 warning beklenen
curl -s https://wiki.oluk.org/platform/ -o /tmp/idx.html -w "boyut=%{size_download} sure=%{time_total}\n"
# Beklenen: boyut <60KB, süre <0.5sn

# og:image kontrol
curl -s https://wiki.oluk.org/platform/bolum-1/ | grep -c 'og:'
# Beklenen: 5+

# JS sayısı kontrol
curl -s https://wiki.oluk.org/platform/bolum-1/ | grep -c '<script'
# Beklenen: 3-4 (loader + bundle + glightbox)

# Güvenlik test
for i in 1 2 3 4; do
  curl -s https://wiki.oluk.org/platform/api/auth/init -X POST \
    -H "Content-Type: application/json" \
    -d "{\"token\":\"final-test-$(uuidgen)\",\"nick\":\"TestUser\"}" \
    -w " HTTP=%{http_code} nick=" | grep -oE '"nick":"[^"]+"'
  echo
done
# Beklenen: ilk 3 başarı (nick=TestUser), 4. = 429
```

### 10.2 — Final commit + push

```bash
git commit --allow-empty -m "docs(temizlik-v1): kapsamli profesyonelleştirme tamamlandi

- Kimlik krizi cozuldu (vaat-teslimat tutarli)
- Guvenlik aciklari kapatildi (nick default, rate limit siki, audit log)
- UI profesyonel (anthropic palette, nav daralti, persona kutusu 4 satir)
- Performans (9 JS -> 2, sayfa-spesifik lazy load)
- SEO (og:image, twitter card, json-ld, RSS)
- 5 pilot sayfa TL;DR + sade format

CTO eleştirisi v1: 38 madde, 10 kategori, hepsi iş bitti."

GH=\$(grep -oP '(?<=GITHUB_TOKEN=)\S+' /root/radar/.env | head -1)
git push "https://KemalG-u:\${GH}@github.com/KemalG-u/muhendisal-platform.git" main
```

### 10.3 — Brain raporu

`brain_write` ile `projects/muhendisal/audits/temizlik-v1-final`:
- 10 aşama × 38 madde sonuçları
- Her aşamadan sonra commit SHA
- Build/test/güvenlik kontrolü kanıtları
- Skor: önceki 9.95 → yeni X (gerçekçi)
- Sonraki seansa not: kalan içerik sadeleştirme (Aşama 8 sadece 5 sayfa pilot, 73 sayfa daha)

### 10.4 — Kemal'e final rapor (tek mesaj)

```
Temizlik v1 bitti.
- Aşama: 10/10
- Madde: 38/38 (içerik sadeleştirme 5 pilot sayfa, 73 sayfa kaldı)
- Commit: M
- GitHub push: ✓
- Build: 0 warning
- Güvenlik test: nick=TestUser ✓, rate limit 3/hour ✓
- Site canlı: https://wiki.oluk.org/platform/
- Skor: önceki 9.95 → şimdi X
```

---

## TIKANIRSAN — KARAR AĞACI

| Tıkanma | Karar |
|---|---|
| `pip install` paket bulunamadı | Alternatif paket dene; bulunamazsa o aşamayı atla, raporda "atlanmış" yaz |
| `social` plugin Pillow eksik | `pip install pillow cairosvg` retry; başarısızsa bu plugin'i atla, manuel `og:image` (statik tek görsel) ekle |
| `pm2 restart` başarısız | `pm2 logs muhendisal-api` 20 satır oku, hatayı raporla, eski sürüme `git checkout HEAD~1 -- backend/` ile dön |
| Build warning verirse | Warning'i oku, kaynağını düzelt, tekrar build. 3 deneme sonrası warning ile commit |
| GitHub push başarısız | Manuel push komutunu mesaja yaz, Kemal'e bildir |
| Pilot sayfa yeniden yazımı çok sürdü (45+ dk) | İlk 2 sayfa yapıldıysa kabul et, 3-5 sonraki seansa bırak |

---

## BİTİRME KRİTERİ

- [ ] Aşama 1 (güvenlik) %100 — bu kritik
- [ ] Aşama 2 (kimlik vaat) %100
- [ ] Aşama 3 (UI) %100
- [ ] Aşama 4 (nav) %100
- [ ] Aşama 5 (perf) %100
- [ ] Aşama 6 (SEO) en az og:image + twitter card
- [ ] Aşama 7 (XP) %100
- [ ] Aşama 8 (içerik) en az 2 pilot sayfa
- [ ] Aşama 9 (topluluk) en az footer sosyal
- [ ] Aşama 10 (push + rapor) %100

Tam yapılamayan aşamalar **brain raporuna** yazılır, sonraki seansta tamamlanır.

---

## BAŞLATMA

1. Aşama 0 (5 dk)
2. Tek mesaj Kemal'e: "Temizlik başladı, 10 aşama × 38 madde, otonom ilerliyorum, bitince final rapor."
3. Aşama 1 → 10 sırayla
4. Bitince final rapor (tek mesaj)

**Bu çapa anayasan. Soru sormak yasak. Yapmak zorunlu. 38 madde × 10 aşama × ~3 saat.**
