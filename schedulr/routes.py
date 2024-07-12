from aiohttp import web
from aiohttp_swagger import setup_swagger

from schedulr.logger import log_info


class Routes:
    _routes = []

    def __init__(self, app: web.Application):
        self.app = app

    @classmethod
    def register(cls, path: str, method: str):
        def decorator(func):
            log_info(f"Registering route {method} {path}")
            cls._routes.append((path, method, func))
            return func

        return decorator

    def activate(self):
        for path, method, func in self._routes:
            if isinstance(func, staticmethod):
                func = func.__func__
            self.app.router.add_route(method, path, func)
        self.setup_swagger()

    def setup_swagger(self):
        setup_swagger(self.app, swagger_url="/api/v1/docs")

    def __iter__(self):
        return iter(self._routes)
