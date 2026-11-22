(function(){
var d=document,h=d.documentElement,$=function(s,c){return (c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
// 目录开关
var wide=function(){return innerWidth>1100};
function tocToggle(){if(wide()){h.classList.toggle('toc-off');store('pw-toc',h.classList.contains('toc-off')?'0':'1')}else h.classList.toggle('toc-open')}
$('#tocbtn').onclick=tocToggle;$('#tocx').onclick=function(){if(wide()){h.classList.add('toc-off');store('pw-toc','0')}else h.classList.remove('toc-open')};
$('#scrim').onclick=function(){h.classList.remove('toc-open')};
$$('#toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())h.classList.remove('toc-open')})});
// 目录宽度：拖动右边缘（鼠标、触控、笔），记住宽度
var grip=$('#tocgrip'),TW0=300;
function maxW(){return wide()?Math.max(260,Math.min(820,innerWidth-520)):innerWidth}
function setW(w,save){w=Math.round(Math.max(220,Math.min(maxW(),w)));h.style.setProperty('--tocw',w+'px');if(grip){grip.setAttribute('aria-valuenow',w);grip.setAttribute('aria-valuemax',Math.round(maxW()))}if(save)store('pw-tocw',w);return w}
if(grip){var drag=false,sx=0,sw=0;
 grip.addEventListener('pointerdown',function(e){drag=true;sx=e.clientX;sw=$('#toc').getBoundingClientRect().width;h.classList.add('toc-drag');h.classList.remove('toc-full');try{grip.setPointerCapture(e.pointerId)}catch(_){}e.preventDefault()});
 var raf=0,lastX=0;grip.addEventListener('pointermove',function(e){if(!drag)return;lastX=e.clientX;if(!raf)raf=requestAnimationFrame(function(){raf=0;setW(sw+lastX-sx,false)})});
 function end(){if(!drag)return;drag=false;h.classList.remove('toc-drag');setW($('#toc').getBoundingClientRect().width,true)}
 grip.addEventListener('pointerup',end);grip.addEventListener('pointercancel',end);grip.addEventListener('lostpointercapture',end);
 grip.addEventListener('dblclick',function(){setW(TW0,true)});
 grip.addEventListener('keydown',function(e){var w=$('#toc').getBoundingClientRect().width;if(e.key==='ArrowRight'){setW(w+24,true);e.preventDefault()}if(e.key==='ArrowLeft'){setW(w-24,true);e.preventDefault()}});
 addEventListener('resize',function(){var w=+store('pw-tocw');if(w)setW(w,false)},{passive:true})}
$('#tocfull').onclick=function(){h.classList.toggle('toc-full')};
// 目录多级折叠：记住每页每项的展开状态
var tl=$('#toc .toc-list'),TK='pw-tocx:'+(tl?tl.dataset.pid:''),ost={};try{ost=JSON.parse(store(TK)||'{}')}catch(_){ost={}}
function setOpen(li,on,save){li.classList.toggle('open',on);var b=$('.tx',li);if(b)b.setAttribute('aria-expanded',on?'true':'false');if(save){ost[li.dataset.k]=on?1:0;store(TK,JSON.stringify(ost))}}
// 默认：各部分只显示一级；当前所在部分自动展开到二级（滚动时跟随）。用户手动展开／折叠的会记住
$$('#toc .toc-list li').forEach(function(li){if(!$('ol',li))return;var k=li.dataset.k;setOpen(li,k in ost?!!ost[k]:false,false)});
// 每个分支的“全部展开／收起”按钮（⊕／⊖）：只作用于该分支的所有下级
$$('#toc .toc-list li').forEach(function(li){if(!$('ol li ol',li))return;var tr=$('.tr',li),b=d.createElement('button');b.className='txa';b.type='button';b.title='展开／收起此项的全部下级';b.setAttribute('aria-label','展开或收起此项的全部下级');tr.appendChild(b);
 b.onclick=function(e){e.preventDefault();var sub=[li].concat($$('li',li).filter(function(x){return $('ol',x)}));var all=sub.every(function(x){return x.classList.contains('open')});sub.forEach(function(x){setOpen(x,!all,true)});upd()}});
var auto=[];(function(){var f=$('#toc .toc-list>li');if(f&&$('ol',f)&&!(f.dataset.k in ost)){setOpen(f,true,false);auto.push(f)}})();
function upd(){$$('#toc .txa').forEach(function(b){var li=b.closest('li');var all=[li].concat($$('li',li).filter(function(x){return $('ol',x)})).every(function(x){return x.classList.contains('open')});b.classList.toggle('on',all)})}upd();
$$('#toc .toc-list .tx').forEach(function(b){b.onclick=function(e){e.preventDefault();var li=b.closest('li');setOpen(li,!li.classList.contains('open'),true);upd()}});
$$('#toc .toc-lv button').forEach(function(b){b.onclick=function(){var lv=+b.dataset.lv;$$('#toc .toc-list li').forEach(function(li){if(!$('ol',li))return;var l=+li.className.match(/tl(\d)/)[1];setOpen(li,l<lv,true)});$$('#toc .toc-lv button').forEach(function(x){x.classList.toggle('on',x===b)});upd()}});
d.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.key==='t'||e.key==='T')$('#tocbtn').click();if(e.key==='l'||e.key==='L')h.classList.toggle('leg-on');if(e.key==='Escape'){h.classList.remove('toc-open');h.classList.remove('leg-on')}});
// 图例
$('#legbtn').onclick=function(e){e.stopPropagation();h.classList.toggle('leg-on')};$('#legx').onclick=function(){h.classList.remove('leg-on')};
d.addEventListener('click',function(e){if(h.classList.contains('leg-on')&&!e.target.closest('#legpop,#legbtn'))h.classList.remove('leg-on')});
d.addEventListener('visibilitychange',function(){h.classList.toggle('hidden-tab',d.hidden)});
// 视频：点击后才载入（不拖慢页面）
d.addEventListener('click',function(e){var b=e.target.closest('.media button');if(!b)return;var f=d.createElement('iframe');f.src=b.dataset.src;f.title=b.dataset.title||'视频';f.allow='accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen';f.loading='lazy';f.referrerPolicy='strict-origin-when-cross-origin';b.replaceWith(f)});
// 主题与字号
$('#themebtn').onclick=function(){var t=h.dataset.theme==='day'?'night':'day';h.dataset.theme=t;store('pw-theme',t)};
function fs(dl){var c=parseFloat(getComputedStyle(h).getPropertyValue('--fs'))||17;c=Math.min(22,Math.max(14,c+dl));h.style.setProperty('--fs',c+'px');store('pw-fs',c)}
$('#fsm').onclick=function(){fs(-1)};$('#fsp').onclick=function(){fs(1)};
// 进度条 & 回顶部
var prog=$('#prog'),tt=$('#fab'),tick=false,ring=$('#fab .fab-ring circle');
var cssProg=window.CSS&&CSS.supports&&CSS.supports('animation-timeline','scroll()'),ttOn=false;
function onS(){var y=scrollY;if(!cssProg){var m=h.scrollHeight-innerHeight;prog.style.transform='scaleX('+(m>0?y/m:0)+')'}var o=y>240;if(o!==ttOn){ttOn=o;tt.classList.toggle('on',o)}if(ring&&h.classList.contains('fab-open')===false){var m2=h.scrollHeight-innerHeight;ring.style.strokeDashoffset=100-(m2>0?Math.round(y/m2*100):0)}tick=false}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(onS)}},{passive:true});onS();
// 右下角快速导航：返回／前进／顶部／底部／目录／首页；点 ⋯ 展开，点别处或滚动后自动收起
var fb=$('#fabt');function fab(on){h.classList.toggle('fab-open',on);fb.setAttribute('aria-expanded',on?'true':'false')}
fb.onclick=function(e){e.stopPropagation();fab(!h.classList.contains('fab-open'))};
d.addEventListener('click',function(e){if(h.classList.contains('fab-open')&&!e.target.closest('#fab'))fab(false)});
function go(y,bot){var c=scrollY,v=innerHeight;if(Math.abs(y-c)>v*2)scrollTo({top:bot?y-v*1.5:v*1.5,behavior:'instant'});scrollTo({top:bot?h.scrollHeight:0,behavior:sm});
 var n=0,t=setInterval(function(){n++;var dy=bot?h.scrollHeight-v-scrollY:scrollY;if(Math.abs(dy)<3||n>20){clearInterval(t);return}if(n%4===0)scrollTo({top:bot?h.scrollHeight:0,behavior:'instant'})},120)}
