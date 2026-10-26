from __future__ import annotations

import atexit
import logging
import threading
import traceback
import warnings
import weakref
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Union

from .category import Category
from .failure import Failure

PathLike = Union[str, Path]

DEFAULT_LOG_FILENAME = "livy.log"
_FORMAT = "%(asctime)s [%(levelname)s] [%(category)s] %(message)s"

_registry: "weakref.WeakSet[Livy]" = weakref.WeakSet()
_registry_lock = threading.Lock()
_implicit_warned = False


class Livy:
    """A logging/accounting context with instance-specific last-failure state."""

    def __init__(self, name: str = "Auctor", path: Optional[PathLike] = None) -> None:
        self.name = name
        self._path = path
        self._lock = threading.RLock()
        self._logger: Optional[logging.Logger] = None
        self._handler: Optional[logging.Handler] = None
        self._categories: dict[str, Category] = {}
        self._last_failure: Optional[Failure] = None
        self._category_failures: dict[str, Failure] = {}
        self._log_file: Optional[Path] = None

    # Lifecycle

    def initialize(self, path: Optional[PathLike] = None) -> bool:
        """Open the log output; safe to call repeatedly."""
        with self._lock:
            if self._logger is not None:
                return True
            target = path if path is not None else self._path
            try:
                log_file = self._resolve_log_file(target)
                log_file.parent.mkdir(parents=True, exist_ok=True)
                handler = logging.FileHandler(log_file, encoding="utf-8")
            except OSError as e:
                self._record_failure("ERROR", f"Livy initialization failed: {e}", None, e)
                return False
            handler.setFormatter(logging.Formatter(_FORMAT))
            # Unique, non-propagating logger so instances never share state.
            logger = logging.Logger(f"Auctor.Livy.{self.name}.{id(self)}", logging.DEBUG)
            logger.addHandler(handler)
            logger.propagate = False
            self._logger, self._handler, self._log_file = logger, handler, log_file
            with _registry_lock:
                _registry.add(self)
            return True

    def shutdown(self) -> None:
        """Flush and close log output; safe to call repeatedly."""
        with self._lock:
            handler, self._handler, self._logger = self._handler, None, None
            if handler is not None:
                try:
                    handler.flush()
                    handler.close()
                except OSError as e:
                    self._record_failure("ERROR", f"Livy shutdown failed: {e}", None, e)
            with _registry_lock:
                _registry.discard(self)

    def is_initialized(self) -> bool:
        return self._logger is not None

    @property
    def log_file(self) -> Optional[Path]:
        return self._log_file

    # Logging

    def info(self, message: str, **context: Any) -> None:
        self._log(logging.INFO, message, None, context)

    def debug(self, message: str, **context: Any) -> None:
        self._log(logging.DEBUG, message, None, context)

    def warning(self, message: str, **context: Any) -> None:
        self._log(logging.WARNING, message, None, context)

    def error(self, message: str, **context: Any) -> None:
        self._log(logging.ERROR, message, None, context)

    def exception(self, exc: BaseException, message: str = "", **context: Any) -> None:
        self._log_exception(exc, message, None, context)

    # Categories and diagnostics

    def create_category(self, name: str) -> Category:
        if not isinstance(name, str) or not name:
            raise ValueError("Category name must be a non-empty string")
        with self._lock:
            category = self._categories.get(name)
            if category is None:
                category = self._categories[name] = Category(self, name)
            return category

    def get_last_failure(self, category: Optional[str] = None) -> Optional[Failure]:
        if category is not None:
            return self._category_failures.get(category)
        return self._last_failure

    # Internals

    @staticmethod
    def _resolve_log_file(path: Optional[PathLike]) -> Path:
        base = Path(path) if path is not None else Path.cwd()
        if base.is_dir() or base.suffix == "":
            return base / DEFAULT_LOG_FILENAME
        return base

    def _ensure_initialized(self) -> Optional[logging.Logger]:
        global _implicit_warned
        if self._logger is None:
            with _registry_lock:
                first = not _implicit_warned
                _implicit_warned = True
            if first:
                warnings.warn(
                    "Livy used without explicit initialization; call initialize() "
                    "for deterministic lifecycle control.",
                    RuntimeWarning,
                    stacklevel=4,
                )
            self.initialize()
        return self._logger

    def _record_failure(
        self, level: str, message: str, category: Optional[str], exc: Optional[BaseException]
    ) -> None:
        detail = None
        if exc is not None:
            detail = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        self._last_failure = Failure(
            level=level,
            message=message,
            category=category,
            timestamp=datetime.now(timezone.utc).isoformat(),
            exception=detail,
        )
        if category is not None:
            self._category_failures[category] = self._last_failure

    @staticmethod
    def _format(message: str, context: dict[str, Any]) -> str:
        if not context:
            return message
        return message + " " + " ".join(f"{k}={v!r}" for k, v in context.items())

    def _emit(self, level: int, text: str, category: Optional[str], exc_text: Optional[str]) -> None:
        with self._lock:
            logger = self._ensure_initialized()
            if logger is None:
                return
            if exc_text:
                text = f"{text}\n{exc_text}".rstrip()
            logger.log(level, text, extra={"category": category or "-"})

    def _log(self, level: int, message: str, category: Optional[str], context: dict[str, Any]) -> None:
        text = self._format(message, context)
        if level >= logging.ERROR:
            self._record_failure(logging.getLevelName(level), text, category, None)
        self._emit(level, text, category, None)

    def _log_exception(
        self, exc: BaseException, message: str, category: Optional[str], context: dict[str, Any]
    ) -> None:
        text = self._format(message or f"{type(exc).__name__}: {exc}", context)
        self._record_failure("EXCEPTION", text, category, exc)
        detail = self._last_failure.exception if self._last_failure else None
        self._emit(logging.ERROR, text, category, detail)

    def __enter__(self) -> "Livy":
        self.initialize()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.shutdown()


def shutdown_all() -> None:
    """Shut down every active Livy instance."""
    with _registry_lock:
        instances = list(_registry)
    for livy in instances:
        livy.shutdown()


atexit.register(shutdown_all)
