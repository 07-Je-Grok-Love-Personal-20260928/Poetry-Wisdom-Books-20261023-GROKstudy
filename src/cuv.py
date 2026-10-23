# -*- coding: utf-8 -*-
"""和合本（新标点，简体）经文：从信望爱站 FHL API 取得并缓存；构建时逐字使用，不手打经文。"""
import json, os, urllib.request, urllib.parse, time
C = os.path.join(os.path.dirname(__file__), '..', 'data', 'cuv.json')
cache = json.load(open(C)) if os.path.exists(C) else {}
def _get(bk, ch, sec):
    key = f"{bk}{ch}:{sec}"
    if key in cache: return cache[key]
    u = "https://bible.fhl.net/json/qb.php?" + urllib.parse.urlencode({"chineses": bk, "chap": ch, "sec": sec, "gb": 1})
    for i in range(4):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read().decode('utf8')); break
        except Exception as e:
            print('retry',key,e); time.sleep(2)
    else: raise RuntimeError(key)
    recs = [(r['sec'], r['bible_text'].strip()) for r in d['record']]
    assert recs, key
    cache[key] = recs
    json.dump(cache, open(C, 'w'), ensure_ascii=False, indent=0)
    return recs
def verse(bk, ch, sec):
    """返回 (引用字符串, 经文)；多节以空格连接。"""
    recs = _get(bk, ch, str(sec))
    return recs
