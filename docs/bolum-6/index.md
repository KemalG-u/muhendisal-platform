# Bölüm 6 — AI Agents ve MCP

<div class="ma-meta" markdown>
<div class="ma-meta-row" markdown>
<strong>Kim için:</strong>
<span class="ma-persona ma-persona-baslangic">🟢 başlangıç</span>
<span class="ma-persona ma-persona-is">🔵 iş</span>
<span class="ma-persona ma-persona-kisisel">🟣 kişisel</span>
</div>
<div class="ma-meta-row"><strong>📋 Önkoşul:</strong> Bölüm 2 bitmiş (prompt engineering + tool use kavramı), Bölüm 4 bitmiş (RAG — retrieve/generate ayrımı oturmuş); bir MCP sunucusu kurabilecek backend refleksin var (FastAPI + venv)</div>
<div class="ma-meta-row"><strong>🎯 Çıktı:</strong> Kendi yazdığın **MCP sunucun** ayakta, Claude Desktop'tan "takvimimi göster" dediğinde senin yazdığın tool çalışıyor + Claude'un ReAct döngüsünde çok adımlı görev bitirdiği **canlı demo** + 4 Anthropic Academy kursu (Intro MCP, Advanced MCP, Subagents, Agent Skills) için içerik zemini.</div>
</div>

## Neden bu bölüm?

2024 sonunda Anthropic **MCP (Model Context Protocol)**'ü duyurdu. 2025'te "AI için USB-C" dediler. 2026 itibarıyla MCP **Anthropic'in en güçlü ürün farkı.** OpenAI yok, Google yok — MCP Anthropic ekosistemine özel açık standart.

Senin için iki büyük getirisi var: (1) Claude Desktop'a kendi araçlarını bağlayıp "Claude Slack'ime mesaj at" demek; (2) İşyeri projende "Claude kendi database'imle konuşsun, rapor üretsin" sistemini kurmak. İkisi de MCP ile 30 satırlık kod.

Üçüncü neden: **Agent = LLM + Tool + Loop.** Bu denklem bu bölümde kurulur. ReAct pattern'ını öğrenince "Claude'a özerk görev delege etmek" mimarsı zihinde oturur.

## Bölüm 6 kısaca

**6.1 — Agent Nedir, ReAct Pattern.** LLM vs agent farkı. "Think → Act → Observe" döngüsü. Hata durumunda agent ne yapar (retry, fallback, hand-off).

**6.2 — Tool Calling.** Claude API'nin `tools` parametresi. JSON schema ile tool tanımlama, Claude'un hangi tool'u çağırdığını anlama, sonucu geri yollama. 3-4 basit tool örnek.

**6.3 — MCP Protokolü.** MCP ne, neyi çözüyor, **tool use'dan farkı**. Resources + Tools + Prompts üç primitive. Neden "AI için USB-C".

**6.4 — MCP Server Yazma.** Python `mcp` kütüphanesi ile kendi server'ın. 3-4 endpoint: "takvim oku", "email taslak yaz", "dosya listele". Claude Desktop'a entegre etme.

**6.5 — Multi-Agent Sistemler.** Tek agent yetmediğinde — planner + executor + critic rolleri. Multi-agent orkestrasyon teknikleri (Subagents Anthropic yaklaşımı).

**6.6 — Claude Agent SDK.** Anthropic'in yeni SDK'sı (2025). "Kendi agent'ını 50 satırda kur" vaadi. Gerçeklikle karşılaştırma.

