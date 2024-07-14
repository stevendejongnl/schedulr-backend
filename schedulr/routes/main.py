from aiohttp import web
from aiohttp.web_request import Request

from schedulr.routes import Routes, SwaggerDoc


class MainRoutes:
    @staticmethod
    @Routes.register(
        "/",
        "GET",
        SwaggerDoc(
            tags=["Main"],
            description="Main endpoint",
            responses={"200": {"description": "successful operation"}},
        ),
    )
    async def index(request: Request) -> web.Response:
        routes = Routes(app=request.app)
        return web.json_response(
            {
                "message": "Welcome to Schedulr!",
                "routes": [route[0] for route in routes],
            }
        )
