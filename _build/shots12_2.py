# v12.2 legend shots: WebKit iPhone 13 (EdgiOS UA), overview #em-legend and memory legendbox
import sys,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT='/workspace/wb/shots/v12_2/'
tag=sys.argv[1] if len(sys.argv)>1 else 'after'
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/129.0.2792.84 Mobile/15E148 Safari/604.1'
with sync_playwright() as p:
    d=dict(p.devices['iPhone 13']);d['user_agent']=UA;d['viewport']={'width':390,'height':664}
    b=p.webkit.launch();ctx=b.new_context(**d);ctx.add_init_script("localStorage.setItem('wb-theme','night')")
    pg=ctx.new_page();pg.goto('file://'+SITE+'/overview.html#em-legend');pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));document.getElementById('em-legend').scrollIntoView()}");pg.wait_for_timeout(800)
    el=pg.locator('.legend-em').first;el.scroll_into_view_if_needed();pg.wait_for_timeout(400)
    el.screenshot(path=OUT+f'legend_overview_{tag}_webkit390.png')
    pg.goto('file://'+SITE+'/memory.html');pg.wait_for_timeout(1500)
    sm=pg.locator('details.legendbox summary').first;sm.scroll_into_view_if_needed();sm.click();pg.wait_for_timeout(800)
    pg.evaluate("()=>{const d=document.querySelector('details.legendbox');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-120)}");pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+f'legend_panel_{tag}_webkit390.png')
    b.close()
print('ok')
