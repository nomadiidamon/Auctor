import os
import sys
from typing import TextIO

from Auctor.Runtime import get_auctor_environment


def _enabled(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in ("", "0", "false", "no", "off")
    return False


def _is_windows() -> bool:
    return os.name == "nt"


def _enable_windows_vt(stream: TextIO) -> bool:
    try:
        import ctypes
        import msvcrt
        from ctypes import wintypes

        handle = wintypes.HANDLE(msvcrt.get_osfhandle(stream.fileno()))
        mode = wintypes.DWORD()
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel32.GetConsoleMode.restype = wintypes.BOOL
        kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel32.SetConsoleMode.restype = wintypes.BOOL
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False

        enable_virtual_terminal_processing = 0x0004
        if mode.value & enable_virtual_terminal_processing:
            return True
        return bool(
            kernel32.SetConsoleMode(
                handle, mode.value | enable_virtual_terminal_processing
            )
        )
    except (AttributeError, OSError, TypeError, ValueError, ctypes.ArgumentError):
        return False


class TTY:
    """Inspect terminal attachment, color support, and terminal dimensions."""

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream = stream
        self._settings = dict(get_auctor_environment("Stylus.TTY"))

    def is_tty(self) -> bool:
        stream = self._out()
        try:
            return bool(stream.isatty())
        except (AttributeError, OSError, ValueError):
            return False

    def supports_color(self) -> bool:
        stream = self._out()
        force_color = _enabled(self._settings.get("FORCE_COLOR", False))
        no_color = _enabled(self._settings.get("NO_COLOR", False))

        if force_color:
            if _is_windows() and self.is_tty():
                return _enable_windows_vt(stream)
            return True
        if no_color or str(self._settings.get("TERM", "")).lower() == "dumb":
            return False
        if not self.is_tty():
            return False
        if _is_windows():
            return _enable_windows_vt(stream)
        return True

    def get_size(self) -> os.terminal_size | None:
        if not self.is_tty():
            return None
        try:
            return os.get_terminal_size(self._out().fileno())
        except (AttributeError, OSError, TypeError, ValueError):
            return None

    def _out(self) -> TextIO:
        return self._stream if self._stream is not None else sys.stdout