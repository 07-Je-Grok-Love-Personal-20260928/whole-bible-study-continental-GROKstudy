# usage: python3 shots11_2.py [chromium|webkit] width theme [tag]
import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
eng=sys.argv[1]; W=int(sys.argv[2]); TH=sys.argv[3]; tag=sys.argv[4] if len(sys.argv)>4 else 'v11_2'
OUT='/workspace/wb/shots/v11_2'
with sync_playwright() as p:
    if eng=='webkit': b=p.webkit.launch(env={**os.environ,'LD_LIBRARY_PATH':'/workspace/wkdeps/root/usr/lib/x86_64-linux-gnu'})
    else: b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':W,'height':900},device_scale_factor=2 if W<800 else 1); ctx.add_init_script(f"localStorage.setItem('wb-theme','{TH}')")
    pg=ctx.new_page(); pg.goto('file://'+SITE+'/index.html'); pg.wait_for_timeout(1000)
    pg.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}.filters{position:static!important}.top,.prog,.fab,.totop,.rchip,.ndd{visibility:hidden!important}')
    pg.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
    pg.wait_for_timeout(1500)
    for bid in ('exo','lev'):
        el=pg.locator('#bk-'+bid); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        fn=f'{OUT}/{bid}_{eng}_{W}_{TH}.png'; el.screenshot(path=fn); print(fn)
    b.close()
