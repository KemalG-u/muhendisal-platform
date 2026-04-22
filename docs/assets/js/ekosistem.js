/* MühendisAl — Ekosistem JS (v3 sablonu)
 *
 * Iki is yapar:
 *   1. Dis linkleri yeni sekmede ac (target=_blank + rel)
 *   2. Mermaid runtime'i yukle, sayfa gecisinde yeniden parse et
 *
 * MkDocs Material instant navigation ile uyumludur:
 *   document$ observable varsa subscribe; yoksa DOMContentLoaded.
 */
(function () {
  "use strict";

  var MERMAID_VERSION = "10.9.1";
  var MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@" + MERMAID_VERSION + "/dist/mermaid.min.js";
  var INTERNAL_HOSTS = ["wiki.oluk.org", "localhost", "127.0.0.1"];

  function isExternal(href) {
    if (!href) return false;
    if (href.indexOf("mailto:") === 0) return false;
    if (href.indexOf("tel:") === 0) return false;
    if (href.indexOf("#") === 0) return false;
    // Relative linkler — internal
    if (href.indexOf("http://") !== 0 && href.indexOf("https://") !== 0) return false;
    try {
      var u = new URL(href);
      return INTERNAL_HOSTS.indexOf(u.hostname) === -1;
    } catch (e) {
      return false;
    }
  }

  function markExternalLinks(root) {
    var links = (root || document).querySelectorAll("a[href]");
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (a.dataset.maExternalProcessed === "1") continue;
      if (isExternal(a.href)) {
        a.setAttribute("target", "_blank");
        // rel=noopener XSS guvenligi, noreferrer referrer sizintisi
        var existing = (a.getAttribute("rel") || "").split(/\s+/);
        ["noopener", "noreferrer", "external"].forEach(function (r) {
          if (existing.indexOf(r) === -1) existing.push(r);
        });
        a.setAttribute("rel", existing.filter(Boolean).join(" "));
        // Gorsel ipucu — CSS'te ↗ eklenir
        a.classList.add("ma-ext-link");
      }
      a.dataset.maExternalProcessed = "1";
    }
  }

  var mermaidLoaded = false;
  var mermaidLoading = null;

  function loadMermaid() {
    if (mermaidLoaded) return Promise.resolve();
    if (mermaidLoading) return mermaidLoading;
    mermaidLoading = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = MERMAID_URL;
      s.async = true;
      s.onload = function () {
        try {
          var isDark = document.body &&
            document.body.getAttribute("data-md-color-scheme") === "slate";
          window.mermaid.initialize({
            startOnLoad: false,
            theme: isDark ? "dark" : "default",
            securityLevel: "strict",
            flowchart: { htmlLabels: true, curve: "basis" }
          });
          mermaidLoaded = true;
          resolve();
        } catch (e) {
          reject(e);
        }
      };
      s.onerror = function () { reject(new Error("mermaid yuklenemedi")); };
      document.head.appendChild(s);
    });
    return mermaidLoading;
  }

  function renderMermaid(root) {
    root = root || document;
    var blocks = root.querySelectorAll("pre.mermaid, code.language-mermaid, .mermaid:not([data-processed])");
    if (!blocks.length) return;
    loadMermaid().then(function () {
      // Superfences html: <pre class="mermaid"><code>graph LR...</code></pre>
      // Once <pre> -> <div class="mermaid"> donustur, sonra mermaid'e ver.
      blocks.forEach(function (b) {
        if (b.dataset.maMermaidDone === "1") return;
        var source = b.textContent.trim();
        var host = document.createElement("div");
        host.className = "mermaid";
        host.textContent = source;
        b.parentNode.replaceChild(host, b);
        host.dataset.maMermaidDone = "1";
      });
      try {
        window.mermaid.run({ querySelector: ".mermaid:not([data-processed])" });
      } catch (e) {
        console.error("[MA] mermaid render fail:", e);
      }
    }).catch(function (e) {
      console.warn("[MA] mermaid yuklenemedi, diyagramlar metin olarak kalacak:", e);
    });
  }

  function initAll() {
    markExternalLinks(document);
    renderMermaid(document);
  }

  // Material instant navigation ile uyumlu initialize
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initAll);
  } else {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initAll);
    } else {
      initAll();
    }
  }

  // Dark mode toggle'da mermaid'i yeniden renderlamak icin theme degisimini izle
  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (m) {
      if (m.attributeName === "data-md-color-scheme" && mermaidLoaded) {
        var isDark = document.body.getAttribute("data-md-color-scheme") === "slate";
        try {
          window.mermaid.initialize({
            startOnLoad: false,
            theme: isDark ? "dark" : "default",
            securityLevel: "strict",
            flowchart: { htmlLabels: true, curve: "basis" }
          });
          // Rerender: tum mermaid blocklarinin data-processed attribute'unu sil
          document.querySelectorAll(".mermaid[data-processed]").forEach(function (el) {
            el.removeAttribute("data-processed");
            // Onceki render urettigi <svg>'yi temizle
            el.innerHTML = el.dataset.maOriginal || el.textContent;
          });
          window.mermaid.run({ querySelector: ".mermaid:not([data-processed])" });
        } catch (e) { console.warn("[MA] mermaid theme switch:", e); }
      }
    });
  });
  if (document.body) {
    observer.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }

  window.MA = window.MA || {};
  window.MA.ekosistem = { markExternalLinks: markExternalLinks, renderMermaid: renderMermaid };
})();
