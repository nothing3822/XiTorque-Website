# Xitorque Solutions & Studio — website package

```
site/      ← the finished website. Upload the CONTENTS of this folder to GitHub.
source/    ← build.py + data/*.json. Edit data, run `python build.py`, re-upload site/.
snippets/  ← install-prompt.js: paste into each of your own apps (see step 5).
```

Pages: Home, Services, Work, Studio, Store, About, Contact (+ Privacy, 404, Offline).
Dark and light theme, mobile-first, installable (PWA), SEO files included (sitemap, robots, Open Graph, JSON-LD).

---

## 1. Deploy on GitHub Pages (free)

**Do NOT name this repo `nothing3822.github.io`.** When your main user site gets a custom domain, GitHub also serves all your other project sites under it (Tijarat would move to `xitorque.com/XiT-Khata/`, and so on) and this cannot be switched off. That changes the web address your apps run on: data saved inside the browser does not follow, installed home-screen copies break, and Firebase sign-in needs the new domain added. Putting the website in its own repo avoids all of that. Your apps keep their current addresses.

1. On GitHub create a **public** repo named `xitorque-website`.
2. Upload everything inside `site/` to the repo root (including the hidden `.nojekyll` file). `index.html` must sit at the top level.
3. Repo → Settings → Pages → Source: *Deploy from a branch* → `main` / `(root)` → Save.
4. After about a minute a preview is live at `https://nothing3822.github.io/xitorque-website/`. The preview is only for a quick look: the 404 page and share tags are built for `xitorque.com`.

## 2. Custom domain (xitorque.com)

This package is already built for `xitorque.com` (`custom_domain` is set in `source/data/config.json`, which also writes the `CNAME` file and sets canonical URLs, sitemap and share tags). For a different domain, change that value, run `python build.py` and re-upload `site/`.

Follow this order (GitHub's docs warn that adding DNS first can let someone else claim your domain on GitHub):

1. Repo `xitorque-website` → Settings → Pages → **Custom domain** → `xitorque.com` → Save.
2. Recommended: GitHub profile → Settings → Pages → *Add a domain* and add the TXT record it shows. This verifies the domain is yours.
3. At your registrar's DNS settings, delete any default or parking records, then add:
   - four **A** records, host `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - one **CNAME** record, host `www` → `nothing3822.github.io` (only your username, no repo name)
   - optional IPv6: four **AAAA** records, host `@` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - no wildcard (`*`) records
4. DNS can take up to 24 hours. When GitHub's DNS check passes, tick **Enforce HTTPS** (the option may take up to 24 hours to appear).

## 3. Fill the gaps (the site works without them, but these make it sell)

Edit the files in `source/data/`, then run `python build.py`. The build prints a to-do list every time.

| File | What to add |
|---|---|
| `config.json` | **`whatsapp`** (digits only with country code, e.g. `923001234567`). This is the most important one: the contact form and buttons then open WhatsApp. Also `email`, `links.daraz_store`, social links, `custom_domain`. Until WhatsApp/email is set, the form falls back to your Fiverr profile. |
| `services.json` | `price_from` for each service (number or text). Empty shows "Custom quote". |
| `products.json` | Daraz product URL and optional price for each product. |
| `apps.json` | Check the five items flagged `confirm` (see list below). Add screenshots later if you want. |
| `config.json → shopify_theme` | `demo_url` when you have a demo store link (dev-store preview links expire after about 2 days, so use a permanent link or video). |
| `team.json` | Real names/roles when your teammates agree to be listed. |
| `faq.json` | Check the answers match how you actually work (payments, timelines). |

Items I could not verify and marked for you to check:
- **Nexus Chat**: used `nexus-frontend-sage.vercel.app` (from your repo). Your older link was `chat-with-mashori.vercel.app`. Use whichever is live.
- **ISP Manager**: the description is inferred from the name. Replace it with what the app really does.
- **Tajweez** and **Flappy Dash**: no live URL found, so they show "Coming soon" with a source link. Add `url` and set `"status": "live"` when deployed.
- **Snake (Android)**: the Download button points to `github.com/nothing3822/snake-game/releases/latest`. Create a Release and attach the `.apk`, otherwise that page is empty.
- **Fiverr link** is `fiverr.com/m_affaque` (from your handle). Confirm it opens your profile.

## 4. Add a new project or service later

Open `data/apps.json`, copy one block, change the fields, run `python build.py`. Fields: `category` (business / tools / websites / games), `division` (solutions = Work page, studio = Studio page), `status` (live / soon), `install` (pwa / web / apk / none), `for_sale: true` adds a "License this game" button.

## 5. Make "Install" one-tap in your apps

The Install button opens your app with `?install=1`. Paste `snippets/install-prompt.js` before `</body>` in each of your own PWAs. When someone arrives from this site, it shows a big **Install this app** button the moment the browser allows it. It does nothing on normal visits. Without the snippet, the modal's step-by-step guide still works.

## 6. After launch (15 minutes, big SEO win)

1. Google Search Console → add your site → submit `https://yourdomain/sitemap.xml`.
2. Create a Google Business Profile for Xitorque Solutions (Sukkur) to appear in local searches.
3. Put the website link in your Fiverr, Upwork, GitHub, Gumroad and Daraz seller profiles.
4. Share the Work page link when pitching local shops.

## 7. Security: please fix this soon (only you can do it)

Both `Nexus-backend` and `Nexus-frontend` have a `.env` file committed in their **public** repos, and the backend also has `nexus.db`. Anyone can read them.
- Treat every secret in those `.env` files as leaked: rotate `SECRET_KEY`, the database password/URL and any API keys in Railway and Vercel.
- Remove the files from the repos (`git rm --cached .env nexus.db`, add both to `.gitignore`) and push. They remain in git history, so rotating the secrets is what actually protects you.
- Before deleting `nexus.db`, check whether production still uses it; your live app uses PostgreSQL on Railway.
- Alternatively make those two repos private. The website's "Code" button for Nexus will then 404, so remove `repo` from that entry in `apps.json`.

## Notes
- No tracking or cookies. The contact form sends nothing to a server: it opens WhatsApp or your email app with the message ready.
- The Shopify theme card says "In development" and offers "Request a demo". Change `shopify_theme.status` to `live` when it ships.
- Screenshots of the live apps could not be captured from my environment (outbound access to github.io is blocked), so cards use colour posters. You can add real screenshots later.
