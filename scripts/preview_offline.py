"""Serve a build with external requests blocked by Content Security Policy."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import sys

class OfflineHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; worker-src 'self' blob:; connect-src 'self'")
        super().end_headers()

ThreadingHTTPServer(("127.0.0.1", 8018), partial(OfflineHandler, directory=sys.argv[1])).serve_forever()
