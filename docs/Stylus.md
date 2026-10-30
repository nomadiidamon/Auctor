# Stylus

Stylus is Auctor's terminal-facing utility group: colors, TTY state, prompting and the spinner. It does not depend on Livy.

| Subsection | Purpose | Status |
|---|---|---|
| Colors | ANSI escape sequences and text styling | Implemented |
| Spinner | Background progress animation | Implemented |
| Prompt | Interactive terminal prompting | Implemented |
| TTY | Terminal-state detection | Planned |

Everything is importable from `Auctor.Stylus`; each subsection is its own subpackage (`Auctor.Stylus.Colors`, `Auctor.Stylus.Spinner`, `Auctor.Stylus.Prompt`).

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
| @ref colors_01_palette.py "colors_01_palette.py" | Every constant printed in its own color |
| @ref colors_02_style.py "colors_02_style.py" | Wrapping text with `Style()` |

Sources are in `examples/python/stylus/colors/`.

### Tests

Tests live in `python/tests/Stylus/Colors/`. Run them with `python/scripts/Stylus/Colors/run_tests.bat` or `.sh`, or `python python/tools/Stylus/Colors/run_tests.py`. `python/tools/Stylus/run_tests.py` runs every Stylus subsection.

## Spinner

`Spinner` animates a progress indicator on a background thread. It can be stopped and restarted with its configuration kept, so a caller can pause it around other output.

### Package layout

| Module | Contents |
|---|---|
| `Auctor/Stylus/Spinner/spinner.py` | `Spinner`, `DEFAULT_FRAMES`, `format_elapsed()` |

`Spinner` is the class and `Auctor.Stylus.Spinner` is the subpackage. Import the class with `from Auctor.Stylus.Spinner import Spinner`.

### Construction

```python
Spinner(message="", *, interval=0.08, color="", endc="", frames=None,
        stop_frame=None, final_message=None, stream=None)
```

| Argument | Meaning |
|---|---|
| `message` | Text shown after the frame |
| `interval` | Seconds between frames; must be positive |
| `color`, `endc` | Escape sequences written before and after each line |
| `frames` | Sequence of strings to cycle through; defaults to `DEFAULT_FRAMES` (nine frames) |
| `stop_frame` | Frame left behind when the spinner stops; `None` leaves nothing |
| `final_message` | Message written when the spinner stops; may contain `{elapsed}` |
| `stream` | Output stream; defaults to `sys.stdout` at write time |

An empty `frames` sequence, a plain string, non-string entries or a non-positive `interval` raise `ValueError`.

### Lifecycle

```python
spinner.start()      # safe to call while running
spinner.update("x")  # change the message
spinner.is_running()
spinner.stop()       # safe when not running
```

- `stop()` waits for the worker thread, clears the line, then writes the stop frame and final message if configured.
- `stop()` on a spinner that is not running writes nothing, so the final line is never repeated.
- `with Spinner(...) as spinner:` starts on entry and stops on exit, including when an exception is raised. Exceptions propagate.
- Output is flushed on every write. A closed stream ends the animation without raising.

### Changing frames, stop frame and final message

`frames`, `stop_frame` and `final_message` are properties and can be set before or after `start()`. A running spinner uses new frames on its next tick; the stop frame and final message are read at the next `stop()`. Invalid values raise `ValueError` and leave the previous value in place.

### Final line and timer

When the spinner stops with a stop frame, a final message, or both, it writes them as one line (`<stop_frame> <message>`) in the configured color, followed by a newline.

- `stop(final_message)` overrides the configured message for that call only.
- `{elapsed}` in the message is replaced by the total time spun, for example `Done in 12.3s` or `Done in 1m 05s`. Other braces are left alone.
- `spinner.elapsed` is the time in seconds: live while running, frozen after `stop()`, and `0.0` before the first start.
- Each `start()` begins a new timer. `update()` does not affect it.

### Examples

| Example | Shows |
|---|---|
| @ref spinner_01_basic.py "spinner_01_basic.py" | Start and stop, repeated calls |
| @ref spinner_02_context.py "spinner_02_context.py" | Context manager and `update()` |
| @ref spinner_03_frames.py "spinner_03_frames.py" | Custom frames, changed before and during a run |
| @ref spinner_04_stop_frame.py "spinner_04_stop_frame.py" | A consistent final frame |
| @ref spinner_05_final_message.py "spinner_05_final_message.py" | Final message with elapsed time |
| @ref spinner_06_restart.py "spinner_06_restart.py" | Stopping around other output and restarting |

Sources are in `examples/python/stylus/spinner/`.

### Tests

Tests live in `python/tests/Stylus/Spinner/`. Run them with `python/scripts/Stylus/Spinner/run_tests.bat` or `.sh`, or `python python/tools/Stylus/Spinner/run_tests.py`.

## Prompt

`Prompt` asks questions on the terminal: free text, yes/no and a choice from a list. Cancelling is an expected outcome, never an exception.

### Package layout

| Module | Contents |
|---|---|
| `Auctor/Stylus/Prompt/prompt.py` | `Prompt` |

`Prompt` is the class and `Auctor.Stylus.Prompt` is the subpackage. Import the class with `from Auctor.Stylus.Prompt import Prompt`.

### Construction

```python
Prompt(*, color="", endc="", stream=None, input_stream=None)
```

| Argument | Meaning |
|---|---|
| `color`, `endc` | Escape sequences written before and after the question text |
| `stream` | Output stream; defaults to `sys.stdout` at call time |
| `input_stream` | Input stream read one line at a time; defaults to `sys.stdin` at call time |

Passing both streams makes a prompt scriptable, which is how the tests and examples run without a terminal.

### Operations

| Operation | Returns | Behaviour |
|---|---|---|
| `ask(message, default=None)` | `str` or `None` | Reads a line. An empty answer returns `default`, or `""` without one. |
| `confirm(message, default=False)` | `bool` | Accepts `y`, `yes`, `n`, `no` in any case. An empty answer returns `default`; anything else asks again. |
| `select(message, options, default=None)` | `str` or `None` | Lists the options numbered from 1. The answer is a number or the option text (any case). Invalid answers ask again; an empty answer returns `default`, or asks again without one. |

Answers are stripped of surrounding whitespace.

### Cancelling and errors

- End of input, Ctrl-C, or a closed or broken stream cancels the prompt: `ask` and `select` return `None`, and `confirm` returns `False` even when its default is `True`.
- A cancelled prompt writes a newline so the cursor is left on a fresh line.
- `select` raises `ValueError` for empty or non-string `options`, or a `default` that is not one of them. These are programming errors, not user input.

### Examples

| Example | Shows |
|---|---|
| @ref prompt_01_ask.py "prompt_01_ask.py" | Text input with and without a default |
| @ref prompt_02_confirm.py "prompt_02_confirm.py" | Yes/no questions and re-prompting |
| @ref prompt_03_select.py "prompt_03_select.py" | Choosing by number, by name, and by default |
| @ref prompt_04_cancel.py "prompt_04_cancel.py" | Cancelling with end of input |
| @ref prompt_05_styled.py "prompt_05_styled.py" | Colored questions |

Sources are in `examples/python/stylus/prompt/`. Examples script their answers through `input_stream` so they never wait on a terminal.

### Tests

Tests live in `python/tests/Stylus/Prompt/`. Run them with `python/scripts/Stylus/Prompt/run_tests.bat` or `.sh`, or `python python/tools/Stylus/Prompt/run_tests.py`.
