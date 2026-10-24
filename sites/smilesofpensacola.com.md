# smilesofpensacola.com (Perdido Family Dentistry)

- **Worker:** `smilesofpensacola-com`
- **Staging:** https://staging-smilesofpensacola-com.dental-marketing.workers.dev
- **Zone:** `c29b1600c92993f43d9297f3e6801cd5` (Free plan), SSL mode Full
- **Repo:** DentalMarketing-com/smilesofpensacola.com
- **Status:** Preflight passed (2026-10-24 rerun). Ready for DNS cutover; DNS not changed yet.

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

## Log

- 2026-10-24: Preflight failed (production on template). Cutover held; told Judith.
- 2026-10-24: Judith merged the build to main; preflight rerun passed.
