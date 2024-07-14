from aiohttp import web
from aiohttp.web_request import Request

from schedulr.logger import log_info
from schedulr.modules.user.user_database import FakeUserDatabase
from schedulr.modules.user.user_registration import UserRegistered, FakeUserRegistration
from schedulr.routes import Routes, SwaggerDoc

USER_BASE_PATH = "/user"


class UserRoutes:
    def __init__(self, app: web.Application):
        self.app = app

    @staticmethod
    @Routes.register(
        f"{USER_BASE_PATH}/register",
        "POST",
        SwaggerDoc(
            description="User Register endpoint",
            tags=["User"],
            parameters=[
                {
                    "in": "body",
                    "name": "user",
                    "description": "The user to create.",
                    "schema": {
                        "type": "object",
                        "required": ["userName"],
                        "properties": {
                            # "username": {
                            #     "type": "string"
                            # },
                            "email": {"type": "string"},
                            "password": {"type": "string"},
                        },
                    },
                }
            ],
            responses={"200": {"description": "successful operation"}},
        ),
    )
    async def register(
        request: Request,
        user_registration: FakeUserRegistration = FakeUserRegistration(
            database=FakeUserDatabase()
        ),
    ) -> web.Response:
        json_request = await request.json()
        username = json_request.get("username")
        email = json_request.get("email")
        password = json_request.get("password")

        user_registered = user_registration.register(email, password, username)
        log_info(f"User registered: {user_registered}")

        if isinstance(user_registered, UserRegistered):
            return web.json_response({"message": "User registered successfully"})

        return web.json_response({"message": "User not registered"})
