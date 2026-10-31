import pytest

from Auctor import EnvironmentDefaults


def test_qualified_values_use_namespace():
    defaults = EnvironmentDefaults("Stylus.TTY", {"FORCE_COLOR": False, "TERM": "dumb"})

    assert defaults.qualified_values() == {
        "Stylus.TTY.FORCE_COLOR": False,
        "Stylus.TTY.TERM": "dumb",
    }


def test_values_are_immutable_and_detached_from_input():
    values = {"FORCE_COLOR": False}
    defaults = EnvironmentDefaults("Stylus.TTY", values)
    values["FORCE_COLOR"] = True

    assert defaults.values["FORCE_COLOR"] is False
    with pytest.raises(TypeError):
        defaults.values["FORCE_COLOR"] = True
    with pytest.raises(AttributeError, match="immutable"):
        defaults._namespace = "Other"


@pytest.mark.parametrize("namespace", ["", ".TTY", "Stylus.", "Stylus..TTY", "Stylus TTY", None])
def test_invalid_namespace_rejected(namespace):
    with pytest.raises(ValueError):
        EnvironmentDefaults(namespace, {})


@pytest.mark.parametrize("key", ["", "nested.KEY", "bad key", None])
def test_invalid_key_rejected(key):
    with pytest.raises(ValueError):
        EnvironmentDefaults("Stylus.TTY", {key: False})


@pytest.mark.parametrize("value", [[], {}, object()])
def test_non_scalar_values_rejected(value):
    with pytest.raises(ValueError):
        EnvironmentDefaults("Stylus.TTY", {"KEY": value})


def test_aggregate_merges_distinct_namespaces():
    providers = [
        EnvironmentDefaults("Stylus.TTY", {"FORCE_COLOR": False}),
        EnvironmentDefaults("Scriptor.Config", {"FORMAT": "json"}),
    ]

    assert EnvironmentDefaults.aggregate(providers) == {
        "Stylus.TTY.FORCE_COLOR": False,
        "Scriptor.Config.FORMAT": "json",
    }


def test_aggregate_rejects_duplicate_qualified_keys():
    providers = [
        EnvironmentDefaults("Stylus.TTY", {"FORCE_COLOR": False}),
        EnvironmentDefaults("Stylus.TTY", {"FORCE_COLOR": True}),
    ]

    with pytest.raises(ValueError, match="duplicate environment default"):
        EnvironmentDefaults.aggregate(providers)


def test_aggregate_rejects_non_provider():
    with pytest.raises(TypeError, match="EnvironmentDefaults"):
        EnvironmentDefaults.aggregate([object()])