from dataclasses import dataclass

from schedulr.helpers.dependency_injection import register_dependency, DependencyType


@dataclass(frozen=True)
class User:
    email: str


class UserNotFound:
    pass


@register_dependency(DependencyType.FAKE)
class FakeUserDatabase:
    def __init__(self):
        self._users: list[User] = []

    def add_user(self, user: User):
        self._users.append(user)

    def get_users(self) -> list[User]:
        return self._users

    def get_user(self, email: str) -> User | UserNotFound:
        return next(
            (
                user for user in self._users
                if user.email == email
            ),
            UserNotFound()
        )


@register_dependency(DependencyType.REAL)
class RealUserDatabase:
    # raise NotImplementedError
    pass
