"""Step-by-step diagnostic of FastMCP HTTP app construction."""

import traceback
from http.server import BaseHTTPRequestHandler

_status = "starting"

try:
    from fastmcp import FastMCP
    _status = "imported FastMCP"

    inst = FastMCP("SetupCheck")
    _status = "instantiated FastMCP"

    @inst.tool
    def ping() -> str:
        return "pong"

    _status = "registered tool"

    starlette_app = inst.http_app(path="/")
    _status = f"got http_app, type: {type(starlette_app).__name__}"

    routes = [
        getattr(r, "path", repr(r)) for r in getattr(starlette_app, "routes", [])
    ]
    _status += f", routes: {routes}"

except Exception as exc:  # noqa: BLE001
    _status = (
        f"FAILED at step: {_status}\n"
        f"{type(exc).__name__}: {exc}\n\n"
        f"{traceback.format_exc()}"
    )


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write((_status + "\n").encode())
