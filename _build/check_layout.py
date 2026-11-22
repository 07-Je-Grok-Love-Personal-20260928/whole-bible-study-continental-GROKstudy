# v12.2 layout checker: real-device profiles (WebKit iPhone + Edge iOS UA, Chromium Edge Android UA, desktop),
# main-content checks from check_overlap + NEW: narrow-stack (one-char columns), escape (content spilling out of a visible box),
# and opened panels (theme panel, nav dropdowns, TOC drawer, fab menu, legend) + hidden top-bar state. Repeats open/close.
# usage: PROFILES=wk375,wk390,wk430,a360,a390,a412,c768,c1024,c1280,c1440,c1920 THEMES=night python3 check_layout.py [pages|all]
import sys,os,json,collections,time
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from check_overlap import JS as JS1
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else [f for f in sorted(os.listdir(SITE)) if f.endswith('.html') and f not in ('nt.html','ot.html')]
EDGI='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/129.0.2792.84 Mobile/15E148 Safari/604.1'
SAF='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
EDGA='Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 EdgA/129.0.2792.84'
PROF={'wk375':('webkit',375,600,EDGI,3,True),'wk390':('webkit',390,664,EDGI,3,True),'wk390s':('webkit',390,844,SAF,3,True),'wk430':('webkit',430,739,EDGI,3,True),
 'a360':('chromium',360,680,EDGA,3,True),'a390':('chromium',390,700,EDGA,3,True),'a412':('chromium',412,760,EDGA,2.6,True),
 'c768':('chromium',768,1000,None,1,False),'c1024':('chromium',1024,768,None,1,False),'c1280':('chromium',1280,800,None,1,False),'c1440':('chromium',1440,900,None,1,False),'c1920':('chromium',1920,1080,None,1,False)}
