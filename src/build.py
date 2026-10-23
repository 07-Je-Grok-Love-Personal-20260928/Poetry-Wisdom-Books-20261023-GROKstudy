# -*- coding: utf-8 -*-
import os, sys, json, shutil, importlib
sys.path.insert(0, os.path.dirname(__file__))
import lib, shell
OUT = os.path.join(os.path.dirname(__file__), '..', 'docs')
ACC = dict(index='#f5b83d', bible='#5ab0ff', job='#ff9f43', psalms='#3ddc97', proverbs='#f5b83d', eccl='#2fd3d3', song='#ff7eb6', confessions='#5ab0ff', creeds='#b48cff', compare='#ff6b6b', memory='#ff7eb6', sources='#a9b4c6')
MOD = dict(index='p_index', bible='p_bible', job='p_job', psalms='p_psalms', proverbs='p_proverbs', eccl='p_eccl', song='p_song', confessions='p_conf', creeds='p_creeds', compare='p_compare', memory='p_memory', sources='p_sources')
only = sys.argv[1:]
os.makedirs(OUT + '/assets', exist_ok=True)
for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'static')):
    shutil.copy(os.path.join(os.path.dirname(__file__), '..', 'static', f), OUT + '/assets/' + f)
for pid, _, _, _ in shell.PAGES:
    if only and pid not in only: continue
    try: mod = importlib.import_module(MOD[pid])
    except ModuleNotFoundError as e:
        print('skip', pid, e); continue
    hr, main = mod.build()
    open(f'{OUT}/{pid}.html', 'w').write(shell.page(pid, hr, main, ACC[pid]))
    print('built', pid, len(main))
if not only:
    open(OUT + '/assets/search.js', 'w').write('window.PW_IDX=' + json.dumps(shell.S_IDX, ensure_ascii=False) + ';')
    json.dump(sorted(set(lib.CUV_USED)), open(os.path.join(OUT, '..', 'data', 'cuv_used.json'), 'w'), ensure_ascii=False, indent=0)
open(OUT + '/.nojekyll', 'w').write('')

open(os.path.join(OUT,'404.html'),'w').write("""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 · 诗歌智慧书</title><link rel="stylesheet" href="assets/app.css"></head><body><main style="max-width:640px;margin:15vh auto;padding:24px;text-align:center"><div style="font-size:64px">📖</div><h1>找不到此页</h1><p>“你的话是我脚前的灯，是我路上的光。”（诗119:105）</p><p><a href="index.html">← 回到首页</a></p></main></body></html>""")
open(os.path.join(OUT,'netlify.toml'),'w').write("""[[headers]]\n  for = "/assets/*"\n  [headers.values]\n    Cache-Control = "public, max-age=3600"\n""")
