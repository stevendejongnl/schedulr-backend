from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any


class DependencyType(Enum):
    REAL = "real"
    FAKE = "fake"


class DependencyNotFound(Exception):
    pass


@dataclass(frozen=True)
class Dependency:
    instance: Callable
    type: DependencyType


class DependencyInjection:
    _instance = None
    _dependency_type: DependencyType = DependencyType.REAL
    dependencies: dict[str, Dependency] = {}

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls._instance:
            cls._instance = super(DependencyInjection, cls).__new__(
                cls, *args, **kwargs
            )
            cls._instance.dependencies = {}
        return cls._instance

    def use_type(self, dependency_type: DependencyType) -> None:
        self._dependency_type = dependency_type

    def add_dependency(
        self, class_name: str, instance: Callable, dependency_type: DependencyType
    ) -> None:
        self.dependencies[class_name] = Dependency(
            instance=instance,
            type=dependency_type,
        )

    def _get_dependency(self, cls: Any, *args: Any, **kwargs: Any) -> Any:
        dependency = self.dependencies.get(cls.__name__)
        if not dependency:
            raise DependencyNotFound

        return dependency.instance(*args, **kwargs)

    def get(self, real: Any, fake: Any, *args: Any, **kwargs: Any) -> Any:
        if self._dependency_type == DependencyType.FAKE:
            return self._get_dependency(fake, *args, **kwargs)
        return self._get_dependency(real, *args, **kwargs)


def register_dependency(dependency_type: DependencyType) -> Callable:
    def decorator(cls: Any) -> Any:
        dependency_injection = DependencyInjection()
        dependency_injection.add_dependency(cls.__name__, cls, dependency_type)
        return cls

    return decorator
