import os
# -*- coding: utf-8 -*-
"""真实底图：Natural Earth（公有领域）陆地/湖泊/河流，构建时投影为内联 SVG（无 CDN、无瓦片）。
标记 = 真实经纬度；不确定地点以虚线圈＋“约/说法之一”标明。"""
import json, math, functools
NE = '/workspace/ne/'
@functools.lru_cache(None)
def _load(n): return json.load(open(NE + n))
def _polys(geom):
    if geom['type'] == 'Polygon': return [geom['coordinates']]
    if geom['type'] == 'MultiPolygon': return geom['coordinates']
    return []
def _lines(geom):
    if geom['type'] == 'LineString': return [geom['coordinates']]
    if geom['type'] == 'MultiLineString': return geom['coordinates']
    return []
class Proj:
    def __init__(s, bbox, W):
        s.lo0, s.lo1, s.la0, s.la1 = bbox
        s.k = math.cos(math.radians((s.la0 + s.la1) / 2))
        s.W = W; s.sx = W / (s.lo1 - s.lo0); s.H = round((s.la1 - s.la0) * s.sx / s.k)
    def xy(s, lon, lat): return ((lon - s.lo0) * s.sx, (s.la1 - lat) * s.sx / s.k)
def _ring_path(P, ring, m=2.0, clamp=True):
    pts = []; last = None
    for lon, lat in ring:
        x, y = P.xy(lon, lat)
        if clamp: x = min(max(x, -m), P.W + m); y = min(max(y, -m), P.H + m)
        if last and abs(x - last[0]) < .9 and abs(y - last[1]) < .9: continue
        pts.append((x, y)); last = (x, y)
    if len(pts) < 3: return ''
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
def _inside_bb(ring, bb, pad=1.0):
    lo0, lo1, la0, la1 = bb
    xs = [c[0] for c in ring]; ys = [c[1] for c in ring]
    return not (max(xs) < lo0 - pad or min(xs) > lo1 + pad or max(ys) < la0 - pad or min(ys) > la1 + pad)
def basemap(P, bbox, res='50m', rivers=(), lakes=True):
    out = []
    land = _load(f'ne_{res}_land.geojson')
    d = []
    for f in land['features']:
        for poly in _polys(f['geometry']):
            if not _inside_bb(poly[0], bbox): continue
            for ring in poly:
                p = _ring_path(P, ring)
                if p: d.append(p)
    out.append(f'<path class="m-land" d="{"".join(d)}" fill-rule="evenodd"/>')
    if lakes:
        lk = _load('ne_10m_lakes.geojson' if res == '10m' else 'ne_50m_lakes.geojson'); d = []
        for f in lk['features']:
            for poly in _polys(f['geometry']):
                if not _inside_bb(poly[0], bbox, 0): continue
                p = _ring_path(P, poly[0])
                if p: d.append(p)
        out.append(f'<path class="m-lake" d="{"".join(d)}"/>')
    if rivers:
        rv = _load('ne_10m_rivers_lake_centerlines.geojson'); d = []
        for f in rv['features']:
            n = f['properties'].get('name') or ''
            if n not in rivers: continue
            for line in _lines(f['geometry']):
                seg = []
                for lon, lat in line:
                    x, y = P.xy(lon, lat)
                    if -5 <= x <= P.W + 5 and -5 <= y <= P.H + 5: seg.append((x, y))
                    else:
                        if len(seg) > 1: d.append('M' + 'L'.join(f'{a:.1f},{b:.1f}' for a, b in seg))
                        seg = []
                if len(seg) > 1: d.append('M' + 'L'.join(f'{a:.1f},{b:.1f}' for a, b in seg))
        out.append(f'<path class="m-river" d="{"".join(d)}"/>')
    return ''.join(out)
COL = dict(gold='#f5b83d', red='#ff6b6b', blue='#5ab0ff', green='#3ddc97', purple='#b48cff', pink='#ff7eb6', teal='#2fd3d3', gray='#a9b4c6', orange='#ff9f43')

