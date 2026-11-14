# usage: python3 shots11_1.py before|after [chromium|webkit] [width]
import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tag=sys.argv[1]; eng=sys.argv[2] if len(sys.argv)>2 else 'chromium'; W=int(sys.argv[3]) if len(sys.argv)>3 else 390
OUT='/workspace/wb/shots/v11_1'
SPOTS=[('1_keyverse','#b-gen-kv'),('2_mnemonic','#bk-gen .co.mnc'),('3_structbar','#b-lev-ol'),('4_header','#bk-lev>header')]
with sync_playwright() as p:
    if eng=='webkit': b=p.webkit.launch(env={**os.environ,'LD_LIBRARY_PATH':'/workspace/wkdeps/root/usr/lib/x86_64-linux-gnu'})
    else: b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':W,'height':844},device_scale_factor=2); ctx.add_init_script("localStorage.setItem('wb-theme','night')")
    pg=ctx.new_page(); pg.goto('file://'+SITE+'/index.html'); pg.wait_for_timeout(1000)
    pg.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}')
    pg.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
    pg.wait_for_timeout(1500)
    for name,sel in SPOTS:
        el=pg.locator(sel).first
        if sel.startswith('#b-'): el=pg.locator(sel).locator('xpath=..')
        el.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
        el.screenshot(path=f'{OUT}/{tag}_{name}_{eng}_{W}.png')
        print('ok',name)
    b.close()
