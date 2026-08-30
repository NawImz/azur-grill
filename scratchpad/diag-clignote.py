"""Detecte les elements qui repassent de VISIBLE a INVISIBLE pendant le scroll.
C'est le symptome decrit : « ils disparaissent puis reapparaissent »."""
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
    # on arme la surveillance TOT, avant que les images finissent de charger
    pg.evaluate("""() => {
      window.__retours = [];
      window.__etat = new WeakMap();
      const els = [...document.querySelectorAll('[data-slice]')];
      setInterval(() => {
        for (const el of els) {
          const o = parseFloat(getComputedStyle(el).opacity);
          const avant = window.__etat.get(el);
          if (avant !== undefined && avant > 0.9 && o < 0.5) {
            window.__retours.push({
              t: Math.round(performance.now()),
              txt: (el.textContent||'').trim().slice(0,34),
              de: avant.toFixed(2), vers: o.toFixed(2),
            });
          }
          window.__etat.set(el, o);
        }
      }, 40);
    }""")
    H=pg.evaluate('document.body.scrollHeight')
    for y in range(0, H-800, 150):
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(80)
    pg.wait_for_timeout(1500)
    r=pg.evaluate('window.__retours')
    print(f"  elements repassEs de visible a invisible : {len(r)}")
    for x in r[:12]:
        print(f"    a {x['t']:>5} ms : {x['de']} -> {x['vers']}  {x['txt']!r}")
    print("  -->", "AUCUN CLIGNOTEMENT" if not r else "BUG REPRODUIT")
    b.close()
srv.shutdown()
