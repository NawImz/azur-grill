import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

h = functools.partial(Quiet, directory='dist')
srv = ThreadingHTTPServer(('127.0.0.1', 0), h)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for rm in ('no-preference', 'reduce'):
        ctx = b.new_context(viewport={'width':1440,'height':900}, reduced_motion=rm)
        pg = ctx.new_page()
        pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
        pg.wait_for_timeout(1500)
        total = pg.evaluate("document.querySelectorAll('[data-reveal]').length")
        print(f"\n=== reduced_motion={rm} === ({total} elements [data-reveal])")
        # scroll progressif, on mesure ce qui est visible DANS le viewport a chaque palier
        H = pg.evaluate("document.body.scrollHeight")
        for freq in range(0, 6):
            y = int(H * freq / 6)
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(900)
            r = pg.evaluate("""() => {
              const els=[...document.querySelectorAll('[data-reveal]')];
              const inView=els.filter(e=>{const r=e.getBoundingClientRect();
                return r.top < innerHeight*0.8 && r.bottom > 0;});
              const hidden=inView.filter(e=>parseFloat(getComputedStyle(e).opacity)<0.5);
              return {inView:inView.length, hidden:hidden.length,
                      sample:hidden.slice(0,3).map(e=>e.tagName+'.'+(e.className||'').slice(0,30))};
            }""")
            print(f"  scroll {y:>5}px : {r['inView']:>2} dans le viewport, {r['hidden']:>2} INVISIBLES {r['sample'] if r['hidden'] else ''}")
        ctx.close()
    b.close()
srv.shutdown()
