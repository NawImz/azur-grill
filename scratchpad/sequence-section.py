"""Capture l'arrivee d'une section image par image, en simulant un vrai
defilement continu plutot qu'un saut."""
import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q, directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
SECTION=sys.argv[1]; OUT=sys.argv[2]
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    ctx=b.new_context(viewport={'width':1200,'height':800})
    ctx.route('**://**', lambda r: r.abort() if '127.0.0.1' not in r.request.url else r.continue_())
    pg=ctx.new_page()
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
    depart=pg.evaluate(f"document.querySelector('#{SECTION}').offsetTop - 520")
    # defilement continu, petits increments : on capture ce que l'oeil voit
    for i in range(6):
        y=depart + i*150
        pg.evaluate(f'window.scrollTo(0,{y})')
        pg.wait_for_timeout(260)
        f=f'scratchpad/_q{i}.png'; pg.screenshot(path=f); shots.append((y-depart,f))
    b.close()
srv.shutdown()
ims=[(d,Image.open(f)) for d,f in shots]
w,h=ims[0][1].size
sheet=Image.new('RGB',(w*len(ims),h+22),(255,255,255)); dr=ImageDraw.Draw(sheet)
for i,(d,im) in enumerate(ims):
    dr.text((i*w+6,5),f'+{d}px',fill=(0,0,0)); sheet.paste(im,(i*w,20))
sheet.thumbnail((1900,900)); sheet.save(OUT); print(OUT, sheet.size)
