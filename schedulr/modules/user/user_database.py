from dataclasses import dataclass

from schedulr.helpers.dependency_injection import register_dependency, DependencyType


@dataclass(frozen=True)
class User:
    email: str


class UserNotFound:
    pass


@register_dependency(DependencyType.FAKE)
class FakeUserDatabase:
    _users: list[User]

    def __init__(self) -> None:
        self._users = []

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def get_users(self) -> list[User]:
        return self._users

    def get_user(self, email: str) -> User | UserNotFound:
        return next(
            (user for user in self._users if user.email == email), UserNotFound()
        )


@register_dependency(DependencyType.REAL)
class RealUserDatabase:
    def add_user(self, user: User) -> None:
        pass

    def get_user(self, email: str) -> None:
        pass
