import sys
from collections.abc import Sequence
from typing import TextIO


def _validate_options(options: Sequence[str]) -> tuple[str, ...]:
    if isinstance(options, str) or not options:
        raise ValueError("options must be a non-empty sequence of strings")
    result = tuple(options)
    if not all(isinstance(option, str) for option in result):
        raise ValueError("options must be a non-empty sequence of strings")
    return result


class Prompt:
    """Interactive terminal prompting.

    Cancelling (end of input or Ctrl-C) is an expected outcome, not an error: `ask` and
    `select` return `None` and `confirm` returns `False`.
    """

    def __init__(
        self,
        *,
        color: str = "",
        endc: str = "",
        stream: TextIO | None = None,
        input_stream: TextIO | None = None,
    ) -> None:
        self.color = color
        self.endc = endc
        self._stream = stream
        self._input_stream = input_stream

    # -- operations ----------------------------------------------------

    def ask(self, message: str, default: str | None = None) -> str | None:
        """Read one line. An empty answer returns `default`, or `""` without one."""
        suffix = f" [{default}]" if default else ""
        answer = self._read_line(f"{self._styled(message)}{suffix}: ")
        if answer is None:
            return None
        if answer == "" and default is not None:
            return default
        return answer

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask a yes/no question; an empty answer returns `default`, invalid ones re-prompt."""
        hint = "[Y/n]" if default else "[y/N]"
        text = f"{self._styled(message)} {hint}: "
        while True:
            answer = self._read_line(text)
            if answer is None:
                return False
            answer = answer.lower()
            if answer == "":
                return default
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            text = f"Please answer yes or no.\n{self._styled(message)} {hint}: "

    def select(self, message: str, options: Sequence[str], default: str | None = None) -> str | None:
        """Choose one option by number or by its text; invalid answers re-prompt.

        An empty answer returns `default` when given, otherwise re-prompts.
        """
        choices = _validate_options(options)
        if default is not None and default not in choices:
            raise ValueError("default must be one of the options")

        count = len(choices)
        hint = f" [{choices.index(default) + 1}]" if default is not None else ""
        prompt = f"Choose 1-{count}{hint}: "
        listing = [self._styled(message)] + [f"  {number}. {option}" for number, option in enumerate(choices, 1)]
        text = "\n".join(listing) + "\n" + prompt
        while True:
            answer = self._read_line(text)
            if answer is None:
                return None
            if answer == "" and default is not None:
                return default
            if answer.isdigit() and 1 <= int(answer) <= count:
                return choices[int(answer) - 1]
            for option in choices:
                if option.lower() == answer.lower():
                    return option
            text = f"Enter a number from 1 to {count}.\n{prompt}"

    # -- internals -----------------------------------------------------

    def _styled(self, text: str) -> str:
        return f"{self.color}{text}{self.endc}"

    def _read_line(self, text: str) -> str | None:
        """Write `text` and read one stripped line; `None` means the prompt was cancelled."""
        out = self._stream if self._stream is not None else sys.stdout
        source = self._input_stream if self._input_stream is not None else sys.stdin
        try:
            out.write(text)
            out.flush()
            line = source.readline()
        except (KeyboardInterrupt, EOFError, OSError, ValueError):  # Ctrl-C, closed or broken stream
            line = ""
        if line == "":
            try:
                out.write("\n")  # leave the cursor on a fresh line
                out.flush()
            except (OSError, ValueError):
                pass
            return None
        return line.strip()
