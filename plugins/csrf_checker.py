from fastapi import HTTPException, Request

async def csrf_checker(request: Request) -> None:
    csrf_token: str | None = request.headers.get("X-CSRF-Token")

    if not csrf_token:
        raise HTTPException(status_code=401, detail="X-CSRF-Token not found or invalid")
