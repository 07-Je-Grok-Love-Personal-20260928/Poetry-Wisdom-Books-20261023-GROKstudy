# -*- coding: utf-8 -*-
"""v4.3.0：《家庭灵修·诗篇》阅读版 / 篇目页的图解。全部由 data/devotional_index.json、devotional_xrefs.json、和合本诗篇全文与本站概述计算。"""
import re, json, os, collections
from lib import esc
import viz43 as V
from viz43 import fig, tbl, stats, hbars, donut, psalter, heat, scatter, BOOKS, BKN, BKW, VERSES, book_of, BC
ROOT = os.path.join(os.path.dirname(__file__), '..')
X = {int(k): v for k, v in json.load(open(os.path.join(ROOT, 'data', 'devotional_xrefs.json'))).items()}
SECC = {'a1': '#ff7eb6', 'a2': '#2fd3d3', 'a3': '#9be564'}
SECN = {'a1': '附录一 · 基督', 'a2': '附录二 · 节令', 'a3': '附录三 · 圣餐'}
OT = ['创', '出', '利', '民', '申', '书', '士', '得', '撒上', '撒下', '王上', '王下', '代上', '代下', '拉', '尼', '斯', '伯', '诗', '箴', '传', '歌', '赛', '耶', '哀', '结', '但', '何', '珥', '摩', '俄', '拿', '弥', '鸿', '哈', '番', '该', '亚', '玛']
OTFULL = dict(创='创世记', 出='出埃及记', 利='利未记', 民='民数记', 申='申命记', 书='约书亚记', 士='士师记', 撒上='撒上', 撒下='撒下', 王上='王上', 王下='王下', 代上='代上', 代下='代下', 尼='尼希米记', 伯='约伯记', 箴='箴言', 传='传道书', 赛='以赛亚书', 耶='耶利米书', 哀='哀歌', 结='以西结书', 但='但以理书', 何='何西阿书', 珥='约珥书', 摩='阿摩司书', 拿='约拿书', 弥='弥迦书', 哈='哈巴谷书', 亚='撒迦利亚书', 玛='玛拉基书')
THEMES = [('信靠', r'信靠|倚靠|投靠|避难所|信心'), ('赞美感恩', r'赞美|称颂|颂赞|感谢|感恩|称谢|欢呼'), ('祷告', r'祷告|呼求|祈求|求告'), ('罪与悔改', r'罪|悔改|认罪|赦免|过犯'),
          ('苦难', r'苦难|患难|仇敌|痛苦|忧伤|眼泪|受苦'), ('神的话', r'律法|神的话|话语|典章|训词|圣经'), ('基督', r'基督|耶稣|弥赛亚|十字架'), ('家庭', r'家|儿女|孩子|父母|世代|子孙')]
# 附录一：按基督生平分段（依本页附录一各天题目与经文整理）
A1 = [('降生', 310, 316), ('进城', 317, 317), ('受难', 318, 324), ('复活', 325, 332), ('升天与坐宝座', 333, 338), ('再来', 339, 339), ('五旬节与圣灵', 340, 346)]
def bookbook(ref):
    m = re.match(r'(撒上|撒下|王上|王下|代上|代下|林前|林后|帖前|帖后|提前|提后|彼前|彼后|约壹|约贰|约叁|[\u4e00-\u9fff])', ref)
    return m.group(1) if m else ''
def order(D):
    main = [i for i in range(len(D)) if D[i]['sec'] == 'main']
    o = []
    for k, a, b in BOOKS:
        for p in range(a, b + 1): o += [i for i in main if int(re.match(r'\d+', D[i]['ps']).group()) == p]
    for s in ('a1', 'a2', 'a3'): o += [i for i in range(len(D)) if D[i]['sec'] == s]
    return o
def psal(x):
    return int(re.match(r'\d+', x['ps']).group()) if x['ps'] else x['kv'][0]
def color(x):
    return BC[book_of(psal(x)) - 1] if x['sec'] == 'main' else SECC[x['sec']]
