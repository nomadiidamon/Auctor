# Stylus

Stylus is Auctor's terminal utility group. Each subsection is its own subpackage with its own tests and examples.

## Contents

| Subpackage | Purpose | Status |
|---|---|---|
| `Colors` | ANSI escape sequences and `Style()` | Implemented |
| `Spinner` | Background progress animation | Planned |
| `Prompt` | Interactive prompting | Planned |
| `TTY` | Terminal-state detection | Planned |

## Quick start

```python
from Auctor.Stylus.Colors import Colors, Style

print(Style("done", Colors.OKGREEN, Colors.BOLD))
```

## Documentation

- Full reference: [docs/Stylus.md](../../../../docs/Stylus.md)
- Examples: [examples/python/stylus](../../../../examples/python/stylus)
- Tests: [python/tests/Stylus](../../../../python/tests/Stylus)

## Running the Stylus tests

```bash
python tools/Stylus/run_tests.py
```
