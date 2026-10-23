import html
# -*- coding: utf-8 -*-
import json, os, re
from lib import *
from shell import S, H3, hero
W = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'wref.json')))
BK = [('job', 'j', '🌪️ 约伯记', '#ff9f43'), ('psa', 'p', '🎼 诗篇', '#3ddc97'), ('pro', 'r', '🦉 箴言', '#f5b83d'), ('ecc', 'e', '🌫️ 传道书', '#2fd3d3'), ('song', 's', '🌹 雅歌', '#ff7eb6')]
def sent(t, n):
    i = t.find(f'^{n}')
    if i < 0: return None
    a = max(t.rfind('。', 0, i), t.rfind('\n', 0, i)) + 1
    b = t.find('。', i); b = len(t) if b < 0 else b + 1
    return ('……' if a > 0 else '') + t[a:b] + ('……' if b < len(t) else '')
def mark(html_, n): return html_.replace(f'<sup class="fn">{n}</sup>', f'<sup class="fn hit">{n}</sup>')
def item(e):
    kind, num, fn, ref = e
    if kind == 'HC':
        ld, q = HCQ_[num]
        return (f'<div class="conf hc"><div class="conf-h">📘 HC 主日{ld} · 第{num}问 <span class="tag">脚注 {fn}：{esc(ref)}</span></div>'
                f'<p class="q">{sup(q["question"])}</p><p class="a">{mark(sup(q["answer"]), fn)}</p>'
                f'<a class="src" href="https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
    if kind == 'BC':
        a = BCA_[num]; s_ = sent(a['text'], fn)
        return (f'<div class="conf bc"><div class="conf-h">📗 BC {esc(a["title"])} <span class="tag">脚注 {fn}：{esc(ref)}</span></div><p>{mark(sup(s_), fn)}</p>'
                f'<a class="src" href="{a["url"]}" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
    h, n = map(int, str(num).split('-')); hd = CD['heads'][h]; a = [x for x in hd['articles'] if x['number'] == n][0]
    t = a['text'].split('\n\n- ')[0]
    if fn: s_ = sent(t, fn)
    else:
        i = t.find(ref.strip('（）')); assert i >= 0, ref
        a0 = max(0, i - 90); s_ = ('……' if a0 else '') + t[a0:i + len(ref)] + '……'
    return (f'<div class="conf cd"><div class="conf-h">📕 CD {esc(hd["title"])} · {esc(a["title"])} <span class="tag">{("脚注 " + str(fn) + "：") if fn else "正文引用："}{esc(ref)}</span></div><p>{mark(sup(s_), fn)}</p>'
            f'<a class="src" href="{a["url"]}" target="_blank" rel="noopener">原文 · ccifellowship.org</a></div>')
def build():
    tot = {k: len(v) for k, v in W.items()}
    hr = hero('📜', '信条对照：五卷书在三项联合信条中', '海德堡要理问答 · 比利时信条 · 多特信经（CCI 中文原文）',
        '本页由程序检索 CCI 网站三项联合信条的全部经文脚注，列出每一处引用诗歌智慧书的地方，并附上对应的信条原文。',
        [(f'约伯记 {tot["job"]} 处', '#ff9f43'), (f'诗篇 {tot["psa"]} 处', '#3ddc97'), (f'箴言 {tot["pro"]} 处', '#f5b83d'), (f'传道书 {tot["ecc"]} 处', '#2fd3d3'), (f'雅歌 {tot["song"]} 处', '#ff7eb6')])
    m = []
    intro = ('<p class="lead">三项联合信条（Three Forms of Unity）是欧陆改革宗教会的信仰告白：<b>比利时信条</b>（1561，德·布雷斯）、<b>海德堡要理问答</b>（1563，乌尔西努与奥利维亚努）、<b>多特信经</b>（1618–1619，多特大会）。</p>' +
             table(['信条', '年代', '作者／来源', '结构', 'CCI 原文'], [
                 ['比利时信条（BC）', '1561', '圭多·德·布雷斯（殉道者）', '37 条', '<a href="https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession" target="_blank" rel="noopener">链接</a>'],
                 ['海德堡要理问答（HC）', '1563', '乌尔西努、奥利维亚努（腓特烈三世委托）', '52 主日 129 问：罪与愁苦 · 救赎 · 感恩', '<a href="https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism" target="_blank" rel="noopener">链接</a>'],
                 ['多特信经（CD）', '1618–1619', '多特大会（驳斥抗辩派五点）', '五项教义（第三、四项合并）', f'<a href="{CD["url"]}" target="_blank" rel="noopener">链接</a>']]) +
             C('ctx', 'CCI 对多特信经的介绍（原文）', esc(CD['intro'].split('\n\n')[0])) +
             stat([(tot['job'], '约伯记', '#ff9f43'), (tot['psa'], '诗篇', '#3ddc97'), (tot['pro'], '箴言', '#f5b83d'), (tot['ecc'], '传道书', '#2fd3d3'), (tot['song'], '雅歌', '#ff7eb6')]) +
             '<p class="note">统计方法：逐条扫描 CCI 网站 HC 129 问、BC 37 条、CD 全部条文的经文脚注（以及正文中的括号经文），匹配“伯／诗／箴／传／歌”书卷缩写。黄色高亮的上标即为引用该书卷的脚注位置。</p>')
    m.append(S('f-intro', '📘', '三项联合信条简介', intro + BCA(4, ('旧约圣经包括', '撒迦利亚书和玛拉基书。'))))
    for key, p, name, col in BK:
        es = W[key]
        if not es:
            body = C('note', '没有直接引用', '三项联合信条的 CCI 原文脚注中没有引用雅歌。BC 4 将雅歌列为正典；本站在 <a href="song.html#s-conf">雅歌页</a> 中以“本站主题关联”的方式连结 HC 1、HC 54、HC 108–109、BC 27。')
        else:
            groups = {}
            for e in es: groups.setdefault(e[0][:2], []).append(e)
            body = ''
            for g, lab in (('HC', '海德堡要理问答'), ('BC', '比利时信条'), ('CD', '多特信经')):
                if g in groups:
                    body += f'<details class="acc" {"open" if len(groups[g]) < 12 else ""}><summary>{lab}（{len(groups[g])} 处）</summary>' + ''.join(item(e) for e in groups[g]) + '</details>'
        m.append(S(f'f-{key}', name.split()[0], name.split()[1] + f'（{len(es)} 处）', body))
    import wm, re as _re
    ix = wm.index_refs(); BK5 = ['约伯记', '诗篇', '箴言', '传道书', '雅歌']
    PG = {'约伯记': ('job.html#j-wm', '约伯记'), '诗篇': ('psalms.html#p-wm', '诗篇'), '箴言': ('proverbs.html#r-wm', '箴言'), '传道书': ('eccl.html#e-wm', '传道书'), '雅歌': ('song.html#s-wm', '雅歌')}
    def snip(kind, no, sec, k):
        u = wm.unit(kind, no, sec); t = u.get('text', u.get('ans'))
        e = t.find(f'⟦{k}⟧'); b = t.rfind('⟧', 0, e) + 1
        b = max(b, e - 60); frag = _re.sub(r'⟦\d+⟧', '', t[b:e]).lstrip('，。；、：')
        if not wm.verified(frag): return '（此处条文未能与 PDF 逐字核对，从略）'
        return ('……' if b > 0 else '') + html.escape(frag)
    def tag(kind, no, sec):
        return f'{kind} {no}.{wm.CN2N[sec]}' if sec else f'{kind} {no}'
    cnt = [[f'<a href="{PG[b][0]}">{b}</a>'] + [str(sum(1 for e in ix[b] if e[0] == d)) for d in ('WCF', 'WLC', 'WSC')] + [f'<b>{len(ix[b])}</b>'] for b in BK5]
    body = ('<p>下面的索引列出威斯敏斯特信仰告白（WCF）、大要理问答（WLC）、小要理问答（WSC）的经文脚注中，凡引用这五卷书的地方。'
            '条文片段与脚注都是逐字摘录，出自 ' + f'<a href="{wm.RTF_URL}" target="_blank" rel="noopener">{wm.RTF_NAME}</a>' + '，并已用脚本与 PDF 原文逐字核对。各卷书的重点逐字引文见对应书卷页的“威斯敏斯特标准”一节。</p>' +
            table(['书卷', 'WCF 脚注', 'WLC 脚注', 'WSC 脚注', '合计'], cnt) +
            C('note', '统计口径', '按“脚注”计数：一条脚注只要提到该书卷就计 1 次（同一条脚注引用该书多处，也只计 1 次）。三项联合信条的统计见上文：雅歌在三项联合信条中没有被引用，但在西敏标准中被引用 6 次。'))
    for b in BK5:
        rows = ''.join(f'<li><span class="chip">{tag(e[0], e[1], e[2])} · 脚注 {e[3]}</span> <q class="cq">{snip(e[0], e[1], e[2], e[3])}</q> <span class="muted">→ {html.escape(e[4])}</span></li>' for e in ix[b])
        body += f'<details class="acc"{" open" if len(ix[b]) < 10 else ""}><summary>{b}（{len(ix[b])} 条脚注）</summary><ul class="tight">{rows}</ul></details>'
    body += H3('f-west-t', '主题对照（条目位置）', table(['主题', '三项联合信条', '威斯敏斯特标准（条目位置）'], [
            ['圣经正典', 'BC 4–7', 'WCF 1.2–1.3'], ['以经解经', 'BC 7', '<a href="bible.html#b-wm1">WCF 1.9</a>'], ['神的护理', 'HC 27–28；BC 13', '<a href="job.html#j-wm1">WCF 5.1</a>；<a href="proverbs.html#r-wm2">WSC 11</a>'],
            ['神的预旨', 'CD 第一项教义', '<a href="proverbs.html#r-wm1">WCF 3.1</a>'], ['行为之约与恩典之约', '（HC 6–11 隐含）；BC 14', '<a href="bible.html#b-wm2">WCF 7.2–7.3</a>（明确称“行为之约”）'],
            ['敬拜中唱诗篇', '多特教会法规第 69 条', '<a href="psalms.html#p-wm1">WCF 21.5</a>（“以感恩的心吟唱诗篇”）'], ['祷告', 'HC 116–129', '<a href="psalms.html#p-wm2">WSC 98</a>；<a href="psalms.html#p-wm3">WLC 186</a>'],
            ['人生的目的', 'HC 1', '<a href="eccl.html#e-wm1">WSC 1；WLC 1</a>'], ['基督三职', 'HC 31', 'WSC 23–26；WLC 42–45'], ['十诫', 'HC 92–115', 'WSC 41–81；WLC 91–148']]))
    body += C('note', '来源与引用规则', f'威斯敏斯特标准的中文引文一律逐字采用 <a href="{wm.RTF_URL}" target="_blank" rel="noopener">{wm.RTF_NAME}</a>（© 2024 RTF-USA，允许免费传播），每段引文都注明 PDF 页码。少数无法与 PDF 逐字核对的段落（WSC 4、WLC 109）本站没有引用。英文原文可参阅 <a href="https://www.opc.org/confessions.html" target="_blank" rel="noopener">opc.org</a>。')
    m.append(S('f-west', '🏛️', '威斯敏斯特标准索引（逐字，RTF 译本）', body))
    return hr, ''.join(m)
