# relaxandsmile.com (Relax and Smile Dental Care, Downtown Miami)

_Copied from the daily check's Slack thread (2026-11-16); the scheduled session couldn't push._

- **Worker:** `relaxandsmile-com` (deployed 2026-11-12 17:11 UTC by Judith)
- **Zone:** `fc26d542bdd8bd165083a4cf7560292e`, NS cash/tia.ns.cloudflare.com (from GoDaddy
  ns17/18.domaincontrol.com; registry change 2026-11-16 14:27 UTC), active 14:44 UTC after
  activation_check. Sheet row 94.
- **Preflight:** title "Relax and Smile Dental Care | Trusted Dentist in Downtown Miami",
  tel:+17869984212 (same as Webflow). No sample data, no Coming Soon, no noindex meta. Sitemap
  on www. CANONICAL_HOST=www.relaxandsmile.com. No WAF, rate limits or page rules; security
  level medium, Bot Fight off. No other records on Webflow (`pay` → GoDaddy paylinks,
  untouched). Branch check not possible; content matched live Webflow.
- **Snapshot:** A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME
  _domainconnect → gd; CNAME pay → paylinks.commerce.godaddy.com; 5 Google MX; SPF + _spfm TXT;
  _dmarc; DKIM; 2× google-site-verification; _webflow TXT.
- **Cutover ~14:45 UTC:** write check OK. Deleted www + apex, attached www then apex (production).
- **Verified:** apex 301 → www (path + query kept), http → https. www served Webflow for about
  1 minute (PITFALLS #3), then 200 with Worker title and no Webflow headers. robots/sitemap 200,
  404 for an unknown path, Universal + Advanced certs active (www Advanced pending_validation),
  MX unchanged (5).
- **Rollback:** remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
