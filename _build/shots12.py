# usage: python3 shots12.py engine width theme mode   mode: card|pano|toc|fab
import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eng=sys.argv[1]; W=int(sys.argv[2]); TH=sys.argv[3]; mode=sys.argv[4]; arg=sys.argv[5] if len(sys.argv)>5 else ''
OUT='/workspace/wb/shots/v12'
with sync_playwright() as p:
    if eng=='webkit': b=p.webkit.launch(env={**os.environ,'LD_LIBRARY_PATH':'/workspace/wkdeps/root/usr/lib/x86_64-linux-gnu'})
    else: b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':W,'height':900 if W>800 else 844},device_scale_factor=2 if W<800 else 1,is_mobile=W<800 and eng!='webkit',has_touch=W<800); ctx.add_init_script(f"localStorage.setItem('wb-theme','{TH}')")
    pg=ctx.new_page()
    if mode=='card':
        pg.goto('file://'+SITE+'/index.html'); pg.wait_for_timeout(1000)
        pg.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}.filters{position:static!important}.top,.prog,.fab,.totop,.rchip,.ndd{visibility:hidden!important}')
        pg.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
        pg.wait_for_timeout(1500)
        for bid in (arg or 'exo').split(','):
            el=pg.locator(f'#bk-{bid} .box.liu'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
            fn=f'{OUT}/liu_{bid}_{eng}_{W}_{TH}.png'; el.screenshot(path=fn); print(fn)
    elif mode=='pano':
        pg.goto('file://'+SITE+'/panorama.html'); pg.wait_for_timeout(1200)
        pg.add_style_tag(content='section.blk{content-visibility:visible!important}')
        pg.evaluate("()=>{document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
        sel=arg or '#eras'
        pg.evaluate(f"()=>document.querySelector('{sel}').scrollIntoView()"); pg.wait_for_timeout(1500)
        fn=f'{OUT}/pano_{sel.strip("#.")}_{eng}_{W}_{TH}.png'; pg.screenshot(path=fn); print(fn)
    else:
        pg.goto('file://'+SITE+'/'+(arg or 'story.html')); pg.wait_for_timeout(1200)
        if mode=='toc':
            if W<1000: pg.click('#tocBtn'); pg.wait_for_timeout(600)
        if mode=='fab':
            pg.mouse.wheel(0,1500); pg.wait_for_timeout(1200); pg.click('.fabt'); pg.wait_for_timeout(600)
        fn=f'{OUT}/{mode}_{(arg or "story").split(".")[0]}_{eng}_{W}_{TH}.png'; pg.screenshot(path=fn); print(fn)
    b.close()
