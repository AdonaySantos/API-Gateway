from fastapi import Request
from fastapi.responses import JSONResponse
import httpx

async def proxy_request(request: Request, target_url: str) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        url = f"{target_url}{request.url.path}"

        body = await request.body()

        proxied_response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=body,
            params=dict(request.query_params)
        )

        try:
            json_data = proxied_response.json()
        except Exception:
            return JSONResponse(
                content={"error": "Resposta do serviço não é JSON válido"},
                status_code=502
            )

        return JSONResponse(
            content=json_data,
            status_code=proxied_response.status_code
        )
