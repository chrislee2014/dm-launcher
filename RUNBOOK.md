# Cutover runbook: Webflow → Cloudflare Worker

## 0. Preflight (do not skip; see PITFALLS #1)

Before you touch DNS, confirm that **production is the client's build**, not
the template:

```sh
W=https://<worker>.dental-marketing.workers.dev
curl -s $W/ | grep -oE '<title>[^<]*</title>|tel:[0-9+]+' | sort -u
curl -s $W/robots.txt            # Sitemap: must be the client's domain
```

- The title names the client's practice and city (not "Sample Dental Practice"
  or "Anytown").
- The phone numbers are the client's numbers (not 555).
- It matches what the staging URL shows: `git ls-remote origin` shows `main`
  and `staging` on the same commit, or `main` ahead of it.
- No Coming Soon, landing, or promo mode is left on in the production env vars
  unless that's intended.

## 1. Snapshot the zone

Record every DNS record (type, name, content, proxied, TTL) in the site log
before you change anything. This is the rollback.

## 2. Remove the Webflow web records

Delete **only**:
- the `A` record on the apex → Webflow IP (e.g. `198.202.211.1`)
- the `CNAME www` → `cdn.webflow.com`

Leave mail (MX, `mail` CNAME), DKIM/SPF/DMARC TXT, and verification TXT alone.
A Worker custom domain can't be added while a conflicting record exists, so do
steps 2 and 3 back to back: the site is down in between.

## 3. Attach the Worker custom domains

Workers & Pages → `<worker>` → Settings → Domains & Routes → Add → Custom
domain: `www.<domain>`, then `<domain>`. Cloudflare creates the DNS records and
the certificates. (API: `PUT /accounts/{id}/workers/domains` with
`{hostname, service, zone_id, environment: "production"}`.)

## 4. Verify

- `https://<domain>/` → 301 → `https://www.<domain>/` (the Worker does this)
- `https://www.<domain>/` 200, served by the Worker, valid cert
- the old Webflow URLs from `public/_redirects` return 301s to the right pages
- phone numbers/DNI swap, booking and forms submit, blog rebuild hook fires
- `robots.txt` and `sitemap.xml` use the client's domain
- email still flows (MX unchanged)

## 5. Clean up (after verification only)

- Remove the `_webflow` verification TXT.
- Cancel Webflow site hosting.
- Write the site log in `sites/`.

## Rollback

Remove the Worker custom domains, then recreate the two Webflow records from
the snapshot (`A @ 198.202.211.1`, `CNAME www cdn.webflow.com`, DNS only).
Webflow keeps serving as long as hosting isn't cancelled, so cancel it last.
