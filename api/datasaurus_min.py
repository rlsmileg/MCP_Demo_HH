"""Minimal FastMCP ASGI app to isolate routing failure."""

from fastmcp import FastMCP

inst = FastMCP("Minimal")


@inst.tool
def hello() -> str:
    return "hi"


_starlette = inst.http_app(path="/")


async def app(scope, receive, send):
    await _starlette(scope, receive, send)
