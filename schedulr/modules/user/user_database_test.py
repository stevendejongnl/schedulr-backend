from schedulr.helpers.dependency_injection import DependencyInjection, DependencyType
from schedulr.modules.user.user_database import (
    FakeUserDatabase,
    RealUserDatabase,
    User,
    UserNotFound,
)


class TestUserDatabase:
    def setup_method(self) -> None:
        self.dependency_injection = DependencyInjection()
        self.dependency_injection.use_type(DependencyType.FAKE)

    def test_that_registered_users_can_be_fetched(self) -> None:
        user_database = self.dependency_injection.get(
            RealUserDatabase, FakeUserDatabase
        )

        user_database.add_user(User(email="user1@email.mail"))
        user_database.add_user(User(email="user2@email.mail"))

        users = user_database.get_users()

        assert len(users) == 2
        assert users == [
            User("user1@email.mail"),
            User("user2@email.mail"),
        ]

    def test_that_specific_user_can_be_fetched(self) -> None:
        user_database = self.dependency_injection.get(
            RealUserDatabase, FakeUserDatabase
        )

        user_database.add_user(User(email="user1@email.mail"))
        user_database.add_user(User(email="user2@email.mail"))

        user = user_database.get_user(email="user2@email.mail")

        assert user == User("user2@email.mail")

    def test_that_fetch_non_existing_user_returns_user_not_found(self) -> None:
        user_database = self.dependency_injection.get(
            RealUserDatabase, FakeUserDatabase
        )

        user_database.add_user(User(email="user1@email.mail"))

        user = user_database.get_user(email="user2@email.mail")

        assert isinstance(user, UserNotFound)
