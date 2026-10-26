from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class Failure:
    """Diagnostic detail for the most recent failure of a Livy instance."""

    level: str
    message: str
    category: Optional[str]
    timestamp: str
    exception: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "message": self.message,
            "category": self.category,
            "timestamp": self.timestamp,
            "exception": self.exception,
        }
