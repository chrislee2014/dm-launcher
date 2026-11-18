# royersforddentalcare.com (Royersford Dental, PA)

_From the 2026-11-18 scheduled run (Slack thread)._

- Worker `royersforddentalcare-com`, canonical www. Zone `991667aec2673526606e5412511dcb6e`, NS cash/tia
  (from GoDaddy ns27/28), active 11/18 00:49 UTC. Sheet row 95.
- Preflight: "Royersford Dental | Dentist in Royersford, PA", tel (484) 369-8625 + 484-917-1961 tracking.
  Matches Webflow; no WAF/page rules; BFM off; HubSpot no extra domains.
- Snapshot: A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME autodiscover,
  enterpriseenrollment, enterpriseregistration, lyncdiscover, sip, pay, _domainconnect; MX
  royersforddentalcare-com.mail.protection.outlook.com; SRV _sip._tls, _sipfederationtls._tcp; TXT
  google-site-verification, MS=ms50857652, SPF outlook -all, _webflow.
- Verified as standard (www Advanced pending_validation). All Microsoft mail records untouched, as the client asked.
- Rollback: remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
