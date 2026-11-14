# v11 interactive overflow/overlap checker: clicks/expands interactive UI then rechecks
import sys,os,json
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else [f for f in sorted(os.listdir(SITE)) if f.endswith('.html')]
widths=[int(x) for x in os.environ.get("WIDTHS","390").split(",")]
THEMES=['night','dawn','jade','ruby','contrast','violet','ocean','amber','sakura','sepia','aurora','spring']
OV="""(tag)=>{const d=document.documentElement;const over=[];const clipped=e=>{if(e instanceof SVGElement&&e.ownerSVGElement){let o=e;while(o.ownerSVGElement)o=o.ownerSVGElement;e=o}let a=e.parentElement;while(a&&a!==d){const o=getComputedStyle(a).overflowX;if(o!=='visible'&&a.getBoundingClientRect().right<=d.clientWidth+1)return true;a=a.parentElement}return false};
document.querySelectorAll('main *').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>d.clientWidth+1&&r.width>0&&!e.closest('.nav,.toc,.leaflet-container')&&!clipped(e))over.push(e.tagName+'.'+(e.getAttribute('class')||'')+':'+Math.round(r.right))});
const esc=[];const inV=(sel)=>document.querySelectorAll(sel).forEach(e=>{const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||e.hidden)return;const r=e.getBoundingClientRect();if(r.width&&(r.left<-1||r.right>innerWidth+1||(s.position==='fixed'&&(r.top<-1||r.bottom>innerHeight+1))))esc.push(sel+':'+Math.round(r.left)+'..'+Math.round(r.right)+' t'+Math.round(r.top)+'..'+Math.round(r.bottom))});
inV('#tpanel');inV('.fabm');inV('.ngi.open .ndd, .open>.ndd');if(tag==='toc')inV('#toc');if(tag==='toc-hidden'&&innerWidth>1000){const t=document.getElementById('toc').getBoundingClientRect(),m=document.getElementById('main').getBoundingClientRect();if(m.left>t.right+40&&t.right>0)esc.push('main-not-reflowed')}inV('.fab');
return {tag,sw:d.scrollWidth,cw:d.clientWidth,over:over.slice(0,6),esc:esc.slice(0,6)}}"""
out=[]
def chk(page,tag,pg,w):
    r=page.evaluate(OV,tag); r.update(page=pg,w=w)
    if r['sw']>r['cw'] or r['over'] or r['esc']: print('BAD',json.dumps(r,ensure_ascii=False),flush=True)
    out.append(r)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in widths:
        ctx=b.new_context(viewport={'width':w,'height':800 if w<800 else 900},device_scale_factor=1,has_touch=w<800)
        for pg in pages:
            page=ctx.new_page(); errs=[]
            page.on('pageerror',lambda e,errs=errs: errs.append(str(e)))
            page.goto('file://'+SITE+'/'+pg); page.wait_for_timeout(600)
            page.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}')
            page.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();window.__mapsAll&&window.__mapsAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
            page.wait_for_timeout(1200)
            # details all open
            page.evaluate("()=>document.querySelectorAll('details').forEach(d=>d.open=true)"); page.wait_for_timeout(300); chk(page,'details',pg,w)
            # expand-all buttons
            page.evaluate("()=>document.querySelectorAll('[data-expand]').forEach(b=>b.click())"); page.wait_for_timeout(200); chk(page,'expand',pg,w)
            # tabs: click each tab in turn
            n=page.evaluate("()=>{const t=[...document.querySelectorAll('[role=tab]')];t.forEach(x=>x.click());return t.length}")
            if n: page.wait_for_timeout(400); chk(page,'tabs-last',pg,w)
            page.evaluate("()=>document.querySelectorAll('[role=tablist]').forEach(l=>{const t=l.querySelector('[role=tab]');t&&t.click()})"); page.wait_for_timeout(200)
            # TOC open + expand all
            page.evaluate("()=>{scrollTo(0,0)}")
            if w<=1000: page.click('#tocBtn'); page.wait_for_timeout(400)
            page.evaluate("()=>{const a=document.getElementById('tocAll');a&&a.click()}"); page.wait_for_timeout(400); chk(page,'toc',pg,w)
            if w<=1000: page.evaluate("()=>document.body.classList.remove('tocopen')")
            else:
                page.click('#tocBtn'); page.wait_for_timeout(300); chk(page,'toc-hidden',pg,w); page.click('#tocBtn'); page.wait_for_timeout(300)
            # theme panel + 12 themes
            page.click('#tpBtn'); page.wait_for_timeout(300); chk(page,'tpanel',pg,w)
            for th in (THEMES if pg in ('index.html','geography.html','creeds.html') else THEMES[-2:]):
                page.evaluate("(t)=>{const b=document.querySelector('#tpanel [data-theme=\"'+t+'\"]');b&&b.click()}",th); page.wait_for_timeout(120)
                chk(page,'theme-'+th,pg,w)
            page.evaluate("()=>{const p=document.getElementById('tpanel');p.hidden=true}")
            # nav dropdowns (desktop)
            for i in range(page.locator('.ngb').count()):
                if page.locator('.ngb').nth(i).is_visible():
                    page.locator('.ngb').nth(i).click(); page.wait_for_timeout(200); chk(page,f'ngb{i}',pg,w)
            page.mouse.click(5,innerh:=300) if False else page.evaluate("()=>document.body.click()")
            # fab cluster
            page.evaluate("()=>scrollTo(0,1500)"); page.wait_for_timeout(500)
            if page.locator('.fabt').is_visible(): page.click('.fabt'); page.wait_for_timeout(300); chk(page,'fab',pg,w)
            # map source pickers & journey player
            if pg=='geography.html':
                page.evaluate("()=>{document.querySelectorAll('.mlk button').forEach(b=>b.click());document.querySelectorAll('.mlsrc select').forEach(s=>{if(s.options.length>1){s.selectedIndex=s.options.length-1;s.dispatchEvent(new Event('change',{bubbles:true}))}})}")
                page.wait_for_timeout(1500); chk(page,'picker',pg,w)
                page.evaluate("()=>document.querySelectorAll('.jyp').forEach(b=>b.click())"); page.wait_for_timeout(2500); chk(page,'journey-mid',pg,w)
                page.evaluate("()=>document.querySelectorAll('.jyf').forEach(b=>{for(let i=0;i<30;i++)b.click()})"); page.wait_for_timeout(800); chk(page,'journey-end',pg,w)
            if errs: print('ERR',pg,w,errs[:3],flush=True)
            print('PG',pg,w,flush=True)
            page.close()
        ctx.close()
print('DONE',len(out),'checks')
