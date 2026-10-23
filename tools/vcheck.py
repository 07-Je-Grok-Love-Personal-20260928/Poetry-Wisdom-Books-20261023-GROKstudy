# -*- coding: utf-8 -*-
"""核对本站手打的经文短引语与和合本（信望爱站 API）是否逐字一致。
提取：docs/*.html 中的 “…”+（经文出处）、出处：“…”、翻卡（正面出处/背面经文）。
排除：自动取得的经文框（blockquote.verse、q.vi）、CCI 原文（.cci/.conf）、信经（.creed-box、q.cq）。"""
import sys, os, re, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import cuv
from bs4 import BeautifulSoup
from lib import BOOKN
D = os.path.join(os.path.dirname(__file__), '..', 'docs')
DEF = dict(job='伯', psalms='诗', proverbs='箴', eccl='传', song='歌')
BK = sorted(BOOKN, key=len, reverse=True)
BKRE = '|'.join(map(re.escape, BK))
def norm(s, verse=False):
    if verse: s = re.sub(r'（[^（）]*?(?:原文|或作|或译|又作)[^（）]*）', '', s)
    else: s = re.sub(r'（[^（）]*）|\([^()]*\)', '', s)
    return re.sub(r'[^\u4e00-\u9fff0-9A-Za-z]', '', s)
def parse_ref(r, dflt):
    """返回 [(书, 章, 节)]；只含章的引用不计。"""
    out = []; bk = dflt; ch = None
    r = r.replace('—', '–').replace('-', '–').replace(' ', '')
    for m in re.finditer(rf'({BKRE})?(\d+):(\d+)(?:–(\d+))?((?:[,，、]\d+(?:–\d+)?)*)|[；;]', r):
        if not m.group(3): continue
        if m.group(1): bk = m.group(1)
        if not bk: return None
        ch = int(m.group(2)); a = int(m.group(3)); b = int(m.group(4) or a)
        out += [(bk, ch, v) for v in range(a, b + 1)]
        for extra in re.findall(r'(\d+)(?:–(\d+))?', m.group(5) or ''):
            x = int(extra[0]); y = int(extra[1] or x); out += [(bk, ch, v) for v in range(x, y + 1)]
    return out or None
CH = {}
def chap(bk, ch):
    k = (bk, ch)
    if k not in CH: CH[k] = dict(cuv._get(bk, ch, '1-200'))
    return CH[k]
def check(q, verses):
    txt = ''.join(norm(chap(b, c).get(v, ''), True) for b, c, v in verses)
    frags = [norm(f) for f in re.split(r'……|\.\.\.|…', q) if norm(f)]
    pos = 0
    for f in frags:
        i = txt.find(f, pos)
        if i < 0: return False
        pos = i + len(f)
    return True
def where(q, verses):
    """在出处所在章（前后一章）寻找该引语，返回实际节号。"""
    fr = [norm(f) for f in re.split(r'……|…', q) if norm(f)]
    hits = []
    for b, c in sorted({(b, c) for b, c, _ in verses}):
        for cc in (c, c - 1, c + 1):
            if cc < 1: continue
            try: t = chap(b, cc)
            except Exception: continue
            for v, s in t.items():
                if fr and fr[0][:6] in norm(s, True): hits.append(f'{b}{cc}:{v}')
    return hits
