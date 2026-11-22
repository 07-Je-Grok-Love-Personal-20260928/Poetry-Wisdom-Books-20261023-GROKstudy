import sys
from playwright.sync_api import sync_playwright
BASE=sys.argv[1]; tag=sys.argv[2]; out='/workspace/shots/v42'
SP=[('psalms-love-read',['','#r-c4','#r-p51']),('psalms-devotional-read',['','#dr-p23','#dr-a1'])]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w,h in ((390,844),(1440,900)):
        for pid,ancs in SP:
            for k,a in enumerate(ancs):
                pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
                pg.goto(f'{BASE}/{pid}.html{a}');pg.wait_for_timeout(1500)
                if pid.startswith('psalms-dev') and k==1:
                    pg.evaluate("document.querySelector('#dr-p23 + p + .dcg details').open=true");pg.wait_for_timeout(300)
                pg.screenshot(path=f'{out}/{tag}-{pid}-{w}-{k}.png');pg.close()
