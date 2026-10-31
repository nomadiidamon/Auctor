# Runtime

Runtime coordinates Auctor-wide settings and, as more services are implemented, their lifecycle. The current Python implementation aggregates namespaced package defaults into an Auctor-owned in-memory mapping. It does not write to process-global `os.environ`.

## Package defaults

`Auctor.EnvironmentDefaults` is the root declaration type for subpackage settings. Each package contributes an instance through an exported child class with a namespace and local defaults. Runtime uses an explicit provider catalog, so declarations do not depend on import-time registration.

```python
from Auctor import EnvironmentDefaults

class TTYEnvironmentDefaults(EnvironmentDefaults):
    def __init__(self):
        super().__init__("Stylus.TTY", {"FORCE_COLOR": False})
```

Defaults are copied and exposed as read-only mappings. Runtime flattens them into dotted keys (`Stylus.TTY.FORCE_COLOR`) and rejects duplicate keys during aggregation.
### Examples

| Example | Shows |
|---|---|
| @ref auctor_environment_defaults.py "auctor_environment_defaults.py" | A package declaration with namespaced values |
| @ref auctor_environment_aggregate.py "auctor_environment_aggregate.py" | Aggregating defaults from separate packages |

Sources are in `examples/python/auctor/`.

## Runtime API

```python
from Auctor import initialize_auctor, shutdown_auctor
from Auctor.Runtime import get_auctor_environment, set_auctor_environment_value

initialize_auctor()
settings = get_auctor_environment("Stylus.TTY")
set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)
print(get_auctor_environment("Stylus.TTY")["FORCE_COLOR"])
shutdown_auctor()
```

- `initialize_auctor(environment_overrides=None)` aggregates package defaults and applies any full-key in-memory overrides.
- `get_auctor_environment(namespace=None)` initializes defaults when needed and returns a read-only snapshot. With a namespace, the prefix is removed from returned keys.
- `set_auctor_environment_value(key, value)` and `update_auctor_environment(mapping)` update Auctor's in-memory values. Values must be scalar (`str`, `int`, `float`, `bool`, or `None`) and keys must be dotted names.
- `shutdown_auctor()` clears the current mapping; the next access gathers defaults again.
- `is_auctor_initialized()` reports whether the mapping is currently initialized.

The module-level wrappers and `Runtime` object methods use the same explicit snake_case names.

Updating Runtime settings affects snapshots requested afterward. Existing snapshots remain unchanged. A TTY instance takes its own namespace snapshot on construction.

## Overrides and persistence

Current precedence is package defaults, then in-memory overrides. Once Scriptor.Config is implemented, a package-wide configuration file will add a middle layer:

```text
package defaults < file overrides < in-memory overrides
```

Runtime will own loading and updating that file through Scriptor.Config. File access is not part of the current implementation.

## Current scope

Runtime currently manages package environment defaults only. It does not yet initialize Livy, Herodotus, or other lifecycle-managed services. See [Architecture](Architecture.md) for broader Auctor status.

## Examples

| Example | Shows |
|---|---|
| @ref runtime_initialize.py "runtime_initialize.py" | Explicit Auctor initialization and shutdown |
| @ref runtime_environment.py "runtime_environment.py" | Reading and overriding Auctor-owned settings |

Sources are in `examples/python/runtime/`.

The root `EnvironmentDefaults` examples are in `examples/python/auctor/`.

## Tests

Runtime aggregation and override tests live in `python/tests/Runtime/`. Run them with `python/scripts/Runtime/run_tests.bat` or `.sh`, or `python python/tools/Runtime/run_tests.py`.
