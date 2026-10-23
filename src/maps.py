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
def mapfig(mid, title, bbox, markers, W=1000, res='50m', rivers=(), water=(), regions=(), routes=(), cap='', note=''):
    """markers: dict(n=名, ll=(lon,lat), t=说明, c=颜色, lab=是否直接标注, off=(dx,dy,anchor), unc=是否不确定)"""
    P = Proj(bbox, W)
    s = [f'<figure class="mapfig" id="map-{mid}"><div class="map-wrap"><svg class="map" viewBox="0 0 {W} {P.H}" role="img" aria-label="{title}">']
    s.append(f'<rect class="m-sea" width="{W}" height="{P.H}"/>')
    s.append(basemap(P, bbox, res, rivers))
    # graticule
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
    s.append('</svg></div>')
    s.append('<ol class="map-legend">' + ''.join(
        f'<li data-i="{i}" style="--c:{COL[m.get("c","gold")]}"><b>{m["n"]}</b>{"<em>（位置不确定）</em>" if m.get("unc") else ""}<span>{m["t"]}</span></li>' for i, m in enumerate(markers, 1)) + '</ol>')
    s.append(f'<figcaption>🗺️ {title}。底图：Natural Earth 公有领域数据（构建时投影为本地 SVG），地点按真实经纬度标注{"；" + cap if cap else ""}。{note}</figcaption></figure>')
    return ''.join(s)
