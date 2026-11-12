# Daily launch check (draft, not scheduled yet)

Runs once a day as a scheduled Claude session. Each run starts with no memory:
this file, RUNBOOK.md, PITFALLS.md and sites/ are what carry over.

## Sources and tools

| What | How |
|---|---|
| Work list | "Webflow to Astro Migration - Control Sheet", tab **Roxy - Batches** (sheet `1FgGnVN1N7Rq07gR9XE3qPobIdyp6yAnS9Fa7wdL4hNU`) |
| Read / write the sheet | n8n **Broker: Migration Sheet (Roxy - Batches)** (`s6Rza5KbcVdiBOp1`): `{action:"read"}`; `{action:"update", domain, launched:"Yes", note}` writes only P and Q, note appended |
| DNS, Workers, WAF | Cloudflare API MCP, account Dental Marketing |
| Messages | Slack MCP (posts as **Alfred**). Channel `C0CG9QQ9MTN` (Chris, Roxy, Ignacio) |
| People | Chris `U03VCDX7059` (launches with Claude), Roxy `U06MW1BRHUZ` (client approval, adds domain to Cloudflare), Ignacio `U063DF5GGHG` (DNS QA, switches nameservers), Judith `U02HJRMRSQ2` (builds the sites; DM only) |

## Each run

1. **Read** all rows via the broker.
2. **Candidates:** column E set, and B = "Nameservers Switched" **or** O = "Yes".
   Skip if P = "Yes" (already launched), R (Hold) is not empty, or the Sites tab
   marks the domain HOLD/PAUSED.
3. **Preflight** each candidate (RUNBOOK step 0 plus PITFALLS #1, #5, #6):
   - zone exists in our account and is **active** (NS on our Cloudflare pair);
     if pending, trigger `activation_check` and retry next run
   - Worker `<domain-with-dashes>` exists; its workers.dev page shows the client's
     title and phone, no "Sample Dental"/"Anytown"/555, no Coming Soon, no noindex;
     robots.txt sitemap on the client domain
   - `CANONICAL_HOST` var set; record which host (www or apex)
   - apex/www records are exactly the Webflow pair (A `198.202.211.1` or CNAME
     `cdn.webflow.com` on @, CNAME `cdn.webflow.com` on www)
   - no enabled WAF custom rule beyond WordPress-path rules (wp-login, xmlrpc,
     user.ini); Bot Fight Mode off; no forwarding page rule that conflicts
   - list other records still pointing at Webflow (visit/promo/wildcard): report only
4. **Preflight problem:** do not launch.
   - Build/config problem (template on main, CANONICAL_HOST empty, Worker missing,
     Coming Soon on): **DM Judith** with exactly what's wrong and what to fix.
   - Anything else (zone not active, WAF/Bot rules, unexpected records): post in
     the channel tagging **Chris**, and tag Roxy/Ignacio if it's their step.
   - Broker `update` with a dated note in Q. Do not touch P.
5. **Clean:** launch per RUNBOOK steps 2–4 (delete the Webflow pair, attach www +
   apex as Worker custom domains, verify apex/www redirect to canonical, Worker
   title on canonical, certs active, MX unchanged; retry verification for ~3 min,
   PITFALLS #3).
   - **Verified:** broker `update` launched=Yes + note; post in channel that it's
     live; DM Judith to run her post-launch checks and handle Webflow.
   - **Failed:** roll back (remove the custom domains, recreate the snapshotted
     records), broker note in Q with the reason, tag **Chris** in the channel. If
     the cause is on Judith's side (build/config), DM Judith instead.
6. **Log** every launch or failure in `sites/` (one file per domain or batch) and push.
7. **Daily summary** in the channel (one message): launched today, blocked with
   reason and owner, and items stuck more than 3 days at a stage, tagging the
   owner (Roxy: approval/contact; Ignacio: DNS QA/NS switch; Judith via DM:
   build fixes). No message about rows that haven't moved and aren't stuck.

## Never

- Disable WAF rules, Bot Fight Mode or other security settings: ask Chris.
- Touch promo/visit/mail or other non-web records.
- Write any column except P and Q.
- Cancel Webflow or delete `_webflow` TXT (Judith's step after her checks).
