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
