import logging

from email_validator import validate_email, EmailNotValidError

from schedulr.helpers.dependency_injection import register_dependency, DependencyType
from schedulr.modules.user.user_database import FakeUserDatabase, RealUserDatabase, User


class UserRegistered:
    pass


class UserCannotBeRegistered:
    pass


class UserNotRegistered:
    pass


class UserEmailValid:
    pass


class UserEmailNotValid:
    pass


@register_dependency(DependencyType.FAKE)
class FakeUserRegistration:
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
        self, user_email: str, user_password: str
    ) -> UserRegistered | UserNotRegistered:
        user_email_valid = self._validate_user_email(user_email=user_email)
        if isinstance(user_email_valid, UserEmailNotValid):
            logging.error(f"User email is not valid: {user_email}")
            return UserNotRegistered()

        existing_user = self._database.get_user(email=self._user_email)
        if isinstance(existing_user, User):
            logging.error(f"User already registered: {existing_user.email}")
            return UserNotRegistered()

        user = User(email=self._user_email)
        self._database.add_user(user)
        return UserRegistered()


@register_dependency(DependencyType.REAL)
class RealUserRegistration:
    pass
