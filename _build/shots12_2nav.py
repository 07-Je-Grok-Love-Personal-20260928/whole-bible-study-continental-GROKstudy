import os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));OUT='/workspace/wb/shots/v12_2/'
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 EdgiOS/129.0.2792.84 Mobile/15E148 Safari/604.1'
def run(pg,name):
    pg.goto('file://'+SITE+'/overview.html');pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))}")
    pg.evaluate("()=>window.scrollTo(0,1800)");pg.wait_for_timeout(300);pg.evaluate("()=>window.scrollTo(0,1600)");pg.wait_for_timeout(700)
    pg.screenshot(path=OUT+f'topnav_shown_{name}.png')
    pg.evaluate("()=>window.scrollTo(0,2600)");pg.wait_for_timeout(250);pg.evaluate("()=>window.scrollTo(0,2700)");pg.wait_for_timeout(900)
    print(name,pg.evaluate("()=>[JSON.stringify(window.__nav.state),getComputedStyle(document.documentElement).scrollPaddingTop]"))
    pg.screenshot(path=OUT+f'topnav_hidden_{name}.png')
with sync_playwright() as p:
    d=dict(p.devices['iPhone 13']);d['user_agent']=UA;d['viewport']={'width':390,'height':664}
    b=p.webkit.launch();c=b.new_context(**d);run(c.new_page(),'webkit390');b.close()
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);c=b.new_context(viewport={'width':1440,'height':900});run(c.new_page(),'chromium1440');b.close()
