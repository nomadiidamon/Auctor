"""
@example 03_shutdown.py
Shut Livy down explicitly, with a context manager, and for every instance at once.
"""

import tempfile
from pathlib import Path

from Auctor.Livy import Livy, shutdown_all

with tempfile.TemporaryDirectory() as tmp:
    # Explicit shutdown flushes and closes the log; calling it again is harmless.
    livy = Livy("Explicit", path=Path(tmp) / "explicit")
    livy.initialize()
    livy.info("working")
    livy.shutdown()
    livy.shutdown()
    print("explicit:", livy.is_initialized())

    # The context manager initializes on entry and shuts down on exit.
    with Livy("Scoped", path=Path(tmp) / "scoped") as scoped:
        scoped.info("working")
    print("scoped:", scoped.is_initialized())

    # shutdown_all() closes every active instance; it also runs automatically at exit.
    first = Livy("First", path=Path(tmp) / "first")
    second = Livy("Second", path=Path(tmp) / "second")
    first.initialize()
    second.initialize()
    shutdown_all()
    print("all:", first.is_initialized() or second.is_initialized())
