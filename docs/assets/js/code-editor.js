/* MühendisAl — Code editor (F9: Pyodide entegrasyonu)
 * Global: window.MA.code
 *
 * Markdown formatı:
 *   <pre data-ma-run="python"><code>import os
 *   print(os.getcwd())
 *   </code></pre>
 *
 * Çalışma:
 *   1. Her blok için kod-üstüne bar (▶ Çalıştır + dil badge)
 *   2. Kod-altına output paneli
 *   3. İlk tıklamada Pyodide lazy-load (CDN ~6MB, promise cache)
 *   4. stdout/stderr batched yakalar, output paneline yazar
 *   5. Exception → kırmızı panel
 *
 * Tek Pyodide instance — aynı sayfadaki tüm bloklar paylaşır (global state korunur).
 */
(function () {
  "use strict";

  var PYODIDE_VERSION = "v0.29.3";
  var PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/" + PYODIDE_VERSION + "/full/";
  var PYODIDE_SCRIPT = PYODIDE_BASE + "pyodide.js";

  var _pyodidePromise = null;   // cache
  var _runningLock = false;     // aynı anda iki çalışma yok

  function loadPyodideOnce() {
    if (_pyodidePromise) return _pyodidePromise;
    _pyodidePromise = new Promise(function (resolve, reject) {
      // Script zaten DOM'da mı
      if (typeof window.loadPyodide === "function") {
        window.loadPyodide({ indexURL: PYODIDE_BASE }).then(resolve, reject);
        return;
      }
      var script = document.createElement("script");
      script.src = PYODIDE_SCRIPT;
      script.async = true;
      script.onload = function () {
        if (typeof window.loadPyodide !== "function") {
          reject(new Error("loadPyodide global bulunamadı"));
          return;
        }
        window.loadPyodide({ indexURL: PYODIDE_BASE }).then(resolve, reject);
      };
      script.onerror = function () {
        reject(new Error("Pyodide script yüklenemedi (ağ / CDN)"));
      };
      document.head.appendChild(script);
    });
    return _pyodidePromise;
  }

  function getCodeFromPre(pre) {
    var code = pre.querySelector("code");
    // textContent — HTML entity'leri decode edilmiş hali, pymdownx highlight yoksa raw metin
    return (code ? code.textContent : pre.textContent) || "";
  }

  function ensureOutput(pre) {
    var existing = pre.nextElementSibling;
    if (existing && existing.classList && existing.classList.contains("ma-code-output")) {
      return existing;
    }
    var out = document.createElement("div");
    out.className = "ma-code-output";
    out.style.display = "none";
    pre.parentNode.insertBefore(out, pre.nextSibling);
    return out;
  }

  function setOutput(outEl, text, isError) {
    outEl.style.display = "";
    outEl.classList.toggle("ma-code-error", !!isError);
    outEl.classList.toggle("ma-code-loading", false);
    outEl.textContent = text;
  }

  function setLoading(outEl, text) {
    outEl.style.display = "";
    outEl.classList.remove("ma-code-error");
    outEl.classList.add("ma-code-loading");
    outEl.textContent = text;
  }

  function runPython(pre, btn) {
    if (_runningLock) {
      // Aynı anda başka blok çalışıyor
      return;
    }
    _runningLock = true;

    var code = getCodeFromPre(pre);
    var outEl = ensureOutput(pre);
    btn.disabled = true;
    var origLabel = btn.textContent;
    btn.textContent = "⏳ Yükleniyor...";
    setLoading(outEl, "⏳ Pyodide yükleniyor (ilk seferde ~6MB, birkaç saniye)...");

    loadPyodideOnce().then(function (pyodide) {
      btn.textContent = "▶ Çalışıyor...";
      setLoading(outEl, "▶ Çalışıyor...");

      var buf = [];
      // Pyodide 0.24+: setStdout({batched})
      try {
        pyodide.setStdout({ batched: function (s) { buf.push(s); } });
        pyodide.setStderr({ batched: function (s) { buf.push(s); } });
      } catch (e) {
        // eski API fallback — ignore
      }

      return pyodide.runPythonAsync(code).then(function (result) {
        // batched callback'in birikimi yakalanması için micro delay
        return new Promise(function (r) {
          setTimeout(function () {
            var out = buf.join("");
            // Eğer son ifadenin bir dönüşü varsa ekle
            if (result !== undefined && result !== null) {
              var rstr;
              try { rstr = result.toString(); } catch (e) { rstr = "<repr hata>"; }
              if (!out.endsWith("\n") && out) out += "\n";
              out += "⤷ " + rstr;
              // Proxy belleği serbest bırak
              if (result.destroy) try { result.destroy(); } catch (e) {}
            }
            setOutput(outEl, out || "(çıktı yok)", false);
            r();
          }, 30);
        });
      }).catch(function (err) {
        var msg = (err && err.message) ? err.message : String(err);
        // Pyodide Python hatası PythonError mesajında traceback var
        setOutput(outEl, msg, true);
      });
    }).catch(function (err) {
      setOutput(outEl, "⚠ Pyodide yüklenemedi: " + ((err && err.message) || String(err)), true);
    }).then(function () {
      btn.disabled = false;
      btn.textContent = origLabel;
      _runningLock = false;
    });
  }

  function bindBlock(pre) {
    if (pre.dataset.maCodeBound === "1") return;
    pre.dataset.maCodeBound = "1";

    var lang = pre.getAttribute("data-ma-run") || "python";

    var bar = document.createElement("div");
    bar.className = "ma-code-bar";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ma-code-run";
    btn.textContent = "▶ Çalıştır";

    if (lang !== "python") {
      btn.title = lang + " için çalıştırma henüz desteklenmiyor";
      btn.addEventListener("click", function () {
        var out = ensureOutput(pre);
        setOutput(out, "⚠ Şu an sadece Python (Pyodide) destekleniyor. Dil: " + lang, true);
      });
    } else {
      btn.title = "Pyodide ile tarayıcıda çalıştır (timeout yok — sonsuz döngüden kaçının)";
      btn.addEventListener("click", function () { runPython(pre, btn); });
    }

    var badge = document.createElement("span");
    badge.className = "ma-code-lang";
    badge.textContent = lang;

    bar.appendChild(btn);
    bar.appendChild(badge);
    pre.parentNode.insertBefore(bar, pre);
  }

  function init() {
    var blocks = document.querySelectorAll("pre[data-ma-run]");
    if (!blocks.length) return;
    Array.prototype.forEach.call(blocks, bindBlock);
  }

  window.MA = window.MA || {};
  window.MA.code = {
    init: init,
    _loadPyodideOnce: loadPyodideOnce,
    _pyodideVersion: PYODIDE_VERSION,
  };
})();
