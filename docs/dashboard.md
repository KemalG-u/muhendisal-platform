# 📊 Dashboard

İlerlemeni, quiz geçmişini ve hedef seçimini tek ekranda takip edersin. Sayfa otomatik olarak backend'den veri çeker.

## 🎯 Hedefin

<div class="ma-target-tabs">
<button class="ma-target-tab" data-target="hepsi">Hepsi</button>
<button class="ma-target-tab" data-target="hbv">HBV Projesi</button>
<button class="ma-target-tab" data-target="kisisel">Kişisel</button>
<button class="ma-target-tab" data-target="is">İş / Freelance</button>
</div>

Hedefin, ileride içerik filtrelemesini ayarlar. Şimdilik profilinde saklanır (F13+ içerik yazıldığında aktif kullanılır).

## 🗓️ Bugün

<div class="ma-today-banner" id="ma-today-banner"><em>Yükleniyor…</em></div>

## 📅 Haftalık Aktivite

<div class="ma-heatmap-wrap">
<div class="ma-heatmap" id="ma-heatmap"></div>
<div class="ma-heatmap-legend"><span>az</span><i class="ma-hm-l0"></i><i class="ma-hm-l1"></i><i class="ma-hm-l2"></i><i class="ma-hm-l3"></i><i class="ma-hm-l4"></i><span>çok</span></div>
</div>
<p class="ma-heatmap-note"><em>Aktivite XP — quiz ve tamamlanan sayfalar. Günlük streak ping (+20 XP/gün) bu grafiğe girmez, toplam XP'de görülür.</em></p>

## 📈 Bu Seviye

<div class="ma-cards">
<div class="ma-card"><div class="ma-card-label">Toplam XP</div><div class="ma-card-value" id="ma-dash-xp">—</div></div>
<div class="ma-card"><div class="ma-card-label">Günlük Streak</div><div class="ma-card-value" id="ma-dash-streak">—</div></div>
<div class="ma-card"><div class="ma-card-label">Tamamlanan Sayfa</div><div class="ma-card-value" id="ma-dash-done">—</div></div>
<div class="ma-card"><div class="ma-card-label">Quiz Doğruluk</div><div class="ma-card-value" id="ma-dash-acc">—</div></div>
</div>

## 🧪 Son Quiz Denemelerin

<div id="ma-dash-quiz"><em>Yükleniyor…</em></div>

## 🗺️ İlerleme

<div class="ma-pg-legend">○ başlamadın · 👁 gördün · ✓ tamamladın</div>