def _base_svg(mid, title, P, bbox, markers, res, rivers, water, regions, routes):
    W = P.W
    s = [f'<svg class="map" viewBox="0 0 {W} {P.H}" role="img" aria-label="{title}（地形图）">']
    s.append(f'<rect class="m-sea" width="{W}" height="{P.H}"/>')
    s.append(basemap(P, bbox, res, rivers))
    for lon in range(math.ceil(bbox[0]), math.floor(bbox[1]) + 1):
        if lon % (5 if bbox[1]-bbox[0] > 12 else 1): continue
        x, _ = P.xy(lon, 0); s.append(f'<line class="m-grat" x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{P.H}"/><text class="m-gt" x="{x+3:.0f}" y="{P.H-6}">{lon}°E</text>')
    for lat in range(math.ceil(bbox[2]), math.floor(bbox[3]) + 1):
        if lat % (5 if bbox[1]-bbox[0] > 12 else 1): continue
        _, y = P.xy(0, lat); s.append(f'<line class="m-grat" x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}"/><text class="m-gt" x="4" y="{y-3:.0f}">{lat}°N</text>')
    for lab, lon, lat, rx, ry, c in regions:
        x, y = P.xy(lon, lat)
        s.append(f'<ellipse class="m-reg" cx="{x:.0f}" cy="{y:.0f}" rx="{rx*P.sx:.0f}" ry="{ry*P.sx/P.k:.0f}" style="--c:{COL[c]}"/><text class="m-regt" x="{x:.0f}" y="{y:.0f}" style="fill:{COL[c]}">{lab}</text>')
    for lab, lon, lat in water:
        x, y = P.xy(lon, lat); s.append(f'<text class="m-water" x="{x:.0f}" y="{y:.0f}">{lab}</text>')
    idx = {m['k']: m for m in markers}
    for r in routes:
        a, b, c = r[0], r[1], r[2]; bend = r[3] if len(r) > 3 else .18
        x1, y1 = P.xy(*idx[a]['ll']); x2, y2 = P.xy(*idx[b]['ll'])
        mx, my = (x1 + x2) / 2 - (y2 - y1) * bend, (y1 + y2) / 2 + (x2 - x1) * bend
        s.append(f'<path class="m-route" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" style="stroke:{COL[c]}" marker-end="url(#ar-{mid})"/>')
    s.append(f'<defs><marker id="ar-{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#ffd27a"/></marker></defs>')
    for i, m in enumerate(markers, 1):
        x, y = P.xy(*m['ll']); c = COL[m.get('c', 'gold')]
        unc = ' unc' if m.get('unc') else ''
        s.append(f'<g class="m-pt{unc}" data-i="{i}" tabindex="0"><title>{m["n"]}：{m["t"]}</title>')
        if m.get('unc'): s.append(f'<circle class="m-halo" cx="{x:.1f}" cy="{y:.1f}" r="22" style="stroke:{c}"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" style="fill:{c}"/><text class="m-num" x="{x:.1f}" y="{y+4.2:.1f}">{i}</text>')
        if m.get('lab', True):
            dx, dy, an = m.get('off', (15, 5, 'start'))
            s.append(f'<text class="m-lab" x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}">{m["n"]}</text>')
        s.append('</g>')
    s.append('</svg>')
    return ''.join(s)

# ---------------- 情景讲解图（插画风、可离线、带动画） ----------------
def _dp(pts, eps):
    """Douglas–Peucker 简化"""
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts)-1):
        d = abs(dy*pts[i][0] - dx*pts[i][1] + b[0]*a[1] - b[1]*a[0]) / L
        if d > dmax: dmax, idx = d, i
    if dmax > eps: return _dp(pts[:idx+1], eps)[:-1] + _dp(pts[idx:], eps)
    return [a, b]
def _smooth(pts, closed=True):
    """以中点为节点的二次贝塞尔平滑（手绘插画感）"""
    if len(pts) < 3: return ''
    if closed and pts[0] != pts[-1]: pts = pts + [pts[0]]
    mids = [((pts[i][0]+pts[i+1][0])/2, (pts[i][1]+pts[i+1][1])/2) for i in range(len(pts)-1)]
    d = f'M{mids[0][0]:.1f},{mids[0][1]:.1f}'
    for i in range(1, len(mids)):
        c = pts[i]; m = mids[i]; d += f'Q{c[0]:.1f},{c[1]:.1f} {m[0]:.1f},{m[1]:.1f}'
    if closed: d += f'Q{pts[0][0]:.1f},{pts[0][1]:.1f} {mids[0][0]:.1f},{mids[0][1]:.1f}Z'
    return d
