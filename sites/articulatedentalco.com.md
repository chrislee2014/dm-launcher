# articulatedentalco.com (Articulate Dental Company, Chicago, IL)

- **Worker:** `articulatedentalco-com` (last deploy 2026-11-04 by Judith, wrangler)
- **Zone:** `983d04ff7ab07b31dba07d3b6a754259`, status **pending** on 2026-11-12
- **Status:** **Blocked at preflight.** DNS not changed.

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

## Log

- 2026-11-12: Preflight failed (template on production, zone pending). Held.
