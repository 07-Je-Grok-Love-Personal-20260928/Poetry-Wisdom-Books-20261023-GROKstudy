/* 诗歌智慧书 · 地图：三视图切换、情景讲解播放、实时地图（本地 Leaflet + 多图源自动切换） */
(function(){
var d=document,$=function(s,c){return (c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
var SRC=[
 {id:'esri-topo',n:'Esri 地形街道',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',a:'Tiles © Esri — Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS',mx:18},
 {id:'osm',n:'OpenStreetMap',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',a:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',mx:19},
 {id:'gaode',n:'高德地图（中文·国内可用）',u:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',s:'1234',a:'© 高德地图 AutoNavi',mx:18},
 {id:'carto',n:'CARTO Voyager',u:'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',s:'abcd',a:'© OpenStreetMap contributors © CARTO',mx:19},
 {id:'esri-img',n:'Esri 卫星影像',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',a:'Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics',mx:18},
 {id:'otm',n:'OpenTopoMap 等高线',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',s:'abc',a:'© OpenStreetMap contributors, SRTM | © OpenTopoMap (CC-BY-SA)',mx:17},
 {id:'dare',n:'古代世界地图（DARE）',u:'https://dh.gu.se/tiles/imperium/{z}/{x}/{y}.png',a:'© Johan Åhlfeldt, Digital Atlas of the Roman Empire (CC BY 4.0)',mx:11},
 {id:'natgeo',n:'Esri 国家地理风格',u:'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',a:'Tiles © Esri — National Geographic, Esri, DeLorme, NAVTEQ',mx:16},
 {id:'gaode-sat',n:'高德卫星（国内可用）',u:'https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',s:'1234',a:'© 高德地图 AutoNavi',mx:18},
 {id:'s2',n:'Sentinel-2 无云影像（EOX）',u:'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless-2020_3857/default/g/{z}/{y}/{x}.jpg',a:'Sentinel-2 cloudless — s2maps.eu by EOX IT Services GmbH (Copernicus Sentinel data 2020)',mx:15},
 {id:'phys',n:'Esri 自然地貌',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',a:'Tiles © Esri — US National Park Service',mx:8},
 {id:'nasa',n:'NASA 蓝色弹珠',u:'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief_Bathymetry/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg',a:'NASA Earth Observatory / GIBS',mx:8},
 {id:'hot',n:'OSM 人道主义风格',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',s:'abc',a:'© OpenStreetMap contributors, Tiles: HOT / OSM France',mx:19},
 {id:'carto-dark',n:'CARTO 暗色',u:'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',s:'abcd',a:'© OpenStreetMap contributors © CARTO',mx:19}
];
window.PW_TILE_SOURCES=SRC;
var LP=null;
function loadLeaflet(){if(window.L)return Promise.resolve();if(LP)return LP;
 LP=new Promise(function(res,rej){var c=d.createElement('link');c.rel='stylesheet';c.href='assets/vendor/leaflet/leaflet.css';d.head.appendChild(c);
  var s=d.createElement('script');s.src='assets/vendor/leaflet/leaflet.js';s.onload=function(){res()};s.onerror=function(){LP=null;rej(new Error('leaflet'))};d.head.appendChild(s)});return LP}
function initLive(f){if(f._lm)return;var data=JSON.parse(f.dataset.live),box=$('.lmap',f),bar=$('.lsrc',f),st=$('.lstat',f);
 loadLeaflet().then(function(){
  if(f._lm)return;box.innerHTML='';
  var m=L.map(box,{zoomControl:true,attributionControl:true,scrollWheelZoom:false,tap:true,preferCanvas:true,worldCopyJump:true});f._lm=m;
  var b=L.latLngBounds([data.b[0],data.b[1]],[data.b[2],data.b[3]]);m.fitBounds(b,{padding:[10,10]});
  var pts=data.m.map(function(p,i){var ll=[p.la,p.lo];
   if(p.u)L.circle(ll,{radius:22000,color:p.c,weight:2,dashArray:'5 5',fillOpacity:.08}).addTo(m);
   L.marker(ll,{icon:L.divIcon({className:'lm-pin',html:'<b style="--c:'+p.c+'">'+(i+1)+'</b>',iconSize:[26,26],iconAnchor:[13,13]}),title:p.n,keyboard:true})
    .bindPopup('<b>'+(i+1)+'. '+p.n+'</b>'+(p.u?'<em>（位置不确定）</em>':'')+'<br>'+p.t,{maxWidth:280}).addTo(m);return ll});
  data.r.forEach(function(r){var a=pts[r[0]-1],c=pts[r[1]-1],k=r[3],line=[];var mla=(a[0]+c[0])/2+(c[1]-a[1])*k,mlo=(a[1]+c[1])/2-(c[0]-a[0])*k;
   for(var t=0;t<=1.0001;t+=.05){var u=1-t;line.push([u*u*a[0]+2*u*t*mla+t*t*c[0],u*u*a[1]+2*u*t*mlo+t*t*c[1]])}
   L.polyline(line,{color:r[2],weight:3,dashArray:'8 6',opacity:.9}).addTo(m)});
  var reset=L.control({position:'topright'});reset.onAdd=function(){var x=L.DomUtil.create('button','lm-reset');x.type='button';x.title='重置视野';x.textContent='⤾';L.DomEvent.on(x,'click',function(e){L.DomEvent.stop(e);m.fitBounds(b,{padding:[10,10]})});return x};reset.addTo(m);
  var cur=null,tried={},order=SRC.map(function(_,i){return i});
  var pref=store('pw-tile');if(pref){var pi=SRC.findIndex(function(s){return s.id===pref});if(pi>0){order.splice(order.indexOf(pi),1);order.unshift(pi)}}
  SRC.forEach(function(s,i){var bt=d.createElement('button');bt.type='button';bt.className='ls';bt.dataset.i=i;bt.textContent=s.n;bt.onclick=function(){tried={};use(i,true)};bar.appendChild(bt)});
  function mark(i,cls){var bt=$('.ls[data-i="'+i+'"]',bar);if(!bt)return;bt.classList.remove('on','fail','ok');if(cls)bt.classList.add(cls)}
  function next(reason){var cand=order.filter(function(i){return !tried[i]});if(!cand.length){st.innerHTML='⚠️ 所有实时底图暂时无法载入（可能离线或网络受限）。请改看 <b>🎨 情景讲解图</b> 或 <b>🗺️ 地形图（离线）</b>，地点、说明完全相同。';return}
   var nx=cand[0];st.textContent='⏳ '+SRC[cur].n+' '+reason+'，自动切换到：'+SRC[nx].n;use(nx,false)}
  function use(i,manual){if(f._tl){m.removeLayer(f._tl);clearTimeout(f._to)}cur=i;tried[i]=1;var s=SRC[i],ok=0,err=0,done=false;
   $$('.ls',bar).forEach(function(x){x.classList.remove('on')});mark(i,'on');
   var tl=L.tileLayer(s.u,{subdomains:s.s||'abc',maxZoom:19,maxNativeZoom:s.mx,attribution:s.a,crossOrigin:false,detectRetina:false});f._tl=tl;
   tl.on('tileload',function(){ok++;if(!done&&ok>=2){done=true;clearTimeout(f._to);st.textContent='✅ 当前底图：'+s.n+(manual?'':'（自动选择）')+' · 可点上方按钮切换来源';store('pw-tile',s.id);var bt=$('.ls[data-i="'+i+'"]',bar);if(bt)bt.classList.add('ok')}});
   tl.on('tileerror',function(){err++;if(!done&&err>=4&&ok===0){done=true;clearTimeout(f._to);mark(i,'fail');next('载入失败')}});
   f._to=setTimeout(function(){if(!done&&ok===0){done=true;mark(i,'fail');next('超时')}},manual?12000:7000);
   tl.addTo(m);st.textContent='⏳ 正在载入：'+s.n+'…'}
  if(navigator.onLine===false){st.innerHTML='📴 当前离线：实时底图不可用，请看情景讲解图或地形图。';}
  use(order[0],false);
  f._invalidate=function(){m.invalidateSize();};
 }).catch(function(){box.innerHTML='<div class="lph">⚠️ 地图组件载入失败，请改看情景讲解图或地形图。</div>'})}
window.PW_initLive=initLive;
// 视图切换
$$('.mapfig').forEach(function(f){
 $$('.mt',f).forEach(function(b){b.onclick=function(){var v=b.dataset.v;$$('.mt',f).forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});
  $$('.mview',f).forEach(function(x){x.classList.toggle('on',x.classList.contains('v-'+v))});store('pw-mapview',v);
  var tp=$('.v-'+v+' template.lazyv',f);if(tp){tp.parentNode.appendChild(tp.content.cloneNode(true));tp.remove();bindPts(f)}
  if(v==='live'){initLive(f);if(f._invalidate)setTimeout(f._invalidate,30)}}});
 // 图例联动（情景图 + 地形图）
 bindPts(f)});
function bindPts(f){
 function on(i){$$('.m-pt,.sc-pt',f).forEach(function(p){p.classList.toggle('on',p.dataset.i===i)});$$('.map-legend li,.st-steps li',f).forEach(function(l){l.classList.toggle('on',l.dataset.i===i)})}
 $$('.map-legend li',f).forEach(function(l){l.onclick=function(){on(l.dataset.i)}});
 $$('.m-pt,.sc-pt',f).forEach(function(p){p.onclick=function(){on(p.dataset.i)}});
 f._on=on}
$$('.mapfig').forEach(function(f){var on=function(i){f._on(i)};
 // 情景讲解播放器
 var steps=$$('.st-steps li',f),k=-1,tm=null,play=$('.st-play',f),cnt=$('.st-n',f);
 function go(n){if(!steps.length)return;k=(n+steps.length)%steps.length;steps.forEach(function(s,j){s.classList.toggle('cur',j===k)});on(steps[k].dataset.i);var ol=steps[k].parentNode;ol.scrollTo({left:steps[k].offsetLeft-ol.offsetLeft-4,behavior:'smooth'});cnt.textContent=(k+1)+' / '+steps.length}
 function stop(){clearInterval(tm);tm=null;play.textContent='▶ 播放讲解';f.classList.remove('playing')}
 $$('.st-b',f).forEach(function(b){b.onclick=function(){var a=b.dataset.a;if(a==='prev'){stop();go(k-1)}else if(a==='next'){stop();go(k+1)}else{if(tm){stop()}else{f.classList.add('playing');play.textContent='⏸ 暂停';go(k+1);tm=setInterval(function(){go(k+1)},3800)}}}});
 steps.forEach(function(s,j){s.onclick=function(){stop();go(j)}});
});
// 滚动到附近才预载 Leaflet；用户上次选“实时地图”则进入视口时自动初始化
if('IntersectionObserver' in window){var pref=store('pw-mapview');
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var f=e.target;io.unobserve(f);
  var idle=window.requestIdleCallback||function(cb){setTimeout(cb,400)};idle(function(){loadLeaflet().catch(function(){})});
  if(pref==='live'){var b=$('.mt[data-v="live"]',f);if(b)b.click()}})},{rootMargin:'300px 0px'});
 $$('.mapfig').forEach(function(f){io.observe(f)});
 // 动画只在可见时运行
 var vio=new IntersectionObserver(function(es){es.forEach(function(e){var t=e.target;t.classList.toggle('live',e.isIntersecting);if(t.pauseAnimations){try{e.isIntersecting?t.unpauseAnimations():t.pauseAnimations()}catch(_){}}})},{rootMargin:'100px 0px'});
 $$('.mapfig svg,.anim,.dg').forEach(function(x){vio.observe(x)});
}
})();
