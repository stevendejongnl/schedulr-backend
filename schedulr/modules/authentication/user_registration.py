import logging

from email_validator import validate_email, EmailNotValidError


class UserRegistered:
    pass


class UserNotRegistered:
    pass


class UserEmailValid:
    pass


class UserEmailNotValid:
    pass


class UserRegistration:
    _user_email: str
    _user_password: str

    def validate_user_email(self, user_email: str) -> UserEmailValid | UserEmailNotValid:
        try:
            valid = validate_email(user_email, check_deliverability=False)
            self._user_email = valid.normalized
            return UserEmailValid()
        except EmailNotValidError as error:
            logging.error(error)
            return UserEmailNotValid()

    def register(self, user_email: str, user_password: str) -> UserRegistered | UserNotRegistered:
        user_email_valid = self.validate_user_email(user_email=user_email)
        if isinstance(user_email_valid, UserEmailNotValid):
            return UserNotRegistered()

        return UserRegistered()
