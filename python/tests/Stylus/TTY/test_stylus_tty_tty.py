import io
import os
import sys

import pytest

from Auctor.Runtime import shutdown_auctor, update_auctor_environment
from Auctor.Stylus.TTY import TTY, TTYEnvironmentDefaults
from Auctor.Stylus.TTY import tty as tty_module


class FakeStream:
    def __init__(self, is_tty=True, fd=7):
        self._is_tty = is_tty
        self._fd = fd

    def isatty(self):
        return self._is_tty

    def fileno(self):
        return self._fd


@pytest.fixture(autouse=True)
def reset_runtime(monkeypatch):
    shutdown_auctor()
    monkeypatch.setattr(tty_module, "_is_windows", lambda: False)
    yield
    shutdown_auctor()

def set_tty_settings(**values):
    update_auctor_environment({f"Stylus.TTY.{key}": value for key, value in values.items()})


def test_defaults_are_namespaced_and_exported():
    defaults = TTYEnvironmentDefaults()

    assert defaults.namespace == "Stylus.TTY"
    assert defaults.qualified_values() == {
        "Stylus.TTY.FORCE_COLOR": False,
        "Stylus.TTY.NO_COLOR": False,
        "Stylus.TTY.TERM": "",
    }


def test_is_tty_uses_explicit_stream():
    assert TTY(FakeStream(is_tty=True)).is_tty()
    assert not TTY(FakeStream(is_tty=False)).is_tty()


def test_is_tty_returns_false_without_isatty():
    assert not TTY(io.StringIO()).is_tty()


@pytest.mark.parametrize("error", [OSError, ValueError])
def test_is_tty_returns_false_when_check_fails(error):
    class BrokenStream:
        def isatty(self):
            raise error("failed")

    assert not TTY(BrokenStream()).is_tty()


def test_default_stream_is_resolved_when_method_is_called(monkeypatch):
    terminal = FakeStream(is_tty=True)
    redirected = FakeStream(is_tty=False)
    detector = TTY()

    monkeypatch.setattr(sys, "stdout", terminal)
    assert detector.is_tty()
    monkeypatch.setattr(sys, "stdout", redirected)
    assert not detector.is_tty()


def test_settings_are_snapshotted_when_tty_is_created():
    detector = TTY(FakeStream(is_tty=False))
    set_tty_settings(FORCE_COLOR=True)

    assert not detector.supports_color()
    assert TTY(FakeStream(is_tty=False)).supports_color()


def test_supports_color_requires_tty_by_default(monkeypatch):
    monkeypatch.setattr(tty_module, "_is_windows", lambda: False)
    assert TTY(FakeStream(is_tty=True)).supports_color()
    assert not TTY(FakeStream(is_tty=False)).supports_color()


def test_force_color_enables_redirected_stream():
    set_tty_settings(FORCE_COLOR=True)

    assert TTY(FakeStream(is_tty=False)).supports_color()


def test_no_color_disables_color_on_tty():
    set_tty_settings(NO_COLOR=True)

    assert not TTY(FakeStream(is_tty=True)).supports_color()


def test_force_color_takes_precedence_over_no_color_and_term():
    set_tty_settings(FORCE_COLOR=True, NO_COLOR=True, TERM="dumb")

    assert TTY(FakeStream(is_tty=False)).supports_color()


def test_dumb_term_disables_color():
    set_tty_settings(TERM="DUMB")

    assert not TTY(FakeStream(is_tty=True)).supports_color()


@pytest.mark.parametrize("value", ["1", "true", "yes", "on"])
def test_string_force_color_values_are_enabled(value):
    set_tty_settings(FORCE_COLOR=value)

    assert TTY(FakeStream(is_tty=False)).supports_color()


@pytest.mark.parametrize("value", ["", "0", "false", "no", "off"])
def test_false_string_force_color_values_are_disabled(value):
    set_tty_settings(FORCE_COLOR=value)

    assert not TTY(FakeStream(is_tty=False)).supports_color()


def test_windows_tty_uses_virtual_terminal_helper(monkeypatch):
    calls = []
    monkeypatch.setattr(tty_module, "_is_windows", lambda: True)
    monkeypatch.setattr(tty_module, "_enable_windows_vt", lambda stream: calls.append(stream) or True)
    stream = FakeStream(is_tty=True)

    assert TTY(stream).supports_color()
    assert calls == [stream]


def test_windows_vt_failure_disables_color(monkeypatch):
    monkeypatch.setattr(tty_module, "_is_windows", lambda: True)
    monkeypatch.setattr(tty_module, "_enable_windows_vt", lambda stream: False)

    assert not TTY(FakeStream(is_tty=True)).supports_color()


def test_force_color_on_redirected_windows_stream_does_not_enable_vt(monkeypatch):
    monkeypatch.setattr(tty_module, "_is_windows", lambda: True)
    monkeypatch.setattr(
        tty_module,
        "_enable_windows_vt",
        lambda stream: pytest.fail("VT mode is only for console streams"),
    )
    set_tty_settings(FORCE_COLOR=True)

    assert TTY(FakeStream(is_tty=False)).supports_color()


def test_get_size_uses_terminal_file_descriptor(monkeypatch):
    requested = []
    monkeypatch.setattr(
        tty_module.os,
        "get_terminal_size",
        lambda fd: requested.append(fd) or os.terminal_size((100, 40)),
    )

    assert TTY(FakeStream(is_tty=True, fd=12)).get_size() == os.terminal_size((100, 40))
    assert requested == [12]


def test_get_size_returns_none_for_non_tty(monkeypatch):
    monkeypatch.setattr(
        tty_module.os,
        "get_terminal_size",
        lambda fd: pytest.fail("size lookup should not run for a non-TTY"),
    )

    assert TTY(FakeStream(is_tty=False)).get_size() is None


def test_get_size_returns_none_when_file_descriptor_is_missing():
    assert TTY(io.StringIO()).get_size() is None


@pytest.mark.parametrize("error", [OSError, TypeError, ValueError])
def test_get_size_returns_none_when_size_lookup_fails(monkeypatch, error):
    monkeypatch.setattr(
        tty_module.os,
        "get_terminal_size",
        lambda fd: (_ for _ in ()).throw(error("failed")),
    )

    assert TTY(FakeStream(is_tty=True)).get_size() is None


def test_color_checks_do_not_change_process_environment(monkeypatch):
    monkeypatch.delenv("AUCTOR_TTY_FORCE_COLOR", raising=False)
    set_tty_settings(FORCE_COLOR=True)

    assert TTY(FakeStream(is_tty=False)).supports_color()
    assert "AUCTOR_TTY_FORCE_COLOR" not in os.environ
