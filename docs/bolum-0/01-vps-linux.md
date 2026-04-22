# 0.1 VPS ve Linux Komutları (VPS and Linux Commands)

!!! info "Bu sayfanın amacı"
    AI Engineer olmak için kendi sunucunda (VPS) çalışacaksın. Bulut sağlayıcısından kiraladığın Linux makinasını yönetmen lazım. Bu sayfa, bilmen gereken **minimum 15 komutu** öğretir.

## 📘 Teori (Türkçe, basit dil)

**VPS (Virtual Private Server)** = Kiraladığın bir bilgisayar. İnternette bir yerde duruyor, sen SSH ile bağlanıp komut yazıyorsun, o da senin için çalışıyor. Senin ev bilgisayarın gibi ama her zaman açık, her yerden erişilebilir.

**Niye lazım?** AI servislerini (Ollama, FastAPI, vector database, chatbot) kendi bilgisayarında çalıştırırsan kapatınca durur. VPS'te 7/24 çalışır. KarıncaAI ve HBV chatbot'un zaten Hetzner VPS'te çalışıyor — `clawdbot2` (89.167.90.113).

**Linux komutları** = VPS'in arayüzü. Tıklama yok, klavye var. İlk başta zor görünür, ama 15-20 komut öğrenince %90'ını çözersin.

## 🗣️ Önemli İngilizce Terimler

| Terim | Türkçe | Nerede Kullanılır |
|---|---|---|
| **SSH** (Secure Shell) | Güvenli kabuk | Uzaktaki VPS'e bağlanmak |
| **shell / terminal** | kabuk / uçbirim | Komut yazdığın siyah ekran |
| **directory** | dizin / klasör | `ls`, `cd` komutlarıyla gezilir |
| **path** | yol | `/root/muhendisal-platform/` gibi |
| **process** | süreç | `ps aux` ile çalışan programlar |
| **daemon** | arkaplan servisi | `systemctl` ile yönetilen kalıcı servisler |
| **permission** | izin | `chmod 600 dosya` ile değiştirilir |
| **stdout / stderr** | standart çıktı / standart hata | `>` ile dosyaya yönlendirilir |

## 💻 Pratik Kod Örneği

Bu **15 komutu** ezberle, %90'ını çözersin:

```bash
# 1. NEREDESIN
pwd                          # şu anki klasörü göster

# 2. NE VAR
ls -la                       # tüm dosyaları detaylı listele

# 3. KLASÖR DEĞIŞTIR
cd /root/muhendisal-platform
cd ..                        # bir üst klasöre

# 4. KLASÖR/DOSYA YARAT
mkdir yeni-klasor
touch yeni-dosya.txt

# 5. SİL (DİKKAT, geri dönüş yok)
rm dosya.txt
rm -rf eski-klasor           # klasörü içindekilerle sil

# 6. KOPYALA / TAŞI
cp dosya.txt yedek.txt
mv eski-isim.txt yeni-isim.txt

# 7. DOSYA OKU
cat dosya.txt                # tüm içerik
head -20 dosya.txt           # ilk 20 satır
tail -f log.txt              # son satırlar (canlı takip için -f)

# 8. ARAMA
grep "kelime" dosya.txt      # dosyada kelime ara
find /root -name "*.py"      # py dosyalarını bul

# 9. ÇALIŞAN SÜREÇLER
ps aux | grep python         # python süreçleri
htop                         # canlı sistem görünümü (q ile çık)

# 10. YETKİ
chmod 755 script.sh          # çalıştırılabilir yap
chmod 600 .env               # sadece sen okuyabil

# 11. SERVİS YÖNETİMİ (systemd)
systemctl status nginx       # nginx durumu
systemctl restart nginx      # nginx'i yeniden başlat
journalctl -u nginx -n 50    # son 50 log satırı

# 12. PM2 (Node.js süreçleri için)
pm2 list                     # çalışan süreçler
pm2 logs hbv-chatbot         # HBV chatbot loglarını gör
pm2 restart 15               # ID 15'i (HBV) yeniden başlat

# 13. DİSK / RAM
df -h                        # disk kullanımı
free -h                      # RAM kullanımı
du -sh /root/MühendisAl/     # bir klasör ne kadar yer kaplıyor

# 14. AĞ
curl https://wiki.oluk.org   # bir URL'den içerik çek
ping google.com              # bağlantı testi (Ctrl+C ile dur)

# 15. ARKAPLANDA ÇALIŞTIR (uzun sürecek işler için)
nohup python3 uzun_is.py > log.txt 2>&1 &
# Not: `&` arkaplana atar, `nohup` SSH kapansa bile çalıştırır
```

## 🛠️ Bugün Yapacağın Görev (15-30 dk)

1. VPS'ine SSH ile bağlan: `ssh vps`
2. Şu komutları sırayla çalıştır ve **çıktıyı bir not defterine yaz**:
   - `pwd`
   - `ls -la /root/`
   - `df -h` → boş disk alanın kaç GB?
   - `free -h` → boş RAM'in kaç GB?
   - `pm2 list` → kaç PM2 süreci çalışıyor?
   - `systemctl status nginx` → çalışıyor mu?
