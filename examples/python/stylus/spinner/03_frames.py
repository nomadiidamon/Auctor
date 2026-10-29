"""
@example 03_frames.py
Choose frames in the constructor, or change them before or during a run.
"""

import time

from Auctor.Stylus.Spinner import DEFAULT_FRAMES, Spinner

# Frames given to the constructor replace the default sweep.
spinner = Spinner("dots", frames=[".  ", ".. ", "..."])
spinner.start()
time.sleep(0.3)

# A running spinner picks up new frames on its next tick.
spinner.frames = ["|", "/", "-", "\\"]
time.sleep(0.3)
spinner.stop()

# Frames can also be set while stopped; the next start uses them.
spinner.frames = DEFAULT_FRAMES
print("frames restored:", len(spinner.frames))
