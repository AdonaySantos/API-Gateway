from pydantic import BaseModel

class RouteConfig(BaseModel):
    service: str
    plugins: list[str]