<div id="ma-pg-list">
<!-- PAGES_START -->
<h3 class="ma-pg-section">Genel</h3>
<div class="ma-pg-row" data-page-path="yazim-kurallari"><span class="ma-pg-icon">○</span><span class="ma-pg-label">Yazım Kuralları (CTO)</span></div>
<h3 class="ma-pg-section">Bölüm 0 — Temel Hazırlık</h3>
<div class="ma-pg-row" data-page-path="bolum-0/01-vps-linux"><span class="ma-pg-icon">○</span><span class="ma-pg-label">0.1 VPS ve Linux Komutları</span></div>
<div class="ma-pg-row" data-page-path="bolum-0/02-python-venv"><span class="ma-pg-icon">○</span><span class="ma-pg-label">0.2 Python ve Sanal Ortam</span></div>
<div class="ma-pg-row" data-page-path="bolum-0/03-ollama"><span class="ma-pg-icon">○</span><span class="ma-pg-label">0.3 Ollama ile Yerel LLM</span></div>
<div class="ma-pg-row" data-page-path="bolum-0/04-fastapi"><span class="ma-pg-icon">○</span><span class="ma-pg-label">0.4 FastAPI İskeleti</span></div>
<div class="ma-pg-row" data-page-path="bolum-0/05-ilk-ai-servisi"><span class="ma-pg-icon">○</span><span class="ma-pg-label">0.5 İlk AI Servisi</span></div>
<h3 class="ma-pg-section">Bölüm 1 — Giriş ve Temeller</h3>
<div class="ma-pg-row" data-page-path="bolum-1/01-ai-engineer-nedir"><span class="ma-pg-icon">○</span><span class="ma-pg-label">1.1 AI Engineer Nedir</span></div>
<div class="ma-pg-row" data-page-path="bolum-1/02-ai-vs-ml-engineer"><span class="ma-pg-icon">○</span><span class="ma-pg-label">1.2 AI Engineer vs ML Engineer</span></div>
<div class="ma-pg-row" data-page-path="bolum-1/03-ekosistem"><span class="ma-pg-icon">○</span><span class="ma-pg-label">1.3 AI Ekosistemi 2026</span></div>
<div class="ma-pg-row" data-page-path="bolum-1/04-yol-secimi"><span class="ma-pg-icon">○</span><span class="ma-pg-label">1.4 Hangi Yolu Seçmeli</span></div>
<h3 class="ma-pg-section">Bölüm 2 — LLM ve Prompt Engineering</h3>
<div class="ma-pg-row" data-page-path="bolum-2/01-llm-temelleri"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.1 LLM Nedir, Nasıl Çalışır</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/02-token-baglam"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.2 Token, Bağlam, Maliyet</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/03-sampling"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.3 Sıcaklık ve Sampling</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/04-sistem-prompt"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.4 Sistem ve Kullanıcı Promptu</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/05-few-shot-cot"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.5 Few-shot ve Chain-of-Thought</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/06-sablonlar"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.6 Prompt Şablonları</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/07-prompt-injection"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.7 Prompt Enjeksiyonu ve Savunma</span></div>
<div class="ma-pg-row" data-page-path="bolum-2/08-test-degerlendirme"><span class="ma-pg-icon">○</span><span class="ma-pg-label">2.8 Prompt Test ve Değerlendirme</span></div>
<h3 class="ma-pg-section">Bölüm 3 — Embeddings ve Vector DB</h3>
<div class="ma-pg-row" data-page-path="bolum-3/01-embedding-nedir"><span class="ma-pg-icon">○</span><span class="ma-pg-label">3.1 Embedding Nedir</span></div>
<div class="ma-pg-row" data-page-path="bolum-3/02-modeller"><span class="ma-pg-icon">○</span><span class="ma-pg-label">3.2 OpenAI ve Açık Kaynak Modeller</span></div>
<div class="ma-pg-row" data-page-path="bolum-3/03-vector-db"><span class="ma-pg-icon">○</span><span class="ma-pg-label">3.3 Vector DB Karşılaştırma</span></div>
<div class="ma-pg-row" data-page-path="bolum-3/04-qdrant"><span class="ma-pg-icon">○</span><span class="ma-pg-label">3.4 Qdrant Pratik Kurulum</span></div>
<div class="ma-pg-row" data-page-path="bolum-3/05-semantic-search"><span class="ma-pg-icon">○</span><span class="ma-pg-label">3.5 Semantic Search Uygulaması</span></div>
<h3 class="ma-pg-section">Bölüm 4 — RAG</h3>
<div class="ma-pg-row" data-page-path="bolum-4/01-rag-nedir"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.1 RAG Nedir, Niye Lazım</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/02-chunking"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.2 Chunking Stratejileri</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/03-retrieval"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.3 Retrieval ve Re-ranking</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/04-context-eng"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.4 Context Engineering</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/05-degerlendirme"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.5 RAG Değerlendirme</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/06-langchain"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.6 LangChain ile RAG</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/07-llamaindex"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.7 LlamaIndex ile RAG</span></div>
<div class="ma-pg-row" data-page-path="bolum-4/08-production"><span class="ma-pg-icon">○</span><span class="ma-pg-label">4.8 Production RAG (HBV Vakası)</span></div>
<h3 class="ma-pg-section">Bölüm 5 — RAG vs Fine-tuning</h3>
<div class="ma-pg-row" data-page-path="bolum-5/01-finetune-nedir"><span class="ma-pg-icon">○</span><span class="ma-pg-label">5.1 Fine-tuning Nedir</span></div>
<div class="ma-pg-row" data-page-path="bolum-5/02-karar"><span class="ma-pg-icon">○</span><span class="ma-pg-label">5.2 Hangisini Seçmeli</span></div>
<div class="ma-pg-row" data-page-path="bolum-5/03-lora"><span class="ma-pg-icon">○</span><span class="ma-pg-label">5.3 LoRA ve QLoRA</span></div>
<div class="ma-pg-row" data-page-path="bolum-5/04-hf-pratik"><span class="ma-pg-icon">○</span><span class="ma-pg-label">5.4 Hugging Face ile Pratik</span></div>
<h3 class="ma-pg-section">Bölüm 6 — AI Agents ve MCP</h3>
<div class="ma-pg-row" data-page-path="bolum-6/01-agent-nedir"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.1 Agent Nedir, ReAct Pattern</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/02-tool-calling"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.2 Tool Calling</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/03-mcp"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.3 MCP Protokolü</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/04-mcp-server"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.4 MCP Server Yazma</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/05-multi-agent"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.5 Multi-Agent Sistemler</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/06-claude-sdk"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.6 Claude Agent SDK</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/07-langchain"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.7 LangChain Agents</span></div>
<div class="ma-pg-row" data-page-path="bolum-6/08-production"><span class="ma-pg-icon">○</span><span class="ma-pg-label">6.8 Üretim Agent (KarincaAI Vakası)</span></div>
<h3 class="ma-pg-section">Bölüm 7 — Multimodal</h3>
<div class="ma-pg-row" data-page-path="bolum-7/01-goruntu"><span class="ma-pg-icon">○</span><span class="ma-pg-label">7.1 Görüntü Modelleri</span></div>
<div class="ma-pg-row" data-page-path="bolum-7/02-ses"><span class="ma-pg-icon">○</span><span class="ma-pg-label">7.2 Ses ve TTS/STT</span></div>
<div class="ma-pg-row" data-page-path="bolum-7/03-video"><span class="ma-pg-icon">○</span><span class="ma-pg-label">7.3 Video İşleme</span></div>
<div class="ma-pg-row" data-page-path="bolum-7/04-vision-language"><span class="ma-pg-icon">○</span><span class="ma-pg-label">7.4 Vision-Language Modeller</span></div>
<h3 class="ma-pg-section">Bölüm 8 — Güvenlik ve Production</h3>
<div class="ma-pg-row" data-page-path="bolum-8/01-tehditler"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.1 Güvenlik Tehditleri</span></div>
<div class="ma-pg-row" data-page-path="bolum-8/02-etik"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.2 Etik ve Önyargı</span></div>
<div class="ma-pg-row" data-page-path="bolum-8/03-maliyet"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.3 Rate Limit ve Maliyet Kontrolü</span></div>
<div class="ma-pg-row" data-page-path="bolum-8/04-loglama"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.4 Loglama ve İzleme</span></div>
<div class="ma-pg-row" data-page-path="bolum-8/05-hata-yonetimi"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.5 Hata Yönetimi</span></div>
<div class="ma-pg-row" data-page-path="bolum-8/06-checklist"><span class="ma-pg-icon">○</span><span class="ma-pg-label">8.6 Production Checklist</span></div>
<h3 class="ma-pg-section">Bölüm 9 — Deployment ve Portföy</h3>
<div class="ma-pg-row" data-page-path="bolum-9/01-docker"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.1 Docker ile Paketleme</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/02-cloud"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.2 Cloud Deploy (DO, Hetzner)</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/03-cicd"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.3 CI/CD GitHub Actions</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/04-proje-1"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.4 Portföy Projesi 1 — RAG Chatbot</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/05-proje-2"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.5 Portföy Projesi 2 — Agent Otomasyon</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/06-proje-3"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.6 Portföy Projesi 3 — Multimodal Asistan</span></div>
<div class="ma-pg-row" data-page-path="bolum-9/07-github"><span class="ma-pg-icon">○</span><span class="ma-pg-label">9.7 GitHub README ve Dokümantasyon</span></div>
<h3 class="ma-pg-section">Bölüm 10 — İleri Seviye ve Kariyer</h3>
<div class="ma-pg-row" data-page-path="bolum-10/01-linkedin"><span class="ma-pg-icon">○</span><span class="ma-pg-label">10.1 LinkedIn Profil Optimizasyonu</span></div>
<div class="ma-pg-row" data-page-path="bolum-10/02-mulakat"><span class="ma-pg-icon">○</span><span class="ma-pg-label">10.2 Mülakat Soruları</span></div>
<div class="ma-pg-row" data-page-path="bolum-10/03-acik-kaynak"><span class="ma-pg-icon">○</span><span class="ma-pg-label">10.3 Açık Kaynak Katkı</span></div>
<div class="ma-pg-row" data-page-path="bolum-10/04-ileri-konular"><span class="ma-pg-icon">○</span><span class="ma-pg-label">10.4 İleri Konular ve Trendler</span></div>
<div class="ma-pg-row" data-page-path="bolum-10/05-topluluk"><span class="ma-pg-icon">○</span><span class="ma-pg-label">10.5 Topluluk ve Mentorluk</span></div>
<!-- PAGES_END -->
</div>