var sm=matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth';
$$('#fab [data-go]').forEach(function(b){b.addEventListener('click',function(e){var g=b.dataset.go;
 if(g==='back'){e.preventDefault();if(history.length>1)history.back();else location.href='index.html'}
 else if(g==='fwd'){e.preventDefault();history.forward()}
 else if(g==='top')go(0,0);
 else if(g==='bot')go(h.scrollHeight,1);
 else if(g==='toc'){e.stopPropagation();tocToggle()}
 if(g!=='home')fab(false)})});
// 滚动高亮：当前位置及其上级都高亮，上级自动展开（不改变保存的状态），目录自动滚到当前项
var links={},tin=$('#toc .toc-in');$$('#toc .toc-list a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
var curA=null;function act(a){if(a===curA)return;curA=a;$$('#toc a.act').forEach(function(x){x.classList.remove('act')});$$('#toc li.path').forEach(function(x){x.classList.remove('path')});
 a.classList.add('act');for(var li=a.closest('li');li;li=li.parentNode.closest('li')){li.classList.add('path');var pl=li.parentNode.closest('li');if(pl&&!(pl.dataset.k in ost)&&!pl.classList.contains('open')){setOpen(pl,true,false);auto.push(pl)}}auto=auto.filter(function(x){if(!x.classList.contains('path')&&!(x.dataset.k in ost)){setOpen(x,false,false);return false}return true});if(typeof upd==='function')upd();
 if(tin&&(h.classList.contains('toc-open')||wide()&&!h.classList.contains('toc-off'))){var r=a.getBoundingClientRect(),b=tin.getBoundingClientRect();if(r.top<b.top+40||r.bottom>b.bottom-40)tin.scrollTo({top:tin.scrollTop+r.top-b.top-b.height/3,behavior:'smooth'})}}
if('IntersectionObserver' in window){
 var vis2={};var io=new IntersectionObserver(function(es){es.forEach(function(e){vis2[e.target.id]=e.isIntersecting?e.target:null});var best=null,bt=1e9;for(var k in vis2){var el=vis2[k];if(!el)continue;var t=Math.abs(el.getBoundingClientRect().top);if(t<bt){bt=t;best=k}}if(best&&links[best])act(links[best])},{rootMargin:'-12% 0px -70% 0px'});
 Object.keys(links).forEach(function(id){var el=d.getElementById(id);if(el)io.observe(el)});
 var rv=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('inview');rv.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
 $$('.reveal,.anim').forEach(function(el){rv.observe(el)});
 var lv=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('live',e.isIntersecting)})},{rootMargin:'80px 0px'});
 $$('.anim,.dg').forEach(function(el){lv.observe(el)});
}else $$('.reveal,.anim,.dg').forEach(function(e){e.classList.add('inview','live')});
// 搜索（索引按需载入）
var q=$('#q'),qr=$('#qres'),sl=false;
function loadIdx(cb){if(window.PW_IDX)return cb();if(sl)return;sl=true;var s=d.createElement('script');s.src='assets/search.js';s.onload=function(){sl=false;cb();if(q.value)doQ()};d.head.appendChild(s)}
if(q){q.addEventListener('focus',function(){loadIdx(function(){})});q.addEventListener('input',function(){loadIdx(doQ)})}
function doQ(){var v=q.value.trim();qr.innerHTML='';if(!v)return;var n=0;PW_IDX.forEach(function(x){if(n<30&&(x.t.indexOf(v)>=0||x.pt.indexOf(v)>=0)){n++;var li=d.createElement('li');li.innerHTML='<a href="'+x.p+'#'+x.id+'"><small>'+x.pt+'</small>'+x.t.replace(/</g,'&lt;')+'</a>';qr.appendChild(li)}});if(!n)qr.innerHTML='<li style="font-size:13px;color:var(--mute);padding:4px 10px">无匹配标题</li>'}
// 翻转卡片
d.addEventListener('click',function(e){var f=e.target.closest('.flip');if(f)f.classList.toggle('on')});
// 测验
$$('.quiz').forEach(function(z){var sc=0;$$('.qz',z).forEach(function(qq){var ok=+qq.dataset.ok;$$('.qo button',qq).forEach(function(b){b.onclick=function(){if(qq.classList.contains('done'))return;qq.classList.add('done');var i=+b.dataset.i;if(i===ok){b.classList.add('ok');sc++}else{b.classList.add('no');$$('.qo button',qq)[ok].classList.add('ok')}$('.qscore b',z).textContent=sc}})})});
// 地图图例联动
$$('.mapfig').forEach(function(f){function on(i){$$('.m-pt',f).forEach(function(p){p.classList.toggle('on',p.dataset.i===i)});$$('.map-legend li',f).forEach(function(l){l.classList.toggle('on',l.dataset.i===i)})}
 $$('.map-legend li',f).forEach(function(l){l.onclick=function(){on(l.dataset.i)}});$$('.m-pt',f).forEach(function(p){p.onclick=function(){on(p.dataset.i);var l=$('.map-legend li[data-i="'+p.dataset.i+'"]',f);if(l)l.scrollIntoView({block:'nearest',behavior:'smooth'})}})});