def compute(D, K, SUM):
    st = {}; O = order(D); st['order'] = O
    st['sec'] = collections.Counter(x['sec'] for x in D)
    main = [x for x in D if x['sec'] == 'main']
    st['days_book'] = collections.Counter(book_of(psal(x)) for x in main)
    st['dpp'] = collections.Counter(psal(x) for x in main)
    st['verses_book'] = {k: sum(VERSES[p] for p in range(a, b + 1)) for k, a, b in BOOKS}
    st['app_ps'] = collections.defaultdict(list)
    for i, x in enumerate(D):
        if x['sec'] != 'main': st['app_ps'][x['kv'][0]].append((i, x['sec'], x['t']))
    co = [i for i, x in enumerate(D) if re.search(r'[；（(]', x['read'])]
    st['co'] = len(co)
    st['co_nt'] = sum(1 for i in co if V.NTRE.search(D[i]['read'].replace(' ', '').replace('：', ':')) or re.search(r'[；（(]\s*(约壹|林前|林后|帖前|帖后|提前|提后|彼前|彼后|太|可|路|约|徒|罗|加|弗|腓|西|多|门|来|雅|犹|启)\s*\d', D[i]['read']))
    xb = collections.Counter(); nt = ot = 0
    for i, refs in X.items():
        for r in refs:
            b = bookbook(r); xb[b] += 1
            if b in OT: ot += 1
            else: nt += 1
    st['xb'] = xb; st['x_nt'] = nt; st['x_ot'] = ot; st['x_total'] = nt + ot; st['x_days'] = sum(1 for v in X.values() if v)
    txt = {i: D[i]['t'] + ' ' + K[i] + ' ' + SUM[i] for i in range(len(D))}
    st['txt'] = txt
    return st
MON = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def part_header(key, D, st):
    if key[0] == 'b':
        k = int(key[1]); a, b = BOOKS[k - 1][1:]; d = st['days_book'][k]; v = st['verses_book'][k]
        longest = max(range(a, b + 1), key=lambda p: VERSES[p])
        idx = [i for i in st['order'] if D[i]['sec'] == 'main' and book_of(psal(D[i])) == k]; xr = sum(len(X.get(i, [])) for i in idx)
        core = {1: '从「有福的人」起步：在敌人环伺中学信靠、认罪与赞美。', 2: '渴慕神的同在，委身于神的城与国，也学会真实悔改。', 3: '面对恶人亨通与圣殿被毁，仍向立约的神呼求。',
                4: '王位动摇时，神自己作王：数算日子，称颂他的恩惠。', 5: '归回与庆祝：感恩、上行之诗、律法之美，直到哈利路亚。'}[k]
        tags = [f'{d} 天', f'{b - a + 1} 篇 · {v} 节', f'平均每天 {v / d:.1f} 节', f'最长：诗{longest}（{VERSES[longest]} 节）', f'延伸经文 {xr} 处']
        ic = ['🌱', '🏛️', '🌩️', '🕯️', '🎺'][k - 1]
    else:
        idx = [i for i in st['order'] if D[i]['sec'] == key]; xr = sum(len(X.get(i, [])) for i in idx)
        ps = sorted({D[i]['kv'][0] for i in idx})
        core = {'a1': '跟着基督的一生读诗篇：降生、受难、复活、升天、再来与圣灵。', 'a2': '为一年里的节令与日常：工作、安睡、收成、感恩、新年。', 'a3': '圣餐前后的预备：省察、品尝主恩、认罪、称颂。'}[key]
        tags = [f'{len(idx)} 天', f'选用 {len(ps)} 篇诗篇', f'延伸经文 {xr} 处']
        ic = {'a1': '✝️', 'a2': '📅', 'a3': '🍞'}[key]
    return (f'<div class="part-x"><span class="px-ic" aria-hidden="true">{ic}</span><p class="px-core">{esc(core)}</p><div class="px-tags">' + ''.join(f'<span>{t}</span>' for t in tags) + '</div></div>')
def calendar(D, st, href='#day-{n}', vid='vz-cal'):
    cells = ''
    for n, i in enumerate(st['order'], 1):
        x = D[i]; lab = f'第 {n} 天 · {x["read"]} · {x["t"]}'
        cc = f'k{book_of(psal(x))}' if x['sec'] == 'main' else x['sec']
        cells += f'<a href="{href.format(n=n)}" data-k="d{n}" class="{cc}" title="{esc(lab)}"></a>'
    leg = ''.join(f'<li><i style="--c:{BC[k - 1]}"></i>卷{BKN[k - 1]}</li>' for k in range(1, 6)) + ''.join(f'<li><i style="--c:{c}"></i>{SECN[s]}</li>' for s, c in SECC.items())
    inner = (f'<div class="vz-cal" role="group" aria-label="366 天阅读日历：每格一天，颜色＝所属卷或附录，实心＝已勾选">{cells}</div><ul class="vz-leg row">{leg}</ul>'
             f'<div class="cal-sum"><span>✅ 已读 <b class="cal-done">0</b> / 366 天</span><span>每列一周（手机上每列三周），自左向右</span><span>点任一格跳到那一天</span></div>')
    rows = []; O = st['order']
    for k, a, b in BOOKS:
        ns = [n for n, i in enumerate(O, 1) if D[i]['sec'] == 'main' and book_of(psal(D[i])) == k]; rows.append((f'卷{BKN[k - 1]}（诗{a}–{b}）', len(ns), f'{ns[0]}–{ns[-1]}'))
    for sc in SECC:
        ns = [n for n, i in enumerate(O, 1) if D[i]['sec'] == sc]; rows.append((SECN[sc], len(ns), f'{ns[0]}–{ns[-1]}'))
    return fig(vid, '📅 366 天阅读日历热图（与勾选进度同步）', inner, tbl(['部分', '天数', '日次'], rows),
               '勾选进度保存在本机浏览器，与「家庭灵修」篇目页共用；勾上或取消后，这张图会即时更新。', 'vz-calf')
