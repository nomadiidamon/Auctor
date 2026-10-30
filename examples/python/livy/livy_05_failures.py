"""
@example livy_05_failures.py
Read the last failure from an instance and from a category.
"""

import tempfile
from pathlib import Path

from Auctor.Livy import Livy

with tempfile.TemporaryDirectory() as tmp:
    app = Livy("App", path=Path(tmp) / "app")
    other = Livy("Other", path=Path(tmp) / "other")
    app.initialize()
    other.initialize()

    importer = app.create_category("Importer")
    filesystem = app.create_category("Filesystem")

    # None until an error or exception has been logged.
    print("before:", app.get_last_failure())

    filesystem.error("cannot read", path="a.txt")
    try:
        raise RuntimeError("halted")
    except RuntimeError as exc:
        importer.exception(exc)

    # Instance-wide: the most recent failure from any category.
    last = app.get_last_failure()
    print("instance:", last.level, "-", last.message)

    # Per category: each keeps its own last failure.
    print("filesystem:", filesystem.get_last_failure().message)
    print("importer:", importer.get_last_failure().level)
    print("same as app.get_last_failure('Filesystem'):",
          app.get_last_failure("Filesystem") is filesystem.get_last_failure())

    # Failure is a frozen record; to_dict() gives a plain dictionary.
    print(last.to_dict()["category"])

    # Instances never share failure state.
    print("other:", other.get_last_failure())

    app.shutdown()
    other.shutdown()
