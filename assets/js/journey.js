/* v11 讲解动画: a guided, video-like walk through each concept map. Only composited properties are animated
   (marker transform via WAAPI, progress bar scaleX); the trail polyline changes once per step. Nothing runs until the user presses play. */
(function(){
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
function J(fig){const pl=fig.nextElementSibling;if(!pl||!pl.classList.contains('jy'))return;
  const st=JSON.parse(fig.dataset.st),n=st.length,w=fig.querySelector('.cmw'),mk=fig.querySelector('.jym'),tr=fig.querySelector('.jyt polyline'),
    vb=fig.querySelector('.jyt').viewBox.baseVal,chips=[...pl.querySelectorAll('.jyk button')],caps=[...pl.querySelectorAll('.jyx p')],
    bar=pl.querySelector('.jybar i'),cnt=pl.querySelector('.jyn'),bp=pl.querySelector('.jyp');
  let i=0,on=false,play=false,tm=0,cur=null,vis=true;
  const xy=k=>[st[k][0]*w.clientWidth,st[k][1]*w.clientHeight],T=p=>`translate(${p[0].toFixed(1)}px,${p[1].toFixed(1)}px)`;
  function act(){if(on)return;on=true;fig.classList.add('jyon');cur=xy(0);mk.style.transform=T(cur)}
  function go(k,anim){act();k=(k+n)%n;const to=xy(k);
    if(anim!==false&&!RM&&cur){mk.animate([{transform:T(cur)},{transform:T(to)}],{duration:Math.min(1400,350+Math.hypot(to[0]-cur[0],to[1]-cur[1])*2.2),easing:'cubic-bezier(.45,0,.2,1)',fill:'forwards'})}
    mk.style.transform=T(to);cur=to;i=k;
    const sc=w.closest('.mxc');if(sc&&sc.scrollWidth>sc.clientWidth+4)sc.scrollTo({left:Math.max(0,to[0]-sc.clientWidth/2),behavior:RM?'auto':'smooth'});
    tr.setAttribute('points',st.slice(0,k+1).map(p=>(p[0]*vb.width).toFixed(0)+','+(p[1]*vb.height).toFixed(0)).join(' '));
    fig.querySelectorAll('.jyd').forEach((d,j)=>d.classList.toggle('dn',j<=k));
    chips.forEach((c,j)=>{c.setAttribute('aria-selected',j===k);if(j===k&&c.parentNode.scrollWidth>c.parentNode.clientWidth){const P=c.parentNode;P.scrollTo({left:c.offsetLeft-P.clientWidth/2+c.clientWidth/2,behavior:RM?'auto':'smooth'})}});
    caps.forEach((c,j)=>c.classList.toggle('on',j===k));bar.style.transform='scaleX('+((k+1)/n).toFixed(3)+')';cnt.textContent=(k+1)+' / '+n}
  function tick(){clearTimeout(tm);if(!play||!vis)return;tm=setTimeout(()=>{if(i>=n-1){stop();return}go(i+1);tick()},2800)}
  function stop(){play=false;clearTimeout(tm);bp.setAttribute('aria-pressed','false');bp.textContent=i>=n-1?'↻ 重新播放':'▶ 继续播放'}
  bp.addEventListener('click',()=>{if(play){stop();return}play=true;bp.setAttribute('aria-pressed','true');bp.textContent='⏸ 暂停';if(!on||i>=n-1)go(0,on);tick()});
  pl.querySelector('.jyb').addEventListener('click',()=>{stop();go(i-1)});pl.querySelector('.jyf').addEventListener('click',()=>{stop();go(i+1)});
  chips.forEach((c,j)=>c.addEventListener('click',()=>{stop();go(j)}));
  pl.querySelector('.jyk').addEventListener('keydown',e=>{if(!/^Arrow(Left|Right)$/.test(e.key))return;e.preventDefault();stop();go(i+(e.key==='ArrowRight'?1:-1));chips[i].focus()});
  if('IntersectionObserver' in window)new IntersectionObserver(es=>{vis=es[0].isIntersecting;if(vis)tick();else clearTimeout(tm)}).observe(fig);
  let rz=0;addEventListener('resize',()=>{if(!on)return;clearTimeout(rz);rz=setTimeout(()=>{cur=xy(i);mk.getAnimations().forEach(a=>a.cancel());mk.style.transform=T(cur)},150)},{passive:true});
}
function init(){document.querySelectorAll('.cmap[data-st]').forEach(J)}
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init);
})();
