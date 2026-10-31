"""Stylus: terminal utilities (colors, TTY, prompts, spinner)."""

from . import Colors, Prompt, Spinner, TTY
from .Colors import Style

# `Colors`, `Prompt`, `Spinner` and `TTY` stay subpackages.
__all__ = ["Colors", "Prompt", "Spinner", "Style", "TTY"]
