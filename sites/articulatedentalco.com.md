# articulatedentalco.com (Articulate Dental Company, Chicago, IL)

- **Worker:** `articulatedentalco-com` (last deploy 2026-11-04 by Judith, wrangler)
- **Zone:** `983d04ff7ab07b31dba07d3b6a754259`, active since 2026-11-12 16:48 UTC
- **Status:** **Live on the Worker** since 2026-11-12 ~17:00 UTC. Waiting on Judith's checks, then cleanup.

## Preflight (2026-11-12)

- **Production Worker serves the template** ("Dentist in Anytown, NY | Sample
  Dental Practice", `tel:+15551234567`, robots.txt sitemap `sampledental.com`).
  PITFALLS #1 again. Live Webflow site: "Articulate Dental Company | Modern
  Dentistry in Chicago, IL".
- Worker vars: `CANONICAL_HOST=` (**empty**), `STRIP_TRAILING_SLASH=true`.
  Confirm the canonical host (www or apex) before cutover.
- Zone pending: public NS already `brit`/`ignacio.ns.cloudflare.com` (moved from
  GoDaddy `ns61/62.domaincontrol.com`), so Cloudflare hadn't re-checked yet.
  Triggered `PUT /zones/{id}/activation_check`. Custom domains need an active zone.
- Cloudflare DNS matches the live answers (A @ 198.202.211.1, www → cdn.webflow.com,
  Google MX, SPF/DMARC, verification TXT, `pay` → GoDaddy paylinks).
- WAF/page rules/rate limits: none. Security level medium, Bot Fight off.

**Unblock:** merge the client build to `main` and redeploy; set `CANONICAL_HOST`;
zone active. Then rerun the preflight and cut over (A @ + CNAME www).

## Preflight rerun (2026-11-12, after Judith's fix)

- Zone active. Worker redeployed 16:58 UTC by Judith; `CANONICAL_HOST=www.articulatedentalco.com`.
- Title "Articulate Dental Company | Modern Dentistry in Chicago, IL", `tel:+18722957133`
  (same number as Webflow), no noindex; sitemap on www (200).
- No WAF rules, page rules or rate limits.

## Cutover (2026-11-12)

Deleted `A @ 198.202.211.1` and `CNAME www cdn.webflow.com`; attached www + apex
to `articulatedentalco-com` (production).

**Verified:** apex → 301 www (path and query kept); http → https; trailing slash
stripped (`/about/` → `/about`); www 200 with Worker title (correct on the third
try, ~1 min, PITFALLS #3); robots.txt and sitemap.xml 200; unknown path 404;
certificates active (Universal + Advanced for www); MX unchanged (5 Google records).

**Cleanup after Judith's OK:** delete `_webflow` TXT, cancel Webflow hosting.

## Log

- 2026-11-12: Preflight failed (template on production, zone pending). Held.
- 2026-11-12: Judith fixed main and CANONICAL_HOST, zone active; preflight passed; cut over and verified.
