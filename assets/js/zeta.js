/* Zeta AI — Xitorque website chatbot widget. No dependencies.
   The endpoint (our Cloudflare Worker) is set by build.py via data-endpoint. */
(function () {
  'use strict';
  var script = document.currentScript || document.querySelector('script[data-zeta]');
  var ENDPOINT = script && script.getAttribute('data-endpoint');
  if (!ENDPOINT) return;

  var WA = 'https://wa.me/923402075073';
  var GREETING = 'Assalam o alaikum! 👋 Main Zeta AI hoon, Xitorque ki assistant. Ask me anything about our apps, services or pricing — English ya Urdu, dono chalein gi.';
  var SUGGEST = ['What does Xitorque build?', 'Tijarat kya hai?', 'ISP Suite ke baare mein batao', 'How do I get a quote?'];

  /* ---------- styles ---------- */
  var css = [
    ':root{--zt-g1:#6d28d9;--zt-g2:#a855f7;--zt-g3:#22d3ee}',
    '.zt-launch{position:fixed;right:18px;bottom:88px;z-index:9998;display:flex;align-items:center;gap:8px;padding:12px 18px;border:0;border-radius:999px;cursor:pointer;font:700 15px/1 Inter,system-ui,sans-serif;color:#fff;background:linear-gradient(135deg,var(--zt-g1),var(--zt-g2));box-shadow:0 10px 32px rgba(109,40,217,.5)}',
    '.zt-launch svg{width:18px;height:18px}',
    '.zt-panel{position:fixed;right:18px;bottom:88px;z-index:9999;width:min(380px,calc(100vw - 24px));height:min(560px,calc(100vh - 110px));display:none;flex-direction:column;border-radius:18px;overflow:hidden;background:#13111f;color:#eceaf6;border:1px solid rgba(168,85,247,.35);box-shadow:0 24px 70px rgba(0,0,0,.55);font-family:Inter,system-ui,sans-serif}',
    '.zt-panel.open{display:flex}',
    'html[data-theme="light"] .zt-panel{background:#fff;color:#1b1830;border-color:rgba(109,40,217,.25);box-shadow:0 24px 70px rgba(40,20,90,.22)}',
    '.zt-head{display:flex;align-items:center;gap:10px;padding:12px 14px;background:linear-gradient(135deg,var(--zt-g1),var(--zt-g2));color:#fff}',
    '.zt-head .zt-mark{width:34px;height:34px;border-radius:10px;background:rgba(255,255,255,.18);display:grid;place-items:center;font-weight:800;font-size:18px}',
    '.zt-head b{font-size:15px;display:block}.zt-head small{font-size:11px;opacity:.85}',
    '.zt-close{margin-left:auto;background:rgba(255,255,255,.15);border:0;color:#fff;width:30px;height:30px;border-radius:8px;cursor:pointer;font-size:15px;line-height:1}',
    '.zt-body{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}',
    '.zt-msg{max-width:85%;padding:9px 13px;border-radius:14px;font-size:13.5px;line-height:1.5;white-space:pre-wrap;word-break:break-word}',
    '.zt-msg a{color:var(--zt-g3);text-decoration:underline}',
    '.zt-bot{align-self:flex-start;background:rgba(168,85,247,.14);border:1px solid rgba(168,85,247,.22);border-bottom-left-radius:4px}',
    'html[data-theme="light"] .zt-bot{background:#f3edfd;border-color:#e4d7fb}',
    '.zt-user{align-self:flex-end;background:linear-gradient(135deg,var(--zt-g1),var(--zt-g2));color:#fff;border-bottom-right-radius:4px}',
    '.zt-sug{display:flex;flex-wrap:wrap;gap:6px}',
    '.zt-sug button{border:1px solid rgba(168,85,247,.45);background:transparent;color:inherit;border-radius:999px;padding:6px 11px;font-size:12px;cursor:pointer}',
    '.zt-typing span{display:inline-block;width:6px;height:6px;margin:0 2px;border-radius:50%;background:var(--zt-g2);animation:ztb 1s infinite}',
    '.zt-typing span:nth-child(2){animation-delay:.15s}.zt-typing span:nth-child(3){animation-delay:.3s}',
    '@keyframes ztb{0%,100%{opacity:.25;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}',
    '.zt-foot{display:flex;gap:8px;padding:10px;border-top:1px solid rgba(168,85,247,.18)}',
    '.zt-foot input{flex:1;min-width:0;background:rgba(168,85,247,.08);border:1px solid rgba(168,85,247,.3);border-radius:12px;padding:10px 12px;color:inherit;font-size:13.5px;outline:none}',
    '.zt-foot input:focus{border-color:var(--zt-g2)}',
    '.zt-send{border:0;border-radius:12px;width:42px;cursor:pointer;background:linear-gradient(135deg,var(--zt-g1),var(--zt-g2));color:#fff;display:grid;place-items:center}',
    '.zt-send:disabled{opacity:.5;cursor:default}',
    '.zt-note{text-align:center;font-size:10.5px;opacity:.55;padding:0 10px 8px}',
    '@media (max-width:480px){.zt-panel{right:8px;bottom:8px;height:min(560px,calc(100vh - 16px))}.zt-launch{bottom:84px}}'
  ].join('');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* ---------- markup ---------- */
  var XI = 'ξ';
  var launch = document.createElement('button');
  launch.className = 'zt-launch'; launch.type = 'button';
  launch.setAttribute('aria-label', 'Chat with Zeta AI');
  launch.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3l1.8 4.6L18 9l-4.2 1.4L12 15l-1.8-4.6L6 9l4.2-1.4z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/></svg><span>Zeta AI</span>';

  var panel = document.createElement('div');
  panel.className = 'zt-panel';
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Zeta AI chat');
  panel.innerHTML =
    '<div class="zt-head"><span class="zt-mark">' + XI + '</span><div><b>Zeta AI</b><small>Xitorque assistant · online</small></div><button class="zt-close" type="button" aria-label="Close chat">✕</button></div>' +
    '<div class="zt-body"></div>' +
    '<form class="zt-foot"><input type="text" maxlength="600" placeholder="Type your question…" aria-label="Your message"><button class="zt-send" type="submit" aria-label="Send"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg></button></form>' +
    '<div class="zt-note">Zeta AI can make mistakes. For quotes, use WhatsApp.</div>';
  document.body.appendChild(launch); document.body.appendChild(panel);

  var body = panel.querySelector('.zt-body');
  var form = panel.querySelector('form');
  var input = panel.querySelector('input');
  var send = panel.querySelector('.zt-send');

  /* ---------- history ---------- */
  var hist = [];
  try { hist = JSON.parse(sessionStorage.getItem('zt-hist') || '[]'); } catch (e) {}
  function remember() { try { sessionStorage.setItem('zt-hist', JSON.stringify(hist.slice(-20))); } catch (e) {} }

  function render(text, cls) {
    var div = document.createElement('div');
    div.className = 'zt-msg ' + cls;
    function link(target, href, label) {
      var a = document.createElement('a');
      a.href = /^https?:\/\//.test(href) ? href : 'https://' + href;
      a.target = '_blank'; a.rel = 'noopener';
      a.textContent = (label || href).replace(/^https?:\/\//, '');
      target.appendChild(a);
    }
    function plain(target, s) { // **bold** + bare URLs, everything else as text
      s.split(/\*\*([^*]+)\*\*/g).forEach(function (b, j) {
        if (!b) return;
        var host = j % 2 ? document.createElement('strong') : target;
        b.split(/(https?:\/\/[^\s<>")]+)/g).forEach(function (p, i) {
          if (!p) return;
          if (i % 2) link(host, p); else host.appendChild(document.createTextNode(p));
        });
        if (j % 2) target.appendChild(host);
      });
    }
    // markdown links [label](url) first, then the rest
    var md = String(text).split(/\[([^\]\n]+)\]\(\s*((?:https?:\/\/)?[^\s)]+?)\s*\)/g);
    for (var i = 0; i < md.length; i++) {
      if (i % 3 === 0) { if (md[i]) plain(div, md[i]); }
      else if (i % 3 === 1) { link(div, md[i + 1], md[i]); i++; }
    }
    body.appendChild(div); body.scrollTop = body.scrollHeight;
    return div;
  }

  function suggestions() {
    var wrap = document.createElement('div'); wrap.className = 'zt-sug';
    SUGGEST.forEach(function (q) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = q;
      b.addEventListener('click', function () { wrap.remove(); ask(q); });
      wrap.appendChild(b);
    });
    body.appendChild(wrap); body.scrollTop = body.scrollHeight;
  }

  var busy = false;
  function ask(text) {
    if (busy || !text.trim()) return;
    text = text.trim().slice(0, 600);
    render(text, 'zt-user');
    hist.push({ role: 'user', text: text }); remember();
    busy = true; send.disabled = true;
    var t = document.createElement('div'); t.className = 'zt-msg zt-bot zt-typing';
    t.innerHTML = '<span></span><span></span><span></span>';
    body.appendChild(t); body.scrollTop = body.scrollHeight;

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: hist.slice(-12) })
    }).then(function (r) { return r.json(); }).then(function (d) {
      t.remove();
      var out = (d && d.reply) ? d.reply : 'Kuch masla aa gaya. WhatsApp par rabta karein: ' + WA;
      render(out, 'zt-bot');
      hist.push({ role: 'model', text: out }); remember();
    }).catch(function () {
      t.remove();
      render('Network issue — thori der baad koshish karein, ya WhatsApp karein: ' + WA, 'zt-bot');
    }).finally(function () { busy = false; send.disabled = false; input.focus(); });
  }

  function open() {
    panel.classList.add('open'); launch.style.display = 'none';
    if (!body.childElementCount) {
      if (hist.length) hist.forEach(function (m) { render(m.text, m.role === 'user' ? 'zt-user' : 'zt-bot'); });
      else { render(GREETING, 'zt-bot'); suggestions(); }
    }
    input.focus();
  }
  function close() { panel.classList.remove('open'); launch.style.display = ''; }

  launch.addEventListener('click', open);
  panel.querySelector('.zt-close').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); var v = input.value; input.value = ''; ask(v); });
})();