// 朗读（Web Speech API）
function speak(t,btn){if(!('speechSynthesis' in window)){alert('此浏览器不支持朗读');return}var s=speechSynthesis;if(s.speaking){s.cancel();if(btn)btn.classList.remove('on');return}var u=new SpeechSynthesisUtterance(t);u.lang='zh-CN';u.rate=.92;u.onend=function(){if(btn)btn.classList.remove('on')};if(btn)btn.classList.add('on');s.speak(u)}
$$('[data-speak]').forEach(function(b){b.onclick=function(){var el=d.getElementById(b.dataset.speak);speak(el.innerText,b)}});
// 背诵工具
$$('.creed-box').forEach(function(box){var ps=$$('.creed p',box);
 var mode=function(m){ps.forEach(function(p,i){p.classList.toggle('hide',m==='all'?true:m==='odd'?i%2===1:false)})};
 $$('[data-mode]',box).forEach(function(b){b.onclick=function(){mode(b.dataset.mode)}});
 ps.forEach(function(p){p.onclick=function(){p.classList.toggle('hide')}});
 var ini=$('[data-init]',box);if(ini)ini.onclick=function(){ini.classList.toggle('on');ps.forEach(function(p){if(!p.dataset.full)p.dataset.full=p.innerHTML;if(ini.classList.contains('on')){p.innerHTML=p.textContent.replace(/([\u4e00-\u9fa5])([\u4e00-\u9fa5]*)/g,function(m,a,b){return '<b>'+a+'</b>'+b.replace(/./g,'＿')}).slice(0,2000)}else p.innerHTML=p.dataset.full})}});
