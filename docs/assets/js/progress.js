/* MühendisAl — Progress (F6 + F7 dark-mode cila)
 * Global: window.MA.progress
 *
 * Görevler:
 *   1. Sayfa açılınca otomatik markSeen (bir kere)
 *   2. Sayfanın altına "Tamamlandım (+10 XP)" butonu (id=ma-complete-wrap)
 *   3. Sağ üstte XP + streak pill badge (id=ma-badge)
 *
 * Stil custom.css'te — JS sadece DOM oluşturur, class toggle eder.
 */
(function () {
  "use strict";

  if (!window.MA || !window.MA.api) {
    console.warn("[MA.progress] api-client yüklenmemiş");
    return;
  }

  var api = window.MA.api;

  // --- Yardımcılar ---

  // URL → normalize page_path. Ör: /platform/bolum-0/01-vps-linux/ → bolum-0/01-vps-linux
  function currentPagePath() {
    var p = window.location.pathname || "";
    p = p.replace(/^\/platform\/?/, "");
    p = p.replace(/^\/+|\/+$/g, "");
    if (!p || p === "index") return "index";
    return p;
  }

  // Cache — aynı sayfada tekrar tekrar markSeen atmasın
  var _seenCache = {};

  function markSeenOnce(page_path) {
    if (_seenCache[page_path]) return Promise.resolve({ cached: true });
    _seenCache[page_path] = true;
    return api.markSeen(page_path).catch(function (err) {
      _seenCache[page_path] = false;
      console.warn("[MA.progress] markSeen fail:", err.message);
    });
  }

  // --- Tamamla butonu ---

  function renderCompleteButton(page_path) {
    // navigation.instant ile sayfa değişiminde eski wrap kalabilir — kaldır
    var existing = document.getElementById("ma-complete-wrap");
    if (existing) existing.parentNode.removeChild(existing);

    var host = document.querySelector(".md-content__inner") || document.querySelector("article") || document.body;
    if (!host) return;

    var wrap = document.createElement("div");
    wrap.id = "ma-complete-wrap";

    var btn = document.createElement("button");
    btn.id = "ma-complete-btn";
    btn.type = "button";
    btn.textContent = "✓ Bu sayfayı tamamladım (+10 XP)";

    btn.addEventListener("click", function () {
      btn.disabled = true;
      btn.textContent = "İşleniyor...";
      api.markComplete(page_path).then(function (res) {
        btn.classList.add("ma-complete-done");
        var xp = res && typeof res.xp_awarded !== "undefined" ? " (+" + res.xp_awarded + " XP)" : "";
        btn.textContent = "✅ Tamamlandı!" + xp;
        refreshBadge();
      }).catch(function (err) {
        btn.disabled = false;
        btn.classList.add("ma-complete-error");
        btn.textContent = "❌ Hata — tekrar dene";
        console.error("[MA.progress] markComplete fail:", err);
      });
    });

    wrap.appendChild(btn);

    var hint = document.createElement("div");
    hint.className = "ma-complete-hint";
    hint.textContent = "Sayfa: " + page_path;
    wrap.appendChild(hint);

    host.appendChild(wrap);
  }

  // --- XP + Streak pill badge ---

  function renderBadge() {
    var badge = document.getElementById("ma-badge");
    if (badge) return badge;
    badge = document.createElement("div");
    badge.id = "ma-badge";
    badge.textContent = "⏳ yükleniyor...";
    document.body.appendChild(badge);
    return badge;
  }

  function refreshBadge() {
    var badge = renderBadge();
    api.getStreak().then(function (s) {
      var xp = (s && s.total_xp) || 0;
      var streak = (s && s.current_streak) || 0;
      badge.textContent = "🔥 " + streak + " gün · " + xp + " XP";
    }).catch(function (err) {
      badge.textContent = "⚠ offline";
      console.warn("[MA.progress] badge fail:", err.message);
    });
  }

  // --- Ana init (her sayfa yüklemesinde çağrılır) ---

  function init() {
    var page_path = currentPagePath();

    if (page_path === "index") {
      refreshBadge();
      return;
    }

    markSeenOnce(page_path);
    renderCompleteButton(page_path);
    refreshBadge();
  }

  window.MA = window.MA || {};
  window.MA.progress = {
    init: init,
    currentPagePath: currentPagePath,
    refreshBadge: refreshBadge,
    _seenCache: _seenCache,
  };
})();
