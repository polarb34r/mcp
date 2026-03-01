# 🎲 MCP Dice Server

Simple MCP server that rolls dice with any number of sides.  
Supports **stdio** (Claude Desktop) and **HTTP/SSE** (Azure / team / browser).  
Auto-deploys to Azure via GitHub Actions on every push to `develop`.

## 🌐 Live Server
```
https://mcp-dice-server.azurewebsites.net/sse
```

---

## 📁 Files

| File | Description |
|------|-------------|
| `dice_mcp_server.py` | stdio server — for Claude Desktop |
| `dice_mcp_server_http_sse.py` | HTTP/SSE server — for Azure / team |
| `dice_mcp_client.py` | Automated test client |
| `requirements.txt` | Python dependencies |
| `startup.sh` | Azure App Service startup script |
| `.github/workflows/azure-deploy.yml` | CI/CD pipeline |

---

## ⚙️ Install

```bash
# Install in the correct Python (same one Claude Desktop uses)
C:\Users\...\Python313\python.exe -m pip install mcp uvicorn httpx
```

---

## 🚀 Run locally

```bash
# stdio (Claude Desktop)
python dice_mcp_server.py

# HTTP/SSE (browser / team / Azure)
python dice_mcp_server_http_sse.py
# → http://localhost:8000/sse
```

---

## 🧪 Test

### MCP Inspector (recommended)
```bash
cd /path/to/this/folder
npx @modelcontextprotocol/inspector python dice_mcp_server.py
# Open http://localhost:5173
```
For HTTP/SSE: change Transport Type to `SSE` → URL: `http://localhost:8000/sse`

### curl
```bash
curl -N https://mcp-dice-server.azurewebsites.net/sse
```

---

## 🖥️ Claude Desktop Config

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

> ⚠️ Claude Desktop does not support HTTP/SSE directly.  
> `mcp-remote` acts as a stdio → HTTP proxy.

---

## ☁️ Azure Deploy (manual)

```bash
az login
az group create --name rg-mcp-dice --location canadaeast
az appservice plan create --name plan-mcp-dice --resource-group rg-mcp-dice --sku B1 --is-linux --location canadaeast
az webapp create --name mcp-dice-server --resource-group rg-mcp-dice --plan plan-mcp-dice --runtime "PYTHON:3.13"
az webapp config set --name mcp-dice-server --resource-group rg-mcp-dice --startup-file "startup.sh"
az webapp deployment source config --name mcp-dice-server --resource-group rg-mcp-dice --repo-url https://github.com/polarb34r/mcp --branch develop --manual-integration
az webapp deployment source sync --name mcp-dice-server --resource-group rg-mcp-dice
```

> ⚠️ Use `canadaeast` — eastus/westus have quota 0 on Test subscriptions.

---

## 🔄 CI/CD — GitHub Actions

Push to `develop` auto-deploys to Azure.

### Required GitHub Secrets

| Secret | Value |
|--------|-------|
| `AZURE_APP_NAME` | `mcp-dice-server` |
| `AZURE_PUBLISH_PROFILE` | XML from Azure Portal → App Service → Get publish profile |

> To enable publish profile: Azure Portal → App Service → Configuration → Platform settings → **SCM Basic Auth Publishing Credentials → On**

---

## 🎲 Tool: roll_dice

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sides` | int | ✅ | Number of sides (min 2) |
| `times` | int | ❌ | How many times to roll (default 1) |

**Examples:**
- *"Roll a d20"* → `sides: 20`
- *"Roll 4d6"* → `sides: 6, times: 4`
- *"Roll a d100"* → `sides: 100`