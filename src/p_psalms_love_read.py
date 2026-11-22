# -*- coding: utf-8 -*-
"""v4.2.0：《爱上诗篇》阅读版——按原书目录 52 个单元；每单元一句核心、3–5 个短要点、指向基督、应用、可折叠的细读与原书讨论题。全部为本站原创转述（讨论题除外，注明出自原书），不含原书页码。"""
from lib import *
import shell
from shell import S, hero
import readdata.god_a as GA
for _n in 'bcdefgh': __import__('readdata.god_' + _n)
from readdata.god_tight import T
U = GA.U
SRC = '《爱上诗篇》（W. Robert Godfrey 著，中文版）'
BKC = ['#3ddc97', '#5ab0ff', '#ff9f43', '#b48cff', '#f5b83d']
BKN = ['信', '委', '危', '慰', '庆']
# 一级＝原书目录的大部分；二级＝每个单元（章）
PARTS = [('intro', '📖', '推荐语与导论八章', '#ff7eb6'),
         ('b1', '👑', '第一卷 · 诗篇 1–41 · 信', BKC[0]), ('b2', '🏰', '第二卷 · 诗篇 42–72 · 委', BKC[1]), ('b3', '⚡', '第三卷 · 诗篇 73–89 · 危', BKC[2]),
         ('b4', '🕊️', '第四卷 · 诗篇 90–106 · 慰', BKC[3]), ('b5', '🎉', '第五卷 · 诗篇 107–150 · 庆', BKC[4]),
         ('final', '🎆', '结论：最后五篇', '#ff6b81'), ('back', '📚', '后记与作者简介', '#a9b4c6')]
def part_of_key(seq):
    out = {}; cur = 'intro'
    for k in seq:
        if k in ('b1', 'b2', 'b3', 'b4', 'b5'): cur = k
        elif k == 'c44': cur = 'final'
        elif k in ('post', 'bio'): cur = 'back'
        out[k] = cur
    return out
def unit(x, part, col, ic):
    th, pts, ch, ap = T[x['key']]
    kicker = esc(x['num']) + ('' if x['key'][0] != 'b' or x['key'] == 'bio' else ' · 卷首总论')
    h = (f'<div class="rd-kick"><span class="rd-ic">{ic}</span><span>{kicker}</span></div>')
    body = f'<p class="rd-th"><span class="mk-key">{esc(th)}</span></p>'
    body += '<ol class="rd-pts">' + ''.join(f'<li><b>{i}</b><span>{esc(p)}</span></li>' for i, p in enumerate(pts, 1)) + '</ol>'
    if ch or ap:
        body += '<div class="rd-ca">'
        if ch: body += f'<div class="rd-c"><i>✝️ 指向基督</i><span class="mk-christ">{esc(ch)}</span></div>'
        if ap: body += f'<div class="rd-a"><i>🌱 应用</i><span>{esc(ap)}</span></div>'
        body += '</div>'
    more = ''
    if x['flow']:
        more += '<details class="rd-more"><summary>📖 细读：本章脉络（本站概述）</summary>' + ''.join(f'<p>{esc(p)}</p>' for p in x['flow']) + (f'<p class="rd-refs">📖 相关经文：{esc(x["refs"])}</p>' if x['refs'] else '') + '</details>'
    if x['qs']:
        more += '<details class="rd-more rd-q"><summary>💬 默想与讨论（原书题目 · ' + str(len(x['qs'])) + ' 题）</summary><ol>' + ''.join(f'<li>{esc(q)}</li>' for q in x['qs']) + '</ol></details>'
    return S('r-' + x['key'], ic, esc(x['title']), h + body + more, 'rd-u bk-' + part)
def build():
    seq = [x['key'] for x in U]; po = part_of_key(seq)
    pinfo = {p[0]: p for p in PARTS}
    shell.PAGE_PARTS['psalms-love-read'] = [('阅读说明', '🧭', ('note',), '#a9b4c6')] + [(t, ic, tuple(k for k in seq if po[k] == pid) + (('end',) if pid == 'back' else ()), c) for pid, ic, t, c in PARTS]
    strip = ''.join(f'<span style="--c:{BKC[i]}"><b>{BKN[i]}</b>第{"一二三四五"[i]}卷</span>' for i in range(5))
    hr = hero('📗', '爱上诗篇 · 阅读版', f'按原书目录：{len(U)} 个单元，一章一页卡片',
        '每章只留最该记住的：一句核心、几条短要点、一句指向基督、一句应用；想深入再展开「细读」和原书讨论题。',
        [(f'{len(U)} 单元', '#ff7eb6'), ('五卷 · 信委危慰庆', '#5ab0ff'), ('本站转述', '#3ddc97'), ('← 导读页', '#f5b83d')])
    note = ('<div class="rd-how">'
            '<div><b>① 核心</b><span>金色荧光一句：这一章在说什么</span></div>'
            '<div><b>② 要点</b><span>3–5 条短语，可按编号背</span></div>'
            '<div><b>③ 基督 · 应用</b><span><span class="mk-christ">紫色</span>＝指向基督，绿色＝怎样活出来</span></div>'
            '<div><b>④ 展开</b><span>细读脉络与原书讨论题，默认收起</span></div></div>'
            f'<div class="rd-strip">{strip}</div>' +
            C('note', '出处与版权', f'依{SRC}的目录编排。全部概述、要点、基督与应用都是本站用自己的话写的，不是原书文字；只有「默想与讨论」的题目取自原书，供小组学习。经文用和合本。阅读全文请购买原书。').replace('<div class="call-h">', '<div class="call-h" data-nt="1">', 1) +
            '<p class="rd-nav">👉 <a href="psalms-love.html">图表式导读</a> · <a href="psalms-devotional-read.html">家庭灵修 · 阅读版</a> · <a href="psalms.html">诗篇主页</a></p>')
    m = [S('r-note', '🧭', '怎样读这一页', note)]
    for x in U:
        pid = po[x['key']]; _, ic, _, col = pinfo[pid]
        m.append(unit(x, pid, col, ic))
    m.append(S('r-end', '➡️', '读完了', '<p class="back-l">➡️ <a href="psalms-love.html">爱上诗篇导读</a> · <a href="psalms-devotional-read.html">家庭灵修阅读版</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    return hr, ''.join(m)
