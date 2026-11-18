# northwestdentalstudio.com (Northwest Dental Studio, Powell OH)

_From the 2026-11-18 scheduled run (Slack thread)._

- Worker `northwestdentalstudio-com`, canonical www. Zone `e9afb82504a4bd5b81fc14fd45345a70`, NS elle/rodney
  (from GoDaddy ns37/38), active 11/18 00:31 UTC. Sheet row 3.
- Preflight: "Dentist in Powell, OH | Northwest Dental Studio", tel +1 614-810-7334. Sheet project says
  "Coming Soon LP", but the Worker serves the full site, matching live Webflow.
- Snapshot: A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME autodiscover,
  _domainconnect, pay, selector1/2._domainkey (MS DKIM); MX northwestdentalstudio-com.mail.protection.outlook.com;
  TXT _dmarc, SPF outlook -all, google-site-verification, MS=ms52486006, _webflow.
- Verified as standard; MX unchanged.
- Rollback: remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
