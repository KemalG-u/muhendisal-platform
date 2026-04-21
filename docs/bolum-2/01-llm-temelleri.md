# 2.1 LLM Nedir — ve İlk Claude Çağrın

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>⏱️ Süre:</strong> 45 dakika</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> Yok (Bölüm 0 kurulumu yapılmadıysa zararı olmaz — Claude Console kısmı tarayıcıda çalışır)</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Claude'a ilk mesajını gönderip yanıtı alırsın; LLM'in yanıtı nasıl ürettiğini kendi cümlelerinle özetleyebilirsin.</div>
</div>

## Neden bu sayfa?

Bu rehberdeki tüm bölümler tek bir temele oturuyor: **Claude'a nasıl konuşulur**. RAG, agent, MCP, prompt teknikleri — hepsi bu temelin üzerine eklenen katmanlar. Bu sayfayı bitirdiğinde elinde ilk çalışan API çağrın olacak. Bundan sonra her şey bu çağrının genişlemiş bir hâli.

İki engel var ve her ikisini de burada aşıyoruz: (1) "LLM nasıl çalışır" sorusu — 3 paragrafta ve matematiksiz; (2) ilk çağrıyı gerçekten yapmak — Console'da 2 dakika, Python'da 5 dakika.

## LLM kısaca — üç paragraf

LLM (Large Language Model, büyük dil modeli) internet ölçeğinde metin üzerine eğitilmiş bir olasılık tahmincisidir. Sana bir cümle verdiğinde yaptığı iş tek şey: **bir sonraki kelimeyi (daha doğrusu token'ı) tahmin etmek**. Bunu tekrar tekrar yapar — her yeni token önceki token'lara bakarak üretilir. "Cevap" dediğimiz şey bu zincirin gözle görünür hâli.

Token kelimenin yaklaşık %75'ine denk gelen bir parça. "İstanbul" tek token olabilir, "kahvaltılık" iki parçaya bölünebilir. Claude API'ye mesaj gönderdiğinde hem gönderdiğin hem de aldığın metin token cinsinden ölçülür — ücretlendirme de buradan.

Bir LLM "düşünmez" klasik anlamda, ama eğitim sırasında gördüğü milyarlarca örüntüden yararlanarak çoğu zaman şaşırtıcı doğru tahminler yapar. Hatalı çıktı (hallucination) bu mekaniğin doğal sonucu: model, emin olmadığı durumda bile bir sonraki token'ı üretmek zorundadır. İyi prompt mühendisliğinin büyük kısmı modeli "emin olmadığını söyleyebileceği" bir çerçeveye oturtmaktır.

??? info "Daha derine inmek istiyorsan (opsiyonel, EN)"
    - [Transformer makalesi (Attention Is All You Need, 2017)](https://arxiv.org/abs/1706.03762) — mimarinin orijinal kaynağı
    - [3Blue1Brown — But what is a GPT?](https://www.youtube.com/watch?v=wjZofJX0v4M) — görsel sezgi, 30 dk
    - Bu platformun odağı proje bitirmek. Matematik olmadan da yola devam edebilirsin.

## Uygulama — iki yol

Seçeneklerden birini yeterli say. İstersen ikisini de yap.

### Yol 1 — Claude Console (kod yazmadan, 2 dakika)

🔵 **İş personası için önerilen başlangıç.** Tarayıcı açıp Claude'u yerinde görmek.

1. [console.anthropic.com](https://console.anthropic.com) adresine git, hesap aç (Google ile giriş yeterli).
2. Sol menüden **Workbench**'e gir.
3. Model olarak "Claude Sonnet 4.6" seç (ücretsiz krediyle deneme için yeterli).
4. "User" alanına şunu yaz:
   ```
   Selam Claude. Sen bir Türkçe konuşan AI asistansın. Bana 3 cümleyle, matematik kullanmadan, bir LLM'in bir sonraki kelimeyi nasıl tahmin ettiğini anlat.
   ```
5. **Run** düğmesine bas. Yanıtı ekranda gör.
6. Ekran görüntüsü al.

### Yol 2 — Python SDK ile ilk API çağrın (5 dakika)

🟢 🟣 **Başlangıç ve kişisel persona için.** Terminal/Colab ortamında.

**Adım 1 — API key al:**

- Console'da sağ üstteki profil → **API Keys** → **Create Key** → adını "muhendisal-deneme" koy → oluştur.
- Key'i kopyala, güvenli bir yere kaydet. **Key'i bir daha göremezsin, sıfırdan oluşturman gerekir.**

**Adım 2 — Paketi kur:**

```bash
pip install anthropic
```

**Adım 3 — İlk çağrı:**

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

yanit = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": (
                "Selam Claude. Sen Türkçe konuşan bir AI asistansın. "
                "Bana 3 cümleyle, matematik kullanmadan, bir LLM'in "
                "bir sonraki kelimeyi nasıl tahmin ettiğini anlat."
            ),
        }
    ],
)

