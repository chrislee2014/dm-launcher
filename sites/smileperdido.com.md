# smileperdido.com (old domain of Perdido Family Dentistry)

- **Canonical site:** www.smilesofpensacola.com (already live on its Worker)
- **Zone:** `b6693e4fe4397e6fb845d5b5446b3ffe` (active in our account)

## What happened (PITFALLS #7)

The apex/www still pointed at Webflow (A @ 198.202.211.1 + CNAME www cdn.webflow.com), unproxied. After the main site
launched and Webflow hosting ended, it returned Cloudflare error 1014. Found by the
broken-domain sweep on 2026-11-16; Chris confirmed it belongs to smilesofpensacola.com.

## Fix (2026-11-16)

- Redirect Rule `06014b7b83cd4c3f9be66e6576db617d` (dynamic redirect phase): host in {apex, www} → 301 to
  `concat("https://www.smilesofpensacola.com", path)`, query kept.
- Apex → A `192.0.2.1` proxied; www → CNAME @ proxied (both commented).
- Untouched: 4 MX, autodiscover CNAME, 4 TXT @, _webflow TXT.
- Verified from the public internet: http/https apex and www → 301 to the same path
  on www.smilesofpensacola.com (with query), one hop then 200.
