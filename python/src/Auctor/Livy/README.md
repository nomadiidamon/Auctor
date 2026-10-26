# Livy

Livy is Auctor's logging and diagnostics context. A `Livy` object owns a log file, named categories, and its own last-failure record.

Livy explains what went wrong; it does not decide how callers handle failure. Expected operational failures elsewhere in Auctor return simple values (`None`, `False`), and the detail is kept here.

## Contents

| Name | Purpose |
|---|---|
| `Livy` | Logging/accounting context: lifecycle, levels, categories, last failure |
| `Category` | Named view onto a `Livy` with the same logging methods |
| `Failure` | Immutable record of the most recent error or exception |
| `shutdown_all()` | Shuts down every active `Livy` instance |

## Quick start

```python
from Auctor.Livy import Livy

with Livy("App", path="logs") as livy:
    importer = livy.create_category("Importer")
    importer.info("started")
    importer.error("failed", step=2)
    print(importer.get_last_failure().message)
```

## Documentation

- Full reference: [docs/Livy.md](../../../../docs/Livy.md)
- Examples: [examples/python/livy](../../../../examples/python/livy)
- Tests: [python/tests/Livy](../../../../python/tests/Livy)

## Running the Livy tests

```bash
python tools/Livy/run_tests.py
```
