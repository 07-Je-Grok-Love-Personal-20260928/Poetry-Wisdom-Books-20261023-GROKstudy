# -*- coding: utf-8 -*-
import re, html
from lib import *
from shell import S, H3, hero
META = {'apostles': ('🕊️', '#5ab0ff', '约 2–4 世纪成形（以约主后 400 年罗马教会的信经为基础）', '洗礼时的信仰告白；西方教会', '三段：父 · 子 · 圣灵（与教会）'),
        'nicene': ('☀️', '#f5b83d', '325 年尼西亚会议／381 年君士坦丁堡会议', '东西方教会共同的大公信经', '三段，加强基督的神性与圣灵的神性'),
        'athanasian': ('🔥', '#b48cff', '约 5 世纪末–6 世纪上半叶，西方教会（作者不详）', '教导三位一体与基督二性的教义信经', '42 点：三位一体（3–28）＋基督论（29–42）')}
def lines(key):
    t = CR[key]['text']; out = []
    for para in t.split('\n\n'):
        if key == 'athanasian':
            parts = [p.strip() for p in re.split(r'(?=\b\d{1,2}\) )', para) if p.strip()]
            for p in parts:
                mm_ = re.match(r'(\d{1,2})\) (.*)', p, re.S)
                out.append((mm_.group(1), mm_.group(2)) if mm_ else ('', p))
        else:
            segs = re.findall(r'[^；]+；?', para)
            for s in segs: out.append(('', s.strip()))
        out.append(None)
    # verbatim reconstruction check
    if key != 'athanasian':
        rec = '\n\n'.join(''.join(s for _, s in grp) for grp in _groups(out))
        assert rec.replace(' ', '') == t.replace(' ', ''), key
    return out
def _groups(out):
    g = []; cur = []
    for x in out:
        if x is None: g.append(cur); cur = []
        else: cur.append(x)
    return g
def creed_box(key):
    ic, col, date, use, struct = META[key]; c = CR[key]
    body = ''
    for grp in _groups(lines(key)):
        body += '<div class="cg">' + ''.join(f'<p>{f"<span class=num>{n}</span>" if n else ""}{html.escape(s)}</p>' for n, s in grp) + '</div>'
    return (f'<div class="creed-box" style="--c:{col}"><div class="ctools">'
            f'<button class="btn" data-mode="all">📖 全文</button><button class="btn" data-mode="odd">🙈 隔行遮盖</button><button class="btn" data-mode="none">🫥 全部遮盖</button>'
            f'<button class="btn" data-init>🔤 首字提示</button><button class="btn" data-speak="cr-{key}">🔊 朗读</button><span class="tip">提示：点击任一行可单独遮盖／显示</span></div>'
            f'<div class="creed" id="cr-{key}"><h3 class="ctitle">{c["title"]}</h3>{body}</div>'
            f'<p class="src">原文逐字取自 CCI：<a href="{c["url"]}" target="_blank" rel="noopener">{c["url"]}</a>（构建前已与在线页面逐段核对）</p></div>')
def build():
    hr = hero('🕯️', '三大信经 · 背诵版', '使徒信经 · 尼西亚信经 · 亚他那修信经（CCI 中文原文）',
        '比利时信条第 9 条：“在这一教义上，我们甘愿接受《使徒信经》、《尼西亚信经》和《亚他拿修信经》，以及其他与它们不相悖，且受到教父们一致认可的信经。”',
        [('逐字取自 ccifellowship.org', '#3ddc97'), ('遮盖背诵 · 首字提示 · 朗读', '#f5b83d'), ('深度对比见“信经对比”页', '#b48cff')])
    m = []
    m.append(S('c-how', '🎯', '怎样使用背诵版',
        grid(card('① 全文朗读', '先按“朗读”听一遍，再出声读三遍。', '🔊', '#5ab0ff'), card('② 隔行遮盖', '遮住一半，凭记忆补出被遮的行。', '🙈', '#f5b83d'),
             card('③ 首字提示', '只显示每句的第一个字，其余用横线代替。', '🔤', '#3ddc97'), card('④ 全部遮盖', '完整默诵；点击任一行即可核对。', '🫥', '#b48cff')) +
        C('note', '原文与字体', '三篇信经的文字均逐字取自 CCI 网站（《赞美手册》信经页面），本站未作任何改动，只按分号或编号断行以便背诵。BC 9 写作“亚他拿修”，CCI 信经页面写作“亚他那修”，本站在引用时各按原文。')))
    for key, sid in (('apostles', 'c-ap'), ('nicene', 'c-ni'), ('athanasian', 'c-at')):
        ic, col, date, use, struct = META[key]; c = CR[key]
        intro = ''.join(f'<p>{html.escape(p)}</p>' for p in c.get('intro_text', []))
        m.append(S(sid, ic, c['title'],
            facts([('时间', date), ('用途', use), ('结构', struct), ('来源', f'<a href="{c["url"]}" target="_blank" rel="noopener">CCI《赞美手册》信经</a>')]) +
            creed_box(key) +
            f'<div class="conf cci"><div class="ch">📘 CCI 页面的介绍（原文）</div>{intro}<div class="cs"><a href="{c["url"]}" target="_blank" rel="noopener">— {c["url"]}</a></div></div>'))
    m.append(S('c-bc9', '📜', '为什么改革宗教会接受三大信经？',
        BCA(9, ('此外，我们必须清楚地看到三个位格', '且受到教父们一致认可的信经。'), refs=False) +
        '<p>海德堡要理问答第 22–23 问则直接把《使徒信经》作为“基督徒必须相信”的内容总结：</p>' + HCQ(22, refs=True) + HCQ(23) +
        C('key', '三大信经与三项联合信条的关系', '<ul class="tight"><li><b>三大信经</b>（大公信经）：古代教会共同的信仰，被东西方（亚他那修信经主要在西方）承认。</li><li><b>三项联合信条</b>：宗教改革后欧陆改革宗教会的信仰告白，<b>站在三大信经的基础上</b>进一步阐明救恩、教会与圣礼。</li><li>HC 第 24–58 问按使徒信经逐条讲解；BC 8–11 讲三位一体，第 9 条明确接受三大信经。</li></ul>') +
        '<p>👉 想看三篇信经的异同、所驳斥的异端，以及“为什么需要三篇”，请到 <a href="compare.html">信经对比</a> 页。</p>'))
    return hr, ''.join(m)
