# Email DNS fixes, 2026-11-18 (approved by Chris)

Pre-existing problems flagged in launch logs; not caused by the migration.

## whitmandental.com
- MX is Microsoft 365 (`whitmandental-com.mail.protection.outlook.com`) but SPF only authorized GoDaddy.
- SPF `v=spf1 include:secureserver.net -all` → `v=spf1 include:spf.protection.outlook.com include:secureserver.net -all`
  (kept secureserver in case anything still sends through GoDaddy). Record `010d580c…`, commented.

## zurcherdentalesthetics.com
- SPF typo: `v=spf1 include:_spf.google.com ~alll` → `~all` (record `8230e4ac…`).
- Two `_dmarc` records (invalid; receivers ignore DMARC when there are two). Deleted
  `v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;` (`7f501b16…`),
  kept `v=DMARC1; p=none; rua=mailto:dmarc@zurcherdentalesthetics.com`. p=none matches how mail was
  effectively treated before (no valid DMARC). Moving to quarantine is a separate decision once
  reports show Google Workspace mail passing.

Verified on public DNS the same day.
