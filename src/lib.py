# -*- coding: utf-8 -*-
import json, re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cuv
VERSION = "v1.0.0"; DATE = "2026-10-23"; TAG = "poetry-wisdom-20261023-v1-GROKstudy"
CCI = '/workspace/cci/'
HC = json.load(open(CCI + 'heidelberg.json')); BC = json.load(open(CCI + 'belgic.json')); CD = json.load(open(CCI + 'dort.json'))
CR = json.load(open(CCI + 'creeds.json'))
HCQ_ = {q['q']: (ld['number'], q) for ld in HC['lordsdays'] for q in ld['questions']}
BCA_ = {a['number']: a for a in BC['articles']}
INDEX = {}
for line in open(CCI + 'text/INDEX.md'):
    p = [x.strip() for x in line.split('|')]
    if len(p) > 4 and p[1].endswith('.txt'): INDEX[p[1]] = (p[2], p[3])
BOOKN = {'伯': '约伯记', '诗': '诗篇', '箴': '箴言', '传': '传道书', '歌': '雅歌', '创': '创世记', '出': '出埃及记', '申': '申命记', '王上': '列王纪上', '撒下': '撒母耳记下', '赛': '以赛亚书', '耶': '耶利米书', '结': '以西结书', '哀': '耶利米哀歌', '何': '何西阿书', '玛': '玛拉基书', '太': '马太福音', '路': '路加福音', '约': '约翰福音', '徒': '使徒行传', '罗': '罗马书', '林前': '哥林多前书', '林后': '哥林多后书', '弗': '以弗所书', '西': '歌罗西书', '来': '希伯来书', '雅': '雅各书', '启': '启示录', '彼前': '彼得前书', '腓': '腓立比书', '代下': '历代志下', '撒上': '撒母耳记上', '拉': '以斯拉记', '尼': '尼希米记', '利': '利未记', '民': '民数记', '加': '加拉太书', '约壹': '约翰一书'}
CUV_USED = []
def esc(s): return html.escape(s, quote=False)
def sup(t):  # CCI 脚注标记 ^N -> <sup>
    return re.sub(r'\^(\d+)', r'<sup class="fn">\1</sup>', esc(t))
# ---------- 经文 ----------
def vtext(bk, ch, sec):
    recs = cuv.verse(bk, ch, sec); CUV_USED.append(f'{bk}{ch}:{sec}')
    return recs
def V(bk, ch, sec, note='', cls=''):
    recs = vtext(bk, ch, sec)
    body = ''.join(f'<span class="vn">{n}</span>{esc(t)}' for n, t in recs)
    return f'<blockquote class="verse {cls}"><p>{body}</p><cite>📖 {BOOKN.get(bk,bk)} {ch}:{sec}（和合本）{note}</cite></blockquote>'
def VI(bk, ch, sec):
    recs = vtext(bk, ch, sec)
    return f'<q class="vi">{esc("".join(t for _, t in recs))}</q><span class="vref">（{bk}{ch}:{sec}）</span>'
