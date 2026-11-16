# zurcherdentalesthetics.com (Zurcher Dental Esthetics, Gallatin, TN)

_Copied from the daily check's Slack thread (2026-11-16); the scheduled session couldn't push._

- **Worker:** `zurcherdentalesthetics-com` (deployed 2026-11-12 17:07 UTC by Judith)
- **Zone:** `57b61016ae709354c5cc2bc974246ab5`, NS cash/tia.ns.cloudflare.com (from GoDaddy
  ns01/02.domaincontrol.com; registry change 2026-11-16 14:24 UTC), active 14:44 UTC after
  activation_check. Sheet row 41.
- **Preflight:** title "Dentist in Gallatin, TN | Zurcher Dental Esthetics", tel:+16159092158
  (same as Webflow). No sample data ("555-" hits were SVG paths), no Coming Soon, no noindex
  meta (x-robots-tag noindex is on workers.dev only). Sitemap on www.
  CANONICAL_HOST=www.zurcherdentalesthetics.com. No WAF, rate limits or page rules; security
  level medium, Bot Fight off. No other records on Webflow. Branch check not possible (no
  GitHub access to the site repo); production content matched live Webflow.
- **Snapshot:** A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME
  _domainconnect → gd; MX smtp.google.com; 2× _dmarc TXT; google._domainkey DKIM; _webflow TXT;
  2× google-site-verification; SPF.
- **Cutover ~14:45 UTC:** write check OK (A @ re-saved). Deleted www + apex, attached www then
  apex as custom domains (production).
- **Verified:** apex 301 → www (path + query kept), http → https, www 200 with Worker title, no
  Webflow headers, robots/sitemap 200, 404 for an unknown path, Universal + Advanced certs
  active (www Advanced pack pending_validation), MX unchanged.
- **Flags (pre-existing, not touched):** two `_dmarc` records (p=none + p=quarantine; two DMARC
  records make DMARC invalid) and SPF typo `~alll`.
- **Alias:** michaelzurcherdds.com broke the same day; see sites/michaelzurcherdds.com.md.
- **Rollback:** remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
