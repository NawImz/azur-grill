import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

W = int(sys.argv[1]) if len(sys.argv)>1 else 1440
OUT = sys.argv[2] if len(sys.argv)>2 else 'scratchpad/avant-sections.png'
h = functools.partial(Quiet, directory='dist')
srv = ThreadingHTTPServer(('127.0.0.1', 0), h)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]
shots=[]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_context(viewport={'width':W,'height':900}).new_page()
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle'); pg.wait_for_timeout(1200)
    H = pg.evaluate("document.body.scrollHeight")
    y=0; i=0
    while y < H and i < 9:
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(1100)
        f=f'scratchpad/_s{i}.png'; pg.screenshot(path=f); shots.append(f)
        y += 860; i+=1
    b.close()
srv.shutdown()
ims=[Image.open(f) for f in shots]
sheet=Image.new('RGB',(ims[0].width, sum(i.height for i in ims)),(255,255,255))
yy=0
for im in ims: sheet.paste(im,(0,yy)); yy+=im.height
sheet.thumbnail((900, 6000))
sheet.save(OUT); print(OUT, sheet.size, len(shots),'ecrans')
