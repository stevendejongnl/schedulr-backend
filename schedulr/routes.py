from dataclasses import dataclass, asdict, field

from aiohttp import web
from aiohttp_swagger import setup_swagger

from schedulr.logger import log_info
from schedulr.version import VERSION


def json_response(response_class):
    return web.json_response(
        {
            "status": response_class.status,
            "message": response_class.message,
        },
        status=response_class.status,
    )


def responses(response_classes: set):
    return {
        str(response_class.status): {"description": response_class.message}
        for response_class in response_classes
    }


@dataclass(frozen=True)
class SwaggerDoc:
    tags: list[str]
    description: str
    responses: dict
    requestBody: dict = field(default_factory=lambda: {})
    consumes: list[str] = field(default_factory=lambda: ["multipart/form-data"])
    produces: list[str] = field(default_factory=lambda: ["application/json"])
    parameters: list[dict] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


class Routes:
    _routes = []

    def __init__(self, app: web.Application):
        self.app = app

    @classmethod
    def register(cls, path: str, method: str, swagger_doc: SwaggerDoc | None = None):
        def decorator(func):
            log_info(f"Registering route {method} {path}")
            cls._routes.append((path, method, func, swagger_doc))
            return func

        return decorator

    def activate(self):
        paths = {}
        for path, method, func, swagger_doc in self._routes:
            self.app.router.add_route(method, path, func)
            if swagger_doc:
                swagger_doc_dict = swagger_doc.to_dict()
                paths[path] = {method.lower(): swagger_doc_dict}
        self.setup_swagger(paths)

    def setup_swagger(self, paths: dict):
        swagger_info = {
            "openapi": "3.0.0",
            "info": {
                "title": "Schedulr API",
                "version": VERSION,
            },
            "paths": paths,
        }

        setup_swagger(
            self.app,
            swagger_url="/api/v1/docs",
            swagger_from_file=None,
            swagger_info=swagger_info,
            api_version=VERSION,
            ui_version=3,
        )

    def __iter__(self):
        return iter(self._routes)
