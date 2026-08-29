"""Mesure OU se trouve un element quand son animation part.
Trop haut dans le viewport = l'animation est finie avant qu'on le regarde."""
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
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle'); pg.wait_for_timeout(1000)
    # descente progressive, on note la position de chaque element au moment ou
    # il recoit la classe `shown`
    pg.evaluate("""() => {
      window.__releves = [];
      const obs = new MutationObserver(muts => {
        for (const m of muts) {
          const el = m.target;
          if (el.classList.contains('shown') && !el.__note) {
            el.__note = true;
            const r = el.getBoundingClientRect();
            window.__releves.push({
              pct: Math.round(r.top / innerHeight * 100),
              txt: (el.textContent||'').trim().slice(0,32)
            });
          }
        }
      });
      document.querySelectorAll('[data-slice]').forEach(e =>
        obs.observe(e, {attributes:true, attributeFilter:['class']}));
    }""")
    H=pg.evaluate('document.body.scrollHeight')
    # descente assez rapide pour rester sous le filet de 4 s : on mesure
    # ainsi le declenchement reel, pas le rattrapage.
    for y in range(0, H-800, 200):
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(45)
    pg.wait_for_timeout(900)
    rel = pg.evaluate('window.__releves')
    print(f"{'position du haut de l element au declenchement':<48}{'texte'}")
    print('-'*84)
    for r in rel[:14]:
        barre = '#' * max(1, int(r['pct']/4))
        print(f"  {r['pct']:>3}% du viewport {barre:<26} {r['txt']!r}")
    if rel:
        moy = sum(r['pct'] for r in rel)/len(rel)
        # Bonne fenetre : 65-95%. En dessous, l'element est deja au centre
        # et l'animation arrive en retard ; au-dessus de 100%, il est encore
        # sous l'ecran et l'animation se joue sans spectateur.
        hors = [r for r in rel if r['pct'] > 95 or r['pct'] < 45]
        etat = 'OK — chaque element s anime en entrant dans le champ' if not hors \
               else f'{len(hors)} element(s) hors fenetre 45-95%'
        print(f"\n  moyenne {moy:.0f}% | min {min(r['pct'] for r in rel)}% | max {max(r['pct'] for r in rel)}%")
        print(f"  --> {etat}")
    b.close()
srv.shutdown()
