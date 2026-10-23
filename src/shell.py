# -*- coding: utf-8 -*-
import re, html
from lib import VERSION, DATE, TAG
PAGES = [
 ('index', '🏛️', '首页', '总览与学习路径'),
 ('bible', '🌍', '整本圣经', '圣经神学 · 圣约神学'),
 ('job', '🌪️', '约伯记', '苦难中的信靠'),
 ('psalms', '🎼', '诗篇', '圣约子民的祷告与敬拜'),
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
def build_toc(main):
    items = re.findall(r'<(h2|h3) id="([^"]+)">(.*?)</\1>', main)
    out = []; open_ = False
    for lv, id, t in items:
        t = re.sub(r'<[^>]+>', '', t)
        if lv == 'h2':
            if open_: out.append('</ul></li>')
            out.append(f'<li class="t2"><a href="#{id}">{t}</a><ul>'); open_ = True
        else:
            out.append(f'<li class="t3"><a href="#{id}">{t}</a></li>')
    if open_: out.append('</ul></li>')
    return ''.join(out).replace('<ul></ul>', '')
def page(pid, hero, main, accent='#f5b83d'):
    me = [p for p in PAGES if p[0] == pid][0]
    # sections lacking id on h2 -> add
    def addid(m):
        return m.group(0)
    main = re.sub(r'<section id="([^"]+)" class="([^"]*)"><h2>', lambda m: f'<section id="{m.group(1)}" class="{m.group(2)}"><h2 id="{m.group(1)}-h">', main)
    toc = build_toc(main)
    S_IDX.extend({'p': pid + '.html', 'pt': me[2], 'id': id, 't': re.sub(r'<[^>]+>', '', t)} for lv, id, t in re.findall(r'<(h2|h3) id="([^"]+)">(.*?)</\1>', main))
    nav = ''.join(f'<a class="pg{" on" if p[0]==pid else ""}" href="{p[0]}.html"><i>{p[1]}</i><span>{p[2]}</span></a>' for p in PAGES)
    pnav = ''.join(f'<li><a class="{"on" if p[0]==pid else ""}" href="{p[0]}.html"><i>{p[1]}</i>{p[2]}<small>{p[3]}</small></a></li>' for p in PAGES)
    i = [p[0] for p in PAGES].index(pid)
    prev = PAGES[i-1] if i > 0 else None; nxt = PAGES[i+1] if i < len(PAGES)-1 else None
    pn = '<nav class="pn">' + (f'<a href="{prev[0]}.html">← {prev[1]} {prev[2]}</a>' if prev else '<span></span>') + (f'<a href="{nxt[0]}.html">{nxt[1]} {nxt[2]} →</a>' if nxt else '<span></span>') + '</nav>'
    title = f'{me[2]} · 诗歌智慧书深读（欧陆改革宗）'
    return f'''<!doctype html><html lang="zh-CN" data-theme="night"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="约伯记·诗篇·箴言·传道书·雅歌 —— 欧陆改革宗、圣经神学与圣约神学深度解读（{TAG}）">
<meta name="theme-color" content="#0b1226"><link rel="icon" href="assets/icon.svg">
<script>try{{var t=localStorage.getItem('pw-theme');if(t)document.documentElement.dataset.theme=t;var f=localStorage.getItem('pw-fs');if(f)document.documentElement.style.setProperty('--fs',f+'px');if(localStorage.getItem('pw-toc')==='0')document.documentElement.classList.add('toc-off')}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/app.css?v={VERSION}"></head>
<body class="p-{pid}" style="--accent:{accent}">
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
<div id="prog" aria-hidden="true"></div>
<header class="top"><button id="tocbtn" class="ib" aria-label="显示/隐藏目录" title="目录（T）">☰</button>
<a class="brand" href="index.html"><b>诗歌智慧书</b><small>GROKstudy · {VERSION}</small></a>
<nav class="pages" aria-label="页面">{nav}</nav>
<div class="tools"><button class="ib" id="fsm" aria-label="缩小字号">A-</button><button class="ib" id="fsp" aria-label="放大字号">A+</button><button class="ib" id="themebtn" aria-label="切换主题">🌓</button></div></header>
<aside id="toc" aria-label="目录"><div class="toc-in">
<input id="q" type="search" placeholder="🔍 搜索全站标题…" aria-label="搜索"><ol id="qres"></ol>
<div class="toc-h">本页目录 <button class="mini" id="tocall">全部展开</button></div><ol class="toc-list">{toc}</ol>
<div class="toc-h">全站页面</div><ol class="toc-pages">{pnav}</ol></div></aside>
<div id="scrim"></div>
<main id="main"><div class="hero">{hero}</div>{main}{pn}
<footer class="foot"><p>📚 {TAG} · 版本 {VERSION} · {DATE}（台北时间）</p><p>信经与三项联合信条原文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>；威斯敏斯特标准逐字取自 <a href="https://rtf-usa.com/wp-content/uploads/2024/08/RTF-Westminster-Standards-FINAL-DIGITAL.pdf" target="_blank" rel="noopener">RTF-USA 简体中文新版</a>；经文取自和合本（新标点，信望爱站 FHL 接口）。本站讲解文字为学习用概述。</p></footer></main>
<button id="totop" aria-label="回到顶部">↑</button>
<script src="assets/search.js?v={VERSION}"></script><script src="assets/app.js?v={VERSION}"></script></body></html>'''
def hero(icon, title, sub, core, chips=(), extra=''):
    ch = ''.join(f'<span class="chip" style="--c:{c}">{t}</span>' for t, c in chips)
    return f'<div class="hero-in"><div class="hero-ic">{icon}</div><div><h1>{title}</h1><p class="sub">{sub}</p><p class="core">💎 {core}</p><div class="chips">{ch}</div>{extra}</div></div>'
