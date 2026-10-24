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
