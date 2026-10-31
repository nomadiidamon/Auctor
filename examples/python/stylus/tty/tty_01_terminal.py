"""
@example tty_01_terminal.py
Inspect whether the current output stream is attached to a terminal.
"""

from Auctor import initialize_auctor
from Auctor.Stylus.TTY import TTY

initialize_auctor()
tty = TTY()
print("is terminal:", tty.is_tty())
print("supports color:", tty.supports_color())
