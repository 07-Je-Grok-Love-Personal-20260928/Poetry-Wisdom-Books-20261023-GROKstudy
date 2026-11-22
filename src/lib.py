# -*- coding: utf-8 -*-
import json, re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cuv
VERSION = "v4.2.0"; DATE = "2026-11-22"; TAG = "poetry-wisdom-20261122-v4.2.0-GROKstudy"
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
    return '<div class="flips">' + ''.join(f'<button class="flip" title="翻转卡片"><span class="ff">{a}</span><span class="fb">{b}</span></button>' for a, b in items) + '</div>'
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

# ================= v2.0.0：本质核心、动态故事线、笔记标记 =================
def story_dg(nodes, title='故事线'):
    """nodes: [(emoji, 短标签≤4字, 小字≤9字, 颜色)] → 动画 SVG 故事线（移动光点 + 依次脉动的节点）"""
    n = len(nodes); W = 600; H = 236; xs = [50 + i * (W - 100) / (n - 1) for i in range(n)]
    ys = [92 + (26 if i % 2 else -10) for i in range(n)]
    d = f'M{xs[0]:.0f},{ys[0]}' + ''.join(f' C{(xs[i-1]+xs[i])/2:.0f},{ys[i-1]} {(xs[i-1]+xs[i])/2:.0f},{ys[i]} {xs[i]:.0f},{ys[i]}' for i in range(1, n))
    pid = 'sp' + str(abs(hash(title)) % 10**8)
    s = [f'<div class="dg anim"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
         f'<defs><linearGradient id="{pid}g" x1="0" x2="1">' + ''.join(f'<stop offset="{i/(n-1):.2f}" stop-color="{c}"/>' for i, (_, _, _, c) in enumerate(nodes)) + '</linearGradient></defs>',
         f'<path id="{pid}" d="{d}" fill="none" stroke="url(#{pid}g)" stroke-width="6" stroke-linecap="round" opacity=".55"/>',
         f'<path d="{d}" fill="none" stroke="#fff" stroke-width="2" class="flowd" opacity=".5"/>',
         f'<circle r="8" fill="#fff" class="dg-dot" style="offset-path:path(\'{d}\');animation-duration:{2.2*n:.1f}s"/>']
    for i, (e, t, sub, c) in enumerate(nodes):
        x, y = xs[i], ys[i]
        s.append(f'<g><circle cx="{x:.0f}" cy="{y}" r="30" fill="{c}" opacity=".22" class="pulse" style="animation-delay:{i*.45:.2f}s"/>'
                 f'<circle cx="{x:.0f}" cy="{y}" r="22" fill="{c}"/><text x="{x:.0f}" y="{y+9}" text-anchor="middle" font-size="24">{e}</text>'
                 f'<text x="{x:.0f}" y="{y+58}" text-anchor="middle" font-size="21" font-weight="800" style="fill:{c}">{esc(t)}</text>'
                 f'<text x="{x:.0f}" y="{y+82}" text-anchor="middle" class="t2" font-size="15">{esc(sub)}</text>'
                 f'<text x="{x:.0f}" y="{y-38}" text-anchor="middle" font-size="15" font-weight="800" opacity=".7">{i+1}</text></g>')
    s.append('</svg></div>')
    return ''.join(s)
def kws(items):   # [(icon, 词, 小字, 颜色)]
    return '<div class="kws">' + ''.join(f'<span class="kw" style="--c:{c}"><i>{i}</i>{t}<small>{s}</small></span>' for i, t, s, c in items) + '</div>'
def www(why, what, how, who=None):
    cols = [('❓ 为什么写', why, 'var(--blue)'), ('📖 写了什么', what, 'var(--gold)'), ('🌱 怎么活出来', how, 'var(--green)')]
    if who: cols.append(('✝️ 怎样指向基督', who, 'var(--purple)'))
    return '<div class="www">' + ''.join(f'<div style="--c:{c}"><h4>{h}</h4>{b}</div>' for h, b, c in cols) + '</div>'
def CORE(thesis, kw, why, what, how, christ, story, verse, mnemonic, extra=''):
    return (f'<p class="thesis">💎 {thesis}</p>' + kws(kw) + story + www(why, what, how, christ) +
            f'<div class="must"><span class="must-tag">📌 必背</span>{verse}' + C('mem', '一句口诀记全书', f'<span class="mk-mem">{mnemonic}</span>') + '</div>' + extra)
def media(src, title, note):
    """外部视频：点击后才载入（facade），不影响首屏性能"""
    return f'<figure class="mediafig"><div class="media"><button type="button" data-src="{src}" data-title="{esc(title)}">▶ 点击播放：{esc(title)}</button></div><figcaption>🎬 {note}</figcaption></figure>'

