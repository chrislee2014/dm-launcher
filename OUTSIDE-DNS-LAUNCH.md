# Launching a site when we can't change the DNS

Use this for a client whose nameservers can't move to our Cloudflare account.
Typical reasons: the registrar account belongs to the client and we have no
login, the DNS host won't release the zone, or the client won't approve a
nameserver change. Reference launch: **robinwoodsmiles.com** (2026-11-19).

**How to use this file:** give it to a Claude Code session with a request like
"Walk me through launching `<domain>` using OUTSIDE-DNS-LAUNCH.md". Claude does
the Cloudflare side, and tells you exactly which records to change at the
client's DNS host and in Redirect Pizza.

---

## Instructions for Claude

You are walking a teammate through this launch. Work one phase at a time.
Before you change anything, show what you're about to do. Then verify the
result before you move on. Ask the user for anything only they can do or
see: the client's DNS host, the Redirect Pizza dashboard, and approvals.

**Pick your toolset once, at the start:**

1. **Cloudflare MCP available** (a tool that runs Cloudflare API requests,
   e.g. `mcp__CloudFlare_MCP__execute`): make the REST calls below through it.
2. **No MCP, but `CLOUDFLARE_API_TOKEN` is set** in the environment: use the
   `curl` commands below.
3. **Neither:** give the user the dashboard steps (each step lists them) and
   have them paste back what they see.

Check access before Phase 1. With MCP, run its `whoami` or equivalent. With
curl, call `GET /accounts/$ACCOUNT/workers/scripts/saas-router`: a 200 means
the token can do the Worker part. The token needs **Workers Scripts: Edit**
on the account and **SSL and Certificates: Edit** on the dentalmarketing.com
zone (custom hostnames live there).

**Hard rules:**
- Never touch MX, TXT/SPF/DKIM, or any record other than the ones named here.
  The client's email must keep working.
- Never delete a Cloudflare zone, a custom hostname, or a Worker without the
  user's explicit OK.
- Never disable WAF, Bot Fight Mode or other security settings.
- Never paste API tokens into chat or files.
- When you redeploy `saas-router`, you must send **every** existing binding,
  not just the new one. An upload replaces the whole binding list, so a
  missing binding takes another client's site down.

---

## How it works

```
visitor ─► www.<domain>  (CNAME at the client's DNS host)
              │
              ▼
        sites.dentalmarketing.com   (Cloudflare for SaaS fallback origin)
              │  custom hostname www.<domain> → certificate issued by Cloudflare
              ▼
        Worker "saas-router"  ─(service binding)─►  client site Worker (e.g. robinwoodsmiles-com)

visitor ─► <domain> (bare/apex)  ─A record─►  Redirect Pizza ─301─► https://www.<domain>
```

- **Cloudflare for SaaS** runs on the **dentalmarketing.com** zone. It's
  already set up; don't change it:
  - Zone id `3615d25778dcffa537b03d38014dc344`.
  - Account id `d846903de770bbb35d01ffe32db0a01f`.
  - Fallback origin and CNAME target: `sites.dentalmarketing.com`. This is a
    proxied placeholder A 192.0.2.1 and is never served directly.
  - Two Worker routes on that zone: `*dentalmarketing.com/*` runs no Worker
    (an exclusion, so our own hostnames are untouched), and `*/*` runs
    `saas-router`.
- **saas-router** (source: `tools/saas-router/`) maps each client hostname to
  the client's site Worker. Unknown hostnames get a 404, never another
  client's site.
- **The apex can't be a CNAME** at most DNS hosts, and SaaS custom hostnames
  need a CNAME. So the site lives on `www`, and the bare domain goes to
  Redirect Pizza, which 301s to `https://www.<domain>` with its own
  certificate.

Fill these in at the start and reuse them:

