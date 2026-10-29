"""Stylus: terminal utilities (colors, TTY, prompts, spinner)."""

from . import Colors, Spinner
from .Colors import Style

# `Colors` and `Spinner` stay subpackages; the classes are Stylus.Colors.Colors and Stylus.Spinner.Spinner.
__all__ = ["Colors", "Spinner", "Style"]
