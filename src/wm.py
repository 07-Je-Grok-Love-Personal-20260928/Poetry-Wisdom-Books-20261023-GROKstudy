# -*- coding: utf-8 -*-
"""威斯敏斯特标准逐字引文：RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，© 2024 RTF-USA，免费分发）。
文字取自 data/westminster_rtf.json（由该 PDF 解析），每段引文在构建时都要在 PDF 全文（data/rtf_live.txt）中逐字找到，否则构建失败。"""
import json, os, re, unicodedata, html
B = os.path.join(os.path.dirname(__file__), '..', 'data')
RTF_URL = 'https://rtf-usa.com/wp-content/uploads/2024/08/RTF-Westminster-Standards-FINAL-DIGITAL.pdf'
RTF_NAME = 'RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，2024）'
D = json.load(open(os.path.join(B, 'westminster_rtf.json')))
PAGES = open(os.path.join(B, 'rtf_live.txt')).read().split('\f')
def n(s): return re.sub(r'[^\u4e00-\u9fff]', '', unicodedata.normalize('NFKC', s))
NP = [n(p) for p in PAGES]; ALL = ''.join(NP)
WCF = {c['no']: (c['title'], {s['sec']: s for s in c['secs']}) for c in D['wcf']}
WSC = {q['q']: q for q in D['wsc']}; WLC = {q['q']: q for q in D['wlc']}
USED = []
def page_of(t):
    k = n(t)[:14]
    for i, p in enumerate(NP):
        if k in p: return i + 1
    for i in range(len(NP) - 1):
        if k in NP[i][-40:] + NP[i + 1][:60]: return i + 1
    return None
def verified(t):
    """逐字核对：允许 PDF 中因换页插入的页脚（经文脚注、页码），引文本身必须按顺序连续出现。"""
    x = n(t)
    if x in ALL: return True
    pos = None; k = 0
    while k < len(x):
        best = 0; bpos = -1
        lo = 6 if len(x) - k >= 6 else len(x) - k
        seg = x[k:k + lo]
        start = 0 if pos is None else pos
        end = len(ALL) if pos is None else pos + 2500
        i = ALL.find(seg, start, end)
        while i >= 0:
            L = lo
            while k + L < len(x) and i + L < len(ALL) and ALL[i + L] == x[k + L]: L += 1
            if L > best: best, bpos = L, i
            if pos is not None: break
            i = ALL.find(seg, i + 1, end)
        if best == 0: return False
        if pos is not None and bpos > pos:
            gap = ALL[pos:bpos]
            if len(gap) < 12 or len(re.findall(r'(?:书|记|篇|福音|箴言|雅歌|启示录|使徒行传|耶利米哀歌)', gap)) < 2: return False
        k += best; pos = bpos + best
    return True
def fn(t): return re.sub(r'⟦(\d+)⟧', r'<sup class="fn">\1</sup>', html.escape(t, quote=False))
def W(kind, no, sec=None, part=None, refs=True, hi=(), book=None):
    """kind: WCF/WSC/WLC；part=(起, 止) 取摘录。"""
    if kind == 'WCF':
        title, secs = WCF[no]; u = secs[sec]; text = u['text']; head = f'西敏信仰告白 · 第{no}章 {title} · 第{sec}节'; tag = f'WCF {no}.{"一二三四五六七八九十".index(sec[-1]) + 1 + (10 if len(sec) > 1 else 0)}'
        q = ''
    else:
        u = (WSC if kind == 'WSC' else WLC)[no]; text = u['ans']; q = u['ques']
        head = f'{"西敏小要理问答" if kind == "WSC" else "西敏大要理问答"} · 第{no}问'; tag = f'{kind} {no}'
    if part:
        i = text.find(part[0]); j = text.find(part[1], i); assert i >= 0 and j >= 0, (kind, no, sec, part)
        text = ('……' if i > 0 else '') + text[i:j + len(part[1])] + ('……' if j + len(part[1]) < len(u.get('text', u.get('ans'))) else '')
    plain = re.sub(r'⟦\d+⟧', '', text)
    for seg in re.split(r'……', plain):
        assert verified(seg), ('NOT VERBATIM in RTF PDF', kind, no, sec, seg[:40])
    if q: assert verified(q), ('question not verbatim', kind, no)
    pg = page_of(re.sub(r'⟦\d+⟧', '', text).strip('…')[:30])
    body = fn(text)
    for h in hi: body = body.replace(html.escape(h, quote=False), f'<mark class="k">{html.escape(h, quote=False)}</mark>')
    used_fn = [int(x) for x in re.findall(r'⟦(\d+)⟧', text)]
    rf = ''
    if refs and u.get('refs'):
        items = [(k, v) for k, v in u['refs'].items() if int(k) in used_fn] if used_fn else list(u['refs'].items())
        hitk = [k for k, v in items if book and book in v]
        for k in hitk: body = body.replace(f'<sup class="fn">{k}</sup>', f'<sup class="fn hit">{k}</sup>')
        rf = (f'<details class="refs"{" open" if hitk else ""}><summary>经文脚注（RTF 译本）</summary><ol>' +
              ''.join(f'<li value="{k}"{" class=\"hit\"" if k in hitk else ""}>{html.escape(v)}</li>' for k, v in items) + '</ol></details>')
    USED.append(tag)
    qh = f'<p class="q">问：{html.escape(q)}</p>' if q else ''
    return (f'<div class="conf wm"><div class="conf-h">🏛️ {head}</div>{qh}<p class="a">{"答：" if q else ""}{body}</p>{rf}'
            f'<a class="src" href="{RTF_URL}" target="_blank" rel="noopener">原文 · {RTF_NAME}{f" · PDF 第 {pg} 页" if pg else ""}</a></div>')
BOOKS = {'约伯记': 'job', '诗篇': 'psa', '箴言': 'pro', '传道书': 'ecc', '雅歌': 'song'}
def index_refs():
    """五卷书在西敏三份文件经文脚注中的出现：{book: [(tag, 单位文字, 脚注号, 脚注)]}"""
    out = {b: [] for b in BOOKS}
    for c in D['wcf']:
        for s in c['secs']:
            for k, v in s.get('refs', {}).items():
                for b in BOOKS:
                    if b in v: out[b].append(('WCF', c['no'], s['sec'], k, v))
    for kind in ('WSC', 'WLC'):
        for q in D[kind.lower()]:
            for k, v in q.get('refs', {}).items():
                for b in BOOKS:
                    if b in v: out[b].append((kind, q['q'], None, k, v))
    return out
CN2N = {c: i + 1 for i, c in enumerate('一二三四五六七八九十')}
CN2N.update({'十' + c: 11 + i for i, c in enumerate('一二三四五六七八九')})
def unit(kind, no, sec=None):
    return WCF[no][1][sec] if kind == 'WCF' else (WSC if kind == 'WSC' else WLC)[no]
