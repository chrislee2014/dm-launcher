# Pitfalls

## 1. "Live on main" but main is still the template

**Site:** smilesofpensacola.com, 2026-10-24.
The production Worker was deployed and returning 200, but `main` was still the
template's `Initial commit`; the client build only existed on
`staging`/`development`. Production served "Sample Dental Practice, Anytown,
NY", `tel:+15551234567`, and a sitemap pointing at `sampledental.com`.
A 200 from the workers.dev URL proves nothing about content.
**Catch it:** the RUNBOOK preflight (title, phone, robots.txt, and
`git ls-remote` for main vs staging) before anyone deletes a DNS record.

## 2. Mail CNAME is proxied

On smilesofpensacola.com, `mail` → `mail.officite.net` has the orange cloud
on. Cloudflare's proxy only handles HTTP(S), so a mail client that connects to
`mail.<domain>` for IMAP/SMTP fails. Webmail over HTTPS may be the only use.
The cutover doesn't affect this, but don't copy the pattern. Ask before
changing it on a live client.

## 3. Right after cutover, some checks still hit Webflow

**Site:** smilesofpensacola.com, 2026-10-24.
In the first minute after the switch, one request got Webflow's old 301
(`/doctor-individual-…` → `/our-doctor`, which 404s on the new site), while the
Worker serves `/dr-john-ledford`. A minute later it was correct. Cache or
propagation can mix the two, even with proxied records.
**Catch it:** before calling a redirect broken, check
`curl -sI` headers on the live host and on workers.dev side by side, then
retest a couple of minutes later. Only report a failure that's still there.

## 4. Certificate checks from a sandbox/corporate proxy lie

`openssl s_client` from a machine behind a TLS-inspecting proxy shows the
proxy's issuer, not Cloudflare's. Check certificates through the API
(`GET /zones/{zone}/ssl/certificate_packs?status=all`) or from an unproxied
machine. The Universal pack (`<domain>` + `*.<domain>`) covers www and is
usually already active; extra Advanced packs show `initializing` for a few
minutes and aren't a blocker.

## 5. Webflow-hosted subdomains hide in the zone

Cutting over apex and www doesn't move `visit.`, `promo.`, or a wildcard
`*` that also points at Webflow (`cdn.webflow.com`, `proxy-ssl.webflow.com`,
`198.202.211.1`). Those keep working until Webflow hosting is cancelled, then
die quietly. Before cancelling, list every zone record whose content
matches Webflow and decide each one.

## 6. Old WAF rules wake up at cutover

**Sites:** chesterfieldwoodlakedental.com, lithiaspringsdental.com,
shortpumpfamilydentistry.com, 2026-10-26.
Webflow records were DNS-only (grey cloud), so traffic never passed Cloudflare's
WAF. Worker custom domains are always proxied, so the zone's custom rules
apply from the moment of cutover. WordPress-era rules from 2023 suddenly fired:
- "International Challenge": `js_challenge` for every non-US visitor
  (chesterfield, lithiasprings). Shows "Just a moment..." to anyone abroad,
  plus non-US crawlers, link-preview bots and monitoring.
- "Semi-Aggressive Blocking": hard `block` for 22 countries incl. DE/FR/NL
  (lithiasprings).
- "Aggressive Blocking": `block` non-US/CO/GT/PH on `/blog` (shortpump).
Checks from a US machine pass, so the batch verify missed it.
**Catch it:** in preflight, list enabled rules in
`/zones/{zone}/rulesets/phases/http_request_firewall_custom/entrypoint`, plus
page rules (forwarding_url / cache_level) and security_level. Decide on each
before cutover. Rules aimed only at `wp-login` / `xmlrpc.php` / `user.ini`
are harmless on a static site.
