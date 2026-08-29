#!/usr/bin/env python3
"""
QA mesuree : contraste par echantillonnage pixel du COMPOSITE reel,
overflow, cibles tactiles, console. Sortie OK/FAIL par zone avec ratio.

Deux pieges evites, tires du catalogue d'erreurs :
 - getBoundingClientRect() sur un bloc centre renvoie la boite pleine largeur,
   pas les glyphes : on passe par Range.getClientRects() (§4.8).
 - getComputedStyle().color peut renvoyer oklch() sur Chromium recent, et
   Tailwind v4 emet justement de l'oklch : la couleur est resolue par un
   round-trip <canvas>, jamais par un regex CSS (§4.9).
"""
import functools, threading, sys, io, json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image

CHROME = '/opt/pw-browsers/chromium'

def lin(c):
    c /= 255
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4

def lum(rgb):
    r, g, b = rgb[:3]
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)

JS_ZONES = """
() => {
  const out = [];
  const sel = 'h1,h2,h3,p,a,li,span,dt,dd,blockquote,button';
  for (const el of document.querySelectorAll(sel)) {
    if (el.children.length && ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const txt = (el.textContent || '').trim();
    if (!txt) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < 0.5) continue;
    if (el.offsetWidth <= 1 || el.offsetHeight <= 1) continue; // sr-only : hors ecran, pas a mesurer
    // bbox collee aux glyphes, pas la boite du bloc
    const r = document.createRange(); r.selectNodeContents(el);
    const rects = [...r.getClientRects()].filter(x => x.width > 2 && x.height > 2);
    if (!rects.length) continue;
    const b = rects[0];
    if (b.bottom < 0 || b.top > innerHeight) continue;
    // Test de visibilite reelle : un element passant sous une barre fixe
    // (la barre mobile, l'en-tete) serait mesure contre CETTE barre et
    // produirait un echec de contraste imaginaire.
    const cx2 = b.x + b.width / 2, cy2 = b.y + b.height / 2;
    if (cx2 >= 0 && cy2 >= 0 && cx2 <= innerWidth && cy2 <= innerHeight) {
      const dessus = document.elementFromPoint(cx2, cy2);
      if (dessus && dessus !== el && !el.contains(dessus) && !dessus.contains(el)) continue;
    }
    // couleur resolue par round-trip canvas (l'oklch casse tout parsing texte)
    const cv = document.createElement('canvas'); cv.width = cv.height = 1;
    const cx = cv.getContext('2d'); cx.fillStyle = cs.color; cx.fillRect(0,0,1,1);
    const px = cx.getImageData(0,0,1,1).data;
    const fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight) || 400;
    out.push({
      texte: txt.slice(0, 44),
      x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
      couleur: [px[0], px[1], px[2]],
      grand: fs >= 24 || (fs >= 18.66 && fw >= 700),
      tag: el.tagName.toLowerCase(),
    });
  }
  return out;
}
"""

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else 'dist'
    path = sys.argv[2] if len(sys.argv) > 2 else '/'
    widths = [int(w) for w in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['375', '768', '1440'])]

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *a): pass

    srv = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=directory))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    echecs = 0

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for W in widths:
            ctx = b.new_context(viewport={'width': W, 'height': 900}, device_scale_factor=2)
            pg = ctx.new_page()
            msgs = []
            pg.on('console', lambda m: msgs.append(f'[{m.type}] {m.text}') if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e: msgs.append(f'[pageerror] {e}'))
            pg.on('requestfailed', lambda r: msgs.append(f'[netfail] {r.url}'))
            pg.goto(f'http://127.0.0.1:{port}{path}', wait_until='networkidle')
            pg.wait_for_timeout(1600)

            print(f'\n{"="*74}\n  {path}  @  {W}px\n{"="*74}')

            ov = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            print(f'  overflow horizontal : {ov}px  {"OK" if ov == 0 else "FAIL"}')
            if ov: echecs += 1

            H = pg.evaluate('document.body.scrollHeight')
            paliers = [int(H * k / 5) for k in range(5)]
            pires = []
            for y in paliers:
                pg.evaluate(f'window.scrollTo(0,{min(y, max(0, H-900))})')
                pg.wait_for_timeout(700)
                zones = pg.evaluate(JS_ZONES)
                if not zones: continue
                # composite reel : on masque le texte et on photographie le fond
                pg.evaluate("""() => {
                  document.querySelectorAll('h1,h2,h3,p,a,li,span,dt,dd,blockquote,button')
                    .forEach(e => { e.dataset._c = e.style.color; e.style.color = 'transparent'; });
                }""")
                pg.wait_for_timeout(180)
                shot = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
                pg.evaluate("""() => {
                  document.querySelectorAll('[data-_c]').forEach(e => { e.style.color = e.dataset._c; delete e.dataset._c; });
                }""")
                s = shot.width / W
                for z in zones:
                    # La bbox d'un Range englobe la boite de ligne, plus haute que les
                    # glyphes : sans marge, le p05 attrape un voisin (un bouton colore
                    # au-dessus) et invente un echec. On resserre, et on n'echantillonne
                    # que les zones entierement dans le viewport.
                    if z['y'] < 0 or z['y'] + z['h'] > 900: continue
                    mx = max(1, int(z['w'] * 0.04)); my = max(2, int(z['h'] * 0.18))
                    x0 = int((z['x'] + mx) * s); x1 = int((z['x'] + z['w'] - mx) * s)
                    y0 = int((z['y'] + my) * s); y1 = int((z['y'] + z['h'] - my) * s)
                    if x1 - x0 < 4 or y1 - y0 < 4: continue
                    px = list(shot.crop((x0, y0, x1, y1)).getdata())
                    if not px: continue
                    # p05 de luminance : le fond le plus defavorable sous le texte
                    px.sort(key=lum)
                    fond = px[max(0, int(len(px) * 0.05))] if lum(z['couleur']) > lum(px[len(px)//2]) else px[min(len(px)-1, int(len(px)*0.95))]
                    r = ratio(z['couleur'], fond)
                    seuil = 3.0 if z['grand'] else 4.5
                    if r < seuil:
                        pires.append((r, seuil, z['texte'], z['tag'], f'#{fond[0]:02X}{fond[1]:02X}{fond[2]:02X}'))

            vus = set(); uniq = []
            for it in sorted(pires):
                if it[2] in vus: continue
                vus.add(it[2]); uniq.append(it)
            if uniq:
                print(f'  contraste : {len(uniq)} zone(s) SOUS le seuil')
                for r, seuil, t, tag, f in uniq[:8]:
                    print(f'      FAIL {r:5.2f}:1 (min {seuil}) <{tag}> fond {f} — "{t}"')
                echecs += len(uniq)
            else:
                print('  contraste : OK — toutes les zones mesurees au-dessus du seuil')

            pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(400)
            petites = pg.evaluate("""() => {
              const out = [];
              for (const el of document.querySelectorAll('a[href],button')) {
                const r = el.getBoundingClientRect();
                if (r.width <= 1 || r.height <= 1) continue; // sr-only, visible seulement au focus
                if (getComputedStyle(el).display === 'none') continue;
                if (r.width < 44 || r.height < 44) out.push({t:(el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,30), w:Math.round(r.width), h:Math.round(r.height)});
              }
              return out;
            }""")
            if W <= 768:
                if petites:
                    print(f'  cibles tactiles : {len(petites)} sous 44px  FAIL')
                    for c in petites[:6]: print(f'      {c["w"]}x{c["h"]}  "{c["t"]}"')
                    echecs += len(petites)
                else:
                    print('  cibles tactiles : OK — toutes >= 44px')

            if msgs:
                print(f'  console : {len(msgs)} probleme(s)  FAIL')
                for m in msgs[:6]: print('      ', m[:100])
                echecs += len(msgs)
            else:
                print('  console : OK — 0 erreur, 0 warning, 0 requete echouee')
            ctx.close()
        b.close()
    srv.shutdown()
    print(f'\n{"="*74}\n  TOTAL : {echecs} point(s) en echec\n{"="*74}')
    return 1 if echecs else 0

if __name__ == '__main__':
    sys.exit(main())
