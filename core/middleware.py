from typing import Any
from fastapi import Request
from plugins.csrf_checker import csrf_checker 

PLUGIN_MAP: dict[str, Any] = {
    "csrf_checker": csrf_checker
}

async def apply_plugins(request: Request, plugins: list[str]):
    for plugin in plugins:
        plugin_func = PLUGIN_MAP.get(plugin)
        if plugin_func:
            await plugin_func(request)
