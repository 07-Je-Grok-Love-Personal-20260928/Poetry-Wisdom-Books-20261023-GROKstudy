# -*- coding: utf-8 -*-
"""v4.0.0：《家庭灵修·诗篇》（Peter H. Holtvlüwer）366 天灵修计划——每篇一句核心（本站概括）+ 每天的题目、经文与对读经文（原书）。"""
import json, os, re
from lib import *
from shell import S, H3, hero
from dev_core import CORE
from v3content import bars
D = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'devotional_index.json')))
SRC = '《家庭灵修·诗篇》（Peter H. Holtvlüwer 著，中文版 2018）'
BK = [(1, 1, 41, '#3ddc97', '👑'), (2, 42, 72, '#5ab0ff', '🏰'), (3, 73, 89, '#ff9f43', '⚡'), (4, 90, 106, '#b48cff', '🕊️'), (5, 107, 150, '#f5b83d', '🎉')]
def kvtxt(kv):
    if not kv: return ''
    ch, sec = kv
    sec = re.split(r'[,]', sec)[0]
    try: return VI('诗', int(ch), sec)
    except Exception: return f'<span class="vref">（诗{ch}:{sec}）</span>'
def day(i, x):
    rd = esc(x['read'])
    return (f'<li class="dv"><label class="dchk"><input type="checkbox" data-k="d{i}" aria-label="第 {i} 天已读"><span>{i}</span></label>'
            f'<div class="dv-b"><b>{esc(x["t"])}</b><small>📖 {rd}</small><div class="dv-k">{kvtxt(x["kv"])}</div></div></li>')
