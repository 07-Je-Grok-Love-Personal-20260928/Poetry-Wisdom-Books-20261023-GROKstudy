# -*- coding: utf-8 -*-
"""近似重复检查：把本站每一段（readdata 里的每个字符串）与原书文本做「字符 8-gram Jaccard」比较，
取原书中最相似的同长窗口的得分；>0.3 视为可疑（贴近改写）。用法：python3 tools/neardup.py [N=8] [阈值=0.3] files..."""
import sys, re, ast, glob, json, collections
args = sys.argv[1:]
N = int(args.pop(0)) if args and args[0].isdigit() else 8
TH = float(args.pop(0)) if args and re.fullmatch(r'0?\.\d+', args[0]) else 0.3
files = args or sorted(glob.glob('src/readdata/*.py'))
han = lambda s: re.sub(r'[^\u4e00-\u9fff]', '', s)
src = han(''.join(open(p).read() for p in glob.glob('/workspace/pdfin/*.txt')))
idx = collections.defaultdict(list)
for i in range(len(src) - N + 1): idx[src[i:i + N]].append(i)
cuv = ''
try: cuv += han(json.dumps(json.load(open('data/cuv.json')), ensure_ascii=False))
except Exception: pass
try: cuv += han(json.dumps(json.load(open('data/psalms_cuv.json')), ensure_ascii=False))  # 和合本诗篇全文：经文不算雷同
except Exception: pass
cuvg = {cuv[i:i + N] for i in range(len(cuv) - N + 1)}
def grams(s): return {s[i:i + N] for i in range(len(s) - N + 1)}
def strings(p):
    out = []
    for node in ast.walk(ast.parse(open(p).read())):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(han(node.value)) >= 20: out.append(node.value)
    return out
flag = 0; tot = 0; worst = []
for p in files:
    for s in strings(p):
        h = han(s); g = grams(h) - cuvg; tot += 1
        if not g: continue
        hits = [pos for x in g for pos in idx.get(x, ())]
        best = 0.0
        if hits:
            L = len(h); step = max(1, L // 4)
            for c in sorted(set(q // step for q in hits)):
                for st in (max(0, c * step - L // 2), max(0, c * step - L // 4), c * step):
                    w = grams(src[st:st + L]) - cuvg
                    if w: best = max(best, len(g & w) / len(g | w))
        worst.append((best, p.split('/')[-1], s[:60]))
        if best > TH: flag += 1
worst.sort(reverse=True)
# 原书讨论题按简报允许原样引用（注明出处），单独列出、不计入 flagged
import sys as _s; _s.path.insert(0, '/workspace/pw/src')
import readdata.god_a as _GA
for _n in 'bcdefgh': __import__('readdata.god_' + _n)
QS = {q for x in _GA.U for q in x['qs']}
own = [w for w in worst if w[2] not in QS]
qflag = sum(1 for w in worst if w[2] in QS and w[0] > TH)
print(f'paragraphs {tot}  N={N}  threshold {TH}  flagged(all) {flag}  flagged(own text, excl. allowed book discussion questions) {sum(1 for w in own if w[0] > TH)}  max(own) {own[0][0]:.3f}  allowed-questions>{TH}: {qflag}')
for b, f, s in worst[:12]: print(f'  {b:.3f} {f} {s}')