def sections(D, K, SUM, st):
    out = {}
    s = st['sec']; vb = st['verses_book']; db = st['days_book']
    tv = sum(vb.values())
    out['stat'] = (stats([(366, '天', '一年（含闰日）', '#3ddc97'), (150, '篇诗篇', '全部读完', '#5ab0ff'), (s['main'], '天按卷顺读', '五卷', '#f5b83d'),
                          (s['a1'] + s['a2'] + s['a3'], '天附录', f'基督 {s["a1"]} · 节令 {s["a2"]} · 圣餐 {s["a3"]}', '#ff7eb6'), (tv, '节经文', '和合本诗篇总节数', '#b48cff'),
                          (st['co'], '天另配经文', f'其中新约 {st["co_nt"]} 天', '#2fd3d3'), (st['x_total'], '处延伸经文', f'分布在 {st["x_days"]} 天的概述里', '#ff9f43'),
                          (st['dpp'][119], '天读诗119', '最长的一篇', '#ff6b81')]) +
                   donut('vz-dsec', '🍩 366 天怎样分配', [(f'卷{BKN[k - 1]} · {BKW[k - 1]}', db[k], BC[k - 1]) for k in range(1, 6)] + [(SECN[x], s[x], c) for x, c in SECC.items()], (366, '天'),
                         '按本页卡片计数：五卷顺读 310 天，三个附录 56 天。'))
    out['cal'] = calendar(D, st)
    out['book'] = (hbars('vz-dbk', '📊 每卷读几天', [(f'卷{BKN[k - 1]}（诗{a}–{b}）', db[k], BC[k - 1], '') for k, a, b in BOOKS], ' 天') +
                   hbars('vz-dvd', '📏 每卷平均每天读几节（和合本节数 ÷ 天数）', [(f'卷{BKN[k - 1]}', round(vb[k] / db[k], 1), BC[k - 1], '') for k, a, b in BOOKS], ' 节',
                         f'卷五最长（{vb[5]} 节，含诗119 的 176 节），所以平均每天读得最多。'))
    pts = [(VERSES[p], st['dpp'][p], BC[book_of(p) - 1], f'诗{p}：{VERSES[p]} 节，{st["dpp"][p]} 天') for p in range(1, 151)]
    odd = sorted((p for p in range(1, 151) if st['dpp'][p] != 2), key=lambda p: -st['dpp'][p])
    out['len'] = scatter('vz-len', '🔵 诗篇长度 vs 读几天（150 篇，每点一篇）', pts, '经节数（平方根刻度）', '天数',
                         '几乎每篇都分两天读；例外：' + '、'.join(f'诗{p} {st["dpp"][p]} 天（{VERSES[p]} 节）' for p in odd) + '。长诗不一定多读，短诗也读两天——重在慢嚼。',
                         tbl(['天数', '篇数', '诗篇（节数）'], [(d, len(ps), '、'.join(f'诗{p}（{VERSES[p]}）' for p in ps) if len(ps) < 10 else f'其余 {len(ps)} 篇；最短 诗{min(ps, key=lambda p: VERSES[p])}（{min(VERSES[p] for p in ps)} 节），最长 诗{max(ps, key=lambda p: VERSES[p])}（{max(VERSES[p] for p in ps)} 节）')
                                                    for d, ps in sorted(((d, [p for p in range(1, 151) if st['dpp'][p] == d]) for d in set(st['dpp'].values())), key=lambda x: -x[0])]))
    O = st['order']; segs = []; c = 0
    for m in MON: segs.append(O[c:c + m]); c += m
    cols = [t for t, _ in THEMES]
    M = [[sum(len(re.findall(pat, st['txt'][i])) for i in seg) for _, pat in THEMES] for seg in segs]
    fa = O.index(next(i for i in O if D[i]['sec'] == 'a1')) + 1; cm = 0
    for mi, m in enumerate(MON):
        if fa <= cm + m: fm, fd = mi + 1, fa - cm; break
        cm += m
    jc = cols.index('基督'); top = max(range(12), key=lambda r: M[r][jc])
    hot = [max(range(12), key=lambda r: M[r][j]) + 1 for j in range(len(cols))]
    out['month'] = heat('vz-month', '🗓️ 主题随月份的变化（若从 1 月 1 日开读）', [f'{k + 1} 月' for k in range(12)], cols, M,
                        f'按每天的题目、本站核心句与概述中的关键词计数；颜色越深越集中。第 {fa} 天（{fm} 月 {fd} 日）起进入三个附录；「基督」一栏最深的是 {top + 1} 月。'
                        '各主题最集中的月份：' + '、'.join(f'{c} {h} 月' for c, h in zip(cols, hot)) + '。')
    a1 = ''.join(f'<a href="#day-{a + 1}" style="--c:#ff7eb6"><span>{b - a + 1} 天</span><b>{t}</b><small>第 {a + 1}{"–" + str(b + 1) if b > a else ""} 天</small></a>' for t, a, b in A1)
    def chips(sec):
        ids = [i for i in O if D[i]['sec'] == sec]
        return ''.join(f'<a href="#day-{O.index(i) + 1}" style="--c:{SECC[sec]}"><b>{esc(D[i]["t"])}</b><small>第 {O.index(i) + 1} 天 · 诗{D[i]["kv"][0]}</small></a>' for i in ids)
    flow = (f'<h4 class="vz-h4">✝️ 附录一：基督的一生（{s["a1"]} 天）</h4><div class="vz-flow">{a1}</div>'
            f'<h4 class="vz-h4">📅 附录二：节令与日常（{s["a2"]} 天）</h4><div class="vz-flow sm">{chips("a2")}</div>'
            f'<h4 class="vz-h4">🍞 附录三：圣餐（{s["a3"]} 天）</h4><div class="vz-flow sm">{chips("a3")}</div>')
    out['flow'] = (fig('vz-flow', '🧭 三个附录的流程', flow, tbl(['阶段', '天数', '日次'], [(t, b - a + 1, f'{a + 1}–{b + 1}') for t, a, b in A1]),
                       '附录一按基督生平分段（依各天题目整理）；点任一格跳到那一天。') +
                   psalter('vz-aps', f'🗺️ 附录选用了哪些诗篇（{len(st["app_ps"])} 篇）', {p: '；'.join(f'{SECN[sec].split(" · ")[1]}：{t}' for _, sec, t in v) for p, v in st['app_ps'].items()},
                           '亮色＝附录里有一天以这篇为主经文（同一篇在五卷里另有两天）。'))
    wk = ''
    for w in range(0, 366, 7):
        ids = O[w:w + 7]; xs = [D[i] for i in ids]
        if all(x['sec'] == 'main' for x in xs):
            ps = sorted({psal(x) for x in xs}); lab = f'诗{ps[0]}' + (f'–{ps[-1]}' if ps[-1] != ps[0] else '')
        else:
            lab = '、'.join(dict.fromkeys(SECN.get(x['sec'], f'诗{psal(x)}').split(' · ')[-1] if x['sec'] != 'main' else f'诗{psal(x)}' for x in xs))
        wk += f'<a href="#day-{w + 1}" style="--c:{color(xs[0])}"><b>第 {w // 7 + 1} 周</b>{esc(lab)}<br><i>第 {w + 1}–{w + len(ids)} 天</i></a>'
    out['week'] = fig('vz-week', '🗂️ 53 周一览：每周读哪几篇', f'<nav class="vz-wk" aria-label="53 周一览">{wk}</nav>', '', '每格一周（第 53 周只有 2 天）；点一下跳到该周第一天。')
    top = [(V.NTFULL.get(b) or OTFULL.get(b) or b, n, 'var(--purple)' if b not in OT else 'var(--b3)', '') for b, n in st['xb'].most_common(12)]
    out['xref'] = (hbars('vz-xr', f'📚 概述里的延伸经文：最常出现的 12 卷（共 {st["x_total"]} 处）', top, ' 处',
                         f'从每天的本站概述中抽出、不含当天诗篇本身：新约 {st["x_nt"]} 处（紫色）、旧约 {st["x_ot"]} 处（橙色），分布在 {st["x_days"]} 天。每张卡片展开后可见当天的延伸经文。'))
    return out