# ---------- 自动笔记标记（构建时；不进入逐字引文、标题、SVG） ----------
MK_TERMS = [
    ('mk-key', ['敬畏耶和华', '敬畏神', '智慧的开端', '无故的敬畏', '日光之下', '唯一的安慰', '盟约之爱', '虚空的虚空']),
    ('mk-cov', ['恩典之约', '行为之约', '大卫之约', '亚伯拉罕之约', '西奈之约', '救赎历史', '圣约神学', '圣约家庭', '圣约']),
    ('mk-god', ['主权', '护理', '创造主', '神的智慧', '耶和华作王', '独一的神']),
    ('mk-christ', ['基督', '弥赛亚', '救赎主', '中保', '受膏者', '比所罗门更大', '道成肉身', '新郎']),
    ('mk-sin', ['机械报应论', '报应论', '撒但', '愚昧人', '禁欲主义', '成功神学', '享乐主义', '虚无主义', '偶像', '异端']),
    ('mk-hard', ['咒诅诗', '寓意解经', '难点']),
    ('mk-dash', ['位置不确定', '不确定', '有争议', '说法一', '说法二', '说法三', '说法之一']),
]
MK_CONF = re.compile(r'(?:HC|BC|WCF|WSC|WLC|CD)\s?\d+(?:[.．:：]\d+)?(?:[–-]\d+)?|多特信经|比利时信条|海德堡要理问答|威斯敏斯特信仰告白')
MK_NUM = re.compile(r'约?(?:主)?前\s?\d{3,4}(?:[–-]\d{3,4})?(?:\s?年)?')
SKIP_CLS = ('conf', 'cci', 'creed', 'creed-box', 'chip', 'tag', 'ref', 'vref', 'kw', 'lg', 'lgc', 'map-legend', 'st-steps', 'thesis', 'mk-', 'tl-d', 'ctools', 'mtabs', 'lsrc', 'pn', 'q', 'src', 'conf-h', 'call-h')
SKIP_TAG = {'svg', 'script', 'style', 'h1', 'h2', 'h3', 'h4', 'a', 'button', 'th', 'mark', 'b', 'strong', 'q', 'blockquote', 'summary', 'figcaption', 'nav', 'dt', 'code', 'cite', 'title', 'textarea', 'select', 'option', 'sup', 'em'}
VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'wbr', 'source', 'col', 'area', 'base', 'embed', 'param', 'track'}
BLOCK = {'p', 'li', 'td', 'div', 'dd', 'section', 'ul', 'ol', 'figure', 'details', 'table', 'tr'}
def automark(main, extra=(), per_sec=12):
    terms = [(c, t) for c, ts in list(MK_TERMS) + list(extra) for t in ts]
    terms.sort(key=lambda x: -len(x[1]))
    alt = re.compile('|'.join(re.escape(t) for _, t in terms) + '|' + MK_CONF.pattern + '|' + MK_NUM.pattern)
    cls_of = {t: c for c, t in terms}
    toks = re.split(r'(<[^>]+>)', main); stack = []; out = []; used = set(); cnt = 0; depth = 0; nmark = 0
    for tk in toks:
        if tk.startswith('<'):
            m = re.match(r'<\s*(/)?\s*([a-zA-Z0-9]+)([^>]*)>', tk)
            if m:
                close, tag, rest = m.group(1), m.group(2).lower(), m.group(3)
                if tag == 'section' and not close: used = set(); cnt = 0
                if tag in BLOCK: depth = 0
                if close:
                    for i in range(len(stack) - 1, -1, -1):
                        if stack[i][0] == tag: del stack[i:]; break
                elif tag not in VOID and not rest.rstrip().endswith('/'):
                    cm = re.search(r'class="([^"]*)"', rest)
                    stack.append((tag, cm.group(1) if cm else ''))
            out.append(tk); continue
        if not tk or not stack or tk.isspace(): out.append(tk); continue
        skip = any(t in SKIP_TAG or any(c == k or c.startswith(k) for c in cl.split() for k in SKIP_CLS) for t, cl in stack)
        if skip:
            depth += tk.count('“') - tk.count('”'); out.append(tk); continue
        res = []; pos = 0
        for mm in alt.finditer(tk):
            seg = tk[pos:mm.start()]; depth += seg.count('“') - seg.count('”'); res.append(seg); pos = mm.end()
            w = mm.group(0); c = cls_of.get(w) or ('mk-num' if MK_NUM.fullmatch(w) else 'mk-conf')
            key = w if c not in ('mk-conf', 'mk-num') else c + ':' + w
            if depth <= 0 and cnt < per_sec and key not in used:
                res.append(f'<span class="{c}">{w}</span>'); used.add(key); cnt += 1; nmark += 1
            else: res.append(w)
        seg = tk[pos:]; depth += seg.count('“') - seg.count('”'); res.append(seg)
        out.append(''.join(res))
    automark.count = getattr(automark, 'count', 0) + nmark
    return ''.join(out)