def build():
    main = [x for x in D if x['sec'] == 'main']; a1 = [x for x in D if x['sec'] == 'a1']; a2 = [x for x in D if x['sec'] == 'a2']; a3 = [x for x in D if x['sec'] == 'a3']
    hr = hero('🏡', '家庭灵修 · 诗篇', 'Peter H. Holtvlüwer《家庭灵修·诗篇》366 天全部篇目',
        '150 篇诗篇每篇两天（共 310 天），另有三组附录：基督生平 37 天、节令节日 15 天、圣餐 4 天。每篇配本站一句话核心，每天列出原书题目、经文与对读经文，可勾选「已读」。',
        [('366 天', '#3ddc97'), ('每篇两课', '#5ab0ff'), ('勾选进度自动保存', '#f5b83d'), ('← 返回诗篇', '#ff7eb6')])
    m = []
    m.append(S('d-core', '💎', '本质核心：怎样用这本灵修书',
        '<p class="thesis">💎 一家人每天一段诗篇、一个题目、一节钥节：<b>读 → 想 → 问 → 祷</b>，把诗篇变成家庭的祷告本。</p>' +
        facts([('书名', '《家庭灵修·诗篇》'), ('作者', 'Peter H. Holtvlüwer（加拿大归正教会牧师）'), ('版本', '中文版 2018（原 PDF 带水印，本站只整理篇目与要点）'),
               ('结构', f'诗篇 1–150：{len(main)} 天（每篇 2 天；诗119 为 11 天，诗139 为 3 天）；附录一 基督传道生涯 {len(a1)} 天；附录二 节令节日 {len(a2)} 天；附录三 圣餐 {len(a3)} 天'),
               ('共计', f'{len(D)} 天，一年一轮')]) +
        flow([('📖', '读', '读当天经文（含对读的新约经文）', '#5ab0ff'), ('💡', '想', '抓住题目与钥节（本页已列出）', '#f5b83d'), ('❓', '问', '问孩子：这里怎样指向基督？', '#b48cff'), ('🙏', '祷', '用这篇诗的话一起祷告', '#3ddc97')]) +
        bars('各部分天数', [('第一卷 1–41', sum(1 for x in main if int(re.match(r"\d+", x["ps"]).group()) <= 41), '#3ddc97', ''), ('第二卷 42–72', sum(1 for x in main if 42 <= int(re.match(r"\d+", x["ps"]).group()) <= 72), '#5ab0ff', ''),
                            ('第三卷 73–89', sum(1 for x in main if 73 <= int(re.match(r"\d+", x["ps"]).group()) <= 89), '#ff9f43', ''), ('第四卷 90–106', sum(1 for x in main if 90 <= int(re.match(r"\d+", x["ps"]).group()) <= 106), '#b48cff', ''),
                            ('第五卷 107–150', sum(1 for x in main if int(re.match(r"\d+", x["ps"]).group()) >= 107), '#f5b83d', ''), ('附录（基督·节令·圣餐）', len(a1) + len(a2) + len(a3), '#ff7eb6', '')], ' 天') +
        '<div class="dprog"><span>✅ 已读 <b id="dcount">0</b> / ' + str(len(D)) + ' 天</span><i><b id="dbar"></b></i></div>' +
        C('note', '出处与本页做法', f'篇目、经文和对读经文整理自{SRC}；每篇的「核心」一句是本站的概括。钥节文字用和合本显示（原书中文译文与和合本略有差异）。'), 'key'))
    n = 0
    for k, a, b, col, ic in BK:
        cn = '一二三四五'[k-1]; body = ''
        for g0 in range(a, b + 1, 10):
            g1 = min(g0 + 9, b); blk = ''
            for p in range(g0, g1 + 1):
                ds = [x for x in main if int(re.match(r'\d+', x['ps']).group()) == p]
                items = ''
                for x in ds:
                    n += 1; items += day(n, x)
                blk += f'<div class="dps" style="--c:{col}"><div class="dps-h"><span class="dps-n">{p}</span><span class="dps-c">{CORE[p]}</span></div><ol class="dvl">{items}</ol></div>'
            body += H3(f'd-b{k}-{g0}', f'🎵 诗篇 {g0}–{g1}', f'<div class="dgrid">{blk}</div>')
        m.append(S(f'd-b{k}', ic, f'第{cn}卷 · 诗篇 {a}–{b}', body))
    def app_list(xs, start):
        return '<ol class="dvl dapp">' + ''.join(day(start + i, x) for i, x in enumerate(xs)) + '</ol>'
    st = n
    tl = timeline([(f'第 {st + i + 1} 天', esc(x['t']), '📖 ' + esc(x['read']), '#b48cff', '') for i, x in enumerate(a1)])
    m.append(S('d-a1', '✝️', '附录一 · 基督传道生涯中的重大事件（诗篇里的基督）',
        '<p>从降生、受洗、受试探、传道、受难、复活、升天到五旬节和再来：每一天用一篇诗篇对照福音书中的一件大事——这是「诗篇满有基督」最直观的证明。</p>' +
        '<details class="gq" open><summary>🧭 时间线视图</summary>' + tl + '</details>' + app_list(a1, st)))
    st += len(a1)
    m.append(S('d-a2', '📅', '附录二 · 节令、节日篇', '<p>创造、劳动、安息、收成、感恩、新年、国庆等时节的诗篇灵修。</p>' + app_list(a2, st)))
    st += len(a2)
    m.append(S('d-a3', '🍞', '附录三 · 圣餐篇', '<p>领圣餐前的自省与感恩（参 HC 75–82；BC 35）。</p>' + app_list(a3, st)))
    m.append(S('d-notes', '📜', '改革宗信条对照与评注',
        C('key', '与信条一致', '作者是加拿大归正教会（Canadian Reformed Churches）牧师，全书以圣约、基督中心、认罪悔改与感恩为主线，与三项联合信条一致（参 HC 1、86；BC 22–24）。') +
        C('view', '守护天使（诗91:11）', '原书第 91 篇的题目谈到天使的保护。圣经确认神差遣天使服事承受救恩的人（来1:14；BC 12）；至于「每人各有一位守护天使」，加尔文认为圣经没有确定的教导（《基督教要义》1.14.7），宜存而不论。') +
        C('hard', '咒诅诗（诗35、58、69、109、137、139:22）', '原书把这些诗理解为把伸冤交给神、恨恶罪恶。信徒不可存私人报复的心（HC 105–107；罗12:19），而要为仇敌祷告。') +
        C('view', '节令篇', '附录二按家庭与社会生活的时节安排灵修（如新年、收成、感恩），这是灵修的时机，不是圣经规定的节期；信徒的圣日是主日（HC 103）。')))
    m.append(S('d-mem', '🧠', '速记：家庭灵修的一年',
        cards_flip([('一年怎么排', '1–150 篇各两天（诗119 十一天、诗139 三天）＋ 基督 37 ＋ 节令 15 ＋ 圣餐 4 ＝ 366'), ('每天四步', '读 · 想 · 问 · 祷'), ('第一天', '诗1：有福的人'), ('最后一篇', '诗150：凡有气息的都要赞美耶和华'),
                    ('附录一主线', '诗篇中的基督：降生 → 受难 → 复活 → 升天 → 五旬节 → 再来')]) +
        '<p class="back-l">➡️ 继续：<a href="psalms-love.html">爱上诗篇 · 戈弗雷导读</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    return hr, ''.join(m)
