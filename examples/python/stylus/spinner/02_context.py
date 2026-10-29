"""
@example 02_context.py
Use a spinner as a context manager and change its message while it runs.
"""

import time

from Auctor.Stylus.Spinner import Spinner

with Spinner("step one") as spinner:
    time.sleep(0.2)
    spinner.update("step two")
    time.sleep(0.2)

print("running after the block:", spinner.is_running())
