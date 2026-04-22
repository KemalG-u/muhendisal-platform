/* MühendisAl — Quiz widget (F6 + F7 dark-mode cila)
 * Global: window.MA.quiz
 *
 * Markdown formatı:
 *   <div class="ma-quiz" data-quiz-id="b0-01-q1" data-correct="B">
 *     <p class="ma-quiz-q">Soru metni</p>
 *     <div class="ma-opt" data-key="A">A şıkkı</div>
 *     <div class="ma-opt" data-key="B">B şıkkı</div>
 *     <div class="ma-opt" data-key="C">C şıkkı</div>
 *   </div>
 *
 * Stil custom.css'te (.ma-quiz, .ma-opt, .ma-opt-correct vs.) — JS sadece class toggle eder.
 */
(function () {
  "use strict";

  if (!window.MA || !window.MA.api) {
    console.warn("[MA.quiz] api-client yüklenmemiş");
    return;
  }

  var api = window.MA.api;

  function currentPagePath() {
    if (window.MA.progress && window.MA.progress.currentPagePath) {
      return window.MA.progress.currentPagePath();
    }
    var p = (window.location.pathname || "").replace(/^\/platform\/?/, "").replace(/^\/+|\/+$/g, "");
    return p || "index";
  }

  function bindQuiz(quiz) {
    if (quiz.dataset.maBound === "1") return;
    quiz.dataset.maBound = "1";

    var quizId = quiz.getAttribute("data-quiz-id") || "unknown";
    var correctKey = (quiz.getAttribute("data-correct") || "").trim().toUpperCase();
    var opts = quiz.querySelectorAll(".ma-opt");
    if (!opts.length) return;

    // Feedback container (her quiz için bir tane)
    var fb = document.createElement("div");
    fb.className = "ma-quiz-feedback";
    fb.style.display = "none";
    quiz.appendChild(fb);

    Array.prototype.forEach.call(opts, function (opt) {
      opt.addEventListener("click", function () {
        if (quiz.dataset.maAnswered === "1") return;
        onAnswer(quiz, opt, opts, quizId, correctKey, fb);
      });
    });
  }

  function onAnswer(quiz, chosen, allOpts, quizId, correctKey, fb) {
    quiz.dataset.maAnswered = "1";
    var selected = (chosen.getAttribute("data-key") || "").trim().toUpperCase();
    var isCorrect = selected === correctKey;

    // Class toggle — stil CSS'ten gelir
    Array.prototype.forEach.call(allOpts, function (o) {
      var k = (o.getAttribute("data-key") || "").trim().toUpperCase();
      if (k === correctKey) {
        o.classList.add("ma-opt-correct");
      } else if (o === chosen) {
        o.classList.add("ma-opt-wrong");
      } else {
        o.classList.add("ma-opt-disabled");
      }
    });

    // Feedback
    fb.style.display = "";
    fb.classList.remove("ma-fb-correct", "ma-fb-wrong");
    if (isCorrect) {
      fb.classList.add("ma-fb-correct");
      fb.textContent = "✅ Doğru! +5 XP";
    } else {
      fb.classList.add("ma-fb-wrong");
      fb.textContent = "❌ Yanlış. Doğru cevap: " + correctKey + " (+1 XP)";
    }

    // API submit + badge refresh
    var page_path = currentPagePath();
    api.submitQuiz(page_path, quizId, selected, isCorrect).then(function () {
      if (window.MA.progress && window.MA.progress.refreshBadge) {
        window.MA.progress.refreshBadge();
      }
    }).catch(function (err) {
      fb.textContent += " (⚠ API offline)";
      console.warn("[MA.quiz] submit fail:", err.message);
    });
  }

  function init() {
    var quizzes = document.querySelectorAll(".ma-quiz");
    if (!quizzes.length) return;
    Array.prototype.forEach.call(quizzes, bindQuiz);
  }

  window.MA = window.MA || {};
  window.MA.quiz = {
    init: init,
    _bindQuiz: bindQuiz,
  };
})();
