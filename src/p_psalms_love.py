# -*- coding: utf-8 -*-
"""v4.0.0：《爱上诗篇》（戈弗雷）逐章导读——本站概括 + 原书讨论题（注明出处）。"""
import json, os
from lib import *
from shell import S, H3, hero
import godfrey as G
from v3content import bars
QS = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'godfrey_questions.json')))
def qs_for(key):
    for c in QS:
        if c['h'] == key: return c['q']
    return []
def qbox(key):
    q = qs_for(key)
    if not q: return ''
    return ('<details class="gq"><summary>💬 默想与讨论（原书题目，' + str(len(q)) + ' 题）</summary><ol>' +
            ''.join(f'<li>{esc(x.split(".", 1)[1].strip() if "." in x[:3] else x)}</li>' for x in q) + '</ol><p class="src-n">— 摘自《爱上诗篇》相应章末</p></details>')
def stairs():
    """五卷书「阶梯」：从哀歌走向赞美（SVG，进入视口时逐级升起）"""
    cols = [b[3] for b in G.BOOKS]; ic = [b[4] for b in G.BOOKS]
    s = '<figure class="stairs reveal"><svg viewBox="0 0 600 260" role="img" aria-label="诗篇五卷：从哀歌走向赞美"><defs><linearGradient id="stg" x1="0" x2="1"><stop offset="0" stop-color="#ff6b6b"/><stop offset="1" stop-color="#f5b83d"/></linearGradient></defs>'
    for k in range(5):
        h = 50 + k * 38; x = 20 + k * 114
        s += (f'<g class="st" style="--d:{k * 0.12:.2f}s"><rect x="{x}" y="{230 - h}" width="104" height="{h}" rx="10" fill="{cols[k]}" opacity=".85"/>'
              f'<text x="{x + 52}" y="{222 - h + 30}" text-anchor="middle" font-size="22">{ic[k]}</text>'
              f'<text x="{x + 52}" y="{250}" text-anchor="middle" font-size="13" fill="currentColor">第{"一二三四五"[k]}卷 {G.BOOKS[k][1]}</text></g>')
    s += '<path d="M20 200 C200 190 380 120 580 30" fill="none" stroke="url(#stg)" stroke-width="3" stroke-dasharray="6 6" class="st-line"/>'
    s += '<text x="22" y="20" font-size="13" fill="currentColor">😢 哀歌多</text><text x="578" y="20" text-anchor="end" font-size="13" fill="currentColor">🎉 赞美满</text></svg>'
    s += '<figcaption>🪜 五卷书像五级台阶：前面哀歌多，越往后赞美越多，最后以诗150 的纯赞美结束（颜色＝各卷主题色）。</figcaption></figure>'
    return s
