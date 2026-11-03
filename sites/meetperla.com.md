# meetperla.com (Perla, DentalMarketing.com product site)

- **Worker:** `meetperla-com` (https://meetperla-com.dental-marketing.workers.dev)
- **Zone:** `857ad0ee6eeee6c755af66210ca6be56` (Free plan), SSL mode Flexible
- **Repo:** DentalMarketing-com/meetperla.com (Astro port of the Webflow site "perla-staging", `695155b753ea2b43981dcfb6`)
- **Status:** **Live on the Worker** since 2026-11-03 ~00:55 UTC. Cleanup (RUNBOOK step 5) pending.

## Zone snapshot (2026-11-03, before cutover)

| Type  | Name                       | Content                                   | Proxied | Keep? |
|-------|----------------------------|-------------------------------------------|---------|-------|
| A     | meetperla.com              | 198.202.211.1 (Webflow)                   | no      | deleted at cutover |
| CNAME | www                        | cdn.webflow.com                           | no      | deleted at cutover |
| CNAME | admin, leune, my, sharedpractices, signup | cname.vercel-dns.com      | no      | keep |
| CNAME | allegra                    | 055b7e363eebbe10.vercel-dns-016.com (ttl 600) | no  | keep |
| CNAME | _domainconnect             | _domainconnect.gd.domaincontrol.com       | no      | keep |
| CNAME | 3 × `*._domainkey.my`      | *.dkim.amazonses.com                      | no      | keep |
| MX    | email.my                   | feedback-smtp.us-east-1.amazonses.com (10) | no     | keep |
| TXT   | _dmarc.my                  | v=DMARC1; p=none;                         | no      | keep |
| TXT   | email.my                   | v=spf1 include:amazonses.com ~all         | no      | keep |
| TXT   | meetperla.com              | google-site-verification=LiTWHuoT…        | no      | keep |
| TXT   | _vercel                    | vc-domain-verify=allegra.meetperla.com,…  | no      | keep |
| TXT   | _webflow                   | one-time-verification=ea5e23d5…           | no      | delete after launch |

No apex MX: no mail on the apex.

## Preflight (2026-11-03)

- Production Worker: "Perla | AI-Powered Dental Marketing Agents for your Dental Practice", robots.txt sitemap on www.meetperla.com, no noindex on the custom domain. `main` = 53a4fdc.
- WAF custom / managed rules, rate limits, transform and origin rules: none. Security level medium. Bot fight mode off.
- **Page rule** `www.meetperla.com/signup` → 301 `https://signup.dentalmarketing.com/plan/ai`: dormant while www was DNS-only (live returned 404). Its target has an **expired certificate**, so it was **disabled** (not deleted; id `a03930d77351b944d83af97c6c012a68`) to keep live behavior. Re-enable once the target works, if wanted.

## Cutover (2026-11-03 ~00:55 UTC)

Deleted the two Webflow records, attached Worker custom domains `www.meetperla.com` and `meetperla.com` (Cloudflare created proxied AAAA 100:: records + certs).

## Verification (2026-11-03, after ~2 min of DNS propagation)

- First checks still hit Webflow (`x-wf-region` header) for ~2 minutes (PITFALLS #3); then all from the Worker.
- `https://meetperla.com/*`, `http://meetperla.com/*`, `http://www…` → one 301 to `https://www.meetperla.com/…`; `/seo/` → `/seo`.
- All 7 pages 200 from the Worker, `/nope` and `/signup` 404, `/sitemap.xml` → `/sitemap-index.xml` (7 URLs), robots.txt OK, no `x-robots-tag` on the custom domain, no Webflow CDN references.
- Untouched Vercel subdomains: `signup.meetperla.com` 200. `my.meetperla.com` and `admin.meetperla.com` serve **expired certificates** (pre-existing, Vercel side; DNS unchanged).

## Rollback

Remove the two Worker custom domains, recreate `A meetperla.com 198.202.211.1` and `CNAME www cdn.webflow.com` (DNS only). Works only while Webflow hosting for "perla-staging" exists.

## Cleanup (pending, after a few days live)

- Delete TXT `_webflow.meetperla.com`.
- Cancel Webflow hosting / delete the "perla-staging" site.
