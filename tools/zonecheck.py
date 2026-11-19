import json, re, sys, os, urllib.request
path = sys.argv[1]
txt = open(path).read()
D = re.search(r'^\$ORIGIN\s+(\S+?)\.?\s*$', txt, re.M).group(1)
want = []
for line in txt.splitlines():
    line = line.split(';',1)[0] if not '"' in line else line
    m = re.match(r'^(\S+)\s+(\d+)\s+IN\s+(A|AAAA|CNAME|MX|TXT|SRV|CAA)\s+(.*)$', line.strip())
    if not m: continue
    name, ttl, t, rest = m.groups()
    name = name.replace('.@','')
    if t == 'MX':
        p, h = rest.split(); val = f"{p} {h.rstrip('.')}"
    elif t == 'SRV':
        p, w, port, tgt = rest.split(); val = f"{p} {w} {port} {tgt.rstrip('.')}"
    elif t == 'TXT':
        val = ''.join(re.findall(r'"((?:[^"\\]|\\.)*)"', rest)) or rest
    else:
        val = rest.strip().rstrip('.')
        if val == '@': val = D
    want.append((t, name, val))
tok = os.environ['CLOUDFLARE_API_TOKEN']
def get(u):
    r = urllib.request.Request('https://api.cloudflare.com/client/v4/'+u, headers={'Authorization':'Bearer '+tok})
    return json.load(urllib.request.urlopen(r))['result']
z = get(f'zones?name={D}')[0]
cf = get(f"zones/{z['id']}/dns_records?per_page=500")
def key(r):
    n = r['name']; n = '@' if n == D else n[:-len(D)-1]
    if r['type'] == 'MX': c = f"{r['priority']} {r['content']}"
    elif r['type'] == 'SRV': d = r['data']; c = f"{d['priority']} {d['weight']} {d['port']} {d['target']}"
    elif r['type'] == 'TXT': c = ''.join(re.findall(r'"((?:[^"\\]|\\.)*)"', r['content'])) or r['content']
    else: c = r['content']
    return (r['type'], n, c)
have = {key(r): r for r in cf}
print(f"{D}: zone {z['status']}, NS {', '.join(z['name_servers'])} | export {len(want)} records, Cloudflare {len(cf)}")
miss = [w for w in want if w not in have]
for w in want:
    r = have.get(w)
    print(('OK      ' if r else 'MISSING ') + ' '.join(w)[:140] + ('   [PROXIED]' if r and r.get('proxied') else ''))
print('EXTRA in Cloudflare:', [k for k in have if k not in want])
print('MISSING count:', len(miss))
