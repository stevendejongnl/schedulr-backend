from schedulr.helpers.dependency_injection import (
    DependencyType,
    register_dependency,
    DependencyInjection,
)


class RealDependency:
    def __init__(self) -> None:
        self.name = "Real"


class FakeDependency:
    def __init__(self, name: str | None = None) -> None:
        self.name = name


@register_dependency(DependencyType.FAKE)
class DecoratedFakeDependency:
    def __init__(self, name: str) -> None:
        self.name = name


class TestDependencyInjection:
    def setup_method(self) -> None:
        self.dependency_injection = DependencyInjection()
        self.dependency_injection.add_dependency(
            "RealDependency", RealDependency, DependencyType.REAL
        )
        self.dependency_injection.add_dependency(
            "FakeDependency", FakeDependency, DependencyType.FAKE
        )

    def test_real_dependency(self) -> None:
        self.dependency_injection.use_type(DependencyType.REAL)
        real_instance = self.dependency_injection.get(RealDependency, FakeDependency)
        assert isinstance(real_instance, RealDependency)

    def test_fake_dependency(self) -> None:
        self.dependency_injection.use_type(DependencyType.FAKE)
        fake_instance = self.dependency_injection.get(RealDependency, FakeDependency)
        assert isinstance(fake_instance, FakeDependency)

    def test_fake_dependency_with_arguments(self) -> None:
        self.dependency_injection.use_type(DependencyType.FAKE)
        fake_instance = self.dependency_injection.get(
            RealDependency, FakeDependency, name="Test"
        )
        assert fake_instance.name == "Test"

    def test_register_decorator(self) -> None:
        self.dependency_injection.use_type(DependencyType.FAKE)
        decorated_fake_instance = self.dependency_injection.get(
            RealDependency, DecoratedFakeDependency, name="Test"
        )
        assert isinstance(decorated_fake_instance, DecoratedFakeDependency)
        assert decorated_fake_instance.name == "Test"
