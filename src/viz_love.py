# -*- coding: utf-8 -*-
"""v4.3.0：《爱上诗篇》阅读版 / 导读页的图解。所有数字由本站数据实时计算；类型与哀歌/赞美归类为本站近似分类（并在图注中说明）。"""
import re, collections
from lib import esc
import viz43 as V
from viz43 import fig, tbl, stats, hbars, donut, psalter, heat, network, cloud, mindmap, lines, BKN, BKW, BOOKS, VERSES, book_of
FEAT = [3, 8, 18, 21, 22, 30, 46, 48, 51, 68, 69, 72, 73, 74, 78, 81, 86, 87, 88, 89, 90, 92, 95, 103, 104, 106, 109, 110, 118, 121, 135, 138]
EXTRA = [114, 146, 147, 148, 149, 150]          # 导论第二章示范诗 + 结论五篇
# 本站近似分类（单一主类型，便于计数；许多诗篇兼具多种类型）
GENRE = {'赞美诗': [8, 68, 92, 95, 103, 104, 114, 135, 146, 147, 148, 149, 150], '感恩诗': [18, 30, 118, 138], '君王诗': [21, 72, 89, 110],
         '锡安诗': [46, 48, 87], '个人哀歌': [3, 22, 69, 86, 88], '群体哀歌': [74, 90], '忏悔诗': [51], '智慧 / 训诲': [73, 81],
         '历史诗': [78, 106], '咒诅诗': [109], '信靠诗': [121]}
GCOL = {'赞美诗': '#f5b83d', '感恩诗': '#3ddc97', '君王诗': '#b48cff', '锡安诗': '#5ab0ff', '个人哀歌': '#ff6b81', '群体哀歌': '#ff9f43', '忏悔诗': '#a9b4c6',
        '智慧 / 训诲': '#2fd3d3', '历史诗': '#8fb3ff', '咒诅诗': '#e07a5f', '信靠诗': '#7bd389'}
# 全卷 150 篇的哀歌 / 赞美（含感恩）近似归类——用来画「从哀歌到赞美」的走势
LAMENT = {3, 4, 5, 6, 7, 9, 10, 12, 13, 17, 22, 25, 26, 27, 28, 31, 35, 38, 39, 40, 42, 43, 44, 51, 54, 55, 56, 57, 58, 59, 60, 61, 64, 69, 70, 71, 74, 77, 79, 80, 83, 85, 86, 88, 89, 90, 94, 102, 108, 109, 120, 123, 126, 130, 137, 140, 141, 142, 143}
PRAISE = {8, 18, 19, 24, 29, 30, 32, 33, 34, 46, 47, 48, 65, 66, 67, 68, 76, 84, 87, 92, 93, 95, 96, 97, 98, 99, 100, 103, 104, 105, 107, 111, 113, 114, 116, 117, 118, 122, 124, 134, 135, 136, 138, 145, 146, 147, 148, 149, 150}
THEMES = [('基督', r'基督|耶稣|弥赛亚|大卫的子孙|羔羊'), ('君王与国度', r'君王|王位|王权|国度|作王|受膏'), ('圣约与应许', r'立约|圣约|之约|守约|王约|背约|应许|信实'),
          ('苦难与哀歌', r'苦难|受苦|哀歌|患难|危机|仇敌|离弃|黑暗|痛苦'), ('赞美与感恩', r'赞美|称颂|颂赞|欢呼|哈利路亚|感恩|称谢'), ('神的话', r'律法|神的话|话语|训诲|教导|默想'),
          ('罪与悔改', r'罪|悔改|认罪|赦免'), ('敬拜与圣殿', r'敬拜|圣殿|锡安|圣所|节期|唱诗')]
