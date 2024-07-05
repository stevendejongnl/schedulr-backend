from aiohttp import web
from aiohttp.web_request import Request

from schedulr.routes import Routes


class Dashboard:
    @staticmethod
    @Routes.register('/', 'GET')
    async def index(request: Request) -> web.Response:
        return web.json_response({
            'message': 'Welcome to Schedulr!'
        })
