#!/usr/bin/env python3
"""One-off helper that draws the logo, app icons and social-share image. Needs Pillow (pip install pillow).
The results are already saved in static/assets/img, so you only run this if you want to change the artwork."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(__file__).resolve().parent / "static" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Xitorque">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6d28d9"/><stop offset=".55" stop-color="#a855f7"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs>
<rect width="64" height="64" rx="16" fill="url(#g)"/>
<path d="M19 18 45 46M45 18 19 46" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"/>
<circle cx="47" cy="17" r="4" fill="#fff" opacity=".9"/></svg>"""
(OUT / "logo.svg").write_text(LOGO_SVG, encoding="utf-8")
(OUT / "favicon.svg").write_text(LOGO_SVG, encoding="utf-8")

def gradient(size, c1, c2, c3):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            if t < .55:
                k = t / .55; a, b = c1, c2
            else:
                k = (t - .55) / .45; a, b = c2, c3
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
    return img

C1, C2, C3 = (109, 40, 217), (168, 85, 247), (34, 211, 238)

def icon(size, pad_ratio=0.0, rounded=True):
    base = gradient((size, size), C1, C2, C3)
    d = ImageDraw.Draw(base)
    pad = size * (0.27 + pad_ratio)
    w = int(size * 0.11)
    d.line([(pad, pad), (size - pad, size - pad)], fill="white", width=w)
    d.line([(size - pad, pad), (pad, size - pad)], fill="white", width=w)
    for pt in [(pad, pad), (size - pad, size - pad), (size - pad, pad), (pad, size - pad)]:
        d.ellipse([pt[0] - w / 2, pt[1] - w / 2, pt[0] + w / 2, pt[1] + w / 2], fill="white")
    if not rounded:
        return base
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.25), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(base, (0, 0), mask)
    return out

icon(192).save(OUT / "icon-192.png")
icon(512).save(OUT / "icon-512.png")
icon(512, pad_ratio=0.04, rounded=False).save(OUT / "icon-maskable-512.png")

# social share image 1200x630
W, H = 1200, 630
bg = Image.new("RGB", (W, H), (10, 10, 18))
glow = Image.new("RGB", (W, H), (10, 10, 18))
gd = ImageDraw.Draw(glow)
gd.ellipse([700, -250, 1350, 380], fill=(110, 50, 220)); gd.ellipse([-200, 330, 420, 900], fill=(8, 120, 150))
glow = glow.filter(ImageFilter.GaussianBlur(120))
bg = Image.blend(bg, glow, .75)
d = ImageDraw.Draw(bg)
for x in range(0, W, 56): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10) if False else (24, 24, 38))
for y in range(0, H, 56): d.line([(0, y), (W, y)], fill=(24, 24, 38))
def font(size, bold=True):
    for path in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        try: return ImageFont.truetype(path, size)
        except OSError: pass
    return ImageFont.load_default()
logo = icon(120)
bg.paste(logo, (80, 80), logo)
d.text((222, 96), "Xitorque", font=font(52), fill="white")
d.text((222, 158), "Solutions & Studio", font=font(26, False), fill=(190, 190, 215))
d.text((80, 270), "Apps, websites & online", font=font(76), fill="white")
d.text((80, 360), "stores that grow your", font=font(76), fill="white")
d.text((80, 450), "business.", font=font(76), fill=(192, 132, 252))
d.text((80, 565), "Sukkur, Pakistan  ·  Working with clients worldwide", font=font(26, False), fill=(190, 190, 215))
bg.save(OUT / "og.png", optimize=True)
print("assets written to", OUT)
