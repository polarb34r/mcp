"""
Simple MCP Server - Dice Roller
Allows rolling dice with any number of sides.

Install dependencies:
    pip install mcp

Run the server:
    python dice_mcp_server.py
"""

import random
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Create the MCP server
app = Server("dice-roller")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="roll_dice",
            description="Roll a dice with a given number of sides. You provide the number of sides (e.g. 4, 6, 8, 10, 12, 20, 100).",
            inputSchema={
                "type": "object",
                "properties": {
                    "sides": {
                        "type": "integer",
                        "description": "Number of sides on the dice (e.g. 6 for a standard dice)",
                        "minimum": 2,
                    },
                    "times": {
                        "type": "integer",
                        "description": "How many times to roll the dice (default: 1)",
                        "minimum": 1,
                        "default": 1,
                    },
                },
                "required": ["sides"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    if name == "roll_dice":
        sides = arguments["sides"]
        times = arguments.get("times", 1)

        if sides < 2:
            return [types.TextContent(type="text", text="Error: A dice must have at least 2 sides.")]

        rolls = [random.randint(1, sides) for _ in range(times)]
        total = sum(rolls)

        if times == 1:
            result = f"🎲 Rolled a d{sides}: **{rolls[0]}**"
        else:
            result = (
                f"🎲 Rolled {times}x d{sides}: {rolls}\n"
                f"Total: {total} | Average: {total / times:.1f}"
            )

        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
