# -*- coding: utf-8 -*-
"""v4.1.0：《爱上诗篇》阅读版——按原书目录 52 个单元逐一概述（本站原创转述，注明原书页码；讨论题为原书题目）。"""
import sys, os
from lib import *
from shell import S, H3, hero
import readdata.god_a as GA
for _n in 'bcdefgh': __import__('readdata.god_' + _n)
U = GA.U
SRC = '《爱上诗篇》（W. Robert Godfrey 著，中文版）'
def Cq(kind, title, body):
    """同 C()，但提示框标题不进目录（阅读版目录只列单元）"""
    return C(kind, title, body).replace('<div class="call-h">', '<div class="call-h" data-nt="1">', 1)
def unit(x):
    b = f'<p class="pref">📄 原书第 {esc(x["pages"])} 页 · {esc(x["num"])}</p>'
    b += ''.join(f'<p>{esc(p)}</p>' for p in x['flow'])
    if x['points']: b += Cq('key', '要点', '<ul>' + ''.join(f'<li>{esc(p)}</li>' for p in x['points']) + '</ul>')
    if x['refs']: b += f'<p class="src-n">📖 相关经文：{esc(x["refs"])}</p>'
    if x['christ']: b += Cq('christ', '指向基督', esc(x['christ']))
    if x['app']: b += Cq('app', '应用', esc(x['app']))
    if x['quote']: b += f'<blockquote>“{esc(x["quote"][0])}”<small>（原书第 {esc(x["quote"][1])} 页）</small></blockquote>'
    if x['qs']: b += ('<details class="gq"><summary>💬 默想与讨论（原书题目，' + str(len(x['qs'])) + ' 题）</summary><ol>' + ''.join(f'<li>{esc(q)}</li>' for q in x['qs']) + '</ol></details>')
    return H3('u-' + x['key'], f'{esc(x["num"])} · {esc(x["title"])}', b)
GROUPS = [('intro', '📖', '前页与导论八章', lambda k: k == 'front' or (k[0] == 'c' and k[1:].isdigit() and int(k[1:]) <= 8)),
          ('b1', '👑', '第一卷', None), ('b2', '🏰', '第二卷', None), ('b3', '⚡', '第三卷', None), ('b4', '🕊️', '第四卷', None), ('b5', '🎉', '第五卷', None),
          ('final', '🎆', '结论：最后五篇', lambda k: k == 'c44' or k in ('p146', 'p147', 'p148', 'p149', 'p150')),
          ('back', '📚', '后记与作者简介', lambda k: k in ('post', 'bio'))]
def build():
    hr = hero('📗', '爱上诗篇 · 阅读版', f'按原书目录逐单元概述：{len(U)} / {len(U)} 个单元全覆盖',
        '每个单元都是本站用自己的话写的概述，注明原书页码，并附要点、相关经文、指向基督、应用与原书讨论题。想看图表式导读请回到「爱上诗篇」导读页。',
        [(f'{len(U)} 单元', '#ff7eb6'), ('注明页码', '#5ab0ff'), ('本站转述', '#3ddc97'), ('← 导读页', '#f5b83d')])
    m = [S('r-note', '📝', '阅读说明', Cq('note', '出处与版权', f'内容概述自{SRC}；正文为本站原创转述，不是原文；页码为原书印刷页码；讨论题取自原书章末，供小组使用。经文用和合本。请购买原书阅读全文。') +
           '<p>👉 <a href="psalms-love.html">图表式导读</a> · <a href="psalms-devotional-read.html">家庭灵修 · 阅读版</a> · <a href="psalms.html">诗篇主页</a></p>')]
    seq = [x['key'] for x in U]; used = set()
    for gid, ic, title, pred in GROUPS:
        if pred: keys = [k for k in seq if pred(k)]
        else:
            i = seq.index(gid); keys = [gid]
            for k in seq[i + 1:]:
                if k[0] == 'b' or k == 'c44': break
                keys.append(k)
        used |= set(keys)
        xs = [x for x in U if x['key'] in keys]
        head = xs[0]['title'] if not pred else ''
        m.append(S('r-' + gid, ic, title + (f' · {esc(head)}' if head else ''), ''.join(unit(x) for x in xs)))
    assert used == set(seq), set(seq) - used
    m.append(S('r-end', '➡️', '继续', '<p class="back-l">➡️ <a href="psalms-love.html">爱上诗篇导读</a> · <a href="psalms-devotional-read.html">家庭灵修阅读版</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    return hr, ''.join(m)
