"""
@example spinner_05_final_message.py
Write a final message with the total time spun, and read the timer directly.
"""

import time

from Auctor.Stylus.Spinner import Spinner

spinner = Spinner("downloading", stop_frame="[=====]", final_message="Done in {elapsed}")
spinner.start()
time.sleep(0.3)

# A message passed to stop() overrides the configured one for that call only.
spinner.stop()

# The elapsed time stays readable, as a number, after the spinner stops.
print("seconds spun:", spinner.elapsed >= 0.3)
