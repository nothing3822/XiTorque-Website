/*
 * Xitorque install helper — paste this ONCE into each of your own apps (before </body>).
 *
 * What it does: when someone arrives from the Xitorque website with ?install=1 in the link,
 * it catches the browser's install prompt and shows a clear "Install" button right away,
 * so people can install your app without hunting for the browser menu.
 *
 * It does nothing for normal visits, so it is safe to add to every app.
 */
(function () {
  var wantsInstall = /[?&]install=1\b/.test(location.search);
  var deferred = null;

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    if (wantsInstall) showButton();
  });

  function showButton() {
    if (document.getElementById('xt-install')) return;
    var b = document.createElement('button');
    b.id = 'xt-install';
    b.type = 'button';
    b.textContent = 'Install this app';
    b.style.cssText = 'position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:99999;' +
      'padding:14px 26px;border:0;border-radius:999px;font:700 16px system-ui,sans-serif;color:#fff;' +
      'background:linear-gradient(135deg,#6d28d9,#8b5cf6);box-shadow:0 12px 40px rgba(109,40,217,.55);cursor:pointer';
    b.onclick = function () {
      if (!deferred) return;
      deferred.prompt();
      deferred.userChoice.finally(function () { deferred = null; b.remove(); });
    };
    document.body.appendChild(b);
  }

  window.addEventListener('appinstalled', function () {
    var b = document.getElementById('xt-install');
    if (b) b.remove();
  });
})();
