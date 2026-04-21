# Bölüm 0 — Temel Hazırlık (Foundation Setup)

!!! tip "Niye 'Bölüm 0'?"
    Çünkü bu bölüm AI dersi değil, **kurulum dersi**. Ama ön koşul. Bunlar kurulu değilse sonraki bölümlerin pratik kısımlarını yapamazsın.

## Bu Bölümde Öğreneceğin

- [ ] VPS'in temel Linux komutlarını ezbere bilmek
- [ ] Python 3.11+ kurulumu ve sanal ortam (venv) yönetimi
- [ ] Ollama ile yerel ücretsiz LLM çalıştırmak
- [ ] FastAPI ile basit bir web servisi yazmak
- [ ] İlk uçtan-uca AI servisini canlıya almak

## Sayfalar

1. **[0.1 VPS ve Linux Komutları](01-vps-linux.md)** — 15 komutta yetkin ol *(20 dk)*
2. **[0.2 Python ve Sanal Ortam](02-python-venv.md)** — venv, pip, requirements.txt *(15 dk)*
3. **[0.3 Ollama ile Yerel LLM](03-ollama.md)** — llama3.2 ve qwen2.5 indir, çalıştır *(30 dk)*
4. **[0.4 FastAPI İskeleti](04-fastapi.md)** — REST API yazma temelleri *(30 dk)*
5. **[0.5 İlk AI Servisi](05-ilk-ai-servisi.md)** — Ollama + FastAPI birleştir, canlı endpoint *(45 dk)*

## Tahmini Süre

**~2 saat** (5 sayfa × ortalama 25 dakika)

## Bittiğinde Elinde Ne Olacak

- VPS'inde çalışan yerel bir AI servisi: `http://89.167.90.113:9000/chat`
- POST attığında Ollama llama3.2 ile cevap dönen FastAPI uygulaması
- `/root/muhendisal-platform/playground/` altında temiz Python ortamı
- Sonraki tüm bölümlerin pratik kodlarını çalıştıracağın altyapı

---

**[Bölüm 0.1'e başla →](01-vps-linux.md)** &nbsp;&nbsp;|&nbsp;&nbsp; [← Ana Sayfa](../index.md)
