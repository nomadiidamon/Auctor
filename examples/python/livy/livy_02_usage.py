"""
@example livy_02_usage.py
Log at every level and attach context to a message.
"""

import tempfile

from Auctor.Livy import Livy

with tempfile.TemporaryDirectory() as tmp:
    livy = Livy("Example", path=tmp)
    livy.initialize()

    livy.debug("loading settings")
    livy.info("started", version="0.1.0")
    livy.warning("cache is cold")
    livy.error("could not open file", path="a.txt")

    try:
        int("not a number")
    except ValueError as exc:
        # exception() logs the traceback; an optional message replaces the default text.
        livy.exception(exc, "bad input", field="count")

    livy.shutdown()
    print(livy.log_file.read_text())
