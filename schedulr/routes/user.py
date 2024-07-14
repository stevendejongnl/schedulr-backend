from dataclasses import dataclass

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from schedulr.modules.user.user_database import FakeUserDatabase
from schedulr.modules.user.user_registration import UserRegistered, FakeUserRegistration
from schedulr.routes import Routes, SwaggerDoc, json_response, responses

USER_BASE_PATH = "/user"


@dataclass(frozen=True)
class UserRegisterResponse:
    status: int = 201
    message: str = "User registered successfully"


@dataclass(frozen=True)
class UserRegisterFailedResponse:
    status: int = 400
    message: str = "User not registered"


class UserRoutes:
    def __init__(self, app: web.Application):
        self.app = app

    @staticmethod
    @Routes.register(
        f"{USER_BASE_PATH}/register",
        "POST",
        SwaggerDoc(
            tags=["User"],
            description="User Register endpoint",
            requestBody={
                "description": "The user to create.",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "required": ["email", "password"],
                            "properties": {
                                "username": {"type": "string"},
                                "email": {"type": "string"},
                                "password": {"type": "string"},
                            },
                        }
                    }
                },
            },
            responses=responses(
                {
                    UserRegisterResponse(),
                    UserRegisterFailedResponse(),
                }
            ),
        ),
    )
    async def register(
        request: Request,
        user_registration: FakeUserRegistration = FakeUserRegistration(
            database=FakeUserDatabase()
        ),
    ) -> Response:
        json_request = await request.json()
        username = json_request.get("username")
        email = json_request.get("email")
        password = json_request.get("password")

        user_registered = user_registration.register(email, password, username)

        if isinstance(user_registered, UserRegistered):
            return json_response(UserRegisterResponse())

        return json_response(UserRegisterFailedResponse())
