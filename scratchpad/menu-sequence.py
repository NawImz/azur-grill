"""Capture l'ouverture du menu image par image + controle des etats."""
import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q, directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
temps=[0, 90, 180, 300, 480]
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for t in temps:
        pg=b.new_context(viewport={'width':390,'height':780}).new_page()
        pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle'); pg.wait_for_timeout(900)
        pg.click('#menu-toggle')
        if t: pg.wait_for_timeout(t)
        f=f'scratchpad/_m{t}.png'; pg.screenshot(path=f); shots.append((t,f))
        pg.context.close()
    # controle des etats
    pg=b.new_context(viewport={'width':390,'height':780}).new_page()
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle'); pg.wait_for_timeout(900)
    def etat(label):
        r=pg.evaluate("""() => {
          const n=document.getElementById('mobile-nav'), t=document.getElementById('menu-toggle');
          const b1=document.querySelector('.barre-1'), b2=document.querySelector('.barre-2');
          const cs=getComputedStyle(n);
          return {ouvert:n.dataset.ouvert, aria:t.getAttribute('aria-expanded'),
                  label:t.getAttribute('aria-label'),
                  transform:cs.transform, visibility:cs.visibility,
                  barre1:getComputedStyle(b1).transform,
                  barre2_opacity:getComputedStyle(b2).opacity,
                  tab:[...n.querySelectorAll('a')].map(a=>a.tabIndex)[0]};}""")
        print(f"  {label}")
        for k,v in r.items(): print(f"      {k:16} {v}")
    etat("--- ferme ---")
    pg.click('#menu-toggle'); pg.wait_for_timeout(700)
    etat("--- ouvert ---")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(700)
    etat("--- referme par Echap ---")
    b.close()
srv.shutdown()
ims=[(t,Image.open(f)) for t,f in shots]
w,h=ims[0][1].size
sheet=Image.new('RGB',(w*len(ims), h+26),(255,255,255)); d=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(ims):
    d.text((i*w+6,6), f'{t} ms', fill=(0,0,0)); sheet.paste(im,(i*w,22))
sheet.thumbnail((1500,2000)); sheet.save('scratchpad/menu-sequence.png')
print('\n  scratchpad/menu-sequence.png', sheet.size)
