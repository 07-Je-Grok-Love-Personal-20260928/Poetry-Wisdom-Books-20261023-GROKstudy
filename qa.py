import sys, os, json
from playwright.sync_api import sync_playwright
_a=[x for x in sys.argv[1:] if not x.startswith('--')]; pages = _a[0].split(',') if _a else None
widths = [390, 768, 1440]
D = os.path.abspath('docs')
if not pages: pages = [f[:-5] for f in sorted(os.listdir(D)) if f.endswith('.html')]
JS = '''() => {
 const vw = document.documentElement.clientWidth; const bad = [];
 const isClip = el => { for (let p = el.parentElement; p; p = p.parentElement) { const s = getComputedStyle(p); if (['auto','scroll','hidden'].includes(s.overflowX) && p !== document.body && p !== document.documentElement) return true; } return false; };
 for (const el of document.querySelectorAll('main *')) { const r = el.getBoundingClientRect(); if (r.width && (r.right > vw + 1 || r.left < -1) && !isClip(el)) { bad.push((el.tagName + '.' + el.className).slice(0,60) + ' ' + Math.round(r.left) + '-' + Math.round(r.right)); if (bad.length > 8) break; } }
 // text overlap check in flows/grids: siblings overlapping
 let ov = [];
 for (const c of document.querySelectorAll('.grid,.flow,.facts,.stats,.mm-br,.flips,.map-legend,.big5,.path,.two')) { const k = [...c.children].map(x => x.getBoundingClientRect()); for (let i = 0; i < k.length; i++) for (let j = i+1; j < k.length; j++) { const a = k[i], b = k[j]; if (a.left < b.right - 2 && b.left < a.right - 2 && a.top < b.bottom - 2 && b.top < a.bottom - 2) ov.push(c.className); } }
 return {sw: document.documentElement.scrollWidth, vw, bad, ov: [...new Set(ov)].slice(0,5), h: document.documentElement.scrollHeight};
}'''
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for w in widths:
        ctx = b.new_context(viewport={'width': w, 'height': 900}, device_scale_factor=1)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        for pid in pages:
            errs.clear()
            pg.goto(f'file://{D}/{pid}.html'); pg.wait_for_timeout(400)
            pg.evaluate('document.querySelectorAll(".sec").forEach(s=>s.style.contentVisibility="visible");document.querySelectorAll(".reveal").forEach(s=>s.classList.add("inview"))')
            r = pg.evaluate(JS); r['errs'] = list(errs)
            res[f'{pid}@{w}'] = r
            flag = 'OK ' if r['sw'] <= r['vw'] and not r['bad'] and not r['ov'] and not errs else 'BAD'
            print(flag, pid, w, 'sw', r['sw'], 'vw', r['vw'], 'h', r['h'], r['bad'][:4], r['ov'], errs[:3])
            pg.screenshot(path=f'qa/{pid}_{w}_top.png')
            if '--full' in sys.argv: pg.screenshot(path=f'qa/{pid}_{w}_full.png', full_page=True)
        ctx.close()
    b.close()
json.dump(res, open('qa/report.json', 'w'), indent=1)
