# -*- coding: utf-8 -*-
from lib import *
from shell import S, H3, hero
def L(u, t=None): return f'<a href="{u}" target="_blank" rel="noopener">{t or u}</a>'
def build():
    hr = hero('🔗', '来源与方法', '引用原则 · 资料来源 · 版本记录', '本站所有信条、信经与 CCI 讲章的引文均逐字取自 ccifellowship.org；威斯敏斯特标准逐字取自 RTF-USA 简体中文新版；经文取自和合本（新标点），每一处短引语都已用脚本核对。无法逐字核实的内容一律标注为“本站概述”。',
              [(f'版本 {VERSION}', '#3ddc97'), (f'日期 {DATE}', '#f5b83d'), ('GROKstudy', '#b48cff')])
    m = []
    m.append(S('o-rule', '📏', '引用原则',
        grid(card('信条与信经：逐字', '三大信经、海德堡要理问答、比利时信条、多特信经的引文全部取自 CCI 网站的抓取原文（JSON），生成页面时用程序检查每个摘录的起止文字确实存在于原文中；三大信经另外与在线页面逐段核对。', '📜', '#5ab0ff'),
             card('经文：和合本', '经文段落（引用框）由信望爱站（bible.fhl.net）API 取得和合本（新标点，简体），不手打。正文中的短引语为和合本文字。', '📖', '#3ddc97'),
             card('CCI 讲章与书籍', '摘录自 CCI 网站的讲章与《我属于主》《圣经故事》等，每段附原文链接。', '⛪', '#f5b83d'),
             card('威斯敏斯特标准：逐字（v1.1.0）', '威斯敏斯特信仰告白、大/小要理问答的引文逐字取自 RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，2024，PDF），每段注明 PDF 页码；生成页面时用程序逐字核对 PDF 原文，未通过核对的段落（WSC 4、WLC 109）不作引用。', '🏛️', '#b48cff'),
             card('其他资料：概述', '其他改革宗教会与神学院的资料只作概述或链接，标明“本站概述”，不作原文引用。', '🏫', '#2fd3d3'),
             card('引号的用法', '“……”加出处＝逐字引文（和合本、CCI、RTF 译本）；「……」或标注“意译／概括／本站译”＝转述，不是原文。v1.1.0 用脚本（tools/vcheck.py）把全站带出处的短引语逐一与和合本核对。', '❝', '#5ab0ff'),
             card('不确定的事', '地理位置不确定者用虚线圈标示；学术上有争议的年代、作者问题列出不同观点。', '❔', '#ff9f43'),
             card('本站主题关联', '信条原文中没有引用、但本站认为有神学关联的地方，明确标注“本站主题关联”。', '🔗', '#ff7eb6'))))
    m.append(S('o-cci', '⛪', 'CCI（ccifellowship.org）原文来源',
        table(['内容', '链接'], [['使徒信经', L(CR['apostles']['url'])], ['尼西亚信经', L(CR['nicene']['url'])], ['亚他那修信经', L(CR['athanasian']['url'])],
                                ['海德堡要理问答', L('https://ccifellowship.org/books/book-of-praise/confessions/heidelberg-catechism')], ['比利时信条', L('https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession')],
                                ['多特信经', L(CD['url'])], ['讲章：约伯记19:25–27', L(INDEX['sermons_text_1.txt'][1])], ['讲章：约伯记2:13–3:1', L(INDEX['sermons_text_24.txt'][1])],
                                ['讲章：诗篇130', L(INDEX['sermons_text_25.txt'][1])], ['讲章：传道书7:15–19', L(INDEX['sermons_text_91.txt'][1])], ['讲章：创世记第3章（雅歌7:10）', L(INDEX['sermons_text_44.txt'][1])],
                                ['讲章：主日45-II（雅歌1:1–8）', L(INDEX['sermons_heidelberg-catechism_lord-day-45-2.txt'][1])], ['《我属于主》主日三十九、五十等', L(INDEX['books_i-belong_39.txt'][1]) + '；' + L(INDEX['books_i-belong_50.txt'][1])],
                                ['《圣经故事》第70章 荣辱兴衰', L(INDEX['books_bible-story_2_70.txt'][1])], ['《我属于主》主日四十九（约伯记）', L(INDEX['books_i-belong_49.txt'][1])],
                                ['v2.0.0 新增：教会规章第55条 诗篇和赞美诗', L(INDEX['books_book-of-praise_church-order_iv-worship-sacraments-and-ceremonies_55.txt'][1])], ['v2.0.0 新增：讲章《神将聆听的耳受教的心赐给所罗门王》', L(INDEX['sermons_text_103.txt'][1])],
                                ['v2.0.0 新增：讲章《论八福（二）》（传道书7章）', L(INDEX['sermons_text_31.txt'][1])], ['v2.0.0 新增：讲章《生命的河》', L(INDEX['sermons_text_54.txt'][1])], ['v2.0.0 新增：《我属于主》主日三十五', L(INDEX['books_i-belong_35.txt'][1])]])))
    m.append(S('o-map', '🗺️', '地图与底图来源（v2.0.0）',
        '<p>'+('每幅地图有三种视图：🎨 情景讲解图（本站自绘的 SVG，离线可用，带讲解步骤）、🗺️ 地形图（Natural Earth 公有领域数据，离线）和 🌐 实时地图（Leaflet 1.9.4，已打包在本站 <code>assets/vendor/leaflet/</code>，BSD-2 许可）。实时地图提供 14 个瓦片来源，加载出错或超时会自动切换到下一个，并记住上次可用的来源。地点位置凡有争议者用虚线圈标示。')+'</p>' +
        table(['瓦片来源', '链接', '说明'], [
            ['Esri（World Topo / Imagery / NatGeo / Shaded Relief / Physical）', L('https://www.esri.com/'), '© Esri 及其数据提供方'], ['OpenStreetMap / Humanitarian (HOT)', L('https://www.openstreetmap.org/copyright'), '© OpenStreetMap 贡献者（ODbL）'],
            ['CARTO（Voyager / Dark Matter）', L('https://carto.com/attributions'), '© CARTO，数据 © OSM'], ['OpenTopoMap', L('https://opentopomap.org/'), 'CC BY-SA'],
            ['高德地图（道路 / 卫星）', L('https://www.amap.com/'), '中国大陆网络下可用'], ['DARE 罗马帝国数字地图集', L('https://dh.gu.se/dare/'), '哥德堡大学 Johan Åhlfeldt，CC BY 4.0；古代地名'],
            ['EOX Sentinel-2 cloudless', L('https://s2maps.eu/'), 'Sentinel-2 cloudless © EOX（含修改过的 Copernicus Sentinel 数据），CC BY-NC-SA 4.0'], ['NASA GIBS（Blue Marble）', L('https://earthdata.nasa.gov/gibs'), 'NASA EOSDIS GIBS，公有领域'],
            ['Leaflet', L('https://leafletjs.com/'), '开源地图库，BSD-2-Clause，本地打包'], ['Natural Earth', L('https://www.naturalearthdata.com/'), '离线地形图与情景图的海岸线、河流（公有领域）']])))
    m.append(S('o-mark', '🖍️', '标注系统（v2.0.0）',
        '<p>'+('全站正文使用统一的标注：粗体、颜色、底色、实线／虚线／波浪下划线与提示框，各有固定含义；点页面右上角的 🖍️ 或按 L 键可随时打开图例。标注只加在本站的讲解文字上，不加在经文、信条和 CCI 原文中，以免改变原文。首页“怎样使用”一节有完整图例和示例。')+'</p>'))
    m.append(S('o-books', '📚', '诗篇读本来源（v4.0.0 / v4.1.0）',
        table(['读本', '本站用法', '页面'], [
            ['《爱上诗篇》W. 罗伯特·戈弗雷 著，乔兰山以妲 译（英文原著 Learning to Love the Psalms, Reformation Trust, 2017）', '49 章逐章概括（本站文字）；各章「默想与讨论」题目摘自原书并注明', '<a href="psalms-love.html">爱上诗篇</a> · <a href="psalms-love-read.html">阅读版（52 章卡片）</a>'],
            ['《家庭灵修·诗篇》Peter H. Holtvlüwer 著，中文版 2018', '366 天的题目、经文与对读经文（原书篇目）；每篇一句核心为本站概括；钥节改用和合本显示', '<a href="psalms-devotional.html">家庭灵修</a> · <a href="psalms-devotional-read.html">阅读版（366 天卡片）</a>']]) +
        '<p>两本书的 PDF 由用户提供，只用于整理学习要点，仓库中不包含原书文件或全文。阅读版（v4.1.0 起；v4.2.0 精简改版）的核心、要点与概述均为本站原创转述，不复制原书文字，也不标原书页码；用 n-gram 重合检查对照原书文本，16 字以上的雷同片段只剩和合本经文、书名与原书讨论题。两书与改革宗信条的对照评注见各页「改革宗信条对照与评注」。</p>'))
    m.append(S('o-ref', '📚', '其他参考',
        table(['机构', '链接', '用途'], [
            ['中国改革宗教会（ccreformed.org）', L('https://www.ccreformed.org/'), '信仰立场；讲章（如诗篇130）'], ['改革宗初学者（reformedbeginner.net）', L('https://www.reformedbeginner.net/'), '约伯记导论、大公信经介绍'],
            ['加拿大归正教会（canrc.org）', L('https://canrc.org/'), '《赞美手册》、唱诗篇传统'], ['北美联合改革宗教会（urcna.org）', L('https://www.urcna.org/'), '信条'],
            ['传承改革宗（heritagereformed.com）', L('https://heritagereformed.com/'), '信条与教义'], ['美国基督教改革宗教会（prca.org）', L('https://prca.org/'), '圣约观（胡克码）'],
            ['RTF-USA《威斯敏斯特标准》简体中文新版（贾少彬 译，2024）', L('https://rtf-usa.com/wp-content/uploads/2024/08/RTF-Westminster-Standards-FINAL-DIGITAL.pdf', 'rtf-usa.com（PDF）'), '威斯敏斯特标准逐字引文的来源'], ['正统长老会（opc.org）', L('https://www.opc.org/confessions.html'), '威斯敏斯特标准英文原文'], ['加拿大改革宗神学院（canadianreformedseminary.ca）', L('https://canadianreformedseminary.ca/'), '欧陆改革宗神学'],
            ['威斯敏斯特神学院（wts.edu）', L('https://www.wts.edu/'), '圣经神学传统'], ['加拿大归正神学院（crts.edu）', L('https://crts.edu/'), '欧陆改革宗神学'],
            ['信望爱站（bible.fhl.net）', L('https://bible.fhl.net/'), '和合本经文 API'], ['Natural Earth', L('https://www.naturalearthdata.com/'), '地图底图（公有领域）']])))
    m.append(S('o-ver', '🏷️', '版本记录',
        table(['版本', '日期（台北）', '说明'], [['v4.2.0', '2026-11-22', '两个阅读版全面精简并重新设计：《爱上诗篇·阅读版》每章一张卡片——一句核心（荧光）、3–5 条平行短要点（编号）、一句指向基督、一句应用，细读脉络与原书讨论题默认收起；《家庭灵修·阅读版》每天一张卡片——题目、经文、一句不超过 60 字的核心，点开看和合本钥节与较长概述，按诗篇分组、附录按周分组。去掉全部原书页码标记。新设计：书页式阅读栏（约 40 字宽）、宋体标题、五卷各有颜色、章卡与部分标题卡、顶部「当前部分 + 阅读进度」条、实线／虚线／波浪线与荧光标注；手机版单栏。重新做 n-gram 版权检查。'], ['v4.1.0', '2026-11-21', '新增两个阅读版分页：《爱上诗篇·阅读版》按原书目录 52 个单元（推荐语、导论八章、五卷总论、30 章重点诗篇、结论五篇、后记与作者简介）逐一概述，注明原书页码，附要点、相关经文、指向基督、应用与原书讨论题；《家庭灵修·阅读版》366 天每天一段概述，附题目、经文与和合本钥节，勾选进度与篇目页共用。所有概述为本站原创转述，并用 n-gram 重合检查脚本对照原书文本，改写了较长的雷同片段。'], ['v4.0.0', '2026-11-19', '新增两个诗篇分页：《爱上诗篇》（戈弗雷）全书 49 章逐章导读（导论八章、五卷总论与大纲、30 章重点诗篇（32 篇）、最后五篇，附原书讨论题）；《家庭灵修·诗篇》（Holtvlüwer）366 天全部篇目（每篇一句核心、每天题目与和合本钥节、附录基督生平／节令／圣餐，可勾选进度）；两书都加了改革宗信条对照评注。右下角新增快速导航（返回、前进、顶部、底部、目录、首页）；目录默认只显示一级、当前部分自动展开到二级，每个分支可一键展开全部下级。'], ['v3.0.0', '2026-11-14', '目录全面改版：一级（带序号的“第X部分”）、二级、三级三层目录，每层可折叠并记住状态，可一键展开到 1／2／3 级；目录可左右拖动调宽（鼠标、触控、键盘方向键，双击还原，宽度会记住），长标题自动换行不截断；手机上为抽屉，可切换全宽；滚动时自动高亮当前位置。顺滑度：滚动监听改用 IntersectionObserver，进度条改用 CSS 滚动时间轴，悬停预取页面。新增朝圣之路地图（诗篇）与箴言作者地图，新增动画柱状图、“📌 必背”区块和年代数字标注。'], ['v2.1.0', '2026-11-14', '实时地图修正：最高缩放级较低的来源（DARE、Esri 自然地貌、NASA）改为放大显示原有瓦片，不再显示空白；自动选择时优先用能清晰显示当前缩放级的来源。精简重复内容：删去与“本质核心”重复的“一句话”提示框与一览表中的“核心／基督”两行、地图说明中每图重复的套话、图例中与讲解步骤相同的说明等。8 种宽度多轮检查全部通过；4 个地图页 × 14 个来源 × 2 种宽度逐一测试。'], ['v2.0.0', '2026-11-14', '全面优化：每卷新增“本质核心”一页总结（论点、关键词、为什么/是什么/怎么用、指向基督、故事线、钥节、口诀）；地图改为三种视图（情景讲解图带讲解步骤与动画、离线地形图、实时地图带 14 个瓦片来源并自动切换），新增乌斯/以东/阿拉伯商路、锡安与大卫王国、所罗门贸易、古代近东智慧（埃及至两河）等地图；统一的标注系统与图例；新配色；性能优化（减少毛玻璃、只用 GPU 动画、支持减少动态效果、脚本延迟加载、页面切换动画）；新增 5 段 CCI 原文摘录；8 种宽度（360–1920）多轮版面检查。'], ['v1.1.0', '2026-10-24', '经文核对与威斯敏斯特标准：用脚本把全站带出处的短引语与和合本逐字核对，修正用字差异（如“不致缺乏”“息灭”“甚么”），并把转述改为「」或标注意译／概括；在约伯记、诗篇、箴言、传道书、雅歌和整本圣经页新增威斯敏斯特标准逐字引文（RTF-USA 译本，注明 PDF 页码）；信条页新增逐字的威斯敏斯特经文脚注索引；三种宽度（390/768/1440）重新做版面检查。'], ['v1.0.0', '2026-10-23', '首次发布：首页、整本圣经、五卷书各一页、信条对照、三大信经背诵版、信经对比、速记中心、来源页；12 幅以上 SVG 地图、时间线、思维导图、测验与翻卡。']]) +
        C('note', '纠错', '如发现引文与 CCI 原文或和合本不符，请以原文为准，并欢迎在 GitHub 仓库提出 issue。')))
    return hr, ''.join(m)
