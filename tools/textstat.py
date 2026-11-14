"""统计每页正文字数：总字数 / 原文（经文、信条、CCI、威斯敏斯特等逐字引文）字数 / 本站讲解字数，并列出每节讲解字数。"""
import sys, re, json, os
from html.parser import HTMLParser
VERB = {'blockquote', 'q'}
VCLS = re.compile(r'\b(conf|cci|creed|wm|verse|bq|scrip|cuv)\b')
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st = []; s.sec = None; s.tot = 0; s.ver = 0; s.secs = {}; s.skip = 0; s.inmain = False
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == 'main': s.inmain = True
        if t in ('script', 'style', 'svg', 'template', 'nav'): s.skip += 1
        if t == 'section' and a.get('id'): s.sec = a['id']
        v = t in VERB or bool(VCLS.search(a.get('class') or ''))
        if t not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'wbr', 'source'): s.st.append((t, v))
    def handle_endtag(s, t):
        if t in ('script', 'style', 'svg', 'template', 'nav'): s.skip = max(0, s.skip - 1)
        while s.st:
            x = s.st.pop()
            if x[0] == t: break
    def handle_data(s, d):
        if not s.inmain or s.skip: return
        n = len(re.sub(r'\s', '', d))
        if not n: return
        s.tot += n
        if any(v for _, v in s.st): s.ver += n
        else: s.secs[s.sec] = s.secs.get(s.sec, 0) + n
out = {}
D = sys.argv[1] if len(sys.argv) > 1 else 'docs'
for f in sorted(os.listdir(D)):
    if not f.endswith('.html') or f == '404.html': continue
    p = P(); p.feed(open(os.path.join(D, f)).read())
    out[f] = dict(total=p.tot, verbatim=p.ver, own=p.tot - p.ver, secs=p.secs)
if '--secs' in sys.argv:
    for f, v in out.items(): print(f, sorted(v['secs'].items(), key=lambda x: -x[1])[:12])
for f, v in out.items(): print(f'{f:18} total {v["total"]:6} verbatim {v["verbatim"]:6} own {v["own"]:6}')
print('SUM own', sum(v['own'] for v in out.values()), 'verbatim', sum(v['verbatim'] for v in out.values()))
json.dump(out, open('/tmp/textstat_' + os.path.basename(os.path.abspath(D)) + '.json', 'w'))
