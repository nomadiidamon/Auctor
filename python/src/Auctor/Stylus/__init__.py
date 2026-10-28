"""Stylus: terminal utilities (colors, TTY, prompts, spinner)."""

from . import Colors
from .Colors import Style

# `Colors` stays the subpackage; its `Colors` class is reached as Stylus.Colors.Colors.
__all__ = ["Colors", "Style"]
