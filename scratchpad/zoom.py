import functools, threading, sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
class Q(SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0), functools.partial(Q, directory='dist'))
threading.Thread(target=srv.serve_forever,daemon=True).start(); port=srv.server_address[1]
W=int(sys.argv[1]); sel=sys.argv[2]; out=sys.argv[3]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg=b.new_context(viewport={'width':W,'height':900},device_scale_factor=2).new_page()
    pg.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle'); pg.wait_for_timeout(1500)
    el=pg.locator(sel).first
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(1200)
    el.screenshot(path=out)
    print(out,'OK')
    b.close()
srv.shutdown()
