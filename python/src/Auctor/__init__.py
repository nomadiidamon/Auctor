"""Auctor: filesystem, parsing, terminal, and logging utilities."""

from .environment import EnvironmentDefaults
from .Runtime import initialize_auctor, is_auctor_initialized, shutdown_auctor

__version__ = "0.1.0"

__all__ = ["__version__", "EnvironmentDefaults", "initialize_auctor", "shutdown_auctor", "is_auctor_initialized"]
