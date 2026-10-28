# Stylus

Stylus is Auctor's terminal-facing utility group: colors, TTY state, prompting and the spinner. It does not depend on Livy.

| Subsection | Purpose | Status |
|---|---|---|
| Colors | ANSI escape sequences and text styling | Implemented |
| Spinner | Background progress animation | Planned |
| Prompt | Interactive terminal prompting | Planned |
| TTY | Terminal-state detection | Planned |

Everything is importable from `Auctor.Stylus`; each subsection is its own subpackage (`Auctor.Stylus.Colors`).

## Colors

Colors provides the ANSI escape sequences used for terminal output and one helper that applies them.

### Package layout

| Module | Contents |
|---|---|
| `Auctor/Stylus/Colors/colors.py` | `Colors`, `Style()` |

`Colors` is the class and `Auctor.Stylus.Colors` is the subpackage. Import the class with `from Auctor.Stylus.Colors import Colors`.

### Constants

| Name | Sequence | Effect |
|---|---|---|
| `HEADER` | `\033[95m` | Bright magenta |
| `FAIL` | `\033[91m` | Bright red |
| `WARNING` | `\033[93m` | Bright yellow |
| `OKGREEN` | `\033[92m` | Bright green |
| `OKBLUE` | `\033[94m` | Bright blue |
| `OKCYAN` | `\033[96m` | Bright cyan |
| `OKYELLOW` | `\033[93m` | Bright yellow (same as `WARNING`) |
| `ENDC` | `\033[0m` | Reset all attributes |
| `BOLD` | `\033[1m` | Bold |
| `ITALICS` | `\033[3m` | Italic |
| `UNDERLINE` | `\033[4m` | Underline |

The values are plain strings and can be concatenated directly.

### Style

```python
from Auctor.Stylus.Colors import Colors, Style

print(Style("error: something failed", Colors.FAIL))
print(Style("combined", Colors.BOLD, Colors.OKCYAN))
```

- `Style(text, *codes)` returns the codes, then the text, then `ENDC`.
- With no codes the text is returned unchanged, without a reset.
- Empty text is still wrapped.
- Codes are not removed when the output is not a terminal. Detecting that is planned for TTY.

### Examples

| Example | Shows |
|---|---|
| @ref 01_palette.py "01_palette.py" | Every constant printed in its own color |
| @ref 02_style.py "02_style.py" | Wrapping text with `Style()` |

Sources are in `examples/python/stylus/colors/`.

### Tests

Tests live in `python/tests/Stylus/Colors/`. Run them with `python/scripts/Stylus/Colors/run_tests.bat` or `.sh`, or `python python/tools/Stylus/Colors/run_tests.py`. `python/tools/Stylus/run_tests.py` runs every Stylus subsection.