def _scene_land(P, bbox, res):
    land = _load(f'ne_{res}_land.geojson'); out = []
    eps = max(1.6, P.W / 420)
    for f in land['features']:
        for poly in _polys(f['geometry']):
            if not _inside_bb(poly[0], bbox): continue
            ring = poly[0]; pts = []
            for lon, lat in ring:
                x, y = P.xy(lon, lat); m = 320
                pts.append((min(max(x, -m), P.W + m), min(max(y, -m), P.H + m)))
            if len(pts) > 3:
                k = max(range(len(pts)), key=lambda i: (pts[i][0]-pts[0][0])**2 + (pts[i][1]-pts[0][1])**2)
                pts = _dp(pts[:k+1], eps)[:-1] + _dp(pts[k:], eps)
            if len(pts) >= 4:
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                if (max(xs)-min(xs)) * (max(ys)-min(ys)) < 60: continue
                out.append(_smooth(pts))
    return ''.join(out)
def _scene_rivers(P, rivers):
    if not rivers: return ''
    rv = _load('ne_10m_rivers_lake_centerlines.geojson'); d = []
    for f in rv['features']:
        if (f['properties'].get('name') or '') not in rivers: continue
        for line in _lines(f['geometry']):
            pts = [P.xy(lon, lat) for lon, lat in line]
            pts = [p for p in pts if -20 <= p[0] <= P.W + 20 and -20 <= p[1] <= P.H + 20]
            pts = _dp(pts, 2.2)
            if len(pts) > 2: d.append(_smooth(pts, closed=False))
            elif len(pts) == 2: d.append(f'M{pts[0][0]:.1f},{pts[0][1]:.1f}L{pts[1][0]:.1f},{pts[1][1]:.1f}')
    return ''.join(d)
ICON_RULES = [('耶路撒冷', '🏰'), ('锡安', '🏰'), ('圣殿', '🛕'), ('山', '⛰️'), ('黎巴嫩', '🌲'), ('旷野', '🏜️'), ('沙漠', '🏜️'), ('巴比伦', '🏛️'), ('尼尼微', '🏛️'),
              ('埃及', '🏺'), ('孟斐斯', '🏺'), ('底比斯', '🏺'), ('示巴', '🐪'), ('迦勒底', '🐎'), ('推罗', '⛵'), ('以旬迦别', '⛵'), ('他施', '⛵'), ('海', '🌊'),
              ('水池', '💧'), ('泉', '💧'), ('园', '🌿'), ('葡萄', '🍇'), ('平原', '🌸'), ('基列', '🐐'), ('隐基底', '🌴'), ('大马士革', '🏙️'), ('提幔', '🦉'), ('乌斯', '⛺'),
              ('基达', '⛺'), ('书亚', '⛺'), ('拿玛', '⛺'), ('布斯', '⛺'), ('尼西亚', '⛪'), ('君士坦丁堡', '⛪'), ('以弗所', '⛪'), ('迦克墩', '⛪'), ('亚历山大', '📚'), ('城', '🏘️')]
def _icon(m):
    if m.get('ic'): return m['ic']
    for k, v in ICON_RULES:
        if k in m['n']: return v
    return '📍'
