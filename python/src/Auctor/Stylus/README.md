# Stylus

Stylus is Auctor's terminal utility group. Each subsection is its own subpackage with its own tests and examples.

## Contents

| Subpackage | Purpose | Status |
|---|---|---|
| `Colors` | ANSI escape sequences and `Style()` | Implemented |
| `Spinner` | Background progress animation | Implemented |
| `Prompt` | Interactive prompting | Implemented |
| `TTY` | Terminal-state detection and dimensions | Implemented |

## Quick start

```python
from Auctor.Stylus.Colors import Colors, Style

print(Style("done", Colors.OKGREEN, Colors.BOLD))
```

```python
from Auctor.Stylus.TTY import TTY

terminal = TTY()
print(terminal.is_tty(), terminal.supports_color(), terminal.get_size())
```

## Documentation

- Full reference: [docs/Stylus.md](../../../../docs/Stylus.md)
- Runtime settings: [docs/Runtime.md](../../../../docs/Runtime.md)
- Examples: [examples/python/stylus](../../../../examples/python/stylus)
- Tests: [python/tests/Stylus](../../../../python/tests/Stylus)

## Running the Stylus tests

```bash
python tools/Stylus/run_tests.py
```
