"""Capture la sequence d'entree du hero image par image."""
import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q,directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
temps=[80, 260, 440, 620, 900]
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for t in temps:
        pg=b.new_context(viewport={'width':900,'height':620}).new_page()
        pg.goto(f'http://127.0.0.1:{port}/', wait_until='domcontentloaded')
        pg.wait_for_timeout(t)
        f=f'scratchpad/_seq{t}.png'; pg.screenshot(path=f); shots.append((t,f))
        pg.context.close()
    b.close()
srv.shutdown()
ims=[(t,Image.open(f)) for t,f in shots]
w,h=ims[0][1].size
sheet=Image.new('RGB',(w, (h+26)*len(ims)),(255,255,255)); d=ImageDraw.Draw(sheet)
y=0
for t,im in ims:
    d.text((6,y+6), f'{t} ms', fill=(0,0,0)); sheet.paste(im,(0,y+22)); y+=h+26
sheet.thumbnail((760,4000)); sheet.save('scratchpad/sequence-hero.png')
print('scratchpad/sequence-hero.png', sheet.size)
