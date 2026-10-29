import itertools
import sys
import threading
import time
from collections.abc import Callable, Sequence
from typing import TextIO

DEFAULT_FRAMES: tuple[str, ...] = (
    "[=    ]",
    "[==   ]",
    "[===  ]",
    "[==== ]",
    "[=====]",
    "[ ====]",
    "[  ===]",
    "[   ==]",
    "[    =]",
)

_JOIN_TIMEOUT = 1.0


def format_elapsed(seconds: float) -> str:
    """Render seconds as `12.3s`, or `1m 05s` from one minute up."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, rest = divmod(int(seconds), 60)
    return f"{minutes}m {rest:02d}s"


def _validate_frames(frames: Sequence[str]) -> tuple[str, ...]:
    if isinstance(frames, str) or not frames:
        raise ValueError("frames must be a non-empty sequence of strings")
    result = tuple(frames)
    if not all(isinstance(frame, str) for frame in result):
        raise ValueError("frames must be a non-empty sequence of strings")
    return result


def _validate_optional_text(value: str | None, name: str) -> str | None:
    if value is not None and not isinstance(value, str):
        raise ValueError(f"{name} must be a string or None")
    return value


class Spinner:
    """Background terminal spinner that can be stopped and restarted with its configuration kept.

    Frames, stop frame and final message can be changed at any time; a running spinner
    picks up new frames on its next tick, the others on the next stop.
    """

    def __init__(
        self,
        message: str = "",
        *,
        interval: float = 0.08,
        color: str = "",
        endc: str = "",
        frames: Sequence[str] | None = None,
        stop_frame: str | None = None,
        final_message: str | None = None,
        stream: TextIO | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if interval <= 0:
            raise ValueError("interval must be positive")
        self.interval = interval
        self.color = color
        self.endc = endc
        self._message = message
        self._frames = _validate_frames(DEFAULT_FRAMES if frames is None else frames)
        self._stop_frame = _validate_optional_text(stop_frame, "stop_frame")
        self._final_message = _validate_optional_text(final_message, "final_message")
        self._stream = stream
        self._clock = clock

        self._lifecycle = threading.RLock()  # serializes start/stop
        self._state = threading.Lock()  # guards what the worker thread reads and writes
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._last_width = 0
        self._started_at: float | None = None
        self._frozen_elapsed: float | None = None

    # -- configuration -------------------------------------------------

    @property
    def frames(self) -> tuple[str, ...]:
        return self._frames

    @frames.setter
    def frames(self, value: Sequence[str]) -> None:
        validated = _validate_frames(value)
        with self._state:
            self._frames = validated

    @property
    def stop_frame(self) -> str | None:
        return self._stop_frame

    @stop_frame.setter
    def stop_frame(self, value: str | None) -> None:
        self._stop_frame = _validate_optional_text(value, "stop_frame")

    @property
    def final_message(self) -> str | None:
        return self._final_message

    @final_message.setter
    def final_message(self, value: str | None) -> None:
        self._final_message = _validate_optional_text(value, "final_message")

    @property
    def message(self) -> str:
        return self._message

    # -- state ---------------------------------------------------------

    def is_running(self) -> bool:
        thread = self._thread
        return thread is not None and thread.is_alive()

    @property
    def elapsed(self) -> float:
        """Seconds spun: live while running, frozen after stop, 0.0 before the first start."""
        with self._state:
            if self._started_at is None:
                return 0.0
            if self._frozen_elapsed is not None:
                return self._frozen_elapsed
            return self._clock() - self._started_at

    def update(self, message: str) -> None:
        with self._state:
            self._message = message

    # -- lifecycle -----------------------------------------------------

    def start(self) -> None:
        """Start animating; does nothing if already running. Each start begins a new timer."""
        with self._lifecycle:
            if self.is_running():
                return
            with self._state:
                self._started_at = self._clock()
                self._frozen_elapsed = None
                self._last_width = 0
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._spin, name="Auctor-Spinner", daemon=True)
            self._thread.start()

    def stop(self, final_message: str | None = None) -> None:
        """Stop and clear the line, then write the stop frame and final message if any.

        `final_message` overrides the configured one for this call; `{elapsed}` in it is
        replaced by the total time spun. Does nothing if not running.
        """
        with self._lifecycle:
            thread = self._thread
            if thread is None:
                return
            self._stop_event.set()
            thread.join(_JOIN_TIMEOUT)
            self._thread = None

            with self._state:
                if self._started_at is not None:
                    self._frozen_elapsed = self._clock() - self._started_at
                width = self._last_width
                self._last_width = 0
                elapsed = self._frozen_elapsed or 0.0

            text = self._final_line(final_message, elapsed)
            out = self._out()
            try:
                out.write("\r" + " " * width + "\r")
                if text:
                    out.write(f"{self.color}{text}{self.endc}\n")
                out.flush()
            except (OSError, ValueError):  # stream closed during shutdown
                pass

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.stop()
        return False

    # -- internals -----------------------------------------------------

    def _out(self) -> TextIO:
        return self._stream if self._stream is not None else sys.stdout

    def _final_line(self, override: str | None, elapsed: float) -> str:
        message = override if override is not None else self._final_message
        if message is not None:
            # replace(), not format(), so other braces in user text are safe
            message = message.replace("{elapsed}", format_elapsed(elapsed))
        return " ".join(part for part in (self._stop_frame, message) if part)

    def _spin(self) -> None:
        for index in itertools.count():
            with self._state:
                frame = self._frames[index % len(self._frames)]
                text = f"{frame} {self._message}" if self._message else frame
                padding = max(0, self._last_width - len(text))
                self._last_width = len(text)
            out = self._out()
            try:
                out.write(f"\r{self.color}{text}{self.endc}{' ' * padding}")
                out.flush()
            except (OSError, ValueError):
                return
            if self._stop_event.wait(self.interval):
                return
