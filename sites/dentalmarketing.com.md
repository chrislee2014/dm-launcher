# dentalmarketing.com (agency site)

- **Worker:** `dentalmarketing-com` (https://dentalmarketing-com.dental-marketing.workers.dev)
- **Zone:** `3615d25778dcffa537b03d38014dc344` (Free plan), SSL mode Flexible, Always Use HTTPS off (the Worker 301s http)
- **Repo:** DentalMarketing-com/dentalmarketing.com (Astro port of the Webflow site "Dental Marketing", `675ed97f5fafbd1f37a996ce`); blog in Sanity `kzjcwtn0`; leads in D1 `dentalmarketing-com-leads` + Mailgun
- **Status:** **Live on the Worker** since 2026-11-03 (~1 min of propagation). Cleanup (RUNBOOK step 5) pending.

## Zone snapshot (2026-11-03, before cutover): records changed

| Type  | Name                    | Content                                              | Proxied | Action |
|-------|-------------------------|------------------------------------------------------|---------|--------|
| A     | dentalmarketing.com     | 198.202.211.1 (Webflow)                              | no      | deleted at cutover |
| CNAME | www                     | cdn.webflow.com                                      | no      | deleted at cutover |
| CNAME | _acme-challenge.www     | 360e3c7d-0aa6-49bc-8d5d-7b47cd5818ba.stackpath-tls.com | no    | deleted at cutover (stale cert-validation delegation from an earlier host; a CNAME there blocks TXT validation for www) |
| TXT   | _webflow.www            | one-time-verification=42ff7fbd…                      | no      | delete after launch |
| TXT   | _webflow.pap            | one-time-verification=a4de9816…                      | no      | delete after launch (pap is on Vercel) |

The other 96 records were left as is: Google Workspace MX on the apex (5), Mailgun `mg`, SES `my`/`app`/`billing`, HubSpot/Mailchimp/Mandrill DKIM, SPF/DMARC, Stripe `billing`, ~20 Vercel subdomains (pap, wizard, my, start, signup, try…), `grow` (HubSpot), `report`, `es` (Weglot), `recordings` (Worker r2-audio-proxy), `dni-script` (R2), `meeting` (page rule → HubSpot meetings), analytics/onboarding A records. Full export of all 101 records: in the session that did the cutover; recreate from this table + Cloudflare audit log if needed.

## Preflight (2026-11-03)

- Webflow last published 2026-09-01 (same version ported); no Webflow blog posts newer than the Sanity import.
- Production Worker: "Dental Marketing | The 5-C Method for Dental Marketing®", `tel:855-980-0091`, robots sitemap on www; `main` = 74baec6.
- WAF custom rules, rate limits, transforms, origin, cache rules: none. Dynamic redirect "Try to Wizard" (try.dentalmarketing.com only) and page rule meeting.dentalmarketing.com → HubSpot meetings: neither matches www/apex. Security medium, browser check on. No CAA records.
- Certificates: Universal (apex + `*.dentalmarketing.com`, Google, active) + advanced pack for recordings.

## Cutover (2026-11-03)

Deleted the three records above, attached Worker custom domains `www.dentalmarketing.com` and `dentalmarketing.com`.

## Verification (2026-11-03)

- Public DNS on Cloudflare after ~55 s; apex MX intact (5 Google records).
- apex / http → one 301 to `https://www.dentalmarketing.com/…`; `/about/` → `/about`; `/blog?4dc2aabd_page=3` → `/blog/page/3`.
- Webflow 301 list: `/about-us`, `/results`, `/NewPatientPlan` (→ pap), `/roi` (→ Vercel calculator) all correct.
- 19 pages across every template 200 from the Worker (no `x-wf-region`, no noindex); `/nope` 404; robots + sitemap OK; blog images from Sanity CDN; form API answers (422 on a bad email).
- Untouched subdomains: pap, wizard, my 200; try 301 (redirect rule); grow 404 (HubSpot side, record unchanged).
- Vimeo embeds: not verifiable from the cloud sandbox (Vimeo serves its bot challenge to datacenter IPs for any referer). Check in a real browser.

## Rollback

Remove the two Worker custom domains, recreate `A dentalmarketing.com 198.202.211.1` and `CNAME www cdn.webflow.com` (DNS only). Works only while Webflow hosting for "Dental Marketing" exists.

## Cleanup (pending, after a few days live)

- Delete TXT `_webflow.www` and `_webflow.pap`.
- Sanity webhook → Workers Builds Deploy Hook "Sanity publish" (still to create in Sanity).
- Export Webflow form submissions + CMS CSVs, then delete the Webflow sites "Dental Marketing" and "PATIENT ACCELERATOR" (pap is served by Vercel).
