/* Xitorque Solutions — site behaviour. No dependencies. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  root.classList.add('js');

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }

  /* ---------- theme ---------- */
  var themeBtn = doc.getElementById('themeBtn');
  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    if (themeBtn) {
      themeBtn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      themeBtn.setAttribute('aria-pressed', t === 'light' ? 'true' : 'false');
    }
    var m = doc.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', t === 'dark' ? '#0a0a12' : '#f7f6fc');
  }
  applyTheme(root.getAttribute('data-theme') || 'dark');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next); store('xt-theme', next);
  });

  /* ---------- mobile menu ---------- */
  var menuBtn = doc.getElementById('menuBtn'), nav = doc.getElementById('nav');
  function setMenu(open) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !e.target.closest('.site-header')) setMenu(false);
    });
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = [].slice.call(doc.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el, i) { el.style.setProperty('--d', (i % 4) * 70 + 'ms'); io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- count-up numbers ---------- */
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  [].forEach.call(doc.querySelectorAll('[data-count]'), function (el) {
    var target = parseInt(el.getAttribute('data-count'), 10), suffix = el.getAttribute('data-suffix') || '';
    if (reduce || !('IntersectionObserver' in window) || isNaN(target)) { el.textContent = target + suffix; return; }
    var seen = new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting) return; seen.disconnect();
      var t0 = null, dur = 900;
      (function step(t) {
        if (t0 === null) t0 = t;
        var p = Math.min((t - t0) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + (p === 1 ? suffix : '');
        if (p < 1) requestAnimationFrame(step);
      })(performance.now());
    });
    seen.observe(el);
  });

  /* ---------- work / studio filters ---------- */
  [].forEach.call(doc.querySelectorAll('[data-filter-root]'), function (rootEl) {
    var cards = [].slice.call(rootEl.querySelectorAll('[data-cat]'));
    var buttons = [].slice.call(rootEl.querySelectorAll('[data-filter]'));
    var search = rootEl.querySelector('.search');
    var empty = rootEl.querySelector('.empty');
    var active = 'all';
    function run() {
      var q = search ? search.value.trim().toLowerCase() : '', shown = 0;
      cards.forEach(function (c) {
        var okCat = active === 'all' || c.getAttribute('data-cat') === active;
        var okQ = !q || (c.getAttribute('data-search') || '').indexOf(q) > -1;
        var show = okCat && okQ; c.hidden = !show; if (show) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        active = b.getAttribute('data-filter');
        buttons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        run();
      });
    });
    if (search) search.addEventListener('input', run);
  });

  /* ---------- install modal ---------- */
  var dlg = doc.getElementById('installDlg');
  function platform() {
    var ua = navigator.userAgent || '';
    if (/iPhone|iPad|iPod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) return 'ios';
    if (/Android/i.test(ua)) return 'android';
    return 'desktop';
  }
  var STEPS = {
    android: [
      ['1. Open the app', 'Tap “Open app” below. It opens in Chrome.'],
      ['2. Tap the ⋮ menu', 'In Chrome’s top-right corner.'],
      ['3. Choose “Install app”', 'Some phones say “Add to Home screen”. Confirm, and the icon appears on your home screen.']
    ],
    ios: [
      ['1. Open the app in Safari', 'Tap “Open app” below. Installing only works from Safari on iPhone and iPad.'],
      ['2. Tap the Share button', 'The square with an arrow, at the bottom of the screen.'],
      ['3. Choose “Add to Home Screen”', 'Tap Add. The app now opens full-screen like any other.']
    ],
    desktop: [
      ['1. Open the app', 'Click “Open app” below. It opens in a new tab.'],
      ['2. Click the install icon', 'In Chrome or Edge it sits at the right end of the address bar (a small screen with a down-arrow).'],
      ['3. Click Install', 'The app gets its own window and a shortcut on your computer.']
    ]
  };
  function addInstallFlag(url) { return url + (url.indexOf('?') > -1 ? '&' : '?') + 'install=1'; }
  function openInstall(btn) {
    if (!dlg || !dlg.showModal) { window.open(btn.getAttribute('data-url') || btn.getAttribute('data-apk'), '_blank', 'noopener'); return; }
    var name = btn.getAttribute('data-name'), url = btn.getAttribute('data-url'), apk = btn.getAttribute('data-apk');
    var kind = btn.getAttribute('data-kind');
    dlg.querySelector('[data-i="name"]').textContent = 'Install ' + name;
    var p = platform(), html = '';
    if (kind === 'apk') {
      html = '<div><b>Android</b><span>Download the APK, open it, and allow “Install unknown apps” for your browser if Android asks. No store account needed.</span></div>' +
             '<div><b>Not on Android?</b><span>Ask us for a web version or a build for your device.</span></div>';
    } else {
      html = (STEPS[p] || STEPS.desktop).map(function (s) { return '<div><b>' + s[0] + '</b><span>' + s[1] + '</span></div>'; }).join('');
    }
    dlg.querySelector('[data-i="steps"]').innerHTML = html;
    var actions = dlg.querySelector('[data-i="actions"]');
    actions.innerHTML = '';
    function link(href, label, cls) {
      var a = doc.createElement('a'); a.href = href; a.target = '_blank'; a.rel = 'noopener';
      a.className = 'btn ' + cls; a.textContent = label; actions.appendChild(a);
    }
    if (kind === 'apk' && apk) link(apk, 'Download APK', 'btn--primary');
    if (url) link(kind === 'pwa' ? addInstallFlag(url) : url, 'Open app', 'btn--primary');
    var close = doc.createElement('button'); close.type = 'button'; close.className = 'btn btn--ghost'; close.textContent = 'Close';
    close.addEventListener('click', function () { dlg.close(); }); actions.appendChild(close);
    dlg.showModal();
  }
  [].forEach.call(doc.querySelectorAll('[data-install]'), function (b) { b.addEventListener('click', function () { openInstall(b); }); });
  if (dlg) {
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    var x = dlg.querySelector('[data-i="close"]'); if (x) x.addEventListener('click', function () { dlg.close(); });
  }

  /* ---------- contact form -> WhatsApp / email (no backend) ---------- */
  var form = doc.getElementById('contactForm');
  if (form) {
    var qs = new URLSearchParams(location.search);
    var sel = form.querySelector('[name="service"]');
    var wanted = qs.get('service');
    if (sel && wanted) { for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === wanted) sel.selectedIndex = i; }
    var msg = form.querySelector('[name="message"]');
    if (msg && qs.get('about') && !msg.value) msg.value = 'I’m interested in: ' + qs.get('about') + '.\n';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var svc = sel && sel.selectedIndex > -1 ? sel.options[sel.selectedIndex].text : 'Not sure yet';
      var text = 'Hi Xitorque! I’m ' + (f.get('name') || '') + '.\nService: ' + svc +
        '\n\n' + (f.get('message') || '') + (f.get('reply') ? '\n\nReach me at: ' + f.get('reply') : '');
      var wa = form.getAttribute('data-wa'), mail = form.getAttribute('data-mail');
      if (wa) window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
      else if (mail) location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent('Project enquiry: ' + svc) + '&body=' + encodeURIComponent(text);
      else {
        var fb = form.getAttribute('data-fallback');
        if (navigator.clipboard) { try { navigator.clipboard.writeText(text); } catch (err) {} }
        if (fb) window.open(fb, '_blank', 'noopener');
      }
    });
  }

  /* ---------- footer year + service worker ---------- */
  [].forEach.call(doc.querySelectorAll('[data-year]'), function (el) { el.textContent = new Date().getFullYear(); });
  if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }
})();
