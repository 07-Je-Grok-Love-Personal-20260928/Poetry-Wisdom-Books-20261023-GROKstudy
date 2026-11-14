"""实时地图逐源测试：每页每图 × 14 个来源，记录是否显示瓦片（加载成功 + 实际可见瓦片数）。用法：python3 tools/livemaps.py BASE 390,1280 page..."""
import sys, json, time
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; WS = [int(x) for x in sys.argv[2].split(',')]; PAGES = sys.argv[3:]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for w in WS:
        ctx = b.new_context(viewport={'width': w, 'height': 860}, is_mobile=w < 800, has_touch=w < 800)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for pid in PAGES:
            pg.goto(f'{BASE}/{pid}.html', wait_until='load'); pg.evaluate('localStorage.clear()')
            figs = pg.locator('.mapfig')
            for i in range(figs.count()):
                f = figs.nth(i); mid = f.get_attribute('id'); f.scroll_into_view_if_needed()
                f.locator('.mt[data-v=live]').click(); f.locator('.ls').first.wait_for(timeout=15000)
                t0 = time.time()
                while time.time() - t0 < 15 and '✅' not in f.locator('.lstat').inner_text(): pg.wait_for_timeout(250)
                auto = f.locator('.lstat').inner_text()[:40]
                row = {'auto': auto, 'ok': [], 'bad': []}
                for j in range(f.locator('.ls').count()):
                    f.locator(f'.ls[data-i="{j}"]').click(); t0 = time.time()
                    while time.time() - t0 < 14:
                        st = f.locator('.lstat').inner_text()
                        if '✅' in st or '⏳' not in st: break
                        pg.wait_for_timeout(250)
                    pg.wait_for_timeout(400)
                    st = f.locator('.lstat').inner_text()
                    vis = f.evaluate('''f=>{const b=f.querySelector('.lmap').getBoundingClientRect();return [...f.querySelectorAll('.leaflet-tile-loaded')].filter(t=>{const r=t.getBoundingClientRect();return r.right>b.left&&r.left<b.right&&r.bottom>b.top&&r.top<b.bottom}).length}''')
                    name = f.locator(f'.ls[data-i="{j}"]').inner_text()
                    (row['ok'] if '✅' in st and vis > 0 else row['bad']).append(f'{name}:{vis}:{st[:20]}' if not ('✅' in st and vis > 0) else name)
                res[f'{pid}/{mid}@{w}'] = row
                print(pid, mid, w, f"{len(row['ok'])}/{len(row['ok'])+len(row['bad'])}", row['bad'], '| auto:', auto, flush=True)
        print('errs', errs[:5]); ctx.close()
    b.close()
json.dump(res, open('qa/livemaps.json', 'w'), ensure_ascii=False, indent=1)
