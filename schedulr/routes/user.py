import logging

from aiohttp import web
from aiohttp.web_request import Request

from schedulr.routes import Routes


USER_BASE_PATH = "/user"


class UserRoutes:

    @Routes.register(f"{USER_BASE_PATH}/register", "POST")
    async def register(self, request: Request) -> web.Response:
        user_email = request.get("user_email")
        user_password = request.get("user_password")

        logging.info(f"{user_email=}, {user_password}=")

        return web.json_response({})
