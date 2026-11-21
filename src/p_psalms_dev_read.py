# -*- coding: utf-8 -*-
"""v4.1.0：《家庭灵修·诗篇》阅读版——366 天每天一段本站原创概述（非原文），附题目、经文与钥节。"""
import importlib, re
from lib import *
from shell import S, H3, hero
from p_psalms_dev import D, SRC, BK, kvtxt
from dev_core import CORE
SUM = {}
for _n in range(1, 10): SUM.update(importlib.import_module(f'readdata.dev_s{_n}').S)
def day(n, i, x):
    return (f'<li class="dv"><label class="dchk"><input type="checkbox" data-k="d{n}" aria-label="第 {n} 天已读"><span>{n}</span></label>'
            f'<div class="dv-b"><b>{esc(x["t"])}</b><small>📖 {esc(x["read"])}</small><p class="dv-s">{esc(SUM[i])}</p><div class="dv-k">{kvtxt(x["kv"])}</div></div></li>')
def build():
    assert len(SUM) == len(D) == 366
    idx = list(range(len(D)))
    main = [i for i in idx if D[i]['sec'] == 'main']
    hr = hero('📘', '家庭灵修 · 阅读版', f'366 天每天一段概述：{len(SUM)} / {len(D)} 天全覆盖',
        '每天列出原书题目与经文，加上本站用自己的话写的一段概述（约 100–150 字）和和合本钥节；勾选进度与「家庭灵修」页共用。',
        [('366 天', '#3ddc97'), ('每日概述', '#5ab0ff'), ('进度共用', '#f5b83d'), ('← 篇目页', '#ff7eb6')])
    m = [S('dr-note', '📝', '阅读说明', C('note', '出处与版权', f'题目与经文整理自{SRC}；每日概述为本站原创转述，不是原文，个别短语为和合本经文。请购买原书阅读全文。') +
           '<div class="dprog"><span>✅ 已读 <b id="dcount">0</b> / 366 天</span><i><b id="dbar"></b></i></div>' +
           '<p>👉 <a href="psalms-devotional.html">篇目与进度页</a> · <a href="psalms-love-read.html">爱上诗篇 · 阅读版</a> · <a href="psalms.html">诗篇主页</a></p>')]
    n = 0
    for k, a, b, col, ic in BK:
        body = ''
        for g0 in range(a, b + 1, 10):
            g1 = min(g0 + 9, b); blk = ''
            for p in range(g0, g1 + 1):
                ds = [i for i in main if int(re.match(r'\d+', D[i]['ps']).group()) == p]
                items = ''
                for i in ds: n += 1; items += day(n, i, D[i])
                blk += f'<div class="dps" style="--c:{col}"><div class="dps-h"><span class="dps-n">{p}</span><span class="dps-c">{CORE[p]}</span></div><ol class="dvl">{items}</ol></div>'
            body += H3(f'dr-b{k}-{g0}', f'🎵 诗篇 {g0}–{g1}', blk)
        m.append(S(f'dr-b{k}', ic, f'第{"一二三四五"[k-1]}卷 · 诗篇 {a}–{b}', body))
    for sec, ic, title in (('a1', '✝️', '附录一 · 基督传道生涯中的重大事件'), ('a2', '📅', '附录二 · 节令、节日篇'), ('a3', '🍞', '附录三 · 圣餐篇')):
        items = ''
        for i in idx:
            if D[i]['sec'] == sec: n += 1; items += day(n, i, D[i])
        m.append(S('dr-' + sec, ic, title, f'<ol class="dvl dapp">{items}</ol>'))
    assert n == 366
    m.append(S('dr-end', '➡️', '继续', '<p class="back-l">➡️ <a href="psalms-devotional.html">家庭灵修篇目页</a> · <a href="psalms-love-read.html">爱上诗篇阅读版</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    return hr, ''.join(m)
