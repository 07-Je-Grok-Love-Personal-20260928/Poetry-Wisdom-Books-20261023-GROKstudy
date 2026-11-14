"""v2 QA：多视口 × 多轮交互。检查横向溢出、元素重叠、文字被裁切、控制台错误；保存截图。
用法：python3 tools/qa2.py [BASE_URL] [--pages a,b] [--widths 360,390] [--sources]"""
import sys, os, json, time
from playwright.sync_api import sync_playwright
args = sys.argv[1:]
BASE = next((a for a in args if a.startswith('http')), 'http://localhost:8820')
def opt(k, d):
    return args[args.index(k) + 1].split(',') if k in args else d
D = os.path.join(os.path.dirname(__file__), '..', 'docs')
PAGES = opt('--pages', [f[:-5] for f in sorted(os.listdir(D)) if f.endswith('.html')])
WIDTHS = [int(w) for w in opt('--widths', ['360', '390', '414', '768', '1024', '1280', '1440', '1920'])]
ALLSRC = '--sources' in args
NOSHOT = '--noshot' in args
OUT = os.path.join(os.path.dirname(__file__), '..', 'qa'); os.makedirs(OUT, exist_ok=True)
CHECK = r'''() => {
 const vw = document.documentElement.clientWidth, res = {sw: document.documentElement.scrollWidth, vw, over: [], ov: [], clip: []};
 const scrollers = el => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) { const s = getComputedStyle(p); if (['auto','scroll','hidden','clip'].includes(s.overflowX)) return true; } return false; };
 const vis = el => { const s = getComputedStyle(el); return s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity !== 0; };
 for (const el of document.querySelectorAll('main *')) { if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue; const r = el.getBoundingClientRect(); if (!r.width) continue;
   if ((r.right > vw + 1 || r.left < -1) && !scrollers(el)) { res.over.push((el.tagName + '.' + el.className).slice(0, 70) + ' ' + Math.round(r.left) + '→' + Math.round(r.right)); if (res.over.length > 10) break; } }
 const okClip = '.map-wrap,.anim,.dg,.media,.lmap,.hero,.v-live,.leaflet-container,.tbl-wrap,.st-steps,.toc-in,#toc,.pages,.sec,.flip,.mview,.story,main,.aurora,.lsrc';
 for (const el of document.querySelectorAll('main *')) { if (el.closest('svg') || el.closest('.leaflet-container')) continue; const s = getComputedStyle(el);
   if (['hidden','clip'].includes(s.overflowX) || ['hidden','clip'].includes(s.overflowY) || s.textOverflow === 'ellipsis') { if (el.matches(okClip)) continue; if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) { res.clip.push((el.tagName + '.' + el.className).slice(0,60) + ` ${el.scrollWidth}/${el.clientWidth}×${el.scrollHeight}/${el.clientHeight}`); if (res.clip.length > 8) break; } } }
 for (const sp of document.querySelectorAll('.flip span')) if (sp.scrollHeight > sp.clientHeight + 2) { res.clip.push('flip-text ' + sp.textContent.slice(0, 16) + ` ${sp.scrollHeight}/${sp.clientHeight}`); if (res.clip.length > 12) break; }
 const items = [];
 for (const el of document.querySelectorAll('main *')) { if (el.closest('svg,.leaflet-container,.flip,.tbl-wrap,.st-steps,.lph,.media')) continue; if (!vis(el)) continue; const cd = el.closest('details:not([open])'); if (cd && !el.closest('summary')) continue;
   let has = false; for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { has = true; break; } if (!has) continue;
   const s = getComputedStyle(el); if (s.position === 'fixed') continue;
   for (const r of el.getClientRects()) if (r.width > 2 && r.height > 2) items.push([el, r]); }
 const G = 80, grid = new Map();
 items.forEach((it, i) => { const r = it[1]; for (let gx = Math.floor(r.left / G); gx <= Math.floor(r.right / G); gx++) for (let gy = Math.floor((r.top + scrollY) / G); gy <= Math.floor((r.bottom + scrollY) / G); gy++) { const k = gx + ',' + gy; if (!grid.has(k)) grid.set(k, []); grid.get(k).push(i); } });
 const seen = new Set();
 for (const arr of grid.values()) for (let a = 0; a < arr.length; a++) for (let b = a + 1; b < arr.length; b++) { const i = arr[a], j = arr[b], key = i < j ? i + '-' + j : j + '-' + i; if (seen.has(key)) continue; seen.add(key);
   const [e1, r1] = items[i], [e2, r2] = items[j]; if (e1 === e2 || e1.contains(e2) || e2.contains(e1)) continue;
   const w = Math.min(r1.right, r2.right) - Math.max(r1.left, r2.left), h = Math.min(r1.bottom, r2.bottom) - Math.max(r1.top, r2.top);
   if (w > 3 && h > 3 && w * h > 0.25 * Math.min(r1.width * r1.height, r2.width * r2.height)) { res.ov.push((e1.tagName + '.' + e1.className).slice(0, 40) + ' × ' + (e2.tagName + '.' + e2.className).slice(0, 40) + ' «' + e1.textContent.trim().slice(0, 10) + '»'); if (res.ov.length > 8) return res; } }
 return res; }'''
