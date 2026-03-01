# 🎲 MCP Dice Server

Simple MCP server that rolls dice with any number of sides. Supports both **stdio** (Claude Desktop) and **HTTP/SSE** (Azure / team / browser).

## Live Server
```
https://mcp-dice-server.azurewebsites.net/sse
```

## Files

| File | Description |
|------|-------------|
| `dice_mcp_server.py` | stdio server for Claude Desktop |
| `dice_mcp_server_http_sse.py` | HTTP/SSE server for Azure / team |
| `dice_mcp_client.py` | Automated test client |
| `requirements.txt` | Python dependencies |
| `startup.sh` | Azure App Service startup script |

## Install

```bash
pip install mcp uvicorn httpx
```

## Run locally

```bash
# stdio (for Claude Desktop)
python dice_mcp_server.py

# HTTP/SSE (for browser / team)
python dice_mcp_server_http_sse.py
# → http://localhost:8000/sse
```

## Test with MCP Inspector

```bash
cd /path/to/this/folder
npx @modelcontextprotocol/inspector python dice_mcp_server.py
# Open http://localhost:5173
```

For HTTP/SSE: change Transport Type to `SSE` and enter URL `http://localhost:8000/sse`

## Claude Desktop Config

```json
{
  "mcpServers": {
    "dice-roller": {
      "command": "python",
      "args": ["C:\\path\\to\\dice_mcp_server.py"]
    },
    "dice-roller-azure": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp-dice-server.azurewebsites.net/sse"]
    }
  }
}
```

> ⚠️ Claude Desktop does not support HTTP/SSE directly. Use `mcp-remote` as a stdio → HTTP proxy.

## Azure Deploy

```bash
az login
az group create --name rg-mcp-dice --location canadaeast
az appservice plan create --name plan-mcp-dice --resource-group rg-mcp-dice --sku B1 --is-linux --location canadaeast
az webapp create --name mcp-dice-server --resource-group rg-mcp-dice --plan plan-mcp-dice --runtime "PYTHON:3.13"
az webapp config set --name mcp-dice-server --resource-group rg-mcp-dice --startup-file "startup.sh"
az webapp deployment source config --name mcp-dice-server --resource-group rg-mcp-dice --repo-url https://github.com/polarb34r/mcp --branch develop --manual-integration
az webapp deployment source sync --name mcp-dice-server --resource-group rg-mcp-dice
```

## Tool: roll_dice

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sides` | int | ✅ | Number of sides (min 2) |
| `times` | int | ❌ | How many times to roll (default 1) |

Example: *"Roll 3d20"* → `sides: 20, times: 3`
