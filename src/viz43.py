# -*- coding: utf-8 -*-
"""v4.3.0 可视化：所有数字都由真实数据（本站概述、原书目录、和合本诗篇全文）计算；SVG/HTML 内联，<template> 懒渲染，附数据表。"""
import re, math, json, os, collections
from lib import esc
ROOT = os.path.join(os.path.dirname(__file__), '..')
PSV = json.load(open(os.path.join(ROOT, 'data', 'psalms_cuv.json')))           # 和合本诗篇全文（每篇经节列表）
VERSES = {int(k): len(v) for k, v in PSV.items()}
BOOKS = [(1, 1, 41), (2, 42, 72), (3, 73, 89), (4, 90, 106), (5, 107, 150)]
def book_of(p): return next(k for k, a, b in BOOKS if a <= p <= b)
BKN = '一二三四五'; BKW = ['信', '委', '危', '慰', '庆']
NT = ['太', '可', '路', '约', '徒', '罗', '林前', '林后', '加', '弗', '腓', '西', '帖前', '帖后', '提前', '提后', '多', '门', '来', '雅', '彼前', '彼后', '约壹', '犹', '启']
NTFULL = dict(太='马太福音', 可='马可福音', 路='路加福音', 约='约翰福音', 徒='使徒行传', 罗='罗马书', 林前='林前', 林后='林后', 加='加拉太书', 弗='以弗所书', 腓='腓立比书', 西='歌罗西书', 帖前='帖前', 帖后='帖后', 提前='提前', 提后='提后', 多='提多书', 门='腓利门书', 来='希伯来书', 雅='雅各书', 彼前='彼前', 彼后='彼后', 约壹='约壹', 犹='犹大书', 启='启示录')
NTRE = re.compile(r'(?<![\u4e00-\u9fff])(约壹|林前|林后|帖前|帖后|提前|提后|彼前|彼后|太|可|路|约|徒|罗|加|弗|腓|西|多|门|来|雅|犹|启)\s*(\d+)[:：](\d+)')
REFRE = re.compile(r'[\u4e00-\u9fff]{1,2}\d+[:：][\d–\-、,]+')
def nt_refs(text):
    """去重后的新约引用：[(书卷, '章:节')]"""
    seen = []
    for m in NTRE.finditer(text):
        k = (m.group(1), f'{m.group(2)}:{m.group(3)}')
        if k not in seen: seen.append(k)
    return seen
# ---------- 通用外壳 ----------
def fig(vid, title, inner, table='', note='', cls=''):
    tb = f'<details class="vz-t"><summary>📋 数据表（无障碍 / 打印）</summary>{table}</details>' if table else ''
    nt = f'<p class="vz-n">{note}</p>' if note else ''
    return (f'<figure class="vz {cls}" id="{vid}" aria-labelledby="{vid}-t"><figcaption id="{vid}-t">{title}</figcaption>'
            f'<div class="vz-c"><div class="vz-ph" aria-hidden="true"></div></div><template>{inner}</template>{tb}{nt}</figure>')
