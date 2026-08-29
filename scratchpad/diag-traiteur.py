import functools, threading, io
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q,directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_context(viewport={'width':375,'height':900},device_scale_factor=2).new_page()
    pg.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle'); pg.wait_for_timeout(1500)
    H=pg.evaluate('document.body.scrollHeight')
    for k in range(5):
        y=min(int(H*k/5), max(0,H-900))
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(700)
        info=pg.evaluate("""() => {
          const li=[...document.querySelectorAll('li')].find(e=>e.textContent.trim()==='Traiteur');
          if(!li) return null;
          const r=document.createRange(); r.selectNodeContents(li);
          const rects=[...r.getClientRects()].map(x=>({x:Math.round(x.x),y:Math.round(x.y),w:Math.round(x.width),h:Math.round(x.height)}));
          const bb=li.getBoundingClientRect();
          return {rects, box:{x:Math.round(bb.x),y:Math.round(bb.y),w:Math.round(bb.width),h:Math.round(bb.height)}};
        }""")
        if info: print(f'scroll {y:>5} | Range[0]={info["rects"][0] if info["rects"] else None} | box={info["box"]}')
    b.close()
srv.shutdown()
