"""
Simple MCP Client - Dice Roller Test
Tests the dice_mcp_server.py by connecting and calling roll_dice.

Run after starting the server:
    python dice_mcp_client.py
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["dice_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}\n")

            # --- Roll different dice ---
            dice_examples = [
                {"sides": 6},           # Standard d6
                {"sides": 20},          # D&D d20
                {"sides": 4},           # d4
                {"sides": 100},         # d100
                {"sides": 6, "times": 3},  # Roll 3d6
            ]

            for args in dice_examples:
                result = await session.call_tool("roll_dice", arguments=args)
                print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