// 悬停或触摸页面链接时预取该页（下一次点击几乎瞬开）
var pf={};function pre(u){if(pf[u]||!/\.html$/.test(u))return;pf[u]=1;var l=d.createElement('link');l.rel='prefetch';l.href=u;d.head.appendChild(l)}
d.addEventListener('pointerover',function(e){var a=e.target.closest&&e.target.closest('a[href$=".html"]');if(a&&a.host===location.host)pre(a.getAttribute('href'))},{passive:true});
d.addEventListener('touchstart',function(e){var a=e.target.closest&&e.target.closest('a[href$=".html"]');if(a)pre(a.getAttribute('href'))},{passive:true});
// 学习进度
var pid=(location.pathname.split('/').pop()||'index.html');var vis=JSON.parse(store('pw-vis')||'{}');vis[pid]=1;store('pw-vis',JSON.stringify(vis));
$$('.path a.card').forEach(function(a){if(vis[a.getAttribute('href')])a.insertAdjacentHTML('beforeend','<span class="done-mark">✔ 已读</span>')});
var pc=$('#pcount');if(pc)pc.textContent=Object.keys(vis).length;
})();
// 滚动时暂停 SVG 内的动画（SVG 子元素动画无法由 GPU 合成，滚动中暂停可避免每帧重绘），停止滚动 180ms 后恢复
(function(){var de=document.documentElement,t=null,on=false;
function svgs(f){document.querySelectorAll('svg.scene.live,svg.map.live,.anim.live svg,.dg.live svg,svg.anim.live,svg.dg.live').forEach(function(s){if(s.pauseAnimations){try{f?s.pauseAnimations():s.unpauseAnimations()}catch(_){}}})}
addEventListener('scroll',function(){if(!on){on=true;de.classList.add('scrolling');svgs(true)}clearTimeout(t);t=setTimeout(function(){on=false;de.classList.remove('scrolling');svgs(false)},180)},{passive:true})})();
// v4 灵修进度：勾选已读（本机保存）
(function(){var bx=document.querySelectorAll('.dchk input');if(!bx.length)return;var K='pw-dev',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(_){}
function up(){var n=0;bx.forEach(function(b){if(b.checked)n++});var c=document.getElementById('dcount'),br=document.getElementById('dbar');if(c)c.textContent=n;if(br)br.style.setProperty('--p',(n/bx.length).toFixed(4))}
bx.forEach(function(b){b.checked=!!st[b.dataset.k];b.addEventListener('change',function(){if(b.checked)st[b.dataset.k]=1;else delete st[b.dataset.k];try{localStorage.setItem(K,JSON.stringify(st))}catch(_){}up()})});up()})();
/* v4.1：带 # 的深链接——先让目标之前的 .sec 正常渲染（取消 content-visibility 估算高度），再精确跳到目标 */
(function(){function go(){var h=location.hash.slice(1);if(!h)return;var t;try{t=document.getElementById(decodeURIComponent(h))}catch(_){return}if(!t)return;
var ss=document.querySelectorAll('.sec');for(var i=0;i<ss.length;i++){ss[i].style.contentVisibility='visible';if(ss[i].contains(t)||(ss[i].compareDocumentPosition(t)&2))break}
t.scrollIntoView({behavior:'instant',block:'start'});requestAnimationFrame(function(){t.scrollIntoView({behavior:'instant',block:'start'})})}
if(document.readyState==='complete')go();else addEventListener('load',go);addEventListener('hashchange',go)})();
/* v4.2 阅读条：在阅读版页面显示当前部分与阅读进度 */
(function(){var ps=document.querySelectorAll('main>.part');if(!ps.length||!document.querySelector('.rd-u,.rd-g'))return;
var b=document.createElement('div');b.id='rbar';b.setAttribute('aria-hidden','true');b.innerHTML='<span class="rb-dot"></span><span class="rb-t"></span><span class="rb-p"></span><i class="rb-l"></i>';document.body.appendChild(b);
var t=b.querySelector('.rb-t'),pp=b.querySelector('.rb-p'),cur=null,tk=false,lastP=-1;
function up(){tk=false;var y=window.scrollY,h=document.documentElement.scrollHeight-innerHeight,hdr=110,c=null;
for(var i=0;i<ps.length;i++){if(ps[i].getBoundingClientRect().top<hdr)c=ps[i];else break}
var on=!!c&&y>200;b.classList.toggle('on',on);
if(c&&c!==cur){cur=c;t.textContent=(c.querySelector('.part-n')||{}).textContent+' · '+(c.querySelector('.part-t')||{}).textContent;b.style.setProperty('--rbc',getComputedStyle(c).getPropertyValue('--accent'))}
var p=h>0?Math.min(1,y/h):0,pc=Math.round(p*100);if(pc!==lastP){lastP=pc;pp.textContent=pc+'%';b.style.setProperty('--rp',p.toFixed(3))}}
addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(up)}},{passive:true});up()})();
/* v4.2 家庭灵修阅读版：展开日卡时再加载钥节与概述（assets/devread.json），减小首屏 HTML */
(function(){if(!document.querySelector('.dc-x[data-i]'))return;var P=null;
function load(){return P||(P=fetch('assets/devread.json').then(function(r){return r.json()}))}
document.addEventListener('toggle',function(e){var d=e.target;if(!d.open||!d.closest||!d.closest('.dc'))return;var x=d.querySelector('.dc-x[data-i]');if(!x||x.dataset.ok)return;
x.textContent='…';load().then(function(a){x.innerHTML=a[+x.dataset.i]||'';x.dataset.ok=1}).catch(function(){x.textContent='加载失败，请刷新重试。'})},true);
var hov=function(){load();removeEventListener('pointerover',hov)};addEventListener('pointerover',hov,{passive:true,once:true})})();
/* v4.3.0 图表：靠近视口才把 <template> 里的 SVG/HTML 放进来（IntersectionObserver）；无 IO 的浏览器直接渲染 */
(function(){var fs=document.querySelectorAll('figure.vz');if(!fs.length)return;
function r(f){var t=f.querySelector(':scope>template');if(!t)return;var c=f.querySelector('.vz-c');c.innerHTML='';c.appendChild(t.content.cloneNode(true));t.parentNode.removeChild(t);f.classList.add('on');
 var n=f.querySelector('.vz-net');if(n)net(n);if(f.querySelector('.vz-cal'))cal(f);f.querySelectorAll('figure.vz').forEach(function(g){if(io)io.observe(g);else r(g)})}
function net(svg){function hl(k,v){svg.classList.add('hl');svg.querySelectorAll('path').forEach(function(p){p.classList.toggle('on',p.getAttribute(k)===v)})}
 svg.querySelectorAll('.nd').forEach(function(g){var k=g.hasAttribute('data-l')?'data-l':'data-r',v=g.getAttribute(k);g.addEventListener('mouseenter',function(){hl(k,v)});g.addEventListener('focusin',function(){hl(k,v)});g.addEventListener('mouseleave',function(){svg.classList.remove('hl')})})}
function cal(f){var st={};try{st=JSON.parse(localStorage.getItem('pw-dev')||'{}')}catch(_){}var n=0,cs=f.querySelectorAll('.vz-cal a');cs.forEach(function(a){var on=!!st[a.dataset.k];a.classList.toggle('done',on);if(on)n++});var o=f.querySelector('.cal-done');if(o)o.textContent=n}
var io=null;if('IntersectionObserver' in window){io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);r(e.target)}})},{rootMargin:'600px 0px'});fs.forEach(function(f){if(!f.parentNode.closest('figure.vz,template'))io.observe(f)})}else fs.forEach(r);
function recal(){document.querySelectorAll('figure.vz.on').forEach(function(f){if(f.querySelector('.vz-cal'))cal(f)})}
document.addEventListener('change',function(e){if(e.target.closest&&e.target.closest('.dchk'))setTimeout(recal,0)});window.addEventListener('storage',function(e){if(e.key==='pw-dev')recal()});
window.addEventListener('beforeprint',function(){fs.forEach(r)})})();
