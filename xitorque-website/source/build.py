#!/usr/bin/env python3
"""
Xitorque website builder.

  1. Edit the files in  data/   (config.json, apps.json, services.json, products.json, team.json, faq.json)
  2. Run:  python build.py
  3. Upload everything inside the generated  ../site  folder to your GitHub Pages repo.

Needs only Python 3.8+. No packages to install.
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STATIC = ROOT / "static"
OUT = ROOT.parent / "site"
KEEP = {".git", "CNAME", ".nojekyll"}

def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)

CFG = load("config.json")
SERVICES = load("services.json")
APPS = load("apps.json")
PRODUCTS = load("products.json")
TEAM = load("team.json")
FAQ = load("faq.json")
LINKS = CFG.get("links", {})
DOMAIN = (CFG.get("custom_domain") or "").strip().strip("/")
SITE_URL = ("https://" + DOMAIN) if DOMAIN else CFG["site_url"].rstrip("/")
WA = re.sub(r"\D", "", CFG.get("whatsapp", ""))
EMAIL = CFG.get("email", "").strip()
BRAND = CFG["brand"]
TODAY = date.today().isoformat()

def e(s):
    return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ icons
ICONS = {
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/>',
    "store": '<path d="m3 9 1-5h16l1 5"/><path d="M4 9v11h16V9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20v-6h4v6"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V5"/><circle cx="12" cy="3.5" r="1.3"/><path d="M9 13.5h.01M15 13.5h.01M9.5 17h5"/>',
    "gamepad": '<path d="M6 11h4M8 9v4"/><path d="M15 12h.01M18 10h.01"/><path d="M17.3 5H6.7a4 4 0 0 0-3.9 3.2L1.5 15a3 3 0 0 0 5.2 2.4L8 16h8l1.3 1.4a3 3 0 0 0 5.2-2.4l-1.3-6.8A4 4 0 0 0 17.3 5z"/>',
    "video": '<rect x="2" y="5" width="14" height="14" rx="3"/><path d="m22 8-6 4 6 4z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "calc": '<rect x="4" y="2" width="16" height="20" rx="3"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h.01M12 19h.01M16 19h.01"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-5.4A8 8 0 1 1 21 12z"/>',
    "ledger": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 0 4 22.5z"/><path d="M4 19.5v-15M9 7h7M9 11h5"/>',
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "wifi": '<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0M12 20h.01"/>',
    "cake": '<path d="M4 20h16v-7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2z"/><path d="M4 16c2 1.5 4 1.5 8 0s6-1.5 8 0M12 11V8M12 4v1"/>',
    "rocket": '<path d="M5 15c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9s-2.2-.8-2.9-.1z"/><path d="m12 15-3-3a22 22 0 0 1 2-4A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22 22 0 0 1-4 2z"/><path d="M9 12H4s.6-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.6 4-2c1.1-1.6 0-5 0-5"/>',
    "swords": '<path d="M14.5 17.5 3 6V3h3l11.5 11.5M13 19l6-6M16 16l4 4M19 21l2-2"/><path d="M9.5 6.5 21 18v3h-3L6.5 9.5M5 11l6 6M8 8 4 4"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "snake": '<path d="M4 19c0-3 3-3 5-3s4 0 4-3-3-3-5-3-3-2-1-4c2-2 7-1 9 1"/><path d="M19 4h.01"/>',
    "bottle": '<path d="M9 2h6v3H9z"/><path d="M10 5v2a3 3 0 0 0-2 3v10a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V10a3 3 0 0 0-2-3V5"/><path d="M8 13h8"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9a3.4 3.4 0 0 0-.9-2.6c3.1-.3 6.4-1.5 6.4-6.9a5.4 5.4 0 0 0-1.5-3.8 5 5 0 0 0-.1-3.7s-1.2-.3-3.9 1.5a13.4 13.4 0 0 0-7 0C6.3 1.9 5.1 2.2 5.1 2.2a5 5 0 0 0-.1 3.7A5.4 5.4 0 0 0 3.5 9.7c0 5.4 3.3 6.6 6.4 6.9a3.4 3.4 0 0 0-.9 2.6V22"/>',
    "external": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "download": '<path d="M12 3v12m0 0-4-4m4 4 4-4M4 21h16"/>',
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "spark": '<path d="m12 3 1.9 5.5L19 10l-5.1 1.5L12 17l-1.9-5.5L5 10l5.1-1.5z"/><path d="M19 17v4M17 19h4"/>',
    "cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
}

def ic(name, cls=""):
    return '<span class="ico %s" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">%s</svg></span>' % (cls, ICONS.get(name, ICONS["spark"]))

# ------------------------------------------------------------------ helpers
def wa_url(text=None):
    if not WA:
        return ""
    return "https://wa.me/%s?text=%s" % (WA, quote(text or CFG["wa_default"]))

def contact_href(service=None, about=None):
    q = []
    if service:
        q.append("service=" + quote(service))
    if about:
        q.append("about=" + quote(about))
    return "contact.html" + ("?" + "&".join(q) if q else "")

def price_html(price):
    cur = CFG.get("currency", "PKR")
    if price in ("", None):
        return '<div class="price"><small>Pricing</small>Custom quote</div>'
    if isinstance(price, (int, float)):
        price = "{:,}".format(price)
    return '<div class="price"><small>Starting from</small>%s %s</div>' % (e(cur), e(price))

def ext(url, label, cls="btn btn--ghost btn--sm", icon="external"):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s%s</a>' % (cls, e(url), label, ic(icon))

def sec_head(kicker, title, text="", link=None):
    right = ""
    if link:
        right = '<a class="btn btn--ghost btn--sm" href="%s">%s%s</a>' % (e(link[0]), e(link[1]), ic("arrow"))
    inner = '<div class="sec-head"><span class="kicker">%s</span><h2>%s</h2>%s</div>' % (e(kicker), title, ("<p>%s</p>" % text) if text else "")
    if link:
        return '<div class="sec-head--row">%s%s</div>' % (inner, right)
    return inner

NAV = [("index.html", "Home"), ("services.html", "Services"), ("work.html", "Work"), ("studio.html", "Studio"),
       ("store.html", "Store"), ("about.html", "About"), ("contact.html", "Contact")]

PAGES_FOR_SITEMAP = []

# ------------------------------------------------------------------ layout
def header(current):
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else "", l) for h, l in NAV)
    return '''<header class="site-header"><div class="container header__row">
<a class="brand" href="index.html" aria-label="%s home"><img src="assets/img/logo.svg" alt="" width="36" height="36"><span>Xitorque<small>Solutions &amp; Studio</small></span></a>
<nav class="nav" id="nav" aria-label="Main">%s</nav>
<div class="header__actions">
<button class="icon-btn" id="themeBtn" type="button" aria-label="Switch theme" aria-pressed="false"><span class="ico" aria-hidden="true"><svg class="i-sun" viewBox="0 0 24 24">%s</svg><svg class="i-moon" viewBox="0 0 24 24">%s</svg></span></button>
<a class="btn btn--primary btn--sm hire" href="contact.html">Start a project</a>
<button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">%s</button>
</div></div></header>''' % (e(BRAND), links, ICONS["sun"], ICONS["moon"], ic("menu"))

def social_links():
    out = []
    spec = [("github", "GitHub", "github"), ("fiverr", "Fiverr", "bag"), ("upwork", "Upwork", "bag"), ("gumroad", "Gumroad", "download"),
            ("daraz_store", "Daraz store", "store"), ("instagram", "Instagram", "link"), ("facebook", "Facebook", "link"),
            ("youtube", "YouTube", "video"), ("tiktok", "TikTok", "video"), ("linkedin", "LinkedIn", "link")]
    for key, label, icon in spec:
        if LINKS.get(key):
            out.append((label, LINKS[key], icon))
    return out

def footer():
    explore = "".join('<a href="%s">%s</a>' % (h, l) for h, l in NAV)
    svc = "".join('<a href="services.html#%s">%s</a>' % (s["slug"], e(s["name"])) for s in SERVICES[:6])
    conn = ""
    if WA:
        conn += '<a href="%s" target="_blank" rel="noopener">WhatsApp</a>' % e(wa_url())
    if EMAIL:
        conn += '<a href="mailto:%s">%s</a>' % (e(EMAIL), e(EMAIL))
    for label, url, _ in social_links():
        conn += '<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(url), e(label))
    if not conn:
        conn = '<a href="contact.html">Contact form</a>'
    return '''<footer class="site-footer"><div class="container">
<div class="footer__grid">
<div class="footer__brand"><a class="brand" href="index.html"><img src="assets/img/logo.svg" alt="" width="36" height="36"><span>Xitorque</span></a>
<p>%s. Based in %s, working with clients anywhere.</p></div>
<div><h4>Explore</h4>%s</div>
<div><h4>Services</h4>%s</div>
<div><h4>Connect</h4>%s</div>
</div>
<div class="footer__bar"><span>&copy; <span data-year>%s</span> %s. All rights reserved.</span><span><a href="privacy.html">Privacy</a></span></div>
</div></footer>''' % (e(CFG["tagline"]), e(CFG["location"]), explore, svc, conn, date.today().year, e(BRAND))

INSTALL_DIALOG = '''<dialog id="installDlg" aria-labelledby="installTitle"><div class="modal">
<div class="modal__head"><h3 id="installTitle" data-i="name">Install app</h3><button class="icon-btn" type="button" data-i="close" aria-label="Close">%s</button></div>
<p class="muted">No app store needed. Follow these steps on your device:</p>
<div class="steps" data-i="steps"></div>
<div class="actions" data-i="actions"></div></div></dialog>''' % ic("x")

def jsonld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def page(filename, title, desc, body, current=None, ld=None, base=False, noindex=False, og_title=None):
    url = SITE_URL + "/" + ("" if filename == "index.html" else filename)
    full_title = title if title.startswith(BRAND) else "%s | %s" % (title, BRAND)
    if filename == "index.html":
        full_title = "%s | %s" % (BRAND, CFG["tagline"])
    og_img = SITE_URL + "/assets/img/og.png"
    head = '''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
%s<title>%s</title>
<meta name="description" content="%s">
%s<link rel="canonical" href="%s">
<meta name="theme-color" content="#0a0a12">
<meta property="og:type" content="website"><meta property="og:site_name" content="%s">
<meta property="og:title" content="%s"><meta property="og:description" content="%s">
<meta property="og:url" content="%s"><meta property="og:image" content="%s">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<script>try{var t=localStorage.getItem('xt-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>
<link rel="stylesheet" href="assets/css/site.css">
%s</head>
<body>
<a class="skip" href="#main">Skip to content</a>
''' % ('<base href="/">\n' if base else "", e(full_title), e(desc),
       '<meta name="robots" content="noindex">\n' if noindex else "", e(url), e(BRAND), e(og_title or full_title), e(desc), e(url), e(og_img),
       "".join(jsonld(x) for x in (ld or [])))
    tail = '''
%s
%s
<script src="assets/js/site.js" defer></script>
</body>
</html>
''' % (footer(), INSTALL_DIALOG)
    doc = head + header(current) + '\n<main id="main">\n' + body + '\n</main>' + tail
    (OUT / filename).write_text(doc, encoding="utf-8")
    if not noindex and filename not in ("404.html", "offline.html"):
        PAGES_FOR_SITEMAP.append(filename)

def page_hero(kicker, title, lead, extra=""):
    return '''<section class="hero hero--page"><div class="grid-bg"></div><div class="orb orb--a"></div>
<div class="container hero__inner" style="grid-template-columns:1fr"><div>
<span class="eyebrow">%s</span><h1>%s</h1><p class="lead">%s</p>%s</div></div></section>''' % (e(kicker), title, lead, extra)

def cta_band(title="Have an idea? Let’s build it.", text="Tell us what you need. We’ll reply with an honest plan and a price before any work begins.", service=None):
    return '''<section class="section"><div class="container"><div class="cta-band reveal">
<h2>%s</h2><p>%s</p>
<div class="hero__cta" style="justify-content:center;margin-top:0">%s<a class="btn btn--ghost" href="work.html">See our work</a></div>
</div></div></section>''' % (title, text, '<a class="btn btn--primary" href="%s">Start a project%s</a>' % (e(contact_href(service)), ic("arrow")))

def faq_block(items):
    return '<div class="faq">%s</div>' % "".join(
        '<details class="reveal"><summary>%s</summary><p>%s</p></details>' % (e(f["q"]), e(f["a"])) for f in items)

# ------------------------------------------------------------------ cards
def status_badge(a):
    s = a.get("status", "live")
    if s == "live":
        label = "Live"
        if a.get("install") == "apk" and not a.get("url"):
            label = "Android APK"
        return '<span class="badge badge--live">%s</span>' % label
    if s == "soon":
        return '<span class="badge badge--soon">Coming soon</span>'
    return '<span class="badge badge--concept">Concept</span>'

def app_card(a):
    poster = '<div class="poster" style="--h:%s">%s%s</div>' % (a.get("hue", 265), status_badge(a), ic(a.get("icon", "spark")))
    tags = '<div class="tags">%s</div>' % "".join('<span class="tag">%s</span>' % e(t) for t in a.get("tags", []))
    btns = []
    kind = a.get("install", "none")
    if a.get("url"):
        btns.append(ext(a["url"], "Open live", "btn btn--primary btn--sm"))
        if kind in ("pwa", "web"):
            btns.append('<button class="btn btn--ghost btn--sm" type="button" data-install data-name="%s" data-url="%s" data-kind="%s">%sInstall</button>' % (e(a["name"]), e(a["url"]), kind, ic("download")))
    if kind == "apk" and a.get("apk_url"):
        btns.append('<button class="btn btn--primary btn--sm" type="button" data-install data-name="%s" data-apk="%s" data-kind="apk">%sGet the APK</button>' % (e(a["name"]), e(a["apk_url"]), ic("download")))
    if a.get("for_sale"):
        btns.append('<a class="btn btn--ghost btn--sm" href="%s">License this game</a>' % e(contact_href("games", "Licence the game " + a["name"])))
    if a.get("repo"):
        btns.append(ext(a["repo"], "Code", "btn btn--ghost btn--sm", "github"))
    if not a.get("url") and kind != "apk":
        btns.insert(0, '<a class="btn btn--primary btn--sm" href="%s">Ask for a demo</a>' % e(contact_href(about="A demo of " + a["name"])))
    search = " ".join([a["name"], a.get("by", ""), a.get("tagline", ""), a.get("desc", ""), " ".join(a.get("tags", []))]).lower()
    return '''<article class="card reveal" data-cat="%s" data-search="%s">
%s<div><h3>%s</h3><p class="muted" style="font-size:.84rem;margin:2px 0 6px">%s</p></div>
<p>%s</p>%s<div class="card__foot" style="gap:8px;justify-content:flex-start">%s</div></article>''' % (
        e(a.get("category", "")), e(search), poster, e(a["name"]), e(a.get("tagline", "")), e(a.get("desc", "")), tags, "".join(btns))

def service_card(s, detailed=True):
    badge = ' <span class="badge badge--soon" style="margin-left:6px;vertical-align:middle">Studio</span>' if s.get("division") == "studio" else ""
    if not detailed:
        return '''<a class="card reveal" href="services.html#%s" style="text-decoration:none">
<div class="card__icon">%s</div><h3>%s</h3><p>%s</p><div class="card__foot"><span class="price" style="color:var(--p2)">Learn more</span>%s</div></a>''' % (
            e(s["slug"]), ic(s["icon"]), e(s["name"]), e(s["short"]), ic("arrow"))
    lis = "".join("<li>%s<span>%s</span></li>" % (ic("check"), e(b)) for b in s["bullets"])
    tags = '<div class="tags">%s</div>' % "".join('<span class="tag">%s</span>' % e(t) for t in s.get("tags", []))
    return '''<article class="card reveal" id="%s">
<div class="card__icon">%s</div><h3>%s%s</h3><p>%s</p><ul class="list" style="margin-top:6px">%s</ul>%s
<div class="card__foot">%s<a class="btn btn--primary btn--sm" href="%s">Get a quote</a></div></article>''' % (
        e(s["slug"]), ic(s["icon"]), e(s["name"]), badge, e(s["short"]), lis, tags, price_html(s.get("price_from")), e(contact_href(s["slug"])))

def product_card(p):
    btns = []
    if p.get("url"):
        btns.append(ext(p["url"], "View on Daraz", "btn btn--primary btn--sm"))
    elif LINKS.get("daraz_store"):
        btns.append(ext(LINKS["daraz_store"], "Daraz store", "btn btn--primary btn--sm"))
    btns.append('<a class="btn %s btn--sm" href="%s">Ask about this</a>' % ("btn--ghost" if btns else "btn--primary", e(contact_href(about=p["name"]))))
    price = ('<span class="price">%s %s</span>' % (e(CFG.get("currency", "PKR")), e(p["price"]))) if p.get("price") else ""
    tags = '<div class="tags">%s</div>' % "".join('<span class="tag">%s</span>' % e(t) for t in p.get("tags", []))
    return '''<article class="card reveal"><div class="poster" style="--h:%s"><span class="badge">Daraz</span>%s</div>
<div><h3>%s</h3><p class="muted" style="font-size:.84rem;margin:2px 0 6px">%s</p></div><p>%s</p>%s
<div class="card__foot">%s<div style="display:flex;gap:8px;flex-wrap:wrap">%s</div></div></article>''' % (
        p.get("hue", 170), ic(p.get("icon", "bag")), e(p["name"]), e(p.get("variant", "")), e(p.get("desc", "")), tags, price, "".join(btns))

def process_block():
    steps = [("Talk", "Tell us what you need on WhatsApp or the form. We ask the right questions and listen."),
             ("Plan & quote", "You get a clear scope, timeline and price before any work starts."),
             ("Build & preview", "We build in stages and show you real, working previews along the way."),
             ("Launch & support", "We launch, teach you how to use it, and stay around for fixes and updates.")]
    return '<div class="process">%s</div>' % "".join('<div class="step reveal"><h3>%s</h3><p>%s</p></div>' % (e(t), e(d)) for t, d in steps)

def org_ld():
    same = [u for _, u, _ in social_links()]
    o = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": BRAND, "url": SITE_URL + "/",
         "logo": SITE_URL + "/assets/img/icon-512.png", "image": SITE_URL + "/assets/img/og.png",
         "description": CFG["tagline"] + " from " + CFG["location"] + ".",
         "address": {"@type": "PostalAddress", "addressLocality": "Sukkur", "addressCountry": "PK"},
         "areaServed": "Worldwide", "founder": {"@type": "Person", "name": CFG["founder"]},
         "knowsAbout": ["Web development", "Progressive web apps", "Shopify", "Daraz store management", "AI automation", "Game development"]}
    if same:
        o["sameAs"] = same
    if EMAIL:
        o["email"] = EMAIL
    if WA:
        o["telephone"] = "+" + WA
    return o

# ------------------------------------------------------------------ pages
live_count = sum(1 for a in APPS if a.get("status") == "live")
solutions_apps = [a for a in APPS if a.get("division") == "solutions"]
studio_apps = [a for a in APPS if a.get("division") == "studio"]

def build_home():
    feat = [a for a in APPS if a.get("featured") and a.get("division") == "solutions" and a.get("status") == "live"][:4]
    games = [a for a in studio_apps if a.get("status") == "live" and a.get("url")][:2]
    art = '''<div class="art" aria-hidden="true">
<div class="art__win"><div class="art__bar"><i></i><i></i><i></i></div><div class="art__body"><div class="art__hero"></div><div class="art__line"></div><div class="art__line"></div><div class="art__line"></div><div class="art__cols"><span></span><span></span><span></span></div></div></div>
<div class="art__phone"><b></b><span></span><span></span><span></span></div>
<span class="chip chip--1">%s Installable apps</span><span class="chip chip--2">%s Shopify</span><span class="chip chip--3">%s Daraz</span></div>''' % (ic("phone"), ic("bag"), ic("store"))
    stats = [(live_count, "", "Live projects"), (25, "+", "Daraz listings"), (len(SERVICES), "", "Services"), (6, "", "Team members")]
    stat_html = "".join('<div class="stat reveal"><b data-count="%s" data-suffix="%s">%s%s</b><span>%s</span></div>' % (n, suf, n, suf, e(l)) for n, suf, l in stats)
    hero = '''<section class="hero"><div class="grid-bg"></div><div class="orb orb--a"></div><div class="orb orb--b"></div>
<div class="container"><div class="hero__inner"><div>
<span class="eyebrow">%s &middot; %s</span>
<h1>We build the apps, websites &amp; stores that <span class="grad-text">grow your business</span></h1>
<p class="lead">Custom software, Shopify stores and Daraz management from a small, fast-growing team. Open and install real apps we have built, right from this site.</p>
<div class="hero__cta"><a class="btn btn--primary" href="contact.html">Start a project%s</a><a class="btn btn--ghost" href="work.html">See our work</a></div>
</div><div class="hero__art">%s</div></div>
<div class="stats">%s</div></div></section>''' % (e(BRAND), e(CFG["location"]), ic("arrow"), art, stat_html)

    services = '''<section class="section"><div class="container">%s<div class="grid grid--4">%s</div></div></section>''' % (
        sec_head("What we do", "Everything your business needs online", "One team for your website, your apps, your store and your day-to-day digital work.", ("services.html", "All services")),
        "".join(service_card(s, detailed=False) for s in SERVICES[:8]))

    work = '''<section class="section section--alt"><div class="container">%s<div class="grid grid--two">%s</div></div></section>''' % (
        sec_head("Selected work", "Real apps you can open today", "No mock-ups. Every project below is live. Tap Open to try it, or Install to put it on your phone.", ("work.html", "All work")),
        "".join(app_card(a) for a in feat))

    split = '''<section class="section"><div class="container"><div class="split">
<div class="panel reveal"><span class="badge badge--live">Solutions</span><h2 style="margin-top:14px">%s</h2>
<p class="muted">Our agency side. We build websites, apps and Shopify stores, run Daraz stores and automate the boring work, so owners can focus on growing.</p>
<ul class="list">%s</ul><a class="btn btn--primary" href="services.html">Explore services</a></div>
<div class="panel panel--studio reveal"><span class="badge badge--concept">Studio</span><h2 style="margin-top:14px">%s</h2>
<p class="muted">Our creative side. Games with real polish, product ads and AI-made videos that get attention.</p>
<ul class="list">%s</ul><a class="btn btn--primary" href="studio.html">Visit the Studio</a></div></div></div></section>''' % (
        e(BRAND), "".join("<li>%s<span>%s</span></li>" % (ic("check"), e(t)) for t in ["Websites and landing pages", "Installable business apps", "Shopify and Daraz"]),
        e(CFG["studio"]), "".join("<li>%s<span>%s</span></li>" % (ic("check"), e(t)) for t in ["Branded browser and Android games", "Product ads and photos", "AI cartoon and video content"]))

    store = '''<section class="section section--alt"><div class="container"><div class="panel reveal" style="display:grid;gap:20px;align-items:center">
<div><span class="badge badge--live">Xitorque Store</span><h2 style="margin-top:14px">We sell on Daraz, and we can run your Daraz store too.</h2>
<p class="muted" style="max-width:62ch">We list, price and photograph products every day. See what we sell, or hand your own store to a team that knows the platform.</p>
<div class="hero__cta"><a class="btn btn--primary" href="store.html">Visit the Store%s</a><a class="btn btn--ghost" href="%s">Daraz management</a></div></div></div></div></section>''' % (ic("arrow"), e(contact_href("daraz")))

    if games:
        gm = '''<section class="section"><div class="container">%s<div class="grid grid--two">%s</div></div></section>''' % (
            sec_head("From the Studio", "Games you can play right now", "", ("studio.html", "More games")), "".join(app_card(a) for a in games))
    else:
        gm = ""

    proc = '<section class="section section--alt"><div class="container">%s%s</div></section>' % (
        sec_head("How it works", "Simple, clear and honest", "No jargon and no surprises."), process_block())
    faq = '<section class="section"><div class="container" style="max-width:820px">%s%s</div></section>' % (
        sec_head("Questions", "Quick answers"), faq_block(FAQ[:5]))
    body = hero + services + work + split + gm + store + proc + faq + cta_band()
    ld = [org_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE_URL + "/"}]
    page("index.html", BRAND, "%s. Custom apps, websites, Shopify stores, Daraz management and games from %s." % (CFG["tagline"], CFG["location"]), body, "index.html", ld)

def build_services():
    body = page_hero("Services", "Everything your business needs, <span class=\"grad-text\">under one roof</span>",
                     "Pick a service, or tell us your goal and we’ll put the right pieces together. Every price below is a starting point, and the final quote is agreed with you first.")
    body += '<section class="section" style="padding-top:20px"><div class="container"><div class="grid grid--2">%s</div></div></section>' % "".join(service_card(s) for s in SERVICES)
    body += '<section class="section section--alt"><div class="container">%s%s</div></section>' % (sec_head("How we work", "From first message to launch"), process_block())
    body += '<section class="section"><div class="container" style="max-width:820px">%s%s</div></section>' % (sec_head("Questions", "Before you ask"), faq_block(FAQ))
    body += cta_band()
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": s["name"], "description": s["short"], "provider": {"@type": "Organization", "name": BRAND}}}
        for i, s in enumerate(SERVICES)]}]
    page("services.html", "Services", "Websites, installable apps, Shopify, Daraz store management, AI automation, games and product ads from %s." % BRAND, body, "services.html", ld)

def build_work():
    cats = [("business", "Business apps"), ("tools", "Tools"), ("websites", "Websites")]
    present = {a.get("category") for a in solutions_apps}
    chips = '<button class="chipbtn" type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        '<button class="chipbtn" type="button" data-filter="%s" aria-pressed="false">%s</button>' % (k, l) for k, l in cats if k in present)
    th = CFG.get("shopify_theme", {})
    th_btns = []
    if th.get("demo_url"):
        th_btns.append(ext(th["demo_url"], "View demo", "btn btn--primary btn--sm"))
    if th.get("buy_url"):
        th_btns.append(ext(th["buy_url"], "Get the theme", "btn btn--primary btn--sm"))
    th_btns.append('<a class="btn %s btn--sm" href="%s">Request a demo</a>' % ("btn--ghost" if th_btns else "btn--primary", e(contact_href("shopify", "Xitorque Shopify theme demo"))))
    th_status = {"live": "Available", "soon": "In development", "concept": "Concept"}.get(th.get("status", "soon"), "In development")
    feats = ["Quick View and Recently Viewed", "Slide-out cart and sticky cart bar", "Mega menu and sticky header", "Colour swatches, product tabs, image zoom", "Product recommendations and blog templates", "Built to work for any kind of store"]
    theme = '''<article class="panel reveal"><div class="split" style="align-items:center"><div>
<span class="badge badge--concept">%s</span><h2 style="margin-top:14px">Xitorque Shopify theme</h2>
<p class="muted">A fast, flexible theme designed to suit any niche, built to compete with premium themes. Tested on our own development store with a real product.</p>
<ul class="list">%s</ul><div class="hero__cta" style="margin-top:8px">%s</div></div>
<div class="poster" style="--h:150;height:240px;border-radius:20px"><span class="badge">Shopify</span>%s</div></div></article>''' % (
        th_status, "".join("<li>%s<span>%s</span></li>" % (ic("check"), e(f)) for f in feats), "".join(th_btns), ic("bag"))
    body = page_hero("Work", "Things we’ve built, <span class=\"grad-text\">ready to try</span>",
                     "Open any project live. Install the apps on your phone like a normal app. Everything here was designed and built by our team.")
    body += '''<section class="section" style="padding-top:20px"><div class="container" data-filter-root>
<div class="filters">%s<input class="search" type="search" placeholder="Search projects" aria-label="Search projects"></div>
<div class="grid grid--3">%s</div><div class="empty" hidden>No projects match your search.</div></div></section>''' % (chips, "".join(app_card(a) for a in solutions_apps))
    body += '<section class="section section--alt"><div class="container">%s%s</div></section>' % (sec_head("Shopify", "A theme for any store"), theme)
    body += '''<section class="section"><div class="container"><div class="panel reveal"><h2>Want something like this for your business?</h2>
<p class="muted" style="max-width:60ch">We can build a custom version for your shop, your service or your idea. Tell us what you do and we’ll suggest the right tool.</p>
<a class="btn btn--primary" href="contact.html">Talk to us%s</a></div></div></section>''' % ic("arrow")
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "SoftwareApplication", "name": a["name"], "description": a.get("desc", ""), "applicationCategory": "WebApplication", "operatingSystem": "Any", "url": a["url"]}}
        for i, a in enumerate([x for x in solutions_apps if x.get("url")])]}]
    page("work.html", "Work", "Live apps and websites by %s: shop management, a physics and maths calculator, realtime chat, business sites and more." % BRAND, body, "work.html", ld)

def build_studio():
    studio_services = [s for s in SERVICES if s.get("division") == "studio"]
    body = page_hero("Xitorque Studio", "Games and ads that <span class=\"grad-text\">get attention</span>",
                     "The creative side of Xitorque. We make polished browser and Android games, product ads and AI video content, and we can brand them for you.")
    body += '<section class="section" style="padding-top:20px"><div class="container">%s<div class="grid grid--3">%s</div></div></section>' % (
        sec_head("Games", "Play, install, or license one", "Open a game in your browser or install it on your phone. Games marked “License” can be rebranded for your own project."),
        "".join(app_card(a) for a in studio_apps))
    body += '<section class="section section--alt"><div class="container">%s<div class="grid grid--2">%s</div></div></section>' % (
        sec_head("Studio services", "Made for you"), "".join(service_card(s) for s in studio_services))
    body += cta_band("Need a game or an ad for your brand?", "Tell us your idea, audience and budget. We’ll come back with a plan and a quote.", "games")
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {"@type": "VideoGame", "name": a["name"], "description": a.get("desc", ""), "url": a["url"]}}
        for i, a in enumerate([x for x in studio_apps if x.get("url")])]}]
    page("studio.html", "Studio: Games & Product Ads", "%s makes branded browser and Android games, product ads and AI video content." % CFG["studio"], body, "studio.html", ld)

def build_store():
    dz = LINKS.get("daraz_store")
    hero_btns = '<div class="hero__cta">%s<a class="btn btn--ghost" href="%s">Daraz management service</a></div>' % (
        ext(dz, "Visit our Daraz store", "btn btn--primary") if dz else '<a class="btn btn--primary" href="%s">Ask about products</a>' % e(contact_href(about="Your products on Daraz")),
        e(contact_href("daraz")))
    body = page_hero("Xitorque Store", "Products we sell, and a team that can <span class=\"grad-text\">sell yours</span>",
                     "We run a real Daraz store, so we know what it takes to list, price and photograph products that sell. See what we offer, or let us manage your store.", hero_btns)
    body += '<section class="section" style="padding-top:20px"><div class="container">%s<div class="grid grid--2">%s</div></div></section>' % (
        sec_head("On Daraz", "What we sell", "A growing range of everyday products, sold to customers and to shops."), "".join(product_card(p) for p in PRODUCTS))
    body += '''<section class="section section--alt"><div class="container"><div class="split">
<div class="panel reveal"><span class="badge badge--live">For shopkeepers</span><h2 style="margin-top:14px">Wholesale mobile accessories</h2>
<p class="muted">Running a shop? We supply mobile accessories in bulk. Ask us about what is in stock and wholesale rates.</p>
<a class="btn btn--primary" href="%s">Ask about wholesale</a></div>
<div class="panel panel--studio reveal"><span class="badge badge--concept">For sellers</span><h2 style="margin-top:14px">Daraz store management</h2>
<ul class="list"><li>%s<span>Seller Center setup and product listings</span></li><li>%s<span>Titles, descriptions and pricing that rank</span></li><li>%s<span>Professional product pictures</span></li><li>%s<span>Daily upkeep so you can focus on sourcing</span></li></ul>
<a class="btn btn--primary" href="%s">Get a quote</a></div></div></div></section>''' % (
        e(contact_href(about="Wholesale mobile accessories")), ic("check"), ic("check"), ic("check"), ic("check"), e(contact_href("daraz")))
    if LINKS.get("gumroad"):
        body += '''<section class="section"><div class="container"><div class="panel reveal"><span class="badge badge--soon">Digital</span><h2 style="margin-top:14px">Digital downloads</h2>
<p class="muted" style="max-width:60ch">Prefer something you can download instantly? Find our digital products on Gumroad.</p>%s</div></div></section>''' % ext(LINKS["gumroad"], "View on Gumroad", "btn btn--primary")
    body += cta_band("Want us to run your Daraz store?", "Send us a few details about your products and we’ll tell you how we can help.", "daraz")
    page("store.html", "Store: Daraz Products & Management", "Products %s sells on Daraz, plus Daraz store management: listings, pricing and product pictures." % BRAND, body, "store.html")

def build_about():
    team = "".join('<div class="card reveal"><div class="avatar">%s</div><h3>%s</h3><p class="price" style="color:var(--p2)">%s</p><p>%s</p></div>' % (
        e(t["initials"]), e(t["name"]), e(t["role"]), e(t["bio"])) for t in TEAM)
    values = [("Show, don’t tell", "Every project on this site is live. You can open it before you hire us.", "rocket"),
              ("Built for local reality", "Urdu and right-to-left support, WhatsApp-first contact, and apps that keep working with a weak connection.", "pin"),
              ("Honest scope & price", "You know what you’re getting and what it costs before we start.", "shield"),
              ("Small team, direct access", "You talk to the people building your project, not a sales desk.", "users")]
    vals = "".join('<div class="card reveal"><div class="card__icon">%s</div><h3>%s</h3><p>%s</p></div>' % (ic(i), e(t), e(d)) for t, d, i in values)
    body = page_hero("About", "A small team with <span class=\"grad-text\">big-team habits</span>",
                     "%s is a growing digital team based in %s. We build apps and websites, run online stores, and make games and ads, all under one roof." % (e(BRAND), e(CFG["location"])))
    body += '''<section class="section" style="padding-top:20px"><div class="container"><div class="split">
<div class="panel reveal"><h2>Our story</h2><p class="muted">Xitorque began with a founder who taught himself design, then Python, HTML, CSS and JavaScript, and then e-commerce. Today he leads a team of six that combines hands-on development experience with modern AI tools to ship quickly.</p>
<p class="muted">What we learned building our own apps, games and Daraz store is exactly what we now bring to client projects: practical, tested and made for real businesses.</p></div>
<div class="panel panel--studio reveal"><h2>Two brands, one team</h2>
<p><b>%s</b> is the agency. It builds websites, apps and Shopify stores, manages Daraz stores and automates the busywork.</p>
<p><b>%s</b> is the creative division. It makes games and product ads.</p></div></div></div></section>''' % (e(BRAND), e(CFG["studio"]))
    body += '<section class="section section--alt"><div class="container">%s<div class="grid grid--3">%s</div></div></section>' % (sec_head("The team", "Six people, growing steadily", "Skills across development, AI, design, documents and e-commerce."), team)
    body += '<section class="section"><div class="container">%s<div class="grid grid--4">%s</div></div></section>' % (sec_head("How we work", "What you can expect"), vals)
    body += cta_band("Let’s work together", "Tell us about your project. A short message is enough to start.")
    page("about.html", "About", "%s is a growing six-person team in %s building apps, websites, Shopify stores and games." % (BRAND, CFG["location"]), body, "about.html")

def build_contact():
    opts = '<option value="">Not sure yet</option>' + "".join('<option value="%s">%s</option>' % (e(s["slug"]), e(s["name"])) for s in SERVICES) + '<option value="other">Something else</option>'
    fallback = LINKS.get("fiverr", "")
    btn_label = "Send message" if (WA or EMAIL) else "Send via Fiverr"
    form = '''<form class="form" id="contactForm" data-wa="%s" data-mail="%s" data-fallback="%s">
<div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-svc">What do you need?</label><select id="f-svc" name="service">%s</select></div>
<div class="field"><label for="f-msg">Tell us about your project</label><textarea id="f-msg" name="message" required placeholder="What do you sell or do? What should we build or manage?"></textarea></div>
<div class="field"><label for="f-reply">Phone or email (optional)</label><input id="f-reply" name="reply" autocomplete="tel"></div>
<button class="btn btn--primary" type="submit">%s%s</button>
<p class="muted" style="font-size:.86rem;margin:0">%s</p></form>''' % (
        e(WA), e(EMAIL), e(fallback), opts, btn_label, ic("arrow"),
        "This opens WhatsApp with your message ready to send." if WA else ("This opens your email app with your message ready to send." if EMAIL else "Your message is copied, then our Fiverr profile opens. Paste it into a message to us."))
    items = ""
    if WA:
        items += '<a href="%s" target="_blank" rel="noopener">%s<span>WhatsApp<small>Fastest way to reach us</small></span></a>' % (e(wa_url()), ic("chat"))
    if EMAIL:
        items += '<a href="mailto:%s">%s<span>Email<small>%s</small></span></a>' % (e(EMAIL), ic("mail"), e(EMAIL))
    notes = {"fiverr": "Order through Fiverr", "upwork": "Hire us on Upwork", "gumroad": "Digital downloads", "github": "See our code", "daraz_store": "Shop our products"}
    for label, url, icon in social_links():
        key = [k for k, v in LINKS.items() if v == url][0]
        items += '<a href="%s" target="_blank" rel="noopener">%s<span>%s<small>%s</small></span></a>' % (e(url), ic(icon), e(label), e(notes.get(key, "Follow us")))
    items += '<a href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">%s<span>Based in %s<small>Working with clients worldwide</small></span></a>' % (quote(CFG["location"]), ic("pin"), e(CFG["location"]))
    body = page_hero("Contact", "Tell us what you’d like to <span class=\"grad-text\">build</span>", "A few lines are enough. We’ll reply with questions, ideas and an honest price.")
    body += '<section class="section" style="padding-top:20px"><div class="container"><div class="split"><div class="panel">%s</div><div><div class="contact-list">%s</div></div></div></div></section>' % (form, items)
    page("contact.html", "Contact", "Start a project with %s. Message us on WhatsApp or send the form." % BRAND, body, "contact.html")

def build_misc():
    body = '''<section class="section"><div class="container" style="max-width:760px"><h1>Privacy</h1>
<p class="muted">Last updated %s</p>
<p>This site does not use advertising cookies or trackers.</p>
<h3>What we store</h3><p>If you switch between light and dark mode, your choice is saved in your own browser so the site remembers it. Nothing else is stored.</p>
<h3>The contact form</h3><p>The form does not send data to our servers. It prepares a message that opens in WhatsApp or your email app, and you decide whether to send it. Anything you send arrives with us directly and is used only to reply to you.</p>
<h3>Other sites</h3><p>Links to apps, GitHub, Daraz, Fiverr, Gumroad and other sites lead to services with their own privacy policies.</p>
<h3>Apps we build</h3><p>Each app has its own data handling. Ask us if you want details about a specific app.</p>
<h3>Contact</h3><p>Questions about this policy? Reach us through the <a href="contact.html">contact page</a>.</p></div></section>''' % TODAY
    page("privacy.html", "Privacy", "How this website handles your data.", body, None)

    body404 = '''<section class="hero hero--page"><div class="container" style="text-align:center;padding:60px 0"><span class="eyebrow">Error 404</span><h1>This page took a wrong turn</h1>
<p class="lead" style="margin-inline:auto">The page you’re looking for doesn’t exist or has moved.</p>
<div class="hero__cta" style="justify-content:center"><a class="btn btn--primary" href="/">Go home</a><a class="btn btn--ghost" href="/work.html">See our work</a></div></div></section>'''
    page("404.html", "Page not found", "Page not found.", body404, None, base=True, noindex=True)

    off = '''<section class="hero hero--page"><div class="container" style="text-align:center;padding:60px 0"><span class="eyebrow">Offline</span><h1>You’re offline</h1>
<p class="lead" style="margin-inline:auto">Check your connection and try again. Pages you’ve already visited still open.</p>
<div class="hero__cta" style="justify-content:center"><a class="btn btn--primary" href="index.html">Home</a></div></div></section>'''
    page("offline.html", "Offline", "You are offline.", off, None, noindex=True)

# ------------------------------------------------------------------ extra files
def write_extras():
    manifest = {"name": BRAND, "short_name": CFG["short"], "description": CFG["tagline"], "start_url": "./", "scope": "./", "display": "standalone",
                "background_color": "#0a0a12", "theme_color": "#0a0a12", "icons": [
                    {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                    {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                    {"src": "assets/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    (OUT / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (SITE_URL, "" if p == "index.html" else p, TODAY) for p in PAGES_FOR_SITEMAP)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls, encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if DOMAIN:
        (OUT / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    core = sorted(p.name for p in OUT.glob("*.html")) + ["manifest.webmanifest"] + sorted(
        str(p.relative_to(OUT)).replace("\\", "/") for p in (OUT / "assets").rglob("*") if p.is_file())
    sw = '''/* Xitorque service worker: generated by build.py */
const CACHE = 'xt-%s';
const CORE = %s;
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; })
      .catch(() => caches.match(req).then(m => m || caches.match('offline.html'))));
    return;
  }
  e.respondWith(caches.match(req).then(m => {
    const net = fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; }).catch(() => m);
    return m || net;
  }));
});
''' % (TODAY.replace("-", ""), json.dumps(["./"] + core))
    (OUT / "sw.js").write_text(sw, encoding="utf-8")

# ------------------------------------------------------------------ main
def report():
    todo = []
    if not WA:
        todo.append("config.json: add your WhatsApp number (digits only, with country code, e.g. 923001234567)")
    if not EMAIL:
        todo.append("config.json: add a contact email (optional but recommended)")
    if not DOMAIN:
        todo.append("config.json: after you buy your domain, set custom_domain (e.g. xitorque.com) and rebuild")
    if not LINKS.get("daraz_store"):
        todo.append("config.json: links.daraz_store (your Daraz store URL)")
    for p in PRODUCTS:
        if not p.get("url"):
            todo.append("products.json: add the Daraz link for '%s'" % p["name"])
    empty = [s["name"] for s in SERVICES if s.get("price_from") in ("", None)]
    if empty:
        todo.append("services.json: add price_from for: " + ", ".join(empty))
    for a in APPS:
        if a.get("confirm"):
            todo.append("apps.json: check '%s'. %s" % (a["name"], a.get("confirm_note", "")))
    th = CFG.get("shopify_theme", {})
    if not th.get("demo_url"):
        todo.append("config.json: shopify_theme.demo_url (when a demo store link is ready)")
    print("\nBuild finished: %s" % OUT)
    print("Pages: " + ", ".join(sorted(p.name for p in OUT.glob("*.html"))))
    if todo:
        print("\nStill to fill in / confirm (the site works without these):")
        for t in todo:
            print("  - " + t)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for item in OUT.iterdir():
        if item.name in KEEP:
            continue
        shutil.rmtree(item) if item.is_dir() else item.unlink()
    for item in STATIC.iterdir():
        if item.name == "snippets":
            continue
        if item.is_dir():
            shutil.copytree(item, OUT / item.name)
        else:
            shutil.copy2(item, OUT / item.name)
    build_home(); build_services(); build_work(); build_studio(); build_store(); build_about(); build_contact(); build_misc()
    write_extras()
    report()

if __name__ == "__main__":
    sys.exit(main())
