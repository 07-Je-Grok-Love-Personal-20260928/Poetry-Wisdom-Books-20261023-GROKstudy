# -*- coding: utf-8 -*-
"""v4.3.0：加「导览与图解」（统计、366 天日历热图、每卷天数与节数、长度散点、月份主题热图、附录流程、附录选用诗篇地图、53 周一览、延伸经文统计）、每部分信息头、每天「延伸经文」。v4.2.0：《家庭灵修·诗篇》阅读版——366 天卡片：题目、经文、一句核心（≤60 字，本站原创转述），展开看和合本钥节与较长的概述。按原书目录：五卷（每篇诗一组）＋ 三个附录（按周分组）。"""
import importlib, re, os, json
from lib import *
import shell
from shell import S, H3, hero
from p_psalms_dev import D, SRC, BK, kvtxt
from dev_core import CORE
from readdata.dev_core2 import K
import viz_dev as VDZ
SUM = {}
for _n in range(1, 10): SUM.update(importlib.import_module(f'readdata.dev_s{_n}').S)
CN = '一二三四五'
def card(n, i, x):
    return (f'<div class="dc" id="day-{n}"><label class="dchk"><input type="checkbox" data-k="d{n}" aria-label="第 {n} 天已读"><span>{n}</span></label>'
            f'<details><summary><b class="dc-t">{esc(x["t"])}</b><small class="dc-r">📖 {esc(x["read"])}</small><span class="dc-k">{esc(K[i])}</span></summary>'
            f'<div class="dc-x" data-i="{i}"></div></details></div>')
def extra(i, x):
    xr = VDZ.X.get(i, [])
    xs = (f'<p class="rd-x"><b>📚 延伸经文（{len(xr)}）</b> ' + ''.join(f'<span>{esc(r)}</span>' for r in xr) + '</p>') if xr else ''
    return f'<div class="dv-k">{kvtxt(x["kv"])}</div><p>{esc(SUM[i])}</p>{xs}'
def build():
    assert len(K) == len(SUM) == len(D) == 366
    idx = list(range(len(D))); main = [i for i in idx if D[i]['sec'] == 'main']
    st = VDZ.compute(D, K, SUM); vz = VDZ.sections(D, K, SUM, st)
    VIZ = [('stat', '🔢', '数字一览：366 天怎样分配'), ('cal', '📅', '366 天日历热图'), ('book', '📊', '每卷天数与节数'), ('len', '🔵', '诗篇长度与天数'),
           ('month', '🗓️', '主题随月份变化'), ('flow', '🧭', '三个附录：流程与选篇'), ('week', '🗂️', '53 周一览'), ('xref', '📚', '延伸经文统计')]
    parts = [('导览与图解', '📊', ('note',) + tuple('v' + k for k, _, _ in VIZ), '#2fd3d3',
              '<div class="part-x"><span class="px-ic" aria-hidden="true">📊</span><p class="px-core">先用 8 组图看清一年的路线、节奏与主题，再按天读卡片。</p><div class="px-tags"><span>12 张图表</span><span>数字均由本站数据计算</span><span>日历与勾选同步</span></div></div>')]
    hr = hero('📘', '家庭灵修 · 阅读版', '366 天，一天一张卡片',
        '每张卡片：题目、经文和一句核心（不超过 60 字）；点开看和合本钥节与较长的概述。勾选进度与「家庭灵修」篇目页共用。',
        [('366 天', '#3ddc97'), ('一句核心', '#5ab0ff'), ('点开看钥节', '#f5b83d'), ('← 篇目页', '#ff7eb6')])
    strip = ''.join(f'<span style="--c:{c}"><b>{CN[k-1]}</b>诗{a}–{b}</span>' for k, a, b, c, ic in BK)
    note = ('<div class="rd-how"><div><b>① 看卡片</b><span>题目 · 经文 · 一句核心</span></div><div><b>② 点开</b><span>和合本钥节、较长的概述与延伸经文</span></div>'
            '<div><b>③ 勾选</b><span>左上角数字＝第几天，勾上即记进度；日历热图同步变色</span></div><div><b>④ 图解</b><span>下面 8 组图先看一年全貌</span></div></div>'
            f'<div class="rd-strip">{strip}<span style="--c:#ff7eb6"><b>附</b>基督 · 节令 · 圣餐</span></div>'
            '<div class="dprog"><span>✅ 已读 <b id="dcount">0</b> / 366 天</span><i><b id="dbar"></b></i></div>' +
            C('note', '出处与版权', f'题目与经文依{SRC}的目录。每天的核心与概述都是本站用自己的话写的，不是原书文字；钥节用和合本。阅读全文请购买原书。').replace('<div class="call-h">', '<div class="call-h" data-nt="1">', 1) +
            '<p class="rd-nav">👉 <a href="psalms-devotional.html">篇目与进度页</a> · <a href="psalms-love-read.html">爱上诗篇 · 阅读版</a> · <a href="psalms.html">诗篇主页</a></p>')
    m = [S('dr-note', '🧭', '怎样用这一页', note)]
    for k, ic, t in VIZ:
        m.append(S('dr-v' + k, ic, t, vz[k], 'rd-viz'))
    n = 0
    for k, a, b, col, ic in BK:
        sfx = []
        for g0 in range(a, b + 1, 10):
            g1 = min(g0 + 9, b); body = ''
            for p in range(g0, g1 + 1):
                ds = [i for i in main if int(re.match(r'\d+', D[i]['ps']).group()) == p]
                cards = ''
                for i in ds: n += 1; cards += card(n, i, D[i])
                body += H3(f'dr-p{p}', f'诗篇 {p}', f'<p class="dc-ps">{CORE[p]}</p><div class="dcg">{cards}</div>')
            sid = f'dr-b{k}x{g0}'; sfx.append(sid.split('-', 1)[1])
            m.append(S(sid, ic, f'诗篇 {g0}–{g1}', body, f'rd-g bk-b{k}'))
        parts.append((f'第{CN[k-1]}卷 · 诗篇 {a}–{b}', ic, tuple(sfx), col, VDZ.part_header(f'b{k}', D, st)))
    for sec, ic, title, col in (('a1', '✝️', '附录一 · 基督传道生涯中的重大事件', '#ff7eb6'), ('a2', '📅', '附录二 · 节令、节日篇', '#2fd3d3'), ('a3', '🍞', '附录三 · 圣餐篇', '#ff9f43')):
        ids = [i for i in idx if D[i]['sec'] == sec]; body = ''
        for w0 in range(0, len(ids), 7):
            cards = ''
            for i in ids[w0:w0 + 7]: n += 1; cards += card(n, i, D[i])
            body += H3(f'dr-{sec}w{w0 // 7 + 1}', f'第 {n - len(ids[w0:w0 + 7]) + 1}–{n} 天', f'<div class="dcg">{cards}</div>')
        m.append(S('dr-' + sec, ic, title, body, 'rd-g bk-' + sec))
        parts.append((title.split(' · ')[0] + ' · ' + title.split(' · ')[1], ic, (sec,) + (('end',) if sec == 'a3' else ()), col, VDZ.part_header(sec, D, st)))
    assert n == 366
    m.append(S('dr-end', '➡️', '继续', '<p class="back-l">➡️ <a href="psalms-devotional.html">家庭灵修篇目页</a> · <a href="psalms-love-read.html">爱上诗篇阅读版</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    shell.PAGE_PARTS['psalms-devotional-read'] = parts
    out = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets'); os.makedirs(out, exist_ok=True)
    json.dump([extra(i, D[i]) for i in idx], open(os.path.join(out, 'devread.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    return hr, ''.join(m)
