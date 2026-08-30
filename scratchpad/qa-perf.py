"""LCP / CLS mesures dans Chromium. Ce n'est PAS un audit Lighthouse
(non disponible ici) : reseau local, machine non bridee — les valeurs
sont donc un PLANCHER optimiste, pas une note de terrain."""
import functools, threading, statistics
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q,directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]

MESURE = """() => new Promise(res => {
  let lcp = 0, cls = 0;
  new PerformanceObserver(l => { for (const e of l.getEntries()) lcp = Math.max(lcp, e.startTime); })
    .observe({type:'largest-contentful-paint', buffered:true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) cls += e.value; })
    .observe({type:'layout-shift', buffered:true});
  setTimeout(() => {
    const nav = performance.getEntriesByType('navigation')[0];
    res({lcp, cls, dcl: nav ? nav.domContentLoadedEventEnd : 0,
         element: (performance.getEntriesByType('largest-contentful-paint').slice(-1)[0]||{}).element});
  }, 4200);
})"""

with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for W,label in [(375,'mobile 375'), (1440,'desktop 1440')]:
        lcps, clss = [], []
        for _ in range(3):
            ctx=b.new_context(viewport={'width':W,'height':812 if W==375 else 900})
            pg=ctx.new_page()
            pg.goto(f'http://127.0.0.1:{port}/', wait_until='domcontentloaded')
            r=pg.evaluate(MESURE)
            lcps.append(r['lcp']); clss.append(r['cls'])
            ctx.close()
        lcp=statistics.median(lcps); cls=statistics.median(clss)
        print(f"\n=== {label} (mediane sur 3 chargements) ===")
        print(f"  LCP : {lcp:7.0f} ms   cible <= 1500 ms   {'OK' if lcp<=1500 else 'FAIL'}")
        print(f"  CLS : {cls:7.3f}      cible <= 0.02      {'OK' if cls<=0.02 else 'FAIL'}")
    b.close()
srv.shutdown()
