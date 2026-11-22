# -*- coding: utf-8 -*-
import re, html
from lib import VERSION, DATE, TAG, automark
MK_EXTRA = {}
PAGES = [
 ('index', '🏛️', '首页', '总览与学习路径'),
 ('bible', '🌍', '整本圣经', '圣经神学 · 圣约神学'),
 ('job', '🌪️', '约伯记', '苦难中的信靠'),
 ('psalms', '🎼', '诗篇', '圣约子民的祷告与敬拜'),
 ('psalms-love', '💗', '爱上诗篇', '戈弗雷导读 · 49 章'),
 ('psalms-devotional', '🏡', '家庭灵修', '诗篇 366 天'),
 ('psalms-love-read', '📗', '爱上诗篇·阅读版', '52 章卡片 · 核心与要点'),
 ('psalms-devotional-read', '📘', '家庭灵修·阅读版', '366 天卡片 · 一句核心'),
 ('proverbs', '🦉', '箴言', '敬畏耶和华的日常智慧'),
 ('eccl', '🌫️', '传道书', '日光之下的虚空与敬畏'),
 ('song', '🌹', '雅歌', '盟约之爱的歌'),
 ('confessions', '📜', '信条对照', '三项联合信条 × 智慧书'),
 ('creeds', '🕯️', '三大信经', '干净诵读版 · 背诵'),
 ('compare', '⚖️', '信经对比', '异同 · 异端 · 为何三份'),
 ('memory', '🧠', '速记中心', '口诀 · 卡片 · 自测'),
 ('sources', '🔗', '来源', '出处与核对'),
]
S_IDX = []
def S(id, icon, title, body, cls=''):
    return f'<section id="{id}" class="sec {cls}"><h2><span class="hi">{icon}</span>{title}</h2>{body}</section>'
def H3(id, title, body=''):
    return f'<h3 id="{id}">{title}</h3>{body}'
LEGEND = ('<div class="lg">'
  '<div><span><b>加粗</b></span><small>关键词、关键句</small></div>'
  '<div><span><span class="mk-key">金色荧光</span></span><small>核心要点：必须记住</small></div>'
  '<div><span><span class="mk-god">蓝色字</span></span><small>神／基督的属性与作为</small></div>'
  '<div><span><span class="mk-christ">紫色粗体</span></span><small>指向基督（基督中心）</small></div>'
  '<div><span><span class="mk-cov">绿色实线</span></span><small>圣约、救赎历史的线索</small></div>'
  '<div><span><span class="mk-conf">紫色双线</span></span><small>信条连接（HC／BC／CD／WCF）</small></div>'
  '<div><span><span class="mk-mem">粉色底纹</span></span><small>口诀、记忆钩</small></div>'
  '<div><span><span class="mk-hard">红色波浪线</span></span><small>难点、容易误解之处</small></div>'
  '<div><span><span class="mk-dash">橙色虚线</span></span><small>有争议、位置或年代不确定</small></div>'
  '<div><span><span class="mk-sin">红色字</span></span><small>罪、错误观点、警告</small></div>'
  '<div><span><span class="mk-app">绿色底纹</span></span><small>生活应用</small></div>'
  '<div><span><span class="mk-num">前 586 年</span></span><small>年代、数字（青色等宽标签）</small></div>'
  '<div><span><span class="must-demo">📌 必背</span></span><small>金色边框区块：必须背下来的经文和口诀</small></div>'
  '<div><span>“……”＋出处</span><small>逐字引文（和合本／CCI／RTF）；「……」＝转述、概括</small></div>'
  '</div><div class="lgc">'
  '<span style="--cc:var(--gold)">🔑 要点</span><span style="--cc:var(--red)">⚠️ 难点</span><span style="--cc:var(--pink)">🧠 记忆</span><span style="--cc:var(--purple)">📜 信条</span>'
  '<span style="--cc:var(--green)">🌱 应用</span><span style="--cc:var(--red)">🚫 警示</span><span style="--cc:var(--purple)">✝️ 基督</span><span style="--cc:var(--blue)">🤝 圣约</span>'
  '<span style="--cc:var(--orange)">🏺 背景</span><span style="--cc:var(--teal)">🧭 地理</span><span style="--cc:var(--teal)">🔭 观点</span><span style="--cc:var(--mute)">📝 说明</span></div>')