**6.7 ve 6.8 (nav'da kapalı):** Production agent — timeout, maliyet, gözlemlenebilirlik, insan onayı gerektiren adımlar.

## Bu bölümün yol haritası

```mermaid
flowchart LR
  S["👤 Sen\n(B5 bitti)"]
  P61["📄 6.1\nAgent +\nReAct"]
  P62["📄 6.2\nTool\ncalling"]
  P63["📄 6.3\nMCP ne"]
  P64["🏁 6.4\nMCP server\nyazma"]
  P65["📄 6.5\nMulti-\nagent"]
  P66["📄 6.6\nAgent\nSDK"]
  P67["📄 6.7-6.8\nProduction"]
  MCP[("🔌 MCP\nprotokolü\nJSON-RPC")]
  OUT{{"✅ Kendi MCP\nsunucun + Claude\nDesktop entegre"}}
  ANT[("📖 Anthropic\n4 Academy\nkursu + MCP\ndocs"])

  S --> P61 --> P62 --> P63 --> P64 --> P65 --> P66 --> P67 --> OUT
  P63 -.köprü.-> ANT
  P64 -.kullanır.-> MCP
  P65 -.köprü.-> ANT
  P66 -.köprü.-> ANT

  classDef user fill:#ddd6fe,stroke:#7c3aed,color:#111
  classDef page fill:#dbeafe,stroke:#2563eb,color:#111
  classDef pilot fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef infra fill:#fed7aa,stroke:#ea580c,color:#111
  classDef goal fill:#fef3c7,stroke:#ca8a04,color:#111
  classDef ext fill:#fed7aa,stroke:#ea580c,color:#111
  class S user
  class P61,P62,P63,P65,P66,P67 page
  class P64 pilot
  class MCP infra
  class OUT goal
  class ANT ext
```

### Aktör tablosu

| Düğüm | Nerede | Ne iş yapıyor |
|---|---|---|
| 👤 **Sen** | Python + Claude Desktop + terminal | Tool use dene, MCP server yaz, Claude Desktop'a entegre et |
| 📄 **6.1 Agent + ReAct** | Platform | Kavram + döngü |
| 📄 **6.2 Tool calling** | Platform + Python | 3-4 basit tool örnek (hesap makinesi, tarih, arama) |
| 📄 **6.3 MCP ne** | Platform | Protokol + 3 primitive tanım |
| 🏁 **6.4 MCP server yazma** | Python + MCP kütüphanesi | 30 satır kod, Claude Desktop bağlanıyor |
| 📄 **6.5 Multi-agent** | Platform + Python | 3 rol örneği |
| 📄 **6.6 Agent SDK** | Python + Claude SDK | "Anthropic'in yeni SDK" karşılaştırma |
| 📄 **6.7-6.8 Production** | Python + monitoring | Timeout + maliyet + insan onayı |
| 🔌 **MCP protokolü** | Standart (JSON-RPC üstü) | Claude ↔ tool arası iletişim kuralları |
| 📖 **Anthropic Academy (4 kurs)** | skilljar.com | Intro to MCP + Advanced MCP + Intro to Subagents + Agent Skills |
| ✅ **Çıktı** | Repo `6-mcp-server/` + Claude Desktop config | Canlı demo: "Claude Desktop'tan 'takvimimi göster' dedim, geldi" |

## Bu bölüm bittiğinde elinde ne olacak

- **Çalışan MCP sunucun:** 3-4 tool'la, Claude Desktop'tan çağrılabiliyor. Bu **Anthropic ekosisteminde saygı gören refleks**
- **Tool calling refleksi:** Yeni bir proje için "bu LLM + şu external servis" entegrasyonunu 30 dk'da kurabilirsin
- **Agent mimarisi anlamı:** Multi-step görev geldiğinde "tek agent yeter mi, planner+executor ayrımı lazım mı" sorusunu sorup cevaplayabiliyorsun
- **ReAct döngüsü deneyimi:** Think-Act-Observe döngüsünü kendi kodunda yazmışsın
- **Production gerçeği:** "Agent devasa tokenle patlar" tuzağına düşmeden timeout + cost cap + human-in-the-loop kurmayı biliyorsun
- **4 Anthropic Academy sertifikası eşiği:** Bölümü bitirirken 4 kursun tamamı senin için erişilebilir — içerik hazırlığı tamamsa sertifika almak 1-2 gün iş

Bu çıktı **platformun zirvesi.** Bölüm 7-10 kalan pürüzleri (multimodal, güvenlik, deploy, kariyer) kapatıyor ama teknik olarak bu bölüm sonunda bir agent geliştiricisisin.

<div class="ma-anthropic-oz" markdown>
<div class="ma-anthropic-oz-header">📖 Anthropic bu bölümde ne der — öz</div>

Bölüm 6 **Anthropic'in en kalın ve en güncel teknik koleksiyonu.** 4 Academy kursu burada:

**1. Introduction to Model Context Protocol (~45 dk, sertifikalı).** MCP ne, niye var, nasıl çalışır. Bizim 6.3'ü geniş kapsamda işler. 6.3 bittikten sonra aç.

**2. Model Context Protocol: Advanced Topics (~60 dk, sertifikalı).** Production MCP — authentication, streaming, resource templates. 6.4'ten sonra aç; kendi server'ını yazdıktan sonra derinleşmek için.

**3. Introduction to Subagents (~30 dk, sertifikalı).** Multi-agent orkestrasyonun Anthropic yaklaşımı. 6.5'le paralel okuma.

**4. Introduction to Agent Skills (~45 dk, sertifikalı).** "Skills" Anthropic'in yeni kavramı (2025) — MCP tool'larının üstüne "yetenek paketi" katmanı. 6.6 Agent SDK ile birleşik okuma.

**5. Docs — MCP Resources + Tools + Prompts.** [platform.claude.com/docs/en/mcp](https://platform.claude.com/docs/en/mcp) Anthropic'in kanonik MCP dokümantasyonu. 3 yapı taşının (resource, tool, prompt) tam spesifikasyonu burada. 6.3-6.4'te referans.

**6. GitHub — anthropics/mcp-server ve ekosistem sunucuları.** Claude'un desteklediği örnek MCP server'lar (Slack, Google Drive, GitHub, Postgres). 6.4'te kendi server'ını yazarken örnek olarak oku.

<div class="ma-anthropic-oz-kaynak" markdown>
**Kaynak:** [Anthropic Academy — Introduction to Model Context Protocol](https://anthropic.skilljar.com/) (İngilizce, ~45 dk, ücretsiz + sertifika). 6.3'ten önce veya sonra aç. MCP'yi Anthropic'in ağzından dinlemek kavramın yerleşmesi için kritik — bu protokol Anthropic'in farkı.
</div>
</div>

---

<div class="ma-sonraki" markdown>
**Bir sonraki adım →** [6.1 Agent Nedir, ReAct Pattern](01-agent-nedir.md) (40 dk, agent kavramı + döngü)

← [Bölüm 5 — RAG vs Fine-tuning](../bolum-5/index.md) &nbsp;|&nbsp; [Ana Sayfa](../index.md)
</div>