JS2=r"""(o)=>{const out=[];const roots=[...document.querySelectorAll(o.root||'main')];
const nm=e=>{let s=e.tagName.toLowerCase();if(e.id)s+='#'+e.id;const c=(e.getAttribute('class')||'').trim();if(c)s+='.'+c.split(/\s+/).slice(0,2).join('.');const bk=e.closest('[id]');return s+(bk&&bk!==e?' @'+bk.id:'')+' «'+(e.textContent||'').trim().slice(0,18)+'»'};
const skip=o.panel?(e=>e.closest('svg,canvas,[aria-hidden=true],.leaflet-container,.sr-only')):(e=>e.closest('svg,.leaflet-container,.nav,#toc,.toc,.fab,.fabm,#tpanel,.mersvg,canvas,.cmw,[aria-hidden=true],.sr-only,.visually-hidden'));
const vis=(e,s)=>{if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0)return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
const clear=c=>!c||c==='transparent'||/rgba\([^)]*,\s*0\)$/.test(c);
for(const R0 of roots){const rs0=getComputedStyle(R0);if(!vis(R0,rs0))continue;
 if(o.panel){const r=R0.getBoundingClientRect();if(r.left<-1||r.right>innerWidth+1)out.push(['panel-offscreen-x',nm(R0)+' '+Math.round(r.left)+'..'+Math.round(r.right)]);
   if(r.bottom>innerHeight+1&&!/auto|scroll/.test(rs0.overflowY)&&rs0.position==='fixed')out.push(['panel-offscreen-y',nm(R0)+' bottom '+Math.round(r.bottom)])}
 const all=[...R0.querySelectorAll('*')].filter(e=>!skip(e));const S=new Map();for(const e of all)S.set(e,getComputedStyle(e));
 // 7 narrow-stack: own text run >4 chars squeezed into <2.2em width over >=3 lines
 for(const e of all){const s=S.get(e);if(!vis(e,s))continue;const fs=parseFloat(s.fontSize)||14;
  for(const n of e.childNodes){if(n.nodeType!==3)continue;const t=n.textContent.trim();if([...t].length<=4)continue;const rg=document.createRange();rg.selectNodeContents(n);const r=rg.getBoundingClientRect();
   if(r.width>0&&r.width<fs*2.2&&r.height>fs*3.2){out.push(['narrow-stack',nm(e)+' w'+Math.round(r.width)+' h'+Math.round(r.height)]);break}}}
 // 8 escape: text-bearing in-flow element spilling outside a visible (bordered/filled) overflow-visible parent box
 for(const e of all){const s=S.get(e);if(!vis(e,s)||/^(absolute|fixed|sticky)$/.test(s.position)||s.display==='contents'||!(e.textContent||'').trim())continue;
  const p=e.parentElement;if(!p||p===document.body)continue;const ps=S.get(p)||getComputedStyle(p);if(ps.display==='contents'||ps.display==='inline'||ps.overflowX!=='visible'||ps.overflowY!=='visible')continue;
  const box=(parseFloat(ps.borderTopWidth)>0&&!clear(ps.borderTopColor))||(parseFloat(ps.borderLeftWidth)>0&&!clear(ps.borderLeftColor))||!clear(ps.backgroundColor)||ps.backgroundImage!=='none';if(!box)continue;
  if(e.closest('.tw,.tblw,.spines,pre')&&!o.panel)continue;
  const a=e.getBoundingClientRect(),b=p.getBoundingClientRect();const dx=Math.max(b.left-a.left,a.right-b.right),dy=a.bottom-b.bottom;
  if(dx>4||dy>4)out.push(['escape',nm(e)+' in '+nm(p)+' dx'+Math.round(dx)+' dy'+Math.round(dy)])}
 if(o.panel){// sibling overlap inside panels (any display incl. inline-block/flex items)
  const par=new Set(all.map(e=>e.parentElement));for(const p of par){if(!p)continue;const kids=[...p.children].filter(k=>{const s=S.get(k);return s&&vis(k,s)&&!/^(absolute|fixed)$/.test(s.position)&&s.display!=='inline'&&(k.textContent||'').trim()});
   const R=kids.map(k=>k.getBoundingClientRect());for(let i=0;i<kids.length;i++)for(let j=i+1;j<Math.min(kids.length,i+8);j++){const a=R[i],b=R[j];const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(w>2&&h>2)out.push(['panel-overlap',nm(kids[i])+' × '+nm(kids[j])+' '+Math.round(w)+'x'+Math.round(h)])}}}
}
const d=document.documentElement;if(d.scrollWidth>d.clientWidth+1)out.push(['page-hscroll',d.scrollWidth+'>'+d.clientWidth]);
return out}"""
NAVJS=r"""()=>{const o=[];const t=document.getElementById('topbar').getBoundingClientRect();if(t.bottom>2)o.push(['nav-not-hidden','bottom '+t.bottom]);
const tab=document.getElementById('navTab');const r=tab.getBoundingClientRect(),s=getComputedStyle(tab);if(s.visibility!=='visible'||r.top<0||r.bottom>innerHeight||r.width<40)o.push(['navtab-missing',JSON.stringify([s.visibility,r.top,r.width])]);
const sp=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop);if(sp>20)o.push(['scrollpad-not-adapted',sp]);
const toc=document.getElementById('toc');if(toc&&innerWidth>1000&&!document.body.classList.contains('tochide')){const tr=toc.getBoundingClientRect();if(tr.top>2)o.push(['toc-not-adapted','top '+tr.top])}
const d=document.documentElement;if(d.scrollWidth>d.clientWidth+1)o.push(['page-hscroll',d.scrollWidth+'>'+d.clientWidth]);return o}"""
PREP="()=>{window.__hydrateAll&&window.__hydrateAll();window.__merAll&&window.__merAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'));document.querySelectorAll('details').forEach(d=>d.open=true)}"
NOANIM='section.blk,.bk{content-visibility:visible!important}*{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important}'
TH=os.environ.get('THEMES','night').split(',');N=int(os.environ.get('N','3'))
tot=collections.Counter()
def report(prof,pg,tag,res):
    if not res: return
    c=collections.Counter(t for t,_ in res);tot.update(c);print(f'BAD {prof} {pg} {tag} '+json.dumps(dict(c)),flush=True);seen=collections.Counter()
    for t,m in res:
        seen[t]+=1
        if seen[t]<=N: print('   ',t,m,flush=True)
