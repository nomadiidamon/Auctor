"""Stylus: terminal utilities (colors, TTY, prompts, spinner)."""

from . import Colors, Prompt, Spinner
from .Colors import Style

# `Colors`, `Prompt` and `Spinner` stay subpackages; the classes are Stylus.<Name>.<Name>.
__all__ = ["Colors", "Prompt", "Spinner", "Style"]