```bash
ACCOUNT=d846903de770bbb35d01ffe32db0a01f
SAAS_ZONE=3615d25778dcffa537b03d38014dc344
DOMAIN=example.com                 # the client's domain, no www
WORKER=example-com                 # the client's site Worker (domain with dots → dashes)
BINDING=EXAMPLECOM                 # uppercase, letters/digits/_ only, unique in saas-router
CF="https://api.cloudflare.com/client/v4"
H="Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

---

## Phase 0: Preflight (change nothing)

1. **Confirm this path is actually needed.** Ask whether the nameservers
   really can't move. A normal zone launch (RUNBOOK.md) is simpler and
   preferred.
2. **Look at the current DNS** (public lookups, from any machine):
   ```bash
   for t in A AAAA CNAME MX TXT CAA NS; do echo "== $t"; dig +short $t $DOMAIN; done
   dig +short CNAME www.$DOMAIN
   ```
   Or use `https://dns.google/resolve?name=<name>&type=<type>` if `dig` is
   missing. Record:
   - Who hosts the DNS (the NS records). That's where the user makes the
     changes.
   - The current apex A record and www target (usually Webflow:
     `198.202.211.1` and `cdn.webflow.com`). These are your rollback values.
   - Whether MX records exist. If they do, call out to the user that email
     must not be touched.
   - **CAA records.** If any exist, they must allow the certificate
     authorities Cloudflare uses (`letsencrypt.org`, `pki.goog`,
     `ssl.com`) and Redirect Pizza's (`letsencrypt.org`). Otherwise
     certificates won't issue. Tell the user what to add before going on.
3. **The site Worker is ready.** Same content checks as RUNBOOK.md:
   - `https://<WORKER>.dental-marketing.workers.dev` shows the client's real
     content: no template/"Sample Dental", no 555 numbers, no `noindex`.
   - Sitemap and robots load.
   - The Worker's `CANONICAL_HOST` variable is `www.<domain>`. Check it in
     the dashboard (Worker → Settings → Variables), or via
     `GET $CF/accounts/$ACCOUNT/workers/scripts/$WORKER/settings`.
   - Template or config problems go to Judith; don't launch.
4. **No stale zone for this domain in our account.** Check with
   `GET $CF/zones?name=$DOMAIN`. If a pending zone exists, tell the user. A
   leftover zone is the suspected cause of Robinwood's outage (see Pitfalls
   below). Deleting it needs their OK.
5. **No existing custom hostname** for www.<domain>. Check with
   `GET $CF/zones/$SAAS_ZONE/custom_hostnames?hostname=www.$DOMAIN`.

Report the preflight results and get the user's go-ahead.

---

## Phase 1: Create the custom hostname (no visitor impact)

**API:**
```bash
curl -s -X POST -H "$H" -H "Content-Type: application/json" \
  "$CF/zones/$SAAS_ZONE/custom_hostnames" \
  --data "{\"hostname\":\"www.$DOMAIN\",\"ssl\":{\"method\":\"http\",\"type\":\"dv\",\"settings\":{\"min_tls_version\":\"1.2\"}}}"
```
Save the returned `result.id` (the custom hostname id).

**Which validation method:**
- **`http`** (the default here): the certificate issues automatically
  within minutes once the www CNAME points at us. Nothing extra for the
  client to add. Use this when the user will make the CNAME change
  directly, like Robinwood.
- **`txt`** (zero-downtime option): use it if the client can add TXT records
  a day early. The response's `ownership_verification` and
  `ssl.validation_records` list the records to add: a
  `_cf-custom-hostname.www` TXT and the `_acme-challenge.www` TXT values.
  Wait until both hostname and SSL show **active** before Phase 3. Then
  https works from the first second after the CNAME switch.

**Dashboard fallback:** dentalmarketing.com zone → SSL/TLS → Custom Hostnames
→ Add Custom Hostname → `www.<domain>`, validation HTTP (or TXT).

**Note:** you can't choose the certificate authority (that's Enterprise
only). Cloudflare picks one.

---

## Phase 2: Route the hostname to the site (no visitor impact yet)

Nothing reaches saas-router for this hostname until the CNAME changes, so
this is safe to deploy now.

1. Edit `tools/saas-router/worker.js`: add `"www.<domain>": "<BINDING>"` to
   `SITES`.
2. Edit `tools/saas-router/metadata.json`: add
   `{"type":"service","name":"<BINDING>","service":"<WORKER>","environment":"production"}`
   to `bindings`.
3. **Compare against what's live first**, so you don't drop a binding someone
   added outside the repo:
   ```bash
   curl -s -H "$H" "$CF/accounts/$ACCOUNT/workers/scripts/saas-router/settings" \
     | python3 -c "import sys,json;print(sorted(b['name'] for b in json.load(sys.stdin)['result']['bindings']))"
   ```
   Every live binding must also be in metadata.json. If one isn't, add it
   and tell the user.
