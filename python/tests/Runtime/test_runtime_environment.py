import os

import pytest

from Auctor import (
    EnvironmentDefaults,
    initialize_auctor,
    is_auctor_initialized,
    shutdown_auctor,
)
from Auctor.Runtime import Runtime, get_auctor_environment, set_auctor_environment_value


class TTYDefaults(EnvironmentDefaults):
    def __init__(self):
        super().__init__("Stylus.TTY", {"FORCE_COLOR": False, "TERM": ""})


class ExtraDefaults(EnvironmentDefaults):
    def __init__(self):
        super().__init__("Example", {"ENABLED": True})


def test_root_wrappers_name_the_auctor_lifecycle_explicitly():
    shutdown_auctor()
    assert not is_auctor_initialized()

    initialize_auctor({"Stylus.TTY.FORCE_COLOR": True})
    assert is_auctor_initialized()
    assert get_auctor_environment("Stylus.TTY")["FORCE_COLOR"] is True

    set_auctor_environment_value("Stylus.TTY.TERM", "dumb")
    assert get_auctor_environment("Stylus.TTY")["TERM"] == "dumb"
    shutdown_auctor()
    assert not is_auctor_initialized()


def test_runtime_collects_namespaced_package_defaults():
    runtime = Runtime(providers=[TTYDefaults, ExtraDefaults])

    values = runtime.get_auctor_environment()

    assert values == {
        "Stylus.TTY.FORCE_COLOR": False,
        "Stylus.TTY.TERM": "",
        "Example.ENABLED": True,
    }


def test_runtime_empty_provider_catalog_does_not_load_built_in_providers():
    runtime = Runtime(providers=[])

    assert runtime.get_auctor_environment() == {}


def test_runtime_returns_namespace_local_snapshot():
    runtime = Runtime(providers=[TTYDefaults])

    values = runtime.get_auctor_environment("Stylus.TTY")

    assert values == {"FORCE_COLOR": False, "TERM": ""}
    with pytest.raises(TypeError):
        values["FORCE_COLOR"] = True


def test_runtime_override_updates_future_snapshots_only():
    runtime = Runtime(providers=[TTYDefaults])
    old_snapshot = runtime.get_auctor_environment("Stylus.TTY")

    runtime.set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)

    assert old_snapshot["FORCE_COLOR"] is False
    assert runtime.get_auctor_environment("Stylus.TTY")["FORCE_COLOR"] is True


def test_runtime_initialize_accepts_memory_overrides():
    runtime = Runtime(providers=[TTYDefaults])

    runtime.initialize_auctor({"Stylus.TTY.TERM": "dumb"})

    assert runtime.get_auctor_environment("Stylus.TTY")["TERM"] == "dumb"


def test_runtime_shutdown_clears_state_and_overrides():
    runtime = Runtime(providers=[TTYDefaults])
    runtime.set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)
    assert runtime.is_auctor_initialized()

    runtime.shutdown_auctor()

    assert not runtime.is_auctor_initialized()
    assert runtime.get_auctor_environment("Stylus.TTY")["FORCE_COLOR"] is False


def test_runtime_does_not_modify_process_environment(monkeypatch):
    monkeypatch.setenv("AUCTOR_TEST_VALUE", "external")
    runtime = Runtime(providers=[TTYDefaults])

    runtime.initialize_auctor({"Stylus.TTY.FORCE_COLOR": True})

    assert os.environ["AUCTOR_TEST_VALUE"] == "external"
    assert "Stylus.TTY.FORCE_COLOR" not in os.environ


@pytest.mark.parametrize("bad", [[], {}, object()])
def test_runtime_rejects_non_scalar_overrides(bad):
    runtime = Runtime(providers=[TTYDefaults])

    with pytest.raises(ValueError):
        runtime.set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", bad)


def test_runtime_rejects_unqualified_override_keys():
    runtime = Runtime(providers=[TTYDefaults])

    with pytest.raises(ValueError):
        runtime.set_auctor_environment_value("FORCE_COLOR", True)


def test_runtime_validates_empty_override_argument():
    runtime = Runtime(providers=[])

    with pytest.raises(ValueError, match="must be a mapping"):
        runtime.initialize_auctor([])


def test_runtime_rejects_duplicate_defaults():
    runtime = Runtime(providers=[TTYDefaults, TTYDefaults])

    with pytest.raises(ValueError, match="duplicate environment default"):
        runtime.initialize_auctor()

    assert not runtime.is_auctor_initialized()