REFP = re.compile(rf'^\s*[（(]\s*((?:参|见)?\s*(?:{BKRE})?\s*\d+:\d+[^）)]*)[）)]')
PREP = re.compile(rf'((?:{BKRE})\s*\d+:\d+(?:[–\-]\d+)?)\s*[：:，,]?\s*$')
def items():
    for fn in sorted(os.listdir(D)):
        if not fn.endswith('.html'): continue
        pid = fn[:-5]; s = BeautifulSoup(open(os.path.join(D, fn)), 'html.parser')
        for sel in ['blockquote.verse', 'q.vi', '.cci', '.conf', '.creed-box', 'q.cq', 'script', 'style', 'nav', '#toc', 'header', 'footer']:
            for e in s.select(sel): e.decompose()
        for f in s.select('.flip'):
            ff = f.select_one('.ff'); fb = f.select_one('.fb')
            if ff and fb: yield pid, 'card', fb.get_text('', strip=True), ff.get_text('', strip=True)
            f.decompose()
        blocks = [b for b in s.find_all(['p', 'td', 'li', 'div', 'span', 'h4', 'summary', 'small', 'b', 'text', 'button', 'dd', 'th', 'h3', 'h2'])
                  if not b.find(['p', 'td', 'li', 'div', 'table'])]
        blocks.append(s)  # 兜底：整页文本
        for blk in blocks:
            t = blk.get_text('', strip=False)
            for m in re.finditer(r'“([^“”]{2,200})”', t):
                after = t[m.end():m.end() + 60]; before = t[max(0, m.start() - 25):m.start()]
                rm = REFP.match(after); pm = PREP.search(before)
                ref = rm.group(1) if rm else (pm.group(1) if pm else None)
                if not ref:
                    pm2 = re.match(r'^\s*[（(]([^（）()]{0,40})[）)]', after)
                    if pm2:
                        m3 = re.search(rf'(?:{BKRE})\s*\d+:\d+[^）)]*', pm2.group(1))
                        if m3: ref = m3.group(0)
                yield pid, 'quote', m.group(1), ref
# 表格中“旧约经文｜新约引用｜引语”三栏：引语出自第一栏的旧约经文，而非紧邻的新约出处
OVERRIDE = {'我来了……乐意照你的旨意行': '诗40:7–8', '我为你的殿心里焦急': '诗69:9'}
def run(verbose=True):
    seen = set(); res = []
    for pid, kind, q, ref in items():
        key = (pid, q, ref)
        if ref is None and any(k[0] == pid and k[1] == q for k in seen): continue
        if key in seen: continue
        seen.add(key)
        ref = OVERRIDE.get(q, ref)
        vs = parse_ref(ref.lstrip('参见 '), DEF.get(pid)) if ref else None
        if not vs or not re.search(r'[\u4e00-\u9fff]{2}', q): res.append((pid, kind, q, ref, 'noref', '')); continue
        try: ok = check(q, vs)
        except Exception as e: res.append((pid, kind, q, ref, 'err', str(e))); continue
        res.append((pid, kind, q, ref, 'ok' if ok else 'BAD', '' if ok else ' / '.join(where(q, vs)[:4])))
    return res
# ---------- 无出处引语：在五卷全书 + 站内引用过的章节里搜索；再在 CCI 语料里搜索 ----------
NCH = dict(伯=42, 诗=150, 箴=31, 传=12, 歌=8)
def corpus():
    chs = {(b, c) for b, n in NCH.items() for c in range(1, n + 1)}
    for k in list(cuv.cache):
        m = re.match(rf'({BKRE})(\d+):', k)
        if m: chs.add((m.group(1), int(m.group(2))))
    return {k: norm(''.join(chap(*k).values()), True) for k in sorted(chs)}
def cci_corpus():
    import glob
    t = ''
    for f in glob.glob('/workspace/cci/*.json') + glob.glob('/workspace/cci/text/*.txt'): t += open(f).read()
    return norm(t.replace('\\n', ''))
def find_in(q, corp):
    fr = [norm(f) for f in re.split(r'……|…', q) if norm(f)]
    out = []
    for k, t in corp.items():
        pos = 0; ok = True
        for f in fr:
            i = t.find(f, pos)
            if i < 0: ok = False; break
            pos = i + len(f)
        if ok: out.append(f'{k[0]}{k[1]}')
    return out

if __name__ == '__main__':
    r = run(); json.dump(r, open('/tmp/vcheck.json', 'w'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(Counter(x[4] for x in r))
    C = corpus(); X = cci_corpus(); summ = Counter(); rows = []
    for x in r:
        tag = x[4]
        if tag == 'noref':
            if len(norm(x[2])) < 4: tag = 'term'
            else:
                hit = find_in(x[2], C)
                tag = 'bible-found' if hit else ('cci-found' if all(norm(f) in X for f in x[2].split('……') if norm(f)) else 'term')
        summ[tag] += 1; rows.append(list(x) + [tag])
    print(dict(summ))
    json.dump({'summary': dict(summ), 'items': rows}, open(os.path.join(os.path.dirname(__file__), 'vcheck_report.json'), 'w'), ensure_ascii=False, indent=0)
    for x in r:
        if x[4] in ('BAD', 'err'): print(x[4], x[0], x[1], '|', x[2], '|', x[3], '|', x[5])

