# -*- coding: utf-8 -*-
from lib import *
from shell import S, H3, hero, PAGES, LEGEND
def build():
    hr = hero('📖', '诗歌智慧书深度学习', '约伯记 · 诗篇 · 箴言 · 传道书 · 雅歌',
        '从整本圣经的圣约与救赎历史出发，以基督为中心，按照三项联合信条（海德堡要理问答、比利时信条、多特信经）和三大信经学习五卷诗歌智慧书。',
        [(f'{VERSION} · {DATE}', '#3ddc97'), ('🗺️ 地图三视图 · 🖍️ 笔记标记', '#ff7ac6'), ('欧陆改革宗 · 正统立场', '#5ab0ff'), ('信条原文逐字取自 CCI', '#f5b83d'), ('GROKstudy', '#b48cff')])
    m = []
    m.append(S('i-five', '📚', '五卷书一览',
        '<div class="big5">' + ''.join(f'<a class="b5" href="{h}.html" style="--c:{c}"><div class="e">{e}</div><b>{t}</b><small>{d}</small></a>' for h, e, t, d, c in [
            ('job', '🌪️', '约伯记', '苦 · 受苦中的敬畏', '#ff9f43'), ('psalms', '🎼', '诗篇', '祷 · 圣约的祷告本', '#3ddc97'), ('proverbs', '🦉', '箴言', '行 · 敬畏中的日常', '#f5b83d'),
            ('eccl', '🌫️', '传道书', '思 · 日光之下的虚空', '#2fd3d3'), ('song', '🌹', '雅歌', '爱 · 婚约之爱', '#ff7eb6')]) + '</div>' +
        C('mem', '总口诀', '<b>苦·祷·行·思·爱</b>：五卷书都指向基督。约伯记中的<b>中保</b>（伯9:33；19:25），诗篇中的<b>君王</b>（诗2；110），箴言中的<b>智慧</b>（箴8；林前1:24、30），传道书中胜过虚空的<b>盼望</b>（传12:13–14；罗8:20–21），雅歌中的<b>新郎</b>（弗5:32）。') +
        story_dg([('🌪️', '约伯记', '苦·受苦', '#ffa24c'), ('🎼', '诗篇', '祷·敬拜', '#34e3a4'), ('🦉', '箴言', '行·生活', '#ffc94d'), ('🌫️', '传道书', '思·意义', '#2ee0d6'), ('🌹', '雅歌', '爱·婚约', '#ff7ac6'), ('✝️', '基督', '都指向他', '#b69cff')], '五卷书一线') +
        stat([('5', '卷书', '#5ab0ff'), ('243', '章（42+150+31+12+8）', '#3ddc97'), ('111', '处信条脚注引用（按卷累计）', '#f5b83d'), ('3', '大信经背诵版', '#b48cff')])))
    m.append(S('i-path', '🧭', '学习路径',
        '<p>你已读过 <b id="pcount">0</b> / ' + str(len(PAGES)) + ' 页（记录只存在本机浏览器中）。</p><div class="path">' +
        ''.join(f'<a class="card" href="{p[0]}.html" style="--c:{c}"><span class="n">{i+1:02d}</span><b>{p[1]} {p[2]}</b><span>{p[3]}</span></a>'
                for i, (p, c) in enumerate(zip(PAGES, ['#5ab0ff', '#b48cff', '#ff9f43', '#3ddc97', '#f5b83d', '#2fd3d3', '#ff7eb6', '#5ab0ff', '#f5b83d', '#b48cff', '#3ddc97', '#8aa0b8']))) + '</div>'))
    m.append(S('i-how', '🖍️', '笔记标记图例：颜色就是记忆', 
        '<p class="lead">全站用<b>同一套</b>标记：看到颜色就知道这句话的“身份”。页面右上角 <span class="kbd">🖍️</span>（或按 <span class="kbd">L</span>）随时打开图例。</p>' + LEGEND +
        '<p>示例：约伯记的问题是<span class="mk-hard">「义人为何受苦」</span>，但书中真正的答案是<span class="mk-god">神的主权与护理</span>；朋友们的<span class="mk-sin">机械报应论</span>被神否定；约伯渴望的<span class="mk-christ">救赎主</span>就是基督；这一切都在<span class="mk-cov">恩典之约</span>之内（<span class="mk-conf">HC 27–28</span>；<span class="mk-conf">BC 13</span>）。口诀：<span class="mk-mem">苦·祷·行·思·爱</span>。乌斯地的位置<span class="mk-dash">不确定</span>。<span class="mk-app">今天就把一篇诗篇读成祷告。</span></p>' +
        C('note', '使用方法', '左侧（手机为左上角 ☰，按 <span class="kbd">T</span>）是可隐藏的详细目录；目录顶部可搜索全站标题；右上角可调字号、切换明暗主题。每张地图都有三种视图：<b>🎨 情景讲解图</b>（可离线、可播放讲解）、<b>🗺️ 地形图</b>（离线）、<b>🌐 实时地图</b>（14 个全球底图来源，失败自动换源）。') +
        C('key', '引用原则', '信条和信经的文字逐字取自 <a href="https://ccifellowship.org/" target="_blank" rel="noopener">ccifellowship.org</a>，威斯敏斯特标准逐字取自 RTF-USA 译本，经文取自和合本。“……”＋出处＝逐字；「……」＝转述。详见<a href="sources.html">来源与方法</a>。')))
    m.append(S('i-cov', '🤝', '为什么先看整本圣经？',
        flow([('🌱', '创造', '神借智慧创造世界（箴3:19；8:22–31）', '#3ddc97'), ('🐍', '堕落', '虚空与咒诅（传1:2；罗8:20）', '#ff6b6b'), ('🤝', '圣约', '敬畏耶和华的百姓（诗25:14）', '#5ab0ff'),
              ('👑', '基督', '神的智慧与受膏君王（林前1:24；诗2）', '#b48cff'), ('🌅', '成全', '新天新地，婚筵（启19:7；21:1）', '#f5b83d')]) +
        '<p>诗歌智慧书不是零散的格言和诗歌，而是圣约百姓在<b>创造—堕落—救赎—成全</b>的历史中如何受苦、祷告、生活、思考和相爱的书。<a href="bible.html">→ 先读“整本圣经视角”</a></p>'))
    return hr, ''.join(m)
