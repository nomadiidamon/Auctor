# Runtime

Runtime currently aggregates package environment defaults into an Auctor-owned in-memory mapping. The broader runtime lifecycle for other Auctor services remains planned.

## Quick start

```python
from Auctor import initialize_auctor, shutdown_auctor
from Auctor.Runtime import get_auctor_environment, set_auctor_environment_value

initialize_auctor()
set_auctor_environment_value("Stylus.TTY.FORCE_COLOR", True)
print(get_auctor_environment("Stylus.TTY")["FORCE_COLOR"])
shutdown_auctor()
```

Examples:

- [runtime_initialize.py](../../../../examples/python/runtime/runtime_initialize.py)
- [runtime_environment.py](../../../../examples/python/runtime/runtime_environment.py)
- [Auctor environment defaults](../../../../examples/python/auctor)

## Documentation

- Full reference: [docs/Runtime.md](../../../../docs/Runtime.md)
- Architecture: [docs/Architecture.md](../../../../docs/Architecture.md)
- Tests: [python/tests/Runtime](../../../../python/tests/Runtime)

## Running Runtime tests

```bash
python tools/Runtime/run_tests.py
```
