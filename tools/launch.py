import json,os,sys,urllib.request,concurrent.futures as cf
TOK=os.environ['CLOUDFLARE_API_TOKEN']; ACC=os.environ['CLOUDFLARE_ACCOUNT_ID']
def call(m,u,b=None):
    r=urllib.request.Request('https://api.cloudflare.com/client/v4/'+u,method=m,data=json.dumps(b).encode() if b is not None else None,headers={'Authorization':'Bearer '+TOK,'Content-Type':'application/json'})
    try: return json.load(urllib.request.urlopen(r,timeout=60))
    except urllib.error.HTTPError as e: return json.load(e)
pre={o['domain']:o for o in json.load(open(sys.argv[1]))}
def launch(d):
    o=pre[d]; z=o['zone']; snap=o['web_ids']; w=o['worker']; log={'domain':d,'snapshot':[f"{s['type']} {s['name']} {s['content']} proxied={s['proxied']}" for s in snap]}
    cur=call('GET',f'zones/{z}/dns_records?per_page=500')['result']
    curweb={r['id']:r for r in cur if r['name'] in (d,'www.'+d) and r['type'] in('A','AAAA','CNAME')}
    if set(curweb)!={s['id'] for s in snap}: log['result']='SKIPPED: records changed since preflight'; return log
    s0=snap[0]; wc=call('PATCH',f"zones/{z}/dns_records/{s0['id']}",{'content':s0['content'],'proxied':s0['proxied'],'ttl':s0['ttl']})
    if not wc.get('success'): log['result']='HELD: write check failed '+str(wc.get('errors')); return log
    for s in snap:
        r=call('DELETE',f"zones/{z}/dns_records/{s['id']}")
        if not r.get('success'): log['result']='ERROR deleting '+s['name']+' '+str(r.get('errors')); return log
    added=[]
    for h in ['www.'+d, d]:
        r=call('PUT',f'accounts/{ACC}/workers/domains',{'hostname':h,'service':w,'zone_id':z,'environment':'production'})
        if not r.get('success'):
            for s in snap:
                if s['name'] not in added: call('POST',f"zones/{z}/dns_records",{'type':s['type'],'name':s['name'],'content':s['content'],'proxied':s['proxied'],'ttl':s['ttl']})
            log['result']='ROLLED BACK: '+h+' '+str(r.get('errors')); return log
        added.append(h)
    log['result']='launched'; return log
doms=[d for d in sys.argv[2].split(',')]
with cf.ThreadPoolExecutor(5) as ex: res=list(ex.map(launch,doms))
json.dump(res,open(sys.argv[3],'w'),indent=1)
for r in res: print(f"{r['domain']:<40} {r['result']}")
