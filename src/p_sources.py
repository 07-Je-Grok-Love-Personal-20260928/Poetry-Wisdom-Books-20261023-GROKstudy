# -*- coding: utf-8 -*-
from lib import *
from shell import S, H3, hero
def L(u, t=None): return f'<a href="{u}" target="_blank" rel="noopener">{t or u}</a>'
def build():
    hr = hero('🔗', '来源与方法', '引用原则 · 资料来源 · 版本记录', '本站所有信条、信经与 CCI 讲章的引文均逐字取自 ccifellowship.org；经文取自和合本（新标点）；无法逐字核实的内容一律标注为“本站概述”。',
              [(f'版本 {VERSION}', '#3ddc97'), (f'日期 {DATE}', '#f5b83d'), ('GROKstudy', '#b48cff')])
    m = []
    m.append(S('o-rule', '📏', '引用原则',
        grid(card('信条与信经：逐字', '三大信经、海德堡要理问答、比利时信条、多特信经的引文全部取自 CCI 网站的抓取原文（JSON），生成页面时用程序检查每个摘录的起止文字确实存在于原文中；三大信经另外与在线页面逐段核对。', '📜', '#5ab0ff'),
             card('经文：和合本', '经文段落（引用框）由信望爱站（bible.fhl.net）API 取得和合本（新标点，简体），不手打。正文中的短引语为和合本文字。', '📖', '#3ddc97'),
             card('CCI 讲章与书籍', '摘录自 CCI 网站的讲章与《我属于主》《圣经故事》等，每段附原文链接。', '⛪', '#f5b83d'),
             card('其他资料：概述', '威斯敏斯特标准、其他改革宗教会与神学院的资料只作概述或链接，标明“本站概述”，不作原文引用。', '🏛️', '#b48cff'),
             card('不确定的事', '地理位置不确定者用虚线圈标示；学术上有争议的年代、作者问题列出不同观点。', '❔', '#ff9f43'),
             card('本站主题关联', '信条原文中没有引用、但本站认为有神学关联的地方，明确标注“本站主题关联”。', '🔗', '#ff7eb6'))))
    m.append(S('o-cci', '⛪', 'CCI（ccifellowship.org）原文来源',
        table(['内容', '链接'], [['使徒信经', L(CR['apostles']['url'])], ['尼西亚信经', L(CR['nicene']['url'])], ['亚他那修信经', L(CR['athanasian']['url'])],
                                ['海德堡要理问答', L('https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism')], ['比利时信条', L('https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession')],
                                ['多特信经', L(CD['url'])], ['讲章：约伯记19:25–27', L(INDEX['sermons_text_1.txt'][1])], ['讲章：约伯记2:13–3:1', L(INDEX['sermons_text_24.txt'][1])],
                                ['讲章：诗篇130', L(INDEX['sermons_text_25.txt'][1])], ['讲章：传道书7:15–19', L(INDEX['sermons_text_91.txt'][1])], ['讲章：创世记第3章（雅歌7:10）', L(INDEX['sermons_text_44.txt'][1])],
                                ['讲章：主日45-II（雅歌1:1–8）', L(INDEX['sermons_heidelberg-catechism_lord-day-45-2.txt'][1])], ['《我属于主》主日三十九、五十等', L(INDEX['books_i-belong_39.txt'][1]) + '；' + L(INDEX['books_i-belong_50.txt'][1])],
                                ['《圣经故事》第70章 荣辱兴衰', L(INDEX['books_bible-story_2_70.txt'][1])], ['《我属于主》主日四十九（约伯记）', L(INDEX['books_i-belong_49.txt'][1])]])))
    m.append(S('o-ref', '📚', '其他参考',
        table(['机构', '链接', '用途'], [
            ['中国改革宗教会（ccreformed.org）', L('https://www.ccreformed.org/'), '信仰立场；讲章（如诗篇130）'], ['改革宗初学者（reformedbeginner.net）', L('https://www.reformedbeginner.net/'), '约伯记导论、大公信经介绍'],
            ['加拿大归正教会（canrc.org）', L('https://canrc.org/'), '《赞美手册》、唱诗篇传统'], ['北美联合改革宗教会（urcna.org）', L('https://www.urcna.org/'), '信条'],
            ['传承改革宗（heritagereformed.com）', L('https://heritagereformed.com/'), '信条与教义'], ['美国基督教改革宗教会（prca.org）', L('https://prca.org/'), '圣约观（胡克码）'],
            ['正统长老会（opc.org）', L('https://www.opc.org/confessions.html'), '威斯敏斯特标准'], ['加拿大改革宗神学院（canadianreformedseminary.ca）', L('https://canadianreformedseminary.ca/'), '欧陆改革宗神学'],
            ['威斯敏斯特神学院（wts.edu）', L('https://www.wts.edu/'), '圣经神学传统'], ['加拿大归正神学院（crts.edu）', L('https://crts.edu/'), '欧陆改革宗神学'],
            ['信望爱站（bible.fhl.net）', L('https://bible.fhl.net/'), '和合本经文 API'], ['Natural Earth', L('https://www.naturalearthdata.com/'), '地图底图（公有领域）']])))
    m.append(S('o-ver', '🏷️', '版本记录',
        table(['版本', '日期（台北）', '说明'], [[VERSION, DATE, '首次发布：首页、整本圣经、五卷书各一页、信条对照、三大信经背诵版、信经对比、速记中心、来源页；12 幅以上 SVG 地图、时间线、思维导图、测验与翻卡。']]) +
        C('note', '纠错', '如发现引文与 CCI 原文或和合本不符，请以原文为准，并欢迎在 GitHub 仓库提出 issue。')))
    return hr, ''.join(m)