TERMS = {'耶和华': '耶和华', '君王': '君王', '基督': '基督', '护理': '护理', '国度': '国度', '圣约': '立约|圣约|之约|王约', '赞美': '赞美|颂赞|称颂', '祷告': '祷告|祈求|呼求',
         '苦难': '苦难|受苦|患难', '仇敌': '仇敌|恶人', '锡安': '锡安', '圣殿': '圣殿|圣所', '敬拜': '敬拜', '信心': '信心|信靠|倚靠', '恩典': '恩典|恩惠',
         '罪': '罪', '悔改': '悔改|认罪', '救恩': '救恩|拯救', '公义': '公义|义人', '律法': '律法', '智慧': '智慧', '创造': '创造|受造', '历史': '历史|列祖',
         '盼望': '盼望', '安慰': '安慰', '慈爱': '慈爱|怜悯', '百姓': '百姓', '万国': '万国|列国', '默想': '默想', '唱': '唱|歌'}
PCOL = {'intro': '#ff7eb6', 'b1': '#3ddc97', 'b2': '#5ab0ff', 'b3': '#ff9f43', 'b4': '#b48cff', 'b5': '#f5b83d', 'final': '#ff6b81', 'back': '#a9b4c6'}
PNAME = {'intro': '导论', 'b1': '卷一 · 信', 'b2': '卷二 · 委', 'b3': '卷三 · 危', 'b4': '卷四 · 慰', 'b5': '卷五 · 庆', 'final': '结论五篇', 'back': '后记'}
def short(x):
    k = x['key']
    if k == 'front': return '推荐语'
    if k[0] == 'c' and k != 'c44': return '导' + k[1:]
    if k == 'c44': return '末五篇'
    if k[0] == 'b' and k != 'bio': return '卷' + BKN[int(k[1]) - 1]
    if re.match(r'p\d', k): return {'p86': '诗86–87', 'p88': '诗88–89'}.get(k, '诗' + k[1:])
    return {'post': '后记', 'bio': '作者'}[k]
def own_text(x, T, D):
    th, pts, ch, ap = T[x['key']]
    t = ' '.join([th, ' '.join(pts), ch, ap, ' '.join(x['flow']), ' '.join(b for _, b in D.get(x['key'], []))])
    return t
def compute(U, T, D, po):
    st = {}
    st['units'] = len(U); st['qs'] = sum(len(x['qs']) for x in U); st['deep'] = sum(len(D.get(x['key'], [])) for x in U)
    st['parts'] = collections.Counter(po[x['key']] for x in U)
    nt = {}
    for x in U:
        nt[x['key']] = V.nt_refs(x['refs'] + ' ' + x['christ'] + ' ' + own_text(x, T, D))
    st['nt'] = nt; st['nt_total'] = sum(len(v) for v in nt.values())
    st['nt_books'] = collections.Counter(b for v in nt.values() for b, _ in v)
    clean = {x['key']: V.REFRE.sub('', own_text(x, T, D)) for x in U}
    st['theme'] = {k: [len(re.findall(p, t)) for _, p in THEMES] for k, t in clean.items()}
    allt = ' '.join(clean.values())
    st['terms'] = {w: len(re.findall(p, allt)) for w, p in TERMS.items()}
    st['chars'] = sum(len(re.sub(r'\s', '', t)) for t in clean.values())
    return st
def part_header(pid, U, T, D, po, st):
    us = [x for x in U if po[x['key']] == pid]
    core = {'intro': '先学会怎样读：魅力、难点、主题、说话者、形式与大结构，最后收成十个读诗问题。', 'b1': T['b1'][0], 'b2': T['b2'][0], 'b3': T['b3'][0], 'b4': T['b4'][0],
            'b5': T['b5'][0], 'final': T['c44'][0], 'back': T['post'][0]}[pid]
    ps = [short(x) for x in us if re.match(r'p\d', x['key'])]
    q = sum(len(x['qs']) for x in us); n = sum(len(st['nt'][x['key']]) for x in us)
    tags = [f'{len(us)} 单元', f'{q} 道讨论题' if q else '无讨论题', (f'精读 {len(ps)} 章' if ps else f'{sum(len(D.get(x["key"], [])) for x in us)} 条深入要点')]
    if n: tags.append(f'新约引用 {n} 处')
    ico = {'intro': '🧭', 'b1': '🛡️', 'b2': '🏛️', 'b3': '🌩️', 'b4': '🕯️', 'b5': '🎺', 'final': '🎶', 'back': '📜'}[pid]
    return (f'<div class="part-x"><span class="px-ic" aria-hidden="true">{ico}</span><p class="px-core">{esc(core)}</p><div class="px-tags">' +
            ''.join(f'<span>{t}</span>' for t in tags) + '</div></div>')