def build():
    hr = hero('💗', '爱上诗篇 · 戈弗雷导读', 'W. 罗伯特·戈弗雷《爱上诗篇》全书 49 章逐章精要',
        '八章导论教你怎样读诗篇；五卷书各有一个围绕「君王」的主题；30 篇重点诗篇默想；最后五篇对应五卷。本页为本站概括，讨论题取自原书。',
        [('信·委·危·慰·庆', '#ff7eb6'), ('读诗十问', '#5ab0ff'), ('49 章全覆盖', '#3ddc97'), ('← 返回诗篇', '#f5b83d')])
    m = []
    five = ''.join(f'<li style="--c:{b[3]}"><b>{b[4]} 第{"一二三四五"[b[0]-1]}卷（{b[1]}）</b> {b[2]}</li>' for b in G.BOOKS)
    m.append(S('l-core', '💎', '本质核心：这本书在讲什么',
        f'<p class="thesis">💎 诗篇是<b>君王</b>的诗歌——大卫的诗、大卫之子<span class="mk-christ">基督</span>的诗，也是在基督里的我们的诗。按五卷书的次序读，就会看见从<span class="mk-hard">哀歌</span>走向<span class="mk-key">赞美</span>的旅程。</p>' +
        facts([('书名', '《爱上诗篇》（Learning to Love the Psalms）'), ('作者', 'W. 罗伯特·戈弗雷（W. Robert Godfrey），教会史学者，西敏神学院（加州）荣休院长'), ('译者', '乔兰山以妲'),
               ('结构', '导论 8 章 → 五卷书各一章总论 + 重点诗篇 → 结论（诗146–150）→ 后记'), ('方法', '每章末有「默想与讨论」3 题，本页全部收录')]) +
        stairs() + '<ol class="five-k">' + five + '</ol>' +
        '<div class="must"><span class="must-tag">📌 必背</span>' + C('mem', '五卷主题口诀：信 · 委 · 危 · 慰 · 庆', '<span class="mk-mem">王<b>信</b>护理 → 王<b>委</b>身国度 → 王遇<b>危</b>机 → 王得安<b>慰</b> → 王<b>庆</b>祝拯救</span>') + '</div>' +
        bars('五卷各有多少篇', [(f'第{"一二三四五"[b[0]-1]}卷', n, b[3], b[2]) for b, n in zip(G.BOOKS, (41, 31, 17, 17, 44))], ' 篇') +
        C('note', '出处与本页做法', f'本页内容整理自{G.SRC}。各章要点是本站的概括（用「」表示转述），经文以和合本为准；「默想与讨论」题目摘自原书，便于小组使用。'), 'key'))
    body = ''
    for n, t, ic, summ, pts in G.INTRO:
        key = '第' + '一二三四五六七八'[n-1] + '章'
        body += H3(f'l-i{n}', f'{ic} 第 {n} 章 · {t}', f'<p>{summ}</p><ul class="pts">' + ''.join(f'<li>{p}</li>' for p in pts) + '</ul>' + qbox(key))
    m.append(S('l-intro', '📖', '导论八章：怎样读诗篇',
        flow([('📜', '大卫', '先问：这首诗对大卫和以色列意味着什么？', '#f5b83d'), ('👑', '基督', '再问：它怎样在大卫之子基督身上成全？', '#b48cff'), ('🙋', '我们', '最后问：对在基督里的我和教会意味着什么？', '#3ddc97')]) +
        mm('诗篇的主题网', [('大主题', '#f5b83d', ['神的良善与慈爱', '回应：信靠、赞美、感恩']), ('从属主题', '#ff6b6b', ['义人的罪性', '恶人亨通', '义人受苦', '苦难中仍有信心']),
                          ('诗歌形式', '#5ab0ff', ['平行体', '中心句（金字塔）', '交叉结构', '离合诗']), ('说话者', '#b48cff', ['大卫', '君王代表百姓', '基督', '在基督里的教会'])]) + body))
    for k, rng, theme, col, ic, intro, outline, chs in G.BOOKS:
        cn = '一二三四五'[k-1]
        ol = '<ol class="outl">' + ''.join(f'<li style="--c:{col}"><b>诗{r}</b><span>{t}</span></li>' for r, t in outline) + '</ol>'
        b = f'<p class="thesis" style="--c:{col}">{ic} <b>{theme}</b>（诗{rng}）</p><p>{intro}</p>' + '<h4 class="sub">🗂️ 本卷大纲（原书）</h4>' + ol + qbox(next((c["h"] for c in QS if c["h"].startswith(f"第{cn}卷")), ''))
        for ps, t, core, christ, app in chs:
            key = f'诗篇 {ps}' if ps not in (86, 88) else f'诗篇 {ps} 与 {ps+1}'
            if ps in (87, 89): key = None
            body = (f'<p>{core}</p><div class="gl3"><div class="gl-c"><b>✝️ 指向基督</b><span>{christ}</span></div><div class="gl-a"><b>🌱 应用</b><span>{app}</span></div></div>' + (qbox(key) if key else ''))
            b += H3(f'l-b{k}-{ps}', f'🎵 诗篇 {ps} · {t}', body)
        m.append(S(f'l-b{k}', ic, f'第{cn}卷 · {theme}', b))
    fin = '<div class="fin">' + ''.join(f'<div class="fin-r" style="--c:{G.BOOKS[b-1][3]}"><span class="fin-p">诗{p}</span><span class="fin-arrow">⟷</span><span class="fin-b">第{"一二三四五"[b-1]}卷</span><p>{x}<small>{y}</small></p></div>' for p, b, x, y in G.FINAL) + '</div>'
    m.append(S('l-final', '🎆', '结论：最后五篇对应五卷', '<p>作者指出：诗146–150 这五首「哈利路亚诗」逐一回应前面五卷的主题，使全书以赞美收束。</p>' + fin + qbox('最后五首诗篇') +
        ''.join(qbox(f'诗篇 {p}') for p in (146, 147, 148, 149, 150)) + C('key', '后记：继续的诗篇旅程', G.AFTER)))
    notes = ''.join(C(k, t, x) for k, t, x in G.NOTES)
    m.append(S('l-notes', '📜', '改革宗信条对照与评注', notes + C('cov', '相关信条', 'HC 1（唯一的安慰）、HC 26–28（护理）、BC 13（神的护理）、HC 116–129（祷告）、BC 37（最后审判）。诗篇的「护理」「祷告」「审判」主题与这些条目直接相关，原文见<a href="confessions.html">信条对照页</a>。')))
    m.append(S('l-mem', '🧠', '速记：一页记住这本书',
        cards_flip([('五卷主题', '信·委·危·慰·庆：护理的信心、国度的委身、应许的危机、信实的安慰、拯救的庆祝'), ('四种魅力', '美、深、全、满有基督'), ('五个难点', '译本、少用、复杂、学术、排序'),
                    ('四个从属主题', '义人有罪、恶人亨通、义人受苦、苦中有信'), ('读诗三问', '大卫 → 基督 → 我们'), ('诗19–26', '创造与罪 · 降临 · 进城 · 受难 · 复活 · 升天 · 五旬节 · 审判'),
                    ('诗87', '最伟大的宣教诗篇：万国生在锡安'), ('诗110', '王又是祭司；新约引用最多')]) +
        quiz('love', [('戈弗雷概括第三卷的主题是？', ['王对神护理的信心', '王对神应许的危机', '王庆祝神的拯救', '王对神国度的委身'], 1, '第三卷（73–89）：王对神应许的危机，以诗89 结束。'),
                      ('诗23 的「中心」是哪一句的意思？', ['我必不致缺乏', '你与我同在', '我要住在耶和华的殿中', '使我的福杯满溢'], 1, '希伯来诗常把重心放在中央：「因为你与我同在」。'),
                      ('作者称哪首为「最伟大的宣教诗篇」？', ['诗67', '诗87', '诗96', '诗117'], 1, '诗87：万国的人都被登记为生在锡安。'),
                      ('诗146–150 与五卷的关系是？', ['没有关系', '逐一对应五卷主题', '只对应第五卷', '对应摩西五经'], 1, '146↔第一卷 … 150↔第五卷。')]) +
        '<p class="back-l">➡️ 继续：<a href="psalms-devotional.html">家庭灵修 · 诗篇 366 天</a> · <a href="psalms.html">返回诗篇主页</a></p>'))
    return hr, ''.join(m)
