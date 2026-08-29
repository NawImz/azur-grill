#!/usr/bin/env python3
"""Screenshot d'un build statique. Serveur ephemere + Chromium preinstalle."""
import argparse, functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

CHROME = '/opt/pw-browsers/chromium'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='dist')
    ap.add_argument('--out', required=True)
    ap.add_argument('--path', default='/')
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--fullpage', action='store_true')
    ap.add_argument('--settle', type=int, default=1200)
    ap.add_argument('--section')
    ap.add_argument('--click')
    ap.add_argument('--reduced-motion', action='store_true')
    a = ap.parse_args()

    h = functools.partial(SimpleHTTPRequestHandler, directory=a.dir)
    h.log_message = lambda *x, **k: None
    srv = ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    errors = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME)
            ctx = b.new_context(viewport={'width': a.width, 'height': a.height},
                                device_scale_factor=2,
                                reduced_motion='reduce' if a.reduced_motion else 'no-preference')
            pg = ctx.new_page()
            pg.on('console', lambda m: errors.append(f'[{m.type}] {m.text}') if m.type in ('error','warning') else None)
            pg.on('pageerror', lambda e: errors.append(f'[pageerror] {e}'))
            pg.on('requestfailed', lambda r: errors.append(f'[netfail] {r.url}'))
            pg.goto(f'http://127.0.0.1:{port}{a.path}', wait_until='networkidle')
            if a.click:
                pg.click(a.click); pg.wait_for_timeout(600)
            if a.fullpage:
                pg.evaluate("""async () => { await new Promise(r => {
                    let y = 0; const step = () => { y += window.innerHeight * 0.8;
                    window.scrollTo(0, y); if (y < document.body.scrollHeight) setTimeout(step, 90);
                    else { window.scrollTo(0,0); setTimeout(r, 400); } }; step(); }); }""")
            pg.wait_for_timeout(a.settle)
            tgt = pg.locator(a.section) if a.section else pg
            tgt.screenshot(path=a.out, full_page=a.fullpage and not a.section)
            ow = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            print(f'OK {a.out} {a.width}px overflow_h={ow}px')
            for e in errors[:12]: print('  CONSOLE', e)
            if not errors: print('  console: propre')
            b.close()
    finally:
        srv.shutdown()

if __name__ == '__main__':
    sys.exit(main())
