from aiohttp import web
from aiohttp.web_request import Request

from schedulr.routes import Routes


class MainRoutes:
    @staticmethod
    @Routes.register('/', 'GET')
    async def index(request: Request) -> web.Response:
        routes = Routes(app=request.app)
        return web.json_response({
            'message': 'Welcome to Schedulr!',
            'routes': [route[0] for route in routes]
        })
