import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q,directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for rm in ('reduce','no-preference'):
        ctx=b.new_context(viewport={'width':1440,'height':900}, reduced_motion=rm)
        pg=ctx.new_page()
        pg.goto(f'http://127.0.0.1:{port}/', wait_until='domcontentloaded')
        pg.wait_for_timeout(120 if rm=='reduce' else 2500)
        r=pg.evaluate("""() => {
          const sl=[...document.querySelectorAll('[data-slice]')];
          const caches=sl.filter(e=>parseFloat(getComputedStyle(e).opacity)<0.9);
          const bandes=[...document.querySelectorAll('.lame-bande')];
          const broche=document.querySelector('.broche');
          const lignes=[...document.querySelectorAll('.hero-ligne')];
          return {
            slice_total: sl.length,
            slice_caches: caches.length,
            bandes_affichees: bandes.filter(e=>getComputedStyle(e).display!=='none').length,
            broche_affichee: broche ? getComputedStyle(broche).display!=='none' : false,
            hero_lignes_cachees: lignes.filter(e=>parseFloat(getComputedStyle(e).opacity)<0.9).length,
          };
        }""")
        etiq = 'REDUIT (a 120ms, sans attendre)' if rm=='reduce' else 'NORMAL (apres 2,5s)'
        print(f"\n=== prefers-reduced-motion: {rm} — {etiq} ===")
        print(f"  elements [data-slice] caches : {r['slice_caches']}/{r['slice_total']}")
        print(f"  bandes de la lame affichees  : {r['bandes_affichees']}")
        print(f"  broche affichee              : {r['broche_affichee']}")
        print(f"  lignes du hero cachees       : {r['hero_lignes_cachees']}")
        if rm=='reduce':
            ok = r['slice_caches']==0 and r['bandes_affichees']==0 and not r['broche_affichee'] and r['hero_lignes_cachees']==0
            print(f"  --> {'OK — tout visible d emblee, aucune cinematique' if ok else 'FAIL'}")
        ctx.close()
    b.close()
srv.shutdown()
