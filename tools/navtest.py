import sys,json
from playwright.sync_api import sync_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8820'
PG=sys.argv[2] if len(sys.argv)>2 else 'psalms-devotional.html'
out=[]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
  for w,hgt,mob in [(360,740,True),(1280,800,False)]:
    pg=b.new_page(viewport={'width':w,'height':hgt},is_mobile=mob,has_touch=mob);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto(BASE+'/psalms.html');pg.goto(BASE+'/'+PG)
    pg.wait_for_load_state('load');pg.wait_for_timeout(400)
    r={}
    r['toc_vis_l1']=pg.evaluate("[...document.querySelectorAll('#toc .toc-list>li')].length")
    r['toc_open_default']=pg.evaluate("[...document.querySelectorAll('#toc .toc-list li.open')].length")
    r['txa']=pg.evaluate("document.querySelectorAll('#toc .txa').length")
    pg.click('#fabt');pg.wait_for_timeout(400)
    r['fab_btns_visible']=pg.evaluate("[...document.querySelectorAll('#fabm>*')].filter(e=>getComputedStyle(e).opacity>0.9).length")
    # fab inside viewport
    r['fab_box']=pg.evaluate("(()=>{const b=document.getElementById('fab').getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.right),Math.round(b.bottom)]})()")
    pg.click('#fabm [data-go=bot]');pg.wait_for_timeout(1500)
    r['at_bottom']=pg.evaluate("Math.abs(scrollY+innerHeight-document.documentElement.scrollHeight)<4")
    r['ring']=pg.evaluate("getComputedStyle(document.querySelector('#fab .fab-ring circle')).strokeDashoffset")
    r['collapsed_after']=pg.evaluate("!document.documentElement.classList.contains('fab-open')")
    pg.click('#fabt');pg.wait_for_timeout(300);pg.click('#fabm [data-go=top]');pg.wait_for_timeout(1500)
    r['at_top']=pg.evaluate("scrollY<4")
    pg.click('#fabt');pg.wait_for_timeout(300);pg.click('#fabm [data-go=toc]');pg.wait_for_timeout(500)
    r['toc_toggled']=pg.evaluate("document.documentElement.className")
    if mob: pg.evaluate("document.documentElement.classList.remove('toc-open')")
    else: pg.evaluate("document.documentElement.classList.remove('toc-off')")
    # per-branch expand
    pg.evaluate("document.querySelector('#toc .txa').click()")
    r['after_txa_open']=pg.evaluate("document.querySelectorAll('#toc .toc-list li.open').length")
    pg.click('#fabt');pg.wait_for_timeout(300);pg.click('#fabm [data-go=back]');pg.wait_for_load_state('load');pg.wait_for_timeout(300)
    r['back_url']=pg.url.split('/')[-1]
    pg.click('#fabt');pg.wait_for_timeout(300);pg.click('#fabm [data-go=fwd]');pg.wait_for_load_state('load');pg.wait_for_timeout(300)
    r['fwd_url']=pg.url.split('/')[-1]
    pg.click('#fabt');pg.wait_for_timeout(300);pg.click('#fabm [data-go=home]');pg.wait_for_load_state('load')
    r['home_url']=pg.url.split('/')[-1]; r['errs']=errs
    out.append((w,r)); print(w,json.dumps(r,ensure_ascii=False))
  b.close()
