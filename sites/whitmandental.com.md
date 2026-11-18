# whitmandental.com (Whitman Dental Center, Philadelphia)

_From the 2026-11-18 scheduled run (Slack thread)._

- Worker `whitmandental-com`, canonical www. Zone `7c90577516c50e04f42fc13aa052689d`, NS cash/tia (from
  GoDaddy ns07/08), active 11/18 00:46 UTC. Sheet row 98.
- Preflight: "Top-Rated Dentist in Philadelphia, PA | Whitman Dental Center", tel +1 215-551-9151 +
  267-930-2506 tracking. All checks passed.
- Snapshot: A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME autodiscover, email
  (secureserver), lyncdiscover, msoid, sip, _domainconnect; MX whitmandental-com.mail.protection.outlook.com;
  SRV _sip._tls, _sipfederationtls._tcp; TXT _webflow, google-site-verification, MS=ms10970030, SPF
  `v=spf1 include:secureserver.net -all`.
- Verified as standard; MX unchanged.
- **Flag (pre-existing):** MX is Microsoft 365 but SPF only includes secureserver.net with -all.
- Rollback: remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