3. Şu klasörü bul: `find /root -name "translate_gemini.py" 2>/dev/null`
4. Bulduğun dosyanın ilk 5 satırını oku: `head -5 BULUNAN_YOL`
5. Disk kullanımı en büyük 3 klasörü bul: `du -sh /root/* 2>/dev/null | sort -hr | head -3`

## 🧪 Simülasyon ve Test

Şu komut serisini çalıştır:

```bash
cd /tmp
mkdir test-muhendisal
cd test-muhendisal
echo "Merhaba VPS" > test.txt
cat test.txt
ls -la
cd ..
rm -rf test-muhendisal
ls /tmp/test-muhendisal 2>&1
```

**Beklenen çıktı:**

```
Merhaba VPS
total 12
drwxr-xr-x 2 root root 4096 ...  .
drwxrwxrwt ... ...                ..
-rw-r--r-- 1 root root   12 ...  test.txt
ls: cannot access '/tmp/test-muhendisal': No such file or directory
```

Son satır **hata vermesi normal** — çünkü klasörü sildin, artık yok. "No such file or directory" hatası, başarılı bir silme işleminin kanıtı.

!!! warning "Sık yapılan hata"
    `rm -rf /` **sakın yazma**. Bu tüm sistemi siler. `rm -rf` sadece sınırlı bir alt klasörle kullan, kök dizinde değil.

## 🎮 Canlı Pratik (Etkileşimli Widget)

Aşağıdaki bloklar **F6/F7 interaktif widget'larla** çalışır. Quiz'lere tıklayınca anında doğru/yanlış görürsün, backend'e kaydedilir, **+XP** kazanırsın. Kod bloğundaki "▶ Çalıştır" butonu **F9'da** Pyodide ile aktif olacak.

### Python örneği

<pre data-ma-run="python"><code>import os

# Şu anki klasor
print(os.getcwd())

# Icindeki dosyalar
for dosya in sorted(os.listdir('.')):
    print(dosya)
</code></pre>

### Quiz 1 — pwd komutu

<div class="ma-quiz" data-quiz-id="b0-01-live-q1" data-correct="B">
<p class="ma-quiz-q"><code>pwd</code> komutu ne yapar?</p>
<div class="ma-opt" data-key="A">A) Dosya siler</div>
<div class="ma-opt" data-key="B">B) Şu anki dizinin yolunu yazdırır</div>
<div class="ma-opt" data-key="C">C) Kullanıcı şifresi değiştirir</div>
<div class="ma-opt" data-key="D">D) Paket kurar</div>
</div>

### Quiz 2 — Klasör silme

<div class="ma-quiz" data-quiz-id="b0-01-live-q2" data-correct="C">
<p class="ma-quiz-q">Bir klasörü <strong>içindekilerle birlikte</strong> silmek için hangi komut kullanılır?</p>
<div class="ma-opt" data-key="A">A) <code>rm dosya.txt</code></div>
<div class="ma-opt" data-key="B">B) <code>rmdir klasor</code></div>
<div class="ma-opt" data-key="C">C) <code>rm -rf klasor</code></div>
<div class="ma-opt" data-key="D">D) <code>delete klasor</code></div>
</div>

## ❓ Kendini Test Et

??? quiz "1. SSH'ın açılımı nedir?"
    **Secure Shell** — uzak makinaya güvenli bağlanma protokolü.

??? quiz "2. Bir klasördeki tüm `.py` dosyalarını nasıl listelersin?"
    `find /klasör -name "*.py"` veya `ls *.py` (sadece o klasör için).

??? quiz "3. SSH kapansa bile çalışmaya devam eden bir Python scripti nasıl başlatırsın?"
    `nohup python3 script.py > log.txt 2>&1 &` — `nohup` SSH'tan bağımsız tutar, `&` arkaplana atar.

??? quiz "4. `chmod 600 dosya` ne yapar?"
    Dosyayı **sadece sahibinin** okuyabileceği/yazabileceği yapar. API anahtarları (`.env`) için kritik.

??? quiz "5. `pm2 logs hbv-chatbot` ne yapar?"
    HBV chatbot süreci tarafından üretilen logları **canlı olarak** gösterir. Hata yakalamak için her geliştiricinin günlük kullandığı komut.

## 🔗 Sonraki Adım

Linux temellerini öğrendin. Şimdi Python ve sanal ortam kurmaya geç:

**[→ 0.2 Python ve Sanal Ortam](02-python-venv.md)**

## 📚 Daha Detay

- 📖 [Linux komut sözlüğü (Türkçe)](https://www.linuxakademi.com/komutlar) — daha derin gitmek için
- 📖 [The Missing Semester (MIT)](https://missing.csail.mit.edu/) — İngilizce ama çok değerli
- 📖 Referans çeviri: [Linux temelleri](https://wiki.oluk.org/muhendisal/) (mevcut çeviri arşivinde)
- 🎥 [Linux 101 Türkçe (YouTube)](https://www.youtube.com/results?search_query=linux+t%C3%BCrk%C3%A7e+temel)
