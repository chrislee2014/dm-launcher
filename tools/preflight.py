import json,os,re,sys,urllib.request,concurrent.futures as cf
TOK=os.environ['CLOUDFLARE_API_TOKEN']; ACC=os.environ['CLOUDFLARE_ACCOUNT_ID']; HS=os.environ.get('HUBSPOT_API_TOKEN')
WF=re.compile(r'^(198\.202\.211\.1|cdn\.webflow\.com|proxy-ssl\.webflow\.com)$')
def cfapi(u):
    r=urllib.request.Request('https://api.cloudflare.com/client/v4/'+u,headers={'Authorization':'Bearer '+TOK})
    try: return json.load(urllib.request.urlopen(r,timeout=30))
    except urllib.error.HTTPError as e: return json.load(e)
def fetch(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 preflight'}),timeout=25); return r.status, r.read().decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return 0, str(e)
def hubspot(d):
    if not HS: return 'no token'
    body=json.dumps({"filterGroups":[{"filters":[{"propertyName":"domain","operator":"EQ","value":d}]}],"properties":["name","domain","website","hs_additional_domains"],"limit":20}).encode()
    r=urllib.request.Request('https://api.hubapi.com/crm/v3/objects/companies/search',data=body,headers={'Authorization':'Bearer '+HS,'Content-Type':'application/json'})
    try: res=json.load(urllib.request.urlopen(r,timeout=30))['results']
    except Exception as e: return 'err '+str(e)[:60]
    al=set()
    for c in res:
        p=c['properties']
        for v in [p.get('website') or '']+(p.get('hs_additional_domains') or '').split(';'):
            h=re.sub(r'^https?://','',v.strip().lower()).split('/')[0].replace('www.','',1)
            if h and h!=d: al.add(h)
    return {'companies':len(res),'aliases':sorted(al)}
def pre(d):
    o={'domain':d,'problems':[]}; w=d.replace('.','-'); o['worker']=w
    z=cfapi(f'zones?name={d}')['result']; z=z[0] if z else None
    if not z: o['problems'].append('no zone'); return o
    o['zone']=z['id']; 
    if z['status']!='active': o['problems'].append('zone '+z['status'])
    dep=cfapi(f'accounts/{ACC}/workers/scripts/{w}/deployments')
    if not dep.get('success'): o['problems'].append('worker missing'); return o
    v=dep['result']['deployments'][0]; o['deploy']=f"{v['created_on'][:16]} {v.get('author_email','')}"
    ver=cfapi(f"accounts/{ACC}/workers/scripts/{w}/versions/{v['versions'][0]['version_id']}")['result']
    vars_={b['name']:b.get('text') for b in ver['resources']['bindings'] if b['type']=='plain_text'}
    o['canonical']=vars_.get('CANONICAL_HOST')
    if not o['canonical']: o['problems'].append('CANONICAL_HOST empty')
    st,h=fetch(f'https://{w}.dental-marketing.workers.dev/')
    t=re.search(r'<title>([^<]*)</title>',h); o['title']=t.group(1) if t else None
    o['tel']=sorted(set(re.findall(r'tel:[+0-9()\- ]{7,}',h)))[:2]
    if st!=200: o['problems'].append(f'workers.dev {st}')
    if re.search(r'sample dental|anytown',h,re.I) or any('555' in x for x in o['tel']): o['problems'].append('TEMPLATE/sample data')
    if re.search(r'coming soon',o['title'] or '',re.I): o['problems'].append('Coming Soon title')
    if re.search(r'<meta[^>]*robots[^>]*noindex',h,re.I): o['problems'].append('noindex meta')
    _,rb=fetch(f'https://{w}.dental-marketing.workers.dev/robots.txt'); sm=re.findall(r'(?i)sitemap:\s*(\S+)',rb)
    o['sitemap']=sm[0] if sm else None
    if not sm or d not in sm[0]: o['problems'].append('sitemap not on domain')
    recs=cfapi(f"zones/{z['id']}/dns_records?per_page=500")['result']
    web=[r for r in recs if r['name'] in (d,'www.'+d) and r['type'] in('A','AAAA','CNAME')]
    o['web']=[f"{r['type']} {'@' if r['name']==d else 'www'} {r['content']}{' [P]' if r['proxied'] else ''}" for r in web]
    o['web_ids']=[{'id':r['id'],'type':r['type'],'name':r['name'],'content':r['content'],'proxied':r['proxied'],'ttl':r['ttl']} for r in web]
    if not web or not all(WF.match(r['content']) for r in web) or {('@' if r['name']==d else 'www') for r in web}!={'@','www'}:
        o['problems'].append('web records not the plain Webflow pair')
    o['other_webflow']=[f"{r['type']} {r['name']}" for r in recs if r['type'] in('A','AAAA','CNAME') and WF.match(r['content']) and r['name'] not in(d,'www.'+d)]
    ent=cfapi(f"zones/{z['id']}/rulesets/phases/http_request_firewall_custom/entrypoint")
    rules=[r for r in (ent.get('result') or {}).get('rules',[]) if r.get('enabled')] if ent.get('success') else []
    bad=[r['description'] for r in rules if not re.search(r'wp-login|xmlrpc|user\.ini|wp-admin|wp-content',r.get('expression',''),re.I) or re.search(r'geoip|country',r.get('expression',''),re.I)]
    if bad: o['problems'].append('WAF rules: '+'; '.join(bad))
    bm=cfapi(f"zones/{z['id']}/bot_management").get('result') or {}
    if bm.get('fight_mode'): o['problems'].append('Bot Fight Mode on')
    pr=cfapi(f"zones/{z['id']}/pagerules").get('result') or []
    o['pagerules']=[p['targets'][0]['constraint']['value']+' '+','.join(a['id'] for a in p['actions']) for p in pr if p.get('status')=='active']
    if any('forwarding_url' in x for x in o['pagerules']): o['problems'].append('forwarding page rule')
    o['hubspot']=hubspot(d)
    return o
doms=sys.argv[1].split(',')
with cf.ThreadPoolExecutor(7) as ex: res=list(ex.map(pre,doms))
json.dump(res,open(sys.argv[2],'w'),indent=1)
for o in res:
    print(f"{'OK ' if not o['problems'] else 'HOLD'} {o['domain']:<40} {(o.get('title') or '')[:55]:<55} {','.join(o.get('tel',[]))[:30]:<30} canon={o.get('canonical')} hs={o.get('hubspot') if isinstance(o.get('hubspot'),str) else o.get('hubspot',{}).get('aliases')} {'| '+'; '.join(o['problems']) if o['problems'] else ''}")
    if o.get('other_webflow'): print('      other records on Webflow:',o['other_webflow'])
