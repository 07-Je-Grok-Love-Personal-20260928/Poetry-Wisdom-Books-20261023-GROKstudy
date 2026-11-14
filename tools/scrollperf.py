"""滚动流畅度测量：Pixel 5 视口 + CPU 4× 降速，自动滚动全页，统计帧间隔。用法：python3 scrollperf.py BASEURL page..."""
import sys, json
from playwright.sync_api import sync_playwright
base = sys.argv[1]; pages = sys.argv[2:]
JS = """async()=>{const f=[];let last=performance.now(),run=true;function t(n){f.push(n-last);last=n;if(run)requestAnimationFrame(t)}requestAnimationFrame(t);
const H=document.documentElement.scrollHeight-innerHeight;const step=Math.max(40,H/240);for(let y=0;y<H;y+=step){scrollTo(0,y);await new Promise(r=>requestAnimationFrame(r))}
run=false;await new Promise(r=>setTimeout(r,50));f.shift();f.sort((a,b)=>a-b);const n=f.length,avg=f.reduce((a,b)=>a+b,0)/n;
return {frames:n,avg_ms:+avg.toFixed(1),fps:+(1000/avg).toFixed(1),p95_ms:+f[Math.floor(n*.95)].toFixed(1),jank_pct:+(100*f.filter(x=>x>33.4).length/n).toFixed(1)}}"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--enable-gpu-rasterization'])
    for pg in pages:
        ctx = b.new_context(viewport={'width': 393, 'height': 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True)
        page = ctx.new_page(); cdp = ctx.new_cdp_session(page); cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        page.goto(f'{base}/{pg}.html', wait_until='load'); page.wait_for_timeout(800)
        cdp.send('Performance.enable'); m0 = {x['name']: x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
        b.start_tracing(page=page, categories=['devtools.timeline', 'disabled-by-default-devtools.timeline', 'cc', 'gpu'])
        r = page.evaluate(JS)
        tr = json.loads(b.stop_tracing())
        m1 = {x['name']: x['value'] for x in cdp.send('Performance.getMetrics')['metrics']}
        for k in ('TaskDuration', 'LayoutDuration', 'RecalcStyleDuration', 'ScriptDuration'): r[k + '_ms'] = round((m1[k] - m0[k]) * 1000)
        ev = tr['traceEvents'] if isinstance(tr, dict) else tr
        agg = {}
        for e in ev:
            if e.get('ph') == 'X' and e.get('name') in ('Paint', 'RasterTask', 'PaintImage', 'UpdateLayerTree', 'Layerize', 'Layout'):
                agg[e['name']] = agg.get(e['name'], 0) + e.get('dur', 0) / 1000
        r['trace_ms'] = {k: round(v) for k, v in agg.items()}
        out[pg] = r; print(pg, out[pg], flush=True); ctx.close()
    b.close()
if len(sys.argv) > 1: json.dump(out, open('/tmp/scrollperf.json', 'w'))
