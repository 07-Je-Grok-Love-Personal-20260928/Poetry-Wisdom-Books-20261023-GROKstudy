"""v4.3 截图：python3 tools/shots43.py BASE tag [pid:anchor,...] ——每个锚点滚到位置、等图表懒渲染后截一屏；加 :day 用浅色主题"""
import sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; tag = sys.argv[2]; out = '/workspace/shots/v43'
SP = [x.split(':') for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for w, h in ((390, 844), (1440, 900)):
        for it in SP:
            pid, a = it[0], it[1]; day = len(it) > 2
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            if day: pg.add_init_script("try{localStorage.setItem('pw-theme','day')}catch(e){}")
            pg.goto(f'{BASE}/{pid}.html' + (f'#{a}' if a else '')); pg.wait_for_timeout(1800)
            pg.screenshot(path=f'{out}/{tag}-{pid}-{a or "top"}{"-day" if day else ""}-{w}.png'); pg.close()
