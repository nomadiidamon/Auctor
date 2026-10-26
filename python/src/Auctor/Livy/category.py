from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .failure import Failure
    from .livy import Livy


class Category:
    """A named logging view onto a Livy instance."""

    def __init__(self, livy: "Livy", name: str) -> None:
        self._livy = livy
        self.name = name

    def info(self, message: str, **context: Any) -> None:
        self._livy._log(logging.INFO, message, self.name, context)

    def debug(self, message: str, **context: Any) -> None:
        self._livy._log(logging.DEBUG, message, self.name, context)

    def warning(self, message: str, **context: Any) -> None:
        self._livy._log(logging.WARNING, message, self.name, context)

    def error(self, message: str, **context: Any) -> None:
        self._livy._log(logging.ERROR, message, self.name, context)

    def exception(self, exc: BaseException, message: str = "", **context: Any) -> None:
        self._livy._log_exception(exc, message, self.name, context)

    def get_last_failure(self) -> Optional[Failure]:
        return self._livy.get_last_failure(self.name)
