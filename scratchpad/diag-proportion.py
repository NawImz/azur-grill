"""Quelle PART de l'element est visible au moment ou son animation part ?
Un seuil calcule sur le seul haut de l'element traite un plat de 90 px
comme une galerie de 800 : le premier est presque entier dans le champ,
la seconde depasse largement en bas."""
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
    pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle'); pg.wait_for_timeout(900)
    pg.evaluate("""() => { window.__d=[];
      const o=new MutationObserver(m=>{for(const x of m){const el=x.target;
        if(el.classList.contains('shown')&&!el.__n){el.__n=1;
          const r=el.getBoundingClientRect();
          const visible=Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
          window.__d.push({h:Math.round(r.height),
                           part:Math.round(visible/r.height*100),
                           top:Math.round(r.top/innerHeight*100),
                           sec:el.closest('section')?.id||'?',
                           txt:(el.textContent||'').trim().slice(0,24)});}}});
      document.querySelectorAll('[data-slice]').forEach(e=>o.observe(e,{attributes:1,attributeFilter:['class']})); }""")
    H=pg.evaluate('document.body.scrollHeight')
    for y in range(0,H-800,140): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(85)
    pg.wait_for_timeout(1500)
    d=pg.evaluate('window.__d')
    print(f"{'section':<10}{'hauteur':>8}{'top':>7}{'VISIBLE':>9}   texte")
    print('-'*72)
    for x in sorted(d, key=lambda z: z['part']):
        alerte = '  <-- part faible' if x['part'] < 60 else ''
        print(f"{x['sec']:<10}{x['h']:>7}px{x['top']:>6}%{x['part']:>8}%   {x['txt']!r}{alerte}")
    faibles=[x for x in d if x['part']<60]
    print(f"\n  {len(faibles)}/{len(d)} elements a moins de 60 % visibles au declenchement")
    b.close()
srv.shutdown()