def R(s): return f'<span class="ref">{s}</span>'
# ---------- 信条 ----------
def HCQ(n, refs=False, hi=None):
    ld, q = HCQ_[n]
    a = sup(q['answer'])
    if hi:
        if isinstance(hi, str): hi = [hi]
        for h in hi: a = a.replace(esc(h), f'<mark class="k">{esc(h)}</mark>')
    rf = ''
    if refs and q['refs']:
        rf = '<details class="refs"><summary>经文脚注（CCI）</summary><ol>' + ''.join(f'<li>{esc(r)}</li>' for r in q['refs']) + '</ol></details>'
    return (f'<div class="conf hc"><div class="conf-h">📘 海德堡要理问答 · 主日{ld} · 第{n}问</div>'
            f'<p class="q">{sup(q["question"])}</p><p class="a">{a}</p>{rf}'
            f'<a class="src" href="https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
def BCA(n, part=None, refs=False):
    a = BCA_[n]; t = a['text']
    if part:
        i = t.find(part[0]); j = t.find(part[1], i)
        assert i >= 0 and j >= 0, (n, part)
        t = ('……' if i > 0 else '') + t[i:j + len(part[1])] + ('……' if j + len(part[1]) < len(t) else '')
    paras = ''.join(f'<p>{sup(p)}</p>' for p in t.split('\n') if p.strip())
    rf = ''
    if refs and a['refs']:
        rf = '<details class="refs"><summary>经文脚注（CCI）</summary><ol>' + ''.join(f'<li>{esc(r)}</li>' for r in a['refs']) + '</ol></details>'
    return (f'<div class="conf bc"><div class="conf-h">📗 比利时信条 · {esc(a["title"])}</div>{paras}{rf}'
            f'<a class="src" href="{a["url"]}" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
def CDA(head, n, part=None):
    hd = CD['heads'][head]; a = [x for x in hd['articles'] if x['number'] == n][0]
    t = a['text'].split('\n\n- ')[0]
    if part:
        i = t.find(part[0]); j = t.find(part[1], i); assert i >= 0 and j >= 0, (head, n, part)
        t = ('……' if i > 0 else '') + t[i:j + len(part[1])] + '……'
    paras = ''.join(f'<p>{sup(p)}</p>' for p in t.split('\n') if p.strip())
    return (f'<div class="conf cd"><div class="conf-h">📕 多特信经 · {esc(hd["title"])} · {esc(a["title"])}</div>{paras}'
            f'<a class="src" href="{a["url"]}" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
def cci_text(fn): return open(CCI + 'text/' + fn).read()
def CX(fn, start, end, note=''):
    t = cci_text(fn); i = t.find(start); j = t.find(end, i)
    assert i >= 0 and j >= 0, (fn, start, end)
    ex = t[i:j + len(end)]
    title, url = INDEX[fn]
    paras = ''.join(f'<p>{esc(p)}</p>' for p in ex.split('\n') if p.strip())
    return (f'<div class="cci"><div class="conf-h">⛪ CCI 讲章／书籍摘录 · 《{esc(title)}》</div>{paras}'
            f'<a class="src" href="{url}" target="_blank" rel="noopener">原文 · {url.replace("https://","")}</a>{("<p class=note>"+note+"</p>") if note else ""}</div>')
# ---------- 组件 ----------
def C(kind, title, body):
    ic = dict(key='🔑', hard='⚠️', app='🌱', christ='✝️', cov='🤝', mem='🧠', ctx='🏺', geo='🧭', why='❓', view='🔭', note='📝').get(kind, '•')
    return f'<div class="call {kind}"><div class="call-h">{ic} {title}</div><div class="call-b">{body}</div></div>'
def grid(*cards, cls=''): return f'<div class="grid {cls}">' + ''.join(cards) + '</div>'
def card(title, body, icon='', color='', cls=''):
    st = f' style="--c:{color}"' if color else ''
    return f'<div class="card {cls}"{st}><h4>{icon} {title}</h4><div>{body}</div></div>'
def table(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl {cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def flow(steps, cls=''):
    """steps: (icon,title,text,color)"""
    return f'<div class="flow {cls}">' + ''.join(f'<div class="step" style="--c:{c}"><div class="si">{i}</div><b>{t}</b><span>{x}</span></div>' for i, t, x, c in steps) + '</div>'
def timeline(items):
    """items: (年代, 标题, 说明, 颜色, 标签)"""
    return '<ol class="tl">' + ''.join(f'<li style="--c:{c}"><div class="tl-d">{d}</div><div class="tl-c"><b>{t}</b>{"<em class=tag>"+g+"</em>" if g else ""}<p>{x}</p></div></li>' for d, t, x, c, g in items) + '</ol>'
def mm(root, branches):
    """思维导图：root, branches=[(标题, 颜色, [叶...])]"""
    s = f'<div class="mm"><div class="mm-root">{root}</div><div class="mm-br">'
    for t, c, leaves in branches:
        s += f'<div class="mm-b" style="--c:{c}"><div class="mm-bt">{t}</div><ul>' + ''.join(f'<li>{l}</li>' for l in leaves) + '</ul></div>'
    return s + '</div></div>'
def cards_flip(items):
    """items: (正面, 背面)"""
    return '<div class="flips">' + ''.join(f'<button class="flip" aria-label="翻转卡片"><span class="ff">{a}</span><span class="fb">{b}</span></button>' for a, b in items) + '</div>'
def quiz(qid, items):
    """items: (题, [选项], 正确索引, 解析)"""
    s = f'<div class="quiz" id="quiz-{qid}">'
    for k, (q, opts, ok, ex) in enumerate(items):
        s += f'<div class="qz" data-ok="{ok}"><p class="qq">{k+1}. {q}</p><div class="qo">' + ''.join(f'<button data-i="{i}">{o}</button>' for i, o in enumerate(opts)) + f'</div><p class="qx">{ex}</p></div>'
    return s + f'<div class="qscore">得分：<b>0</b> / {len(items)}</div></div>'
def stat(items):
    return '<div class="stats">' + ''.join(f'<div class="st" style="--c:{c}"><b data-count="{n}">{n}</b><span>{l}</span></div>' for n, l, c in items) + '</div>'
def facts(rows):
    return '<dl class="facts">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'
