# tools

- `zonecheck.py <export.txt>`: compares a GoDaddy zone-file export with the domain's Cloudflare zone
  and lists OK / MISSING / EXTRA records (MX priorities, SRV, multi-string TXT handled).
  Needs `CLOUDFLARE_API_TOKEN` in the environment. Read-only.