def tbl(head, rows):
    return ('<div class="tbl-wrap"><table class="tbl vz-tb"><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in head) + '</tr></thead><tbody>' +
            ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
def stats(items):
    """items: (数字, 标签, 说明, 颜色)"""
    return '<div class="vz-stats">' + ''.join(f'<div style="--c:{c}"><b data-n="{n}">{n}</b><span>{l}</span><small>{d}</small></div>' for n, l, d, c in items) + '</div>'
def hbars(vid, title, rows, unit='', note='', maxv=None):
    """rows: (标签, 数值, 颜色, 链接或'')；HTML 横条（天然响应式）"""
    mx = maxv or max(v for _, v, _, _ in rows) or 1
    inner = '<div class="vz-hb" role="img" aria-label="' + esc(title) + '：' + '，'.join(f'{l} {v}{unit}' for l, v, _, _ in rows) + '">' + ''.join(
        f'<div class="hb-r"><span class="hb-l">{(f"<a href={chr(34)}{h}{chr(34)}>{l}</a>" if h else l)}</span><span class="hb-b"><i style="--w:{v / mx:.4f};--c:{c}"></i></span><b>{v}{unit}</b></div>' for l, v, c, h in rows) + '</div>'
    return fig(vid, title, inner, tbl(['项目', '数值'], [(l, f'{v}{unit}') for l, v, _, _ in rows]), note)
def donut(vid, title, rows, center, note=''):
    """rows: (标签, 数值, 颜色)"""
    tot = sum(v for _, v, _ in rows); r = 70; C = 2 * math.pi * r; off = 0; seg = ''
    for l, v, c in rows:
        L = C * v / tot
        seg += f'<circle r="{r}" cx="100" cy="100" fill="none" stroke-width="34" style="stroke:{c}" stroke-dasharray="{L - 1.5:.2f} {C - L + 1.5:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 100 100)"><title>{l}：{v}</title></circle>'
        off += L
    leg = '<ul class="vz-leg">' + ''.join(f'<li><i style="--c:{c}"></i>{l}<b>{v}</b><small>{v * 100 / tot:.0f}%</small></li>' for l, v, c in rows) + '</ul>'
    svg = (f'<div class="vz-donut"><svg viewBox="0 0 200 200" role="img" aria-label="{esc(title)}">{seg}'
           f'<text x="100" y="96" text-anchor="middle" class="dn-n">{center[0]}</text><text x="100" y="120" text-anchor="middle" class="dn-l">{center[1]}</text></svg>{leg}</div>')
    return fig(vid, title, svg, tbl(['部分', '数量', '占比'], [(l, v, f'{v * 100 / tot:.1f}%') for l, v, _ in rows]), note)
BC = ['var(--b1)', 'var(--b2)', 'var(--b3)', 'var(--b4)', 'var(--b5)']
# ---------- 诗篇地图：150 格 ----------
def psalter(vid, title, marks, note='', href=lambda p: ''):
    """marks: {诗篇号: 提示}；按五卷分带排列"""
    rows = ''
    for k, a, b in BOOKS:
        cells = ''
        for p in range(a, b + 1):
            on = p in marks; h = href(p) if on else ''
            t = f'诗{p}（{VERSES[p]} 节）' + (f'：{esc(marks[p])}' if on else '')
            inner = f'<span>{p}</span>'
            cells += (f'<a class="ps on" href="{h}" title="{t}" aria-label="{t}">{inner}</a>' if on and h else f'<i class="ps{" on" if on else ""}" title="{t}">{inner}</i>')
        rows += f'<div class="ps-row" style="--c:{BC[k - 1]}"><b class="ps-k">卷{BKN[k - 1]}<small>{BKW[k - 1]} · {a}–{b}</small></b><div class="ps-cells">{cells}</div></div>'
    inner = f'<div class="vz-ps" role="img" aria-label="{esc(title)}：共 150 篇，高亮 {len(marks)} 篇">{rows}</div>'
    tr = [(f'卷{BKN[book_of(p) - 1]}', f'诗{p}', esc(marks[p])) for p in sorted(marks)]
    return fig(vid, title, inner, tbl(['卷', '诗篇', '说明'], tr), note)
# ---------- 热力矩阵 ----------
def heat(vid, title, rowlabels, cols, M, note='', rowhref=None, rowgroups=None):
    mx = max(max(r) for r in M) or 1
    head = '<div class="hm-h"><span></span>' + ''.join(f'<b>{c}</b>' for c in cols) + '</div>'
    body = ''
    for i, (lab, r) in enumerate(zip(rowlabels, M)):
        g = rowgroups[i] if rowgroups else ''
        lb = f'<a href="{rowhref[i]}">{lab}</a>' if rowhref else lab
        body += f'<div class="hm-r" style="--g:{g or "var(--accent)"}"><span>{lb}</span>' + ''.join(f'<i style="--v:{v / mx:.3f}" title="{esc(lab)} · {cols[j]}：{v}">{v or ""}</i>' for j, v in enumerate(r)) + '</div>'
    inner = f'<div class="vz-hm" style="--nc:{len(cols)}" role="img" aria-label="{esc(title)}">{head}{body}</div>'
    return fig(vid, title, inner, tbl(['单元'] + cols, [[lab] + r for lab, r in zip(rowlabels, M)]), note)
# ---------- 二部网络：诗篇 → 新约 ----------
def network(vid, title, edges, lhref=None, note=''):
    """edges: {诗篇标签: Counter(新约书卷)}"""
    L = list(edges); R = sorted({b for c in edges.values() for b in c}, key=lambda b: NT.index(b) if b in NT else 99)
    rc = collections.Counter(); [rc.update(c) for c in edges.values()]
    H = max(len(L), len(R)) * 22 + 40; W = 560
    ly = {l: 30 + i * (H - 50) / max(1, len(L) - 1) for i, l in enumerate(L)}; ry = {r: 30 + i * (H - 50) / max(1, len(R) - 1) for i, r in enumerate(R)}
    s = f'<svg class="vz-net" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
    for l, c in edges.items():
        for r, n in c.items():
            s += f'<path d="M150 {ly[l]:.1f} C 290 {ly[l]:.1f}, 290 {ry[r]:.1f}, 420 {ry[r]:.1f}" style="stroke-width:{1 + n * .9:.1f}" data-l="{esc(l)}" data-r="{r}"><title>{esc(l)} → {NTFULL.get(r, r)}（{n}）</title></path>'
    for l in L:
        k = book_of(int(re.match(r'\D*(\d+)', l).group(1)))
        lab = f'<a href="{lhref(l)}">' if lhref else ''
        s += f'{lab}<g class="nd" data-l="{esc(l)}"><circle cx="150" cy="{ly[l]:.1f}" r="6" style="fill:{BC[k - 1]}"/><text x="140" y="{ly[l] + 4:.1f}" text-anchor="end">{esc(l)}</text></g>{"</a>" if lhref else ""}'
    for r in R:
        s += f'<g class="nd" data-r="{r}"><circle cx="420" cy="{ry[r]:.1f}" r="{5 + rc[r] * .8:.1f}" style="fill:var(--purple)"/><text x="{432 + rc[r] * .8:.1f}" y="{ry[r] + 4:.1f}">{NTFULL.get(r, r)} · {rc[r]}</text></g>'
    s += '</svg>'
    rows = [(l, '、'.join(f'{NTFULL.get(r, r)}×{n}' for r, n in c.most_common())) for l, c in edges.items()]
    return fig(vid, title, s, tbl(['诗篇', '新约书卷 × 次数'], rows), note, 'vz-wide')
# ---------- 关键词云（频次） ----------
def cloud(vid, title, freq, note=''):
    items = sorted(freq.items(), key=lambda x: -x[1]); mx = items[0][1]; mn = items[-1][1]
    order = items[::2] + items[1::2][::-1]
    inner = '<div class="vz-cloud" role="img" aria-label="' + esc(title) + '：' + '，'.join(f'{t}{n}' for t, n in items) + '">' + ''.join(
        f'<span style="--s:{(n - mn) / max(1, mx - mn):.3f};--h:{(i * 47) % 360}" title="{t}：{n} 次">{t}<sup>{n}</sup></span>' for i, (t, n) in enumerate(order)) + '</div>'
    return fig(vid, title, inner, tbl(['词', '次数'], items), note)
# ---------- 思维导图（径向） ----------
def mindmap(vid, title, root, branches, note=''):
    """两侧树形导图：左右各半分支，子项纵向排列，不会互相遮挡。branches: (标题, 颜色, [子项])"""
    half = (len(branches) + 1) // 2; sides = [branches[:half], branches[half:]]
    hs = [sum(len(k) * 32 + 26 for _, _, k in sd) for sd in sides]; H = max(hs) + 20; W = 900; cx, cy = W / 2, H / 2
    s = f'<svg class="vz-mm" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
    for si, sd in enumerate(sides):
        y = (H - hs[si]) / 2; bx = cx - 175 if si == 0 else cx + 175; kx = bx - 95 if si == 0 else bx + 95
        for t, c, kids in sd:
            bh = len(kids) * 32 + 26; by = y + bh / 2
            s += f'<path d="M{cx} {cy} C {(cx + bx) / 2:.0f} {cy:.0f}, {(cx + bx) / 2:.0f} {by:.0f}, {bx:.0f} {by:.0f}" style="stroke:{c}" class="mm-l"/>'
            for j, kd in enumerate(kids):
                ky = y + 13 + 16 + j * 32
                s += f'<path d="M{bx:.0f} {by:.0f} C {(bx + kx) / 2:.0f} {by:.0f}, {(bx + kx) / 2:.0f} {ky:.0f}, {kx:.0f} {ky:.0f}" style="stroke:{c}" class="mm-k"/>'
                s += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="3.5" style="fill:{c}"/><text x="{kx - 8 if si == 0 else kx + 8:.0f}" y="{ky + 4:.0f}" text-anchor="{"end" if si == 0 else "start"}" class="mm-kt">{esc(kd)}</text>'
            s += f'<g class="mm-b"><rect x="{bx - 64:.0f}" y="{by - 19:.0f}" width="128" height="38" rx="19" style="fill:{c}"/><text x="{bx:.0f}" y="{by + 6:.0f}" text-anchor="middle">{esc(t)}</text></g>'
            y += bh
    s += f'<g class="mm-r"><circle cx="{cx}" cy="{cy}" r="62"/><text x="{cx}" y="{cy + 7}" text-anchor="middle">{esc(root)}</text></g></svg>'
    rows = [(t, '、'.join(k)) for t, _, k in branches]
    return fig(vid, title, s, tbl(['分支', '要点'], rows), note, 'vz-wide')
# ---------- 折线（多序列，按卷） ----------
def lines(vid, title, xlabels, series, note='', unit='%'):
    """series: (名称, 颜色, [值])"""
    W, H, P = 560, 260, 44; mx = max(max(v) for _, _, v in series) or 1; mx = math.ceil(mx / 10) * 10
    X = lambda i: P + i * (W - 2 * P) / (len(xlabels) - 1); Y = lambda v: H - P - v / mx * (H - 2 * P)
    s = f'<svg class="vz-ln" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
    for t in range(0, mx + 1, mx // 4 or 1):
        s += f'<line x1="{P}" x2="{W - P}" y1="{Y(t):.1f}" y2="{Y(t):.1f}" class="gl"/><text x="{P - 8}" y="{Y(t) + 4:.1f}" text-anchor="end" class="ax">{t}{unit}</text>'
    for i, xl in enumerate(xlabels): s += f'<text x="{X(i):.1f}" y="{H - P + 22}" text-anchor="middle" class="ax">{xl}</text>'
    for nm, c, v in series:
        pts = ' '.join(f'{X(i):.1f},{Y(y):.1f}' for i, y in enumerate(v))
        area = f'{X(0):.1f},{Y(0):.1f} ' + pts + f' {X(len(v) - 1):.1f},{Y(0):.1f}'
        s += f'<polygon points="{area}" style="fill:{c}" class="ar"/><polyline points="{pts}" style="stroke:{c}" class="ln"/>'
        s += ''.join(f'<circle cx="{X(i):.1f}" cy="{Y(y):.1f}" r="4.5" style="fill:{c}"><title>{nm} · {xlabels[i]}：{y}{unit}</title></circle>' for i, y in enumerate(v))
    s += '</svg><ul class="vz-leg row">' + ''.join(f'<li><i style="--c:{c}"></i>{nm}</li>' for nm, c, _ in series) + '</ul>'
    return fig(vid, title, s, tbl(['卷'] + [nm for nm, _, _ in series], [[xl] + [f'{v[i]}{unit}' for _, _, v in series] for i, xl in enumerate(xlabels)]), note)
# ---------- 散点 ----------
def scatter(vid, title, pts, xlab, ylab, note='', table=None):
    """条带散点：x＝经节数（平方根刻度），y＝天数（按类别等距分带）。pts: (x, y, 颜色, 提示)"""
    ys = sorted({p[1] for p in pts}); W, P = 560, 46; band = 54; H = P + len(ys) * band + 34; mxx = max(p[0] for p in pts)
    X = lambda v: P + 10 + math.sqrt(v / mxx) * (W - 2 * P - 10); Y = lambda v: P - 14 + (len(ys) - 1 - ys.index(v)) * band + band / 2
    s = f'<svg class="vz-sc" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
    for t in (1, 10, 25, 50, 100, 176):
        if t <= mxx: s += f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{P - 14}" y2="{H - 34}" class="gl"/><text x="{X(t):.1f}" y="{H - 18}" text-anchor="middle" class="ax">{t}</text>'
    cnt = collections.Counter(p[1] for p in pts)
    for v in ys:
        s += f'<rect x="{P + 4}" y="{Y(v) - band / 2 + 4:.1f}" width="{W - 2 * P}" height="{band - 8}" rx="10" class="sc-band"/><text x="{P - 2}" y="{Y(v) + 4:.1f}" text-anchor="end" class="ax">{v} 天</text>'
        s += f'<text x="{W - P + 6}" y="{Y(v) + 4:.1f}" class="ax">{cnt[v]} 篇</text>'
    import random; rnd = random.Random(7)
    for x, y, c, t in pts:
        s += f'<circle cx="{X(x):.1f}" cy="{Y(y) + rnd.uniform(-band / 2 + 12, band / 2 - 12):.1f}" r="4.2" style="fill:{c}" class="pt"><title>{t}</title></circle>'
    s += f'<text x="{W / 2}" y="{H - 2}" text-anchor="middle" class="ax">{xlab}</text></svg>'
    return fig(vid, title, s, table if table is not None else tbl([xlab, ylab, '诗篇'], [(x, y, t) for x, y, _, t in pts]), note)
