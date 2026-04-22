/* MühendisAl — App entry (F6)
 * Global: window.MA.init()
 *
 * Sayfa yüklenince ve Material theme'in her sayfa geçişinde çalışır.
 * Akış:
 *   1. initAuth (token hazırla, backend'e kayıt)
 *   2. Başarılı → progress.init + quiz.init + code.init
 *   3. Başarısız → badge "offline", diğer modüller hala çalışır (offline-safe)
 */
(function () {
  "use strict";

  var _authDone = false;

  function runModules() {
    try { window.MA.progress && window.MA.progress.init(); } catch (e) { console.error("[MA] progress init fail:", e); }
    try { window.MA.quiz && window.MA.quiz.init(); } catch (e) { console.error("[MA] quiz init fail:", e); }
    try { window.MA.code && window.MA.code.init(); } catch (e) { console.error("[MA] code init fail:", e); }
    try { window.MA.dashboard && window.MA.dashboard.init(); } catch (e) { console.error("[MA] dashboard init fail:", e); }
  }

  function init() {
    if (!window.MA || !window.MA.api) {
      console.warn("[MA] api-client yüklenmemiş — init iptal");
      return;
    }

    // Auth sadece ilk yüklemede (token localStorage'da kalıcı)
    if (!_authDone) {
      window.MA.api.initAuth().then(function (user) {
        _authDone = true;
        console.log("[MA] auth OK — nick:", user && user.nick);
        runModules();
      }).catch(function (err) {
        console.warn("[MA] auth fail:", err.message);
        // Offline-safe: modülleri yine de başlat (badge 'offline' gösterir)
        runModules();
      });
    } else {
      runModules();
    }
  }

  window.MA = window.MA || {};
  window.MA.init = init;

  // --- Tetikleyiciler ---

  // 1. İlk yükleme
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // 2. Material theme'in navigation.instant'ı — her sayfa değişiminde tekrar init
  //    Material global olarak document$ observable'ı yayınlar (RxJS).
  //    window.document$ yoksa sessizce atlıyoruz (DOMContentLoaded yeterli).
  function hookMaterial() {
    if (typeof window.document$ !== "undefined" && window.document$ && typeof window.document$.subscribe === "function") {
      window.document$.subscribe(function () {
        // navigation.instant sayfa değiştirdiğinde auth zaten yapılmış, sadece modülleri çağır
        init();
      });
      return true;
    }
    return false;
  }

  if (!hookMaterial()) {
    // Material henüz yüklenmediyse biraz bekle, tekrar dene
    var tries = 0;
    var ivl = setInterval(function () {
      tries++;
      if (hookMaterial() || tries > 20) clearInterval(ivl);
    }, 250);
  }
})();
