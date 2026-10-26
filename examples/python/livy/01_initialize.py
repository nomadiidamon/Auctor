"""
@example 01_initialize.py
Initialize a Livy instance, with an explicit path and with the defaults.
"""

import tempfile
from pathlib import Path

from Auctor.Livy import Livy

with tempfile.TemporaryDirectory() as tmp:
    # A directory path gets the default "livy.log" filename appended.
    livy = Livy("Example", path=tmp)
    print("before:", livy.is_initialized())

    # initialize() returns False on an expected failure instead of raising.
    if not livy.initialize():
        raise SystemExit(livy.get_last_failure().message)
    print("after:", livy.is_initialized())
    print("log file:", livy.log_file)

    # Repeated initialization is safe and keeps the same log file.
    assert livy.initialize()

    # A path with an extension is used as the log file itself.
    custom = Livy("Custom")
    custom.initialize(Path(tmp) / "nested" / "custom.log")
    print("custom log file:", custom.log_file)

    custom.shutdown()
    livy.shutdown()

# With no path, the log goes to "livy.log" in the current working directory.
