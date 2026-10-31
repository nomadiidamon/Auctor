"""Runtime lifecycle and Auctor-owned environment settings."""

import threading
from collections.abc import Callable, Iterable, Mapping
from types import MappingProxyType

from Auctor.environment import EnvironmentDefaults, EnvironmentValue


def _default_providers() -> tuple[Callable[[], EnvironmentDefaults], ...]:
    from Auctor.Stylus.TTY import TTYEnvironmentDefaults

    return (TTYEnvironmentDefaults,)


def _validate_overrides(values: Mapping[str, EnvironmentValue]) -> dict[str, EnvironmentValue]:
    if not isinstance(values, Mapping):
        raise ValueError("environment overrides must be a mapping")
    result: dict[str, EnvironmentValue] = {}
    for key, value in values.items():
        if (
            not isinstance(key, str)
            or key.count(".") < 1
            or any(not part for part in key.split("."))
        ):
            raise ValueError("environment override keys must be non-empty dotted names")
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ValueError(f"environment override for {key!r} must be a scalar")
        result[key] = value
    return result


class Runtime:
    """Aggregate package defaults and keep user overrides in memory."""

    def __init__(
        self,
        providers: Iterable[Callable[[], EnvironmentDefaults]] | None = None,
    ) -> None:
        self._providers = tuple(providers) if providers is not None else None
        self._lock = threading.RLock()
        self._initialized = False
        self._values: dict[str, EnvironmentValue] = {}
        self._overrides: dict[str, EnvironmentValue] = {}

    def initialize_auctor(
        self, environment_overrides: Mapping[str, EnvironmentValue] | None = None
    ) -> None:
        """Load declared defaults once and apply any supplied in-memory overrides."""
        with self._lock:
            if not self._initialized:
                providers = (
                    self._providers
                    if self._providers is not None
                    else _default_providers()
                )
                defaults = EnvironmentDefaults.aggregate(provider() for provider in providers)
                self._values = dict(defaults)
                self._initialized = True
            if environment_overrides is not None:
                self.update_auctor_environment(environment_overrides)

    def shutdown_auctor(self) -> None:
        """Clear the current mapping; the next access gathers package defaults again."""
        with self._lock:
            self._initialized = False
            self._values.clear()
            self._overrides.clear()

    def is_auctor_initialized(self) -> bool:
        with self._lock:
            return self._initialized

    def get_auctor_environment(self, namespace: str | None = None) -> Mapping[str, EnvironmentValue]:
        """Return a read-only snapshot, optionally with a namespace prefix removed."""
        self.initialize_auctor()
        with self._lock:
            if namespace is None:
                snapshot = dict(self._values)
            else:
                prefix = f"{namespace}."
                snapshot = {
                    key[len(prefix):]: value
                    for key, value in self._values.items()
                    if key.startswith(prefix)
                }
            return MappingProxyType(snapshot)

    def set_auctor_environment_value(self, key: str, value: EnvironmentValue) -> None:
        """Set or add one Auctor-owned value without changing process environment state."""
        self.update_auctor_environment({key: value})

    def update_auctor_environment(self, values: Mapping[str, EnvironmentValue]) -> None:
        """Apply in-memory overrides, which take precedence over package defaults."""
        validated = _validate_overrides(values)
        self.initialize_auctor()
        with self._lock:
            self._overrides.update(validated)
            self._values.update(validated)


_runtime = Runtime()


def initialize_auctor(
    environment_overrides: Mapping[str, EnvironmentValue] | None = None,
) -> None:
    _runtime.initialize_auctor(environment_overrides)


def shutdown_auctor() -> None:
    _runtime.shutdown_auctor()


def is_auctor_initialized() -> bool:
    return _runtime.is_auctor_initialized()


def get_auctor_environment(namespace: str | None = None) -> Mapping[str, EnvironmentValue]:
    return _runtime.get_auctor_environment(namespace)


def set_auctor_environment_value(key: str, value: EnvironmentValue) -> None:
    _runtime.set_auctor_environment_value(key, value)


def update_auctor_environment(values: Mapping[str, EnvironmentValue]) -> None:
    _runtime.update_auctor_environment(values)