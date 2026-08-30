"""Ou se trouve REELLEMENT la « ligne » qui fait apparaitre un element ?

Deux positions differentes, souvent confondues :
  - DEPART   : l'element commence a bouger (opacite quitte 0)
  - PERCU    : l'element devient franchement lisible (opacite > 0,5)
Entre les deux il s'ecoule ~0,85 s pendant lesquelles la page continue de
defiler : l'element remonte. C'est le PERCU que l'oeil appelle « la ligne ».
"""
import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

class Q(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

srv = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory='dist'))
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

SONDE = """() => {
  window.__m = [];
  const suivis = [...document.querySelectorAll('[data-slice]')].map(el => ({el, depart:null, percu:null}));
  const boucle = () => {
    const vh = innerHeight;
    for (const s of suivis) {
      if (s.percu !== null) continue;
      const o = parseFloat(getComputedStyle(s.el).opacity);
      const top = s.el.getBoundingClientRect().top / vh * 100;
      if (s.depart === null && o > 0.01) s.depart = top;
      if (s.depart !== null && o > 0.5) {
        s.percu = top;
        window.__m.push({depart: Math.round(s.depart), percu: Math.round(top),
                         sec: s.el.closest('section')?.id || '?',
                         txt: (s.el.textContent || '').trim().slice(0, 26)});
      }
    }
    requestAnimationFrame(boucle);
  };
  requestAnimationFrame(boucle);
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
    pg.wait_for_timeout(900)
    pg.evaluate(SONDE)
    H = pg.evaluate('document.body.scrollHeight')
    # defilement realiste : petits pas rapproches, pas de saut de 140 px
    pas, pause = int(sys.argv[1]) if len(sys.argv) > 1 else 30, int(sys.argv[2]) if len(sys.argv) > 2 else 60
    print(f"  defilement : {pas} px toutes les {pause} ms = {pas/pause*1000:.0f} px/s\n")
    for y in range(0, H - 900, pas):
        pg.evaluate(f'window.scrollTo(0,{y})')
        pg.wait_for_timeout(pause)
    pg.wait_for_timeout(1500)
    d = pg.evaluate('window.__m')
    b.close()
srv.shutdown()

print(f"{'section':<10}{'DEPART':>9}{'PERCU':>9}   texte")
print('-' * 74)
for x in d:
    print(f"{x['sec']:<10}{x['depart']:>8}%{x['percu']:>8}%   {x['txt']!r}")
if d:
    md = sum(x['depart'] for x in d) / len(d)
    mp = sum(x['percu'] for x in d) / len(d)
    print(f"\n  {len(d)} elements")
    print(f"  DEPART  moyenne {md:.0f}% du viewport  (min {min(x['depart'] for x in d)}%, max {max(x['depart'] for x in d)}%)")
    print(f"  PERCU   moyenne {mp:.0f}% du viewport  (min {min(x['percu'] for x in d)}%, max {max(x['percu'] for x in d)}%)")
