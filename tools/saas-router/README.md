# Outside-DNS launches (Cloudflare for SaaS)

For clients whose nameservers can't move to our Cloudflare (registrar we can't access, Wix plan, etc.).
Enabled on the **dentalmarketing.com** zone by Chris, 2026-11-19.

- **CNAME target / fallback origin:** `sites.dentalmarketing.com` (A 192.0.2.1, proxied; never served directly).
- **Routes on dentalmarketing.com:** `*dentalmarketing.com/*` → no Worker (exclusion: keeps every
  dentalmarketing.com hostname, incl. dni-script and recordings, untouched) and `*/*` → `saas-router`.
- **saas-router** (`worker.js`): maps custom hostname → service binding to the client's site Worker;
  unknown hostnames get 404. Deploy: `metadata.json` + `worker.js` multipart PUT to
  `/accounts/{id}/workers/scripts/saas-router`.

## Adding a client
1. `POST /zones/{dentalmarketing.com}/custom_hostnames` `{hostname:"www.<domain>", ssl:{method:"txt",type:"dv"}}`.
2. Add the hostname to `SITES` in worker.js and a `service` binding in metadata.json; redeploy.
3. Client DNS, phase 1 (no impact): TXT `_cf-custom-hostname.www` (ownership) + the `_acme-challenge.www`
   TXT values. Wait until the custom hostname's SSL is **active**.
4. Phase 2: `www` CNAME → `sites.dentalmarketing.com`; bare domain → registrar/DNS-host forwarding to
   `https://www.<domain>` (check it works over https). The site Worker needs CANONICAL_HOST=www.<domain>.

## Clients
| Domain | Custom hostname id | Status |
|---|---|---|
| www.robinwoodsmiles.com | b54fafd1-1966-489b-9293-4f971e6b582f | **live 2026-11-19 ~13:50 ET** (see below) |

## robinwoodsmiles.com launch notes (2026-11-19)

- Registrar GoDaddy (client account, no access); DNS at Network Solutions (worldnic). No MX.
- Chris made the phase-2 changes directly (skipped the phase-1 TXT records): `www` CNAME →
  sites.dentalmarketing.com; apex A → 89.106.200.1 (redirect.pizza: 301 → https://www.robinwoodsmiles.com,
  path + query forwarding, SSL by redirect.pizza).
- Hostname went active on the CNAME. SSL was on TXT validation, so switched it to **HTTP** validation
  (`PATCH ssl.method=http`); SSL.com issued ~8 min later. Lesson: if the client goes straight to the
  CNAME, use HTTP validation. Choosing the CA (google) is Enterprise-only.
- Visitors kept getting Webflow until the hostname went active, then the Worker; no error window seen.
- Verified: www 200 from Worker, http → https, apex http/https → www with path + query, robots/sitemap 200,
  404 on unknown path. Sheet P=Yes + note (O will stay blank: no nameserver switch). Judith DM'd.
- Rollback: www CNAME → cdn.webflow.com and apex A → 198.202.211.1 at Network Solutions (only while
  Webflow hosting is still active).
