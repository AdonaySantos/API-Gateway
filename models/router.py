from pydantic import BaseModel

class Router(BaseModel):
    service: str
    plugins: list[str]
