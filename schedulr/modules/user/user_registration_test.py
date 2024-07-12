from schedulr.helpers.dependency_injection import DependencyInjection, DependencyType
from schedulr.modules.user.user_database import RealUserDatabase, FakeUserDatabase, User
from schedulr.modules.user.user_registration import (
    RealUserRegistration,
    FakeUserRegistration,
    UserRegistered,
    UserNotRegistered,
)


class TestUserRegistration:
    def setup_method(self) -> None:
        self.dependency_injection = DependencyInjection()
        self.dependency_injection.use_type(DependencyType.FAKE)
        self.user_database = self.dependency_injection.get(
            RealUserDatabase, FakeUserDatabase
        )
        self.user_registration = self.dependency_injection.get(
            RealUserRegistration, FakeUserRegistration, database=self.user_database
        )

    def test_that_an_user_can_register(self) -> None:
        user_email = "user@email.mail"
        user_password = "password"

        user_registered = self.user_registration.register(user_email, user_password)
        assert isinstance(user_registered, UserRegistered)

    def test_that_an_user_cannot_register(self) -> None:
        user_email = "Invalid email"
        user_password = "password"

        user_not_registered = self.user_registration.register(user_email, user_password)
        assert isinstance(user_not_registered, UserNotRegistered)

    def test_that_you_can_not_register_with_an_already_registered_email(self) -> None:
        first_user_email = "user@email.mail"
        first_user_password = "password"
        self.user_registration.register(first_user_email, first_user_password)

        second_user_email = "user@email.mail"
        second_user_password = "another_password"
        second_user_registered = self.user_registration.register(
            second_user_email, second_user_password
        )

        assert isinstance(second_user_registered, UserNotRegistered)

    def test_that_registered_users_can_be_fetched_by_database(self) -> None:
        self.user_registration.register("user1@email.mail", "password1")
        self.user_registration.register("user2@email.mail", "password2")

        users = self.user_database.get_users()

        assert len(users) == 2
        assert users == [User("user1@email.mail"), User("user2@email.mail")]
