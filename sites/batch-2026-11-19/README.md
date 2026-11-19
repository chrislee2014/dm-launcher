# Batch 1 launch, 2026-11-19 (21 sites, launched by Claude at Chris's request)

Ignacio switched nameservers 19:48–19:55 UTC; launched ~20:20 UTC with `tools/preflight.py` + `tools/launch.py`
(write check, delete Webflow pair, attach www + apex, auto-rollback). All 21 verified: apex 301 → www
(path + query), www 200 on Worker (title matches workers.dev, no Webflow headers), robots/sitemap 200,
certs active, MX unchanged. Sheet P=Yes + note on all 21. Judith DM'd; channel summary posted.

Full preflight data and record snapshots (rollback) are in `preflight.json`; results in `launch.json`.

| Domain | Title on Worker | Old web records (rollback) | HubSpot aliases |
|---|---|---|---|
| bespokedentistrytx.com | Bespoke Dentistry / Coming Soon in Katy, TX | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| cherishyoursmile.com | Dentist in Taylorsville, UT 84123 / Cherish Your Smile | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| hilldentalstudiotn.com | Hill Dental Studio / Trusted Family Dentist in Hixson, TN | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| odentalsmiles.com | Dentist in Grasonville, MD / O Dental | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| pebblecreekdentalandimplants.com | Pebble Creek Dental &amp; Implants Opening Soon in Fall  202 | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| tworiversdentalmo.com | Two Rivers Dental / Dentist in Nixa, MO | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| mydentalworlds.com | DentalWorld / Dentist in Salisbury, NC | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| chisholmcreekdental.com | Dentist in Wichita, KS / Chisholm Creek Dental | A @ 198.202.211.1; CNAME www cdn.webflow.com | hertzlerdds.com |
| whitedental.org | Quality Dental Care in Tremonton, UT / White Dental | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| centraldentalaz.com | Central Dental / Trusted Family Dentistry in Phoenix, AZ | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| claassenfamilyandcosmeticdentistry.com | Family and Cosmetic Dentistry in Richardson, TX / Claassen F | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| yuleefamilydentistry.com | Yulee Family Dentistry / Gentle, Local Dental Care in Yulee, | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| bleupediatricdentistryorthodontics.com | Pediatric Dentist in The Woodlands, TX / Compassionate Denta | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| veritydentalandimplants.com | Verity Dental &amp; Implant Center / Dentist in Salt Lake Ci | A @ 198.202.211.1; CNAME www cdn.webflow.com | completesmilessh.com |
| bensalemdentalcare.com | Bensalem Dental Dentures Implants / Dentist in Bensalem, PA | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| hutchinsonfamilydental.com | Hutchinson Family Dental / Trusted Dentist in Hutchinson, KS | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| eastlakefamilydental.com | Family Dentist in St. Cloud, FL / East Lake Family Dental | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| fruitlandparkdentistry.com | Dentist in Fruitland Park, FL / Comfortable Local Dental Car | A @ 198.202.211.1; CNAME www cdn.webflow.com | jonesdentistryfl.com |
| fangdentalstudio.com | Modern Dentistry in Monrovia, CA / Fang Dental Studio | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| kidstowndentist.com | Kidstown Dental / Pediatric Dentist in Katy, TX / Gentle Kid | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |
| solaradentalfl.com | Solara Dental / Coming Soon to Port St. Lucie / Dr. Emily Ph | A @ 198.202.211.1; CNAME www cdn.webflow.com |  |

## Judgment calls
- **Coming Soon parity:** bespokedentistrytx.com, solaradentalfl.com and pebblecreekdentalandimplants.com
  show pre-opening pages on the Worker, identical titles to live Webflow. Launched (host change only).
- **No MX** on claassen, fruitlandpark, pebblecreek, verity, whitedental: only GoDaddy's default `_dmarc`,
  consistent with never having email (not an import loss).

## Follow-ups
- Aliases to move before Webflow is cancelled: completesmilessh.com (Verity, GoDaddy, no MX),
  jonesdentistryfl.com (Fruitland Park, GoDaddy, 1 MX). hertzlerdds.com (Chisholm Creek, Network
  Solutions → Webflow) already fails over https: asked Judith if still needed.
- solaradentalfl.com expires 2026-11-24: confirm auto-renew (GoDaddy, Emily Pham's account).
- bentwaterdentistry.com on hold (support ticket).
- accdfl.com SPF sub-record restored the same day (Chris OK).

