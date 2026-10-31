"""Declarative, namespaced environment defaults contributed by Auctor packages."""

from collections.abc import Iterable, Mapping
from types import MappingProxyType
from typing import TypeAlias

EnvironmentValue: TypeAlias = str | int | float | bool | None


class EnvironmentDefaults:
    """Immutable defaults declared by one Auctor package or subpackage."""

    __slots__ = ("_namespace", "_values")

    def __setattr__(self, name: str, value: object) -> None:
        if hasattr(self, name):
            raise AttributeError("environment defaults are immutable")
        object.__setattr__(self, name, value)

    def __init__(self, namespace: str, values: Mapping[str, EnvironmentValue]) -> None:
        if (
            not isinstance(namespace, str)
            or not namespace
            or any(not part.isidentifier() for part in namespace.split("."))
        ):
            raise ValueError("namespace must be a non-empty dotted name")
        if not isinstance(values, Mapping):
            raise ValueError("values must be a mapping")

        copied: dict[str, EnvironmentValue] = {}
        for key, value in values.items():
            if not isinstance(key, str) or not key.isidentifier():
                raise ValueError("default keys must be non-empty, undotted strings")
            if not isinstance(value, (str, int, float, bool, type(None))):
                raise ValueError(f"default value for {key!r} must be a scalar")
            copied[key] = value

        self._namespace = namespace
        self._values = MappingProxyType(copied)

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def values(self) -> Mapping[str, EnvironmentValue]:
        return self._values

    def qualified_values(self) -> Mapping[str, EnvironmentValue]:
        return MappingProxyType(
            {f"{self._namespace}.{key}": value for key, value in self._values.items()}
        )

    @classmethod
    def aggregate(
        cls, providers: Iterable["EnvironmentDefaults"]
    ) -> Mapping[str, EnvironmentValue]:
        result: dict[str, EnvironmentValue] = {}
        for provider in providers:
            if not isinstance(provider, EnvironmentDefaults):
                raise TypeError("providers must contain EnvironmentDefaults instances")
            for key, value in provider.qualified_values().items():
                if key in result:
                    raise ValueError(f"duplicate environment default: {key}")
                result[key] = value
        return MappingProxyType(result)
