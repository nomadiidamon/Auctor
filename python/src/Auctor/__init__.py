"""Auctor: A standalone utility library for diagnostics, filesystem operations, data processing, and terminal interaction."""

from .environment import EnvironmentDefaults
from .Runtime import initialize_auctor, is_auctor_initialized, shutdown_auctor

__version__ = "0.2.1"

__all__ = ["__version__", "EnvironmentDefaults", "initialize_auctor", "shutdown_auctor", "is_auctor_initialized"]
