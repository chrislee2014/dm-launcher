# dentaldesignsclermont.com (old domain of Dental Designs at Oakley Seaver)

- **Canonical site:** www.ddsclermont.com (already live on its Worker)
- **Zone:** `6cb6e0ed1462ad77f5d71d3cd88ffcbe` (active in our account)

## What happened (PITFALLS #7)

The apex/www still pointed at Webflow (CNAME @ cdn.webflow.com + CNAME www cdn.webflow.com), unproxied. After the main site
launched and Webflow hosting ended, it returned Cloudflare error 1014. Found by the
broken-domain sweep on 2026-11-16; Chris confirmed it belongs to ddsclermont.com.

## Fix (2026-11-16)

- Redirect Rule `9d18599040ba4ab6847ead3a331e7652` (dynamic redirect phase): host in {apex, www} → 301 to
  `concat("https://www.ddsclermont.com", path)`, query kept.
- Apex → A `192.0.2.1` proxied; www → CNAME @ proxied (both commented).
- Untouched: _domainconnect CNAME, promo CNAME (proxy-ssl.webflow.com, proxied). No MX.
- Verified from the public internet: http/https apex and www → 301 to the same path
  on www.ddsclermont.com (with query), one hop then 200.