def sections(U, T, D, po, st):
    out = {}
    ps_total = sum(VERSES.values())
    nfeat = len(FEAT)
    out['stat'] = (stats([(st['units'], '单元', '按原书目录', '#ff7eb6'), (8, '导论章', '怎样读诗篇', '#2fd3d3'), (5, '卷首总论', '信委危慰庆', '#5ab0ff'),
                          (30, '精读章', f'{nfeat} 首诗篇', '#3ddc97'), (nfeat + len(EXTRA), '首有专门讨论', '另含诗114 与 146–150', '#f5b83d'),
                          (st['qs'], '道讨论题', '原书题目', '#b48cff'), (st['deep'], '条深入要点', '本站整理', '#ff9f43'), (st['nt_total'], '处新约引用', '阅读版概述中出现（去重）', '#ff6b81')]) +
                   donut('vz-parts', '📊 52 个单元在全书中的分布', [(PNAME[p], st['parts'][p], PCOL[p]) for p in PCOL], (st['units'], '个单元'),
                         '按原书目录计数：导论 9（含推荐语）、五卷各 7（1 章总论 + 6 章精读）、结论 6、后记 2。') +
                   structure(U, po))
    out['mind'] = mindmap('vz-mind', '🧠 全书思维导图：读诗篇的六把钥匙', '爱上诗篇', [
        ('怎样读', '#ff7eb6', ['慢读细节（诗114）', '反复默想', '找结构与中心', '十个读诗问题']),
        ('总主题', '#5ab0ff', ['神的慈爱与护理', '义人仍有罪', '恶人亨通', '义人受苦', '苦中仍信']),
        ('谁在说话', '#2fd3d3', ['大卫', '百姓', '教会', '基督']),
        ('五卷', '#3ddc97', ['信 · 护理', '委 · 国度', '危 · 应许', '慰 · 信实', '庆 · 救恩']),
        ('大结构', '#ff9f43', ['各卷颂赞收尾', '个人 → 群体', '哀歌 → 赞美', '君王贯穿']),
        ('收束', '#ff6b81', ['146–150 对应五卷', '读 · 听 · 唱'])],
        '分支与要点取自本页导论各章与结论的概述（本站整理）。')
    marks = {p: '精读' for p in FEAT}; marks.update({114: '导论第二章示范', 146: '结论五篇', 147: '结论五篇', 148: '结论五篇', 149: '结论五篇', 150: '结论五篇'})
    def href(p):
        if p in (87,): return '#r-p86'
        if p in (89,): return '#r-p88'
        if p == 114: return '#r-c2'
        return f'#r-p{p}'
    out['psalter'] = (psalter('vz-psalter', f'🗺️ 诗篇 150 篇地图：本书重点讨论的 {len(marks)} 首', marks,
                              '每格一篇，按五卷分带；亮色格可点击跳到对应单元。悬停（或长按）显示经节数（和合本）。', href) +
                      hbars('vz-genre', f'🎼 {len(marks)} 首重点诗篇的类型（本站分类，近似）', [(g, len(v), GCOL[g], '') for g, v in GENRE.items()], ' 首',
                            '每首只计一个主类型，许多诗篇兼具多种类型。这是本站为方便概览所作的归类，不是原书的统计。'))
    xl = [f'卷{BKN[k - 1]}' for k, _, _ in BOOKS]
    lam = []; pra = []; tl = []
    for k, a, b in BOOKS:
        n = b - a + 1; l = sum(1 for p in range(a, b + 1) if p in LAMENT); r = sum(1 for p in range(a, b + 1) if p in PRAISE)
        lam.append(round(l * 100 / n)); pra.append(round(r * 100 / n)); tl.append((f'卷{BKN[k - 1]}（{a}–{b}，{n} 篇）', l, r))
    out['arc'] = (lines('vz-arc', '📈 从哀歌到赞美：五卷的走势（占该卷篇数的百分比）', xl, [('哀歌', '#ff6b81', lam), ('赞美与感恩', '#f5b83d', pra)],
                        f'本站按常见分类（近似）把 150 篇中的 {len(LAMENT)} 篇归为哀歌、{len(PRAISE)} 篇归为赞美或感恩，其余为智慧、君王、训诲等；用来印证原书「从哀歌走向赞美」的观察。') +
                  f'<details class="vz-t"><summary>📋 各卷计数</summary>{tbl(["卷", "哀歌", "赞美与感恩"], tl)}</details>')
    cols = [t for t, _ in THEMES]
    pids = list(PCOL)
    pm = []
    for p in pids:
        ks = [x['key'] for x in U if po[x['key']] == p]
        pm.append([round(sum(st['theme'][k][j] for k in ks) / len(ks), 1) for j in range(len(cols))])
    out['heat'] = (heat('vz-heat', '🔥 主题热图：各部分平均每单元提到几次', [PNAME[p] for p in pids], cols, pm,
                        '按关键词在本页本站概述（核心、要点、基督、应用、细读、深入）中出现的次数计算，已去掉经文出处。颜色越深＝该部分越常谈这个主题。', rowgroups=[PCOL[p] for p in pids]) +
                   '<details class="rd-more vz-more"><summary>🔎 展开：52 个单元逐一的主题热图</summary>' +
                   heat('vz-heat52', '🔥 52 个单元 × 8 个主题', [short(x) for x in U], cols, [st['theme'][x['key']] for x in U],
                        '点击左侧单元名可跳到该单元。', rowhref=[f'#r-{x["key"]}' for x in U], rowgroups=[PCOL[po[x['key']]] for x in U]) + '</details>')
    edges = collections.OrderedDict()
    for x in U:
        if re.match(r'p\d', x['key']) and st['nt'][x['key']]:
            edges[short(x)] = collections.Counter(b for b, _ in st['nt'][x['key']])
    lk = {short(x): f'#r-{x["key"]}' for x in U}
    nb = st['nt_books']
    out['net'] = (network('vz-net', f'✝️ 基督在诗篇中：{len(edges)} 个诗篇单元 → 新约 {len(nb)} 卷书', edges, lambda l: lk[l],
                          f'连线＝该单元概述里引用的新约经文（去重后共 {sum(sum(c.values()) for c in edges.values())} 处）；线越粗，引用越多。右侧圆点越大，被引越多。') +
                  hbars('vz-ntb', '📚 本页最常连到的新约书卷', [(V.NTFULL[b], n, 'var(--purple)', '') for b, n in nb.most_common(10)], ' 处',
                        f'统计范围：全部 52 个单元的概述与出处，共 {st["nt_total"]} 处（同一单元内去重）。'))
    out['cloud'] = cloud('vz-cloud', '☁️ 关键词云：本页概述里最常出现的词', st['terms'],
                         f'从本页约 {st["chars"]:,} 字的本站概述中计数（不含原书讨论题与经文出处）；字越大越常见，右上角为次数。')
    return out
def structure(U, po):
    rows = ''
    for p in PCOL:
        us = [x for x in U if po[x['key']] == p]
        rows += (f'<div class="sm-r" style="--c:{PCOL[p]}"><b>{PNAME[p]}<small>{len(us)}</small></b><div>' +
                 ''.join(f'<a href="#r-{x["key"]}" title="{esc(x["num"])} · {esc(x["title"])}">{short(x)}</a>' for x in us) + '</div></div>')
    return fig('vz-struct', '🧱 结构地图：原书目录一眼看完（点任一格跳到该单元）', f'<nav class="vz-sm" aria-label="原书目录结构地图">{rows}</nav>', '',
               '颜色＝部分；每格一个单元。')
def cheat(U, T, po):
    return ('<div class="vz-cheat">' + ''.join(
        f'<a class="ch-c" href="#r-{x["key"]}" style="--c:{PCOL[po[x["key"]]]}"><b>{short(x)}</b><span>{esc(T[x["key"]][0])}</span></a>' for x in U) + '</div>')
