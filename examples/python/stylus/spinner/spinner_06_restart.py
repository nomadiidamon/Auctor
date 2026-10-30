"""
@example spinner_06_restart.py
Stop a spinner around other output and restart it with its configuration kept.
"""

import time

from Auctor.Stylus.Spinner import Spinner

spinner = Spinner("thinking", frames=["-", "\\", "|", "/"])
spinner.start()
time.sleep(0.2)

# Stopping clears the spinner's line so this output is not appended to a frame.
spinner.stop()
print("tool output goes here")

# Restarting reuses the same message and frames, and begins a new timer.
spinner.start()
time.sleep(0.2)
spinner.stop()
