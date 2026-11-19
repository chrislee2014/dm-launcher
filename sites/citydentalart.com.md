# citydentalart.com (old domain of City Dental Arts)

- **Canonical site:** www.citydentalarts.com (launched 2026-11-18)
- **Zone:** `89eea5323fba6a04ac0d883ff21d5457`, created 2026-11-19 by Claude (jump_start off),
  assigned NS **elle / rodney.ns.cloudflare.com**. Status **pending** until Ignacio switches the
  nameservers at GoDaddy (currently ns35/ns36.domaincontrol.com). Asked him by DM 2026-11-19;
  he reports to Chris when done.

## What happened (PITFALLS #7)

Still at GoDaddy pointing at Webflow (A @ 198.202.211.1, www CNAME cdn.webflow.com). Went down
overnight 11/18 → 11/19 (HTTPS handshake failure, HTTP 409 / error 1001) despite the request to
hold Webflow.

## Zone setup (ready before the switch)

- Redirect Rule `709892406df649f1a4ea8f2dff494906`: host in {apex, www} → 301 to
  `concat("https://www.citydentalarts.com", path)`, query kept.
- A @ `192.0.2.1` proxied; www → CNAME @ proxied.
- Copied from GoDaddy public DNS (commented "Copied from GoDaddy DNS 2026-11-19"):
  MX 0 citydentalart-com.mail.protection.outlook.com; TXT `v=spf1 include:spf.protection.outlook.com -all`;
  TXT `MS=ms77225779`; CNAME autodiscover → autodiscover.outlook.com; CNAME enterpriseenrollment →
  enterpriseenrollment-s.manage.microsoft.com; CNAME enterpriseregistration → enterpriseregistration.windows.net;
  CNAME lyncdiscover → webdir.online.lync.com; CNAME sip → sipdir.online.lync.com; A mail 69.168.78.192;
  CNAME _domainconnect → _domainconnect.gd.domaincontrol.com; SRV _sip._tls 100 1 443 sipdir.online.lync.com;
  SRV _sipfederationtls._tcp 100 1 5061 sipfed.online.lync.com.
- Public DNS can't be enumerated completely; Ignacio asked to flag any other GoDaddy record before switching.

## After the switch

Zone goes active → verify http/https apex + www 301 to the same path on www.citydentalarts.com,
certificate active, MX/autodiscover resolve unchanged. (The daily check's sweep should confirm this.)
