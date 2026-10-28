# Livy

Livy is a logging and diagnostics context. It is an object, not a logger factory: each instance has its own log output, categories and last-failure state.

Livy answers "why did this fail, and what was recorded?". Herodotus (Carmen's history) answers "which operation happened and with what outcome?".

## Package layout

| Module | Contents |
|---|---|
| `Auctor/Livy/livy.py` | `Livy`, `shutdown_all()` |
| `Auctor/Livy/category.py` | `Category` |
| `Auctor/Livy/failure.py` | `Failure` |

Everything is importable from `Auctor.Livy`.

## Lifecycle

```python
livy = Livy("App", path="logs")
livy.initialize()      # True on success, False on an expected failure
livy.is_initialized()  # True
livy.shutdown()        # flush and close; safe to repeat
```

- `initialize(path=None)` is idempotent. A path given here overrides the constructor path.
- A directory path (or a path with no extension) gets `livy.log` appended. A path with an extension is used as the log file. With no path, `livy.log` goes in the current working directory. Missing parent directories are created.
- If the log cannot be opened, `initialize()` returns `False` and the reason is available from `get_last_failure()`.
- `shutdown()` is idempotent.
- `with Livy(...) as livy:` initializes on entry and shuts down on exit.
- Every initialized instance is tracked internally. `shutdown_all()` closes them all and is registered to run at interpreter exit.

### Implicit initialization

Logging on an uninitialized instance initializes it with the configured path, and the first time this happens in a process a `RuntimeWarning` recommends explicit initialization. Behavior afterwards is identical to explicit initialization.

## Logging

```python
livy.debug("message", key=value)
livy.info("message")
livy.warning("message")
livy.error("message")
livy.exception(exc, "optional message")
```

Keyword arguments are appended to the message as `key=repr(value)`. `exception()` writes the traceback and uses `Type: message` when no message is given.

Log line format:

```text
<timestamp> [LEVEL] [category] message
```

The category field is `-` for messages logged directly on the instance. Instance loggers do not propagate to the Python root logger.

## Categories

```python
importer = livy.create_category("Importer")
importer.info("step complete", step=1)
```

- Names are plain, non-empty strings chosen by the consumer; an empty or non-string name raises `ValueError`.
- `create_category` with the same name returns the same `Category`.
- A category has `info`, `debug`, `warning`, `error`, `exception` and `get_last_failure`.

## Failures

`Livy.get_last_failure()` returns the most recent `Failure` or `None`.

| Source | Sets last failure? |
|---|---|
| `error()` | yes |
| `exception()` | yes |
| `debug()`, `info()`, `warning()` | no |
| failed `initialize()` / `shutdown()` | yes |

- `livy.get_last_failure()` is instance-wide, across all categories.
- `livy.get_last_failure("Name")` and `category.get_last_failure()` return the last failure logged through that category.
- Failure state is never shared between instances.

`Failure` is a frozen dataclass with `level`, `message`, `category`, `timestamp` (ISO 8601, UTC) and `exception` (formatted traceback or `None`). `to_dict()` returns a plain dictionary.

## Examples

| Example | Shows |
|---|---|
| @ref 01_initialize.py "01_initialize.py" | Initialization with and without paths |
| @ref 02_usage.py "02_usage.py" | Logging levels and context |
| @ref 03_shutdown.py "03_shutdown.py" | Explicit, scoped and global shutdown |
| @ref 04_categories.py "04_categories.py" | Categories |
| @ref 05_failures.py "05_failures.py" | Instance and category failures |

Sources are in `examples/python/livy/`.

## Tests

Tests live in `python/tests/Livy/`: one file each for `Failure`, `Category` and `Livy`, plus an integration file. Run them with `python/scripts/Livy/run_tests.bat` or `.sh`, or `python python/tools/Livy/run_tests.py`.
