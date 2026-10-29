"""
@example 01_basic.py
Start a spinner, let it run, and stop it; stopping clears the line.
"""

import time

from Auctor.Stylus.Colors import Colors
from Auctor.Stylus.Spinner import Spinner

spinner = Spinner("loading", color=Colors.OKCYAN, endc=Colors.ENDC)
spinner.start()
print_state = spinner.is_running()
time.sleep(0.3)

# Starting again is safe, and so is stopping when nothing is running.
spinner.start()
spinner.stop()
spinner.stop()

print("was running:", print_state)
print("running now:", spinner.is_running())
