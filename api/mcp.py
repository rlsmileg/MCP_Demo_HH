"""Vercel entrypoint: expose the FastMCP server as an ASGI app.

Vercel's Python runtime auto-detects the module-level `app` variable and
serves it as ASGI. The server logic lives in /server.py at the repo root;
this file just adapts it for Vercel and mounts the MCP routes at the root
of the function so clients can connect to https://<domain>/mcp.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import mcp  # noqa: E402

app = mcp.http_app(path="/")
