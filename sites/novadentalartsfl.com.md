# novadentalartsfl.com (Nova Dental Arts, Jacksonville FL)

**Track:** Buildout - launch on Astro (new site; the old site was NOT Webflow). Launched by
hand on 2026-11-18 with Chris's OK after the daily check held it (no Webflow pair).

- Worker `novadentalartsfl-com` (deployed 2026-11-12 by Judith), CANONICAL_HOST=www.novadentalartsfl.com.
- Zone `c6bf1f106a9154f002dbb99071ba08c4`, NS brit/ignacio, active.
- Preflight: "Nova Dental Arts | Dentist in Jacksonville, FL", tel:+19548331824, no sample data /
  Coming Soon / noindex, sitemap on www, no WAF rules.
- Before: apex showed a GoDaddy Website Builder placeholder (title = domain), www connection reset.
- **Snapshot / deleted:** A @ 13.248.243.5, A @ 76.223.105.230 (GoDaddy Website Builder), CNAME www → apex.
  Kept: CNAME _domainconnect, CNAME pay → paylinks.commerce.godaddy.com, TXT _dmarc (p=quarantine),
  TXT google-site-verification. No MX.
- Write check (A re-saved), then attached www + apex as custom domains (production).
- Verified: apex 301 → www (path + query), http → https, www 200 with Worker title on first try,
  robots/sitemap 200, 404 on unknown path. Universal + Advanced (apex) active; www Advanced
  pending_validation. Sheet P=Yes + note.
- Rollback: remove custom domains; recreate A @ 13.248.243.5 + A @ 76.223.105.230 + CNAME www → apex (DNS only).
