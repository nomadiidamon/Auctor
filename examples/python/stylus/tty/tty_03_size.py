"""
@example tty_03_size.py
Read terminal dimensions when available; redirected output returns None.
"""

from Auctor.Stylus.TTY import TTY

size = TTY().get_size()
print("terminal size:", size if size is not None else "unavailable")
