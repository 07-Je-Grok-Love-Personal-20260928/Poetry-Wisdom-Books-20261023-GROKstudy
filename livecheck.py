import json,re,html,urllib.request
d=json.load(open('/workspace/cci/creeds.json'))
def page(u):
    t=urllib.request.urlopen(u,timeout=30).read().decode('utf8')
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>','',t))
    return re.sub(r'\s+','',t)
for k,v in d.items():
    p=page(v['url'])
    paras=[x for x in v['text'].split('\n') if x.strip()]
    ok=[re.sub(r'\s+','',x) in p for x in paras]
    print(k,len(paras),sum(ok), [paras[i][:30] for i,o in enumerate(ok) if not o])
