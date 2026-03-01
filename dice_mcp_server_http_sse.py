"""
Simple MCP Server - Dice Roller (HTTP/SSE) - Pure ASGI approach
Install: pip install mcp uvicorn
Run:     python dice_mcp_server_http.py
"""

import random
import uvicorn
import os

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp import types

# Create MCP server
mcp_server = Server("dice-roller-http")


@mcp_server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="roll_dice",
            description="Roll a dice with a given number of sides in azure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sides": {
                        "type": "integer",
                        "description": "Number of sides on the dice (e.g. 6, 20, 100)",
                        "minimum": 2,
                    },
                    "times": {
                        "type": "integer",
                        "description": "How many times to roll (default: 1)",
                        "minimum": 1,
                        "default": 1,
                    },
                },
                "required": ["sides"],
            },
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "roll_dice":
        sides = arguments["sides"]
        times = arguments.get("times", 1)
        rolls = [random.randint(1, sides) for _ in range(times)]
        total = sum(rolls)
        if times == 1:
            result = f"🎲 Rolled a DICE {sides}: **{rolls[0]}**"
        else:
            result = (
                f"🎲 ROLLED {times}x d{sides}: {rolls}\n"
                f"Total: {total} | Average: {total / times:.1f}"
            )
        return [types.TextContent(type="text", text=result)]
    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# Setup SSE transport
sse_transport = SseServerTransport("/messages/")


# Pure ASGI app - bypasses FastAPI/Starlette routing entirely
async def asgi_app(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")

        if path == "/sse" and scope["method"] == "GET":
            async with sse_transport.connect_sse(scope, receive, send) as (r, w):
                await mcp_server.run(r, w, mcp_server.create_initialization_options())

        elif path.startswith("/messages/") and scope["method"] == "POST":
            await sse_transport.handle_post_message(scope, receive, send)

        else:
            # 404 for unknown routes
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b"Not found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🎲 Dice MCP Server running at http://0.0.0.0:{port}")
    print(f"   SSE endpoint: http://0.0.0.0:{port}/sse")
    uvicorn.run(asgi_app, host="0.0.0.0", port=port)