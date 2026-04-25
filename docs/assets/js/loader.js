/* MühendisAl JS loader — Aşama 5: sayfa-spesifik lazy load
 *
 * mkdocs.yml extra_javascript artık yalnızca bu loader'ı yükler.
 * Loader sayfa yoluna ve DOM'a göre gerekli widget'ları sıralar.
 */
(function () {
  var path = location.pathname;
  var BASE = '/platform/assets/js/';

  function load(filename) {
    var s = document.createElement('script');
    s.src = BASE + filename;
    s.defer = true;
    document.body.appendChild(s);
  }

  // Her sayfa: api-client + progress (XP toplama her sayfada)
  load('api-client.js');
  load('progress.js');

  // Dashboard
  if (path.indexOf('/dashboard/') !== -1) {
    load('dashboard.js');
  }

  // Quiz: yol içinde 'quiz' ya da .ma-quiz DOM'da varsa
  if (path.indexOf('/quiz') !== -1 || document.querySelector('.ma-quiz')) {
    load('quiz.js');
  }

  // Kod editör: .ma-code-editor varsa
  if (document.querySelector('.ma-code-editor')) {
    load('code-editor.js');
  }

  // Ekosistem: bolum-1/03 veya /ekosistem/ yolu
  if (path.endsWith('/ekosistem/') || path.indexOf('bolum-1/03') !== -1) {
    load('ekosistem.js');
  }

  // Genel uygulama (her sayfa, en son)
  load('app.js');
})();