4. Deploy:
   ```bash
   cd tools/saas-router
   curl -s -X PUT -H "$H" "$CF/accounts/$ACCOUNT/workers/scripts/saas-router" \
     -F "metadata=@metadata.json;type=application/json" \
     -F "worker.js=@worker.js;type=application/javascript+module" \
     | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['success'],d.get('errors'))"
   ```
   With MCP, send the same multipart upload through its API tool. In the
   dashboard: Workers & Pages → saas-router → Settings → Bindings → Add →
   Service binding (name `<BINDING>`, service `<WORKER>`), then Edit code →
   add the `SITES` line → Deploy.
5. Re-run step 3's command and confirm the new binding is there with all the
   old ones. Check that existing SaaS clients still load (see the Clients
   table in `tools/saas-router/README.md`).
6. Commit the two files to dm-launcher.

---

## Phase 3: DNS change at the client's DNS host (the user does this)

Give the user these exact records. Change **only these two**:

| Host | Type | Old value (rollback) | New value | TTL |
|---|---|---|---|---|
| `www` | CNAME | `cdn.webflow.com` (as recorded in Phase 0) | `sites.dentalmarketing.com` | lowest allowed |
| `@` (apex) | A | `198.202.211.1` (as recorded) | the IP Redirect Pizza shows (Phase 4; was `89.106.200.1` for Robinwood) | lowest allowed |

- Do the Redirect Pizza setup (Phase 4) **first**, or at the same time, so
  the apex record has somewhere to point.
- If the apex has more than one A record, or any AAAA records, pointing at
  the old host, they all go. Leave records for other hosts, and all
  MX/TXT, alone.
- With `http` validation, https on www may error for a few minutes until the
  certificate issues. In practice Robinwood visitors kept seeing Webflow
  from cached DNS until it was ready. Prefer launching outside office hours.

**Watch it go active:**
```bash
CH=<custom hostname id>
for i in $(seq 1 30); do
  curl -s -H "$H" "$CF/zones/$SAAS_ZONE/custom_hostnames/$CH" \
   | python3 -c "import sys,json;r=json.load(sys.stdin)['result'];print(r['status'],r['ssl']['status'],r.get('verification_errors') or '')"
  sleep 30
done
```
Done when it shows `active active`. If it's stuck at `pending` for more than
30 minutes, check the CNAME publicly (`dig +short CNAME www.$DOMAIN`). If
the CNAME is right but SSL is stuck in `pending_validation` on `txt`, switch
to `http`:
```bash
curl -s -X PATCH -H "$H" -H "Content-Type: application/json" \
  "$CF/zones/$SAAS_ZONE/custom_hostnames/$CH" \
  --data '{"ssl":{"method":"http","type":"dv","settings":{"min_tls_version":"1.2"}}}'
```

---

## Phase 4: Redirect Pizza (bare domain → www)

Redirect Pizza (redirect.pizza) forwards the apex with a real certificate.
Registrar "domain forwarding" often has no https, so don't use it. The
user does this in the Redirect Pizza dashboard; Claude gives the values and
checks the result.

