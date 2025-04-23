from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.yaml_loader import YamlLoader
from core.middleware import apply_plugins
from core.proxy import proxy_request

app = FastAPI()
yaml_loader = YamlLoader("./config.yaml")

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_handler(request: Request, full_path: str) -> JSONResponse:
    route_match = yaml_loader.get_route_match(f"/{full_path}")

    if not route_match:
        return JSONResponse(status_code=404, content={"error": "Rota não encontrada"})

    service_url = yaml_loader.get_service_for_route(f"/{full_path}")
    plugins = yaml_loader.get_plugins_for_route(f"/{full_path}")

    try:
        _ = await apply_plugins(request, plugins)
        return await proxy_request(request, service_url)
    except Exception as e:
        return JSONResponse(status_code=404, content={"error": f"Error interno: {str(e)}"})
