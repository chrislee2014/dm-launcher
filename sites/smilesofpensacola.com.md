# smilesofpensacola.com (Perdido Family Dentistry)

- **Worker:** `smilesofpensacola-com`
- **Staging:** https://staging-smilesofpensacola-com.dental-marketing.workers.dev
- **Zone:** `c29b1600c92993f43d9297f3e6801cd5` (Free plan), SSL mode Full
- **Repo:** DentalMarketing-com/smilesofpensacola.com
- **Status:** **Live on the Worker** since 2026-10-24 ~15:04 UTC. Waiting on Judith's final verification, then cleanup (RUNBOOK step 5).

## Zone snapshot (2026-10-24, before cutover)

| Type  | Name                   | Content                         | Proxied | Keep? |
|-------|------------------------|---------------------------------|---------|-------|
| A     | smilesofpensacola.com  | 198.202.211.1 (Webflow)         | no      | delete at cutover |
| CNAME | www                    | cdn.webflow.com                 | no      | delete at cutover |
| CNAME | mail                   | mail.officite.net               | yes     | keep (see PITFALLS #2) |
| MX    | smilesofpensacola.com  | mx.officite.net                 | no      | keep |
| TXT   | smilesofpensacola.com  | google-site-verification=wt1n…  | no      | keep |
| TXT   | smilesofpensacola.com  | v=DKIM1; k=rsa; …               | no      | keep |
| TXT   | _webflow               | one-time-verification=aaa970ba… | no      | delete after launch |

No Worker routes or custom domains on the zone yet; workers.dev is enabled.

## Preflight result (2026-10-24)

- Live Webflow site: "Family Dentist in Pensacola, FL | Perdido Family Dentistry".
- Staging Worker: same title, `tel:+18509898567`. Correct build.
- **Production Worker: template sample data** ("Dentist in Anytown, NY |
  Sample Dental Practice", `tel:+15551234567`, robots.txt sitemap
  `sampledental.com`). Last deploy 2026-10-24 12:57 UTC via wrangler.
- Remote branches: `main` = `preview` = 63db86f (Initial commit);
  `staging` = `development` = 1f6f70c.

**Unblock (done):** merge the client build into `main` (via PR), let Workers Builds
redeploy, rerun the preflight, then follow RUNBOOK steps 2–5.

## Preflight rerun (2026-10-24, after Judith merged to main)

- `main` = `staging` = `development` = 1f6f70c. (`preview` is still 63db86f; it doesn't affect production.)
- Production deploy 14:59 UTC via wrangler by Judith. Var `CANONICAL_HOST=www.smilesofpensacola.com`.
- Title "Family Dentist in Pensacola, FL | Perdido Family Dentistry", `tel:+18509898567`, no noindex.
- robots.txt sitemap → `www.smilesofpensacola.com/sitemap.xml`; sitemap 200, 44 URLs on www.
- Sample `_redirects` rules return 301 to the expected targets.

## Cutover (2026-10-24 ~15:04 UTC, via API)

1. Deleted `A @ 198.202.211.1` (id b25371bf…) and `CNAME www cdn.webflow.com` (id 1e190726…).
2. `PUT /accounts/{id}/workers/domains` for `www.smilesofpensacola.com` then
   `smilesofpensacola.com` → `smilesofpensacola-com` (production). Cloudflare
   created proxied `AAAA 100::` records for both.
3. Downtime was seconds: both API calls ran back to back in one script.

**Verified:**
- `https://smilesofpensacola.com/` → 301 `https://www.smilesofpensacola.com/`; path and query kept.
- `http://` → 301 https on both hosts.
- www serves the Perdido build (title, `tel:(850)989-8567`).
- `_redirects` samples: `/articles/general/502365-abscessed-tooth` → `/`, `/doctor-individual-change-to-doctors-name` → `/dr-john-ledford`.
- robots.txt and sitemap.xml 200; unknown path 404.
- Certificates: Universal pack (apex + `*.smilesofpensacola.com`) active; two Advanced packs still initializing at check time.
- Zone has no redirect rulesets or page rules; MX, `mail`, DKIM and google-site-verification untouched.

**Left for Judith:** phones/DNI, forms, the blog rebuild hook, and her final stage.

**Cleanup after her OK:** delete `_webflow` TXT (id 21b4d9a7…), cancel Webflow hosting.

## Log

- 2026-10-24: Preflight failed (production on template). Cutover held; told Judith.
- 2026-10-24: Judith merged the build to main; preflight rerun passed.
- 2026-10-24: DNS cutover done; apex/www live on the Worker. Handed to Judith for final verification.
