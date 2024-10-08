from abc import ABC, abstractmethod
from dataclasses import dataclass

from schedulr.helpers.dependency_injection import register_dependency, DependencyType


@dataclass(frozen=True)
class User:
    email: str
    username: str | None = None


class UserNotFound:
    pass


class UserDatabase(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user(self, email: str) -> User | UserNotFound:
        pass


@register_dependency(DependencyType.FAKE)
class FakeUserDatabase(UserDatabase):
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
class RealUserDatabase(UserDatabase, ABC):
    pass