def _scene_svg(mid, title, P, bbox, markers, res, rivers, water, regions, routes, deco, valleys, land):
    W, H = P.W, P.H
    s = [f'<svg class="scene" viewBox="0 0 {W} {H}" role="img" aria-label="{title}（情景讲解图）">',
         f'<defs><linearGradient id="sea-{mid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="sc-sea1"/><stop offset="1" class="sc-sea2"/></linearGradient>'
         f'<linearGradient id="land-{mid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" class="sc-land1"/><stop offset="1" class="sc-land2"/></linearGradient>'
         f'<pattern id="dune-{mid}" width="26" height="14" patternUnits="userSpaceOnUse"><path d="M0,10 Q6.5,3 13,10 T26,10" class="sc-dune"/></pattern>'
         f'<pattern id="wave-{mid}" width="60" height="26" patternUnits="userSpaceOnUse"><path d="M0,13 Q15,5 30,13 T60,13" class="sc-wave"/></pattern>'
         f'<marker id="sar-{mid}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" class="sc-arh"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sea-{mid})"/>',
         f'<g class="sc-waves"><rect x="-60" y="0" width="{W+120}" height="{H}" fill="url(#wave-{mid})" opacity=".55"/></g>']
    if land:
        d = _scene_land(P, bbox, res)
        s.append(f'<path class="sc-shadow" d="{d}" transform="translate(5 7)"/><path class="sc-land" d="{d}" fill="url(#land-{mid})"/>')
    else:
        s.append(f'<rect class="sc-land" width="{W}" height="{H}" fill="url(#land-{mid})"/>')
    for lab, lon, lat, rx, ry, c in regions:
        x, y = P.xy(lon, lat)
        s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx*P.sx:.0f}" ry="{ry*P.sx/P.k:.0f}" fill="url(#dune-{mid})" class="sc-reg" style="--c:{COL[c]}"/>'
                 f'<text class="sc-regt" x="{x:.0f}" y="{y+5:.0f}" style="fill:{COL[c]}">{lab}</text>')
    for v in valleys:   # (名称, [(lon,lat),...], 颜色)
        pts = [P.xy(*p) for p in v[1]]
        d = _smooth(pts, closed=False) if len(pts) > 2 else f'M{pts[0][0]:.0f},{pts[0][1]:.0f}L{pts[1][0]:.0f},{pts[1][1]:.0f}'
        s.append(f'<path class="sc-valley" d="{d}" style="--c:{COL[v[2]]}"/><path class="sc-flow" d="{d}"/>')
        mx, my = pts[len(pts)//2]; s.append(f'<text class="sc-vt" x="{mx+8:.0f}" y="{my:.0f}">{v[0]}</text>')
    rd = _scene_rivers(P, rivers)
    if rd: s.append(f'<path class="sc-river" d="{rd}"/><path class="sc-flow" d="{rd}"/>')
    for lab, lon, lat in water:
        x, y = P.xy(lon, lat); s.append(f'<text class="sc-water" x="{x:.0f}" y="{y:.0f}">〰 {lab} 〰</text>')
    for e in deco:   # (emoji, lon, lat, size, anim)
        x, y = P.xy(e[1], e[2]); sz = e[3] if len(e) > 3 else 26; an = e[4] if len(e) > 4 else ''
        s.append(f'<text class="sc-deco {an}" x="{x:.0f}" y="{y:.0f}" font-size="{sz}">{e[0]}</text>')
    idx = {m['k']: (i, m) for i, m in enumerate(markers, 1)}
    for j, r in enumerate(routes):
        a, b, c = r[0], r[1], r[2]; bend = r[3] if len(r) > 3 else .18
        x1, y1 = P.xy(*idx[a][1]['ll']); x2, y2 = P.xy(*idx[b][1]['ll'])
        mx, my = (x1 + x2) / 2 - (y2 - y1) * bend, (y1 + y2) / 2 + (x2 - x1) * bend
        pid = f'rt-{mid}-{j}'
        s.append(f'<path id="{pid}" class="sc-route" d="M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" style="stroke:{COL[c]}" marker-end="url(#sar-{mid})"/>'
                 f'<g class="sc-mv" style="offset-path:path(\'M{x1:.0f},{y1:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}\');animation-duration:{6 + j}s"><text class="sc-mover" font-size="22" text-anchor="middle" dy="7">{r[4] if len(r) > 4 else "➤"}</text></g>')
    for i, m in enumerate(markers, 1):
        x, y = P.xy(*m['ll']); c = COL[m.get('c', 'gold')]
        s.append(f'<g class="sc-pt{" unc" if m.get("unc") else ""}" data-i="{i}" tabindex="0" style="--c:{c}"><title>{m["n"]}：{m["t"]}</title>'
                 f'<circle class="sc-ring" cx="{x:.1f}" cy="{y:.1f}" r="24"/>'
                 f'<circle class="sc-badge" cx="{x:.1f}" cy="{y:.1f}" r="17"/><text class="sc-ic" x="{x:.1f}" y="{y+7:.1f}">{_icon(m)}</text>'
                 f'<circle class="sc-nb" cx="{x+13:.1f}" cy="{y-13:.1f}" r="8.5"/><text class="sc-nt" x="{x+13:.1f}" y="{y-9.6:.1f}">{i}</text>')
        if m.get('lab', True):
            dx, dy, an = m.get('off', (15, 5, 'start'))
            dx = dx + (12 if dx > 0 else -12 if dx < 0 else 0)
            s.append(f'<text class="sc-lab" x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{an}">{m["n"]}</text>')
        s.append('</g>')
    s.append(f'<g class="sc-compass" transform="translate({W-54} 54)"><circle r="30"/><path d="M0,-24L6,0L0,24L-6,0Z"/><path class="n" d="M0,-24L6,0L-6,0Z"/><text y="-30">北</text></g>')
    s.append(f'<text class="sc-note" x="12" y="{H-12}">示意图 · 位置按真实经纬度，地形为艺术化简</text></svg>')
    return ''.join(s)

EXTRA = {}
def _lazy_scene(svg):
    import re as _re
    vb = _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    ar = f'{float(vb.group(1)):.0f}/{float(vb.group(2)):.0f}' if vb else '16/10'
    return f'<div class="mview v-scene on"><div class="map-wrap sc-lazy" style="aspect-ratio:{ar}"><template class="lazys">{svg}</template></div>'
def mapfig(mid, title, bbox, markers, W=1000, res='50m', rivers=(), water=(), regions=(), routes=(), cap='', note='',
           deco=(), story=None, valleys=(), base=True, land=True, zoom=None):
    """三视图地图：🎨 情景讲解图（默认，离线 SVG 动画）｜🗺️ 地形图（Natural Earth 离线 SVG）｜🌐 实时地图（Leaflet，多图源自动切换）。
    markers: dict(k, n=名, ll=(lon,lat), t=说明, c=颜色, lab, off=(dx,dy,anchor), unc=不确定, ic=图标)"""
    P = Proj(bbox, W)
    import json as _j, html as _h
    ex = EXTRA.get(mid, {})
    deco = tuple(deco) + tuple(ex.get('deco', ()))
    story = story or ex.get('story')
    mv = ex.get('movers', {})
    _rs = []
    for i, r in enumerate(routes):
        r = list(r) + ([.18] if len(r) == 3 else [])
        if i in mv: r = r[:4] + [mv[i]]
        _rs.append(tuple(r))
    routes = _rs
    st = story or [(m['k'], m['t']) for m in markers]
    kidx = {m['k']: i for i, m in enumerate(markers, 1)}
    live = dict(b=[bbox[2], bbox[0], bbox[3], bbox[1]], z=zoom,
                m=[dict(n=m['n'], la=m['ll'][1], lo=m['ll'][0], t=m['t'], c=COL[m.get('c', 'gold')], u=1 if m.get('unc') else 0) for m in markers],
                r=[[kidx[r[0]], kidx[r[1]], COL[r[2]], r[3] if len(r) > 3 else .18] for r in routes])
    tabs = [('scene', '🎨 情景讲解图'), ('base', '🗺️ 地形图（离线）'), ('live', '🌐 实时地图')]
    if not base: tabs = [t for t in tabs if t[0] != 'base']
    s = [f'<figure class="mapfig" id="map-{mid}" data-live="{_h.escape(_j.dumps(live, ensure_ascii=False))}">',
         f'<div class="mtabs" role="tablist" aria-label="地图视图">' + ''.join(
             f'<button role="tab" class="mt{" on" if k == "scene" else ""}" data-v="{k}" aria-selected="{"true" if k == "scene" else "false"}">{t}</button>' for k, t in tabs) + '</div>',
         _lazy_scene(_scene_svg(mid, title, P, bbox, markers, res, rivers, water, regions, routes, deco, valleys, land)),
         '<div class="story"><div class="st-ctl"><button class="st-b" data-a="prev" aria-label="上一站">◀</button><button class="st-b st-play" data-a="play" aria-label="播放讲解">▶ 播放讲解</button><button class="st-b" data-a="next" aria-label="下一站">▶</button><span class="st-n">0 / ' + str(len(st)) + '</span></div>',
         '<ol class="st-steps">' + ''.join(f'<li data-i="{kidx[k]}"><b>{markers[kidx[k]-1]["n"]}</b><span>{t}</span></li>' for k, t in st) + '</ol></div></div>']
    _st_txt = {t for _, t in st}
    if base:
        _d = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'assets', 'maps'); os.makedirs(_d, exist_ok=True)
        open(os.path.join(_d, f'{mid}.svg'), 'w').write(_base_svg(mid, title, P, bbox, markers, res, rivers, water, regions, routes))
        s.append(f'<div class="mview v-base"><div class="map-wrap" data-svg="assets/maps/{mid}.svg"><div class="lph">🗺️ 正在载入地形图…</div></div></div>')
    s.append('<div class="mview v-live"><div class="lsrc" role="group" aria-label="底图来源"></div><div class="lmap" aria-label="实时地图"><div class="lph">🌐 正在载入实时地图…</div></div><p class="lstat" aria-live="polite"></p></div>')
    s.append('<ol class="map-legend">' + ''.join(
        f'<li data-i="{i}" style="--c:{COL[m.get("c","gold")]}"><b>{_icon(m)} {m["n"]}</b>{"<em>（位置不确定）</em>" if m.get("unc") else ""}{"" if m["t"] in _st_txt else "<span>" + m["t"] + "</span>"}</li>' for i, m in enumerate(markers, 1)) + '</ol>')
    s.append(f'<figcaption>🗺️ {title}{"；" + cap if cap else ""}。{note}</figcaption></figure>')
    return ''.join(s)
