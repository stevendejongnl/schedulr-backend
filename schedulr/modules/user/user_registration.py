import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from email_validator import validate_email, EmailNotValidError

from schedulr.helpers.dependency_injection import register_dependency, DependencyType
from schedulr.modules.user.user_database import FakeUserDatabase, RealUserDatabase, User


@dataclass(frozen=True)
class UserRegistered:
    email: str


class UserCannotBeRegistered:
    pass


class UserNotRegistered:
    pass


class UserEmailValid:
    pass


class UserEmailNotValid:
    pass


class UserRegistrationBase(ABC):
    @abstractmethod
    def register(
        self, user_email: str, user_password: str
    ) -> UserRegistered | UserNotRegistered:
        pass


@register_dependency(DependencyType.FAKE)
class FakeUserRegistration(UserRegistrationBase):
    _user_email: str
    _user_password: str

    def __init__(self, database: RealUserDatabase | FakeUserDatabase):
        self._database = database

    def _validate_user_email(
        self, user_email: str
    ) -> UserEmailValid | UserEmailNotValid:
        try:
            valid = validate_email(user_email, check_deliverability=False)
            self._user_email = valid.normalized
            return UserEmailValid()
        except EmailNotValidError as error:
            logging.error(error)
            return UserEmailNotValid()

    def register(
        self, email: str, password: str, username: str | None = None
    ) -> UserRegistered | UserNotRegistered:
        user_email_valid = self._validate_user_email(user_email=email)
        if isinstance(user_email_valid, UserEmailNotValid):
            logging.error(f"[FakeUserRegistration] Invalid email: {email}")
            return UserNotRegistered()

        existing_user = self._database.get_user(email=self._user_email)
        if isinstance(existing_user, User):
            logging.error(f"[FakeUserRegistration] User already registered: {email}")
            return UserNotRegistered()

        if username is None:
            username = self._user_email.split("@")[0]

        user = User(email=self._user_email, username=username)
        self._database.add_user(user)
        return UserRegistered(email=self._user_email)


@register_dependency(DependencyType.REAL)
class RealUserRegistration(UserRegistrationBase, ABC):
    pass
