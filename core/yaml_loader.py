import os, yaml, time, threading
from re import sub, match
from typing import Any
from models.route_config import RouteConfig

class YamlLoader:
    def __init__(self, config_path: str) -> None:
        self.config_path: str = config_path
        self._config_data: dict[str, RouteConfig] = {}
        self.last_modified: float | None = None

        self.load_config()
        self.start_auto_reload()

    
    def load_config(self) -> None:
        try: 
            with open(self.config_path, "r", encoding="utf-8") as file:
                self.raw_data: dict[str, list[dict[str, Any]]] = yaml.safe_load(file)

            self.last_modified = os.path.getmtime(self.config_path)
            self._config_data.clear()

            for route in self.raw_data.get("routes", []):
                path: str = route.get("path", "")
                service: str = route.get("service", "")
                plugins: list[str] = route.get("plugins", [])

                if path and service:
                    self._config_data[path] = RouteConfig(service=service, plugins=plugins)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")

    def has_file_change(self):
        try:
            current_modified = os.path.getmtime(self.config_path)
            return current_modified != self.last_modified
        except FileNotFoundError:
            return False

    def start_auto_reload(self) -> None:
        def watcher():
            while True:
                time.sleep(1)
                if self.has_file_change():
                    print("Reload arquivo de configuração alterado. Recarregando...")
                    self.load_config()
                    
        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()

    def get_route_match(self, path: str) -> str | None:
        for route_path in self._config_data.keys():
            if route_path == path or self._is_path_match(route_path, path):
                return route_path
        return None

    def get_service_for_route(self, path: str) -> str:
        route = self.get_route_match(path)
        if route:
            return self._config_data[route].service
        return ""

    def get_plugins_for_route(self, path: str) -> list[str]:
        route = self.get_route_match(path)
        if route:
            return self._config_data[route].plugins
        return []

    def _is_path_match(self, route_path: str, incoming_path: str) -> bool:
        pattern = sub(r"\{[^/]+\}", r"[^/]+", route_path)
        return match(f"^{pattern}$", incoming_path) is not None
