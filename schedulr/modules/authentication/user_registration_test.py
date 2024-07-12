class UserRegistered:
    pass


class UserNotRegistered:
    pass


class UserRegistration:
    def register(self, user_email: str, user_password: str) -> UserRegistered | UserNotRegistered:
        return UserRegistered()


class TestUserRegistration:
    def test_that_an_user_can_register(self) -> None:
        user_email = 'user@email.mail'
        user_password = 'password'
        user_registration = UserRegistration()

        user_registered: UserRegistered = user_registration.register(user_email, user_password)
        assert isinstance(user_registered, UserRegistered)
