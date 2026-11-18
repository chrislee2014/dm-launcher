# thecitydental.com (City Dental Arts, City Ave)

_From the 2026-11-18 scheduled run (Slack thread)._

- Worker `thecitydental-com`, CANONICAL_HOST=www.thecitydental.com. Zone `9d683c1e2d14734767befac7db0af0b3`,
  NS cash/tia (from GoDaddy ns39/40), active 11/18 00:33 UTC. Sheet row 97.
- Preflight: "City Dental Arts | Philadelphia Dentist for Implants & Emergency Care", tel (215) 877-3322
  + 267-489-2164 tracking, matches Webflow. No sample data/Coming Soon/noindex; sitemap on www. No WAF
  or page rules; BFM off. HubSpot: no extra domains.
- Snapshot: A @ 198.202.211.1 (deleted); CNAME www cdn.webflow.com (deleted); CNAME _domainconnect;
  TXT google-site-verification; TXT _webflow. No MX.
- Cutover ~14:46 UTC after the write test. www showed Webflow headers ~1.5 min (resolver cache).
- Verified: apex 301 → www (path + query), http → https, www 200 on Worker, robots/sitemap 200, 404 on
  unknown path, certs active.
- Rollback: remove custom domains; recreate A @ 198.202.211.1 + CNAME www cdn.webflow.com (DNS only).
