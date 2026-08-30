"""Un element deja revele peut-il repartir a zero quand on remonte ?
On surveille en continu, y compris pendant les remontees profondes."""
import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q, directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_context(viewport={'width':1440,'height':900}).new_page()
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='domcontentloaded')
    pg.evaluate("""() => {
      window.__rejoue = []; const vu = new WeakMap();
      const els = [...document.querySelectorAll('[data-slice]')];
      setInterval(() => {
        for (const el of els) {
          const o = parseFloat(getComputedStyle(el).opacity);
          const cp = getComputedStyle(el).clipPath;
          const etait = vu.get(el);
          // « deja revele » = opacite pleine ; on note toute rechute
          if (etait && o < 0.9) {
            window.__rejoue.push({txt:(el.textContent||'').trim().slice(0,30),
                                  o:o.toFixed(2), clip:cp.slice(0,28), y:Math.round(scrollY)});
          }
          if (o > 0.95) vu.set(el, true);
        }
      }, 40);
    }""")
    H=pg.evaluate('document.body.scrollHeight')
    # descente lente : les images se chargent au fur et a mesure
    for y in range(0, H-800, 120):
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(110)
    pg.wait_for_timeout(1200)
    # remontee profonde, jusqu'en haut
    for y in range(H-800, -1, -160):
        pg.evaluate(f'window.scrollTo(0,{max(0,y)})'); pg.wait_for_timeout(90)
    pg.wait_for_timeout(1500)
    # puis on redescend
    for y in range(0, H-800, 200):
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(70)
    pg.wait_for_timeout(1200)
    r=pg.evaluate('window.__rejoue')
    print(f"  rechutes apres revelation : {len(r)}")
    vus=set()
    for x in r:
        if x['txt'] in vus: continue
        vus.add(x['txt'])
        print(f"    scrollY={x['y']:>5}  opacite {x['o']}  clip={x['clip']}  {x['txt']!r}")
    print("  -->", "AUCUN REJOUE" if not r else "BUG REPRODUIT")
    b.close()
srv.shutdown()
