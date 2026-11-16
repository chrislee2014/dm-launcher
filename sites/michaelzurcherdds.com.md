# michaelzurcherdds.com (old domain of Zurcher Dental Esthetics)

- **Canonical site:** www.zurcherdentalesthetics.com (Worker `zurcherdentalesthetics-com`,
  launched by the daily check 2026-11-16 ~09:45 ET)
- **Zone:** `3882f1e28d201244bc3893d9040d11f6`, NS `elle`/`rodney.ns.cloudflare.com`
  (registrar GoDaddy, switched from `ns09/ns10.domaincontrol.com` 2026-11-16)

## What happened (PITFALLS #7)

The domain stayed at GoDaddy, pointing at Webflow (A @ 198.202.211.1, www CNAME
cdn.webflow.com), and Webflow redirected it. After the main site launched it went
down: HTTPS handshake failure, HTTP "error code: 1001". No email on the domain (no MX).

## Fix (2026-11-16)

- Chris added the zone and switched the nameservers at GoDaddy.
- Redirect Rule `ec2222dc…` (dynamic redirect phase): host in {apex, www} → 301 to
  `concat("https://www.zurcherdentalesthetics.com", path)`, query kept.
- A @ → `192.0.2.1` (proxied placeholder); www → CNAME @ (proxied). Both commented.
- Kept: google-site-verification TXT, `_domainconnect` CNAME. Left the two `_webflow`
  TXTs (harmless; delete when Webflow is fully gone).
- Verified at Cloudflare's edge: http/https apex and www → 301 to the same path on
  www.zurcherdentalesthetics.com (e.g. `/contact-us?x=1`); one hop then 200;
  Universal cert active. Public resolvers still had GoDaddy NS cached at the time.

## Log

- 2026-11-16: down after the main site's launch; zone + 301 rule set up and verified at the edge.