CN = '一二三四五六七八九十'
def cnum(n):
    if n <= 10: return CN[n-1]
    if n < 20: return '十' + CN[n-11]
    return CN[n//10-1] + '十' + (CN[n%10-1] if n % 10 else '')
# 书卷页：把各节分成五个部分（一级目录）
BOOK_PARTS = [('核心与总览', '💎', ('core', 'glance', 'bible', 'cov')),
              ('历史 · 地理 · 文化', '🧭', ('time', 'geo', 'trade', 'zion', 'kingdom', 'pilgrim', 'anemap', 'auth', 'ctx')),
              ('结构与神学', '🧱', ('why', 'struct', 'theo', 'hard')),
              ('信条与多角度', '📜', ('conf', 'wm', 'views')),
              ('应用与记忆', '🌱', ('app', 'pdf', 'cci2', 'mem', 'pmem'))]
PAGE_PARTS = {
  'psalms-love': [('导读与总览', '💎', ('core', 'intro')), ('五卷书逐章', '📚', ('b1', 'b2', 'b3', 'b4', 'b5')), ('结论 · 对照 · 记忆', '🎆', ('final', 'notes', 'mem'))],
  'psalms-devotional': [('总览', '💎', ('core',)), ('五卷 · 310 天', '📚', ('b1', 'b2', 'b3', 'b4', 'b5')), ('附录 · 56 天', '✝️', ('a1', 'a2', 'a3')), ('对照与记忆', '🧠', ('notes', 'mem'))],
  'bible': [('核心与正典', '💎', ('core', 'canon')), ('圣经神学与圣约', '🤝', ('bt', 'cov')), ('历史与地理', '🧭', ('time', 'geo')),
            ('智慧、诗歌与信条', '🦉', ('wm', 'wis', 'poetry')), ('学习路径', '🧭', ('path',))],
  'compare': [('总览与对照', '⚖️', ('over', 'side', 'same', 'diff')), ('历史：异端与会议', '🏛️', ('here', 'map')), ('为什么三份 · 记忆', '🧠', ('why', 'wis', 'mem'))],
}
for _p in ('job', 'psalms', 'proverbs', 'eccl', 'song'): PAGE_PARTS[_p] = BOOK_PARTS
def structure(pid, main):
    """建立三级结构：一级＝部分（或无部分时的节），二级＝节／小标题，三级＝小标题／提示框。给正文标题加编号，返回 (main, toc_html)。"""
    parts = PAGE_PARTS.get(pid)
    tok = re.compile(r'<section id="([^"]+)" class="([^"]*)"><h2 id="[^"]+"><span class="hi">([^<]*)</span>(.*?)</h2>|<h3 id="([^"]+)">(.*?)</h3>|<div class="call-h">(.*?)</div>', re.S)
    out = []; pos = 0; tree = []; cur_part = None; part_of = {}
    if parts:
        for k, pt_ in enumerate(parts, 1):
            for x in pt_[2]: part_of[x] = k
    n1 = n2 = n3 = 0; ccount = {}
    sec_n = 0
    def node(lv, id, num, title, icon=''):
        return dict(lv=lv, id=id, num=num, t=re.sub(r'<[^>]+>', '', title).strip(), ic=icon, ch=[])
    for m in tok.finditer(main):
        out.append(main[pos:m.start()]); pos = m.end()
        if m.group(1):
            sid, cl, ic, title = m.group(1), m.group(2), m.group(3), m.group(4)
            if parts:
                k = part_of.get(sid.split('-', 1)[1], cur_part or 1)
                if k != cur_part:
                    cur_part = k; n1 += 1; n2 = 0
                    pt, pic = parts[k-1][0], parts[k-1][1]; pcol = parts[k-1][3] if len(parts[k-1]) > 3 else ''
                    out.append(f'<div class="part" id="{pid}-part{k}"' + (f' style="--accent:{pcol}"' if pcol else '') + '>' + f'<span class="part-n">第{cnum(n1)}部分</span><span class="part-t">{pic} {pt}</span></div>')
                    tree.append(node(1, f'{pid}-part{k}', f'{cnum(n1)}、', pt, pic))
                n2 += 1; n3 = 0; num = f'{n1}.{n2}'
                nd = node(2, sid, num, title, ic); tree[-1]['ch'].append(nd)
                out.append(f'<section id="{sid}" class="{cl}"><h2 id="{sid}-h"><span class="hi">{ic}</span><span class="hn">{num}</span>{title}</h2>')
            else:
                n1 += 1; n2 = 0; num = f'{cnum(n1)}、'
                tree.append(node(1, sid, num, title, ic))
                out.append(f'<section id="{sid}" class="{cl}"><h2 id="{sid}-h"><span class="hi">{ic}</span><span class="hn">{num}</span>{title}</h2>')
            cur_sec = sid
        elif m.group(5) or m.group(7) is not None:
            if not tree: out.append(m.group(0)); continue
            is_h3 = bool(m.group(5))
            title = m.group(6) if is_h3 else m.group(7)
            if parts:
                parent = tree[-1]['ch'][-1] if tree[-1]['ch'] else tree[-1]
                n3 += 1; num = f'{n1}.{n2}.{n3}'; lv = 3
            else:
                parent = tree[-1]; n2 += 1; num = f'{n1}.{n2}'; lv = 2
            if is_h3: hid = m.group(5)
            else:
                ccount[cur_sec] = ccount.get(cur_sec, 0) + 1; hid = f'{cur_sec}-c{ccount[cur_sec]}'
            parent['ch'].append(node(lv, hid, num, title))
            if is_h3: out.append(f'<h3 id="{hid}"><span class="hn">{num}</span>{title}</h3>')
            else: out.append(f'<div class="call-h" id="{hid}"><span class="hn">{num}</span>{title}</div>')
    out.append(main[pos:])
    def li(nd):
        kids = ''.join(li(c) for c in nd['ch'])
        tg = f'<button class="tx" type="button" aria-label="展开/折叠" aria-expanded="false"></button>' if kids else '<span class="tx0"></span>'
        ic = f'<i>{nd["ic"]}</i>' if nd['ic'] and nd['lv'] < 3 else ''
        return (f'<li class="tl{nd["lv"]}" data-k="{nd["id"]}"><div class="tr">{tg}<a href="#{nd["id"]}"><span class="tn">{nd["num"]}</span>{ic}<span class="tt">{html.escape(nd["t"])}</span></a></div>'
                + (f'<ol>{kids}</ol>' if kids else '') + '</li>')
    return ''.join(out), ''.join(li(n) for n in tree), tree
def page(pid, hero, main, accent='#f5b83d'):
    me = [p for p in PAGES if p[0] == pid][0]
    # sections lacking id on h2 -> add
    def addid(m):
        return m.group(0)
    main = automark(main, MK_EXTRA.get(pid, ()))
    def _cls(m):
        sid, cl = m.group(1), m.group(2)
        if re.search(r'-(core|theo|app|christ)$', sid) and 'key' not in cl: cl += ' key'
        if re.search(r'-(views|ane)$', sid) and 'minor' not in cl: cl += ' minor'
        return f'<section id="{sid}" class="{cl.strip()}">'
    main = re.sub(r'<section id="([^"]+)" class="([^"]*)">', _cls, main)
    main = re.sub(r'<section id="([^"]+)" class="([^"]*)"><h2>', lambda m: f'<section id="{m.group(1)}" class="{m.group(2)}"><h2 id="{m.group(1)}-h">', main)
    main, toc, _tree = structure(pid, main)
    S_IDX.extend({'p': pid + '.html', 'pt': me[2], 'id': id, 't': re.sub(r'<span class="hn">.*?</span>|<[^>]+>', '', t)} for lv, id, t in re.findall(r'<(h2|h3) id="([^"]+)">(.*?)</\1>', main))
    nav = ''.join(f'<a class="pg{" on" if p[0]==pid else ""}" href="{p[0]}.html"><i>{p[1]}</i><span>{p[2]}</span></a>' for p in PAGES if '-' not in p[0] or p[0] == pid)
    pnav = ''.join(f'<li><a class="{"on" if p[0]==pid else ""}" href="{p[0]}.html"><i>{p[1]}</i>{p[2]}<small>{p[3]}</small></a></li>' for p in PAGES)
    i = [p[0] for p in PAGES].index(pid)
    prev = PAGES[i-1] if i > 0 else None; nxt = PAGES[i+1] if i < len(PAGES)-1 else None
    pn = '<nav class="pn">' + (f'<a href="{prev[0]}.html">← {prev[1]} {prev[2]}</a>' if prev else '<span></span>') + (f'<a href="{nxt[0]}.html">{nxt[1]} {nxt[2]} →</a>' if nxt else '<span></span>') + '</nav>'
    title = f'{me[2]} · 诗歌智慧书深读（欧陆改革宗）'
    return f'''<!doctype html><html lang="zh-CN" data-theme="night"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="约伯记·诗篇·箴言·传道书·雅歌 —— 欧陆改革宗、圣经神学与圣约神学深度解读（{TAG}）">
<meta name="theme-color" content="#090d21"><link rel="icon" href="assets/icon.svg"><meta name="color-scheme" content="dark light">
<script>try{{var t=localStorage.getItem('pw-theme');if(t)document.documentElement.dataset.theme=t;var f=localStorage.getItem('pw-fs');if(f)document.documentElement.style.setProperty('--fs',f+'px');if(localStorage.getItem('pw-toc')==='0')document.documentElement.classList.add('toc-off');var w=+localStorage.getItem('pw-tocw');if(w>=220)document.documentElement.style.setProperty('--tocw',Math.min(w,innerWidth*.96)+'px')}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/app.css?v={VERSION}">
<script src="assets/app.js?v={VERSION}" defer></script>{'<script src="assets/map.js?v=' + VERSION + '" defer></script>' if 'class="mapfig"' in main else ''}</head>
<body class="p-{pid}" style="--accent:{accent}">
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
<div id="prog" aria-hidden="true"></div>
<header class="top"><button id="tocbtn" class="ib" aria-label="显示/隐藏目录" title="目录（T）">☰</button>
<a class="brand" href="index.html"><b>诗歌智慧书</b><small>GROKstudy · {VERSION}</small></a>
<nav class="pages" aria-label="页面">{nav}</nav>
<div class="tools"><button class="ib" id="legbtn" aria-label="标记图例" title="标记图例（L）">🖍️</button><button class="ib" id="fsm" aria-label="A- 缩小字号">A-</button><button class="ib" id="fsp" aria-label="A+ 放大字号">A+</button><button class="ib" id="themebtn" aria-label="切换主题">🌓</button></div></header>
<aside id="toc" aria-label="目录"><div class="toc-bar"><b>📑 目录</b><span><button class="mini" id="tocfull" title="全宽／还原">⤢</button><button class="mini" id="tocx" title="隐藏目录">✕</button></span></div><div class="toc-in">
<input id="q" type="search" placeholder="🔍 搜索全站标题…" aria-label="搜索"><ol id="qres"></ol>
<div class="toc-h">本页目录<span class="toc-lv" role="group" aria-label="展开层级"><button class="mini" data-lv="1" title="只看一级">一级</button><button class="mini" data-lv="2" title="展开到二级">二级</button><button class="mini" data-lv="3" title="全部展开">三级</button></span></div><ol class="toc-list" data-pid="{pid}">{toc}</ol>
<div class="toc-h">全站页面</div><ol class="toc-pages">{pnav}</ol></div><div id="tocgrip" role="separator" aria-orientation="vertical" aria-label="拖动调整目录宽度" aria-valuenow="300" aria-valuemin="220" aria-valuemax="820" tabindex="0" title="拖动调整宽度（双击还原）"></div></aside>
<div id="scrim"></div>
<div id="legpop" role="dialog" aria-label="笔记标记图例"><h4>🖍️ 笔记标记图例 <button class="mini" id="legx" aria-label="关闭图例">关闭</button></h4>{LEGEND}</div>
<main id="main"><div class="hero">{hero}</div>{main}{pn}
<footer class="foot"><p>📚 {TAG} · 版本 {VERSION} · {DATE}（台北时间） · <a href="sources.html#o-ver">版本记录</a></p><p>信经与三项联合信条原文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>；威斯敏斯特标准逐字取自 <a href="https://rtf-usa.com/wp-content/uploads/2024/08/RTF-Westminster-Standards-FINAL-DIGITAL.pdf" target="_blank" rel="noopener">RTF-USA 简体中文新版</a>；经文取自和合本（新标点，信望爱站 FHL 接口）。本站讲解文字为学习用概述。</p></footer></main>
<nav id="fab" aria-label="快速导航"><div class="fab-m" id="fabm"><button type="button" data-go="back" aria-label="返回上一页" title="返回（Alt+←）"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" data-go="fwd" aria-label="前进到下一页" title="前进（Alt+→）"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button><button type="button" data-go="top" aria-label="回到顶部" title="顶部（Home）"><svg viewBox="0 0 24 24"><path d="M6 5h12M12 19V9m-5 5l5-5 5 5"/></svg></button><button type="button" data-go="bot" aria-label="到页面底部" title="底部（End）"><svg viewBox="0 0 24 24"><path d="M6 19h12M12 5v10m-5-5l5 5 5-5"/></svg></button><button type="button" data-go="toc" aria-label="显示或隐藏目录" title="目录（T）"><svg viewBox="0 0 24 24"><path d="M5 7h14M5 12h10M5 17h12"/></svg></button><a href="index.html" data-go="home" aria-label="回到首页" title="首页"><svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7M6 10v9h4v-5h4v5h4v-9"/></svg></a></div><button type="button" id="fabt" aria-expanded="false" aria-controls="fabm" aria-label="快速导航" title="快速导航"><svg viewBox="0 0 24 24" class="fab-i"><circle cx="12" cy="12" r="1.6"/><circle cx="6" cy="12" r="1.6"/><circle cx="18" cy="12" r="1.6"/></svg><svg class="fab-ring" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18" pathLength="100"/></svg></button></nav>
</body></html>'''
def hero(icon, title, sub, core, chips=(), extra=''):
    ch = ''.join(f'<span class="chip" style="--c:{c}">{t}</span>' for t, c in chips)
    return f'<div class="hero-in"><div class="hero-ic">{icon}</div><div><h1>{title}</h1><p class="sub">{sub}</p><p class="core">💎 {core}</p><div class="chips">{ch}</div>{extra}</div></div>'