def interact(pg):
    n = {}
    pg.evaluate('document.querySelectorAll(".sec").forEach(s=>s.style.contentVisibility="visible");document.querySelectorAll(".reveal").forEach(s=>s.classList.add("inview"))')
    pg.evaluate('document.querySelectorAll(".mapfig").forEach(f=>window.PW_mountScene&&PW_mountScene(f))')
    n['details'] = pg.evaluate('(()=>{const d=[...document.querySelectorAll("main details")];d.forEach(x=>x.open=true);return d.length})()')
    n['flip'] = pg.evaluate('(()=>{const f=[...document.querySelectorAll(".flip")];f.forEach(x=>x.click());return f.length})()')
    n['quiz'] = pg.evaluate('(()=>{let k=0;document.querySelectorAll(".qz").forEach(q=>{const b=q.querySelector(".qo button");if(b){b.click();k++}});return k})()')
    n['story'] = pg.evaluate('(()=>{let k=0;document.querySelectorAll(".mapfig .st-b[data-a=next]").forEach(b=>{b.click();b.click();k++});return k})()')
    n['creed'] = pg.evaluate('(()=>{let k=0;document.querySelectorAll("[data-mode],[data-init]").forEach(b=>{b.click();k++});document.querySelectorAll("[data-init].on").forEach(b=>b.click());document.querySelectorAll(".creed p.hide").forEach(p=>p.classList.remove("hide"));return k})()')
    figs = pg.locator('.mapfig'); nf = figs.count(); n['maps'] = nf; n['map_views'] = 0; n['src_ok'] = 0; n['src_try'] = 0
    for i in range(nf):
        f = figs.nth(i)
        for v in ('base', 'scene'):
            b = f.locator(f'.mt[data-v={v}]')
            if b.count(): b.click(); n['map_views'] += 1
    return n
def live_sources(pg, n, all_src):
    figs = pg.locator('.mapfig'); nf = figs.count()
    for i in range(nf):
        f = figs.nth(i); f.scroll_into_view_if_needed(); f.locator('.mt[data-v=live]').click(); n['map_views'] += 1
        try: f.locator('.ls').first.wait_for(timeout=8000)
        except Exception: n['live_fail'] = n.get('live_fail', 0) + 1; continue
        k = f.locator('.ls').count(); idx = list(range(k)) if all_src else [1, 2]
        for j in idx:
            f.locator(f'.ls[data-i="{j}"]').click(); n['src_try'] += 1
            t0 = time.time()
            while time.time() - t0 < 13:
                st = f.locator('.lstat').inner_text()
                if '✅' in st or '⏳' not in st: break
                pg.wait_for_timeout(250)
            st = f.locator('.lstat').inner_text()
            if '✅' in st: n['src_ok'] += 1
            else: n.setdefault('src_bad', []).append(f'{j}:{st[:30]}')
        f.locator('.mt[data-v=scene]').click()
rep = {}; tot = dict(ok=0, bad=0)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--disable-dev-shm-usage'])
    for w in WIDTHS:
        mobile = w < 800
        ctx = b.new_context(viewport={'width': w, 'height': 860 if mobile else 900}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append('JS ' + str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
        for pid in PAGES:
            errs.clear(); r = {}
            pg.goto(f'{BASE}/{pid}.html', wait_until='load'); pg.wait_for_timeout(300)
            pg.add_style_tag(content='*,*:before,*:after{transition:none!important}.sec{content-visibility:visible!important}')
            pg.evaluate('document.querySelectorAll(".reveal").forEach(s=>s.classList.add("inview"))'); pg.wait_for_timeout(150)
            r['pass1'] = pg.evaluate(CHECK)
            if not NOSHOT: pg.screenshot(path=f'{OUT}/{pid}_{w}_top.jpg', type='jpeg', quality=70)
            n = interact(pg)
            if w in (390, 1280) or ALLSRC: live_sources(pg, n, ALLSRC and w == 1280)
            pg.wait_for_timeout(300)
            r['pass2'] = pg.evaluate(CHECK)
            pg.evaluate('document.documentElement.classList.add(innerWidth>1100?"x":"toc-open");var T=document.getElementById("toc");if(T)T.classList.add("all");document.documentElement.classList.add("leg-on")')
            pg.wait_for_timeout(350); r['pass3'] = pg.evaluate(CHECK)
            if not NOSHOT: pg.screenshot(path=f'{OUT}/{pid}_{w}_tocleg.jpg', type='jpeg', quality=65)
            pg.evaluate('document.documentElement.classList.remove("toc-open","leg-on")'); pg.wait_for_timeout(300)
            if not NOSHOT:
                h = pg.evaluate('document.documentElement.scrollHeight')
                try: pg.screenshot(path=f'{OUT}/{pid}_{w}_full.jpg', type='jpeg', quality=50, full_page=h <= 24000, clip=None if h <= 24000 else {'x': 0, 'y': 0, 'width': w, 'height': 24000}, timeout=120000, animations='disabled', scale='css')
                except Exception as e: print('shot-fail', pid, w, str(e)[:80], flush=True)
            r['n'] = n; r['errs'] = list(errs)
            bad = [k for k in ('pass1', 'pass2', 'pass3') if r[k]['sw'] > r[k]['vw'] or r[k]['over'] or r[k]['ov'] or r[k]['clip']] + (['errs'] if errs else [])
            r['ok'] = not bad; tot['ok' if not bad else 'bad'] += 1
            print(('OK ' if not bad else 'BAD'), pid, w, 'sw/vw', r['pass2']['sw'], r['pass2']['vw'], {k: n[k] for k in n if n[k]},
                  '' if not bad else {k: (r[k]['over'][:3], r[k]['ov'][:3], r[k]['clip'][:3]) for k in bad if k != 'errs'}, errs[:3], flush=True)
            rep[f'{pid}@{w}'] = r
        ctx.close()
    b.close()
json.dump(rep, open(f'{OUT}/report2.json', 'w'), ensure_ascii=False, indent=1)
print('TOTAL', tot)
