# v11.1 layout-quality checker: sibling overlap, empty bordered boxes, clipped text, overlapping inline fragments, chip-row wrap
# usage: WIDTHS=390,1440 ENGINE=chromium|webkit python3 check_overlap.py [pages|all]
import sys,os,json,collections
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else [f for f in sorted(os.listdir(SITE)) if f.endswith('.html')]
widths=[int(x) for x in os.environ.get('WIDTHS','390').split(',')]; ENG=os.environ.get('ENGINE','chromium'); TH=os.environ.get('THEME','night')
JS=r"""()=>{
const out=[];const nm=e=>{let s=e.tagName.toLowerCase();if(e.id)s+='#'+e.id;const c=(e.getAttribute('class')||'').trim();if(c)s+='.'+c.split(/\s+/).slice(0,2).join('.');const bk=e.closest('[id^=bk-],section[id],[id]');const pp=e.parentElement;return s+' <'+(pp?pp.tagName.toLowerCase()+'.'+(pp.getAttribute('class')||'').split(' ')[0]:'')+(bk&&bk!==e?' @'+bk.id:'')+(window.__DBG?' «'+e.outerHTML.slice(0,140)+'»':'')};
const skip=e=>e.closest('svg,.leaflet-container,.nav,#toc,.toc,.fab,.fabm,#tpanel,.mersvg,canvas,.cmw,[aria-hidden=true],.sr-only,.visually-hidden');
const vis=(e,s)=>{if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0)return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
const txt=e=>(e.textContent||'').trim().length>0;
const clear=c=>!c||c==='transparent'||/rgba\([^)]*,\s*0\)$/.test(c);
const all=[...document.querySelectorAll('main *')].filter(e=>!skip(e));
const S=new Map();for(const e of all)S.set(e,getComputedStyle(e));
// 1 sibling overlap (block-level, in-flow)
const par=new Set(all.map(e=>e.parentElement));
for(const p of par){if(!p||skip(p))continue;const ps=S.get(p)||getComputedStyle(p);if(/^(inline|contents)$/.test(ps.display))continue;
 const kids=[...p.children].filter(k=>{const s=S.get(k);return s&&vis(k,s)&&!/^(absolute|fixed|sticky)$/.test(s.position)&&s.display!=='inline'&&s.display!=='contents'&&txt(k)&&!k.matches('br,wbr')});
 const R=kids.map(k=>k.getBoundingClientRect());
 for(let i=0;i<kids.length;i++)for(let j=i+1;j<Math.min(kids.length,i+6);j++){const a=R[i],b=R[j];const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(w>2&&h>2)out.push(['overlap',nm(kids[i])+' × '+nm(kids[j])+' '+Math.round(w)+'x'+Math.round(h)])}}
// 2 empty bordered/filled boxes
for(const e of all){const s=S.get(e);if(!vis(e,s)||txt(e)||e.querySelector('img,svg,canvas,input,select,textarea,iframe,video,picture,button'))continue;if(e.children.length||/--v:/.test(e.getAttribute('style')||'')||e.matches('[title],th,td,img,svg,canvas,input,select,textarea,iframe,video,hr,br,i,.sbar>span,[role=img],[role=img] *,.dot,.sw,.swatch'))continue;const r=e.getBoundingClientRect();if(r.width<16||r.height<16)continue;
 const bw=parseFloat(s.borderTopWidth)+parseFloat(s.borderLeftWidth);const bd=bw>0&&!clear(s.borderTopColor);const bg=!clear(s.backgroundColor)||s.backgroundImage!=='none';if(s.backgroundImage.includes('url('))continue;if(bd||(bg&&r.height>=16&&r.width>=40))out.push(['empty-box',nm(e)+' '+Math.round(r.width)+'x'+Math.round(r.height)])}
// 3 clipped text
for(const e of all){const s=S.get(e);if(!vis(e,s)||!txt(e))continue;if(e.matches('.spines,.tw,.tblw,pre,code')||s.webkitLineClamp&&s.webkitLineClamp!=='none')continue;
 const ox=s.overflowX,oy=s.overflowY;if((ox==='hidden'||ox==='clip')&&e.scrollWidth>e.clientWidth+2&&s.textOverflow!=='ellipsis'&&!e.querySelector('svg,.leaflet-container')&&(()=>{const R=e.getBoundingClientRect();if(!e.children.length)return true;const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects())if(r.width>0&&(r.right>R.right+1||r.left<R.left-1))return true}return false})())out.push(['clip-x',nm(e)+' '+e.scrollWidth+'>'+e.clientWidth]);
 if((oy==='hidden'||oy==='clip')&&e.scrollHeight>e.clientHeight+3&&!/^(auto|scroll)$/.test(ox)&&!e.matches('details,.bk,.body')&&!e.querySelector('svg,.leaflet-container')&&e.clientHeight>0)out.push(['clip-y',nm(e)+' '+e.scrollHeight+'>'+e.clientHeight])}
// 4 inline decorated fragments overlapping
for(const e of all){const s=S.get(e);if(s.display!=='inline'||!txt(e))continue;const dec=parseFloat(s.paddingTop)+parseFloat(s.paddingBottom)>2||(parseFloat(s.borderTopWidth)>0&&!clear(s.borderTopColor))||!clear(s.backgroundColor);if(!dec)continue;const rs=[...e.getClientRects()].filter(r=>r.width>1);if(rs.length<2)continue;
 let ov=0;for(let i=0;i+1<rs.length;i++){const a=rs[i],b=rs[i+1];if(b.top>=a.bottom-0.5)continue;const w=Math.min(a.right,b.right)-Math.max(a.left,b.left);if(w>2&&a.bottom-b.top>1.5)ov=Math.max(ov,a.bottom-b.top)}
 if(ov)out.push(['inline-frag-overlap',nm(e)+' frags'+rs.length+' ov'+ov.toFixed(1)])}
// 5 chip rows wrapping into >2 rows (messy)
if(innerWidth>=390)for(const e of document.querySelectorAll('main .chips')){if(skip(e)||e.children.length>6)continue;const tops=new Set([...e.children].filter(k=>k.offsetParent).map(k=>Math.round(k.getBoundingClientRect().top/4)));if(tops.size>2)out.push(['chip-wrap',nm(e)+' rows'+tops.size])}
// 6 page horizontal overflow
const d=document.documentElement;if(d.scrollWidth>d.clientWidth+1)out.push(['page-hscroll',d.scrollWidth+'>'+d.clientWidth]);
return out}"""
tot=collections.Counter(); rows=[]
with sync_playwright() as p:
    if ENG=='webkit': b=p.webkit.launch()
    else: b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in widths:
        ctx=b.new_context(viewport={'width':w,'height':800 if w<800 else 900},device_scale_factor=1); ctx.add_init_script(f"localStorage.setItem('wb-theme','{TH}')")
        for pg in pages:
            page=ctx.new_page(); page.goto('file://'+SITE+'/'+pg); page.wait_for_timeout(700)
            page.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}*{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important}')
            page.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();window.__merAll&&window.__merAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'));document.querySelectorAll('details').forEach(d=>d.open=true)}")
            page.wait_for_timeout(1500 if pg!='index.html' else 2500)
            page.evaluate('()=>{window.__DBG=%s}'%('true' if os.environ.get('DBG') else 'false'));res=page.evaluate(JS); page.close()
            c=collections.Counter(t for t,_ in res); tot.update(c)
            print(f'PG {pg} {w} '+json.dumps(dict(c)),flush=True)
            seen=collections.Counter()
            for t,m in res:
                seen[t]+=1
                if seen[t]<=int(os.environ.get('N','4')): print('  ',t,m,flush=True)
        ctx.close()
    b.close()
print('TOTAL',ENG,widths,json.dumps(dict(tot)))
