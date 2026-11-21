"""版权自查：找出数据文件中与 /workspace/pdfin/*.txt 原文连续重合 ≥N 个汉字的片段（和合本经文除外需人工判断）。"""
import re, sys, glob, json
N = int(sys.argv[1]) if len(sys.argv) > 1 else 14
def norm(s): return re.sub(r'[^\u4e00-\u9fff]', '', s)
src = norm(''.join(open(f).read() for f in glob.glob('/workspace/pdfin/*.txt')))
grams = set(src[i:i+N] for i in range(len(src)-N+1))
cuv = norm(json.dumps(json.load(open('/workspace/pw/data/cuv.json')), ensure_ascii=False))
cuvg = set(cuv[i:i+N] for i in range(len(cuv)-N+1))
tot = 0
for f in sorted(sys.argv[2:] or glob.glob('/workspace/pw/src/readdata/*.py')):
    t = norm(open(f).read()); i = 0; runs = []
    while i <= len(t)-N:
        g = t[i:i+N]
        if g in grams and g not in cuvg:
            j = i + N
            while j < len(t) and t[i:j+1] in src: j += 1
            runs.append(t[i:j]); i = j
        else: i += 1
    tot += sum(len(r) for r in runs)
    print(f.split('/')[-1], len(t), 'runs', len(runs), 'chars', sum(len(r) for r in runs), 'max', max((len(r) for r in runs), default=0))
    for r in sorted(runs, key=len, reverse=True)[:6]: print('   ', len(r), r[:60])
print('TOTAL overlap chars', tot)
