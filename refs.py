import json,re
h=json.load(open('/workspace/cci/heidelberg.json'));b=json.load(open('/workspace/cci/belgic.json'));t=json.load(open('/workspace/cci/dort.json'))
B={'伯':'job','诗':'psa','箴':'pro','传':'ecc','歌':'song'}
def books(r):
    out=set()
    for m in re.finditer(r'(?:^|[；;，,\s])(伯|诗|箴|传|歌)\s*\d',r): out.add(B[m.group(1)])
    return out
res={k:[] for k in B.values()}
for ld in h['lordsdays']:
  for q in ld['questions']:
    for i,r in enumerate(q['refs']):
      for bk in books(r): res[bk].append(('HC',q['q'],i+1,r))
for a in b['articles']:
  for i,r in enumerate(a['refs']):
    for bk in books(r): res[bk].append(('BC',a['number'],i+1,r))
for hd_i,hd in enumerate(t['heads']):
  for a in hd['articles']:
    for i,r in enumerate(a['refs']):
      for bk in books(r): res[bk].append(('CD',f"{hd_i}-{a['number']}",i+1,r))
    for m in re.finditer(r'（(伯|诗|箴|传|歌)\s*[\d:：\-，,]+）',a['text']): res[B[m.group(1)]].append(('CDtxt',f"{hd_i}-{a['number']}",0,m.group(0)))
for k,v in res.items(): print(k,len(v),v[:40])
json.dump(res,open('wref.json','w'),ensure_ascii=False)
