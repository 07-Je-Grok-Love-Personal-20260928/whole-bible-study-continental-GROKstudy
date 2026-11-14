import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); tag=sys.argv[1]; eng=sys.argv[2] if len(sys.argv)>2 else 'chromium'
with sync_playwright() as p:
    b=p.webkit.launch() if eng=='webkit' else p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for W in (390,1440):
        ctx=b.new_context(viewport={'width':W,'height':900},device_scale_factor=2 if W<500 else 1); ctx.add_init_script("localStorage.setItem('wb-theme','night')")
        pg=ctx.new_page(); pg.goto('file://'+SITE+'/index.html'); pg.wait_for_timeout(1500)
        pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
        el=pg.locator('#shelf'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
        pg.screenshot(path=f'/workspace/wb/shots/v11_1/{tag}_shelf_{W}{"" if eng=="chromium" else "_"+eng}.png')
        # tap a spine and check landing
        pg.locator('#shelf a[href="#b-isa"]').click(); pg.wait_for_timeout(2500)
        r=pg.evaluate("()=>{const h=document.getElementById('bk-isa').getBoundingClientRect();const on=document.querySelector('#shelf a.on');return {top:Math.round(h.top),on:on&&on.getAttribute('href'),sw:document.documentElement.scrollWidth,cw:innerWidth}}")
        print(W,eng,r); ctx.close()
    b.close()
