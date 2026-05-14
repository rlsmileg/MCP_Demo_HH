"""Diagnostic: does `import fastmcp` succeed on Vercel?"""

from http.server import BaseHTTPRequestHandler

try:
    import fastmcp
    _result = f"fastmcp imported OK, version: {getattr(fastmcp, '__version__', 'unknown')}"
except Exception as exc:  # noqa: BLE001
    _result = f"fastmcp import FAILED: {type(exc).__name__}: {exc}"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write((_result + "\n").encode())
