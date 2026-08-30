import functools, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Q(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory='scratchpad/pt'))
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    err = []
    pg.on('response', lambda r: err.append(f"{r.status} {r.url.split(str(port))[-1]}") if r.status >= 400 else None)
    pg.goto(f'http://127.0.0.1:{port}/azur-grill/', wait_until='networkidle')
    pg.wait_for_timeout(900)

    pg.click('a[href$="/carte"]')
    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(700)
    print("  1. accueil -> carte     :", pg.url.split(str(port))[-1])

    # le lien exact signale comme cassE
    pg.click('main a[href*="#carte"]')
    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(800)
    print("  2. carte -> accueil     :", pg.url.split(str(port))[-1],
          "| h1 :", pg.inner_text('h1').replace('\n', ' ')[:36])

    pg.click('a[href$="/carte"]')
    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(600)
    pg.click('nav[aria-label="Navigation principale"] a[href*="#avis"]')
    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(900)
    print("  3. depuis carte -> Avis :", pg.url.split(str(port))[-1])
    print("  4. section atteinte     :", pg.evaluate("document.querySelector('#avis').getBoundingClientRect().top < 400"))
    print("  erreurs HTTP :", err or "aucune")
    b.close()
srv.shutdown()
