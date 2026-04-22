/* MühendisAl — Dashboard (F8)
 * Global: window.MA.dashboard
 *
 * Görevler:
 *   1. Target tab'lar (hbv/kisisel/is/hepsi) — tıklayınca PATCH /me
 *   2. 4 kart: toplam XP, streak, tamamlanan sayfa sayısı, ortalama quiz doğruluk
 *   3. Son 10 quiz denemesi listesi
 *   4. Progress listesi: her .ma-pg-row için ○ / 👁 / ✓ status ikonu
 *
 * Sadece /platform/dashboard/ sayfasında çalışır (page guard).
 */
(function () {
  "use strict";

  if (!window.MA || !window.MA.api) return;
  var api = window.MA.api;

  // Dashboard sayfasında mıyız?
  function isDashboardPage() {
    // .ma-target-tabs varsa dashboard'dayız — DOM-based guard navigation.instant uyumlu
    return !!document.querySelector(".ma-target-tabs");
  }

  // --- Target tab ---

  function setupTargetTabs(currentTarget) {
    var tabs = document.querySelectorAll(".ma-target-tab");
    Array.prototype.forEach.call(tabs, function (tab) {
      if (tab.dataset.maBound === "1") return;
      tab.dataset.maBound = "1";

      if (tab.getAttribute("data-target") === currentTarget) {
        tab.classList.add("ma-target-active");
      }

      tab.addEventListener("click", function () {
        var newTarget = tab.getAttribute("data-target");
        // UI optimistic update
        Array.prototype.forEach.call(tabs, function (t) { t.classList.remove("ma-target-active"); });
        tab.classList.add("ma-target-active");
        tab.disabled = true;
        api.updateMe({ target: newTarget }).then(function () {
          tab.disabled = false;
        }).catch(function (err) {
          tab.disabled = false;
          // Rollback
          tabs.forEach(function (t) {
            if (t.getAttribute("data-target") === currentTarget) t.classList.add("ma-target-active");
            else t.classList.remove("ma-target-active");
          });
          console.warn("[MA.dashboard] target update fail:", err.message);
        });
      });
    });
  }

  // --- Kartlar ---

  function renderCards(streak, progressRows) {
    var xpEl = document.getElementById("ma-dash-xp");
    var stEl = document.getElementById("ma-dash-streak");
    var doneEl = document.getElementById("ma-dash-done");
    var accEl = document.getElementById("ma-dash-acc");

    if (xpEl) xpEl.textContent = (streak && streak.total_xp) || 0;
    if (stEl) stEl.textContent = "🔥 " + ((streak && streak.current_streak) || 0);

    var completed = 0;
    if (Array.isArray(progressRows)) {
      progressRows.forEach(function (p) {
        if (p.status === "completed") completed++;
      });
    }
    if (doneEl) doneEl.textContent = completed;

    // Doğruluk: son 10 quiz'den ortalama — dashboardQuiz'de set edilecek
    if (accEl) accEl.textContent = "—";
  }

  // --- Son quiz kartı ---

  function renderRecentQuiz(attempts) {
    var host = document.getElementById("ma-dash-quiz");
    if (!host) return;

    if (!Array.isArray(attempts) || attempts.length === 0) {
      host.innerHTML = '<em>Henüz quiz çözmedin. Bölümlere dal ve +5 XP kazan.</em>';
      // Doğruluk "—" bırak
      return;
    }

    // Doğruluk hesapla
    var correct = 0;
    attempts.forEach(function (a) { if (a.is_correct) correct++; });
    var acc = attempts.length ? Math.round((correct / attempts.length) * 100) : 0;
    var accEl = document.getElementById("ma-dash-acc");
    if (accEl) accEl.textContent = acc + "%";

    var rows = attempts.map(function (a) {
      var icon = a.is_correct ? "✅" : "❌";
      var date = new Date(a.attempted_at);
      var when = isNaN(date.getTime()) ? a.attempted_at : (
        date.toLocaleDateString("tr-TR") + " " + date.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" })
      );
      return (
        '<div class="ma-quiz-row">' +
          '<span class="ma-qr-icon">' + icon + '</span>' +
          '<span class="ma-qr-id">' + escapeHtml(a.quiz_id) + '</span>' +
          '<span class="ma-qr-page">' + escapeHtml(a.page_path) + '</span>' +
          '<span class="ma-qr-when">' + when + '</span>' +
        '</div>'
      );
    }).join("");
    host.innerHTML = rows;
  }

  function escapeHtml(s) {
    if (s == null) return "";
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // --- Heatmap + bugün banner (F10) ---

  // XP miktarına göre yoğunluk bucket'i: l0 (boş) → l4 (yoğun)
  function xpBucket(xp) {
    if (!xp || xp <= 0) return "l0";
    if (xp <= 5) return "l1";
    if (xp <= 15) return "l2";
    if (xp <= 30) return "l3";
    return "l4";
  }

  function renderHeatmap(daily) {
    var host = document.getElementById("ma-heatmap");
    if (!host) return;
    host.innerHTML = "";
    if (!Array.isArray(daily) || daily.length === 0) {
      host.innerHTML = '<em>Veri yok</em>';
      return;
    }
    daily.forEach(function (d) {
      var cell = document.createElement("div");
      cell.className = "ma-hm-cell ma-hm-" + xpBucket(d.total_xp);
      var dateObj = new Date(d.date + "T00:00:00");
      var gunStr = isNaN(dateObj.getTime()) ? d.date : dateObj.toLocaleDateString("tr-TR", { weekday: "short", day: "numeric", month: "short" });
      cell.title = gunStr + " · " + d.total_xp + " XP (" + d.quiz_count + " quiz, " + d.pages_completed + " sayfa)";
      // Minik gün baş harfi etiketi
      var letter = "";
      if (!isNaN(dateObj.getTime())) {
        letter = dateObj.toLocaleDateString("tr-TR", { weekday: "narrow" });
      }
      var lbl = document.createElement("span");
      lbl.className = "ma-hm-label";
      lbl.textContent = letter;
      cell.appendChild(lbl);
      host.appendChild(cell);
    });
  }

  function renderTodayBanner(daily, streak) {
    var host = document.getElementById("ma-today-banner");
    if (!host) return;
    var today = Array.isArray(daily) && daily.length ? daily[daily.length - 1] : null;
    var xp = today ? today.total_xp : 0;
    var quizN = today ? today.quiz_count : 0;
    var pagesN = today ? today.pages_completed : 0;
    var streakN = (streak && streak.current_streak) || 0;

    var emoji, msg;
    if (xp === 0) {
      emoji = "😴";
      msg = "Bugün henüz aktivite yok. Bir sayfaya uğra, streak'i koru!";
      host.classList.add("ma-today-quiet");
      host.classList.remove("ma-today-active", "ma-today-hot");
    } else if (xp < 15) {
      emoji = "🌱";
      msg = "İyi başlangıç — bugün " + xp + " XP. " + quizN + " quiz · " + pagesN + " sayfa.";
      host.classList.add("ma-today-active");
      host.classList.remove("ma-today-quiet", "ma-today-hot");
    } else {
      emoji = "🔥";
      msg = "Güzel tempo! Bugün " + xp + " XP. " + quizN + " quiz · " + pagesN + " sayfa.";
      host.classList.add("ma-today-hot");
      host.classList.remove("ma-today-quiet", "ma-today-active");
    }

    var streakStr = streakN > 0 ? ' · 🔥 <strong>' + streakN + ' gün</strong> streak' : "";
    host.innerHTML = '<span class="ma-today-emoji">' + emoji + '</span>' +
                     '<span class="ma-today-msg">' + escapeHtml(msg) + streakStr + '</span>';
  }

  // --- Progress liste ---

  function renderProgressList(progressRows) {
    // Backend'den gelen [{page_path, status, ...}, ...] — lookup map'e çevir
    var map = {};
    if (Array.isArray(progressRows)) {
      progressRows.forEach(function (p) { map[p.page_path] = p.status; });
    }

    var rows = document.querySelectorAll(".ma-pg-row");
    Array.prototype.forEach.call(rows, function (row) {
      var path = row.getAttribute("data-page-path");
      var iconEl = row.querySelector(".ma-pg-icon");
      if (!iconEl) return;

      // Reset class'ları (re-render)
      row.classList.remove("ma-pg-seen", "ma-pg-done");

      var status = map[path];
      if (status === "completed") {
        iconEl.textContent = "✓";
        row.classList.add("ma-pg-done");
      } else if (status === "started") {
        iconEl.textContent = "👁";
        row.classList.add("ma-pg-seen");
      } else {
        iconEl.textContent = "○";
      }
    });
  }

  // --- Ana init ---

  function init() {
    if (!isDashboardPage()) return;

    // Paralel: me + streak + progress + recent quiz
    Promise.all([
      api.getMe().catch(function (e) { return null; }),
      api.getStreak().catch(function (e) { return null; }),
      api.getProgress().catch(function (e) { return []; }),
      api.getRecentQuiz(10).catch(function (e) { return []; }),
      api.getDailyXP(7).catch(function (e) { return []; }),
    ]).then(function (results) {
      var user = results[0];
      var streak = results[1];
      var progress = results[2];
      var recentQuiz = results[3];
      var daily = results[4];

      setupTargetTabs(user && user.target ? user.target : "hepsi");
      renderTodayBanner(daily, streak);
      renderHeatmap(daily);
      renderCards(streak, progress);
      renderProgressList(progress);
      renderRecentQuiz(recentQuiz);
    });
  }

  window.MA = window.MA || {};
  window.MA.dashboard = {
    init: init,
    isDashboardPage: isDashboardPage,
  };
})();
