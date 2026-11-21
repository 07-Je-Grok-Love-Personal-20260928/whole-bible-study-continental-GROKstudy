# usage: python3 shots12_1.py engine width theme page [scrollSelector] [full]
import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eng,W,TH,pgn=sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4]; sel=sys.argv[5] if len(sys.argv)>5 else ''; full=len(sys.argv)>6
OUT='/workspace/wb/shots/v12_1'; os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    if eng=='webkit': b=p.webkit.launch(env={**os.environ,'LD_LIBRARY_PATH':'/workspace/wkdeps/root/usr/lib/x86_64-linux-gnu'})
    else: b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':W,'height':900 if W>800 else 844},device_scale_factor=2 if W<800 else 1,has_touch=W<800); ctx.add_init_script(f"localStorage.setItem('wb-theme','{TH}')")
    pg=ctx.new_page(); pg.goto('file://'+SITE+'/'+pgn); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
    if sel: pg.evaluate(f"()=>{{const e=document.querySelector('{sel}');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-70)}}"); pg.wait_for_timeout(1200)
    fn=f'{OUT}/{pgn[:-5]}{("_"+sel.strip("#.")) if sel else ""}_{eng}_{W}_{TH}.png'; pg.screenshot(path=fn,full_page=full); print(fn)
    b.close()
