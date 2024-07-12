from schedulr.modules.authentication.user_registration import UserRegistered, UserNotRegistered, UserRegistration


class TestUserRegistration:
    def test_that_an_user_can_register(self) -> None:
        user_email = 'user@email.mail'
        user_password = 'password'
        user_registration = UserRegistration()

        user_registered = user_registration.register(user_email, user_password)
        assert isinstance(user_registered, UserRegistered)

    def test_that_an_user_cannot_register(self) -> None:
        user_email = 'Invalid email'
        user_password = 'password'
        user_registration = UserRegistration()

        user_not_registered = user_registration.register(user_email, user_password)
        assert isinstance(user_not_registered, UserNotRegistered)