with sync_playwright() as p:
    B={}
    for prof in os.environ.get('PROFILES','wk390').split(','):
        eng,w,h,ua,dpr,mob=PROF[prof]
        if eng not in B: B[eng]=p.webkit.launch() if eng=='webkit' else p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        kw=dict(viewport={'width':w,'height':h},device_scale_factor=dpr,has_touch=mob)
        if ua: kw['user_agent']=ua
        if mob and eng=='chromium': kw['is_mobile']=True
        if mob and eng=='webkit': kw['is_mobile']=True
        for th in TH:
            ctx=B[eng].new_context(**kw);ctx.add_init_script(f"localStorage.setItem('wb-theme','{th}');localStorage.removeItem('wb-nav')")
            t0=time.time()
            for pg in pages:
                page=ctx.new_page();errs=[];page.on('pageerror',lambda e,errs=errs:errs.append(str(e)))
                try:
                    page.goto('file://'+SITE+'/'+pg);page.wait_for_timeout(600);page.add_style_tag(content=NOANIM);page.evaluate(PREP);page.wait_for_timeout(1200 if pg!='index.html' else 2200)
                    report(prof,pg,'main1',page.evaluate(JS1));report(prof,pg,'main2',page.evaluate(JS2,{}))
                    for rep in range(2):
                        page.evaluate("()=>scrollTo(0,0)");page.wait_for_timeout(100)
                        page.click('#tpBtn');page.wait_for_timeout(150);report(prof,pg,f'tpanel{rep}',page.evaluate(JS2,{'root':'#tpanel','panel':1}));page.click('#tpBtn');page.wait_for_timeout(100)
                    n=page.locator('.ngb').count()
                    for i in range(n):
                        b=page.locator('.ngb').nth(i)
                        if not b.is_visible(): continue
                        b.scroll_into_view_if_needed();b.click();page.wait_for_timeout(150);report(prof,pg,f'ndd{i}',page.evaluate(JS2,{'root':'.ng.open .ndd','panel':1}));page.evaluate("()=>document.body.click()");page.wait_for_timeout(80)
                    page.click('#tocBtn');page.wait_for_timeout(250);page.evaluate("()=>{const a=document.getElementById('tocAll');a&&a.click()}");page.wait_for_timeout(200)
                    if w<=1000: report(prof,pg,'toc',page.evaluate(JS2,{'root':'#toc','panel':1}));page.evaluate("()=>document.body.classList.remove('tocopen')")
                    else: page.click('#tocBtn');page.wait_for_timeout(200);report(prof,pg,'toc',page.evaluate(JS2,{'root':'#toc','panel':1}))
                    page.evaluate("()=>scrollTo(0,1400)");page.wait_for_timeout(300)
                    for rep in range(2):
                        if page.locator('.fabt').is_visible():
                            page.click('.fabt');page.wait_for_timeout(200);report(prof,pg,f'fab{rep}',page.evaluate(JS2,{'root':'.fab','panel':1}));page.evaluate("()=>document.body.click()");page.wait_for_timeout(120)
                    if page.locator('.legend-em').count():
                        page.evaluate("()=>document.documentElement.classList.add('recall')");page.wait_for_timeout(100);report(prof,pg,'legend-recall',page.evaluate(JS2,{'root':'.legend-em','panel':1}));page.evaluate("()=>document.documentElement.classList.remove('recall')")
                    page.evaluate("()=>window.__nav.hide()");page.wait_for_timeout(250);report(prof,pg,'navhidden',page.evaluate(NAVJS));report(prof,pg,'navhidden-main',[x for x in page.evaluate(JS1) if x[0] in('overlap','page-hscroll')])
                    page.evaluate("()=>window.__nav.show()");page.wait_for_timeout(150)
                    if errs: report(prof,pg,'js',[('pageerror',e[:160]) for e in errs])
                except Exception as ex: report(prof,pg,'exc',[('exception',str(ex)[:200])])
                page.close()
            print(f'DONE {prof} {th} {len(pages)}p {time.time()-t0:.0f}s',flush=True);ctx.close()
    for b in B.values(): b.close()
print('TOTAL',json.dumps(dict(tot)))
