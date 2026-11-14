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
function setW(w,save){w=Math.round(Math.max(220,Math.min(maxW(),w)));h.style.setProperty('--tocw',w+'px');if(save)store('pw-tocw',w);return w}
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
$$('#toc .toc-list li').forEach(function(li){if(!$('ol',li))return;var k=li.dataset.k,def=li.classList.contains('tl1');setOpen(li,k in ost?!!ost[k]:def,false)});
$$('#toc .toc-list .tx').forEach(function(b){b.onclick=function(e){e.preventDefault();var li=b.closest('li');setOpen(li,!li.classList.contains('open'),true)}});
$$('#toc .toc-lv button').forEach(function(b){b.onclick=function(){var lv=+b.dataset.lv;$$('#toc .toc-list li').forEach(function(li){if(!$('ol',li))return;var l=+li.className.match(/tl(\d)/)[1];setOpen(li,l<lv,true)});$$('#toc .toc-lv button').forEach(function(x){x.classList.toggle('on',x===b)})}});
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
var prog=$('#prog'),tt=$('#totop'),tick=false;
function onS(){var m=h.scrollHeight-innerHeight;prog.style.transform='scaleX('+(m>0?scrollY/m:0)+')';tt.classList.toggle('on',scrollY>600);tick=false}
addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(onS)}},{passive:true});onS();
tt.onclick=function(){scrollTo({top:0,behavior:'smooth'})};
// 滚动高亮：当前位置及其上级都高亮，上级自动展开（不改变保存的状态），目录自动滚到当前项
var links={},tin=$('#toc .toc-in');$$('#toc .toc-list a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
var curA=null;function act(a){if(a===curA)return;curA=a;$$('#toc a.act').forEach(function(x){x.classList.remove('act')});$$('#toc li.path').forEach(function(x){x.classList.remove('path')});
 a.classList.add('act');for(var li=a.closest('li');li;li=li.parentNode.closest('li'))li.classList.add('path');
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
