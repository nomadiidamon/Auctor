import logging
import warnings

import pytest

from Auctor.Livy import Livy
from Auctor.Livy import livy as livy_module


def test_initialize_creates_default_log_in_directory(tmp_path):
    livy = Livy(path=tmp_path)
    assert not livy.is_initialized()
    assert livy.initialize()
    assert livy.is_initialized()
    assert livy.log_file == tmp_path / "livy.log"
    livy.shutdown()


def test_initialize_with_explicit_file_path(tmp_path):
    target = tmp_path / "sub" / "custom.log"
    livy = Livy()
    assert livy.initialize(target)
    livy.info("hi")
    livy.shutdown()
    assert "hi" in target.read_text()


def test_default_path_is_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    livy = Livy()
    livy.initialize()
    livy.shutdown()
    assert (tmp_path / "livy.log").exists()


def test_initialize_and_shutdown_are_safe_to_repeat(tmp_path):
    livy = Livy(path=tmp_path)
    assert livy.initialize() and livy.initialize()
    livy.shutdown()
    livy.shutdown()
    assert not livy.is_initialized()


def test_initialize_failure_returns_false_and_records(tmp_path):
    blocker = tmp_path / "file.txt"
    blocker.write_text("x")
    livy = Livy()
    assert livy.initialize(blocker / "child" / "a.log") is False
    assert "initialization failed" in livy.get_last_failure().message


def test_levels_written(tmp_path):
    with Livy(path=tmp_path) as livy:
        livy.debug("d")
        livy.info("i")
        livy.warning("w")
        livy.error("e", code=2)
    text = (tmp_path / "livy.log").read_text()
    assert "[DEBUG] [-] d" in text
    assert "[INFO] [-] i" in text
    assert "[WARNING] [-] w" in text
    assert "[ERROR] [-] e code=2" in text


def test_only_error_and_exception_set_failure(tmp_path):
    with Livy(path=tmp_path) as livy:
        livy.info("i")
        livy.warning("w")
        assert livy.get_last_failure() is None
        livy.error("e")
        assert livy.get_last_failure().level == "ERROR"
        livy.exception(KeyError("k"))
        failure = livy.get_last_failure()
        assert failure.level == "EXCEPTION"
        assert "KeyError" in failure.exception


def test_exception_custom_message(tmp_path):
    with Livy(path=tmp_path) as livy:
        livy.exception(ValueError("v"), "while parsing", line=3)
        assert livy.get_last_failure().message == "while parsing line=3"


def test_last_failure_isolated_between_instances(tmp_path):
    a, b = Livy("A", tmp_path / "a"), Livy("B", tmp_path / "b")
    a.initialize()
    b.initialize()
    a.error("boom")
    assert a.get_last_failure().message == "boom"
    assert b.get_last_failure() is None
    a.shutdown()
    b.shutdown()


def test_categories_are_per_instance(tmp_path):
    a, b = Livy("A", tmp_path / "a"), Livy("B", tmp_path / "b")
    assert a.create_category("X") is not b.create_category("X")


def test_instance_logger_does_not_propagate(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        with Livy(path=tmp_path) as livy:
            livy.info("quiet")
    assert "quiet" not in caplog.text


def test_registry_tracks_active_instances(tmp_path):
    livy = Livy(path=tmp_path)
    livy.initialize()
    assert livy in livy_module._registry
    livy_module.shutdown_all()
    assert not livy.is_initialized()
    assert livy not in livy_module._registry


def test_implicit_initialization_warns_once(tmp_path, monkeypatch):
    monkeypatch.setattr(livy_module, "_implicit_warned", False)
    a, b = Livy("A", tmp_path / "a"), Livy("B", tmp_path / "b")
    with pytest.warns(RuntimeWarning):
        a.info("x")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        b.info("y")
    assert a.is_initialized() and b.is_initialized()
    a.shutdown()
    b.shutdown()
