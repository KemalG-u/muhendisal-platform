# MühendisAl Platform — Sözlük (Glossary)
#
# Bu dosya pre_build.py hook'u tarafından her sayfaya otomatik eklenir.
# Markdown `abbr` extension bu tanımları alıp terimin her geçtiği yerde
# HTML `<abbr title="...">` sarımı yapar → MkDocs Material tooltip gösterir.
#
# DİKKAT: abbr case-sensitive. "Agent" tanımı "agent" kelimesini sarmaz.
# Bu yüzden hem büyük hem küçük harf varyantları ayrı tanımlanır.
#
# Yeni terim eklerken: *[TERIM]: Açıklama — tek satır, 160 karakterden kısa
# Terimler alfabetik (büyük harf), hemen altında küçük harf varyantı.

*[Agent]: Kendi kendine karar veren, araç kullanıp iş tamamlayan yapay zeka — "sohbet eden Claude" değil "iş yapan Claude"
*[agent]: Kendi kendine karar veren, araç kullanıp iş tamamlayan yapay zeka — "sohbet eden Claude" değil "iş yapan Claude"
*[API]: Application Programming Interface — iki yazılımın birbiriyle konuşmasını sağlayan köprü
*[API Key]: Senin kimliğini ispatlayan gizli anahtar — sızdırılmamalı, koda yazılmaz
*[Bağlam penceresi]: Modelin bir defada görebileceği en fazla token miktarı
*[bağlam penceresi]: Modelin bir defada görebileceği en fazla token miktarı
*[Chunking]: Uzun belgeyi küçük parçalara bölme — RAG için
*[chunking]: Uzun belgeyi küçük parçalara bölme — RAG için
*[CLI]: Command Line Interface — komut satırı / terminal
*[CoT]: Chain-of-Thought — modelin adım adım düşünmesini istemek
*[Console]: Anthropic'in web paneli (console.anthropic.com) — API key, fatura, Workbench burada
*[console]: Anthropic'in web paneli (console.anthropic.com) — API key, fatura, Workbench burada
*[Context window]: Modelin bir defada görebileceği en fazla token miktarı (bağlam penceresi)
*[Embedding]: Bir metni sayılardan oluşan vektöre çevirme — benzer anlamlı metinler yakın vektörler üretir
*[embedding]: Bir metni sayılardan oluşan vektöre çevirme — benzer anlamlı metinler yakın vektörler üretir
*[Endpoint]: API'nin belirli bir işlevinin adresi — /v1/messages, /v1/embeddings gibi
*[endpoint]: API'nin belirli bir işlevinin adresi — /v1/messages, /v1/embeddings gibi
*[Fine-tuning]: Hazır bir modeli kendi verinle özel göreve uyarlama
*[fine-tuning]: Hazır bir modeli kendi verinle özel göreve uyarlama
*[Hallucination]: Modelin emin olmadığı bir bilgiyi doğruymuş gibi üretmesi
*[hallucination]: Modelin emin olmadığı bir bilgiyi doğruymuş gibi üretmesi
*[Header]: HTTP isteğinin meta bilgisi — kimlik, format, sürüm bilgisi burada taşınır
*[header]: HTTP isteğinin meta bilgisi — kimlik, format, sürüm bilgisi burada taşınır
*[HTTPS]: Tarayıcı-sunucu iletişim kuralının şifrelenmiş hali
*[IDE]: Integrated Development Environment — kod yazma programı (VS Code, PyCharm gibi)
*[JSON]: JavaScript Object Notation — veri taşıma formatı, `{"ad": "Kemal"}` gibi
*[LLM]: Large Language Model — büyük dil modeli; bir sonraki kelimeyi tahmin ederek cevap üreten yapay zeka
*[LoRA]: Low-Rank Adaptation — fine-tuning'in ucuz ve hızlı versiyonu
*[MCP]: Model Context Protocol — Claude'un dış sistemlere (Gmail, DB, dosya) erişmek için kullandığı standart protokol
*[Multimodal]: Metin dışında görsel, ses, video da işleyebilen model
*[multimodal]: Metin dışında görsel, ses, video da işleyebilen model
*[pip]: Python paket yöneticisi — `pip install paket_adi`
*[Prompt]: Modele verdiğin giriş metni — bir görevi yazılı olarak tarif etmek
*[prompt]: Modele verdiğin giriş metni — bir görevi yazılı olarak tarif etmek
*[Prompt injection]: Kullanıcının modele gizli talimat enjekte ederek onu kandırma saldırısı
*[RAG]: Retrieval-Augmented Generation — modelin cevap üretirken ilgili belgeleri getirip bağlama eklemesi; kendi verin üzerinde AI çalıştırmanın yolu
*[Rate limit]: Belirli bir sürede atabileceğin en fazla istek sayısı sınırı
*[rate limit]: Belirli bir sürede atabileceğin en fazla istek sayısı sınırı
*[Re-ranking]: Getirilen sonuçları yeniden sıralayıp en uygunu seçme
*[Retrieval]: Bir soruya en yakın belge parçalarını bulma
*[retrieval]: Bir soruya en yakın belge parçalarını bulma
*[SDK]: Software Development Kit — bir API'yi kolayca kullanmanı sağlayan hazır kütüphane
*[Semantic search]: Anahtar kelime değil, anlam üzerinden arama
*[semantic search]: Anahtar kelime değil, anlam üzerinden arama
*[Snapshot]: Modelin belirli bir tarihe sabitlenmiş sürümü — `claude-sonnet-4-5-20250929` gibi
*[snapshot]: Modelin belirli bir tarihe sabitlenmiş sürümü — `claude-sonnet-4-5-20250929` gibi
*[Streaming]: Cevabın tamamı beklenmeden, token token anında akması
*[streaming]: Cevabın tamamı beklenmeden, token token anında akması
*[STT]: Speech-to-Text — sesi yazıya çevirme
*[System prompt]: Modelin kimliğini ve kurallarını belirleyen üst düzey yönerge
*[system prompt]: Modelin kimliğini ve kurallarını belirleyen üst düzey yönerge
*[Temperature]: Modelin rastgeleliği; düşük = kararlı, yüksek = yaratıcı
*[temperature]: Modelin rastgeleliği; düşük = kararlı, yüksek = yaratıcı
*[Token]: LLM'in metni ölçtüğü birim — kelimenin kabaca dörtte üçüne denk gelir; API ücreti token sayısına göre
*[token]: LLM'in metni ölçtüğü birim — kelimenin kabaca dörtte üçüne denk gelir; API ücreti token sayısına göre
*[Tool calling]: Modelin belirli fonksiyonları (hava durumu, veritabanı sorgusu) çağırabilmesi
*[tool calling]: Modelin belirli fonksiyonları (hava durumu, veritabanı sorgusu) çağırabilmesi
*[TTS]: Text-to-Speech — yazıyı sese çevirme
*[User prompt]: Son kullanıcının modele yazdığı mesaj
*[user prompt]: Son kullanıcının modele yazdığı mesaj
*[Vector DB]: Embedding vektörlerini depolayıp anlamsal arama yapan veritabanı (Qdrant, Pinecone gibi)
*[venv]: Virtual environment — Python bağımlılıklarını projeye özel izole etme
*[Webhook]: Bir olay olduğunda otomatik tetiklenen dış URL çağrısı
*[webhook]: Bir olay olduğunda otomatik tetiklenen dış URL çağrısı
*[Workbench]: Anthropic Console içinde promptları test ettiğin kod yazmadan çalışan deneme ekranı
*[workbench]: Anthropic Console içinde promptları test ettiğin kod yazmadan çalışan deneme ekranı
*[Zero-shot]: Örnek vermeden doğrudan görev tarif etmek
*[zero-shot]: Örnek vermeden doğrudan görev tarif etmek
