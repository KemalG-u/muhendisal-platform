/* MühendisAl — API Client (F6)
 * Global: window.MA.api
 * Backend: https://wiki.oluk.org/platform/api
 *
 * Token akışı:
 *   - localStorage.ma_token varsa kullan
 *   - Yoksa crypto.randomUUID() üret + /api/auth/init çağır + sakla
 *   - Sonraki tüm isteklerde X-Token header
 */
(function () {
  "use strict";

  var LS_TOKEN = "ma_token";
  var LS_NICK = "ma_nick";

  // Base URL: override için window.MA_API_BASE, varsayılan /platform/api
  var API_BASE = (window.MA_API_BASE || "/platform/api").replace(/\/$/, "");

  function getToken() {
    return localStorage.getItem(LS_TOKEN);
  }

  function setToken(t) {
    localStorage.setItem(LS_TOKEN, t);
  }

  function makeUUID() {
    if (window.crypto && window.crypto.randomUUID) return window.crypto.randomUUID();
    // Fallback: basit rastgele
    return "ma-" + Date.now() + "-" + Math.random().toString(36).slice(2, 10);
  }

  // Merkezi fetch — X-Token, JSON parse, hata normalizasyonu
  function request(method, path, body) {
    var url = API_BASE + path;
    var headers = { "Content-Type": "application/json" };
    var token = getToken();
    if (token) headers["X-Token"] = token;

    var opts = { method: method, headers: headers };
    if (body !== undefined && body !== null) opts.body = JSON.stringify(body);

    return fetch(url, opts).then(function (res) {
      return res.text().then(function (text) {
        var data = null;
        try { data = text ? JSON.parse(text) : null; } catch (e) { data = { raw: text }; }
        if (!res.ok) {
          var err = new Error("API " + res.status + " " + (data && data.detail ? data.detail : res.statusText));
          err.status = res.status;
          err.data = data;
          throw err;
        }
        return data;
      });
    });
  }

  // ---- Auth ----
  function initAuth(nick) {
    var token = getToken();
    if (!token) {
      token = makeUUID();
      setToken(token);
    }
    var payload = { token: token };
    if (nick) payload.nick = nick;
    return request("POST", "/auth/init", payload).then(function (user) {
      if (user && user.nick) localStorage.setItem(LS_NICK, user.nick);
      return user;
    });
  }

  function getMe() {
    return request("GET", "/me");
  }

  function updateMe(patch) {
    // patch: { nick?, target? }
    return request("PATCH", "/me", patch);
  }

  // ---- Progress ----
  function markSeen(page_path) {
    return request("POST", "/progress/seen", { page_path: page_path });
  }

  function markComplete(page_path) {
    return request("POST", "/progress/complete", { page_path: page_path });
  }

  function getProgress() {
    return request("GET", "/progress");
  }

  // ---- Quiz ----
  function submitQuiz(page_path, quiz_id, selected, is_correct) {
    return request("POST", "/quiz/attempt", {
      page_path: page_path,
      quiz_id: quiz_id,
      selected: selected,
      is_correct: is_correct,
    });
  }

  function getQuizStats(page_path) {
    return request("GET", "/quiz/stats/" + encodeURIComponent(page_path));
  }

  function getRecentQuiz(limit) {
    var n = typeof limit === "number" && limit > 0 ? Math.min(limit, 50) : 10;
    return request("GET", "/quiz/recent?limit=" + n);
  }

  // ---- XP timeline (F10) ----
  function getDailyXP(days) {
    var n = typeof days === "number" && days > 0 ? Math.min(days, 90) : 7;
    return request("GET", "/xp/daily?days=" + n);
  }

  // ---- Streak ----
  function getStreak() {
    return request("GET", "/streak");
  }

  // ---- Feedback ----
  function postFeedback(page_path, message, type) {
    // Backend schema: {page_path?, type: question|bug|suggestion|note, message}
    var body = { message: message, type: type || "note" };
    if (page_path) body.page_path = page_path;
    return request("POST", "/feedback", body);
  }

  function getFeedback() {
    return request("GET", "/feedback");
  }

  // ---- Health (debug) ----
  function health() {
    return request("GET", "/health");
  }

  // Global namespace
  window.MA = window.MA || {};
  window.MA.api = {
    base: API_BASE,
    getToken: getToken,
    initAuth: initAuth,
    getMe: getMe,
    updateMe: updateMe,
    markSeen: markSeen,
    markComplete: markComplete,
    getProgress: getProgress,
    submitQuiz: submitQuiz,
    getQuizStats: getQuizStats,
    getRecentQuiz: getRecentQuiz,
    getDailyXP: getDailyXP,
    getStreak: getStreak,
    postFeedback: postFeedback,
    getFeedback: getFeedback,
    health: health,
    _request: request,
  };
})();