1. Log in to redirect.pizza with the Dental Marketing team account
   (ask Judith if you don't have access).
2. **Add a new redirect:**
   - **Source:** `<domain>` (the bare domain only. Don't add `www`; it
     belongs to Cloudflare now).
   - **Destination:** `https://www.<domain>`.
   - **Redirect type:** 301 (permanent).
   - **Path forwarding:** on, so `/services/x` → `https://www.<domain>/services/x`.
   - **Query string forwarding:** on (keeps UTM/gclid tracking on ad clicks).
   - Save.
3. Redirect Pizza then shows the DNS record to create for the source:
   - For an apex, it's an **A record** to its IP. It was `89.106.200.1`
     for Robinwood. Always use the value the dashboard shows, not this
     document.
   - For a subdomain source (like `promo.<domain>`), it's a CNAME to
     `edge.redirect.pizza`.
   - That record is the apex row in the Phase 3 table.
4. After the DNS change, Redirect Pizza issues the source's certificate on
   its own. The dashboard shows the source as active / SSL issued, usually
   within minutes.
5. **Promo subdomains:** if the client also has `promo.<domain>` or
   `visit.<domain>` mailer links pointing at Webflow, they get their own
   redirect in Redirect Pizza (source `promo.<domain>`, destination
   whichever landing page Judith names). That's Judith's step. List them
   for her; don't change them yourself.

---

## Phase 5: Verify

Run all of these and show the results:

```bash
for u in https://www.$DOMAIN/ http://www.$DOMAIN/ https://$DOMAIN/ http://$DOMAIN/ \
         "https://$DOMAIN/some/path?utm_source=test"; do
  echo "$u -> $(curl -s -o /dev/null --max-time 15 -w '%{http_code} %{redirect_url}' "$u")"
done
curl -s https://www.$DOMAIN/ | grep -o '<title>[^<]*'
curl -s -o /dev/null -w 'robots %{http_code}\n'  https://www.$DOMAIN/robots.txt
curl -s -o /dev/null -w 'sitemap %{http_code}\n' https://www.$DOMAIN/sitemap-index.xml
curl -s -o /dev/null -w '404 page %{http_code}\n' https://www.$DOMAIN/definitely-not-a-page
```

**Expected:**
- `https://www` → 200, with the client's title.
- `http://www` → 301 to https.
- Both apex URLs → 301 to `https://www.<domain>/`.
- The path+query URL keeps `/some/path?utm_source=test`.
- robots and sitemap → 200.
- The unknown path → 404.
- MX unchanged (compare with Phase 0).

**Note:** if you run this from a Claude cloud sandbox, its HTTPS proxy
re-signs certificates, so the certificate details you see there aren't the
real ones (PITFALLS #4). For a real certificate check, use
`https://www.ssllabs.com/ssltest/` or the user's browser.

---

## Phase 6: Record it

1. Add a row to the **Clients** table in `tools/saas-router/README.md`:
   domain, custom hostname id, launch date/time. Add a short notes block
   covering:
   - Registrar and DNS host.
   - MX yes/no.
   - Redirect Pizza IP.
   - Rollback values.
2. Mark the sheet: column P = Yes, with a column Q note "Outside-DNS launch
   (Cloudflare for SaaS + Redirect Pizza); nameservers not moved". Column O
   stays blank. Use the n8n broker, as DAILY-CHECK.md describes.
3. DM Judith that it's live (and about any promo subdomains for Redirect
   Pizza).
4. Commit and push dm-launcher.

---

## Rollback

Only works while the Webflow hosting is still active:

1. At the client's DNS host, put the Phase 0 values back: `www` CNAME →
   `cdn.webflow.com`, apex A → `198.202.211.1`.
2. Optionally pause the redirect in Redirect Pizza.
3. Leave the custom hostname and the saas-router entry in place. They're
   harmless with no traffic. Remove them only with the user's OK, and
   redeploy saas-router with all the other bindings intact.

---

## Pitfalls specific to this path

- **Hostname flips to "moved" and the certificate is deleted** (Robinwood,
  2026-11-19, the day of launch):
  - Symptom: https fails the handshake and http returns **409**, even though
    the CNAME is correct.
  - Fix: re-issue SSL with the PATCH in Phase 3. It went active again in
    about 75 seconds.
  - Suspected cause: a never-activated pending zone for the same domain in
    our account.
  - Prevention: check for stale zones in Phase 0, and include SaaS
    hostnames in the daily sweep (status must be `active` / `active`).
- **409 from Cloudflare on http** generally means the hostname isn't an
  active custom hostname on our SaaS zone. Check its status before anything
  else.
- **CAA records** at the client's DNS host silently block certificate
  issuance (Phase 0, step 2).
- **Redeploying saas-router without every binding** takes other outside-DNS
  clients offline (Phase 2, step 3).
- **Don't create a regular zone for this domain** in our account "just to
  stage records". That's how the stale Robinwood zone happened.
- **Apex forwarding at the registrar** usually has no https. Use Redirect
  Pizza.
- **Webflow:** once the site is verified live, the domain can be removed from
  the Webflow project. Don't cancel Webflow hosting until every alias and
  promo subdomain for the client has moved (PITFALLS #7).
