# Login
az login

# Crear grupo de recursos
az group create --name rg-mcp-dice --location eastus

# Crear App Service Plan (gratis)
az appservice plan create --name plan-mcp-dice --resource-group rg-mcp-dice --sku B1 --is-linux

# Crear Web App
az webapp create --name mcp-dice-server --resource-group rg-mcp-dice --plan plan-mcp-dice --runtime "PYTHON:3.13"

# Configurar startup
az webapp config set --name mcp-dice-server --resource-group rg-mcp-dice --startup-file "startup.sh"
```

Luego en GitHub ve a **Settings → Secrets → Actions** y agrega:
- `AZURE_APP_NAME` → `mcp-dice-server`
- `AZURE_PUBLISH_PROFILE` → descárgalo desde Azure Portal → tu App Service → "Get publish profile"

Cuando hagas push a `develop` el pipeline deployará automáticamente. Tu URL quedará:
```
https://mcp-dice-server.azurewebsites.net/sse