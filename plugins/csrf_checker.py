from fastapi import Request

async def csrf_checker(request: Request) -> None:
    csrf_token: str | None = request.headers.get("X-CSRF-Token")

    if not csrf_token:
        print(f"doesn't have an X-CSRF-Token")
    print(f"has an X-CSRF-Token: {csrf-token}")
