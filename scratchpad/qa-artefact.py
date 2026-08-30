"""Aucun bloc vide a l'ecran dans l'artefact, aux trois vitesses de defilement."""
import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

DIR = '/tmp/claude-0/-home-user-azur-grill/91ca05d7-38e3-58aa-9d3e-ad6d8e9ecfdd/scratchpad'
FICHIER = 'azur-grill-preview.html'

class Q(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

srv = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=DIR))
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

VIDES = """() => {
  const vh = innerHeight, vides = [];
  document.querySelectorAll('[data-slice]').forEach(el => {
    if (el.classList.contains('shown')) return;
    const r = el.getBoundingClientRect();
    const visible = Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
    // Un bloc qui pointe a peine au bord bas n'est pas percu comme « vide » :
    // il se revelera en continuant. Le defaut, c'est un bloc franchement
    // dans le champ qui reste blanc une fois le defilement arrete.
    if (visible >= r.height * 0.5 || visible >= vh * 0.35) vides.push({
      top: Math.round(r.top), h: Math.round(r.height), vis: Math.round(visible),
      pctEl: Math.round(visible / r.height * 100), pctEcran: Math.round(visible / vh * 100),
      txt: (el.textContent || '').trim().slice(0, 30)});
  });
  return vides;
}"""

profils = {'lent': (100, 160), 'normal': (300, 90), 'brutal': (900, 40)}
echec = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    for nom, (pas, pause) in profils.items():
        pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        pg.goto(f'http://127.0.0.1:{port}/{FICHIER}', wait_until='networkidle')
        pg.wait_for_timeout(900)
        H = pg.evaluate('document.body.scrollHeight')
        pire = []
        for y in range(0, H, pas):
            pg.evaluate(f'window.scrollTo(0,{y})')
            pg.wait_for_timeout(pause)
            v = pg.evaluate(VIDES)
            # on ne juge qu'apres l'arret : le filet attend 600 ms
            if v:
                pg.wait_for_timeout(750)
                v = pg.evaluate(VIDES)
            if len(v) > len(pire): pire = v
        pg.evaluate(f'window.scrollTo(0,{H})'); pg.wait_for_timeout(1200)
        v = pg.evaluate(VIDES)
        if len(v) > len(pire): pire = v
        total = pg.evaluate("document.querySelectorAll('[data-slice]').length")
        vus = pg.evaluate("document.querySelectorAll('[data-slice].shown').length")
        etat = 'OK  ' if not pire else 'FAIL'
        print(f"{etat} {nom:<7} {vus}/{total} revelés | vides a l'ecran : {len(pire)}")
        for x in pire:
            print(f"       top={x['top']} h={x['h']} visible={x['vis']}px "
                  f"= {x['pctEl']}% de l'element, {x['pctEcran']}% de l'ecran  {x['txt']!r}")
        echec += len(pire)
        pg.close()
    b.close()
srv.shutdown()
print('\n' + ('TOUT OK' if not echec else f'{echec} bloc(s) vide(s)'))
sys.exit(1 if echec else 0)