print(yanit.content[0].text)
print("---")
print("Girdi token:", yanit.usage.input_tokens)
print("Çıktı token:", yanit.usage.output_tokens)
```

Çalıştırmadan önce terminalde:

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-...senin-key'in..."
python ilk_cagri.py
```

Beklenen çıktı — 3 cümlelik bir açıklama, ardından token sayıları. Tam metin Claude'a göre değişir; önemli olan bir yanıtın gelmesi.

??? tip "Hata aldıysan"
    - `AuthenticationError`: API key doğru export edilmemiş. `echo $ANTHROPIC_API_KEY` ile kontrol et, sonuç boşsa tekrar `export` et.
    - `model_not_found`: model adı değişmiş olabilir. [docs.claude.com/en/docs/about-claude/models](https://docs.claude.com/en/docs/about-claude/models) adresinden güncel model adını al.
    - `rate_limit`: ücretsiz krediyi bitirdin. 1 dakika bekle.

<div class="ma-cikti-kaniti" markdown>
### 📦 Çıktı Kanıtı — bu sayfayı bitirdiğini nasıl kanıtlarsın

**Seçeneklerden birini yap:**

1. **Screenshot:** Console Workbench veya terminal çıktısının ekran görüntüsü.
2. **GitHub Gist:** `ilk_cagri.py` dosyanı anonim bir [Gist](https://gist.github.com) olarak yayınla (API key'i **çıkararak**).
3. **1 paragraf refleksiyon:** "LLM'in yanıtı nasıl ürettiğini" kendi cümlelerinle yaz (3-5 cümle).

**Teslim:** [Geri bildirim formu](/platform/#geri-bildirim) — `Tür: proje_teslim` seç, linki veya metni paylaş.

**Neden bu önemli:** Kitap okumak değil, _yapmış olmak_ saymıyor olman için. Bundan sonraki her sayfa bu çağrının üzerine ekleme yapıyor.
</div>

<div class="ma-anthropic" markdown>
<div class="ma-anthropic-header">🎓 Anthropic'in ağzından dinle</div>

**[Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api)** — EN, ~2 saat, ücretsiz sertifikalı.
Bu kursun ilk üç dersi tam olarak bu sayfanın konusunu kaplıyor: ilk API çağrısı, messages yapısı, token hesabı. Python bilmen gerekir ama kod örnekleri adım adım açıklanıyor.

**[Claude 101](https://anthropic.skilljar.com/claude-101)** — EN, ~1 saat.
Kod yazmayan iş personası için: Claude'u günlük iş akışında ne kadar geniş kullanabileceğinin turu. Bu sayfadaki Yol 1 (Console) kısmının uzun versiyonu.

**[Messages API referansı](https://docs.claude.com/en/api/messages)** — EN.
Tek bir sayfa; her parametrenin ne işe yaradığı. Bu sayfada kullandığımız `model`, `max_tokens`, `messages` alanlarının resmi tanımları.
</div>

<div class="ma-sonraki" markdown>
<div class="ma-sonraki-header">➡️ Sonraki adım</div>

**[2.2 Token ve Bağlam Penceresi →](02-token-baglam.md)**
Yanıtı aldın; şimdi "neden bir sınır var" sorusu. Token ekonomisi ve bağlam penceresini anlayınca uzun metinlerle çalışmayı öğreniyorsun.

**Derinleşmek için (opsiyonel, EN):**
- [Anthropic Courses — GitHub](https://github.com/anthropics/courses) — API fundamentals notebook, kendi ritminde çalışılır.
</div>
