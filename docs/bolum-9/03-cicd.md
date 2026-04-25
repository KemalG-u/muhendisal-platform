# 9.3 CI/CD — GitHub Actions

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> ~40 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> 9.1 bitmiş (Dockerfile + compose yerelde çalışıyor) + 9.2 bitmiş (VPS'te servis canlıda, SSH erişimi var) + GitHub hesabı + projenin GitHub repo'su (private veya public fark etmez)</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> `main` dalına her push → **test + lint + Docker build + GHCR push + VPS'e SSH deploy** otomatik akıyor. Başarısızsa kırmızı ✗, başarıysa yeşil ✓ — GitHub'da rozet. Manuel "SSH'la gir, git pull, docker compose up" akışı **saniyelere** iniyor. Aylık maliyet: **0 €** (GitHub Actions ücretsiz 2000 dk/ay public repo için sınırsız).</div>
</div>

!!! tip "Yabancı kelime mi gördün?"
    **CI/CD** (Continuous Integration / Continuous Deployment) = her push otomatik test + deploy. **GHCR** (GitHub Container Registry) = GitHub'ın Docker Hub alternatifi, ücretsiz + rate limit yok. **Workflow** = `.github/workflows/` altında YAML tarifi. **Runner** = GitHub'ın sağladığı Ubuntu sanal makinesi (ücretsiz). **Secret** = GitHub Settings'te saklanan şifre (API key, SSH private key).

## Neden bu sayfa?

Deploy'u manuel yaparsın bir kere, iki kere — üçüncüsünde **yanlış dosyayı push etmişsindir**, ya da SSH'ı unutup iki gün eski versiyonu canlı bırakırsın. **İnsan hatası deploy'un düşmanıdır**; AI Engineer refleksi "her push otomatik akar, insan dokunmaz" demektir. GitHub Actions bu boşluğu doldurur: YAML bir dosya yazıyorsun, `main`'e her push'ta GitHub'ın sunucusu kodunu alıyor, test ediyor, Docker image build ediyor, registry'ye yüklüyor, SSH ile VPS'ine giriyor, `docker compose pull && up -d` çalıştırıyor. 3–5 dakikada, sen başka iş yaparken.

İkincisi: CI/CD **kalite kapısı** kurar. Test geçmeyen kodu production'a gönderemezsin — workflow kırmızı olur, deploy step'i çalışmaz. Pull request açıldığında workflow otomatik çalışır, ekip arkadaşın (veya kendin 2 ay sonraki sen) "testler geçiyor mu?" sorusunu tek bakışta cevaplar. AI ile kod üretirken bu özellikle kritik: Claude'un yazdığı kod lokalde çalışıyor diye canlıya uyacak diye yok — **pipeline süzgeci** yakalar.

Üçüncüsü: AI Engineer iş ilanlarında "CI/CD experience" neredeyse her pozisyonda istenir. GitHub repo'nda yeşil ✓ rozetli workflow + `.github/workflows/deploy.yml` + GHCR'de yayımlanmış image = görüşmede kanıtlanabilir deneyim. Bu sayfa seni **Yol A (test + lint minimum, 3 dk setup)** ile başlatır, sonra **Yol B (full deploy pipeline, 15 dk setup)** ile production refleksi kurar. 9.4'teki RAG Chatbot ve 9.5'teki agent otomasyon sayfaları bu pipeline'ı tekrar kullanacak — **bir kere kur, her projede kopyala**.

## Bu sayfanın ekosistemi — push'tan canlıya

<div class="ma-ekosistem" markdown>
<div class="ma-ekosistem-header">🗺️ Ekosistem — git push → otomatik deploy zinciri</div>

```mermaid
flowchart LR
    DEV["👨‍💻 Geliştirici\ngit push origin main"]
    GH["📦 GitHub repo\n.github/workflows/deploy.yml"]
    RUN["🤖 GitHub runner\nubuntu-24.04"]
    TEST["🧪 Test job\npytest + ruff + mypy"]
    BUILD["🏗 Build job\ndocker buildx multi-arch"]
    GHCR["🗄 GHCR registry\nghcr.io/user/proje:sha"]
    SSH["🔐 SSH deploy\nappleboy/ssh-action"]
    VPS["☁️ Hetzner VPS\ndocker compose pull && up -d"]
    NOT["🔔 Bildirim\nGitHub email / Slack"]

    DEV --> GH --> RUN
    RUN --> TEST
    TEST -->|geçti| BUILD
    TEST -->|kaldı| NOT
    BUILD --> GHCR
    GHCR --> SSH --> VPS
    VPS --> NOT

    classDef dev fill:#ddd6fe,stroke:#7c3aed,color:#111
    classDef gh fill:#e5e7eb,stroke:#374151,color:#111
    classDef run fill:#dbeafe,stroke:#2563eb,color:#111
    classDef test fill:#fef3c7,stroke:#ca8a04,color:#111
    classDef build fill:#fed7aa,stroke:#ea580c,color:#111
    classDef vps fill:#fef3c7,stroke:#ca8a04,color:#111
    class DEV dev
    class GH,GHCR gh
    class RUN run
    class TEST test
    class BUILD build
    class SSH,VPS vps
    class NOT dev
```

<table class="ma-aktorler" markdown>

| Düğüm | Rol | Ne iş yapıyor |
|---|---|---|
| 👨‍💻 **Geliştirici** | Sen | `git push origin main` — tetikleyici |
| 📦 **GitHub repo** | Kaynak kontrol | `.github/workflows/deploy.yml` workflow tanımı; trigger'a göre runner başlatır |
| 🤖 **Runner** | Efemeral sanal makine | Ubuntu 24.04, her iş için temiz; ücretsiz public repo, 2000 dk/ay private |
| 🧪 **Test job** | Kalite kapısı | `pytest` + `ruff` + opsiyonel `mypy`; kalırsa pipeline durur |
| 🏗 **Build job** | Image üretimi | `docker buildx` multi-arch (x86 + ARM64); layer cache kullanır |
| 🗄 **GHCR** | Container registry | `ghcr.io/kullanici/proje:sha` tag'li; Docker Hub rate limit yok |
| 🔐 **SSH deploy** | Uzak komut | `appleboy/ssh-action`; VPS'e SSH key ile girer, `docker compose pull && up -d` |
| ☁️ **VPS** | Production | Yeni image'ı çeker, eski container'ı durdurur, yenisini başlatır |
| 🔔 **Bildirim** | Geri bildirim | Workflow kırmızı/yeşil → GitHub email + repo'da rozet; Slack opsiyonel |

</table>
</div>

## Secret'lar — workflow'un şifreleri

Workflow hiçbir zaman düz metin şifre görmez. GitHub Settings → Secrets → Actions yolundan 4 secret ekleyeceksin:

| Secret adı | İçerik | Nereden |
|---|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| `VPS_HOST` | `49.13.67.89` veya `projen.alanadin.com` | Hetzner panel'den VPS IP |
| `VPS_USER` | `deploy` (9.2'deki non-root user) | 9.2'de oluşturdun |
| `SSH_PRIVATE_KEY` | `-----BEGIN OPENSSH PRIVATE KEY-----...` | Yerelden `cat ~/.ssh/deploy_key` |

!!! danger "Secret sızıntısı = API key iptal"
    Secret'ı **ASLA** `echo $SECRET` ile yazdırma — GitHub loglarda maskeler ama `base64` gibi hilelerle sızabilir. Workflow'da secret kullanan step'lerde `continue-on-error: false` tut — hata durumunda log açık kalmasın. Bir kere sızan Anthropic key'ini HEMEN console'dan iptal et, yenisini ekle. GitHub'ın secret scanning'i Anthropic key formatını otomatik yakalar ama gecikmeli.

## Yol A — Minimal CI: test + lint

İlk workflow'un her push'ta **testi koşsun + lint etsin**. Başka bir şey yapmasın. 3 dakikada kuruluyor, pipeline refleksinin temelini atıyor.

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Ruff lint
        run: ruff check .

      - name: Ruff format check
        run: ruff format --check .

      - name: Pytest
        run: pytest -q --tb=short
```

**Ne oluyor satır satır:**

- `on: push/pull_request branches: [main]` — tetikleyici. Feature branch'a push'ta çalışmaz; sadece `main`'e push veya `main`'e PR'da.
- `strategy.matrix.python-version` — 3 Python sürümünde paralel koşar. Biri kalırsa diğerleri devam eder; proje hangi sürümde kırıldığını görürsün.
- `actions/checkout@v6` — kodu runner'a indirir. v6 Node 24 tabanlı (2026 standart); v4 deprecated.
- `cache: 'pip'` — `pip`'in indirdiği paketler sonraki run'larda cache'lenir; 2 dk → 30 sn.
- `pip install -e ".[dev]"` — `pyproject.toml`'daki `[project.optional-dependencies].dev` grubunu kurar (pytest, ruff, mypy). 9.1'deki multi-stage Dockerfile ile paralel mantık.
- `ruff check .` + `ruff format --check .` — lint + format. Kod standartdan sapmışsa kırmızı.
- `pytest -q` — testler. `--tb=short` = hata çıktısı kısa, log temiz.

!!! tip "İlk push'tan önce yerelde çalıştır"
    `act` (nektos/act) Docker ile GitHub Actions'ı lokalde simüle eder. `act -j test` komutu workflow'u laptop'unda çalıştırır — push etmeden "workflow doğru mu?" doğrulamasını yaparsın. Kurulum: [github.com/nektos/act](https://github.com/nektos/act).

## Yol B — Full deploy pipeline: test → build → GHCR → SSH deploy

Minimum CI refleksini aldıktan sonra tam deploy pipeline'ına geç. 4 job, sıralı:

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:  # manuel tetikleme butonu

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false  # deploy'u iptal etme, kuyruğa al

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: ruff check . && ruff format --check .
      - run: pytest -q --tb=short

  build-and-push:
    needs: test
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Login to GHCR
        uses: docker/login-action@v4
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=sha-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-24.04
    environment: production  # GitHub'da manuel onay katmanı eklemek istersen
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1.2.5
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          script: |
            cd /home/${{ secrets.VPS_USER }}/proje
            echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
            docker compose pull
            docker compose up -d --remove-orphans
            docker image prune -f
            docker compose ps
```

**Neden 3 ayrı job?**

Her job paralel veya sıralı çalışabilir. `needs: test` diyerek build'i teste bağladık — test kalırsa build başlamaz, Docker resource'ı boşa harcanmaz. `needs: build-and-push` diyerek deploy'u build'e bağladık — image registry'de yokken deploy anlamsız. **Zincir: test → build → deploy.** Biri kırılırsa zincir durur.

**Concurrency bloğu** aynı branch'a arka arkaya 3 push atarsan 3 deploy'u aynı anda başlatmasın, kuyruğa alsın diye. `cancel-in-progress: false` = ortadakini iptal etme, sırayla tamamla (eski deploy yarıda kalsın istemezsin).

**Multi-arch build** (`linux/amd64,linux/arm64`) — Hetzner'ın CAX serisi ARM CPU; image iki mimari için de hazır olsun ki hangi VPS'te olduğun fark etmesin. Build süresi 2× artar (~3 dk) ama cache sağolsun 2. push'tan sonra 30 sn.

**Cache** (`type=gha`) — GitHub Actions'ın kendi cache'ini kullanır. Layer'lar değişmemişse yeniden build edilmez; 5 dk build → 40 sn.

**`github.sha` ile tag'leme** — her commit `ghcr.io/kullanici/proje:sha-abc1234` olarak image kaydeder. Sorun çıkarsa eski tag'a rollback yapılır. `latest` tag'i sadece `main`'den gelir.

**Deploy job'unun script'i** VPS'te çalışır: `docker login` + `docker compose pull` (yeni image'ı çek) + `up -d --remove-orphans` (eski container'ı yeniyle değiştir) + `image prune` (eski image'leri sil, disk şişmesin) + `ps` (son durumu log'la).

## Rollback stratejisi — kırılırsa geri dön

Deploy sonrası servis HTTP 500 veriyor diyelim. İki yol:

**Yol 1 — SSH manuel rollback (30 sn):**

```bash
ssh deploy@projen.alanadin.com
cd /home/deploy/proje
# compose.yml'de image: ghcr.io/.../proje:latest yerine eski sha'yı koy:
sed -i 's|proje:latest|proje:sha-bd00c9a|' compose.yml
docker compose pull
docker compose up -d
```

**Yol 2 — GitHub Actions'ta `workflow_dispatch` + eski commit:**

GitHub Actions sekmesinde "Run workflow" butonuna bas → `Use workflow from: ref` bölümüne eski commit SHA'sını gir → runner o commit'in workflow'unu koşar → eski image build edilir veya GHCR'den çekilir → VPS'e o deploy edilir.

!!! tip "Blue-green deploy orta seviye"
    Rollback'i saniyelere indiren desen: iki container aynı anda çalışır (blue + green), trafiği Caddy'de yönlendirirsin. Yeni deploy green'e gider; test geçerse blue'yu durdurursun, geçmezse green'i. Başlangıç için overkill — SHA-tag + manuel rollback yeterli. İleri seviye için [Kamal](https://kamal-deploy.org/) (37signals'ın deploy aracı) bak.

## CTO tuzakları — 10 klasik hata

| # | Tuzak | Sonuç | Doğru |
|---|---|---|---|
| 1 | Secret'ı workflow YAML'e hardcode | GitHub public repo = dünya görür; key 5 dk'da iptal | `${{ secrets.NAME }}` + GitHub Settings |
| 2 | `actions/checkout@v2` gibi eski pin | Node 16 deprecated warning, runner refuse | Yıllık v-major güncelle (`@v6`) |
| 3 | `main`'e direkt push, PR yok | Kötü kod canlıya gider; review kaybı | Branch protection: `main` locked, sadece PR |
| 4 | Test kalırken deploy çalışır | `needs:` unutuldu → kırık kod canlıda | `needs: test` zincir mecburi |
| 5 | Docker cache yok | Her build 5 dk, GHA dk kotası yanar | `cache-from/to: type=gha` |
| 6 | `latest` tag'e deploy, rollback yok | Eski versiyonu geri alamazsın | SHA tag + rollback prosedürü |
| 7 | Aynı anda 3 deploy | Race condition, container bozuk | `concurrency:` bloğu |
| 8 | SSH password auth | Brute force saldırı yüzeyi | Sadece SSH key (9.2'de kurdun) |
| 9 | `docker compose up` (down yok) | Eski volume'lar sızar, config eski | `up -d --remove-orphans` |
| 10 | Deploy sonrası `docker image prune` yok | VPS diski 2 ayda dolar | Her deploy sonunda `prune -f` |

Bonus tuzak 11: **Flaky test**. Test bazen geçer bazen kalır — `retry` koyma, **sebebini bul**. Genelde race condition, external API, veya time.sleep yüzünden. Flaky test CI/CD'yi zehirler — 5. kırmızıda kimse bakmaz, 10.'da gerçek hata kaçar.

## Anthropic ekosistemi — Claude ile CI/CD

<details class="ma-anthropic-oz" markdown>
<summary><strong>🤖 Anthropic-öz: Claude Code ile workflow yazımı</strong></summary>

Anthropic Claude Code bu pipeline'ın **yazıcısı olur** — YAML'i el ile yazmazsın. Terminal'de:

```bash
claude "Bu projeye GitHub Actions ekle: push'ta pytest + ruff, main'de ghcr'e build, VPS'e SSH deploy. Secrets: ANTHROPIC_API_KEY, VPS_HOST, VPS_USER, SSH_PRIVATE_KEY."
```

Claude Code dosya sistemini okur (`pyproject.toml`, `compose.yml`, `Dockerfile`), uygun workflow'u `.github/workflows/deploy.yml` olarak yazar. `claude --allowedTools "str_replace_editor"` ile düzenleme iznini dar tutarsın.

**Budget alertleri kurulumu** (CI/CD ile paralel refleks):

- [Anthropic Console → Billing → Usage alerts](https://console.anthropic.com/settings/billing) aylık limit + threshold
- Workflow içinde `ANTHROPIC_API_KEY`'i sadece integration test step'inde kullan; build step'inde verme → kaza ile cost sıçraması önlenir
- `pytest -m "not integration"` default, `pytest -m integration` sadece `workflow_dispatch` manuel tetik

**Referans:** Anthropic [Claude Code docs](https://platform.claude.com/docs/en/claude-code/overview) + [API error & rate limit handling](https://platform.claude.com/docs/en/api/errors).

</details>

## Çıktı kanıtları — 3 kanıt

<div class="ma-cikti-kaniti" markdown>
<div class="ma-cikti-kaniti-header">📏 Çıktı — 3 kanıt</div>

**1. Workflow yeşil ✓** — GitHub'da `Actions` sekmesi → son commit'te üç job da yeşil tick:

```
✓ test           (1m 24s)
✓ build-and-push (3m 12s)
✓ deploy         (38s)
Total: 5m 14s
```

**2. GHCR'de image yayımlanmış:**

```bash
docker pull ghcr.io/<kullanici>/<proje>:latest
# Status: Downloaded newer image for ghcr.io/.../proje:latest
docker images | grep proje
# ghcr.io/.../proje   latest   abc123def456   2 minutes ago   180MB
```

**3. Canlıda yeni versiyon:**

```bash
curl -I https://projen.alanadin.com/version
# HTTP/2 200
# x-git-sha: bd00c9a   <- son commit SHA'sı, app kodunda env'den okunur
```

**Kanıt dosyası:** `muhendisal-notlarim/bolum-9/03-cicd/workflow-runs.md` — her deploy'un SHA + süre + sonuç kaydı.

</div>

## Görev — kendi pipeline'ını kur

<div class="ma-gorev" markdown>
<div class="ma-gorev-header">🎯 Görev — test yap, deploy yap, rollback dene</div>

Mevcut projene (9.1 + 9.2 tamamsa referans proje `icerik-ozet-agent` veya kendi repon) CI/CD ekle:

1. `.github/workflows/ci.yml` — **Yol A minimum**; push → pytest + ruff. Yeşil olana kadar düzelt.
2. `.github/workflows/deploy.yml` — **Yol B full**; test + build + GHCR + SSH deploy.
3. 4 secret'ı GitHub Settings'e ekle: `ANTHROPIC_API_KEY`, `VPS_HOST`, `VPS_USER`, `SSH_PRIVATE_KEY`.
4. `main`'e küçük bir değişiklik push et (README'ye satır ekle) → 3 job'un yeşil olduğunu gözle.
5. **Rollback tatbikatı:** kasıtlı bir bug push et → kırmızı olduğunu gör → eski SHA'ya `workflow_dispatch` ile geri dön.
6. Branch protection aç: Settings → Branches → `main` → "Require pull request before merging" + "Require status checks to pass".

Kanıt: 3 workflow run ekran görüntüsü (yeşil, kırmızı, rollback-yeşil) + `curl -I https://...` 200 + GHCR image URL.

Dosyaya kaydet: `muhendisal-notlarim/bolum-9/03-cicd/kanit/`

</div>

## Yol A mı Yol B mi? — karar matrisi

| Durum | Tercih | Gerekçe |
|---|---|---|
| İlk hobby proje, VPS yok | **Yol A** | Test refleksi yeter; deploy manuel olsun |
| Solo MVP, VPS var, haftada 1-2 push | **Yol B** | 15 dk setup, aylar boyu tasarruf |
| Ekip projesi, birden çok branch | **Yol B + environments** | `environment: production` manuel onay katmanı ekler |
| Zamanlanmış cron job (agent) | **Yol B** | 9.5 agent otomasyon bu yola ihtiyaç duyar |
| Tam otomasyona güven yok | **Yol A → Yol B kademeli** | Önce test'e güven, sonra deploy otomasyonuna |

!!! warning "Yol B'ye atlamadan önce Yol A'yı çalıştır"
    Test yeşil olmadan deploy otomasyonu = kırık kodu saniyelerde canlıya yollamak. **Önce pipeline'a güven kur.** Haftalarca sadece CI (Yol A) çalıştır; testin gerçekten kırılmaları yakaladığını gör. Sonra CD (Yol B) ekle.

<div class="ma-neden-sonuc" markdown>
<div class="ma-neden-sonuc-header">🔗 Birlikte okuma — neden ne oldu</div>

<ol class="ma-neden-sonuc-zincir" markdown>
<li>**A → B:** Manuel deploy insan hatasına açık — otomasyon kalite kapısı kurar; test geçmeyen kod canlıya çıkmaz. Bu yüzden **CI/CD kalite garantisi.**</li>
<li>**B → C:** GitHub Actions = YAML + runner; ücretsiz (public repo sınırsız, private 2000 dk/ay) + native entegrasyon. Bu yüzden **GHA başlangıç için ideal.**</li>
<li>**C → D:** 4 secret (`ANTHROPIC_API_KEY`, `VPS_HOST`, `VPS_USER`, `SSH_PRIVATE_KEY`) Settings'te saklanır; YAML'da `${{ secrets.X }}` referansı. Bu yüzden **secret YAML'a asla girmez.**</li>
<li>**D → E:** Yol A (test+lint) 3 dk setup; pipeline refleksinin temeli. Yol B (full deploy) Yol A'nın üstüne inşa edilir. Bu yüzden **adım adım kur, karmaşıklık ekle.**</li>
<li>**E → F:** `test → build → deploy` zinciri `needs:` ile bağlanır; biri kırılırsa zincir durur. Zero-downtime için `concurrency:` + multi-arch build + GHA cache. Bu yüzden **bağımlılık zinciri güvenlik kapısı.**</li>
<li>**F → G:** Her commit SHA-tag ile GHCR'de saklanır — rollback SHA'yı değiştirmek kadar kolay. `latest` sadece `main`'den gelir. Bu yüzden **tag disiplini rollback'i kolaylaştırır.**</li>
<li>**G → H:** 10 klasik tuzak (secret leak, flaky test, cache bozulması, direkt push) çözüldüğünde pipeline production'da 6+ ay sorunsuz akar. Bu yüzden **tuzaklar önceden öğrenilir.**</li>
</ol>

<div class="ma-neden-sonuc-sonuc" markdown>
**Sonuç:** `main`'e her push → 5 dakika sonra canlıda. Test kalırsa kırmızı, sebep log'da. Rollback SHA-tag ile 30 saniye. Ay sonu faturası **0 €** (GHA ücretsiz). AI Engineer refleksi kuruldu — 9.4 RAG Chatbot ve 9.5 agent otomasyon bu pipeline'ı kopyalayıp kullanacak.
</div>
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[9.4 Portföy Projesi 1 — RAG Chatbot →](04-proje-1.md)** — PDF yükle, soru sor, Claude kaynak göstererek cevap versin. 9.1 + 9.2 + 9.3'ün birleşimi canlıya.

← [9.2 Cloud Deploy](02-cloud.md) &nbsp;|&nbsp; [Bölüm 9 girişi](index.md) &nbsp;|&nbsp; [Ana sayfa](../index.md)

**Pekiştirme:** [GitHub Actions resmi docs](https://docs.github.com/en/actions) (workflow syntax, contexts) + [docker/build-push-action README](https://github.com/docker/build-push-action) (cache stratejileri) + [appleboy/ssh-action README](https://github.com/appleboy/ssh-action) (advanced SSH options) üçlüsünü oku. CI/CD refleksi bu üç kaynağın kesişiminde olgunlaşır.
</div>
