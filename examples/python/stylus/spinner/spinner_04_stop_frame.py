"""
@example spinner_04_stop_frame.py
Leave a consistent final frame behind instead of a blank line.
"""

import time

from Auctor.Stylus.Colors import Colors
from Auctor.Stylus.Spinner import Spinner

with Spinner("working", stop_frame="[=====]", color=Colors.OKGREEN, endc=Colors.ENDC):
    time.sleep(0.3)

# The final frame stays on its own line, so later output starts cleanly.
print("next output")
